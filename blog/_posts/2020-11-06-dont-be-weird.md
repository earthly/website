---
title: Technology choice? Don't be weird
categories:
  - Articles
tags:
  - Interview
author: Corey
internal-links:
   - weird
   - design decision
topic: kubernetes
funnel: 2
excerpt: In this article, Corey Larson, lead architect at Earthly, discusses the importance of not being "weird" when making technology choices for your platform. He emphasizes the value of staying on the beaten path and only deviating when there is a strong justification, as it allows for better community support and long-term dividends.
---
_Here at Earthly, we are building an internal platform on AWS using EKS. I talked to our lead architect Corey Larson about the decisions and trade offs he is making as he designs our platform._

**The plan for the earthly internal platform says, "One thing to keep in mind as you read this is plan is `don't be weird.`" What does that mean?**

Don't be weird is the short version. The slightly less short version is: "You only have so many weirdness points you can spend. The less weird you are, the more community support you can get because you're still on the beaten path." it's just a real conscious decision you need to make.

**Do you have an example?**

If you go to great lengths to work around some default of Kubernetes or one of the tools you're using, the trouble is you've severely limited the amount of support you can get from the community.

In the past, I've worked on code with services that people made, and they hated a bunch of the defaults that Postgres was pushing on them. So they had this giant 200 and something line init script that laid down how they wanted the database to act before you could even do anything. And personally I'm just like, "Dude, just create some freaking tables, and let's get on with our life." Why are you changing all of these defaults and stuff everywhere?

**Also Postgres defaults are pretty sane right?**

I've always thought it was sane, but apparently he didn't think so. But, yeah, it's just, spend your weirdness points in the place where you're going to get the most mileage out of it, and spend them very wisely. Choosing to stay on the beaten path is just going to pay you dividends in the long run.

**So you should always choose what everybody else chooses unless you have a really good reason?**

I wouldn't even go that far. I'd say that there's a gradient here, it's not black and white. Stay on the beaten path until you have a good reason to get off. And then, document your good reason and get off the path, and consciously acknowledge the maintenance and oversight burden that you're taking on there.

**Does the Kubernetes space have beaten paths?**

There are starting to be some winners. [Kubernetes](/blog/building-on-kubernetes-ingress) itself used to be weirdness points, but it's not anymore. Kubernetes is now the lingua franca of the cloud. Who doesn't have a Kubernetes-managed platform that we could just pack up and move to, assuming we haven't chosen to spend weirdness points on platform lock-in features.

**So if we chose Docker Swarm or something, we'd have to have a really good reason.**

Yes. I would want some justification if we were choosing Docker Swarm or, Rancher 1.6 or whatever. Yeah, it's not wrong to make those choices. It's just, the weirder it is, the better justification you better have.

You've seen that CNCF landscape chart, right? There's tons of combinations out there that still haven't been tried before. It gets real easy, real fast, to get weird.

Whether you want to or not, you're going to end up in a place where nobody else has been. So you want to try to contain that.
