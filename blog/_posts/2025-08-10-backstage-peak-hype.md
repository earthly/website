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

In March 2022, Backstage 1.0 was released, and CNCF promoted the project to Incubation status.

What followed was a massive uptick in adoption. Within just a few years of open-sourcing, some of the largest engineering orgs had adopted Backstage with enthusiasm. Yelp, Twilio, Lyft, Box, VMware, LinkedIn, AirBnB, Epic Games, AWS, Splunk and many others were jumping on the bandwagon.

Meanwhile, a growing ecosystem of vendors emerged. Spotify introduced [SoundCheck](https://backstage.spotify.com/partners/spotify/plugin/soundcheck/), a paid scorecarding plugin, while others like Cortex and OpsLevel began innovating in the broader IDP space beyond Backstage.

![Source \[2020\]\(https://backstage.io/blog/2020/03/16/announcing-backstage/\)]({{site.images}}{{page.slug}}/backstage-adoption-trend.png)

But as adoption surged, so did the realization: running Backstage in the real world is nothing like the demo.

## The Hidden Cost of Adoption

While many companies are eager to adopt Backstage, those a year or two in are starting to realize just how hard it is to maintain \- and even harder to make successful. Reddit user [u/hcaandrade2](https://www.reddit.com/user/hcaandrade2/) put it [best](https://www.reddit.com/r/devops/comments/1kgfqys/comment/mqyvwdm/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button):

![Backstage is a "free" IDP in the same way you would get a "free" car if some dumped all the parts of a Chevy on your desk and said "congratulations, here's your free ride."]({{site.images}}{{page.slug}}/backstage-reddit.png)

Backstage seems like a sleek developer portal out of the box. What you actually get is a skeleton and a long, expensive journey of internal platform engineering.

Here are some of the most common pitfalls teams encounter when adopting Backstage:

### 1. Overwhelming DIY

As part of my effort to understand the Backstage ecosystem better, I spoke with several users about their adoption journey.

One consistent theme stood out: everyone invests heavily in DIY solutions on top of Backstage. Whether it's integrating better catalog data, enabling use cases not covered by community plugins, or adapting to their unique engineering processes - the teams I spoke to ended up building custom plugins or modifying official ones.

In fact, I didn't meet a single company that hadn't built at least one internal plugin tailored to their unique setup.

A big takeaway from all this is that plugin development is not optional. It's table stakes. But most teams don't realize that until they're already knee-deep. The required investment, and the headcount, is non-trivial. It's never a one-person job. While a two-person team might hold the line in some orgs, it's usually 4+, and often 15+ at scale.

Worse still, you're looking for engineers who blend a mix of DevOps, Platform skills, and React JS. The talent for this overlap is scarce, and you'll need to pay top dollar for the uniqueness of the background.

Another commonly overlooked challenge is managing, discovering, and evolving the use cases the platform needs to support. Success depends on a tight feedback loop between plugin authors and internal users - gathering requirements, writing user stories, testing mockups, and refining UX specs. Because UI is involved, it quickly becomes intricate work, with many stakeholders to satisfy: engineers, managers, SREs, security teams, and more. Ideally, this work is led by a technical product manager (TPM). But most companies don't staff one for Backstage - so features get built but go unused, while real needs go unaddressed. Another common failure mode is poor UX decisions that never get user-tested, leading to frustrating experiences that kill adoption at scale.

The need for a TPM yet again highlights the sheer amount of human capital required to pull off a successful Backstage installation.

Finally, DIY work tends to break when Backstage gets updated - especially if you've strayed too far from upstream patterns. The advice we heard from companies getting burnt by this is that you should try to not go against the design choices of Backstage, and try to limit any hacks as much as possible - because those hacks may no longer work later. And no, abandoning upstream altogether is not a great solution, because that would mean your internal platform would stagnate in momentum. It'll get very difficult to add other community plugins on top later.

### 2. Limited Adoption

The next big problem of typical Backstage installations is that the adoption level is very low. While Spotify internally claims to have achieved 99% voluntary adoption, most organizations get stuck at about 10% [Source].

These aren't early experiments. These are mature teams, often with 4–5 custom plugins and 10+ engineers behind them, still struggling to drive meaningful adoption. Imagine sinking so much effort into this great platform that ends up being largely unused at the end of the day.

Most companies try to fix this the wrong way: by building even more features, hoping dev teams will adopt the platform if they just find "the right one". I don't know about you, but I have seen this movie too many times in the startup world: a failing startup isn't taking off and they just endlessly build even more stuff nobody needs in hopes that "we're just missing this one feature". No. It's either a distribution problem or a product-market-fit problem and it needs to be treated as such. It's not a "needs more bells-and-whistels" problem. And no, "build it and they will come" is never the right answer.

### 3. Catalogs Rot Fast

Another common issue: catalog data rots quickly. People leave. Teams reshuffle. Ownership records go out of date. The worst part about this is that you learn about it in a post-mortem. An SRE scrambles to reach the owner during an incident - no one picks up. MTTR tanks.

### 4. Scaffolding Only Works for Greenfield

Scaffolding promises standardization. If every service had the same CI/CD setup, life would be easier. Right?

But the reality is that the most critical apps are the oldest and messiest. You're not migrating that to a new dev setup. It's like doing surgery on a sprinting patient. App teams have their own goals and milestones and they don't have time for your rip-and-replace infrastructure project that gives them very little in return.

### 5. Scorecards are Super Limited

I wrote previously about the limitations of scorecards. In summary: most scorecards are 💩. They promise a lot, but in reality they provide very little insight into key development practices in code and in CI/CD. In addition, they have no way to shift to the left to provide the feedback in context, in PRs. The feedback lives in a dashboard no one checks.

![Traditional scorecards are just the tip of the iceberg]({{site.images}}{{page.slug}}/scorecards-miss.png)

## Limited ROI

Zoom out, and the pattern is clear: Backstage is expensive to implement, and even harder to make stick. The technical lift is high, the organizational cost is even higher, and the payoff, more often than not, just doesn't materialize. DIY piles up. Adoption stalls. Catalogs rot. And scorecards turn into a dashboard of guilt that nobody looks at.

The result is a beautiful portal, used by 10% of the company. It's because of all these points that I fear that Backstage may see tremendous churn over the next few years.

## But It Doesn't Have to Be That Way

Backstage isn't going away \- nor should it. It's a powerful foundation. But the next chapter for most organizations isn't about building more plugins. It's about making the investment finally pay off.

Here's what that might look like:

1. **Fix the adoption bottleneck**. Backstage only creates value when enough teams are onboarded. But adoption doesn't have to be all-or-nothing.

   A smart next step can be to start nudging adoption from the places developers already work \- like the PR workflow. If a service is missing catalog metadata, show a friendly warning in the pull request. If it violates a security baseline, surface that inline.

   These nudges don't block progress \- they raise awareness. And because they're delivered in the right context (not in a dashboard nobody checks), they're far more likely to result in action. Over time, this creates a self-reinforcing loop \- no top-down mandates required.
2. **Use Backstage to drive real engineering alignment**. The catalog should evolve from being a passive registry to an active system of record for engineering health. That means embedding signals directly into it:

   * Which of my 20,000 repos are production-related?
   * Are those services adhering to organizational standards?
   * Did all services apply the mitigation that resulted from that big post-mortem last month?
   * Are we covered against that vulnerability that came out recently in the industry?
   * Is everyone using the provided CI/CD templates correctly?
   * Are services tested and scanned according to compliance standards?
   * How far along is that high-priority migration initiative we launched last quarter?

Backstage can become the lens through which leadership sees engineering maturity at a glance. Not a vanity scorecard, but a dynamic map of what's production-ready, what's at risk, and where to invest. That's when Backstage becomes indispensable.

Backstage isn't the problem. But its success hinges on how it's used, and whether it's integrated into the day-to-day flow of engineering, not just maintained on the sidelines by a heroic platform team.

If this is the kind of platform problem you want to tackle, where developer experience meets governance and engineering culture, [**we're hiring**](https://jobs.earthly.dev/). We want to turn Backstage from a static registry into a real-time, policy-aware visibility layer by plugging directly into code, CI/CD, and PR workflows. We're answering the questions no plugin or scorecard can.
