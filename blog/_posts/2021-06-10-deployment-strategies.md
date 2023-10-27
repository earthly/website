---
title: "Deployment Strategies"
categories:
  - Tutorial
author: Adam
toc: true 
sidebar:
  nav: "deployment-strategies"
internal-links:
 - deployment strategies
 - deployment
 - continous deployment
excerpt: |
    Learn about different deployment strategies, their pros and cons, and how they can impact downtime and deployment complexity. Find the best approach for your application and gain insights into optimizing your deployment process.
last_modified_at: 2023-08-17
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you're into deployment strategies, Earthly can streamline your build process. [Check it out](/).**

There are many ways to deploy applications to a production server environment, and the terminology around deploy strategies is often confusing. In this short guide, I'll review software deployment options starting from the most basic and straightforward and moving towards the more complex.  

## Recreate Deployment Strategy

This is the most straightforward deployment strategy. It's been the default strategy in enterprise IT for a long time and works well when updates are very infrequent and maintenance windows plentiful. You stop the old service and then start up the new service. During the teardown and spin-up process, the service is down.

In a software-as-a-service world, with frequent updates, this strategy can really only work with the use of queues and asynchronous messaging architectures. For example, when upgrading a service that sends email, the mail will queue in an outbox waiting for the upgraded version to start up.

<div class="no_toc_section">
### Pros
</div>

* Easy
* Works excellent with queues and asynchronous message buffers
* Never need to run more than one version of the service in parallel

<div class="no_toc_section">
### Cons
</div>

* Downtime to upgrade
* Downtime to rollback

## Rolling Update Deployment Strategy

The recreate strategy above assumes you only have one instance of your service running at a time. But if you have several with a load balancer in front, you can improve the downtime story with a rolling update strategy. You start an instance of the new version, and once it's up, gracefully terminate one instance of the old version. Then continue this pattern until only new versions of the service are running. This strategy is ubiquitous in Kubernetes and other containerized production environments.

<div class="no_toc_section">
### Pros
</div>

* Easy on Kubernetes
* No Downtime on upgrade

<div class="no_toc_section">
### Cons
</div>

* Multiple versions of same service active during the overlap
* No warm rollback services

## Blue-Green Deployment

A [blue-green deployment](/blog/blue-green/) requires a bit more resources: you need two identical production environments and a load balancer. One of these environments always receives 100% of the traffic while the other version sits idle. Updates are deployed to inactive version, and once it is successfully upgraded, traffic is switched over to it. These two environments are named blue and green, respectively, and traffic alternates back and forth from green to blue and then blue to green and so on. This means that the previously deployed version is always running on the idle environment, which simplifies rollbacks.

<div class="no_toc_section">
### Pros
</div>

* Eliminates upgrade downtime
* Very quick rollbacks

<div class="no_toc_section">
### Cons:
</div>

* More Resources
* More Deployment complexity

## Canary Deployment

A canary deployment strategy looks a lot like a blue-green deployment -- a new version of the service starts up parallel to the existing version -- with a slight improvement made: instead of switching all traffic over to the new version, only a percentage of traffic is initially sent. This traffic is the canary in the coal mine. Canaries were used in mining to measure air quality. The miners would bring a canary with them as they traveled down into the mine. If there was an air quality problem, the canary would die before the miners and act as an early warning signal.

In the same way, a canary deployment does not prevent downtime, but limits its impact by giving an early warning. It limits access to the new version to a subset of users. If [incident management metrics](/blog/incident-management-metrics) indicate that the new service is not responding well to this fraction of requests, then the roll-out can be aborted, lessening its impact. If everything looks OK, request volume is slowly ramped up until its being entirely served by the new version.

Depending on how the canary traffic is chosen, a downside to this approach is that a specific subset of users may experience most of the production issues.

<div class="no_toc_section">
### Pros
</div>

* Catch Problems Early

<div class="no_toc_section">
### Cons
</div>

* Deployment complexity
* Canary users bear the brunt of production issues

## Shadow Deployment

If the problems a canary deployment finds can genuinely be found with metrics alone, and if the cost of incidents is very high, then a shadow or mirrored deployment is worth considering.

In a shadow deployment, the new version of the service is started, and all traffic is mirrored by the load balancer. That is, requests are sent to the current version and the new version, but all responses come only from the existing stable version. In this way, you can monitor the latest version under load without any possibility of customer impact. This strategy is sometimes called a mirrored canary deployment.

The cost of this approach is in the implementation. A service mesh like Istio is probably needed to perform the actual request mirroring, and it gets more complex from there. If a new version of a user service backed by a relational database was shadow deployed, all users might be created twice, leading to untold ramifications. To embrace a shadow or mirrored deployment strategy, you have to think about the implications of duplicated requests, and any non-idempotent actions on downstream services may need to be mocked.

<div class="no_toc_section">
### Pros
</div>

* Catch production problems without custom impact

<div class="no_toc_section">
### Cons
</div>

* Deployment complexity
* Architectural complexity

<div class="no_toc_section">
## Summary

There's a wide range of deployment methods, each with its pros and cons. The best strategy depends on your need to balance downtime cost and deployment complexity. If you're keen to streamline your build process before deployment, you might want to give [Earthly](https://www.earthly.dev/) a try.

If you'd like to learn about other deployment strategies or continuous deployment terms, feel free to contact us through [Twitter](https://twitter.com/earthlytech) or [email](adam@earthly.dev).
