---
title: "Three Ways to Do Developer Experience (DX)"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - dx
 - developer experience
excerpt: |
    Learn about the importance of Developer Experience (DX) and how it can impact different roles within an organization. Discover how Alice, Bob, and Carlos each prioritize DX in their respective roles as a Product Manager, Internal Tools Lead, and Director of Engineering, and how it has transformed their products, improved team collaboration, and accelerated development.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler. It's a nifty tool that could help enhance your team's DX. [Give it a shot](/).**

Developer Experience is the User Experience of a Developer. Developer Experience Design (DX) is User Experience Design (UX Design), the work of improving a user's experience with a product where the user is a developer.

## Who Should Care About Developer Experience?

Okay, now we have a definition, but sometimes definitions aren't enough. Who should care about DX? Why does it matter at all? To answer those questions, let's skip definitions and consider three different scenarios where DX plays a vital role.

<div class="align-right">
![An important moment in DX.]({{site.images}}{{page.slug}}/9740.png)
</div>

Three broad groups of people might care about developer experience, and because of the variance in their jobs, how they think about DX might be wildly different. Let's call these people Alice, Bob, and Carlos.

## DX Awakening

### Alice - Product-Based Developer Experience

<div class="align-left">
  <img src="{{site.images}}{{page.slug}}/0590.png" width="200" height="200" />
  <figcaption>Alice - Product Manager</figcaption>
</div>

Alice is a Product Manager at Request Express, a developer tool for API development. Developer experience is critical for her because Request Express's customers are all developers.

To her, everything you need to know about Developer Experience can be traced back to Stripe. Stripe is a whole successful billion-dollar company based on the observation that the developer experience for payment processing was horrible and they could do better.

Alice raves about how easy Stripe is to work with. She looks to Stripe as a model to emulate for elements like clear documentation, reusable code samples, and a straightforward onboarding process. Stripe helped demonstrate to the industry how valuable investing in developer experience can be.

Alice has modeled some of Request Express's newest features after Stripe's developer-centric approach. She led her team to create interactive documentation with embedded code samples inspired by Stripe's docs. And she led a redesign of Request Express's onboarding flow to simplify the initial integration steps that had been pain points for developers.

### Bob - Internal Platform Developer Experience

<div class="align-right">
  <img src="{{site.images}}{{page.slug}}/0970.png" width="200" height="200" />
  <figcaption>Bob - Internal Tools Lead</figcaption>
</div>

Bob is a Staff Software Engineer at Shop-O-Rama. He works on internal tools and platforms used by Shop-o-rama's engineering teams. Optimizing developer experience for these internal tools helps Bob's colleagues be more productive.

For Bob, his DX awakening centered around failure. His team built an internal dashboard system at Shop-o-rama called 'Dash-forge'. To Bob, it was a powerful system for aggregating and visualizing key performance and usability data. He thought it would be a huge enabler, but no one used it without intense arm-twisting.

In the past, he had seen top-down mandates to standardize on some internal tools cause unneeded friction. Developers were forced to use tools they hated – that didn't make sense for what they were doing – because somebody important misunderstood what was needed. He knew that wasn't the way. So instead, he started acting more like a product manager, treating the internal tools and APIs they were building as a proper product with other teams as customers.

He found that his product solved a genuine problem, but no one could use it. Or at least the usability was bad enough to outweigh any potential benefits.

For Bob, DX is about being selective. He doesn't have the resources of a developer tools company, but he can ensure he's building with DX in mind. Now he treats documentation, user testing, and support as part of the product development process.

### Carlos - Organizational Developer Experience

<div class="align-left">
  <img src="{{site.images}}{{page.slug}}/1020.png" width="200" height="200" />
  <figcaption>Carlos - Director of Engineering</figcaption>
</div>

Carlos is the Director of Engineering at a fast-growing ML startup. Carlos faces onboarding and team productivity challenges as the engineering team has rapidly expanded from 10 to 100 developers.

The quick hiring has led to challenges in adequately training new developers. Providing them with the necessary environment, tools, and documentation to start contributing quickly has become a challenge. Things are slowing down right when they need to speed up.

The ballooning team size has also introduced friction into development workflows. With more developers working across codebases and components, visibility is lacking, leading to duplicated work. For Carlos, it's clear that a team empowered to improve developer experience across the board is essential if this startup plans to keep growing.

## DX Metrics

So for Alice, Bob, and Carlos, the tactics employed to improve the developer experience will vary. But for all, the focus will be on improving the journey that a developer has interacting with an organization's code, tools, and resources. Every touch-point with the developer is an experience; it's just the focal point for Alice, Bob, and Carlos is very different.

For Alice, DX might focus on these key elements of her company's API and CLI tool:

* **Intuitive, well-documented APIs**. Easy discovery of API contracts.
* **Helper libraries** and sample code accelerate building.
* **Extensive and intuitive documentation**
* **Excellent technical support** resources like chat and issue tracking, community management, and support.
* **Dashboards** to provide visibility into API usage, performance, and errors.
* **Release notes**, deprecation schedules, and migration guides help developers stay current with the product.

For Alice, key metrics to watch might include:

* **Onboarding Duration** - How long it takes new developers to use her product successfully.
* **Documentation Hit Rate / Findability**: This is how developers find and access documentation.
* **Support Ticket Frequency**: How often do developers need to contact you for help?

Carlos doesn't have the luxury of focusing on just one tool - he has to think of the whole experience of developers at his company. Key elements of DX for him include:

* **Standardizing tools and technologies** to reduce complexity. This minimizes the learning burden as developers learn new systems.
* **Good collaboration practices** via knowledge-sharing platforms and open communication to prevent duplicate efforts.
* **Documentation** of key procedures and processes to help with onboarding
* **Continuous delivery pipelines** and test automation so developers can ship faster with confidence.

For Carlos, key metrics to measure might include:

* **Onboarding Duration** - How long it takes new developers to make their first successful code contribution.
* **Time To First Commit** - Time from cloning repo to having a local commit ready. Includes time for getting dependencies, setting up the environment, and making a superficial change.
* **Build Time** - The time required to complete a code build in CI. Includes build queue wait time, if any.
* **PR Turn Around Time**: The total duration from submitting a PR until it's finally approved.

Bob's concerns are somewhere between Carlo's and Alice's. He only needs to worry about developers in his Org, like Carlos, and only about the tools he owns, like Alice.

Regardless of the use case, though, there is no perfect metric for measuring DX improvements. Instead, whether your situation is closer to Alice, Bob, or Carlos, you should center your efforts around developer satisfaction and frustration. The least scalable but highest payoff way to do this is field testing.

## Field Testing

Field testing involves observing developers interacting with your tools, libraries, APIs, or frameworks in their natural working environment. The goal is to understand how they use these resources in real-world scenarios, what difficulties they encounter, and how they solve problems or create workarounds.

Alice at Request Express has the most rigorous field testing process, but even so, the process is relatively simple. Alice recruits developers who've never used her product before.

( She originally started with just a few friends from a former company, but as time's gone on, she's moved on to friends of colleagues and even lately to a local coding bootcamp graduating class. )  

Each volunteer gets on a video call with Alice and is given a task to complete using their chosen development environment. The task is always some variation of working through Request Express's onboarding tutorial.

## Field Testing Analysis

The first field test Alice did is hard to forget. The user was confused and lost at step one of the tutorial. He would have never even made it to step two without a nudge from her. That testing led to some tutorial changes and error message cleanup, and then field testing started flowing more smoothly.

For Alice, analysis of the field testing results is never a challenge. A new point of confusion, a missing usage pattern, or just a rough edge is found by every new volunteer. The hundred-dollar gift cards she hands out at the end are the best money her company has ever spent.

## Internal Field Testing

Bob's approach to field testing has been different. He temporarily joined a team looking to use Dash-forge and did the integration himself. It went badly, and for every papercut or roadblock he hit, he documented it and got his team to prioritize a resolution.

The integration after that, he paired with the dev doing the integration whenever he could but generally took a less active role. But again he identified a series of limitations, and now several quarters later, teams are using dash-forge easily.

## Aggregate Feedback

Carlo's approach to gathering feedback was different. He started with anonymous developer surveys. What was preventing you from getting your job done? What frustrates you about your job? He also had new hires make daily lists of any impediments they ran into. Then he took this data – and after some cleaning and summarizing – took it to a focus group of trusted devs.

He came out of this with a list of improvements that the organization needed to prioritize above new feature work. Build speed improvements had to happen, red tape had to be removed, and cross-team collaboration had to be strongly encouraged. There was also implementation work: a new docs system based on markdown, a backstage implementation, and a new role fully dedicated to onboarding training and DevEx improvements.

Six months later, the anonymous developer survey looked a lot better, and six months after that, and the engineering org was moving faster than it ever had before.

## Conclusion

So there you go. Developer Experience Design (DX) is not just a trendy concept but a fundamental pillar of success in modern software development. Alice, Carlos, and Bob underscore its wide-ranging impact.

* For **Alice**, embracing DX, transformed her product's usability and popularity by prioritizing clear documentation and smooth onboarding.
* **Bob** took DX to heart within his organization, turning a once-underused tool into a loved and valued resource by being attuned to his internal users' needs.
* Meanwhile, **Carlos** leveraged DX to tackle rapid scaling challenges, using feedback to implement necessary changes that sped up development and improved team collaboration.

From public-facing APIs to internal tools and across entire organizations, DX defines the quality of the interaction developers have with the systems they use. Field testing and continuous feedback play a critical role in identifying pain points and areas of improvement. They drive adoption, nurture loyalty, and fosters success.

DX can transform an ignored tool into an essential one, facilitate a struggling product's rise to popularity, and turn a rapidly expanding team into a well-oiled machine. Whether you are an Alice, a Bob, or a Carlos, recognizing the importance of DX and continuously working to improve it is the key to ensuring developer satisfaction and, ultimately, your organization's success. And if you're interested in improving your Developer Experience, you might want to check out [Earthly](https://www.earthly.dev/), a build automation tool designed to simplify and accelerate development workflows.
