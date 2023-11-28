---
title: "Bullshit Software Projects"
categories:
  - Articles
toc: true
author: Adam
excerpt: |
    Discover the frustrations and challenges faced by software developers in the world of "bullshit work." From pointless projects to busy work and executive pet projects, this article sheds light on the absurd tasks that developers often encounter in their careers.
last_modified_at: 2023-07-14
---
**This article addresses the annoyance of meaningless tasks in software development. If you're tired of "busy work," Earthly can streamline your build process and cut out the needless tasks. [Check it out](/).**

I was frying a couple of dozen walnut crunch when I first got in trouble at Tim Horton's.

Tim Horton's is a donut and coffee place, and I worked there as a baker assistant around 2002, when I was in university.

Most donuts fry for 30 seconds per side, then you flip them and do the other side. It's hot work, spending a shift working over a deep fryer, but frying walnut crunch (since discontinued ) was my favorite part because they took 3 minutes per side, which gave me time to grab an empty cooking oil pail and sit and rest my legs while they cooked.

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/4840.png --picture --img width="260px" --alt {{ Walnut Crunch Donut }} %}
<figcaption>My introduction To Bullshit work.</figcaption>
</div>

That's when I got caught. The store manager, who wasn't usually there during my shift, saw me sitting. "If you have time to sit, you have time to clean." And so, next shift, while the next walnut crunch batch fried, I had to re-mop the already mopped floor. I could also wipe down the already clean prep surfaces or just recheck our inventory of eggs. Anything was better than resting.

This was my introduction to busy work: work to be done for no other reason than to keep yourself looking busy. It fits into a larger category of bullshit work: work that the worker must do despite having no purpose.

I hated that busy work, and I'm so glad that I finished school and started working as a software developer, where I don't have to make myself look busy all the time – I can read hacker news while a build runs and no one has yet suggested I start polishing my parentheses.

Unfortunately, software developers aren't immune from absurd tasks that seemingly benefit no one. I know this because I asked around. It turns out it's easy to find software developers that answer yes to the following question:

* **Although you are required to do your job, you secretly believe it is pointless and should not need to be performed.**

So that is today's topic, and spoiler alert: tech bullshit work is different from donut shop busy work. Instead of being something to fill downtime, it's often a whole giant project that benefits no one. Let's go through some examples.

## Bullshit Background

<div class="align-left">
 {% picture grid {{site.pimages}}{{page.slug}}/5960.png --picture --img width="260px" --alt {{ Bullshit Jobs Book }} %}
<figcaption>Bullshit Jobs by David Graeber</figcaption>
</div>
Bullshit Jobs: A Theory is a 2018 book by David Graeber investigating the strange phenomenon of pointless jobs. Graeber's book even features interviews with some software developers. Once I started reading it, I felt compelled to test out his theory of BS jobs by asking around[^1]: Did any software developers I knew, or on Lobsters, or Hacker News, have bullshit jobs?

And sure enough, it didn't take me long to hear from people who found their jobs to be pointless, and for the majority of them, it wasn't a specific task, like mopping an already mopped floor, that was useless but an entire software development project. The world is apparently rife with pointless programming projects.

Grant, a Stanford grad who's worked at several big tech companies, worked on a BS project:

> One time, I worked for 12 months on a project I believed was dumb on a team of at least 30 to 40. It made no sense why we were building it. I told my manager my feelings, and he brushed them off.
>
> A year later, the entire project was wound down. It had never shipped past an extremely limited beta. It completely failed to generate any sort of traction or product market fit. The manager who brushed off my concerns left the team way before this and went to work on something else in the organization.

The difference between these BS projects and my donut-based busy work is that I actually had to make the donuts. The busy work was never more than 10% of the job. On the other hand, a busy work project at a large enough org will occupy entire teams of people full time.

One data scientist, who prefers to remain anonymous, reported that their data science team at their start-up was utterly pointless.

> Top management wanted to tell the investors that "we use machine learning for decision making" I wrote a linear model and it fitted the data. [But] the next version was a very complicated model based on embeddings derived from boosted trees. It required an immense infrastructure to version the model, datasets, and to serve it and deploy. Weights alone had 2GB.  
>
> The job was fun at times because all the team was very smart. But certainly not fulfilling.

There are several reasons why pointless work can proliferate, and the need to incorporate buzzwords like 'machine-learning' is certainly one of them. Maybe what I need is a taxonomy of pointless dev work.

## Pointless Dev Work Taxonomy

The most prominent type of pointless work I heard of I'm calling a zombie project and I cover that in the next section. But besides that and the buzzword compliance mentioned above, there are many other types of work that people self-report as being pointless.

### Newb Busywork

One of these was busy work given to new hires or people in lower-status roles. For example, quality assurance people who log bugs that will never be fixed.

Frankie, an LA-based IOS developer, felt QA was just being used to keep them busy as an intern:

> A lot of the work for the first few months was manually testing websites and reverifying bugs that could have easily been checked by the developer fixing the issue.
> And yeah, it was pretty mentally draining, so I started looking for ways outside of work to find fulfillment and better stimulation.

### Cog in the Wheel

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/6910.png --picture --img width="180px" %}
</div>

Another demotivating type of work concerned people working at companies so large that, although the work had a purpose, it wasn't clear what it was. Freddie found this to be accurate at Google where "Larry and Sergey's protobuf moving company" T-Shirts were not-uncommon:

> The protobuf mover's thing is very real and felt very demotivating at times. There are so many servers talking to other servers talking to other servers and so on. So you feel like you're just shuffling protos around between servers.

### Bullshit Industry?

Another type of pointless project I heard about was from people who worked in an industry they didn't believe in. For example, you are shipping a highly used blockchain wallet, and your company is growing fast, yet you think cryptocurrencies are a plague on mankind.

If that describes you, maybe start job hunting, but also you should realize that not everyone sees your industry this way.

Florian, a Munich-based software developer who previously worked in AdTech, is slightly tired of people calling the work in such industries pointless:

> If you think that anything ad-related is bullshit, fine. If you think that not making people watch more ads, but tailoring them better in whatever way is bad or immoral, I also won't convince you.
> [But] one of the coolest jobs I ever worked was in adtech.

However, by far, the largest percentage of responses I saw were for a type of pointless work that is not industry or tenure specific. These were the Zombie Projects.

## Zombie Projects

Claims that twitter could be built in a weekend notwithstanding, building software is resource extensive. That's why Graeber's original findings were shocking to me because, as he says, **"Huge swathes of people spend their days performing tasks they secretly believe do not really need to be performed".** And who knows more about a job than the person performing it?

How can a monumental misallocation of capital like this happen? One reason is a refusal to face reality: A project that is doomed, but a lot rides on it, so people refuse to acknowledge that it's doomed. Tom, a Canadian developer, felt like this was the case at the networking start-up he worked at:

> We had no customers and no great urgency to get them. they didn't know who they were trying to please.

According to Tom, individual contributors were grumbling about the things they were making not making sense, but also, a non-sensical project left a lot of room for tech exploration, and some people really loved that.

> That job taught me all about cargo-culting. Well, Netflix uses microservices, so we should too! I came in with React Native and left with Elixir, so it was a massive trade-up in skills. Also, I learned how not to run a company.
>
> That job also taught me that tech and the business case for a business case are mostly independent. You can have a strong business case and be successful with garbage tech, and the reverse is also true. You should prefer a strong business case because customers are so important.

Tom's story gives me a better way to understand what a pointless job is like. Tom was working on building something, but in his mind, he couldn't see how the project would ever work out and be used by anyone. The project was doomed to fail, yet continued on in zombie mode long past the time when ICs knew its a failure.

## Sunk Cost Much

Not every project succeeds. That is a fact of life, and just because a project doesn't succeed in delivering its stated goal doesn't mean it's a BS project. However, when a project has failed or has ballooned in size to the extent that it will never be completed, and everyone knows it. When that happens, and no one wants to face the facts, and so the project continues to move forward, then it becomes a BS project.

`memorysluice` on hacker news thinks this form of sunk costs is often behind doomed projects:

> I had recently started a job where my new employer had been working with a contractor on their "next-gen" web application for four years, and it was nowhere near production ready.
>
> [two] weeks into the new gig, I looked at my boss and told him that it was a failed project and needed to be canned. I got the "are you kidding me, we've already got millions tied up in this project." Fast forward two years went by, and it's still not production ready.

Sunk cost bias is not a new concept, so you'd think someone would ask carefully about a project and its success and not let it just keep rolling on for years and years. But what if someone important in the org is behind the project, and people are afraid to give them the bad news?

## Executive Pet Projects

One way BS projects happen is a large company chasing something because someone with a lot of power decided it was important. An Amazon developer said this is what being on Amazon's firephone project felt like:

> Every single person involved knew we were just wasting Jeff's money and there was absolutely no chance anyone would buy it.

Whether that truly counts as a pointless project is unclear. Maybe the firephone was a speculative project from the get-go, and Bezo's knew they would likely fail but felt they couldn't communicate this lest it demotivates the teams involved?

Some software companies, though, have a repeated history of abandoned efforts. An exec will have an idea with no basis in reality, which fails, just in time for another executive to have an idea. Gregory saw this happen at a very large ERP company (yes, that one):

> We'd build thing after thing after thing that was always advertised - to the devs building it and to the customers alike - as the next best thing since sliced bread. First, java application servers, then development environments, BPM, model-driven, SOA, SOA take 2, SOA take 3.
>
> There would be an R&D-wide reorg every six months. Previous Senior Vice President would get fired or moved due to lack of results, a new one would show up, and would present us with their master plan and High-Level Enterprise Architecture of their new next best thing since sliced bread.
>
> It never worked. We'd throw it in the can and build the next thing that would never work. They'd be declared a failure in 6-12 months. We'd scrap the thing we were building - pouring our hearts into – and just start over.

Initially, Gregory liked this job, there was a lot of time for learning and an excellent mentorship program, but eventually, the pointlessness of it all can grind people down.

## Mental Health of Doom

You may think that being on a project that will never ship and never have any or many customers is great because you'll have a light schedule and can improve on some skills on the side, but Gregory found it can actually be quite taxing.

> My work would just get binned over and over, and what even was that work? Try to put it into words and explain to a layman, friend, family member - even a fellow programmer at another company, and you'd fail.

Marcelle, another developer, also found doomed projects hard to handle:

> I've never been on a team with lower morale. At one point, I realized, oh, my boss doesn't care. Oh, my boss's boss doesn't care either. I've given an identical daily update for one month [and] no one cared! It was excruciating!

So my advice to you is this: if you suspect you might be on a bullshit project, first talk to your manager or product manager and see if they can explain. Maybe things do make sense, but it is harder to see from your vantage point? But, if they deny the facts and if it feels like their explanations conflict with reality, then start planning your exit because working on a pointless project is a fast track to burnout. Because as David Graeber puts it:

> You're not even living your own lie. Most of the time, you're not even quite living somebody else's lie, either. Your job is more like a boss's unzippered fly that everyone can see but also knows better than to mention.

{% include_html cta/bottom-cta.html %}

[^1]:
    I asked these questions on a private slack group, lobste.rs and [twitter](https://twitter.com/adamgordonbell/status/1593245734723166208).

    Talking about a previous or current employer can be risky, so I've changed the name of the people I talked to in private, and I will refrain from linking to the lobster's thread (which was deleted by the mods, anyhow).

    The [hacker news](https://news.ycombinator.com/item?id=33522495) thread wasn't prompted by my question, but just a thread I stumbled on while writing this article that seems very much on topic.