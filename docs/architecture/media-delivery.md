# Media delivery (step videos and images)

Goal: media should appear as fast as text.

## Naming and lookup (Proposed)
Media belongs to **steps inside modules** (for example `cpr_adult.04`), not to each scenario. One clip serves every scenario
that uses the module, which reduces what you must produce. The full checklist is `media/replace.md` (sorted by how many
scenarios use each module) and the machine-readable list is `media/manifest.yaml`.
Before replying, the backend looks up the step. If a file exists the URL is returned with the step text, otherwise text only.

## Where to host (Open: your decision)
You asked for free hosting without limits. Nothing is free without limits. Facts checked on 2026-10-06:

| Option | Free allowance | Catch |
|---|---|---|
| **Supabase Storage (free plan)** | 1 GB file storage, 5 GB egress (plus 5 GB cached), 500 MB database | Free projects are **paused after 1 week of inactivity**. Stored chat images "forever" share the 1 GB. |
| **Cloudflare R2** | 10 GB storage, 1 million write-type and 10 million read-type operations per month, **no egress fees** | Not unlimited; above the free tier you pay about $0.015 per GB-month. Needs a Cloudflare account. |
| Supabase Pro | 100 GB storage, 250 GB egress | Paid ($25 per month plus usage). |

Suggested split (needs your confirmation): step media on R2 (large and read-heavy, free egress), user photos and data on Supabase.

## Ways to make it faster
Lowering quality does reduce load time, since time is roughly file size divided by connection speed and size follows bitrate.

1. Compress and right-size: H.264 MP4, 480p to 720p, about 1 to 2 Mbps, no audio unless needed, `faststart`. A 15-second clip at 1.5 Mbps is roughly 3 MB.
2. Short clips per step (10 to 20 seconds).
3. Images where video is not needed: WebP with a tiny blurred preview.
4. Looped muted MP4 instead of GIF.
5. Never proxy media through the backend: return URLs.
6. Send the media reference with the step text so the browser starts early.
7. Prefetch the next step's media while the user reads the current step.
8. CDN and caching: versioned filenames, long cache headers.
9. Region: Supabase project in Mumbai for users in India.
10. Offline cache: a service worker keeps the most critical clips.
11. Slow-connection fallback: lower rendition or an image.
12. Adaptive streaming (HLS): more work than short clips need.
