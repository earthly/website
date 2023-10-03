---
title: "macOS containers - Putting Them to the Test"
categories:
  - Articles
toc: true
author: Adam
internal-links:
 - just an example
---


Steps:
- https://macoscontainers.org/
- brew install 

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






## Enable System Integrity Protection
To reenable SIP, do the following:

- Restart your computer in Recovery mode.
- Launch Terminal from the Utilities menu.
- Run the command `csrutil enable`.
- Restart your computer.

> brew install docker docker-buildx macOScontainers/formula/dockerd
==> Pouring docker-buildx--0.11.2.arm64_ventura.bottle.tar.gz
==> Caveats
docker-buildx is a Docker plugin. For Docker to find this plugin, symlink it:
  mkdir -p ~/.docker/cli-plugins
  ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx

zsh completions have been installed to:
  /opt/homebrew/share/zsh/site-functions
==> Summary
🍺  /opt/homebrew/Cellar/docker-buildx/0.11.2: 25 files, 57.8MB
==> Running `brew cleanup docker-buildx`...
==> Installing dockerd from macoscontainers/formula
==> Installing dependencies for macoscontainers/formula/dockerd: macoscontainers/formula/bindfs, macoscontainers/formula/containerd and macoscontainers/formula/rund
==> Installing macoscontainers/formula/dockerd dependency: macoscontainers/
==> ./configure --with-fuse2
==> make
==> make install
🍺  /opt/homebrew/Cellar/bindfs/1.17.4: 8 files, 151.9KB, built in 7 seconds
==> Installing macoscontainers/formula/dockerd dependency: macoscontainers/
==> go build -o bin/ ./cmd...
🍺  /opt/homebrew/Cellar/containerd/0.0.1: 9 files, 77.8MB, built in 19 seconds
==> Installing macoscontainers/formula/dockerd dependency: macoscontainers/
==> go build -o bin/ ./cmd/containerd-shim-rund-v1.go
🍺  /opt/homebrew/Cellar/rund/0.0.3: 6 files, 16.8MB, built in 10 seconds
==> Installing macoscontainers/formula/dockerd
==> cp vendor.mod go.mod
==> cp vendor.sum go.sum
==> go build -o bin/ ./cmd/dockerd
==> Caveats
Start Docker service with:
sudo brew services start dockerd

To start macoscontainers/formula/dockerd now and restart at startup:
  sudo brew services start macoscontainers/formula/dockerd
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/dockerd/bin/dockerd --config-file /opt/homebrew/etc/docker/daemon.json
==> Summary
🍺  /opt/homebrew/Cellar/dockerd/0.0.2: 9 files, 73.2MB, built in 22 seconds
==> Running `brew cleanup dockerd`...
==> Caveats
==> docker-buildx
docker-buildx is a Docker plugin. For Docker to find this plugin, symlink it:
  mkdir -p ~/.docker/cli-plugins
  ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx

zsh completions have been installed to:
  /opt/homebrew/share/zsh/site-functions
==> dockerd
Start Docker service with:
sudo brew services start dockerd

To start macoscontainers/formula/dockerd now and restart at startup:
  sudo brew services start macoscontainers/formula/dockerd
Or, if you don't want/need a background service you can just run:
  /opt/homebrew/opt/dockerd/bin/dockerd --config-file /opt/homebrew/etc/docker/daemon.json


❯ sudo brew services start containerd

Password:
Warning: Taking root:admin ownership of some containerd paths:
  /opt/homebrew/Cellar/containerd/0.0.1/bin
  /opt/homebrew/Cellar/containerd/0.0.1/bin/containerd
  /opt/homebrew/opt/containerd
  /opt/homebrew/opt/containerd/bin
  /opt/homebrew/var/homebrew/linked/containerd
This will require manual removal of these paths using `sudo rm` on
brew upgrade/reinstall/uninstall.
==> Successfully started `containerd` (label: homebrew.mxcl.containerd)

❯ sudo brew services start dockerd

Password:
Warning: Taking root:admin ownership of some dockerd paths:
  /opt/homebrew/Cellar/dockerd/0.0.2/bin
  /opt/homebrew/Cellar/dockerd/0.0.2/bin/dockerd
  /opt/homebrew/opt/dockerd
  /opt/homebrew/opt/dockerd/bin
  /opt/homebrew/var/homebrew/linked/dockerd
This will require manual removal of these paths using `sudo rm` on
brew upgrade/reinstall/uninstall.
==> Successfully started `dockerd` (label: homebrew.mxcl.dockerd)

❯ mkdir -p ~/.docker/cli-plugins
❯ ln -sfn /opt/homebrew/opt/docker-buildx/bin/docker-buildx ~/.docker/cli-plugins/docker-buildx


ECHO $GH_ACCESS |  docker login ghcr.io -u adamgordonbell  --password-stdin  



## You can't run linux containers

> docker run --rm -it alpine /bin/sh
Unable to find image 'alpine:latest' locally
latest: Pulling from library/alpine
docker: no matching manifest for darwin/arm64/v8 in the manifest list entries.
See 'docker run --help'.


## You can't copy?

[+] Building 1.4s (7/8)                                                                                                                                                                        docker:default
 => [internal] load build definition from simple.Dockerfile                                                                                                                                              0.0s
 => => transferring dockerfile: 241B                                                                                                                                                                     0.0s
 => [internal] load metadata for ghcr.io/macoscontainers/macos-jail/ventura:latest                                                                                                                       0.6s
 => [auth] macoscontainers/macos-jail/ventura:pull token for ghcr.io                                                                                                                                     0.0s
 => [internal] load .dockerignore                                                                                                                                                                        0.0s
 => => transferring context: 2B                                                                                                                                                                          0.0s
 => [internal] load build context                                                                                                                                                                        0.0s
 => => transferring context: 29B                                                                                                                                                                         0.0s
 => CACHED [1/3] FROM ghcr.io/macoscontainers/macos-jail/ventura:latest@sha256:e2e480b375688538d1d8c37251f87e029a49d751d68ad80d4ae27f27c0278481                                                          0.0s
 => ERROR [2/3] COPY test.txt /test.txt                                                                                                                                                                  0.5s
------
 > [2/3] COPY test.txt /test.txt:
------
simple.Dockerfile:2
--------------------
   1 |     FROM ghcr.io/macoscontainers/macos-jail/ventura:latest
   2 | >>> COPY test.txt /test.txt
   3 |     # COPY /etc/sudoers /etc/sudoers
   4 |     # COPY /etc/passwd /etc/passwd
--------------------
ERROR: failed to solve: failed to copy files: cross-device link


## Questions
- How does this docker talk to buildkitd?
