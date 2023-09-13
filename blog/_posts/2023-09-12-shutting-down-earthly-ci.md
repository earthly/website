---
title: "We built the fastest CI in the world. It failed. Here's what we learned"
categories:
  - News
toc: true
author: Vlad

internal-links:
 - earthly ci shutting down
 - earthly ci failed
 - learning from failures
 - fastest ci failed
---

### TLDR

- **We are shutting down Earthly CI.**
- **We are doubling down on Earthly's core strengths of local builds and reproducibility.**
- **We are recentering around Earthly and Earthly Satellites.**

## The Fastest CI

Imagine you live in a world where no part of the build has to repeat unless the changes actually impacted it. A world in which all builds happened with automatic parallelism. A world in which you could reproduce very reliably any part of the build on your laptop. Fairy tales, right? Well, that's what we built, and to everyone's surprise, nobody wanted it. It's like flying cars - they sound amazing, but in practice, things are more difficult than they might seem.

Back in April 2020, we at Earthly set out on this quest to improve CI/CD tooling. We dared to ask questions like "What if the CI could run on your laptop?" And "what would the fastest CI system on the planet look like?" With these questions in mind, we came to a pretty strange, but pretty interesting answer... the build system and the CI need to be the same. And it needs to be distributed.

Now we all know dreaming big is easy. Execution is where things get hard.

## What Does Success Look Like?

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4340.png --picture --img height="400px" %}

In a startup, you don't have the luxury of building a mature product with all the possible bells and whistles before shipping it to your customers. Mature products take many years and many engineers to build out.

And yet, you are going up against the incumbents - companies that have hundreds of millions in funding, (maybe even IPO'd), they have hundreds of engineers, they have a 10-year head start, and a ton of reputation. How can you even compete?

Well, you know what they say... "Competition is for losers". The answer is that you don't. At least not on the same level. You'll never be more mature, or have more features, or more integrations. Instead, you can be 10x better in one, very specific way. And you'll appeal to the few teams where the very specific problem you're solving is so painful that they're willing to make compromises on everything else.

You're not going after the whole market in the beginning. You're just going after just enough enthusiasts, mavens, early adopters - whatever you want to call them - for whom the solution that you built on a shoestring budget is dramatically better in their specific situation than any incumbent. So much better, that they're willing to pay the cost of adoption, and they're willing to suffer through the bugs and the missing bells and whistles.

Then, once you have captured that segment, you invest more, extend to a wider audience, get more feedback, then again invest more, extend again, and so on. It's important to understand this dynamic in order to gauge what success looks like at the earliest stages.

So if your MVP is not getting enough validation, you can't just slap more features on it, because, again, features are not what will make you successful. Incumbents win feature contests.

Successful products will show validation at a small scale, despite all their limitations, bugs, and general annoyances. If you can't find a small group of people passionate enough about your product in its experimental stage, you're going to have a hard time capturing an audience even with a feature-rich product. It's a recipe for building something nobody wants.

What early-stage validation looks like is a small group of people who have a lot of passion for what you do. Nobody has heard about your stuff, but your users are passionately shouting from the rooftops about it. You walk into their office and everyone has stickers with your company on their laptops, and everyone wants to talk to you.

## The Master Plan for Earthly CI

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4610.png --picture --img height="400px" %}

To build out the vision of Earthly CI, we devised a master plan. We knew that we didn't want to go on a crazy complex implementation for 3 years only to emerge from a cave with a product that would not fit the needs of the real world. So we split up the end-vision into several independent products that we would validate along the way.

Thus, instead of building Earthly CI from day 0, we first built the syntax, and the general experience around running builds on-demand. The key value we delivered was build consistency: there is a level of guarantee that the build will execute the same, regardless of the environment it runs in. The syntax of this build tool is the same as the CI down the road, but it only ran locally initially and in other CIs. We called this **first milestone** Earthly.

Then we built remote runners that can be invoked from anywhere - again your laptop or any CI. These remote runners bring you all the key benefits of Earthly CI but without being a CI. The key value is build speed. And I'm talking 2-20X faster CI pipelines, thanks to the caching and parallelism. We called this **second milestone** Earthly Satellites.

And finally, **the third milestone**, Earthly CI - the platform that brings everything together, the CI that is ridiculously fast and can run anywhere. This is the full CI that is meant to compete with all the other big CIs like GitHub Actions, CircleCI, Jenkins and so on.

What was particularly appealing about this plan was that Earthly, the build system, targets one problem: **build consistency**, while the final version, Earthly CI, targets another problem: **build speed**. This meant that Earthly, which is free, would not cannibalize in any way the monetization of Earthly CI. We wouldn't be giving away too much for free – as Jenkins did – and instead, it would serve as a sustainable and scalable business model. It made sense to use the build system as a way to then create bottom-up adoption for Earthly CI - and the fact that we were building it first allowed us to build traction that one day will magically just convert over to Earthly CI users.

Little did we know that this difference in value proposition – consistency vs. speed – actually became a problem down the road...

### Milestone 1: Earthly

Earthly was the lowest-stakes validation. I just built the first version on my own, threw it up on GitHub, and then launched it on Reddit and HackerNews. Zero funding (apart from my wife's patience), so close to zero risk. If it takes off, I go raise money. If it doesn't I'll try something else.

We now know that Earthly is used widely across thousands of repositories, by companies big and small, like VMware, Adobe, Namely, Roche, ExpressVPN, Bluecore, and many others. But the early signs were that people were using Earthly even when it was a one-person unfunded project riddled with bugs and limitations. That's validation.

### Milestone 2: Earthly Satellites

After fixing the obvious issues in Earthly, and widened support to appeal to more types of organizations, we were now building momentum. And with enough capital, we were able to now work on the next milestone: Earthly Satellites.

The interesting thing about Satellites was that we were getting the validation even before we built them. Earthly being open-source, you could already run your own Earthly remote runner (since we use Buildkit underneath, it was essentially a remote Buildkit), connect Earthly to it, and get similar benefits to Satellites even before this was a commercial offering. And so people did this on their own, hosting it in their own environment, without us managing it for them. Once we had this packaged up in a managed offering, people were flocking to it, mainly because they did not want to manage remote runners on their own. The initial version of Satellites was buggy, inefficient, and unstable. Yet people came to it despite those inefficiencies, because there was nothing else that would give them CI/CD speed at that level. That's validation.

Interestingly, we didn't really see it for what it was at the time. We were only thinking of the end vision of taking over the CI world completely, and Satellites was just an implementation milestone that we happened to publish as a product along the way. So we just shrugged and figured, "Ok, if this is how people react to this incomplete offering, imagine how they will react to the full vision of Earthly CI!"

### Milestone 3: Earthly CI

Almost everyone who was using Satellites was using them in a CI/CD use case. Meaning that they executed remote Satellite builds via CI with the main goal of speeding up their pipelines. In this configuration, the CI vendor is merely a pass-through that deals with triggering pipelines. The actual execution happens on the satellites. To us, that was validation that Earthly CI was needed. Why not just simplify the stack? Why pay both the CI vendor and us, when you can just pay us?

Plus, many Earthly community members were asking about the possibility of hooking up Earthly Satellites directly to GitHub. More validation.

Whenever we spoke to VPs of engineering, the promise of 2-20X faster builds was making their eyes light up!

The closer we were getting to the Earthly CI launch, the more of a slam dunk it seemed it was going to be.

But, as you already know what this blog post is about, making Earthly CI successful turned out to be more challenging than we thought.

## The Early Symptoms

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4680.png --picture --img height="400px" %}

For Earthly CI, we did a [solid launch](https://earthly.dev/blog/launching-earthly-ci/), landed on [TechCrunch](https://techcrunch.com/2023/02/23/earthly-wants-to-reinvent-continuous-integration-to-make-it-faster-and-cheaper/), and lined up [a few blog articles for Reddit and HackerNews](https://earthly.dev/blog/remote-code-execution/).

From the launch we got about 50 emails signing up on the waitlist in the first week or two, outpacing the goals we had. We started setting up calls with these people, and, right off the bat, we could sense a big difference between existing Earthly users vs. people who were coming to us for the first time.

These weren't the raving fans we were used to talking with. New people would look at Earthly CI with a skeptical eye. They were mostly thinking that "all CIs are the same - they just have different syntax," and then they would not really look any further as to why we might actually be different. As a result, the conversation invariably turned to the **cost of migration**. How difficult would it be for them to rewrite and adapt a bunch of existing scripts to be able to use Earthly effectively?

Existing users, by contrast, were already fans, had already done the work of the migration, and already saw the benefits of Earthly. They were ready to champion us in their organizations, even if not everyone in their organization was on board yet.

We kept talking to as many teams as we could, to understand the apprehension toward Earthly CI, but it always came back to weighing the cost of migration vs. the benefit. And we could never win this up-front, mainly because these prospects had no idea whether we could deliver on the benefits we promised at scale. We don't have a long-established reputation like our incumbents. Existing users claimed we were 10x easier to use, but how can you prove that to a new client on a quick Zoom call? So it didn't make sense for them to jump head-first into an expensive and time-consuming migration effort just because some startup they had never heard of promised to deliver the sun and the moon.

We also tried getting existing Earthly Satellite customers to switch to Earthly CI – after all, they were all using Satellites **in their CIs**. The problem with this group was that they were already getting 95% of the value of Earthly CI through Satellites. Their builds were already really fast. Compared to a GitHub Actions + Satellite setup, Earthly CI wasn't better, or at least, it wasn't better enough to warrant the switch.

And then, after the launch traffic died down... There was silence.

## The Most Ridiculous Negative Lead Qualification Criteria Ever

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4880.png --picture --img height="400px" %}

The odd thing about direct calls with prospects was that we could never convince them to try out any of our products when talking to them face to face. Not Earthly CI, not Satellites, not even Earthly. At this point, we probably had over 100 calls with prospects. We were hearing over and over how they spent 2 years migrating to their current setup, how they put so much effort into it, and how throwing all that away would be so wasteful. And how annoying it is to switch CIs.

And yet, when users were coming on their own to our website, through a mix of product-led / word of mouth and content marketing, the adoption of Earthly was happening every single day. At a very significant and increasing rate.

What seemed like absolutely impossible with one approach was being proven as very much possible - perhaps even easy - with a different approach.

In retrospect, it's of course obvious that there's no way to sell developer products via traditional means. And we already knew that. We were just shocked at how stark of a difference the approach could create. It became clear that a direct GTM approach would not help us validate a product like Earthly CI.

We ended up with the most ridiculous negative qualification criteria I have ever heard of: if the prospect requires a demo, then they're not worth going after. The type of prospect that *does* convert will come to us after they downloaded Earthly, read some docs, and wrote a bunch of Earthfiles. These teams never need a demo. It's weird, but demoing is one of the strongest negative signals we have.

The moral of the story here is that when you introduce a developer tool that requires integration work (work outside of the development team's commonly expected flow, work that replicates already existing work, and work that requires learning a new syntax or API), you can never force, or hurry anyone to adopt it. This can only happen on the user's schedule. **People will buy a developer tool, but you can't sell it**. We all know that engineers like to get their hands dirty and explore things on their own. This conclusion is the corollary of that well-known fact. That's why you can't hard sell to engineers. You can only soft-sell.

## Problems Converting Earthly Users

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5140.png --picture --img height="400px" %}

Our other big channel was converting existing Earthly users into Earthly CI users. This was a key segment because there is no migration concern - everyone in this segment has already converted to Earthfiles. It should be just a flip of a switch, right?... Right?...

Not so fast. What about the GitHub plugins ecosystem? Do you have a codecov action? Do you have manual triggers? Can I trigger based on a git tag creation? Can I select the machine size? Can I cancel stale builds? Can I trust your platform with our build secrets?

Our Earthly CI MVP, despite being the fastest CI ever, never met some key requirements for people. Sure, there were a few enthusiasts who did play around with Earthly CI and started using it. But there were no sizeable organizations, with budgets, willing to use it more widely than just 2-3 engineers. And even the few Earthly CI users, after a while converted into Satellites users, to get the benefit of the combination of a richer GitHub ecosystem and the speed of the Satellites.

But for the most part, the Earthly community came to our product mainly for the value proposition of *consistent builds*. Since we were now trying to sell the *fast builds* value prop instead, well, our audience just wasn't qualified that way. The match was poor.

And the few organizations that did have both of these needs ended up becoming Satellite customers instead. Not that we minded the Satellite customers, but it wasn't helping to validate Earthly CI as a product.

## Validating the Invalidation

At this point, we could see that things weren't going according to plan. Calls weren't converting. Existing Satellite customers weren't converting. And existing Earthly users weren't converting.

We knew that we needed to change things up, but we weren't yet thinking that Earthly CI itself was the problem.

At this point, the messaging on our website was saying "Earthly makes CI super simple" and most of the content on the first page was about CI, CI, CI. Gavin Johnson, our PMM, had the interesting idea to A/B-test swapping the word "CI" for the word "build" on our website: "Earthly makes builds super simple". Inside I kinda thought that it was somewhat of a ridiculous idea... we're trying to push for our grand vision, and we don't want to be bucketed into the "builds" space by investors (a space with limited commercial success). CI is where it's at. But I didn't have any better ideas either, so we went with it.

And then the results came in.

This one-word change ended up **doubling** conversions to the "Get Earthly" page – the main CTA on our website. 🤯

Now we were starting to get really doubtful about this Earthly CI thing.

## Lessons From Another Life

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5320.png --picture --img height="400px" %}

In the fall of 2016, long before Earthly, I, along with two co-founders, a really smart code analysis scientist, and an incredibly dedicated team, started ShiftLeft (nowadays called [Qwiet.ai](https://qwiet.ai)). Our vision was to build a security agent that you could install in production and it would protect your cloud app from attacks on vulnerabilities that you have in your source code. This was an incredibly complex system, which required that we build an entire code analyzer that would work with multiple programming languages, runtime agents for individual runtimes, and a distributed backend to integrate everything. The complexity was akin to three companies, all being built by one tiny startup.

And yet, we somehow got one programming language to work end-to-end after over a year of effort, even if it was incredibly buggy initially. We tried to put it on the market - after all "if you're not embarrassed by your first version, you launched too late". After several attempts, we realized that it wasn't appealing to the market. ShiftLeft being a security product, our target audience was heavily regulated enterprises. These enterprises, by definition, have a lot of red tape, and it is difficult to put anything in production without extensive bureaucracy. To make matters worse, you had to put this both in CI/CD, for the code analysis, and in production, for the runtime protection, thus creating a virtually impossible insertion motion.

But to overcome the difficulty of insertion, we always thought that it just needed more features. With enough features, surely the customer will accept the difficulty of insertion anyway! I mean... looking at the product it was obvious that it had all these rough edges. Maybe it's more appealing if we smooth out the rough edges. It just needs to bake in the oven for a bit longer.

And bake it we did. For another year and a half. And still... Nobody. Wanted. It.

Looking back on the experience, we made many mistakes, which, at this point, sound like startup cliche:

- We did not build the product incrementally, with user feedback informing every step of the execution.
- There were some early signals that certain aspects of the product did not align with what the industry needs, but we didn't listen. We just kept building.

Luckily, we later realized that this complex product can be split into two other products: a security code introspector for security experts, and a standalone code analyzer that is 40 times faster than any other code analyzer on the market. Yay! But we lost over a year of work and hired too many people to execute in a direction that never materialized into anything successful. It would have been so much more efficient if we started out by building smaller components of the end vision and selling those components as independent products first. The team would have been leaner, we would have had an MVP faster, and we would have had customer feedback much sooner, to help direct the roadmap.

My biggest regret from the experience was that we did not stop earlier when the signs were there.

Fast forward to today, learning from mistakes of the past, at Earthly we built everything incrementally. And we even put products on the market that initially seemed like purely engineering intermediate milestones. Each product builds on top of the previous achievements, thus allowing for incremental iteration with the customer in mind. We're now seeing our latest incremental iteration not working in the marketplace. And, knowing what I know about early products, it's not the missing features that are the problem.

## What's Next for Earthly?

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5430.png --picture --img height="400px" %}

Here's how I rationalize what's happening:

- People want faster builds.
- People hate switching CIs.
- There is a stigma toward new CIs in general. Specifically that they are undifferentiated. It's hard to shake that bias, and we scare people off as soon as they see "CI" on our website.
- Design-partner type of engagements don't work when we try to engage with customers directly, due to the perceived high cost of migration.
- The Earthly CI MVP isn't validating, failing to create a significant enough early adopter group.
- When we tell people that they can get faster builds without switching their CI (i.e. through Earthly Satellites), their eyes light up.

Failing to create enough meaningful initial traction with an MVP, for some the conclusion might be simple: "It just needs more features," or "just put it back in the oven." But I know what a promising product's initial traction looks like, and this is not it. If this were the real deal, there would be a group of people tolerating the absence of features for the benefits. But that's not happening here, or at least not to a meaningful enough degree.

So, our conclusion is that we need to shut down Earthly CI and refocus our energy on what is working: Earthly and Earthly Satellites. [^1]

But Vlad, you're deprecating the thing you just launched?

Well, yes. We failed fast. And that is a success in my book (or at least that's what I keep telling myself to feel better about it). Imagine if we had built only Earthly CI from the get-go. Just like with ShiftLeft, the components of the end-vision ended up being more valuable than the original end-vision itself. Only this time, we discovered that much more efficiently.

## Wrapping Up

Earthly CI is shutting down on October 1st, 2023. If you are a user, you have my sincere gratitude for experimenting with Earthly CI - it's because of people like you that there is any innovation in the world. You took a chance on us, and we appreciate it from the bottom of our hearts.

Migration off Earthly CI is really easy because Earthly works with any CI. And if you want to keep getting fast builds, you can plug in Earthly Satellites (there's now a [free tier](https://cloud.earthly.dev) too - yay!). Despite Earthly CI having been marked as beta / experimental, we will fully support your transition off of it. We will be hands-on in the [Earthly Slack community](https://earthly.dev/slack) to help you out every step of the way! We remain committed to serving our users with the utmost care.

It seems that Earthly Satellites are taking off, not just because we are delivering fast and consistent builds, but also, crucially, because we are **letting users keep their own CI**. Given this signal, it makes sense for us, as a company, to continue to invest in this direction. In fact, by shutting down Earthly CI, we have more time to execute on a number of things that the Earthly community have been asking us about:

- Satellite metrics – including CPU, memory, disk, and network I/O usage.

- Build history – for both local and Satellites builds – in the web UI.

- Auto-skip – the ability to skip a build instantly if the changed files don't impact it.

- The ability to execute Dockerfile builds remotely on Satellites, as a fast drop-in replacement for `docker build`.

- Self-hosted Satellites (a better-supported version of [our self-hosted, remote Buildkit](https://docs.earthly.dev/ci-integration/remote-buildkit)).

- The ability to spread a single build onto multiple Satellites for added speed.

- Compute v2 - fully distributed, serverless Satellites (this one will take a while to get right).

If you're not a user and you came to this post just for the story, then boy do I have some goodies for you to check out 🙂.

Earthly Satellites are ridiculously fast remote build runners that work seamlessly with any CI. It is available via Earthly Cloud and free to get started. Satellites are built on top of our open source build framework, Earthly. Earthly gives you write once, run anywhere build consistency, making it super easy to reproduce CI failures on your local computer. Earthly and Satellites together are like peanut butter and jelly – fast, consistent builds that work with any CI and are easy to debug locally. Come check us out at [earthly.dev](https://earthly.dev)!

{% include_html cta/cta-2.html %}
