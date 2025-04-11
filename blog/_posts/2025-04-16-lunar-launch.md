---
title: "Earthly CI: Launching a new era for CI"
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

## We Interviewed 100 Eng Teams. The Problem With Modern Engineering Isn't Speed. It's Chaos

Last year, our team spent a lot of time interviewing fellow Platform, DevOps, DevEx, CI/CD, and SRE engineers, as well as engineering leaders, in order to better understand their day-to-day challenges. We began this effort to see how Earthfiles, one of our products, could serve engineering teams at scale. But as we spoke to more and more people, we realized that platform engineering as an industry is on a collision course with something far more painful and visceral than just build speed.

It was the summer of 2024, and we needed to turn open-source success into commercial success for Earthfiles. Eleven thousand GitHub stars. How hard could it be to monetize that traction?

To make venture-scale money, we needed to go up-market and figure out what makes mid-size companies and enterprises tick and how our product might be able to help them. So we started interviewing platform and engineering leaders across the industry. DocuSign, Affirm, Roblox, Palo Alto Networks, Twilio, LinkedIn, Box, Morgan Stanley, BNY, and many more. We spoke to over 100 of these.

We started with a simple question:

> What are the top issues that you're struggling with in your day-to-day work?

We were hoping to get validation that developer productivity is a top concern and then be able to further narrow down how CI/CD speed would be able to unlock developer efficiency. But of all these interviews, only one mentioned build speed as a top issue, and it was largely biased by a recent production incident where they couldn't get the fix out quickly enough due to a slow end-to-end CI/CD process.

In fact, the top issues they typically mentioned had nothing to do with productivity - not on the surface, anyway. It had to do more with how to best manage the engineering chaos that becomes inevitable at scale. You see, in the era of containers and microservices, there has been a general trend for companies to give more and more freedom to individual dev teams. It's a container - it slots in nicely in production, and there's less of a concern about what's inside the container. [^1]

The increased freedom results in an explosion of diversity at the dev infrastructure layer. You'll find a mix of programming languages, CI technologies, build scripts, packaging constructs, in-house scripts, adapters - you name it. Every team's setup is a unique snowflake. Even within the same programming language ecosystem, different teams will set up their dev process completely differently. Completely different build, test, packaging logic. Completely different runtime versions. Completely different eng culture. So on and so forth. This craziness is now the norm. [^2]

[^1]: Whereas previously, writing a component in the wrong language would simply be incompatible with production altogether. Remember the Java servlet days?

[^2]: There are several exceptions still, of course, like the Google's and Facebook's of the world. Companies born before the era of containers, and more generally, companies who have invested heavily in common CI/CD infrastructure for one reason or another. But most enterprises aren't like that.
