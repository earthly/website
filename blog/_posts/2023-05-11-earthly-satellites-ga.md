---
title: "Announcing General Availability of Earthly Satellites"
categories:
  - News
toc: true
author: Gavin

internal-links:
 - just an example
excerpt: Learn how Earthly Satellites can speed up your CI builds, share compute and cache with your team, and execute builds on different architectures. Find out why users like Ses Goe from NOCD are raving about the performance and simplicity of Earthly Satellites.
---

We're excited to announce that [Earthly Satellites](https://earthly.dev/earthly-satellites) have moved from Beta to General Availability (GA)! Satellites are remote build runners managed by the Earthly team. Satellites make builds fast, are super simple to use, and work with any CI as well as builds triggered from your laptop.

## Why Use Earthly Satellites?

Earthly Satellites come with their own cache that is local to the satellite. This means that builds are faster when executed repeatedly on a satellite. This can be especially useful when using Satellites from a sandboxed CI environment, where the cache from previous builds would not otherwise be available or it would take time to download and upload.

## Typical Use Cases For Earthly Satellites

* Speeding up CI builds in sandboxed CI environments such as GitHub Actions, GitLab, CircleCI, and others. Most CI build times are improved by 2-20X with Satellites.
* Sharing compute and cache with your coworkers or CI.
* Executing builds on x86 architecture natively when you are working from an Apple Silicon machine (Apple M1/M2) and vice versa, arm64 builds from an x86 machine.
* Benefiting from high-bandwidth internet access from the satellite, allowing for fast downloads of dependencies and pushes for deployments. This is particularly useful if you are in a location with slow internet.

## How Earthly Satellites Work on Your Laptop

* You kick off the build from the command line, and Earthly uses a remote satellite for execution.
* The source files used are the ones you have locally in the current directory.
* The build logs from the satellite are streamed back to your terminal in real time, so you can see the progress of the build.
* The outputs of the build - images and artifacts - are downloaded back to your local machine upon success.
* Everything looks and feels as if it is executing on your computer in your terminal.
* In reality, the execution takes place in the cloud with high parallelism and a lot of caching.

## How Earthly Satellites Work in Your CI

* The CI starts a build and invokes Earthly.
* Earthly starts the build on a remote satellite, executing each step in isolated containers.
* The same cache is used between runs on the same satellite, so parts that haven't changed do not repeat.
* Logs are streamed back to the CI in real time.
* Any images, artifacts, or deployments that need to be pushed as part of the build are pushed directly from the satellite.
* Build pass/fail is returned as an exit code, so your CI can report the status accordingly.

I could go on and on about how Earthly Satellites works and why it's great, but, instead of having to trust me, I interviewed Ses Goe, a Satellites user, so you can get his unbiased feedback on Satellites.

## Interview With Earthly Satellites User, Ses Goe From NOCD

<!-- vale off -->
### Tell me about [NOCD](https://www.treatmyocd.com/)
<!-- vale on -->

{% include quotes/earthly_satellites_ga/ses.html %}

OCD is a global health epidemic in the sense that 2% of the world's population is estimated to have OCD. Our mission at NOCD is to restore hope for people with OCD through better awareness and treatment. We provide a particular type of therapy, called exposure and response prevention therapy, which has been clinically shown to be the most effective treatment for people who have OCD.

{% include quotes/end.html %}

<!-- vale off -->
### Tell me about your role at NOCD
<!-- vale on -->

{% include quotes/earthly_satellites_ga/ses.html %}

My technical title is Director of Internal Tools, but we're small so I end up touching a little bit of everything. I would say that my primary responsibilities involve really anything internal – internal dashboards that we use for billing and marketing, internal systems we use to make the process when doctors refer people to us smooth, etc. Anything that our greater corporate employees handle I'm probably in some way responsible for maintaining.

{% include quotes/end.html %}

<!-- vale off -->
### Before Earthly, what tools did NOCD use for builds and CI?
<!-- vale on -->

{% include quotes/earthly_satellites_ga/ses.html %}

We primarily used GitHub Actions with plain old Docker. And builds were notoriously really, really, really, really slow. It was not uncommon to have our CI/CD pipeline take an hour to run all the way through. Especially when we were running our full integration test suite. It just took absolutely forever. A large percentage of that was the fact that our Docker images weren't cached in any meaningful way. So everything was being rebuilt from scratch over and over and over, and it just slowed everything down. I discovered Earthly at one point and just gave it a try. And that was what convinced me that this problem was worth investing more time into.

{% include quotes/end.html %}

<!-- vale off -->
### What initially attracted you to Earthly?
<!-- vale on -->

{% include quotes/earthly_satellites_ga/ses.html %}

Caching but also the fact that the cache was basically attached to your Docker image as a part of the build process. Therefore you could upload that cache to your private registry, and you could pull that cache from your registry. So it meant that it [the cache] would transition across CI runners, which is usually the biggest issue with CI.

When you're using a public service like GitHub Actions or Semaphore or Circle CI or whatever CI platform you prefer, you typically don't have the luxury of a dedicated CI box. And that's also kind of the whole point of CI platforms these days. They're ephemeral – you get a fresh box every push, which typically forces you to create repeatable (slow) builds. But there is no way to share a cache between builds or even use a Docker cache. I experimented with Circle CI's integrated Docker cache for their build runners. That turns out to not really work like I think, or how most people would expect, it would. At least it was weird for me anyway. Earthly gave us the solution to that and it took literally just going from Dockerfile to Earthfile to bring build times from 45-ish minutes down to probably 15 or 20, just from skipping the 25 minutes of installing Python dependencies. That was enough for us to use Earthly from that point forward.

{% include quotes/end.html %}

<!-- vale off -->
### What initially attracted you to Earthly Satellites?
<!-- vale on -->

{% include quotes/earthly_satellites_ga/ses.html %}

I tuned our CI/CD performance as much as I could, but the vast majority of our build time was still spent downloading the Docker image and its cache before actually running anything, because our image ends up being 1.5GB, or something like that, after being fully built. It's pretty big. The majority of our time was spent downloading that cache. I was trying to find a way to maybe improve that or figure out if I was using bad practices. When I learned that when using Satellites you're basically transferring files to an external runner that is no longer ephemeral, you have now reinvented the idea of a dedicated build machine so to speak. That was all I needed to go, "Okay, well obviously that's the fastest possible way to do this."

It was love at first sight switching over to Satellites. It was the same kind of case as switching to Earthly for us. Switching to Earthly took us from 45 minutes to 20 minutes, and using Satellites took us from like 20 minutes to 4 or 5 on average. It's been another 2x increase, literally just from using Satellites. It's been astounding.

{% include quotes/end.html %}

<!-- vale off -->
### Now that you've used Satellites for a while, what are the features or benefits that you think are the most important?
<!-- vale on -->

{% include quotes/earthly_satellites_ga/ses.html %}

Not only has Satellites been great in terms of speed and performance, that's the main reason that we love it, but the reason I love it as the maintainer of our build pipeline is it took away all of the hacky stuff that I was doing to make builds fast for our devs. The inline cache is great, but it requires a lot more ceremony to specify the default read branch (usually develop), among other branch-specific things. With Satellites, all of that stuff disappeared because the satellite is smart enough to just work out of the box. I don't even think about whether I'm running on a PR branch versus running on a development branch. I don't really think about any of that stuff anymore, because I just think of it as if it's running locally on a machine. That mental model tends to translate really, really well because that is effectively what it is. It's an ephemeral machine that you spin up. You spin up the same one every time to run your build.

Another reason that we've effectively hitched ourselves to your wagon is every time I have a conversation with an Earthly employee, it's like you guys are just headed for the moon, man. There's so much opportunity for improvement, and you guys are building around all the primitives of BuildKit itself. So for any further cache improvements you come up with, it's just gonna benefit everybody. It's super cool to see I'm really excited to hear all the stuff you all are working on.

{% include quotes/end.html %}

## Try Earthly Satellites

We want to extend a big thank you to Ses as well as all of the other Earthly Satellites users that have helped us refine and improve Satellites to the point that we can now bring them into GA.

If your CI builds are slow or your team is constantly having to waste time waiting for slow builds, try [Earthly Satellites](https://earthly.dev/earthly-satellites). They are remote build runners that make builds fast with an automatic and instantly available build cache. Builds can be triggered by any CI as well as from your laptop. And they're super simple to use. Get started by following [the steps in our documentation to self-serve Satellites](https://docs.earthly.dev/earthly-cloud/satellites).

**Next, you might like to read about Earthly Compute, the service that underpins Earthly Satellites. Dive into the technicalities of Satellites with some of the engineers that build them in our blog post [Remote Code Execution as a Service](/blog/remote-code-execution/).**

{% include_html cta/bottom-cta.html %}
