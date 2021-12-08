---
title: Earthly BSL Frequently Asked Questions
layout: page
---

<!-- vale HouseStyle.H2 = NO -->
<link rel="stylesheet" href="/assets/css/subpage.css">

<h2 class="text-2xl font-semibold mb-5 mt-20" id="what">What is the BSL?<span class="hide"><a href="#what">¶</a></span></h2>

Business Source License is a source-available license created by MariaDB to “strike a balance between being able to run a financially viable software company while still supporting the original tenets of Open Source, such as empowering all software developers to be part of the innovation cycle”. Under BSL, the licensed code is not open-source in the spirit of The Open Source Definition, however, the code is available for free immediately and will become open-source after a set period of time. In Earthly’s case, the code automatically becomes open-source, under the [Mozilla Public License Version 2.0](https://github.com/earthly/earthly/blob/main/licenses/MPL2), after three years.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="why">Why is Earthly Using the BSL?<span class="hide"><a href="#why">¶</a></span></h2>

We would like to provide Earthly to as many engineers as possible for as long as possible. In order to build a project that continues to evolve, grow, have strong community support, and continues to offer most of the value for free, we need a sustainable business model. We are taking steps to prevent anyone from taking advantage of Earthly in a way that could jeopardize our business model. **We believe that our use of BSL changes nothing for the overwhelming majority of the Earthly user base.**

Unless you are intending to take the Earthly source code, turn it into a competing CI or a build-service product which you commercialize, then the BSL license will not impact you in any way compared to an open-source license.

You can continue to use Earthly, view its code and modify it for free. You may develop unrelated commercial products that are built with Earthly. And you may even build in-house build services or CIs using Earthly, as long as those are not offered commercially to third parties. However, you cannot build a commercial Earthly offering.

Read more about our decision in [our announcement blog post](https://earthly.dev/blog/every-open-core-company-should-be-a-source-available-company/).

<h2 class="text-2xl font-semibold mb-5 mt-20" id="os">How is BSL different from an open-source license?<span class="hide"><a href="#os">¶</a></span></h2>

In the case of Earthly, the BSL license is free and open just like an open-source license, with one key exception: you cannot build a commercial competitor to Earthly (such as a CI) using Earthly while the Earthly code you are using is subject to the BSL.

After three years, Earthly becomes completely open-source, licensed under the [Mozilla Public License Version 2.0](<(https://github.com/earthly/earthly/blob/main/licenses/MPL2)>) (MPL2).

<h2 class="text-2xl font-semibold mb-5 mt-20" id="grant">What is the Additional Use Grant?<span class="hide"><a href="#grant">¶</a></span></h2>

We don't intend to limit the use of Earthly in any way other than preventing a commercial competitor to ourselves. To enable this we have added the following Additional Use Grant into the BSL:

> You may make use of the Licensed Work, provided that you may not use the Licensed Work for a Service Offering.

If your customers cannot change the build definition, artifacts or build secrets directly, then you are allowed to use Earthly for free for any application.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="serviceoffering">What is a Service Offering?<span class="hide"><a href="#serviceoffering">¶</a></span></h2>

As defined by Earthly’s Additional Use Grant:

> _A "Service Offering" is a commercial offering that allows end users or other third parties (other than your employees and contractors or a company that has contracted you to build code that incorporates the Licensed Work) to access the functionality of the Licensed Work by (i) issuing builds whose build steps are controlled by such third parties, (ii) by creating build secrets whose contents or metadata are controlled by such third parties, or (iii) by creating Artifacts whose contents or metadata are controlled by such third parties._

In other words, if your customers can change the build definition, artifacts or secrets used in a build directly, then it is considered a “Service Offering”. A common example of such an offering is a Continuous Integration (CI) system offered to customers commercially.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="production">Can I use Earthly in production?
<span class="hide"><a href="#production">¶</a></span></h2>

Yes, you can use BSL-licensed software in production according to the Additional Use Grant. The BSL and Earthly’s Additional Use Grant allows you to freely use Earthly in production as long as it is not a Service Offering.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="production2">What does “production” mean in the context of a build tool?
<span class="hide"><a href="#production2">¶</a></span></h2>

For Earthly, production is either an environment used to serve customers directly, or an environment that serves the engineering team directly. Because the CI serves the needs of the engineering team, Earthly running in CI is considered as running in production.

Using Earthly in CI is allowed for free, as long as the CI is not offered by you commercially to your customers.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="contractor">I am a software contractor. Can I use Earthly to build the code given that my client will also be able to change the build definition?<span class="hide"><a href="#contractor">¶</a></span></h2>

Yes, you are allowed to use Earthly in this context. The Additional Use Grant includes an exception for software contractors that have been hired to build code for their clients.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="faq">FAQ Disclaimer<span class="hide"><a href="#faq">¶</a></span></h2>

The explanations provided as part of this FAQ are not meant to replace or augment the terms of Earthly’s license. The FAQ is only provided as an informal explanation and is not legally binding. If Earthly’s license contradicts with this FAQ in any way, then Earthly’s license prevails.

Please see the [complete text of the Earthly license](https://github.com/earthly/earthly/blob/main/licenses/BSL) on GitHub.

<!-- vale HouseStyle.H2 = YES -->
<div class="color2">
  <div class="wrapper">
    {% include home/earthlyButton.html padding="pt-8" %}
  </div>
</div>
