---
title: "Misaligned Incentives in Dev Tool Businesses"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - Pricing
 - Costing
 - Open Source
 - Softwares
 - Business 
excerpt: Discover the hidden pitfalls of dev tool businesses and how misaligned incentives can lead to bloated software and unsatisfied users. Learn how Earthly tackles these challenges and prioritizes customer needs in this insightful article.
---
<!-- markdownlint-disable MD028 -->
Back around when Barack Obama was president of the United States, I worked as a software developer on an enterprise 'learning management software.' The work could be challenging but was always adding more complexity. For example, users took classes and classes could have prerequisites. There were optional and mandatory prerequisites, but I was there when we added 'optional-mandatory' prerequisites. And then after that, 'mandatory-optional' prerequisites. These were highly requested features.

(I can't even remember which was which, but they were different from each other.)

The features people requested were always more buttons, more options, more flags, and more complexity. Enterprise software is like this: the people who bought it didn't use it, and those who used it were in it all day. So past a certain point, everything got more complicated.

It's possible to overcome incentives like this. Product managers now understand this trade-off and consider carefully when to say no. But it's a complex trade-off. First, you are fighting against your hardcore users, who are all you hear from. Second, the more features you add, the better deal buyers think they are getting. Because, at least back then, enterprise software was sold based on who had the most features. The incentives are all wrong.

<div class="wide">
![The end-state of Enterprise Software - Source [Howtogeek](https://www.howtogeek.com/wp-content/uploads/gg/up/sshot4d790f334bd5f.jpg)]({{site.images}}{{page.slug}}/sshot4d790f334bd5f.jpg)
</div>

But I never really thought about the incentives at the time. I just observed the software getting stranger and more complex the more the company succeeded. I just thought this was some software end-state where like dying stars, the checkboxes and buttons expand to fill all possible visual space. But then, years later, I joined Earthly, and the topic of incentives started coming up more and more.

## Open Source Incentives

Vlad mentioned in a meeting early after my joining Earthly that the line between what's open source and what's commercial is tricky. Because at that line, incentives can get messy. What do you do if you sell a commercial feature and someone wants to add something like it to the open-source product? You want to encourage contribution, but you also need to keep the lights on. For this reason, we drew the line at compute and SaaS features. Open-source users can contribute as much as they wish to Earthly, because the monetization is SaaS-based, not feature based.

![COST]({{site.images}}{{page.slug}}/cost.png)\

There is this platitude about how you are the product if you aren't paying for something. It's not 100% true, but it does get at an important point. If you cost a business money, they will want to recoup that at some point. (Even if it means angering everyone by trying to charge for [Dockerhub](https://www.theregister.com/2023/03/17/docker_free_teams_plan/) or [Docker Desktop](https://www.theregister.com/2021/08/31/docker_desktop_no_longer_free/).)

TailScale is the only company I've seen talk explicitly about the incentives around free products and what they get out of free users:

> Perhaps we're not supposed to say the quiet part out loud, but it's important for the discussion. Our architectural decisions were made carefully, and are paying off.
>
> We avoid touching your packets—for privacy, but also to reduce our costs.
> You get free stuff. You enjoy it. You tell your boss. Your boss gives us money (eventually).
>
> [TailScale](https://tailscale.com/blog/free-plan/)

## Compute Pricing

So when we at Earthly launched our commercial product, incentives came up again. If Earthly only charged you some markup on top of our server cost to run your build, then the incentives aren't ideal.

Here's an example: We are good at caching parts of builds to get faster build times, but what if we found a way to cache even more? What if our caching got more fine-grained, our cache hit rate doubled, and build times fell in half on average across all our clients? Then, if we priced things based on how many build minutes you used, we would have just cut our revenue in half!

Cutting build times in half is a fantastic improvement, but a feature that halves revenue will not get shipped. It won't even get built. You can be as charitable and well-meaning as you like, but if your bottom line is build-minutes, you want build-minutes to go up, not down. And many CI platforms are operating precisely this way!

But what do we do about it? Well, we don't profit from compute. We give that away at cost and charge based on seats. Of course, seat-based pricing also has downsides, but we think they're less problematic. (That may be an article for another time.)

![Profit]({{site.images}}{{page.slug}}/profit.png)\

## Incentives and Costs

Initially, I thought that the cause of enterprise software bloat was due to some kind of business failure. But now I see that it's a natural byproduct of the buying and product development processes.

Similarly – for dev tools – aligned incentives lead to good outcomes, and everything else is a problem waiting to happen. For example, every free open-source user of Travis CI – back when Travis was the hot CI – cost Travis more money than the potential profit. And then people wonder why things go sour at some point and jump ship to another CI with the same growth model. Meanwhile, TailScale's free users cost them near zero and earn them word of mouth.

So, now I see incentives everywhere, and I'm happy to work at a place that thought them through ahead of time because when free usage or product improvement isn't a win/win, things will eventually get messy.

{% include_html cta/bottom-cta.html %}
