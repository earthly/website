---
title: Source-available
featured: false
categories:
 - News
tags:
- license
- news
- bsl
author: Vlad
internal-links:
  - opencore
  - bsl
  - source-available
  - open core
as_related: false
excerpt: |
    Earthly, a developer tooling and cloud infrastructure company, has announced a switch to the Business Source License 1.1 (BSL) in order to ensure a sustainable business model. While the code will be available for free immediately, it will become open-source after three years. This change will not impact users unless they intend to create a competing commercial offering based on Earthly.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about Earthly's switch to the Business Source License (BSL). Earthly is a popular open-source build tool for CI that offers a sustainable business model with the Business Source License 1. [Check us out](/).**

## EDIT April 20, 2022

This article is out of date as we have since switched back to an open-source license. While we still stand for the principles in this article, our thinking has evolved and we have decided that open-sourcing is the best decision for Earthly specifically. Read more about our [switch back to open-source in the official announcement](/blog/earthly-open-source).

This article is left here for historical purposes.

This article used to be titled "Every open-core company should be a source-available company", however that aged poorly.

## Source-Available

Earthly users and prospective users - today we are announcing our switch to Business Source License 1.1 (BSL).

We would like to provide Earthly to as _many_ engineers as possible for as _long_ as possible. In order to build a project that continues to evolve, to grow, to have strong community support, and to continue to offer most of the value for free, we need a sustainable business model. We are taking steps to prevent anyone from taking advantage of Earthly in a way that could jeopardize our business model. We believe that this changes nothing for the overwhelming majority of the Earthly user-base.

## What Is BSL?

[Business Source License](https://mariadb.com/bsl11/) is a [source-available license](https://en.wikipedia.org/wiki/Source-available_software) created by MariaDB to "strike a balance between being able to run a financially viable software company while still supporting the original tenets of Open Source, such as empowering all software developers to be part of the innovation cycle". Under BSL, the code is not open-source in the spirit of [The Open Source Definition](https://en.wikipedia.org/wiki/The_Open_Source_Definition), however, the code is available for free immediately and it becomes open-source after a set period of time. In Earthly's case, the code automatically becomes open-source, under the Mozilla Public License Version 2.0, after three years.

Our intention is for the code to continue to be provided in the spirit of the pure open-source definition, with one key difference: you cannot create a commercial offering (like a CI) based on Earthly.

## What Does This Mean for Me?

Unless you are intending to take the Earthly source code, turn it into a competing CI or a build-service product, which you sell as a service, then this change will not impact you in any way.

You can continue to use Earthly like you always have. You may build unrelated commercial products that are built with Earthly. And you may even build in-house build services or CIs, as long as those are not offered commercially to third parties. However, you cannot build a commercial Earthly offering.

## What Is Earthly's Business Model?

Our business model will be based on the [open-core model](https://en.wikipedia.org/wiki/Open-core_model). An open-core model means that some amount of additional functionality is built around an open code-base. The core is free and the source is made available, while the additional functionality around the core is paid-for. Usually, the additional functionality is either targeted at large teams or enterprises, and/or is based on a managed service offering. Examples of open-core business models are [Kafka](https://kafka.apache.org/) ([Confluent](https://www.confluent.io/)), [Cassandra](https://cassandra.apache.org/) ([DataStax](https://www.datastax.com/)), the [ELK stack](https://www.elastic.co/what-is/elk-stack) ([Elastic](https://www.elastic.co/)), [Redis](https://redis.io/) ([Redis Labs](https://redislabs.com/)), [CockroachDB](https://github.com/cockroachdb/cockroach) ([Cockroach Labs](https://www.cockroachlabs.com/)) and many others.

We believe that this model has been battle-tested and is becoming the norm in the world of open developer tooling and cloud infrastructure.

## Why is a License Change Needed?

> "We believe in a model where both the creator and the society can win."

We live in a world where the power of supporting innovation is concentrated within a handful of companies. These companies have many orders of magnitude more resources than the average entrepreneur, and have the upper hand when it comes to delivering new technology to large audiences.

However, innovative ideas come from everywhere - not just the giants. Not having the same resources as a large company means that many great ideas do not turn into products, especially for startups. Some tech giants abuse their power and tip the scales in their favor, which means that we, as a society, are losing by missing out on innovation.

We believe in a model where both the creator and the society can win.

Users of developer tools and cloud infrastructure have made their voices heard and they prefer free and open software. Non-free developer tools tend to be the exception rather than the norm. The bar has been set, and we as an industry have agreed that this approach reduces the risk of vendor lock-in and enables integration that will last for a long time. Tool authors have thus adapted, and more often than not the tool comes with the source code too. The investors who back these authors are also embracing this model.

However, certain large technology companies have abused the freedom of open-source and have launched competing products offered as-a-service based on the very same code base. These competing services come supercharged with a strong platform play and seemingly infinite technical resources to pull off the effort. They are not necessarily better products, but a large company can make the offering better known through its influence. This kind of offering starves the original authors of their resources: revenue and investors. Innovation will grind to a halt as a result.

Without stable revenue and an exciting-enough story to tell Wall Street, such creators are doomed to never reach their full potential. The talent that created the innovation in the first place can no longer be sustained. When the creators are losing, the community is losing, because they end up getting sub-par support from third-parties. Such companies end up being acquired for a modest sum by yet another tech giant, a transaction that may or may not hinder their growth. The balance of power is then concentrated even further towards the large and the vicious cycle starts again.

## What Then?

> "Those who cannot remember the past are condemned to repeat it" -- George Santayana

In response to this behavior, innovators have adapted by introducing limitations to their licenses. The licenses are no longer open-source in the purest form, however, the source code is made available (hence the name "source-available license") to be used in wide applications, with certain limitations. Examples of notable switches include [MongoDB](https://techcrunch.com/2018/10/16/mongodb-switches-up-its-open-source-license/), [CockroachDB](https://www.cockroachlabs.com/blog/oss-relicensing-cockroachdb/), [Timescale](https://blog.timescale.com/blog/how-we-are-building-an-open-source-business-a7701516a480/), [Elastic](https://www.elastic.co/blog/why-license-change-AWS), [and many others](https://techcrunch.com/2019/05/30/lack-of-leadership-in-open-source-results-in-source-available-licenses/).

As creators of developer tooling and cloud infrastructure, we are incentivized to create the biggest possible positive impact in our industry. To do that we need investor support to scale the creation from a basement project to a world-class offering. To get investor support, we need sustainable revenue and a shot at becoming the next exciting company on Wall Street. And to build sustainable revenue, we need tech giants to play fair. More success stories create more grass-root creators and more excitement in investor communities, which continue to fuel this positive feedback cycle. Innovation is thus democratized. The user wins, and society wins.

If this delicate chain is broken, the end result is that innovation is hindered. Investors cannot safely bet on these companies, creators [cannot sustain open-source as a side-hustle forever](https://stackoverflow.blog/2021/01/07/open-source-has-a-funding-problem/) (they need to put food on the table) and startups cannot hire top talent to scale the innovation engine beyond a small Sunday project.

Preventing copy-cats from taking over the business model allows us as an industry to sustain this fly-wheel of innovation and continue to serve society. We believe that every open-core company should be a source-available company.

Starting with Earthly v0.5, we begin offering Earthly via BSL while continuing to provide Earthly's code freely on [GitHub](https://github.com/earthly/earthly). Furthermore, we pledge to forever do what we believe is in the best interest of the community and society as a whole.

Many thanks to everyone who has supported Earthly's vision of bringing repeatable builds to the world!

<!--kg-card-end: markdown-->