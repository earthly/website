---
title: "The Canary Deployment Strategy and When to Use It"
categories:
  - Articles
toc: true
author: Keanan Koppenhaver
sidebar:
  nav: "deployment-strategies"
internal-links:
 - canary
excerpt: |
    Learn how canary deployments can help you catch bugs and regressions early in your application deployment process. Discover the benefits and downsides of this strategy, as well as how to implement it effectively.
last_modified_at: 2023-07-14
---
**In this article, you'll learn how the canary deployment strategy requires vigilant monitoring and swift rollback options. Earthly ensures your builds stay consistent and reliable. [Explore how](https://cloud.earthly.dev/login).**

As you're building your application, you want to ensure that your customers have a bug-free user experience as much as possible. Since bugs show up most often when new code is deployed, your deployment process should be set up to catch bugs or regressions early and then quickly deploy patches into production before those bugs affect users.

Implementing a CI/CD pipeline is of course a great first step. Automated testing and automated deployments eliminate much of the error-prone nature of manual deployments. However, even with development environments that mimic your production environment, you can never be completely sure that your deployment will be bug-free. This is where *canary deployment* comes in.

## Before You Dive into Canary Deployment

If you want to get started with canary deployment, there are just a couple crucial processes to have in place.

If a canary deployment reveals a problem, you need to be able to revert that deployment and take the application back to a previously stable state quickly. In most cases, this means having some sort of CI/CD pipeline that can be run quickly. If your deployment pipeline takes a half hour to run or if you're still deploying changes manually, you're going to have issues rolling back when you identify a problem with canary deployments.

If you already have a fast, reliable deployment pipeline in place, why would you want to switch to canary deployments?

For one, implementing a canary deployment process will force your organization to ensure that your rollback pipeline is straight-forward and fast. All of your DevOps tooling has to be faster and more reliable, simply because there is no other choice.

In addition, the canary deployment strategy can be a great way to ensure that the majority of your users experience zero downtime, even in a world where not all deployments can be perfect. Because this strategy allows operations teams to detect problems sooner, downtime can be more easily avoided, even on large-scale or complicated deployments.

And the biggest benefit by far with canary deployments, and how it differs from other deployment strategies, is that when you run a canary deployment, your changes are deployed to just a subset of users. You can observe any negative effects, like increased error rates and decreased app performance, to the overall system before rolling out updates to the rest of your user base.

## How Canary Deployments Work

If your organization has a solid DevOps setup but is still struggling with buggy deployments, user complaints, and app instability when deploying your software, you definitely want to consider adding canary deployments into your workflow. Let's take a look at how they work.

You'll need two different production environments for canary deployment. Let's call them environment A and environment B.

In the standard state of the application, only one of these environments receives traffic. However, when you initiate a deployment, you only deploy your new code to *one* of these environments. So after your initial release, environment A has not been touched yet, but environment B has the new version of your application running on it. You then use a piece of your infrastructure (usually a load balancer) to direct a subset of your traffic to environment B—this is how canary deployment differs from blue-green deployment. This subset is often 10 percent, but the exact breakdown varies by organization and how much traffic your application gets.

If, after a certain period of time, none of the warning signs of a bad deployment are present, you can transition 100 percent of your traffic to environment B, so that all your users are now experiencing the new version. This leaves environment A ready to be the "canary" environment for the next deployment.

## Canary Deployment Benefits

There are some definite benefits to getting the canary deployment model configured on your infrastructure. For one, having an environment that's a true production environment, even when it's receiving limited or no traffic, allows you to ["test in production"](https://www.browserstack.com/guide/testing-in-production). Thanks to tools like Docker, local and staging environments can be quite similar to production environments, but there will always be differences between them, even if it's just the amount of traffic they receive. Having a separate production environment set up for canary deployments allows you to test in production easily and, with the proper monitoring and deployment pipelines, safely.

One common objection to testing in production is that your entire user base will be affected if any of your changes are buggy. However, with canary deployments, you limit the effect of any potentially negative change.

In addition, having two production environments allows you to run A/B tests much more easily, even when you're not running canary deployments.

## Canary Deployment Downsides

As great as using canary deployments can be for your organization, there are some downsides to this approach as well.

If your organization is used to only maintaining one production environment, doubling this to now maintain two environments comes with increased cost and complexity. If your deployment tools are used to only deploying to one environment, they now have to be aware of both environments, which one they should be deploying the canary deployment to, how to shift traffic through your load balancer to begin to expose users to the canary deployment, and much more.

A second potential difficulty revolves around deciding how to segment the traffic that gets the canary deployment when it's first released. If you expose too large of a percentage of users to the new deployment, the strategy becomes less effective in limiting the downside of a bad deployment, but if you expose too few users, you might not be able to effectively detect any issues that will occur when you release the changes to 100 percent of your traffic.

## Other Deployment Methods

One you have canary deployments implemented, your organization may benefit from building off of it into more complex models, such as [shadowed or mirrored deployments](https://earthly.dev/blog/deployment-strategies/). These deployments are a bit more complicated to implement, however, as your organization scales in complexity, both of these strategies can provide even more deployment flexibility for complex features while still limiting the user-facing impact of a bad deployment.

## Wrapping Up

As your application, and more importantly your user base, grows, you want to be sure that any bugs or bad deployments are relatively limited in scope and easy to fix while impacting as few customers as possible. Rolling out any changes to a subset of your customers using the canary deployment strategy can be a great way to do this.

Many of the difficult pieces of implementing a canary deployment system can be mitigated with a tool like [Earthly](https://cloud.earthly.dev/login). Earthly helps manage and automate your build process, which is a key component of managing the added complexity of a canary deployment process. With Earthly, all builds are containerized, repeatable, and language agnostic, ensuring that you get consistent results no matter what language or infrastructure your application currently uses.

{% include_html cta/bottom-cta.html %}
