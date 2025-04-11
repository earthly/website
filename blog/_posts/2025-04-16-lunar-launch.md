---
title: "We Interviewed 100 Eng Teams. The Problem With Modern Engineering Isn’t Speed. It’s Chaos."
categories:
  - news
toc: true
author: Vlad
topic: earthly
funnel: 3
topcta: false
excerpt: |
    Earthly Lunar is revolutionizing how engineering teams measure and improve their SDLC with universal monitoring that works with every tech stack, microservice, and CI pipeline. Lunar allows you to set engineering guardrails centrally, and roll them out gradually across your entire organization, ensuring code quality, security, and compliance requirements are consistently met.
last_modified_at: 2025-04-16
---

Last year, our team spent a lot of time interviewing fellow Platform, DevOps, DevEx, CI/CD, and SRE engineers, as well as engineering leaders, in order to better understand their day-to-day challenges. We began this effort to see how [Earthfiles](https://earthly.dev/earthfile), one of our products, could serve engineering teams at scale. But as we spoke to more and more people, we realized that platform engineering as an industry is on a collision course with something far more painful and visceral than just [build speed](https://earthly.dev/blog/the-roi-of-fast/).

It was the summer of 2024, and we needed to turn open-source success into commercial success for Earthfiles. Eleven thousand GitHub stars. How hard could it be to monetize that traction?

To make venture-scale money, we needed to go up-market and figure out what makes mid-size companies and enterprises tick and how our product might be able to help them. So we started interviewing platform and engineering leaders across the industry. DocuSign, Affirm, Roblox, Palo Alto Networks, Twilio, LinkedIn, Box, Morgan Stanley, BNY, and many more. We spoke to over 100 of these.

We started with a simple question:

> What are the top issues that you're struggling with in your day-to-day work?

We were hoping to get validation that developer productivity is a top concern and then be able to further narrow down how CI/CD speed would be able to unlock developer efficiency. But of all these interviews, only one mentioned build speed as a top issue, and it was largely biased by a recent production incident where they couldn't get the fix out quickly enough due to a slow end-to-end CI/CD process.

In fact, the top issues they typically mentioned had nothing to do with productivity - not on the surface, anyway. It had to do more with how to best manage the engineering chaos that becomes inevitable at scale. You see, in the era of containers and microservices, there has been a general trend for companies to give more and more freedom to individual dev teams. It's a container - it slots in nicely in production, and there's less of a concern about what's **inside** the container. [^1]

The increased freedom results in an **explosion of diversity** at the dev infrastructure layer. You'll find a mix of programming languages, CI technologies, build scripts, packaging constructs, in-house scripts, adapters - you name it. Every team's setup is a unique snowflake. Even within the same programming language ecosystem, different teams will set up their dev process completely differently. Completely different build, test, packaging logic. Completely different runtime versions. Completely different eng culture. So on and so forth. This craziness is now the norm. [^2]

[^1]: Whereas previously, writing a component in the wrong language would simply be incompatible with production altogether. Remember the Java servlet days?

[^2]: There are several exceptions still, of course, like the Google's and Facebook's of the world. Companies born before the era of containers, and more generally, companies who have invested heavily in common CI/CD infrastructure for one reason or another. But most enterprises aren't like that.

## "Explosion of diversity"

This core problem of tech stack diversity is what we heard more commonly in our interviews. The interesting aspect of it is that different companies explained it differently to us, and different personas in the organizations were impacted by different consequences.

Platform teams complained about the constant firefighting required to support every app team's unique needs. App teams on the other hand are focused on shipping features quickly - they complained about having to reinvent the wheel over and over again, by being slowed down by rigid deployment blockers, and by being given production readiness requirements that they learned very late in the process. Security teams complained about not having any visibility into the chaos. Engineering leadership complained about not being able to enforce high-quality engineering standards and not being able to understand the level of maturity of each app.

Everybody complained in their own way about the same fundamental core issue: **extreme tech diversity is impossible to govern efficiently.**

## The goal isn't total standardization

The other thing we heard loud and clear is that going back to the pre-microservice era of more standardized tech stacks isn't a solution. Freedom is useful and necessary. It enables innovation. And hey, for many orgs, even if they suddenly thought that freedom is a bad thing, it would be impossible to go back and rewrite all the existing functionality to make the tech stack consistent. It's just too much work.

We took it all in.

The industry is seemingly facing a catch-22. You can't have strong innovation without freedom. You can't have high-quality engineering and security without standardization.

We became obsessed with this problem: How do you preserve freedom, but still enforce the right standards at scale?

## How organizations deal with this today

After speaking to over 100 engineering leaders, we identified a handful of common strategies for dealing with engineering chaos. Each has its strengths but also major weaknesses.

1. **Common CI/CD Templates** – Centralizing workflows via reusable templates works well for companies that adopted them early. But in mature orgs, adoption is rarely 100%, and maintaining consistency is a losing battle.
Problem: Rigid, difficult to retrofit, and often resented by app teams.
2. **Manual Checklists** – Reviews per PR or before launches. Cheap and flexible, but prone to human error and rubber-stamping.
Problem: Inefficient, inconsistent, and lacks ongoing visibility.
3. **Scorecards (IDPs)** – Great for accountability and high-level visibility. But they're shallow, with limited CI/CD support and no shift-left feedback.
Problem: Issues are discovered too late, and enforcement is manual and inconsistent.
4. **Individual Vendor Tools** – Best for depth in specific areas like code scanning, testing, or licensing. But without unification, coverage remains inconsistent and fragmented.
Problem: Too many dashboards, poor integration, no centralized control plane.
5. **DIY Solutions** – Custom internal systems provide deep insights but are costly and hard to maintain.
Problem: Scalability issues, limited shift-left feedback, and incomplete enforcement.
6. **Doing Nothing** – Policies without enforcement. It's compliance theater: the intention is there, the tools exist, but there's no way to track or govern what's actually happening across teams.
Problem: Inconsistent enforcement, lack of visibility, massive risk.

Each approach tackles part of the problem in some way but none solves it entirely.
