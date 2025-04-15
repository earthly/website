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
**TLDR:**

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

Today, the economic landscape has shifted. Many infrastructure investors have pivoted towards AI, and high interest rates have made LPs prioritize non-venture opportunities. As a result, there is less appetite for open-source moonshots, making early monetization a necessity.

For Earthly, the need to monetize quickly became a do-or-die situation. While Earthly has seen widespread adoption, translating that adoption into revenue has been much harder than we anticipated. Large organizations, despite initial interest, are reluctant to commit to adopting Earthly widely throughout their infrastructure. Despite many conversations, we couldn't secure any company-wide top-down deployments - only slow, organic bottom-up motions.

## Challenge #2: Open-source cannibalization

Our open-source strategy is simple: open-source the syntax and the developer experience to encourage adoption and ecosystem growth, then monetize on dev efficiencies (e.g. faster CI) via Satellites, our build runners.

To this end, we architected Earthly to allow the developer to experience the full power of Earthly locally - including the full speed benefit - while offering Earthly Satellites as a means to reuse cache between runs in CI primarily. But this meant that for some CI environments, the user could run Earthly just like they would run it locally and still get the same speed benefits. And while managing this type of installation isn't necessarily trivial, in an economy that sees massive layoffs and infrastructure budgets cut significantly, when the leadership isn't approving any new budgets, the ICs figure out a way to get the value via DIY.

So, even if the user's CI environment might have been ephemeral initially, they would switch to using a non-ephemeral environment in order to gain the Earthly speed. In short, our users were gravitating toward strategies that avoided our commercial offering (and hey, I get it, I would have done the same if I were in their shoes).

This meant that when adoption did take place bottom-up in big enough companies, we were stuck against comparing the value of Earthly to our own free, open-source offering instead of comparing it to a traditional CI/CD experience. We could no longer claim the 10x value unlock.
