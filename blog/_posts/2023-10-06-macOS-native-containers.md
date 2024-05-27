---
title: "macOS Containers - The Rise of Native Containerization"
toc: true
author: Adam
excerpt: |
    macOS traditionally did not support native containers, but a community initiative has started to develop containerized macOS, which could be useful for CI XCode builds and local macOS development. While still in the early stages, macOS containers show promise for improving performance and eliminating the need for a Linux VM on macOS.
last_modified_at: 2023-10-04
categories:
  - Containers
---
**The article discusses the macOS container initiative. Earthly streamlines CI processes for macOS developers with efficient containerized builds. [Check it out](https://cloud.earthly.dev/login).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/RS9C_4O_Ohg?si=kOWcFxMvPqSNe2n4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

macOS traditionally has not natively supported containers. You can run Linux containers on macOS in a VM. But you could never run native containers, which used the host OS, the way you could on Linux or even on Windows.

Here at Earthly, this has always been inconvenient. We'd love for people to use Earthly for XCode builds. We'd love to offer macOS Satellites. We'd love to help speed up your Swift and Objective-C builds for macOS, and iOS. Today, we might be a little closer to that reality.

A community initiative has begun to around macOS native containers. This is a containerized macOS, great for CI XCode builds, but potentially useful for local macOS development. What if instead of running a Linux Redis container in Linux VM on my mac, I could just run `redis:macos` natively? There would be some downsides, but volume mounts would be much faster without a VM in the middle, and I wouldn't have to deal with Docker Desktop for things with macOS builds.

The macOs container initiative is super early, and `slonopotamus`'s initial use case is XCode builds, so we aren't quite ready to fill up dockerhub with various macOS containers and start doing XCode builds in Earthly quite yet. ( I'll show you why shortly. )

But it's still an exciting project. So, let's take a look.

## What's a Container?

But first - with all this talk of Linux containers, Windows Containers, and macOS containers - distinctions are starting to get murky around what a container actually is. If it's not a namespaced, cgrouped process running on a Linux host, then what is it?

Let me draw something...

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2970.png --alt {{ What is a container? }} %}
<figcaption>What is a container?</figcaption>
</div>

If you were a container purist, then when you talk about containers, you are talking about the far left of this diagram: A Linux host operating-system running a cgrouped, namespaced, pivot-rooted process managed by the docker runtime.

Let's define some of that:

| Term        | Simple Definition |
|-------------|-------------------|
| cgroup      | A Linux feature to organize processes into groups and set resource limits such as memory and CPU usage for each group. |
| namespace   | A Linux feature to isolate and separate different system resources (like network or file system) for different sets of processes. |
| pivot root  | A method to change the root directory in Linux, useful in containers to isolate the filesystem. |
| docker runtime | The software that manages and runs containers based on Docker images. |

Containers, in this definition, are all based on Linux system calls and so need to run inside Linux.

But you can run those same containers on Windows or macOS inside of a Linux VM. This is what Docker Desktop on Mac and Windows does - and it does it reasonably seamlessly.

|                     | Runs In VM |
|---------------------|----------------------------|---------------------------------|
| Linux Containers on Linux | No                         |
| Linux Containers on Window / macOS | Yes                         |

What Windows Server Containers and now macOS native containers do is expand the container concept to a generic shared kernel isolation mechanism. The mechanism on a Windows machine may use a different isolation method - Windows uses something called 'silos' - but if the host OS is shared, and the runtime is OCI compatible, we call it a container. In this conception, a container is implemented differently on each supported host OS; therefore, whether it's using cgroups or not doesn't matter.

| Aspect                    | Purist Definition (Linux Containers) | Expanded Definition (Windows/macOS Containers) |
|---------------------------|--------------------------------------|-------------------------------------------------|
| **Concept**         | A lightweight process isolated using linux system calls. | A generic shared kernel isolation mechanism enabling applications to run in a consistent environment. |
| **Core Features**         | - cgroup (Resource grouping) <br> - namespace (Resource isolation) <br> - pivot root (Filesystem isolation) | - Shared kernel isolation mechanism (may vary across host OS) |
| **Dependency on Host OS** | Relies on Linux system calls; needs to run within a Linux VM on non-Linux OSes. | Implemented differently on each supported host OS; runs natively sharing the host OS kernel. |

Whether you agree with the expanded definition or not, the point is that macOS containers are containers in the Windows server container sense. They run natively on macOS and share the host OS. They do not run in a Linux VM. They do not use cgroups or namespaces for isolation.

Now, let's try them out.

## Installation

### Disable SIP

First thing I need to do is disable System Integrity Protection. System Integrity Protection keeps macOS safe from persistent malware by preventing the modification of OS files. So, turning it off is not to be done lightly. (I will turn it back on at the end with `csrutil enable`, and you should as well. )

To disable SIP, I do the following:

- Restart my mac in Recovery mode.
- Launch Terminal from the Utilities menu.
- Run the command `csrutil disable`.
- Restart my computer.

~~~{.bash caption=">_"}
> csrutil status
System Integrity Protection  status: enabled.

> csrutil disable
Turning off System Integrity Protection requires modifying system security.
Allow booting unsigned operating systems and any kernel extensions for OS "Macintosh HD" [y/n]: y
Enter password for user adam:
System Integrity Protection is off.
~~~

After that, I restarted my machine, ensured Docker Desktop was not running, and installed macOS Containers.

~~~{.bash caption=">_"}
# Install packages
brew install --cask macfuse
brew install docker docker-buildx macOScontainers/formula/dockerd

# Start services
sudo brew services start containerd
sudo brew services start dockerd

# Set up BuildKit
mkdir -p ~/.docker/cli-plugins
ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
~~~

The reason you need to stop Docker Desktop is interesting. The standard version of `dockerd`, the docker deamon, does not support the `darwin` platform. So macOS containers forked `dockerd` ( along with `containerd` and `runc` and `buildkitd`) to add support for darwin.

Browsing through the commits, these mainly add support for darwin in the myriad places required.

~~~{.diff caption="runtime/v2/bundle.go"}
 func (b *Bundle) Delete() error {
    work, werr := os.Readlink(filepath.Join(b.Path, "work"))
    rootfs := filepath.Join(b.Path, "rootfs")
-   if runtime.GOOS != "darwin" {
-       if err := mount.UnmountRecursive(rootfs, 0); err != nil {
-           return fmt.Errorf("unmount rootfs %s: %w", rootfs, err)
-       }
+   if err := mount.UnmountRecursive(rootfs, 0); err != nil {
+       return fmt.Errorf("unmount rootfs %s: %w", rootfs, err)
~~~

<figcaption>[Commits](https://github.com/containerd/containerd/compare/main...macOScontainers:containerd:macos)</figcaption>

## Running `macOS` Containers

After doing all that – and making sure I have GitHub docker repository credentials - I can start up a macOS native container just like this:

~~~{.bash caption=">_"}
> docker run --rm -it ghcr.io/macoscontainers/macos-jail/ventura:latest echo "Hello"

WARNING: The requested image's platform (unknown) does not match the detected host platform (darwin/arm64/v8) and no specific platform was requested
Hello
~~~

I can pop into a shell. ZSH is not quite working, but bash works fine.

~~~{.bash caption=">_"}
❯ docker run --rm -it ghcr.io/macoscontainers/macos-jail/ventura:latest /bin/bash

WARNING: The requested image's platform (unknown) does not match the detected host platform (darwin/arm64/v8) and no specific platform was requested

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
bash-3.2# pwd
/
bash-3.2# whoami
root
~~~

Because this is all implemented in terms of `chroot`, it's probably possible to break out of the container using [chroot escapes](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/escaping-from-limited-bash) and it's possible to see ( and kill ) processes running on the host (`ps -e`). Nevertheless, this is a cool accomplishment.

## The Container Image

The macOS container project provides three base containers, one each for Ventura, BigSur, and Monetery, and they are huge. The Ventura image I'm using is 7.37 GB. macOS was not designed with containerization in mind, so I shouldn't be surprised.

( If all the errors trying to find .so and shared libraries I'm getting inside the container are any indication - these containers will keep getting bigger. )

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5820.png --alt {{ base images }} %}
<figcaption>Base macOS images</figcaption>
</div>

## What Doesn't Work

I started playing with macOS containers with hopes of installing some things with homebrew, building a Redis container, doing an X code build, and then hooking the whole thing up to Earthly.

I wasn't able to get any of that done. It's still early days on this project and so I've since tempered my expectations.

Here are some things that don't yet work.

### You Can't Run Linux Containers

To use macOS Containers, I needed to stop the docker desktop and start `dockerd` and `containerd` forks with brew. These forks do not support running Linux containers - because they are native macOS, so I can't run a Linux container and a macOS container simultaneously.

~~~{.bash caption=">_"}
> docker run --rm -it alpine /bin/sh
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
docker: no matching manifest for darwin/arm64/v8 in the manifest list entries.
See 'docker run --help'.
~~~

I think this should be resolved if the macOS changes are upstreamed. See [this buildkit PR and related prereqs](https://github.com/moby/buildkit/pull/4059).

## You Can't Copy?

Using `docker build` to build my own image based on Ventura did work with as many RUNs as I needed. Unfortunately, neither COPY nor ADD worked, so getting files in the image was a challenge.

~~~{.dockerfile caption="simple.Dockerfile"}
FROM ghcr.io/macoscontainers/macos-jail/ventura:latest
COPY test.txt /test.txt
~~~

Build like so:

~~~{.bash caption=">_"}
docker build -t macos:simple -f simple.Dockerfile .
~~~

And failure:

~~~{.bash caption="Output"}
simple.Dockerfile:2
--------------------
   1 |     FROM ghcr.io/macoscontainers/macos-jail/ventura:latest
   2 | >>> COPY test.txt /test.txt
   3 |     # COPY /etc/sudoers /etc/sudoers
   4 |     # COPY /etc/passwd /etc/passwd
--------------------
ERROR: failed to solve: failed to copy files: cross-device link
~~~

### Can't Install Xcode

The most straightforward use-case for this image is containerized Xcode builds. This is not quite ready because it's currently not possible to install Xcode into the base image. Keep your eyes on this issue [on github](https://github.com/macOScontainers/rund/issues/16).

### Can't Use With Earthly

To use macOS containers with Earthly, buildkit changes would need to be upstreamed into buildkit and then into `Earthly/buildkit`. Then a buildkit build for macOS would need to be built. We are a few steps away from that happening, but we will get there eventually.

### Get Involved and Shape the Future of macOS Containers

The macOS Containers project spearheaded by [slonopotamus](https://github.com/slonopotamus) is a monumental stride toward bridging the containerization gap on macOS. It has working base images, forks of containerd, buildkit, and his own runc shim that all work. That is impressive!

However, the journey has just begun, and there's much terrain to cover to achieve seamless functionality akin to what Linux and Windows platforms offer.

If you want to go deeper into macOS Containers, here's how you can do that:

- **Try Out macOS Containers:** Experience the current capabilities of macOS Containers firsthand. And add your feedback on bugs, performance, and usability. [Try macOS Containers](https://macoscontainers.org/).

- **Contribute Code:** If you have the skills and interest, contribute to [`rund`](https://github.com/macOScontainers/rund)or help get macOS changes [upstreamed](https://github.com/moby/buildkit/pull/4059).

- **Base Image Tweaking:** If you are familiar with macOS and its structure of .`.so` and `.dylib` and associated OS files, then perhaps you can help build a more complete base image for macOS.

So yeah, it's early days for macOS containers, but it has promise, and I hope we can one day use it with Earthly satellites.

{% include_html cta/bottom-cta.html %}
