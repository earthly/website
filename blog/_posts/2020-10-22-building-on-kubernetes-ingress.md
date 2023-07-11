---
title: 'Building on Kubernetes: Ingress'
categories:
  - Articles
tags:
  - Interview
author: Corey
internal-links:
   - ingress
   - kubernetes ingress
as_related: false
topic: kubernetes
funnel: 2
excerpt: |
    In this article, Corey Larson, the lead architect at Earthly, discusses the decisions and trade-offs involved in designing an internal platform on AWS using EKS. He covers topics such as the role of Kubernetes as a platform, the use of Ingress controllers, the benefits of Traefik over Nginx, and the importance of testing in production. If you're interested in learning about the challenges and considerations of building on Kubernetes, this article is a must-read.
---
*Here at Earthly, we are building an internal platform on AWS using EKS. I talked to our lead architect Corey Larson about the decisions and trade offs he is making as he designs our platform.*

 **What is an internal platform?**

The internal platform is really the phrase I've always used in other places. &nbsp;It's the product that's not really the product that you're shipping.

A way to think of it is your own company's internal cloud. What is the set of resources, tooling, workflows that you use to ship software to your company, which itself should really be a product that you ship to yourselves. So for Earthly, that means a whole stack of technology.

We're using AWS, we're using Kubernetes. We're hiding some parts of Kubernetes that we don't want to use from everyday usage, so we don't go there. We're making some trade-offs as to where we choose platform lock-in and where we're not. &nbsp;It's things like that. And as we add more services the platform should develop to accommodate those things in the way we choose to work.

**Isn't Kubernetes supposed to be the platform?**  
It can be, if you don't want to customize it. But the problem space there is just so large. There're so many API objects, and so many different ways to do things that you don't want to necessarily use them all. &nbsp;Otherwise your platform just gets really complicated. So, you need to choose the bits and pieces that you want to use there. And, tons of the plugins that you use will also have custom resource definitions, their own custom definitions of API objects, that's on top of the ones that already exist. So, you likely want to use those instead of the native Kubernetes ones if your software you're choosing uses those. And so it's all of that, but then there's even more.

Kubernetes doesn't do monitoring. Kubernetes generates logs, but doesn't do anything with them. Kubernetes doesn't necessarily force a deployment process or an integration kind of a process onto you as well. So Kubernetes is really just an arrow in your toolkit that kind of lets you build the rest of that, in a really nice way.

The platform should cover from the moment source code is pushed to get all the way up to this code is running in production.

## Kubernetes Ingest Strategies

**What is Ingress and how do requests get to a service inside of Kubernetes?**  
Ingress is the networking layer of how you get requests to your services from the outside. And Kubernetes doesn't really ship with an Ingress controller by default that actually performs all those functions, they want you to bring your own. And there's a ton of really interesting ones out there. There's Nginx that does that, there's people who use Caddy to do some of that stuff. There's newer ones that are cloud native. They're in that giant behemoth of a chart, the cloud native compute foundation puts up, that gets memed all the time on Twitter.

The way it works is a request comes from the internet and it's going to hit some kind of a load balancer usually. We're using one of Amazon's application load balancers, but in the past I've just used even regular HAProxy or things like that. And from there, it bounces into your cluster. Your Ingress controller is going to pick it up, figure out where it should go, which services it should get routed to and route it to that service. And then, your service will generate a response and it follows these layers of the onion back out.

**Which Ingress controller are we going to use?**

The one's like Traefik. It's still like a traditional ingress controller. And I find that that's just a little more straightforward, it's less complex. It fits with the way I like to build services where you don't have a giant sea of microservices, a little bit better.

**What is a service mesh?**

People took the opportunity with it being a new landscape with lots of containers in a large, orchestrated environment to build service meshes. Istio is out there, as one example there, and they have their own huge API with all their CRDs and everything else to create these service meshes that route things around and figure out who's where. I personally find them pretty complex, and I like to avoid them. I like more standard comprehendible routing approaches.

**I've usually seen people use Nginx. So why not Nginx, and why Traefik?**

Back when I first was doing some Kubernetes work, we were spinning up our first cluster. We were in Azure and we were, they didn't have a managed offering at the time we were using some deployment script from Azure team to get it up and running. And, I don't remember what we were using for Ingress. I remember there was the Calico networking layer in there, but... We would do things, and then suddenly the cluster would just stop routing traffic entirely. And, among other things, we chose to move off of Azure. So we went to AWS, and we actually started trying to work with the Nginx proxy. And it uses your standard Nginx server configuration to do a lot of configuration. Personally, I always have to Google a lot on those configuration files, cause they can get pretty complex

But we tried Traefik, and it just kind of worked, and all of the options of things we wanted to do were first class citizens, in terms of route matching and everything else to get the Traefik where it needed to go. And so, we just stuck with it. At the time, the guy I was working with, he would make fun of me a lot, cause I liked to use Go. And I hesitated to suggest Traefik to them early on, because their mascot's the go gopher with the traffic cones and everything else. And I didn't want them to think I was more of a fan boy than I actually was. So I held off suggesting it to him for a while. So we spun our tires a little longer on Nginx than we should have. And I think it's gotten better since then, but I just have enough knowledge around how Traefik works in it.

**Have you ever used Nginx Lua scripting?**

Infrastructure should be declarative, at least in my book. I don't want a program that I have to then debug to figure out what my configuration actually is. For better or worse, a pile of [YAML](/blog/intercal-yaml-and-other-horrible-programming-languages) is not going to change on you once you ship it somewhere else, and it's not going to have bugs. It's all there, it's all declarative. You can put it in Git, and see who did what, when, to your infrastructure.

**When do you think we would consider using a service mesh?**

I've seen it used in a lot of places where people just have a ton of different microservices. I'm not a fan of services that small. I'm a much bigger fan of slightly larger services that are, right-sized, to do things. And I've never found something like a service mesh to be useful, that useful in that kind of an environment.

**What are other important decisions about ingress you had to consider?**

We are terminating SSL in the ingress layer. That way your applications don't necessarily have to worry about that. Pluses and minuses again, everything's a trade-off. But that's what we're choosing to do just because it makes things a little more easily visible and debug-able.

The downside is if someone was in our cluster they could see what's going on between services. But, that is the tradeoff we are making for now.

**What about Deployment strategies?**

Kubernetes has a few of those baked in, where it'll roll through, and you can set how many or maximum amount available, and how many extra can I spin up to give myself headroom while I'm rolling in a deployment. But there's more to it than that because that does let you get to more or less, zero downtime.

Kubernetes will handle that, "Hey, no more traffic comes to this node." And then we'll spin it down as soon as all the traffic there is exhausted and spin up new ones, and let those get routed to. It'll handle all that for you, and that's really nice.

But, there's more to it than that because there's the whole adventure that takes place before it's live in production taking traffic.

## Testing in Production

What I'm hoping to do for us as we're going forward here is, that we can stick new deployments out on production in some small way, and then use our Ingress controller to send it some traffic. Then we can actually [test](/blog/unit-vs-integration) the new version of the code in production without affecting anybody as a canary before we choose to roll that actually out to everybody.

Service meshes are a little bit better at this, then simple ingress controllers. This is one place that service meshes do succeed, but Traefik can do it well enough too, where you actually split percentages of your request volume to one deployment versus the other.
