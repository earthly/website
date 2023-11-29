---
title: "Podman: The Rootless Docker Alternative"
categories:
  - Tutorials
toc: true
author: Cameron Pavey

internal-links:
 - podman
 - rootless
 - docker alternative
last_modified_at: 2023-04-17
excerpt: |
    Learn about Podman, a rootless Docker alternative that implements Open Container Initiative (OCI) standards. Discover its benefits, such as improved security and the ability to create and manage pods, and find out why it may be a compelling choice for developers and companies.
last_modified_at: 2023-07-14
---
**This article discusses Podman container technology's capabilities. Earthly enhances Podman's rootless container management for improved build pipelines. [Check it out](/).**

For many developers, [Docker](https://www.docker.com/) was their first exposure to the wonderful world of containers. Containers have changed the way we develop and ship software, and the pace of change isn't slowing down. As containerization technology matures and becomes more widely adopted, there is a growing desire to bring open standards to the field, and this is where [Podman](https://podman.io/) comes in. Podman is a rootless Docker alternative that implements Open Container Initiative (OCI) standards to give developers and companies the benefits of Docker, delivering some promising new features without some of the limitations, like requiring root access.

## Why Should You Care about Podman?

If you are familiar with using Docker on the command line, you're already most of the way to using Podman. Like Docker, Podman is OCI-compliant. The OCI is a [self-described](https://opencontainers.org/) "open governance structure for the express purpose of creating open industry standards around container formats and runtimes." To be compliant means that the two tools are both able to build and run OCI-compliant images. Furthermore, because Podman's CLI is entirely compatible with Docker's, it can be treated as a drop-in replacement. Podman themselves [even suggest](https://podman.io/whatis.html) just creating an alias to point calls to `docker` straight at `podman`.

It's clear that the two have a lot in common, but where do the differences lie? The greatest and most often touted difference is—as the title suggests—that Podman is rootless or daemon-less. Docker works by having a long-lived daemon that the CLI tool interfaces with to perform operations on your containers and images. Podman, on the other hand, has a different architecture, whereby `podman` commands don't need a connection to a daemon but instead do the equivalent operations in short-lived processes directly.

The second big difference is that, unlike Docker, Podman allows you to create and manage organizational groups of containers known as "pods". You are likely to be familiar with pods if you've spent much time working with Kubernetes; though this is a feature that Docker doesn't currently have at all.

So even if Podman is a drop-in replacement, why would you want to use it over Docker? Aside from the presence of pods, which will be explored more below, Podman has some compelling benefits. Chief among these are the security improvements. Podman is [more secure than Docker](https://cloudnweb.dev/2019/10/heres-why-podman-is-more-secured-than-docker-devsecops/) in a few ways, but the most obvious one is that users do not need root privileges to run containers with Podman. Although best practices mitigate the risks, it is still possible for malicious software to [break out of its container](https://book.hacktricks.xyz/linux-unix/privilege-escalation/docker-breakout/docker-breakout-privilege-escalation) and cause havoc on the host. If this happens, you do not want to be flaunting root privileges where they are not strictly needed, as can often be the case with a poorly configured Docker host. Podman takes a different approach to running containers, which means these Docker security concerns are no longer an issue.

## Why Use Podman and When?

Besides the features you are familiar with from Docker, Podman has some additions of its own. As mentioned before, one of the key differentiators is the presence of pods. Much like Pods in Kubernetes, here, they allow you to organize your containers by grouping them in whatever way makes the most sense to you. If you think about a simple Docker installation, you might have lots of containers running, and when you use `docker ps`, there can be a lot of output. A lot of it probably isn't relevant to what you are looking for most of the time. By organizing your containers with pods, you can focus your operations and keep things neater while giving related containers their own namespace, network, and security context.

An aspect of OCI's goal to create open container standards means that you should stop thinking about containers as Docker containers and, instead, think of them as OCI containers. However, this is easier said than done since Docker was one of the first big players in the mainstream container space and has such a large following that it has developed a bit of a [Xerox problem](https://simplystatedbusiness.com/brand/) concerning containers. Podman's way of dealing with this is to support the Docker CLI and to respect config files named either `Containerfile`—as is the new convention—or `Dockerfile`. While the vast majority of the `docker build` options have been reimplemented, some of them are simple NoOps, only present for scripting compatibility, as seen with the `--disable-content-trust` option.

Interestingly, Podman doesn't build images itself but instead delegates the process to another related OCI-compliant tool called [Buildah](https://buildah.io/). Buildah specializes in building OCI images, which Podman can then run. Although the two tools are closely related, there are some key differences, and the most significant of which is their concept of containers. Podman treats containers in the traditional Docker sense that you are likely familiar with, while Buildah containers exist solely to add content to the image it is building.

Another feature of Podman that shouldn't be overlooked is its `generate` command. This command lets you take one of your Podman pods and export it to a Kubernetes-compatible YAML configuration.

<div class="wide">
![Podman Generate Kube <pod id>]({{site.images}}{{page.slug}}/9Rycjeg.png)
</div>

Granted, you will probably want to modify this configuration and clean it up a bit, but the implications of this are pretty exciting. One often daunting part of the Kubernetes learning curve is all the various configuration files you need to create. Podman generating some of these for you lowers the entry barrier somewhat, allowing developers who are already familiar with the Docker CLI to create Podman pods and export them to Kubernetes. This may not be the most optimized workflow for those familiar with Kubernetes, but making technology more accessible is usually a good thing. This feature, along with Kubernetes [dropping support for Docker](https://levelup.gitconnected.com/kubernetes-is-deprecating-docker-in-2021-fa8317f9f070) as its container runtime, makes the pairing of Kubernetes and Podman seem increasingly appealing.

For all its benefits, there are still some limitations to keep in mind when considering whether Podman is suitable for you. The biggest drawback is that, currently, there isn't a direct replacement for `docker-compose`. While there is a `podman-compose` [project in the works](https://github.com/containers/podman-compose), it is still in development and not yet ready for primetime use. While the upcoming `podman-compose` aims to run your existing `docker-compose.yml` files without any modifications, currently, the closest you can get is using pods to namespace and organize your containers. This approach allows for many of the same benefits as `docker-compose`, such as being able to start multiple containers at once from a single config. Still, this interim solution is not a one-to-one replacement, so your mileage may vary. Alternatively, if you absolutely need `docker-compose` as is, right now, it is possible to [configure it to work with Podman](https://www.redhat.com/sysadmin/podman-docker-compose).

Another thing to note is—much like Docker before it—Podman runs natively on Linux but not on macOS or Windows. Just like with Docker, you can still use Podman on those unsupported platforms, but it will depend on a Linux VM running in the background. There really isn't any way around this limitation at present, but for existing Docker users, this isn't anything new.

With all this in mind, the question now becomes this: Should I switch to Podman, and if so, when?

Red Hat has now adopted Podman as the default container runtime of Red Hat Enterprise Linux, and [if their docs are anything to go by](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux_atomic_host/7/html/managing_containers/finding_running_and_building_containers_with_podman_skopeo_and_buildah), they seem pretty keen on their users adopting it. That being said, it is still a fairly young tool compared to Docker, and new tools often have to prove themselves before being trusted with production workloads by the masses. Still, Podman makes a ton of sense as a local developer tool, especially with Docker's [recent changes to their terms of service](https://www.docker.com/blog/updating-product-subscriptions/). Although Docker itself remains free to use, Docker Desktop will now be subject to revised subscription plans for a lot of teams, making alternative solutions like Podman all the more appealing. Podman might not have all the GUI niceties of Docker Desktop, but it does come with its own advantages, which might make it worth the change.

## Conclusion

Podman is a promising development in the containerization landscape. While Docker is likely to remain the de facto tool for building images and running containers, for the time being, things, like the arrival of Podman and the Kubernetes deprecation of Docker, go to show that OCI's efforts to open up the playing field are paying off. As more and more OCI-compliant tools emerge, it will be interesting to see the impact on workflows and build tools. If you are concerned about these changes to the tool landscape impacting your [CI/CD](/blog/ci-vs-cd) and your builds, consider [Earthly](https://earthly.dev/).

Earthly provides an abstraction layer for your build process to make it repeatable, portable, and most importantly, understandable. Instead of juggling multiple different tools in your builds, Earthly handles this for you and helps you iterate on build scripts by making them run the same no matter where they are running, whether it is your laptop or CI.

{% include_html cta/bottom-cta.html %}