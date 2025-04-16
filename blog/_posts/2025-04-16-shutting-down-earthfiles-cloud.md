---
title: "A message about Earthly"
categories:
  - news
toc: true
author: Vlad
topic: earthly
funnel: 3
topcta: false
excerpt: |
    In the next three months, we will be phasing out our Earthly Satellite commercial services, including the Earthly Cloud Satellites, Self-Hosted Satellites, and BYOC Satellites, together with their respective free tiers. We are also phasing out Earthly Cloud Secrets and Logs.
last_modified_at: 2025-04-16
---
<!-- vale HouseStyle.Spacing = NO -->
<div class="notice--info">
**TL;DR**

- In the next three months, we will be phasing out our Earthly Satellite commercial services, including the Earthly Cloud Satellites, Self-Hosted Satellites, and BYOC Satellites, together with their respective free tiers. We are also phasing out Earthly Cloud Secrets and Logs.
- We are also ending active maintenance of the Earthly open-source project.
- We are supporting the community's efforts to self-organize a fork, and we encourage those interested to get involved.

</div>
<!-- vale HouseStyle.Spacing = YES -->

Dear Earthly Community,

I'll start by saying thank you for being here and for helping shape what Earthly is today. Without early adopters like you, there would be no innovation in the world. Our hearts go out to all our community members for believing in us, helping with contributions big or small along the way, and championing Earthly within your organizations.

Today marks the 5-year anniversary of Earthly. Since the launch, we've built a vibrant community of developers who share our vision for a better CI/CD experience. Earthly has been adopted by thousands of teams worldwide, with numerous integrations into diverse CI/CD environments.

From container-centric dev experiences to cache optimization strategies, we've demonstrated tangible improvements in CI speed and efficiency—providing up to a 10x ROI in compute cost savings and developer productivity. This success is a testament to the creativity and hard work of our community.

With that said, we have encountered some significant challenges when attempting to commercialize Earthly in its current form, and unfortunately, without commercial success, we are no longer able to sustain our development efforts towards the project.

## Challenge #1: Difficulty of adoption

Adopting new open-source technology is a slow process. Even the most successful infrastructure companies, like Docker, took nearly a decade to become mainstream. Despite their technical brilliance, finding a commercialization path was challenging.

In the past, venture-backed companies could rely on open-source traction alone. Hashicorp, for example, sustained itself up to Series C—six years after inception—on open-source projects like Vagrant, Packer, and Consul that weren't even commercialized.

Today, the economic landscape has shifted. Many infrastructure investors have pivoted toward AI, and there is less appetite for pure-play open-source moonshots, making early monetization a necessity.

For Earthly, the need to monetize quickly became a do-or-die situation. While Earthly has seen widespread adoption, translating that adoption into revenue has been much harder than we anticipated. Large organizations, despite initial interest, are reluctant to commit to adopting Earthly widely throughout their infrastructure. Despite many conversations, we couldn't secure any company-wide top-down deployments - only slow, organic bottom-up motions.

## Challenge #2: Open-source cannibalization

Our open-source strategy is simple: open-source the syntax and the developer experience to encourage adoption and ecosystem growth, then monetize on dev efficiencies (e.g. faster CI) via Satellites, our build runners.

To this end, we architected Earthly to allow the developer to experience the full power of Earthly locally - including the full speed benefit - while offering Earthly Satellites as a means to reuse cache between runs in CI primarily. But this meant that for some CI environments, the user could run Earthly just like they would run it locally and still get the same speed benefits. And while managing this type of installation isn't necessarily trivial, in an economy that sees massive layoffs and infrastructure budgets cut significantly, when the leadership isn't approving any new budgets, the ICs figure out a way to get the value via DIY.

So, even if the user's CI environment might have been ephemeral initially, they would switch to using a non-ephemeral environment in order to gain the Earthly speed. In short, our users were gravitating toward strategies that avoided our commercial offering (and hey, I get it, I would have done the same if I were in their shoes).

This meant that when adoption did take place bottom-up in big enough companies, we were stuck against comparing the value of Earthly to our own free, open-source offering instead of comparing it to a traditional CI/CD experience. We could no longer claim the 10x value unlock.

## What then?

There were [a few variations](https://earthly.dev/blog/shutting-down-earthly-ci/) of our solution that we attempted to commercialize, but ultimately, we believe that the barrier to entry in the space of builds & CI/CD is extremely high due to pre-existing diverse dev infrastructure that requires adaptation. At the same time, the monetization potential is significantly reduced due to CI compute being viewed as a commodity, and the developer efficiency gains are heavily discounted due to OSS canibalization, together with budget cuts across the tech industry.

And so, after exhausting several options of how to build a business around our initial product, we came to the realization that we needed a significant pivot.

As a result, we are announcing today that, unfortunately, we will no longer be able to offer Earthly Satellites as a commercial offering. All forms of Cloud Satellites, Self-hosted Satellites, and BYOC Satellites, together with all Earthly Cloud features (cloud secrets, logs, etc), will stop working in the coming months.

At the same time, we are also announcing that we will no longer be contributing actively to the [Earthly open-source project](https://github.com/earthly/earthly) other than critical bug fixes. Unfortunately, this also means that we are no longer accepting PRs since there is a significant amount of effort needed to vet them.

We understand this news is disappointing, especially for those of you who have invested time, effort, and passion into building with Earthly. Your contributions have been invaluable, and we want to ensure you have the clarity and support needed to navigate this transition.

## Community fork

In order to help the Earthly community move forward, we are looking to bring together everyone who would be willing to help maintain a community fork of Earthly. To this end, [we have put together a form where you can register interest](https://forms.gle/CMda8gNFUvmPc4Eu8). If you would be willing to provide some amount of your time weekly to help drive the community fork forward, please fill it out by **April 30th, 2025**.

The only thing that we ask of the community is to change the name and logo of the project, as well as the name of the CLI command when forking, as we want to retain trademark rights - we will continue using "Earthly" and the distinctive logo in our company's name and in future products.

## Earthly Cloud shutdown

Earthly Cloud, including Satellites, will stop working on **July 16th, 2025**. If you rely on Satellite functionality and would like to continue getting similar benefits, you can roll out your own [remote Buildkit](https://docs.earthly.dev/ci-integration/remote-buildkit). Our documentation page on [Remote runners](https://docs.earthly.dev/docs/remote-runners) explains how they work. Please note that cloud features such as Satellite auto-sleep, Satellite automatic mTLS, shared logs, and cloud secrets will no longer be available.

## Alternative: Dagger

Aside from the ongoing community fork, we have arranged with our friends at Dagger to offer a migration path to current Earthly users and customers. Although Dagger is not a drop-in replacement for Earthfiles, there are similarities in the goals of the two projects. In fact, both Earthly and Dagger happen to share Buildkit as an underlying technology.

Dagger has offered to organize a workshop for Earthly users to help evaluate Dagger more easily. Earthly customers also get 1 year for free on Dagger Cloud Pro. [More details in Dagger's announcement](https://dagger.io/blog/earthly-to-dagger-migration?utm_campaign=Earthly-Migration&utm_medium=blog&utm_source=earthly-blog).

## What's next for Earthly Technologies?

Earthly is our first product. Just like Vagrant didn't create commercialization potential for Hashicorp despite being wildly successful as an open-source project, Earthly doesn't have to bring us commercial success all on its own. We are moving forward with developing new products to add to our line. [We are announcing one such product today](/blog/lunar-launch).

We know this is not the news you were hoping to hear. For many of you, Earthly has been more than just a tool - it's been a part of your workflow, your creativity, and your successes. We deeply value every bug report, contribution, feature request, and piece of feedback you've shared with us. Without your support, Earthly would not be what it is today.

We hope that this information will help you to plan accordingly. If you have additional questions, please reach out to us at [support@earthly.dev](mailto:support@earthly.dev).

While this chapter of Earthly is coming to a close, we are committed to moving forward and building tools that solve real problems. Thank you for being part of our journey and for continuing to support us through both successes and setbacks.
