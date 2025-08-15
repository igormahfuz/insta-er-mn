"""
Actor que calcula Engagement Rate (ER) de perfis públicos do Instagram.

• Não requer login nem cookies.
• Usa endpoint público `https://i.instagram.com/api/v1/users/web_profile_info/?username=<user>`
  (header X-IG-App-ID).
• Para cada perfil: pega seguidores + 12 posts → soma likes+comments → ER%.
• Grava cada linha no dataset e exibe progresso via log + set_status_message.
"""

from __future__ import annotations
from apify import Actor
import httpx
import math
import asyncio
import importlib.metadata

IG_ENDPOINT = (
    "https://i.instagram.com/api/v1/users/web_profile_info/"
    "?username={username}"
)

HEADERS = {
    "x-ig-app-id": "936619743392459",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
}

# --- Função de Lógica Principal (sem modificação) ---

async def fetch_profile(client: httpx.AsyncClient, username: str) -> dict:
    url = IG_ENDPOINT.format(username=username)
    try:
        r = await client.get(url, headers=HEADERS, follow_redirects=True, timeout=30)
        r.raise_for_status()
        data = r.json().get("data", {}).get("user")
        if not data:
            return {"username": username, "error": "perfil inexistente/privado"}

        followers = data.get("edge_followed_by", {}).get("count", 0)
        following = data.get("edge_follow", {}).get("count", 0)
        
        edges = data.get("edge_owner_to_timeline_media", {}).get("edges", [])[:12]

        total_likes = 0
        total_comments = 0
        total_video_views = 0
        video_post_count = 0
        recent_posts = []

        for edge in edges:
            node = edge.get("node", {})
            likes = node.get("edge_liked_by", {}).get("count", 0)
            comments = node.get("edge_media_to_comment", {}).get("count", 0)
            video_views = node.get("video_view_count", 0) if node.get('is_video') else None

            total_likes += likes
            total_comments += comments
            if video_views is not None:
                total_video_views += video_views
                video_post_count += 1

            post_details = {
                "url": f"https://www.instagram.com/p/{node.get('shortcode')}/",
                "likes": likes,
                "comments": comments,
                "video_views": video_views,
                "caption": node.get("edge_media_to_caption", {}).get("edges", [{}])[0].get("node", {}).get("text", ""),
                "thumbnail_src": node.get("thumbnail_src"),
            }
            recent_posts.append(post_details)

        n_posts = max(len(edges), 1)
        avg_likes = total_likes / n_posts
        avg_comments = total_comments / n_posts
        avg_video_views = total_video_views / video_post_count if video_post_count > 0 else 0

        total_engagement_score = total_likes + total_comments + total_video_views
        avg_engagement_score = total_engagement_score / n_posts
        er = (avg_engagement_score / followers) * 100 if followers else 0

        return {
            "username": username,
            "followers": followers,
            "following": following,
            "profile_pic_url_hd": data.get("profile_pic_url_hd"),
            "biography": data.get("biography"),
            "external_url": data.get("external_url"),
            "business_email": data.get("business_email"),
            "business_phone_number": data.get("business_phone_number"),
            "category_name": data.get("category_name"),
            "posts_analyzed": n_posts,
            "avg_likes": math.floor(avg_likes),
            "avg_comments": math.floor(avg_comments),
            "avg_video_views": math.floor(avg_video_views),
            "engagement_rate_pct": round(er, 2),
            "recent_posts": recent_posts,
            "error": None,
        }
    except Exception as e:
        raise e

# --- Wrapper com Retentativas (sem modificação) ---

async def fetch_with_retries(username: str, proxy_config) -> dict:
    MAX_RETRIES = 3
    BASE_DELAY_SECONDS = 2
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            session_id = f'session_{username}_{attempt}'
            proxy_url = await proxy_config.new_url(session_id=session_id)
            transport = httpx.AsyncHTTPTransport(proxy=proxy_url)
            async with httpx.AsyncClient(transport=transport) as client:
                return await fetch_profile(client, username)
        except (httpx.HTTPStatusError, httpx.ProxyError, httpx.ReadTimeout) as e:
            last_error = e
            Actor.log.warning(f"Tentativa {attempt + 1}/{MAX_RETRIES} falhou para '{username}': {type(e).__name__}. Retentando...")
            delay = BASE_DELAY_SECONDS * (2 ** attempt)
            await asyncio.sleep(delay)
        except Exception as e:
            return {"username": username, "error": f"Erro inesperado: {type(e).__name__}: {e}"}

    return {"username": username, "error": f"Falha após {MAX_RETRIES} tentativas: {type(last_error).__name__}"}

# --- Função de Processamento Otimizada para PPR ---

async def process_and_save_username(
    username: str,
    proxy_config,
    semaphore: asyncio.Semaphore
) -> dict:
    async with semaphore:
        result = await fetch_with_retries(username, proxy_config)
        
        # **MELHOR PRÁTICA PARA PPR:**
        # Apenas envie para o dataset (e conte como resultado) se não houver erro.
        if result.get("error") is None:
            await Actor.push_data(result)
        
        return result

# --- Função Principal (sem modificação) ---

async def main() -> None:
    async with Actor:
        Actor.log.info(f"httpx version: {importlib.metadata.version('httpx')}")

        inp = await Actor.get_input() or {}
        usernames: list[str] = inp.get("usernames", [])
        concurrency = inp.get("concurrency", 100)

        if not usernames:
            raise ValueError("Input 'usernames' (uma lista de perfis) é obrigatório.")

        semaphore = asyncio.Semaphore(concurrency)
        proxy_configuration = await Actor.create_proxy_configuration()
        
        total_usernames = len(usernames)
        processed_count = 0
        
        Actor.log.info(f"Iniciando processamento de {total_usernames} usernames com concorrência de {concurrency}.")

        tasks = []
        for username in usernames:
            clean_username = username.strip("@ ")
            if not clean_username:
                total_usernames -= 1
                continue
            
            task = process_and_save_username(clean_username, proxy_configuration, semaphore)
            tasks.append(task)

        for future in asyncio.as_completed(tasks):
            result = await future
            processed_count += 1
            
            username_processed = result.get('username', 'N/A')
            msg = f"{processed_count}/{total_usernames} → {username_processed}"
            
            if result.get("error"):
                msg += f" ❌ ({result['error']})"
            else:
                msg += " ✔"
            
            Actor.log.info(msg)
            await Actor.set_status_message(msg)
        
        Actor.log.info("Processamento concluído.")
