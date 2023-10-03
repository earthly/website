---
title: "macOS containers - Putting Them to the Test"
categories:
  - Articles
toc: true
author: Adam
internal-links:
 - just an example
---

macOS traditionally did not natively support containers, which are lightweight, standalone, executable software packages that include everything needed to run a software application. You can run Linux containers on macOS, in a VM. But you could never run native containers, which used the host OS, the way you could on Linux or even on Windows.

Here at Earthly this has always been inconvenient. We'd love for people to use Earthly for XCode builds. We'd love to mac Satellites where Swift and Objective-C builds for macOS and iOS can be done. I'm sure we will get there at some point, and maybe mac containers will be part of how we do it.

Part of the reason that containers aren't availabe for Macs, traditinally has been that macOS doesn't support namespaces, or pivot root or cgroups. However, this is also true of windows, where "Windows Server Containers" share the kernel with the host, but just don't use Linux kernel features to accomplish that – for the obvisous reason that the Windows Kernel is not Linux.

So why not also extend this concept to macOS? 

MacOS, is also not linux and so doesn't have cgroups or namespaces. But like any posix OS, macOS does support chroot. And as I've covered before, its possible to build something like native container support [on top of chroot](/blog/chroot). And that is just what is now happening.

A community initiative has begun to build macOS native containers. This is a containerized macOS, great for CI XCode builds but potentionally also useful for things like local macOS dev. What if instead of running a linux Redis container in Linux VM on my mac I could just run `redis:macos` natively? There would be some downsides, but volume mounts would be a lot faster without a VM in middle, and I wouldnt' have to deal with Docker Desktop for things that have macOS builds. 

This macOs container release is super early and `slonopotamus`'s intial use case is XCode builds, so we aren't quite ready to fill up dockerhub with various macOS containers and start doing XCode builds in Earthly quite yet. ( I'll show you why shortly. )

So let's take a look.

## What's a Container?

I feel like, with all this talk of Windows Containers, and macOS containers, that distinctions are starting to get murky around what a container actually is. If its not a namespaced, cgrouped process then what is it?

Let me draw something...

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2970.png --alt {{  }} %}
<figcaption>What is a container?</figcaption>
</div>

If you were a container purist, then when you talk about containers you are talking about the far left of this diagram. A Linux host operating system running a cgrouped, namespaced, pivot rooted process that is being managed by the docker runtime.

But those same containers can be run on Windows or macOS if they are run inside of a Linux VM and this is what Docker Desktop on mac and windows does and it does it fairly seemlessly.

What Windows Server Containers and now macOS native containers do is expand this concept to a shared kernel isolation mechanism. The mechanism on a windows machine may use a different method of isolation - Windows uses something called 'silos' - but if the host OS is shared, and the runtime is OCI compatible we call it a container.  A container, in this conception, is implemeted differently on each supported host OS and therefore whether its using cgroups or not doesnt' really matter.

( Purist may say this stretches the term beyond all usefulness and perhaps that is true but I think when people talk of Windows containers you know what they are talking about. )

Anyways, the point is macOS containers are containers in the windows server container sense. They run natively on macOS and share the host OS. They do not run in a Linux VM.

Now, let try them out.

## Installation

### Disable SIP

First thing I need to do, is disable System Integrity Protection. System Integrity Protection is what keeps macOS safe from persistent malware by preventing the modification of OS files. So turning it off is not to be done lightly. ( I'm going to turn it back on at the end with `csrutil enable` and you should to. )


To disable SIP, I do the following:

- Restart my mac in Recovery mode.
- Launch Terminal from the Utilities menu.
- Run the command `csrutil disable`.
- Restart my computer.

```
> csrutil status
System Integrity Protection  status: enabled.

> csrutil disable
Turning off System Integrity Protection requires modifying system security.
Allow booting unsigned operating systems and any kernel extensions for OS "Macintosh HD" [y/n]: y
Enter password for user adam:
System Integrity Protection is off.
```

After that I restart my machine, make sure Docker Desktop is not running and then install macOS Containers.

```
# Install packages
brew install --cask macfuse
brew install docker docker-buildx macOScontainers/formula/dockerd

# Start services
sudo brew services start containerd
sudo brew services start dockerd

# Set up BuildKit
mkdir -p ~/.docker/cli-plugins
ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx
```

The reason you need to stop Docker Desktop is interesting. The standard versions of `dockerD`, the docker deamon does not support the `darwin` platform. So macOS containers forked `dockerd` ( along with `containerd` and `runc` and `buildkitd`) to add support for darwin. 

Browsing through the commits, these mainly add support for darwin in the myriad places required.

```
 func (b *Bundle) Delete() error {
    work, werr := os.Readlink(filepath.Join(b.Path, "work"))
    rootfs := filepath.Join(b.Path, "rootfs")
-   if runtime.GOOS != "darwin" {
-       if err := mount.UnmountRecursive(rootfs, 0); err != nil {
-           return fmt.Errorf("unmount rootfs %s: %w", rootfs, err)
-       }
+   if err := mount.UnmountRecursive(rootfs, 0); err != nil {
+       return fmt.Errorf("unmount rootfs %s: %w", rootfs, err)
```
<figcaption>[Commits](https://github.com/containerd/containerd/compare/main...macOScontainers:containerd:macos)</figcaption>

## Running macOS Containers

After doing all that – and making sure I have github docker repository creditentials - I can start up a macOS native container just like this:

```
> docker run --rm -it ghcr.io/macoscontainers/macos-jail/ventura:latest echo "Hello"

WARNING: The requested image's platform (unknown) does not match the detected host platform (darwin/arm64/v8) and no specific platform was requested
Hello
```

I can pop into a shell. ZSH is not quite working, but bash works fine.

```
❯ docker run --rm -it ghcr.io/macoscontainers/macos-jail/ventura:latest /bin/bash

WARNING: The requested image's platform (unknown) does not match the detected host platform (darwin/arm64/v8) and no specific platform was requested

The default interactive shell is now zsh.
To update your account to use zsh, please run `chsh -s /bin/zsh`.
For more details, please visit https://support.apple.com/kb/HT208050.
bash-3.2# pwd
/
bash-3.2# whoami
root
```

Because this is all implemented in terms of `chroot`, its probably possible to break out of the container using [chroot escapes](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/escaping-from-limited-bash) and its possible to see ( and kill ) processes running on host (`ps -e`). Never the less, this is very cool accomplishment.

## The Container Image

The macOS container project provides three base containers, one each for ventura, bigsure and monetery and they are huge. The Ventura image I'm using is 7.37 GB. This is probably to be expected as macOS has not been designed with containerization in mind. 

( If fact, if all the errors trying to find .so shared libraries I'm gettting inside the container are any indication - these containers are going to just keep getting bigger. )

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5820.png --alt {{ base images }} %}
<figcaption>Base macOS images</figcaption>
</div>


## What Doesn't Work

I started playing with macOS containers with hopes of installing some things with homebrew, building a redis container, doing an X code build and then hooking the whole thing up to Earthly. 

I wasn't able to actually get any of that done. It's still early days on this project and so I'm since tempered my expectations.

Here are some things that don't yet work.


### You can't run linux containers

To use macOS Containers I needed to stop docker desktop and start `dockerd` and `containerd` forks with brew. These forks do not support running linux containers - because they are native macos, and therefore I can't run a linux container and a macOS container at the same time.

```
> docker run --rm -it alpine /bin/sh
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
docker: no matching manifest for darwin/arm64/v8 in the manifest list entries.
See 'docker run --help'.
```

This - I think - should be resolved if the macOS changes are upstreamed. See [this buildkit PR and related prereqs](https://github.com/moby/buildkit/pull/4059).

## You Can't Copy?

Using `docker build` to build my own image based on ventura did work with as many RUNs as I needed. Unfortunely neither COPY nor ADD worked, so getting files in the image was a challenge.

```
FROM ghcr.io/macoscontainers/macos-jail/ventura:latest
COPY test.txt /test.txt
```
Build like so:
```
docker build -t macos:simple -f simple.Dockerfile .
```
And failure:
```
simple.Dockerfile:2
--------------------
   1 |     FROM ghcr.io/macoscontainers/macos-jail/ventura:latest
   2 | >>> COPY test.txt /test.txt
   3 |     # COPY /etc/sudoers /etc/sudoers
   4 |     # COPY /etc/passwd /etc/passwd
--------------------
ERROR: failed to solve: failed to copy files: cross-device link
```

### Can't install Xcode

The most straight-forward usecase for this image is containerized xcode builds. This is not quite ready because it's currently not possible to install xcode into the base image. This issue may be soon resolved though and is under active work [on github](https://github.com/macOScontainers/rund/issues/16).

### Can't use with Earthly

To be able to use macOS containers with Earthly, the buildkit changes would need to be upstreamed into buildkit and then into `Earthly/buildkit`, then a buildkit build for macOS would need to be build. We are a couple steps away from that happening but I think we will get there eventaully.

## Overall

Overall macOS Containers is an ambitous project that has made a lot of progress. `slonopotamus` has working base images, forks of containerd, buildkit and his own runc shim that all work. That is impressive!

But much work remaining. All the spit and polish of making things work well inside a mac container will be work. Getting the buy in to upstream changes into the mentioned projects will be work. And doing all this while convincing users to disable SIP and not catching Apple's ire for distributed parts of their operating system - well - a lot need to get right to make this work.

But that is why its a great time to jump in and help `slonopotamus` with this project. Try out [macOS containers](https://github.com/macOScontainers/) and contribute where you can.
