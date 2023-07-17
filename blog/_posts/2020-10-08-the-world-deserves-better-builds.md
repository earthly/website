---
title: The world deserves better builds
featured: true
author: Vlad
categories:
  - News
topic: earthly
funnel: 3
excerpt: |
    Learn how Earthly is revolutionizing the build process with its self-contained, reproducible, and parallel approach. Say goodbye to slow, brittle builds and hello to a more efficient and user-friendly development experience.
---
Hello, developers of planet Earth! Earlier this year, we at Earthly embarked on a journey to bring better builds to the world. We started with a deep belief that builds should be self-contained, reproducible, portable, and parallel. In addition, we think build tools should be friendly, accessible, and down to earth - hence our name.

Today, we are pleased to announce that a number of well-respected industry veterans also share our vision and have joined Earthly's seed round of funding to fuel our growth.
<!-- vale off -->
We have partnered with [468 Capital](https://www.ft.com/content/b93d120e-5c04-458b-bfbc-b147e2e399fa), the fund of [Florian Leibert](https://www.linkedin.com/in/florianleibert/) (Mesosphere), as well as a number of creators of large developer ecosystems, such as [Spencer Kimball](https://www.linkedin.com/in/spencerwkimball/) (Cockroach Labs), [Olivier Pomel](https://www.linkedin.com/in/olivierpomel) (DataDog), [Mitch Wainer](https://www.linkedin.com/in/mitchwainer/) (DigitalOcean), [Matt Klein](https://www.linkedin.com/in/mattklein123/) (Envoy proxy), [Mirko Novakovic](https://www.linkedin.com/in/mirkonovakovic/) (Instana, [NewForge](https://newforge.de/)), [David Cramer](https://www.linkedin.com/in/dmcramer/) (Sentry.io), [Cristian Strat](https://www.linkedin.com/in/cristiangeorgestrat/) (head of trading platform Coinbase) and [David Aronchick](https://www.davidaronchick.com/) (Kubernetes, GKE). In addition, a number of institutional investors with deep experience in developer platforms have joined the round, including [Salil Deshpande](https://www.linkedin.com/in/salil/) of Bain Capital-backed fund [Uncorrelated Ventures](https://uncorrelated.com/), [Jeremy Levine](https://www.linkedin.com/in/jeremyl/) of [Bessemer Venture Partners](https://www.bvp.com/) and [Ed Roman](https://www.linkedin.com/in/ed-roman-19686/) of [Hack VC](https://hack-vc.com/).
<!-- vale on -->

## The General Sentiment Around Builds

Since our initial product launch, we've talked to several engineers, build gurus, and industry experts about traditional build tooling, and we discovered that nobody likes their build process. Builds are always a source of frustration one way or another. They're slow, brittle, too difficult to understand, inconsistent, and difficult to iterate on.

In contrast, we found out that the number one reason people love Earthly so much is its ability to reproduce failures. Reproducibility is key, because it allows people to iterate on builds quickly on their laptops without having to worry that they will break when they push to CI.

Earthfiles represent a reproducibility guarantee, ensuring that your build will run the same way on all platforms - CI, your colleague's laptop, Linux, Mac, Windows, etc. - regardless of any local specific tool chain.

People who have sought out reproducibility before Earthly have developed their own docker-based build scripts that essentially run most of the build within makeshift containers. The common problem with this approach is that the build requires constant fiddling to get right, still breaks occasionally on a colleague's computer, and is poorly understood across wider teams.

Did you know that `sed` on a Mac is different from the `sed` on Linux distributions? So is find. And so is make. And a number of other tools we take for granted. Even on Linux alone, can you be sure that your colleagues are running the same version of Python or of Java? Is JDK even installed? If all of us were build gurus, experts in the likes of bash, Makefile, and cross-system compatibility, maybe this wouldn't be such a big issue. But we're not.

These incompatibilities lead to significant inefficiencies in the software development lifecycle. Too often, teams don't even run integration tests, because they have no idea how to build the projects belonging to other teams. Beyond the typical build scripts, there are often too many unwritten assumptions, so they just give up and leave it to be caught down the pipeline, in CI, UAT… or perhaps in production.

With Earthly, we believe we can make this process an order of magnitude better.

## How Does It Work?

Docker made containers friendlier to use and widely accessible, bringing container isolation into mainstream usage. In a similar spirit, Earthly follows in Docker's footsteps, bringing together a number of important innovations into an easy-to-use package. We bring together BuildKit and OCI images and inspiration from Dockerfiles and Makefiles to make reproducible builds easier to get right and harder to get wrong.

Earthly is somewhat like a Makefile, where each target is fully isolated from one another - and, more importantly, isolated from the host environment. As they're isolated, there is no way to depend on anything you have installed locally. To bring in OS-level dependencies, you install them as part of the build, the same way you would install them in a Dockerfile. In fact, the entire Docker Hub ecosystem can be leveraged in the build process.

In a way, Earthly completes Dockerfiles. While Dockerfiles allow you to define the make-up of Docker images, Earthfiles go beyond and also allow you to run unit tests, integration tests, or to output arbitrary files (eg. binaries, artifacts, jars), not just images - all of which runs within a containerized environment, thus maintaining consistency of execution.

{% include imgf src="glue-diagram.png" alt="Diagram of how Earthly integrates as a distinct layer between build systems and CI. It replaces traditional glue scripts formed of Dockerfiles, Makefiles, and Bash files. These traditional scripts are DIY, clunky, and easy to get wrong." caption="Earthly replaces the scripting glue layer" %}

There are lots of other goodies that Earthly does beyond this, such as automatically running everything in parallel, bringing a modern import system and having native secrets and SSH agent support.

## What's Next?

Having reproducible builds is the first step in our journey. We plan to build shared caching and highly parallel cloud-based builds next. We have a deep belief that builds can create bridges between engineering teams - not roadblocks. This has become our mission, and we will not stop until we've achieved it!  
Since our launch, we've worked with our users to address their needs and make the experience as pleasant and friendly as possible. We love feedback - check out [Earthly](/), drop by our [slack channel](/slack) or tell us what you're building and how your experience can be improved.

We're excited to have you join us on our journey!

{% include_html cta/bottom-cta.html %}

> "Reproducible and parallelizable build and continuous integration, as well as explicit dependency management, are critical to scaling any organization. I'm extremely excited about Earthly bringing this functionality to existing container based build systems without requiring an extremely expensive retooling effort on top of something like Bazel. Earthly is a pragmatic and incremental solution to a thorny problem that all organizations face."
>
> -- Matt Klein, creator of Envoy Proxy
