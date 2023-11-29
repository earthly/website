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
last_modified_at: 2023-08-15
---
**This article emphasizes the vital role of Developer Experience (DX) in boosting productivity and job satisfaction. Earthly improves DX with reliable and efficient build processes. [Learn more about Earthly](/).**

Think of Developer Experience, or DX, as user experience but for developers. Instead of making things easier for the everyday user, DX is about making a developer's life easier when working with tools, libraries, and platforms.

## Who Should Care About Developer Experience?

Okay, we've got a definition. But who cares about DX? Why does it matter? Let's skip the jargon and consider three scenarios where DX is crucial.

<div class="align-right">
![An important moment in DX.]({{site.images}}{{page.slug}}/9740.png)
</div>

Three types of people might care about developer experience. Their jobs are different, so their views on DX might vary. Let's meet Alice, Bob, and Carlos.

## DX Awakening

### Alice - Product-Based Developer Experience

<div class="align-left">
  <img src="{{site.images}}{{page.slug}}/0590.png" width="200" height="200" />
  <figcaption>Alice - Product Manager</figcaption>
</div>

Alice is a Product Manager at Request Express, a developer tool for API development. Developer experience is critical for her because Request Express's customers are all developers.

To her, everything about Developer Experience leads back to Stripe. Stripe, a billion-dollar success, was built on a simple observation: the developer experience for payment processing was horrible, and they could do better.

Alice can't stop talking about Stripe. She loves their clear instructions, reusable code, and easy start-up. Stripe showed everyone the value of making things easy for developers.

Alice took a page from Stripe's book, modeling Request Express's new features after their developer-centric approach. She and her team created interactive documentation with embedded code samples inspired by Stripe's docs. And she led a redesign of Request Express's onboarding flow to simplify the initial integration steps that had been pain points for developers.

### Bob - Internal Platform Developer Experience

<div class="align-right">
  <img src="{{site.images}}{{page.slug}}/0970.png" width="200" height="200" />
  <figcaption>Bob - Internal Tools Lead</figcaption>
</div>

Bob is a staff software engineer at Shop-O-Rama. He works on internal tools and platforms used by Shop-o-rama's engineering teams. His job: make their work easier and more productive.

Bob's wake-up call? Failure. His team built this dashboard system at Shop-o-rama called 'Dash-forge'. Bob thought it was powerful, a game changer. But no one used it. Not without a fight.

He could have forced it. He'd seen it before. Top-down mandates, standardizing internal tools, causing friction. Developers forced to use tools they hated. He knew that wasn't the way. So he changed his approach. Started acting like a product manager. Treating internal tools and APIs as a product. Those other teams were his customers.

His product solved a genuine problem, but no one could use it. Or at least the usability was terrible enough to outweigh any potential benefits.

For Bob, DX is about being selective. He doesn't have the resources of a developer tools company. But he can make sure he's building with his users in mind. Now, things like documentation, user testing, and support are part of the product development process.

### Carlos - Organizational Developer Experience

<div class="align-left">
  <img src="{{site.images}}{{page.slug}}/1020.png" width="200" height="200" />
  <figcaption>Carlos - Director of Engineering</figcaption>
</div>

Meet Carlos. He's the Director of Engineering at a fast-growing ML startup. But he's got a problem. Carlos faces onboarding and team productivity challenges as the engineering team has grown from 10 to 100 developers.

Quick hiring means training new developers is tricky. Getting them the right environment, tools, and documentation to start contributing was even tougher. Just when things need to speed up, they're slowing down.

The ballooning team size has also introduced friction into development workflows. More developers, more confusion. Work's getting duplicated. Carlos sees it. He knows they need a team focused on smoothing things out if this startup wants to keep growing.

## DX Metrics

So for Alice, Bob, and Carlos, the tactics employed to improve the developer experience will vary. They're all about improving how developers interact with code, tools, and resources. Every interaction matters. But what Alice, Bob, and Carlos focus on? That's where they differ.

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

For Carlos, key metrics might include:

* **Onboarding Duration** - How long it takes new developers to make their first successful code contribution.
* **Time To First Commit** - Time from cloning repo to having a local commit ready. Includes time for getting dependencies, setting up the environment, and making a superficial change.
* **Build Time** - The time required to complete a code build in CI. Includes build queue wait time, if any.
* **PR Turn Around Time**: The total duration from submitting a PR until it's finally approved.

Bob's worries are a mix. He's got Carlos' concerns about developers in his Org. And he's got Alice's concerns about the tools he owns.

Regardless of the use case, though, there is no perfect metric for measuring DX improvements. Instead, whether your situation is closer to Alice, Bob, or Carlos, you should center your efforts around developer satisfaction and frustration. The least scalable but highest payoff way to do this is field testing.

## Field Testing

Field testing is observing developers using your tools, libraries, APIs, or frameworks in their natural working environment. You want to see how they handle real-world scenarios, what problems they hit, and how they get around them.

Alice, at Request Express, has the most rigorous field testing process, but even so, the process is relatively simple. She recruits developers, ones who've never used her product before.

( She started with just a few friends from a former company. As time went on, she moved on to friends of colleagues. Lately, she's even reached out to a local coding bootcamp graduating class. )  

Each volunteer gets on a video call with Alice and is given a task to complete using their chosen development environment. The task is always some variation of working through Request Express's onboarding tutorial.

## Field Testing Analysis

The first field test Alice did is hard to forget. The user was confused and lost at step one of the tutorial. He would have never even made it to step two without a nudge from her. That testing led to some tutorial changes and error message cleanup, and then field testing flowed more smoothly.

For Alice, analysis of the field testing results is a breeze. Every new volunteer finds something. A confusion point, a missing usage pattern, or just a rough edge. The hundred-dollar gift cards she hands out at the end are the best money her company has ever spent.

## Internal Field Testing

Bob's approach to field testing has been different. He temporarily joined a team looking to use Dash-forge and did the integration himself. It went badly, and for every papercut or roadblock he hit, he documented it and got his team to prioritize a resolution.

After that integration, he paired with the dev. He took a backseat, but still spotted limitations. Now, several quarters later, teams are using dash-forge with ease.

## Aggregate Feedback

Carlos did things differently. He started with anonymous surveys. What was preventing you from getting your job done? What's frustrating you? New hires made daily lists of problems. Carlos took this data, cleaned it up, summarized it, and took it to a focus group of trusted devs.

He came out of this with a list. Improvements the organization needed to prioritize. Build speed had to go up. Red tape had to go. Cross-team collaboration had to be strongly encouraged. Then there was the implementation work: A new docs system based on markdown, a backstage implementation, and a new role, all about onboarding and training improvements.

Six months later, the anonymous developer survey looked a lot better. Another six months, and the engineering org was moving faster than ever.

## Conclusion

So there you go. Developer Experience is not just a trendy new term but a fundamental pillar of success in modern software development. Alice, Carlos, and Bob underscore its wide-ranging impact.

* For **Alice**, embracing DX, focusing on clear instructions and easy start-up, transformed her product. It became more user-friendly and popular.
* **Bob** really embraced DX in his tool building. He turned a tool that was barely used into something everyone loved by listening to what his users needed.
* Meanwhile, **Carlos** used DX improvements handle fast growth. He listened to feedback, made changes, and sped up work.

From public-facing APIs to internal tools and across entire organizations, DX means asking how easy our tools are to use. Testing these tools, getting feedback, that's how we find problems and fix them. It's how we keep developers happy and successful. It's how we drive adoption, nurture loyalty, and fosters success.

Are there tools or apps you use that could be improved?

DX can turn a tool from ignored to essential, boost a struggling product, and make a growing team run smoothly. Whether you're an Alice, a Bob, or a Carlos, improving DX is key. It ensures developer satisfaction and your organization's success. And if you're looking to improve your Developer Experience, check out [Earthly](https://www.earthly.dev/). It's a tool designed to simplify and speed up builds and accelerate development workflows.