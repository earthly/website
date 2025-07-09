---
title: "Backstage Is at the Peak of Its Hype"
categories:
  - news
toc: true
author: Vlad
topic: earthly
funnel: 3
topcta: false
excerpt: |
   A look behind the portal everyone's building - and the hard truths most discover too late.
last_modified_at: 2025-06-10
---
A look behind the portal everyone's building - and the hard truths most discover too late.

<!-- vale HouseStyle.Spacing = NO -->
<div class="notice--info">
**TL;DR:**

* In 2020, Spotify open-sourced Backstage - a slick internal developer portal that promised to tame microservices chaos and boost productivity. Since then, it's been adopted by Netflix, Lyft, Twilio and dozens of other giants. The CNCF backed it. Vendors jumped in. The hype grew.
* But now, five years in, the story is starting to shift. Behind every polished demo is a platform team buried in custom code, and the ROI is unclear.
* So what's really going on with Backstage, and why are so many teams quietly struggling to make it work? Can we fix that?

</div>

By 2014, Spotify had over 100 engineers and was spinning up new microservices weekly, leading to service sprawl, duplicated efforts, and poor visibility into ownership. In response, a platform team created an internal microservices catalog called System Z. \[[Source](https://newsletter.pragmaticengineer.com/p/backstage)\] System Z let teams register services with metadata (code links, owners, etc.), and later model relationships between components, organizing services into cohesive systems.

![]({{site.images}}{{page.slug}}/system-z.jpg)
