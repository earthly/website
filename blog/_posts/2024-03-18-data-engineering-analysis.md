---
title: "My Adventure in Data Engineering"
toc: true
author: Ido

internal-links:
 - data engineering
 - adventures in data engineering
 - implementing data engineering
excerpt: |
    An engineer at Earthly shares his journey and tips for implementing self-sign-up and analyzing user behavior using tools like Funnel Story and Hex to improve the onboarding process and make data-driven decisions. By tracking user behavior and making strategic product decisions based on the data, Earthly was able to attract more users and convert them into paying customers.
categories:
  - Data
---

**Ido - an engineer at Earthly - recently put on a data analytics hat and dove deep into instrumentation and visualization so he could understand how users are using Earthly. In this article, he shares his journey and tips for others.**

## Initial Challenge: Implementing Self-Sign-Up

We've been working to make Earthly easier for new users. I recently tackled the self-sign-up feature. We wanted to make signing up simple, to draw in more developers and grow our community.

The Streamlined Onboarding for Earthly gets us closer to our goal: making CI/CD simple so developers can focus on their work. But was it working? I needed to find out, but getting to the bottom of that involved mastering Segment and Snowflake, learning what DBT was, and 20 other things I've probably forgotten by now.

## Identifying the Need for an Analytics Approach

![Identifying]({{site.images}}{{page.slug}}/identify.png)\

After we launched self-sign-up, we used what data we had to watch how new users used our platform. Did they like what Earthly offered? We tracked their path from the first click to sign up all the way to buy-in.

But we needed to dig deeper into our customer journey funnel. Track the journey from sign-up to paying customer. Our goal was to make onboarding smoother, and get people to having a satisfy experience with Earthly faster.

The problem is tracking and analyzing people to see where they get stuck in our on-boarding process. Earthly has a bit of a steep onramp at first. How can we make it smoother? How can we measure the drop-off? Traditional tools fell short, and custom solutions seemed too heavy and too costly. So, we turned to specialized tools like [FunnelStory](https://funnelstory.ai/) to really understand people's onboarding journey's.

## Navigating Challenges

Diving into funnel analysis, I hit some snags. It wasn't just about new tools or dashboards. It was about understanding users and tackling tricky data.

I faced a big challenge: messy data. Sometimes, what I needed was just not there, or our numbers didn't add up. It was a wake-up call for me. I had to take a second look at the assumptions behind the data and sometimes add new instrumentation. And getting the data into the right format was another challenge. SQL queries and analytics tools – each with its own quirks.

## Exploring Solutions: Funnel Story and Beyond

![Exploring]({{site.images}}{{page.slug}}/explore.png)\

As I dug into how customers interact and whether they stick around, creating a funnel visualization was another challenge. Standard tools were too vague or too much custom work. Not scalable, not efficient. That's when we decided to try Funnel Story.

It showed us, plain and simple, the path people took from signing up to being active users and maybe even paying us. It was a fairly easy setup, and once I had that in shape, it meshed well with our data.

I turned to Hex and other data tools to build out custom usage models beyond the funnel. With Hex, I crafted custom data models and made visualizations that showed us custom data specific to our customers' usage.

We mixed Funnel Story's funnel tracking with custom stuff made with Hex, and together, it was a powerful toolkit. It lets us see what users do right away and where they bail.

Using data helps you make smart choices, better your product, and keep users happy. It's not just about collecting numbers. It's about understanding them and using them to keep getting better and to innovate.

## Lessons Learned and Best Practices for Data-Driven Development

![Lessons]({{site.images}}{{page.slug}}/lesson.png)\

Diving into analytics, I hit some tough spots. After dropping my daughter off at pre-school, I often work out of a cafe in Brooklyn. If you saw me there, laptop open, confusion on my face, wrestling with SQL variants and Snowflake gotchas, trying to make sense of huge piles of data, I might have looked stressed. Trying to assess accuracy, getting feedback from others on the numbers, but doing much of this solo. I had to double-check my work, with no formal review or second pair of eyes. We are a start-up, and I needed to take the lead on this and power through any impediments.

If I were giving myself advice for making an effort like this again, here's what I'd want to know.

1. **Use different tools:** Sure, Funnel Story is great for tracking accounts, but in some cases, we also needed to build custom usage models. Hex is more work, but it is a way to build exactly whatever specific need you have.
2. **Play to Each Tool's Strengths:** Funnel Story is great for building funnel analysis. Hex shines when you need custom data models and visualizations to help make strategic product decisions.
3. **Guide Big Choices:** Mix customer journey and funnel analysis with other data to shape product development and how we bring in users. This way, decisions rest on a full picture of how users interact with our product.
4. **Keep learning and adapting:** Watch how users react and dive into the data. Change your game plan as you learn what works and what doesn't. Always polish the user experience with what the numbers tell you.

In short, uUse Funnel Story for funnel analysis, then add tools like Hex for performing custom usage analysis to complete the picture. These tools will show you where to tweak your product and how to on-boarding. You'll see exactly how accounts move through your product and where you can improve.

Using data helps you make smart choices that matter for your product and the people using it. Our data analysis taught us a lot. We tracked how accounts behaved from sign-up to using our platform's features. We saw what they liked and didn't, and where we were losing them. This helped us figure out what to build next and how to keep them coming back.

And that's where we're focusing now. And it's paying off – we're not just getting users, we're getting paying customers.

{% include_html cta/bottom-cta.html %}
