---
title: "When to use Bazel?"
categories:
  - Articles
toc: true
author: Adam
sidebar:
  nav: "bazel"
internal-links:
 - bazel
excerpt: |
    Learn about the benefits and challenges of using Bazel, Google's open-source monorepo build system, from experts who have experience with it. Discover when to use Bazel, its history, case studies, migration tips, and the future of this powerful build tool.
last_modified_at: 2023-07-11
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about when to reach for Bazel. If you are looking for a simpler approach to monorepos then [check us out](/).**

## Bazel Build?

Here at Earthly, we care a lot about builds and talk to many people about their struggles with builds and CI. A frequent topic of conversation, especially if an organization has a monorepo and more than 500 developers, is Bazel, Google's open-sourced monorepo build system.

I've never worked at Google or anywhere using Bazel to drive their builds, and so while I can walk through a Bazel tutorial, I felt like I was missing the sense of what using Bazel was like, both the day-to-day and migrating to Bazel. So I interviewed 6 Bazel experts[^1] and asked them what they like about Bazel, when they would use it, and what to expect or consider before doing a Bazel migration.

**Read this if you are considering Bazel and also if you'd like to read gory details of several Bazel migrations, including the level of effort and the results.**

The experts all have experience moving to Bazel and using it day-to-day., including two people who do Bazel migrations for a living, at least one Bazel contributor, and one person, Oscar Boykin, who has been on Bazel projects at Twitter, Stripe, and Netflix.

It's a long read, and I promise, it's worth it. The short version is: **Bazel can solve large monorepo build problems very well, but it has a steep adoption curve.**

## History

Bazel is based on some simple but powerful ideas. Here is Oscar Boykin[^2] explaining:

{% include quotes/oscar.html %}
The idea of Bazel is we're gonna actually build things correctly. Your build is a pure function. There's sources that come in, and then the artifacts go out. And if the sources are the same, the artifacts that pop out the other side will be bit-for-bit identical. That's really cool.

And so the pitch of Bazel is that we will be fast by being correct. At Google scale, they can't afford not to cache. And the only way caching is safe is if it's correct. So the idea is speed-through-correctness. Whereas a lot of people viewed them in tension with one another.

Every programmer has the experience of saying, 'oh the build, broke! Let's just clean it.' It's like the reboot of like builds. It's awful. Why should you have to reboot your build?

So with Bazel, you don't have to do that. You really can build without cleaning. That's amazing. I mean, it's sad that that's the bar, but it's real, and so Bazel really delivers on that.
{% include quotes/end.html %}

Back in the early days of Google, Bazel was designed to replace a giant [makefile](https://bazel.build/about/faq).

<div class="pl-8">
A long time ago, Google built its software using large, generated Makefiles. These led to slow and unreliable builds, which began to interfere with our developers' productivity and the company's agility. Bazel was a way to solve these problems.
</div>

<!-- vale HouseStyle.OxfordComma = NO -->
Google needed Bazel at the time because they had a large monorepo that contained large amounts of C++, and Java code, and they wanted a uniform, correct and performant way to build and test all this code. Son Luong Ngoc[^3], a scalable build consultant at Qarik Group, says many larger companies are starting to hit these problems.
<!-- vale HouseStyle.OxfordComma = YES -->

{% include quotes/son.html %}
So your backend might be in Go or Java, right? There's a front end in react JS. And oh, those data science guys are using Python and Scala, right? And here, these infra people are using Go, Rust, C, C++, and Lua, right? How do you glue all that together to create a cohesive developer experience? A lot of enterprises in recent years start reaching this scale.

So previously, nobody was reaching this scale before, except mostly Google and Facebook. They were about eight to 10 years ahead of the rest of the market. So they actually care about this kind of problem. But now everybody [else] is catching up.
{% include quotes/end.html %}

As people left Google and worked at places with large monorepos, they ended up writing ports of Bazel. Pants was a Bazel clone used at Twitter and Foursquare. Buck was a Bazel clone built at Facebook. Others like Alibaba or Netflix, who didn't have a monorepo or as many languages in use, built their own solutions that tackled problems differently.

Son:

{% include quotes/son.html %}
So yes, folks actually built their own, but these are very expensive. Like you, you need a team the size of a small startup to build this kind of platform. Nobody's got the money or time for that, right? They want to focus on the business objective.
{% include quotes/end.html %}

## Open Sourcing

Then Bazel was open-sourced. That's when Son saw this idea spread:

{% include quotes/son.html %}
Dropbox becomes one of the very first adopters of Bazel and then BMW. And then, slowly, slowly, the ecosystem starts to converge around Bazel.
{% include quotes/end.html %}

It's not just multi-language changes that force large companies onto Bazel. It's also a monorepo with many services in it. Son hit this at Booking.com with one of their monorepos:

{% include quotes/son.html %}
We started with every push going directly into trunk, which is our main branch of the monorepo, and each was creating about 120 CI jobs, and I was the guy who was told to take all those 120 jobs and try to make something reasonable out of them using a dynamic CI pipeline.

And I also managed a whole fleet of GitLab runners and our setup for artifactory. So I was the person who was on call when our CI system got DDoS by our developers [ committing too fast] or when our CI system was DDoSing our GitLab instance because every single push was creating hundreds of containers [for testing] and just fetching the code took down our GitLab storage layer. How do we scale that up?

So eventually, we were like: Hey, maybe capturing dependency information from production in our CI is not the way to go. Maybe we should do declarative dependencies within our code base of this monorepo, and Bazel became a perfect fit.
{% include quotes/end.html %}

## When To Use

### When to Use Bazel - Oscar's Opinion

Oscar's a Bazel contributor who's been involved in Bazel projects at Twitter, Stripe, and Netflix. He got involved with Bazel in an fascinating way:

{% include quotes/oscar.html %}
So I joined Twitter in 2011. And so I saw Pants kind of grow up. And then, in 2015, Bazel was open-sourced. And so we asked the question should we adopt Bazel?

And because I wasn't that vested in the Pants side, I was like part of the crew that investigated Bazel.

And that's when I became very impressed with Bazel. I thought it had really great design and all the principles were really good. And so I actually wrote the first Scala rules. And then those became what's called the rules_scala, and pretty much I think most everybody who's using Bazel with Scala uses those rules.

And we used those [rules] in production at Stripe, I joined Stripe in very early 2016, and we're using them at Netflix, so I've got a lot of experience with [Bazel].
{% include quotes/end.html %}

Bazel is a very specific tool. Oscar thinks it would be a mistake to adopt it if you don't really need it.

{% include quotes/oscar.html %}
Would I recommend [Bazel]? I would not. You know that scene in the fellowship of the ring [where] they're saying should they go under a mountain, and [Gandalf] is like, no, I would not take that route unless there was no other opportunity?

Basically, Bazel is that: don't use it unless you have to.

So if you're only working in one language and you have a relatively small amount of code, let's say like less than a hundred thousand lines, I almost certainly would not use Bazel if it were me. If I were working on an open-source library, I almost certainly wouldn't use it because Bazel's not so great at publishing reusable libraries for others. You can publish deployable artifacts fairly easily, but it's not great right now, maybe won't ever be great, at publishing reusable libraries.

When would I definitely use it?

I would definitely, unfortunately, use it when I had a million lines of code or more. If you have multiple languages that you have dependencies between – like in our [Netflix] case, we're doing a lot of machine learning, but we do data processing in Scala, but we then package up some apps that have like Python for model scoring or model training – so there are dependencies because these systems pass data between one another, maybe then you want to consider Bazel. Each of these would be like maybe-Bazel? And if you accumulate enough of them, you give Bazel a try. I think once you get over like 5 million lines of code, I really wouldn't do anything other than Bazel. It's almost the only game in town.
{% include quotes/end.html %}

## When to Use Bazel - Jason's Opinion

Not everyone would wait for millions of lines to use Bazel, though. Jason Steving[^4], an ML Compiler Engineer on the TensorFlow team at Google, has a different take:
<!-- vale HouseStyle.Repetition = NO -->
{% include quotes/jason.html %}
Always. Always use Bazel.

So I come with a super biased opinion on that that I think that building a monorepo only has benefits for code reuse. Whereas the alternative is difficult to work with.

Here's where I'm gonna struggle to give you any like good counter advice is like, I haven't really used other build systems that much. I left Google a year ago, and I worked at Amazon for like eight months, and I did use their build system there.
<!-- vale HouseStyle.Repetition = YES -->

And I have since come back to Google because honestly, one of the big portions I hated [was] the build system.

Amazon, at least Prime Video, they absolutely do not reuse code. Everyone rewrites the same thing, no matter how trivial the code is. It's such a bad practice. Like for very simple things like, oh, this is gonna customize my login, and everyone needs to do it - everyone writes that code. Literally, they will copy-paste it. That grated against my soul!

And that happens because they were using this build system that like was built around this idea of copying files. And you had to tell it where a file is. So you had to then end up duplicating their build file because they would copy all their files, and then whatever thing they did to generate code, you need to also do in yours to generate code. Whereas in Bazel, if you generate code, there's a target for it. You just depend on the target, and you get the generated code.

So, in my experience, if your project gets significant, beyond a few files, I think you're already ready for Bazel. Like if you have more than one package of code, like a Java package, and especially if you do code gen, then you are ready for Bazel.
{% include quotes/end.html %}

I don't think Jason's opinion is rare within Google. Bazel, as Blaze, was created to solve the challenges of Google's code base, so it's no surprise that it works well there and that people who've spent a lot of time using it make a strong case for everyone using it.

But other places seem to do well without Bazel, Son says:

{% include quotes/son.html %}
I've been through multiple organizations over the past few years. Alibaba was a multi-repo shop [and] they can succeed with a multi-repo setup. They don't need something like Bazel [because] they completely survive [using] Maven and Spring Java.

So it's very clear to me that Bazel is not the key to success.

There are startups out there that only use one language or one software stack, and that's very easy to build. It's a trade-off between costs and [the] return on investment, and the organization needs to make that call. I have seen a range of customers who arrive at different answers in terms of addressing problems of scale.
{% include quotes/end.html %}

## Bazel Case Studies

### Case Study: Netflix Recommendations

Netflix is a multi-repo company where Java code predominates. But as Oscar shares, even in a multi-repo organization, certain code bases can start getting pretty big and slow to build.

{% include quotes/oscar.html %}
I work at Netflix, and Netflix mostly has a multi-repo style. They are very famous for the kind of freedom and responsibility culture. So each team pretty much can do what it wants.

I work on the recommendations algorithms, and the team I'm on, somewhat recently, merged several different algorithms that are part of the whole recommendations product into one team and one repo. And so it's not all of Netflix, but it has a kind of monorepo feel about it because several unrelated projects got jammed into one repo and the build performance was pretty bad.

So I had used Bazel previously, and I was like, you know what, I don't wanna mess with this. I'll just keep working, you know, we'll just keep using it, and I just won't get involved – I won't get pulled into this again.

But the CI times were so long. I mean, we were like maybe 250,000 lines of code, maybe 300,000 lines of code in this repo. It's not a gargantuan amount of code. And the CI times are like 45 minutes in some cases, sometimes an hour, and it was really affecting productivity.

And so then we are faced with this question that a lot of people don't think about if they're working in small orgs or [in] small repos.
{% include quotes/end.html %}

The problem Oscar's team was having was conflicting code getting merged in.

{% include quotes/oscar.html %}
Your PR can be green, and my PR can be green. But if you merge both of them, that will break the build, right? Because like they actually conflict. And that was hitting us more and more frequently that someone would make an incompatible change in their PR. the CI would be green, and the other one would be green. Now it's like 45 minutes. They don't really want to fool with it. They go ahead and merge it. And we detect failures later because we also run a CI on the main branch after it got merged and before we go and deploy things, but still, it's annoying. Main should never break like it shouldn't be possible because it should have already [been] tested before it goes in.
{% include quotes/end.html %}

There is a solution to this problem, though.

{% include quotes/oscar.html %}
We said you know what? We're only gonna allow fast-forward merges into Main. And now this 45-minute or one-hour CI time became basically almost unworkable because they had to be linearized and [if] someone else beats you, you've gotta merge it again. Now it's another hour, you know?

So I was like, you know what? I guess we have to do Bazel. Because Bazel really works for the pitch that it makes. If you set up the build and like you have good rules, and the caching works, it's gonna work.

Previously, when I was quoting like 45 minutes or an hour, those might be the 90th percentile or something. The median build time went from 20 minutes down to six minutes, or maybe it was even a little less.

So now, you've pushed the code, you're filling out the PR, [and] the CI's already green or red. You don't really feel that block and that linearization of the PRs is not a problem at all. No one notices, no one cares. And we made a little (linearization) bot also because we wanted to make it nice. And people don't even think about it anymore. So this linearization of main isn't a problem anymore.
{% include quotes/end.html %}

## Bazel Build Time Expectations - Tweag

Moving from 20 minutes median build to 6 minutes seems like an impressive improvement, especially if the tail build times improved by a similar magnitude. I reached out to a build migration expert Andreas Herrmann[^5], from Tweag, to see if these types of improvements are what people should expect.

{% include quotes/andreas.html %}
The problem with these kinds of numbers is that they're highly dependent on the particular project. So it's very difficult to really make a general statement.
For example, one project I had worked on we did a migration where at the time switching to Bazel, [we] reduced the build time by 40%. And that was on sort of the common, incremental build cycle. So the previous build was using the native tools. They were also doing [an] incremental build, and nonetheless, it was an improvement.

It was a project where a build from scratch was somewhere on the order of an hour or two hours, depending on how many components you added. But the common developer use case of a build was somewhere less than four minutes.

So after the migration to Bazel, the build would still be one to two hours, but with all the caching and incremental features, it was actually 40% less than the original incremental build of 4 minutes.
{% include quotes/end.html %}

So they had brought the 4-minute incremental build time down by 40%! Andreas has found though, that some projects are limited by integration test speed, and so Bazel's ability to speed things up is limited:

{% include quotes/andreas.html %}
Ideally, [a build] should be in the few-minutes range. Now in practice, that can be tricky to achieve [even with] Bazel, especially if you have things like long-running integration tests. Something we've seen in the past is where Bazel makes builds really fast, but there were still large integration tests, and the teams prefer to still have them in pre-merge checks. And if one integration takes half an hour, there's little the build system can do to improve things.
{% include quotes/end.html %}

Even if build times are limited by integration tests, there can be other advantages. For instance, Andreas finds often times non-Bazel solutions to incremental compilation have issues.

{% include quotes/andreas.html %}
I mean, usually, people before have found some kinds of workarounds to have some sort of incremental build. Like they'll have persistent build workers or something like this, but they come with other kinds of costs. For example, the build might be less stable, or it might occasionally get into a bad state.
{% include quotes/end.html %}

Properly used Bazel does not have this issue. Builds run faster because they are more correct, not less so. To Andreas, much like Oscar, this correctness property is important.

{% include quotes/andreas.html %}
Tweag specializes in strongly typed functional programming. So correctness and reproducibility, and purity are important to us. When Google open-sourced Bazel back in 2015, we were very interested in it because it has this focus on fully defined build dependencies. It's something that fit well into our set of values.
{% include quotes/end.html %}

Correctness is not just about speed. Andreas says it can become especially important if you are generating code across languages:

{% include quotes/andreas.html %}
Let's say you have a simple web app with the Haskell backend, and you're using servant to describe your API. Then you have all your API definitions in Haskell code.

Ideally, you wouldn't want to duplicate all the API definitions for the frontend. You want have some tool to generate it. And there are lots of bridge packages. But with native build tooling there isn't really a great way to do this, and [so] one frequently has to run a 'make clean' and do [a] fresh build. Bazel is very well suited to capture these kinds of things. One can define a Bazel target for the library that defines the API, define a Bazel target for the binary that does the code-generation, and the generated sources is just going to be a build artifact.

Then one can define a library target for the frontend that uses those generated files as regular code source inputs, and it's just gonna work from there automatically. So these kinds of complex dependency graphs become really challenging with the native tools but are pretty easy to express in Bazel.
{% include quotes/end.html %}

## Bazel Case Study: Open Systems

Andreas and others at Tweag were such big fans of Bazel (And Nix, but that might be a different article) that they started writing about it to [spread](https://www.tweag.io/blog/2019-10-09-bazel-cabal-stack/) the word. From there, other people found Bazel. Like Julien Perrochet[^7], who was working at Open Systems at the time.

{% include quotes/julien.html %}
I think I first heard about it probably 2018, or 2019-ish.

The learning curve was pretty hardcore. And we basically shelved the idea for a while. And then, my company, we merged into a legacy Java shop (Open Systems). They existed for like 25-ish years, and build times were slow. That triggered all our [research into Bazel]. And we said Okay, hey, let's reevaluate Bazel for that.
{% include quotes/end.html %}

Julien and a small team made a case for Bazel and got buy-in from the company. The problem was convincing the developers:

{% include quotes/julien.html %}
There's a natural resistance to change. There's inertia [because] people are used to a workflow, and you're like coming in with completely crazy ideas like smaller builds, smaller targets. It takes some convincing.

And if I had to do this again, I'd spend more time on communicating [with] the developers. I'd probably spend more time on educating people, finding out who's motivated, who's interested, and then [spending] time on these people to get them on board.
{% include quotes/end.html %}

Julien recommends getting some firm commitments about switching over to Bazel because at Open System waffling about the switch-over took up a lot of time.

{% include quotes/julien.html %}
We had this back and forth where it was like show us it's working before we commit to it.

And then at some point, we said, okay, screw it, we're going to force the whole thing. We're going to migrate this over. We did this in a not-so-elegant way over the holiday.
{% include quotes/end.html %}

After the switch over and some adjustment time, developers came around to Bazel's benefits because of the reduced feedback time:

{% include quotes/julien.html %}
Before you would try something, like will the test pass or not, and then you have a feedback loop that's at least 20 minutes and generally more.

You have a pretty big code base. And now it's just let's just try something. And then you quickly see, is it breaking the build? Once I've written the code, I'll have an answer within even less than five minutes that 'Hey, is this breaking everything, or is there a chance that this will actually work?'.

So that was the best. It's super hard to put in place [but] once you give it to people and they have the basic control to quickly iterate again. Like suddenly, they're happy to be learning to write BUILD files. So it was a two years adventure.
{% include quotes/end.html %}

## Bazel Migration Tips

Because Julien recently finished a two-year migration of a large org, he has a lot of great tips to share about migrating to Bazel and what to expect.

{% include quotes/julien.html %}
You need a critical mass of people who will understand [Bazel]. It doesn't have to be a lot, but be more than one person or it might be a waste of time.

You need people who are who can think on their own. If you have people who are used to, you know, copy-paste build engineering from StackOverflow, it might not be optimal.

So you need to have a few people who are willing to take some time, the same thing with your PM. Like management as well. You know, [a manager who say] "we understand why we need time for this".
{% include quotes/end.html %}

Julien also says the number of languages in use really affects the project's timeline.

{% include quotes/julien.html %}
We migrated some Java. We did it for Scala. We had some Go, and we had some TypeScript and some Python. And each time – this one of the traps is to think, okay, I did it with go, and it took me a long time, so Bazel Java is going to be easy.

I mean, it's probably not Bazel's fault, but it's not abstract – It's giving you primitives to run some other build system like to run the Java compiler or the TypeScript compiler or whatever, and it's super leaky. it's not abstracting away these things because each build tool is a bit different.

[The] transferability from one language to another is not a given. Each time it's new. Each time we did something new, [we'd be] like 'Yeah, should take a week' and then one month later it would be done. The amount of things you actually need to look into and learn is pretty huge.

And so the upside is you have a much deeper understanding of build systems, and then you end up hating all of them equally.
{% include quotes/end.html %}

On the plus side, Julien found that Bazel changed how he tackled certain problems. He's no longer afraid to make a mess.

{% include quotes/julien.html %}
Some things are extremely natural in Bazel that I haven't found anywhere else. Like if you have a dirty bash script doing things, and you forget [running] them [it's a problem], but Bazel just gives you this good layer of abstraction: Just put your tool in here, define what's going in, what's going out, and you can stack these things or combine them together ad infinitum.

Things before Bazel that I would find extremely dirty, like Open API definition languages that TypeScript will spit out. If you do this with makefiles, it starts getting really brittle. If you do it with Bazel, you can do really dirty duct taping of things together, and then once it works, you have pretty good Bazel guarantees.

That was a weird side effect of Bazel: just really duct tape these three tools and three different languages together, and it works.
{% include quotes/end.html %}

## Bazel Case Study: Tink

Julien's Bazel adoption experience at Open System, much like Oscar's at Netflix, is rooted in understanding the Bazel principles and choosing to adopt them. Another common vector for Bazel adoption is just having someone who's X-Google join the company and start trying to recreate Google's internal dev tooling.

Jens Rantil[^6], while working at Tink, a fintech startup, had this form of introduction to Bazel:

{% include quotes/jens.html %}
The funny story is that we, we essentially had a Googler or a Xoogler, I guess, who briefly joined us for like six months and added a bunch of googly tools. He added Kubernetes, and he introduced Prometheus, and he introduced Bazel, and then he kind of disappeared.
{% include quotes/end.html %}

The big feature of Bazel that helped Tink hasn't been mentioned so far:

{% include quotes/jens.html %}
One really amazing thing is they have really great querying capability, which allows you to query the build targets and for a larger repository when you kind of wanna figure out like, okay, give me all the Java binaries that depend on this particular library over here. That helped us a lot when we suddenly had to do security upgrades of some dependency, or [when] we wanted to understand the impact of something, or we wanted to understand how to refactor things.

We also used Bazel query logic to actually check whether we needed to redeploy a service in our CI pipeline.
{% include quotes/end.html %}

## Bazel Migration Tips

### Migration Challenge: Java

Julien at Open Systems had some hiccups with Java users as well.

{% include quotes/julien.html %}
If you're like expecting this whole [thing to be] perfect, if you're using Maven or Gradle and you're used to having your IDE perfectly integrated with the build system, you can get there, but it'll take resources. And then people just expect, 'Hey, I just want to write Java code, that's not, not my job', then you're running into trouble.
{% include quotes/end.html %}

But generally, everyone I interviewed mentioned that Java works fairly smoothly with Bazel. It's other languages where things can be more of a struggle.

### Migration Challenge: JavaScript

Julien, at Open Systems, found getting an acceptable frontend experience out of Bazel to be the hardest language-specific challenge. Front-end devs didn't like losing hot reloading.

{% include quotes/julien.html %}
They managed to adopt it, especially when they were working with the back end: [when] they needed a Java service running – so it was still a net benefit to be using this. But then we would onboard a new recruit, and he didn't have all the memory of the pain [of standing up the backend service]. If it's taking one minute, we're like yeah! and he's like, no, it has to be like 10 seconds.
{% include quotes/end.html %}

Julien did find that experienced front-end devs were able to get a Bazel workflow working that they liked, but it wasn't straightforward:

{% include quotes/julien.html %}
If you have a front-end person who understands how his front-end tooling works, which is pretty rare [then they can get hot reloading to work]. But it's hard to do by copy-pasting things from stack overflow.

You need to understand what's going on, and then you can have someone working with their tooling and be reasonably efficient. It's a surprisingly good way to filter out if you have a senior front-end developer, ask them things about build toolchains, and you can quickly know which one knows their stuff [because] it's a complicated mess.
{% include quotes/end.html %}

Andreas at Tweag has had to overcome this difficulty as well. He says JavaScript's tooling has a larger feature set, and Bazel can't reproduce all of it:

{% include quotes/andreas.html %}
For example, these node modules folders that exist at a specific place and have the entire subtree in it or the way how you can code changes into a running server instance, these kinds of things are very difficult to integrate into a system that tries to sandbox things and then there may be a bit more resistance [to adopting]

Sometimes it can also be a valid approach, in that case, for these specific components to maintain both build systems: have people develop with native tools to get the fast feedback cycle, but then have Bazel for the full integration.
{% include quotes/end.html %}

### Migration Tip: C++

The language tooling picture is not all caveats and frustration, though. Andreas, from Tweag, says that some language communities benefit from Bazel's ergonomics and are very quick to adopt it:

{% include quotes/andreas.html %}
A good example of this is C++. it's not per se that the tooling isn't great. It's just that C++ has such a long history and was created at a time when things like editor integration or package managers weren't really around. So it's such a heterogeneous ecosystem, and there's so many situations where the tooling isn't great. So Bazel will actually be a great improvement [on] what they had before, and then people are very quick to jump on board cause they see, oh, this is actually much, much easier to use.
{% include quotes/end.html %}

## Migration Warning: Overhead

Andreas has learned, in his time doing migrations to Bazel, that it's important to set expectation upfront about the level of effort involved:

{% include quotes/andreas.html %}
So something that I think is fair to say about Bazel is that it does add complexity to a project, and it has a fair maintenance cost. So migration projects take a while to make happen. And the reason is that for Bazel to work the way it does, it tracks the inputs and outputs of build actions very precisely. It tracks every individual files, and it has certain expectations about where files appear on the file system and where outputs can be written, and so on. And these are assumptions or constraints that are not shared by all the tools out there. So there is a overhead there in terms of migration.
{% include quotes/end.html %}

Also, the infrastructure setup for Bazel can take some time to set up and should be factored in:

{% include quotes/andreas.html %}
You need infrastructure [and] it's a space that is still developing.

So there's gonna be some integration effort to get a remote cache and remote execution set up that works for the project. So if it's a small project, if it's a small team that cannot onboard and assign, you know, some number of people to these kinds of tasks, then may not be a good choice yet.
{% include quotes/end.html %}

So, if you're not prepared to provision and manage some servers, Bazel, as a distributed system, won't be a good fit for you. Though for most places at the size where they are considering Bazel, this is less of an issue.

## Migration Challenge: Writing And Maintaining Build Files

The biggest change when moving to Bazel is writing and maintaining BUILD files. This can feel unnatural and like boilerplate or busy work if you are used to build systems where inputs and outputs are inferred. Jason from Google finds this overhead slows him down when refactoring.

{% include quotes/jason.html %}
Like it does feel sometimes like I made a small change, you know, I'm making a refactoring [and] my IntelliJ will just move the file and like update all the references in the other files that point at this thing and that's wonderful.

But then IntelliJ doesn't know about my build targets. And so like the build target got moved along with everything else. And I mean, sometimes that works, like sometimes in Google, the build target automatically gets updated if you use a tool.

But when I'm working on [claro](http://clarolang.com) then, I have to like manually follow the Bazel error messages to update the targets of everything. And it'll become a thing that will prevent me from doing refactorings because I'll be like that's gonna be such a pain to update all my build targets. [So] I save it to be a project where I'm like: today the only thing I'm gonna do is just move build targets around.
{% include quotes/end.html %}

## Migration Helper: Gazelle

Andreas says solutions to managing, generating, and updating BUILD files are a current area of focus for the Bazel community.

{% include quotes/andreas.html %}
The Bazel community as a whole is working on automation. So that one doesn't have to do all this by hand. So a popular idea there is build file generation and I think the most popular tool there is called [gazelle](https://github.com/bazelbuild/bazel-gazelle), which comes from the Go, but is extensible and is being extended to different kinds of language support.

So that thing can do things like go through your project and look at the source files and see what modules a particular source file depends on and then generate the build definitions or update the build definitions to capture these new dependencies.

And what's interesting about it is that it works in a way where it can integrate its results with preexisting build configuration files. And that's interesting because it's very difficult to create automation of this kind to always work in 100% of the cases. Cause in most languages, there's some weird mechanisms that make it really difficult to do that.

So you can have your customization points where you say this target is a bit weird because I don't know why, historical reasons, and so I'm going to make some custom changes, and I can put a special comment telling the tool I know this is weird, but please leave very alone.
{% include quotes/end.html %}

Oscar, at Netflix, ended up building his own BUILD file generating tool.

{% include quotes/oscar.html %}
[Gazellel] doesn't support Scala and in my experience with Google projects, like, if it works great, use it. But you probably don't want to get into trying to contribute to it as an outsider. But for something like how a generator should work for Scala, I didn't really want to get into it, so I just built a tool that does it.
{% include quotes/end.html %}

Oscar's tool parses all the recommender code and builds a dependency graph, even in Scala code, which was considered hard to do, and emits build files.

{% include quotes/oscar.html %}
So I spent on a month making a build generator for Java and Scala, and we've been able to use it with very, very few manual annotations. There's probably 10 of those in a repo of like, you know, 250,000 lines of code.
{% include quotes/end.html %}

So, it may be possible for a sufficiently motivated team to build a BUILD file generator tailored to their use case if Gazelle is not a fit.

## The Future of Bazel

As support for generating build files grows, Jason ( who's building his own programming language Claro ) hopes Bazel can become a universal build solution. He imagines every programming language having Bazel rules and then being able to offload the hard work of building at scale to Bazel. I ran this idea by Oscar.

{% include quotes/oscar.html %}
I would love for that vision, what he is describing, to be true. And I can see how it could happen and even still could happen, but it's not obvious that it's going to happen because there just isn't that momentum. They don't have 20 companies sending PRs every day to Bazel.

I used to pitch it as Bazel could be like a Linux-type project for programming. You know, you could use free BSD, and some people do, but for the most part, you're gonna deploy Linux, and we could get to a world where you just build your code with Bazel.

You've made a new language [and] you're not gonna make a new build system or package manager. You're just gonna like write some Bazel rules. I totally agree with that vision. The difference is look at how Linux is developed.

Everybody can and does contribute to Linux. It has its own direction. It has a leader that is able to, whatever his prickliness, make that project work. There's no like Linus for Bazel [because] ultimately at the end of the day [Bazel] is some people trying to get promoted at Google.

The problem [with Bazel] is it's like been like seven years [and] Bazel is getting better, but it's a Google open-source product. And Google's basically like: 'Hey, just do it our way and you're probably an idiot, and you don't have our scale. Your problems are kind of - like any intern at Google can sketch a solution to your problems. They're not real problems' and that's not true.

And so you have to wrestle with this, and you have to deal with them probably not responding if you send in a PR. You can just kind of browse the issues or PRs on Bazel Build, and they're just like graveyards. It's nobody's job to read or respond to the PRs. Nobody gets promoted at Google for responding to them. So things that they're basically getting to now were things they were like talking about in 2016.

If you look at the rules_python, it's, it's kind of an embarrassment. It's like clearly, totally unfunded by Google. And it's like, I don't really get it. I don't know what they're trying to get out of Bazel here. Can they really not afford to put two or three people on it full-time to make it good? I guess they are choosing not to, but I don't really understand why that is [the case].
{% include quotes/end.html %}

So Oscar is disappointed in where Bazel is today but only because he saw so much promise in it when it came out. He wants it to be more than it is today. Jason echoes the potential Oscar originally saw in Bazel. He sees it as an extension of what your programming language can do that forces good design decisions.

{% include quotes/jason.html %}
So I guess what I like is that it doesn't require you, but it almost forces you to like make very small and composed packages, and then on top of that, you layer the visibility system and all of a sudden you get like, almost full control over who can depend on what, in a way that even like your language does not give you.
{% include quotes/end.html %}

Jens echoed this, saying the emphasis on small packages in Bazel helped him as a Staff Engineer guide developers to write smaller units of code that could be reused. And that hints at probably the most promising future vision for Bazel: a world where large tech orgs use Bazel, scalable testing practices and static analysis to guide developers in writing code that scales with the organization size. A way to escape Conway's law.

## Conclusion

So after talking to all of these Bazel experts, what have I learned? First, I've learned that Bazel's adoption costs can be high, but its value can be worth it. Writing BUILD files and maintaining them is a cost potential adopters should plan for because switching to Bazel isn't like switching from Maven to Gradle or switching from Dockerfiles+Makefiles to Earthfiles. It's a larger lift that involves setting up build and cache servers and potentially requires getting a bit into the weeds of how the software you create is built, down at the compiler and file-system level.

Second, I've learned you shouldn't overlook the education and training aspects either. You should plan to spend time initially getting developers up to speed on this approach. Make sure everyone understands the vision or expect some bumpy roads.

But most importantly, I've learned - and all the people I talked to agreed: Bazel does deliver on its promise of fast and correct builds. Other tools like Pants and Buck exist, but Bazel is the clear category leader. If I had a mono-repo with several million lines of code in it, I'd want a consistent way to build things and a fast way to get feedback on those changes. Doing so would pay for itself over time because developer time is expensive. Bazel is the tool for that job.

If I had less than a million lines of code or I was worried about the adoption costs or if wanted a more gradual approach to monorepo build performance, then I'd take a look at [Earthly](/). But then I work for Earthly so I'm a bit biased.

{% include_html cta/bottom-cta.html %}

[^1]:  Quotes have been edited for clarity.
       Thank you Oscar, Son, Jason, Andreas, Jens, and Julien for letting me pick your brains about builds.

[^2]:  <img class="h-24 md:w-24" style="border-radius: 50%;" src="{{site.images}}{{page.slug}}/0610.png" alt="Oscar Boykin">
       [P. Oscar Boykin](https://twitter.com/posco) is a Bazel contributor, Senior Research Engineer at Netflix, and former physicist, who has worked on Bazel projects at Twitter, Stripe, and Netflix.

[^3]:  <img class="h-24 md:w-24" style="border-radius: 50%;" src="{{site.images}}{{page.slug}}/0910.png" alt="Son Luong Ngoc">
       [Son Luong Ngoc](https://twitter.com/sluongng) is a Dev Ops Engineer at [Qarik group](https://qarik.com/), where he specializes in MonoRepo and Bazel migrations. Before Qarik group he helped booking.com handle the challenges of larger mono-repo.

[^4]:  <img class="h-24 md:w-24" style="border-radius: 50%;" src="{{site.images}}{{page.slug}}/1050.png" alt="Jason Steving">
       [Jason Steving](https://www.linkedin.com/in/jasonsteving/) is an ML Compiler Engineer on the TensorFlow team at Google and is the creator of [Claro-lang](https://www.clarolang.com).

[^5]:  <img class="h-24 md:w-24" style="border-radius: 50%;" src="{{site.images}}{{page.slug}}/1250.png" alt="Andreas Herrmann">
       [Andreas Herrmann](https://www.tweag.io/team/) is a physicist turned software engineer. He leads the Bazel team at Tweag, and maintains Tweag's open source Bazel rule sets and the capability package. 

[^6]:  <img class="h-24 md:w-24" style="border-radius: 50%;" src="{{site.images}}{{page.slug}}/0270.png" alt="Jens Rantil">
       [Jens Rantil](https://mobile.twitter.com/JensRantil) is a Senior Software Engineer at Normative and former Staff Site Reliability Engineer at Tink.

[^7]:  <img class="h-24 md:w-24" style="border-radius: 50%;" src="{{site.images}}{{page.slug}}/1510.png" alt="Julien Perrochet">
       [Julien Perrochet](https://j3t.ch/) is an independent consultant at Perrochet Reactive Systems. Julien was formerly a Principal Software Engineer at OpenSystems where he was responsible for, among other things, build engineering.
