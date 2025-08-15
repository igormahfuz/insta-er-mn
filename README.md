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

- **Actor Price:** **$1.30 per 1,000 successfully analyzed profiles**.
- **Apify Platform Costs:** In addition to the Actor's price, you will also be charged for Apify platform usage costs (such as Residential Proxy usage and Compute Units).

You only pay for profiles that are successfully processed and return data. Profiles that result in an error after all retries are not counted towards the cost.

---

## 📥 Input

The Actor requires a JSON object with a list of Instagram usernames. You can also optionally adjust the concurrency level.

**Input Example:**

```json
{
  "usernames": [
    "apify",
    "instagram",
    "cristiano"
  ],
  "concurrency": 100
}
```

| Field         | Type             | Description                                                                                                 | Default |
|---------------|------------------|-----------------------------------------------------------------------------------------------------------|---------|
| `usernames`   | `Array<string>`  | **Required.** A list of Instagram profile usernames to be analyzed.                                       | `[]`    |
| `concurrency` | `Number`         | **Optional.** The number of profiles to process in parallel. Increasing this value speeds up the execution. | `100`   |

---

## 📤 Output

The Actor returns one result for each successfully analyzed profile.

**Output Example:**

```json
[{
  "username": "apify",
  "followers": 1633,
  "posts_analyzed": 12,
  "avg_engagement_score": 53,
  "engagement_rate_pct": 3.25,
  "biography": "Apify is a web scraping and automation platform that enables developers to build, deploy, and monitor web scrapers, data extractors, and web automation tools.",
  "business_email": "support@apify.com",
  "business_phone_number": "+1-800-555-1234",
  "error": null
}]
```

| Field                    | Type     | Description                                                                 |
|--------------------------|----------|---------------------------------------------------------------------------|
| `username`               | `String` | The username of the analyzed profile.                                       |
| `followers`              | `Number` | The total number of followers for the profile.                              |
| `posts_analyzed`         | `Number` | The number of recent posts analyzed (up to 12).                           |
| `avg_engagement_score`   | `Number` | The average number of interactions (likes + comments + views) per post.     |
| `engagement_rate_pct`    | `Number` | The engagement rate as a percentage. `(avg_engagement_score / followers) * 100` |
| `biography`              | `String` | The user's profile biography, if available.                                 |
| `business_email`         | `String` | The user's public business email, if available.                             |
| `business_phone_number`  | `String` | The user's public business phone number, if available.                      |
| `error`                  | `String` | If an error occurs, this field will contain the description. Otherwise, it will be `null`. |

---

## ⚠️ Disclaimer

This Actor is not an official product of Instagram. It was developed independently to extract public data. Use it responsibly and in compliance with the terms of service of both Apify and Instagram.
