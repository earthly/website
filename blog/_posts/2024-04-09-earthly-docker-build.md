---
title: "Introducing Earthly docker-build: Faster Docker Builds, Persistent Cache, Works with Any CI"
slug: earthly-docker-build
categories:
  - news
toc: true
author: Gavin
topcta: false
internal-links:
 - introducing earthly docker-build
 - introduction to earthly docker-build
 - what is earthly docker-build
 - featuring earthly docker-build
excerpt: |
    Introducing Earthly docker-build: a new feature that enables Dockerfile-based builds with Earthly and speeds them up by giving you a persistent BuildKit cache that can be used with any CI.
---

Earthly has a lot of benefits and useful features, all built on a foundation provided by [BuildKit](https://github.com/moby/buildkit). If you're unfamiliar with BuildKit, it's a tool designed to enhance the process of building container images. It optimizes build performance through parallel processing and efficient caching, significantly reducing build times. BuildKit is the default builder for Docker but supports a variety of frontends, which is how Earthly plugs into it and uses it in the execution of Earthfiles.

_Learn more about BuildKit in our blog post, [What is Buildkit?](https://earthly.dev/blog/what-is-buildkit-and-what-can-i-do-with-it/)._

We have team offsites every six to nine months. At our offsites, we discuss how business and product development are going, figure out what we're going to build next, and set some goals for our company. A few months ago at our last offsite, we had an idea… I bet it'd be pretty easy to add a feature to Earthly that lets it run good, old-fashioned Dockerfiles. That way, developers who were new to Earthly and wanted to try it out could get value quickly without investing the time and effort into writing Earthfiles. One of our engineers looked into it, and it was pretty easy. So they built it, and now it's available to you.

Announcing `earthly docker-build`, a feature of Earthly that lets you run builds using your Dockerfiles, no Earthfiles required. This makes it much easier to have a repo with mixed Dockerfiles and Earthfiles as you start using Earthly, and possibly more importantly, lets you use Earthly Satellites as a persistent remote BuildKit cache for Dockerfile-based builds. So you can get faster Dockerfile-based builds that work with any CI.

![Announcing]({{site.images}}{{page.slug}}/announce.png)\

## What Is `earthly docker-build`?

`earthly docker-build` is a command built-in to Earthly that lets you build container images from Dockerfiles, very similar to running `docker build`. Since both Earthly and Docker use BuildKit to build container images, you get all the benefits you get with `docker build`, such as parallelism and caching for reduced build times.

There are two primary benefits that `earthly docker-build` provides:

1. **You can use both Earthfiles and Dockerfiles in CI.** This provides flexibility for your builds. It allows you to start using Earthly early while gradually migrating big projects, using your existing Dockerfiles, and over time, converting them to Earthfiles. You can migrate incrementally, tackling migration of easier parts of your build early and more complex parts later, when you're more familiar with Earthly.
2. **You can use Earthly Satellites as a persistent remote BuildKit cache.** CI runners are almost always ephemeral. If you're using `docker build` in CI, either your BuildKit cache, one of the most beneficial features of BuildKit, will get blown away at the end of every build, or you'll have to manually configure caching in your CI, which generally requires downloading the cache at the beginning of the build and uploading it at the end of the build, which is slow. Using `earthly docker-build` With Earthly Satellites gives you a persistent BuildKit cache that will speed up every build with no cache upload and download required.

## How To Use `earthly docker-build`

If you're familiar with Earthly and `docker build`, `earthly docker-build` is very easy to use. If you want to build a Dockerfile of that name in the build context of the current directory, you run `earthly docker-build .`. There are also several options to provide the functionality you're used to with `docker build`.

* **`--dockerfile <dockerfile-path>`** to specify an alternative Dockerfile.
* **`--tag <image-tag>`** to specify the name and tag to use for an image (multiple `--tag` options are supported for multiple tags).
* **`--target <target-name>`** to specify a target in a multi-target Dockerfile.
* **`--platform <platform1[,platform2,...]>`** to specify the platforms to build the image for.
* **`--push`** to push container images to remote docker registries. With Docker, this requires a separate push command after you build and tag your image.

If you want to use `earthly docker-build` on an [Earthly Satellite](https://docs.earthly.dev/earthly-cloud/satellites), that's easy too. You just specify the satellite name with `--sat <satellite-name>` directly after the `docker-build` part of the command. For example:  `earthly docker-build --sat my-satellite --tag my-image:latest .`.

_[Visit our docs from more information and details about using `earthly docker-build`](https://docs.earthly.dev/docs/earthly-command#earthly-docker-build)_

## Sign Up for Earthly Cloud and Start Using `earthly docker-build` Today

![Sign]({{site.images}}{{page.slug}}/sign.png)\

You can use `earthly docker-build` with open source Earthly, but if you [sign up for Earthly Cloud](https://cloud.earthly.dev/login) you get 6,000 build minutes per month free on Satellites and the ability to use them as a persistent remote BuildKit cache. Try `earthly docker-build` out, and let us know how it works for you.

{% include_html cta/bottom-cta.html %}
