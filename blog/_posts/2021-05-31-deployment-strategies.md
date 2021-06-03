---
title: "Deployment Strategies"
categories:
  - Reference
author: Adam
---
There are seemingly many ways to deploy applications to production. The terminology around various deploy strategies is often confusing.  In this short guide we will review deployment options from simplest to most complex.

## Recreate Deployment Strategy

This is the simplest deployment strategy and what was used in much software development in the past when uptime requirements were not as important and maintenance windows were common.  You stop and possibly remove the old service and then start up the new service.  During the tear down and spin up process the service is down. Although with use of queues and async responces can make this strategy quite effective.

Pros:
 * Easy
 * Works great if service input can be queued during switch over
 * Never need to run more than one version of the service in parrelell 

Cons:
 * Downtime to upgrade
 * Downtime to rollback

## Rolling Update Deployment Strategy

The recreate strategy above assumes you only have one instance of your service running at a time. But if you have more than one with a load balancer in front of them you can easily improve the downtime story.  You start an instance of your new version and once its up, gracefully terminate one instance of the old version and continue this pattern until all instances are the new version. This strategy is very common in kubernetes and other containerized production environments.

Pros:
 * Easy on Kubernetes 
 * No Downtime on upgrade

Cons:
 * Multiple versions of same service active during overlap
 * No warm rollback services

## Blue-Green Deployment

In Blue-Green Deployment you have two identical production environments and a load balancer.  This requires double the resources of the simple recreate setup but with many benefits. One of these environments, starting with blue, is always receiving 100% of the traffic while the other version sits idle.  Updates are always deployed to idle version and once successfully up traffic is switched to the new version. Because of this traffic moves alternates back and forth from green to blue each deployment. Roll-backs can also be done quickly because the previous version is always running on the idle environment. 

Pros:
 * Eliminates upgrade downtime
 * Very quick roll-backs

Cons:
 * More Resources
 * More Deployment complexity

## Canary Deployment

Canary Deployment looks a lot like Blue Green deployment: a new version of the service is started up in parrelel to the existing version with a slight improvement made: Instead of switching all traffic over to the canary, only a percentage of traffic is intially sent.  This traffic is the canary in the coal mine. Canaries were used in mining to measure the air quality. If their was an air quality problem, the canary would die before any miner would indicating something was seriously wrong.  In the same way a canary deploy does not prevent downtime, but limits it to a subset up users. If metrics indicate that the fraction of traffic sent to the new version is not responding well then the roll-out can be stopped and its impact will be reduced. If that is not the case, traffic slowly switchs completely over to the new version.

Depending how traffic is choosen for the canary a downside to this approach couble be that a certain subset of users may experience most of the production issues.

Pros:
 * Catch Problems Early

Cons:
 * Deployment complexity
 * Canary users bear brunt of production issues

## Shadow Deployment

If the problems a canary deployment identifies can truly be found viaing measuring metrics than a shadow or mirrored deployment can help identify those issues without any customer impact.

In a shadow deployment, the new version of the service is started and all traffic is mirrored by the load balancer. That is it is sent to the current version and the new version, but all responses are sent only from the current version.  In this way the new version can be monitored without any possiblity of customer impact. This is sometimes called a mirrored canary deployment.

The cost of this approach is in implementation.  If a user service back by a relational database was shadow deployed, then all users could be created twice leading to untold ramifications.  To embrace a shadow or mirrored deployment strategy cases like this must be considered and non-idempotent actions on downstream services may need to be mocked.

Pros:
 * Catch production problems without custom impact

Cons:
 * Deployment complexity
 * Architectural complexity


## Summary

There are many deployment methods, from the very simple to the very complex.  The deployment strategy the works best for any given situation depends on many factors. When choosing a deployment strategy balancing the cost of downtime versus the cost of deployment complexity is important. If there are other deployment strategies, or other continous deployment terms you would like to see covered please reach out to us on [twitter](https://twitter.com/earthlytech) or via [email](adam@earthly.dev).
