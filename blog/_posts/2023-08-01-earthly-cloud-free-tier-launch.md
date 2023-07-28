---
title: "Introducing Earthly Cloud: A History of CI, and Our Take on the Future"
categories:
  - News
toc: true
author: Vlad

internal-links:
 - just an example
---

*We're excited to announce the launch of [Earthly Cloud](​​https://earthly.dev/earthly-cloud) and its no time limit free tier. Earthly Cloud is a SaaS build automation platform with consistent builds, ridiculous speed, a next-gen developer experience, and that works with any CI. It includes the functionality of both [Earthly Satellites](https://earthly.dev/earthly-satellites) and [Earthly CI](https://earthly.dev/earthly-ci) in one package. You can get 6,000 build minutes per month to be used across Satellites and CI with Earthly Cloud's free tier. [Get started free](https://cloud.earthly.dev/login).*

## The Birth of CI/CD:  From Manual Pushes to Jenkins and Beyond

CI platforms became popular at a time when we had nothing else. We just had manual pushes, ssh to prod was the way to go, and only big tech could afford some sort of in-house testing and delivery automation. Of course, automating all this is crucial. So it didn't just stay in-house at big tech giants. The emergence of Jenkins (or Hudson!), and later, CircleCI and Travis CI, made it possible for everyone to also share in the benefits of CI/CD.

!["We've hit a bottleneck transferring data between the east and west data centers."]({{site.images}}{{page.slug}}/bvxhJDE.png)

It was like going from walking to the horse and carriage and then to the Model T. We now take CI/CD for granted, and perhaps it's hard to imagine what life would be like without it. Back then, though, it was a Godsend! As an industry, the median frequency of releases dramatically shifted: from quarterly or monthly to weekly or even daily. We were able to find bugs earlier in the development lifecycle, thus reducing integration time. We were also able to gain some basic consistency in the way the build ran, because it always executed in the same environment. Time to market and lead time were reduced significantly, and we were able to shorten the feedback loop between customer requests and engineering's execution of product features.

Growing up as an industry, our DevOps hierarchy of needs has evolved too – we don't just want weekly or daily releases. We want to also be productive as a team when we work with CI/CD. We want to enable every engineer to understand it and contribute to it (in other words, to democratize it), and we want the CI/CD to work well with modern code at every scale. Every company on planet Earth is becoming a software company, and that means that there is vastly more code and more developers in the world but also fewer developers per application on average.

Back when CI/CD was taking off, things were very different. Open source wasn't as widely accepted within organizations, monorepos weren't as popular, and although inconsistent builds were common, there were bigger concerns to deal with first before we could even start thinking about a DevOps hierarchy of needs.

**The bigger concern was that of CI/CD infrastructure.** Since only big tech companies could afford it in the beginning, the limiting factor of running CI/CD within your organization was developing it and hosting/maintaining it in your cloud (or data center depending on how far back you go). Even when Jenkins became available, we no longer had to develop it, but we definitely had to maintain it. And maintain it we did. We were violently thrust into the era of ClickOps. There was no easy way to run, maintain, and configure Jenkins by modern standards. No, the main way was clicking around the UI and configuring things... And crossing your fingers that the machine's hard disk didn't fail for some reason, because then you would have to do it all over again.

Proper management of Jenkins was left as an exercise to the user. So a major part of what the DevOps role has traditionally entailed has been managing CI/CD infrastructure. And if the product, Jenkins in this case, doesn't have a solution to manage it, then you have to come up with your own. And everyone did... Their own unique solution... And this required a lot of human capital.

But you could get Jenkins to do anything. That is its strength and also its weakness. A ton of freedom, little structure, and every build shares the same environment. What could go wrong (footnote: codecov vulnerability)?

CircleCI and Travis CI later came up with the idea of managing CI/CD for you in the cloud. You no longer had to deal with the quirks and lack of maintainability and scalability that plagued Jenkins. And yet many stuck to Jenkins, just because it could do anything. Plus, Jenkins runs in your VPC. So giving access to prod was safe and easy.

Fast forward to today, and we're roughly in the same spot. The most adopted CI for greenfield apps is GitHub Actions, which is pretty much the same thing as CircleCI but next to your code. There's no differentiator, it's just easier to adopt because you already have your code on GitHub. For organizations where on-prem is a requirement, GitLab is popular, and Buildkite is up-and-coming. A huge portion of the market is still on Jenkins, usually for historical reasons.

And yet, our needs as an industry have evolved, and a glorified bash-script runner hardly satisfies them. As soon as you need to scale CI/CD, you end up with YAML spaghetti, tons of copy-pasta, and a side of 40-minute wait times. We're all suffering from some sort of boiling frog syndrome. Every project starts simple but invariably grows in complexity and so does the need for more complex build scripts, duct tape, and even some WD-40. We've accepted the current state of CI/CD as the norm and we're not jumping out of this sinking ship to save our lives. The problem of developer infrastructure complexity keeps creeping up on us and the tools of the past aren't cutting it. And the reason is pretty obvious: we haven't innovated in the CI space for over a decade.

## Advanced Build Systems: Powerful but Challenging to Implement

!["CI/CD has not kept pace with the industry"]({{site.images}}{{page.slug}}/yeI1wm4.jpg)

And yet history repeats itself. Remember how in the past only the big tech companies had some sort of CI/CD-like automation? Now a different trend is taking place. Bazel. Pants. Buck. These are next-level build systems that have an inherent understanding of the interdependencies within large codebases. Why is that important? Caching. If you know what depends on what, and you know what has changed, then you know what to rebuild and (crucially) what to NOT rebuild. Plus, it allows you to heavily parallelize independent steps. This results in MASSIVE performance boosts. And once again, pretty much only big tech companies use these build systems.

The problem with these large-scale build systems is that they are incredibly difficult to adopt unless you have the resources and access to experienced professionals that a big tech company does. As an organization, you have to go all in and swap all your builds at once, in a big-bang effort. For this reason, migration to such a system is frequently a 2-year endeavor. Just ask the Airbnb's and the Spotify's of the world. They've done it. And it's messy, hard, and requires a large team to operate. Every new language you want to onboard takes yet another few quarters.

For these reasons, these setups are inaccessible to mere mortals like you and me. They are only worth doing at a certain scale, because both the cost of switching and the cost of maintenance are high. The rest of us, just like before, are left out.

## The Rise of Developer Experience:  A Changing Perspective for CI/CD

![Developer Experience?]({{site.images}}{{page.slug}}/9hoyDo3.png)

Gone are the days when CI/CD's primary concern is the infrastructure. That is a solved problem. The more important issues at hand are of a different nature: usability, productivity, interoperability, ease of adoption, and perhaps incremental adoption. We are in a different era now. It's the era of Developer Experience.

And what do I mean by Developer Experience?

You might think of this as ponies and butterflies. Emojis in your terminal, and colored text output.

No, it's not that.

It's about making developers productive. It's about making dev tools friendly and accessible, such that the cost of adoption is low, and you don't need a whole army of people to maintain it. It's about lowering the barrier to entry. It's about allowing reusability, so that, again, maintenance is easy. It's about making it integrate with or reuse things you already know instead of ripping and replacing whole systems, reducing the time and effort of implementation and eliminating a lot of costly training. It's about allowing for incremental adoption, to make switching less risky and less costly. It's about making things consistent such that they run the same everywhere: on your laptop or in cloud-hosted CI. And finally, it's about speeding things up so developers can focus on what really matters: iterating tirelessly on the product and delivering value to the customer.

Developer Experience isn't a nice-to-have. Done right, it becomes a critical strategic business need. And you don't have to be a huge corporation to be able to benefit from it. DevEx is for the masses now. There are hundreds of open source and commercial tools on the market that are built to make developers' jobs easier.

## Introducing Earthly Cloud

I'm here to tell you that CI/CD needs rethinking. Its lack of innovation over the last decade, the inaccessibility of modern build systems, and the recent and needed emphasis on Developer Experience are all blaring, screaming signals that the way we CI/CD right now isn't going to last much longer. There will be a category-defining product (or products) that will change the way we do CI/CD.

We believe that everyone should have access to this – CI/CD that is modern like a build system, accessible like a SaaS tool, and that makes developers more productive. For this reason, we are announcing our newest offering,[Earthly Cloud](​​https://earthly.dev/earthly-cloud). Earthly Cloud is a SaaS build automation platform that gives you consistent builds, ridiculous speed, a next-gen developer experience, and it works with any CI (or as a standalone CI).

Earthly Cloud includes the functionality of both [Earthly Satellites](https://earthly.dev/earthly-satellites) and [Earthly CI](https://earthly.dev/earthly-ci) in one package. Earthly Satellites are remote build runners that make builds fast, are super simple to use, and work seamlessly with any CI (and with your laptop). Earthly CI is a full-fledged CI system that uses Earthly Satellites under the hood.

## Get Started With Earthly Cloud for Free

You can use Earthly Cloud today. Its no time limit free tier gives you 6,000 build minutes per month to use across Satellites and CI. [Get started free](https://cloud.earthly.dev/login).

{% include_html cta/bottom-cta.html %}
