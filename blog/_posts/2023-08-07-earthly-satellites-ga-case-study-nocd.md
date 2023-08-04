---
title: "How NOCD Reduced Build Times by 9x with Earthly and Earthly Cloud"
categories:
  - News
toc: true
author: Gavin

internal-links:
 - just an example
excerpt: |
    Learn how NOCD, a leading telehealth provider, reduced their CI build times by 9x using Earthly and Earthly Cloud.
---

![NOCD Logo]({{site.images}}{{page.slug}}/nocd.png)\

## Highlights

* [NOCD](https://www.treatmyocd.com/) struggled with long build times and latency in their CI builds due to a lack of caching and, after caching was implemented with Earthly, slow cache downloads and uploads.
* They implemented Earthly and Earthly Satellites. Earthly's automatic caching sped up builds, and Earthly Satellites’ instantly available cache eliminated latency in their CI caused by cache downloads and uploads.
* The combined implementation of Earthly and Earthly Satellites resulted in a 9x speed increase in CI builds, reducing build times from 45 minutes to just 5 minutes.

## Results

* **9x faster builds in CI**
* **Build Time Reduction: 45min -> 20min** (by implementing Earthly w/ Semaphore)
* **Build Time Reduction: 20min -> 5min** (by implementing Earthly + Earthly Satellites w/ Semaphore)

> “It was love at first sight switching over to Satellites. It was the same kind of case as switching to Earthly for us. Switching to Earthly took us from 45 minutes to 20 minutes, and using Satellites took us from like 20 minutes to 4 or 5 on average. It’s been another 2x increase, literally just from using Satellites. It’s been astounding.” - Ses Goe, Director of Internal Tools at NOCD

## Customer Profile

NOCD is the #1 telehealth provider for the treatment of obsessive-compulsive disorder (OCD). It creates access to online therapy for people with OCD through its telehealth platform. Members can access and schedule live, face-to-face video therapy sessions with licensed therapists that specialize in exposure and response prevention therapy (ERP) - considered the "gold standard" in OCD treatment. In between sessions, patients have access to 24/7 support through NOCD’s self-help tools and peer communities.

Earthly was introduced to NOCD through its internal tooling team. One of that team’s most significant responsibilities involves building and deploying the core Docker images used in their customer-facing services. NOCD primarily writes its software in Python, uses Semaphor for CI (previously used GitHub Actions), and deploys to AWS.

## Challenge: Long build times due to lack of caching

Before implementing Earthly, NOCD faced issues with long build times, driven heavily by the installation of Python dependencies for their Docker image builds. Their Python dependencies rarely changed, which meant that the time taken to download these dependencies was almost always duplicative and wasted.

> “We primarily used GitHub Actions with plain old Docker. And builds were notoriously really, really, really, really slow. It was not uncommon to have our CI/CD pipeline take an hour to run all the way through. Especially when we were running our full integration test suite. It just took absolutely forever. A large percentage of that was the fact that our Docker images weren’t cached in any meaningful way. So everything was being rebuilt from scratch over and over and over, and it just slowed everything down.” - Ses Goe, Director of Internal Tools at NOCD

### Solution: Earthly’s automatic caching

Earthly’s caching functionality addressed this challenge. It automatically identifies parts of the build that haven’t changed since the last successful execution, like Python dependencies, and stores them for future use. When a new build is initiated, Earthly reuses the cached elements instead of rebuilding them, which dramatically speeds up the build process.

> “It took literally just going from Dockerfile to Earthfile to bring build times from 45-ish minutes down to probably 15 or 20, just from skipping the 25 minutes of installing Python dependencies. That was enough for us to use Earthly from that point forward.” - Ses Goe, Director of Internal Tools at NOCD

## Challenge: Build latency in CI from cache download and upload

NOCD moved off GitHub Actions to Semaphor for their CI, Earthly for their builds, and AWS for inline caching. This proved significantly faster than when they were using GitHub Actions alone. Unfortunately, downloading the cache from AWS to Semaphore and vice versa became the new primary contributor to latency in their CI builds.

> “I tuned our CI/CD performance as much as I could, but the vast majority of our build time was still spent downloading the Docker image and its cache before actually running anything, because our image ends up being 1.5GB, or something like that, after being fully built. It’s pretty big.” - Ses Goe, Director of Internal Tools at NOCD

### Solution: Earthly Satellites’ instantly available cache

Earthly Satellites provided a solution to NOCD's CI latency issues by storing build caches close to the build execution, directly on the satellite. This reduced build times by eliminating the cache download to and upload from AWS that was required on every CI run with their previous inline caching solution.

> “Satellites took us from like 20 minutes to 4 or 5 on average. It’s been another 2x increase, literally just from using Satellites. It’s been astounding.” - Ses Goe, Director of Internal Tools at NOCD

## Why Earthly

NOCD chose Earthly and Earthly Cloud over their prior solution and other alternatives for a few key reasons:
1. **Automatic Caching:** Earthly provides an efficient caching mechanism that significantly reduced build times for NOCD with no extra configuration required.
2. **Reduced Latency in CI:** Earthly Satellites eliminated the cache download to and upload from AWS that was required on every CI run with their previous inline caching solution and was the primary source of their CI latency issues.
3. **Flexibility and Ease of Integration:** Earthly fit seamlessly into NOCD's existing workflows. They were able to utilize Earthly with both their old CI – GitHub Actions – as well as through their transition to their current CI – Semaphore,  and they now use Earthly Satellites with Semaphore as well.
4. **Simplicity and Stability:** Earthly provided a straightforward and reliable solution with little required maintenance. NOCD’s Earthfiles often don’t change for 6 months or longer.

> “Every time I have a conversation with an Earthly employee, it’s like you guys are just headed for the moon, man. There’s so much opportunity for improvement, and you guys are building around all the primitives of BuildKit itself. So for any further cache improvements you come up with, it’s just gonna benefit everybody. It’s super cool to see.” - Ses Goe, Director of Internal Tools at NOCD

{% include_html cta/bottom-cta.html %}
