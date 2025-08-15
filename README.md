# Instagram Engagement Rate Calculator

This Apify Actor calculates the engagement rate of any public Instagram profile quickly and efficiently. It does not require a login or cookies, using the platform's public endpoint to extract the data.

The Actor is designed to be robust and scalable, making it ideal for analyzing large lists of profiles for market research, influencer analysis, and competitive studies.

## ✨ Features

- **No Login Required:** Does not require your Instagram credentials.
- **Analyzes Last 12 Posts:** Provides a recent and relevant overview of engagement.
- **Comprehensive Engagement Metric:** The calculation includes likes, comments, and, for videos, view counts.
- **High Speed:** Processes hundreds of profiles simultaneously with configurable concurrency.
- **Robust and Reliable:** Uses the Apify residential proxy network and implements an automatic retry system to handle network errors.
- **Monetization-Ready:** Optimized for the Pay-per-result (PPR) model.

---

## 💰 Cost of Usage & Monetization

This Actor is monetized using the **Pay-per-result (PPR)** model.

- **Actor Price:** **$0.50 per 1,000 successfully analyzed profiles**.
- **Apify Platform Costs:** In addition to the Actor's price, you will also be charged for Apify platform usage costs (such as Residential Proxy usage and Compute Units).

You only pay for profiles that are successfully processed and return data. Profiles that result in an error after all retries are not counted towards the cost.

---

## 📥 Input

The Actor requires a list of Instagram usernames and allows you to configure the proxy settings and concurrency.

**Input Example:**

```json
{
  "usernames": [
    "apify",
    "instagram"
  ],
  "concurrency": 50,
  "proxyGroup": "RESIDENTIAL"
}
```

| Field         | Type             | Description                                                                                                                                                           | Default       |
|---------------|------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------|
| `usernames`   | `Array<string>`  | **Required.** A list of Instagram profile usernames to be analyzed.                                                                                                   | `[]`          |
| `concurrency` | `Number`         | **Optional.** The number of profiles to process in parallel. A lower number is slower but less likely to be blocked.                                                  | `50`          |
| `proxyGroup`  | `String`         | **Optional.** The name of the Apify proxy group to use. To find your available group names, go to the Proxy section in your Apify dashboard. To disable proxies, enter `NONE`. | `RESIDENTIAL` |

---

## 📤 Output

The Actor returns one result for each successfully analyzed profile, containing detailed information.

**Output Example:**

```json
[{
  "username": "apify",
  "followers": 1633,
  "following": 12,
  "profile_pic_url_hd": "https://...",
  "biography": "Apify is a web scraping and automation platform...",
  "external_url": "https://apify.com",
  "business_email": "support@apify.com",
  "business_phone_number": null,
  "category_name": "Technology Company",
  "posts_analyzed": 12,
  "avg_likes": 45,
  "avg_comments": 8,
  "avg_video_views": 0,
  "engagement_rate_pct": 3.25,
  "recent_posts": [
    {
      "url": "https://www.instagram.com/p/Cxyz.../",
      "likes": 50,
      "comments": 10,
      "video_views": null,
      "caption": "Check out our new feature!",
      "thumbnail_src": "https://..."
    }
  ],
  "error": null
}]
```

| Field                    | Type     | Description                                                                 |
|--------------------------|----------|---------------------------------------------------------------------------|
| `username`               | `String` | The username of the analyzed profile.                                       |
| `followers`              | `Number` | The total number of followers for the profile.                              |
| `following`              | `Number` | The total number of accounts the profile is following.                      |
| `profile_pic_url_hd`     | `String` | URL to the high-definition profile picture.                                 |
| `biography`              | `String` | The user's profile biography, if available.                                 |
| `external_url`           | `String` | The external website link from the bio, if available.                       |
| `business_email`         | `String` | The user's public business email, if available.                             |
| `business_phone_number`  | `String` | The user's public business phone number, if available.                      |
| `category_name`          | `String` | The category of the profile (e.g., "Technology Company").                 |
| `posts_analyzed`         | `Number` | The number of recent posts analyzed (up to 12).                           |
| `avg_likes`              | `Number` | The average number of likes per post.                                       |
| `avg_comments`           | `Number` | The average number of comments per post.                                    |
| `avg_video_views`        | `Number` | The average number of views for video posts.                                |
| `engagement_rate_pct`    | `Number` | The engagement rate as a percentage. `(avg_engagement_score / followers) * 100` |
| `recent_posts`           | `Array`  | A list containing details of the last 12 posts.                             |
| `error`                  | `String` | If an error occurs, this field will contain the description. Otherwise, it will be `null`. |

---

## ⚠️ Disclaimer

This Actor is not an official product of Instagram. It was developed independently to extract public data. Use it responsibly and in compliance with the terms of service of both Apify and Instagram.
