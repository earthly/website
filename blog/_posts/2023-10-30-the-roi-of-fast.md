---
title: "A biased take on the ROI of fast"
categories:
  - Tutorials
toc: true
author: Vlad

internal-links:
 - return on investment of fast
 - investment of fast
 - take on investment of fast
---

TLDR: In my totally bias role as one of Earthly's creators, I believe that with Earthly:

- You'll directly cut down on build expenses as builds run faster.
- Developers will save substantial time, translating to an even greater value than mere infrastructure savings.
- The acceleration in iteration enables swifter product improvements leading to substantial execution advantages in fast moving markets.

In our previous blog post, we talked about [how Earthly achieves 2-20X faster builds](TODO link previous article). It is able to do that by addressing common inefficiencies, and utilizing techniques like holistic layer caching, build graphs, and Earthly Satellites.

This is great - but how do you quantify the value of fast builds? Is a fast build something worth pursuing? What's your return on investment (ROI)?

While the first thing some people think about when quantifying performance is the optimized cost of infrastructure, but that is only a small part of the real story. In the context of CI/CD, fast also means more developer productivity, faster time to market and therefore faster product feedback loops. This can be a key competitive advantage for the business as a whole.

Quick disclaimer: This post is written by me, Vlad A. Ionescu, founder and CEO of Earthly, someone who has chosen to dedicate a significant amount of time to solving the problem of slow builds. I therefore realize how this article can come across as very biased. It definitely is biased, but hopefully the evidence-driven presentation can help you think about this topic in your own way.

## Return: CI/CD Infrastructure

![Infrastructure]({{site.images}}{{page.slug}}/infra.png)\

The most obvious and tangible benefit of a fast build is that your CI expenses go down significantly.

Let's take a very conservative real-world example. Let's say you have a team of 30 developers, and each developer performs 5 builds per day. Let's also say that the CI has 5 parallel jobs as part of each build, and each of those jobs takes 25 minutes to complete. This works out to about 400k build minutes per month.

If Earthly speeds up your build by 2.5X (a very common result among Earthly customers), then your build minutes drop down to 161k. And if the CI cost per minute is $0.008 (e.g. [GitHub Actions](https://docs.github.com/en/billing/managing-billing-for-github-actions/about-billing-for-github-actions#per-minute-rates)), well you just saved $23k per year.

While that might seem significant, it's actually a small part of the whole story. Developer productivity is really where most of the returns come from.

## Return: Developer Time Saved

![Image Credit: XKCD #303](https://imgs.xkcd.com/comics/compiling.png)

In a [study conducted by Google and published in IEEE Software (Jaspan and Green, 2023)](https://www.computer.org/csdl/magazine/so/2023/04/10176199/1OAJyfknInm), the authors found that "even modest build latency improvements are helpful" with regards to improving developer productivity. The study was conducted in search for some speed threshold above which developers would stop switching tasks and stay in-context, and thus gain dramatically improved productivity. Sadly, no such threshold was identified, suggesting instead that the benefits follow the speed-up factor linearly.

> While it's disappointing to not have an ideal target number, it's also an opportunity. Every change to build latency can increase the likelihood of developers staying on task, although if there are longer build latencies, one would need a proportionally larger change to see an impact.

GitHub, has also previously [talked about CI speed](https://github.blog/2022-12-08-experiment-the-hidden-costs-of-waiting-on-slow-build-times/). This blog post takes for granted the fact that CI build time improvements are directly translatable to developer time saved.

It is very difficult to measure precisely to what extent CI time saved is equal to developer productivity gained, so in our calculations, we chose to discount build time savings by 50%, to be conservative. If you believe this percentage should be different, I linked a spreadsheet that you can use to make your own custom time-saving calculation toward the end of this article.

In our previous example, you were saving 239k build minutes per month. Note though that these are build minutes from 5 parallel jobs. So we must first divide by 5, resulting in 47.8k wall-clock minutes saved. If we discount this by 50%, we get about 24k minutes per month.

The average developer salary in the US according to the [2022 StackOverflow survey](https://survey.stackoverflow.co/2022/#salary-united-states) is $150k. [USNews](https://money.usnews.com/careers/best-jobs/software-developer/salary) says $120k. Let's use $120k to be conservative. Considering public holidays and vacation time, this works out to about $62.50 per hour, or $1.04 per minute.

Multiplying by the discounted time saved per month and multiplying by 12, we get about $300k per year in savings ($600k if you ignore the discount).

So even though you're saving $23k in CI infrastructure, the real saving of developer time is far more significant, resulting in 13X greater value.

The total savings result in about 2.5 FTEs worth of value. This doesn't mean you can fire a bunch of teammates if you adopt Earthly. Software delivery doesn't exactly work like that. But it gives you some idea about how much more productive the current team can be.

Beyond these savings, Earthly also helps with CI/CD maintenance costs, as it allows you to run CI builds on your laptop, thus significantly improving the dev/test feedback cycle when developing or debugging the CI. We haven't even included this part in our math.

## Return: Tighter Product Feedback Cycles

![Feedback]({{site.images}}{{page.slug}}/feedback.png)\

There is yet another component to the returns you get from faster builds that is harder to quantify. As I don't have a evidence or data for this argument, feel free to take this part with a grain of salt, as I walk you through a more qualitative benefit.

Books such as The Lean Startup (Eric Ries), tell us that lines of code, code commits, or PRs don't give us product progress. Instead it's "validated learning" that really allow you to move forward, and this is possible through a build-measure-learn (BML) feedback cycle between the team executing on the product and the customer. Although the book is about early stage startups mainly, it also argues that new products, new features or, in general, new efforts within a company are like a startup within a bigger organization, and so the same applies to those cases too.

We can then conclude that, the faster this BML loop is, the tighter the feedback cycle gets, and so the faster you can make progress.

When an engineering organization is able to execute faster through build time savings, that organization is then able to run through the "build" part of the loop faster, and that helps keep the whole BML cycle in shorter contexts. This applies regardless of whether the customer is external to the organization, or internal (another team that your product or tool you're building serves).

The benefit of faster BML cycles allows you to ship solutions faster, get feedback earlier, reach market-fit earlier, and get more polished results with fewer resources. It is impossible to quantify how an increase in developer agility can result in better overall business returns as part of this. But intuition would tell us that it's non-zero.

## Cost: Integrating Earthly

There is, however, an upfront cost of integrating Earthly into your existing setup. While this is a real amount of effort, it is lower than you might think at first glance, for the following reasons:

- Learning and understanding Earthly is very easy, as it reuses concepts that developers are already aware of if they use Docker: the syntax is instantly familiar, and many Dockerfiles can be reused.
- Iterating on the build is faster that before, thanks to the fact that you can run CI pipelines on your computer.
- Earthly works with existing language-specific tooling. Unlike ripping and replacing the whole stack, Earthly works by wrapping core tooling, instead of reinventing the wheel.
- You don't have to adopt Earthly for everything in a big-bang. Earthly was designed to be adopted incrementally (possibly starting with the projects where slow build times hurt the most). This reduces the risk of migration.
- This is a one-time cost. Once integrated, you benefit from it every day, every month without additional maintenance burden (not more than before anyway).
- The general developer experience (DX) of Earthly is very polished (or at least that's what our users are telling us) - I admit that this last one is a rather subjective argument. Best way to find out if this is true is to give Earthly a shot 😉.

## Cost: Earthly Cloud Subscription

![Cloud]({{site.images}}{{page.slug}}/cloud.png)\

At Earthly, we believe that billing CI/CD by the build minute is fundamentally broken, because the slower the build gets, the more the vendor profits. It creates misaligned incentives. CI/CD tooling should be aligned to developer productivity (not to the opposite of it!).

For this reason, our pricing model uses the number of active users for the profit-generating component of our pricing, and charges a zero-margin fee on compute. Plus, because we don't want our customers to even think about build minutes, our plans come with a very [generous amount of included build minutes that scale with the team size](https://earthly.dev/pricing) - something very unique in the realm of CI/CD tooling.

In our running example, we showed how a 2.5X build speed improvement can save you $23k in CI infrastructure, and $300k in developer time (conservative estimate) in a team of 30 people. For this setup, Earthly Cloud costs $19.7k per year. So in this case, you're covering the cost of Earthly without even asking for more budget (you just shift from existing CI infrastructure) - yet the benefits are 16X greater than that.

## Try Your Own Scenario

If you want to play around with different scenarios like the one we just walked through in this article, we created [a calculator Google spreadsheet with formulas](https://docs.google.com/spreadsheets/d/1h5zK_oJZ2RHun64-epVIIWCJrgLSbYatoXsnK_I6QgI/edit#gid=1796614132). Just make a copy and play around with the numbers in the blue cells to see the equivalent possible savings.

## Conclusion

From my admittedly biased viewpoint as one of the creators of Earthly, I've always believed in the transformative power of fast builds. But as we've delved into the tangible and intangible benefits of rapid build processes, it's clear that this belief isn't merely grounded in bias. The value of fast builds extends far beyond the immediate cost savings in CI/CD infrastructure. While the tangible benefits, such as reduced infrastructure costs, are easily quantifiable, the intangible benefits, like enhanced developer productivity and tighter product feedback cycles, offer a more profound impact on the overall business. You can not only optimize your CI/CD processes but also unlock a new level of agility and efficiency in development cycles.

**The adoption of Earthly is not merely an expense but an investment**. An investment in faster feedback loops, in developer satisfaction, and in the overall speed of delivering value to the market. In a rapidly evolving tech landscape, the ability to iterate quickly and efficiently can be the difference between leading the market and playing catch-up.

As we've explored in this article, the ROI of fast builds is multifaceted. It's not just about dollars saved but about the compounded benefits that ripple through an organization, from individual developers to the business's bottom line. So, the next time you find yourself waiting for a build to complete, think about the bigger picture. In the end, the pursuit of faster builds is not just about speed; it's about harnessing that speed to drive innovation, responsiveness, and growth.

{% include_html cta/bottom-cta.html %}
