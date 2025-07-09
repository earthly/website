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

![System-Z, An Early Predecessor to Backstage]({{site.images}}{{page.slug}}/system-z.jpg)

By 2017, the growing usage and feature scope of System Z prompted a complete rewrite. This next-generation portal was dubbed **Backstage**. Internally, Backstage delivered notable improvements: a 55% decrease in new engineer onboarding time (measured by time to 10th pull request) and vastly improved developer productivity. By early 2020, 280+ engineering teams at Spotify were using Backstage to manage over 2,000 microservices, 300+ websites, 4,000 data pipelines, and 200 mobile features.

Seeing Backstage's internal success, Spotify leadership realized they had built something many large tech companies could use. So on March 16, 2020, Spotify announced Backstage's open-source release ￼- the company's first major open-source infrastructure platform. The announcement highlighted Backstage's vision: an "open platform for building developer portals" that allows engineers to focus on coding rather than wrangling disparate tooling.

Spotify had a clear roadmap for Backstage's open-source debut, broken into three phases:

1. an **extensible** **frontend** platform (consolidate all tools under one UX)
2. a **software catalog** to "manage your stuff" (services, components, pipelines, etc.), and
3. a vibrant **plugin ecosystem** contributed by the community.

Adoption came quickly. By September 2020, over 130 people had submitted contributions to the Backstage repo, with \~40% of pull requests coming from outside Spotify. Notable early adopters included Expedia, American Airlines and Netflix. That same month, Backstage was accepted as a CNCF Sandbox project.

![An initial release of Backstage in 2020]({{site.images}}{{page.slug}}/backstage-2020.png)
