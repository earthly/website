---
title: "Earthly, Podman And Docker Compose"
categories:
  - Tutorials
toc: true
author: David Szakallas
internal-links:
 - podman
excerpt: |
    Learn how to use Podman, Docker Compose, and Earthly to develop and manage containers on your Linux system. Discover how to install and configure these tools, and explore their features and functionalities.
last_modified_at: 2023-07-14
---
**This article explores Podman's features. Earthly integrates with Podman to enhance container workflows with reproducible builds. [Check it out](/).**

Podman is a daemon-less container engine for developing, managing, and running OCI containers on your Linux System.
With podman, containers can either be run as root or in rootless mode, which improves security as an attacker will not have root privileges over your system. It has a CLI that serves as a drop-in replacement for Docker to make migration easier, so most users can alias Docker to podman without any issues. You can find out more in the project's [documentation](https://docs.podman.io/en/latest/).

Podman recently had the fourth major release in February, which is one of their [most significant releases ever](https://podman.io/releases/2022/02/22/podman-release-v4.0.0.html), featuring over 60 new features, and a completely rewritten network stack.
Being so fresh, most OSes don't have podman 4 release yet, however you can already try it out on Arch Linux or one of its derivatives (e.g Manjaro); or build from source (however that's admittedly a bit complicated given the number of dependencies).
This article shows how to install podman 4 on Arch Linux for rootless and use docker-compose and Earthly.

## Install Core Components

Podman 4 has a couple of required dependencies. First of all, it needs a container networking solution. In previous versions, podman relied on the [CNI](https://github.com/containernetworking/cni), for the new version however,
the team decided to write a dedicated networking stack from scratch, replacing CNI (which is still supported for compatibility). The
new stack consists of two components: [`netavark`](https://github.com/containers/netavark), a container networking tool built specifically for podman;
and [`aardvark-dns`](https://github.com/containers/aardvark-dns) which provides DNS for the containers. The reasons behind this change is explained in RedHat's blog:

> Podman aims to deliver a dedicated single-node container management tool, and the CNI was created to serve Kubernetes,
so it is inherently based on clusters. Podman requires new functionality, such as support for container names and aliases
in Domain Name System (DNS) lookups, that's not very useful to the CNI. Meanwhile, the CNI project is considering deprecating
functionality that Podman relies on because it is not needed to support Kubernetes.
Given the inherent tension between Podman's goals and the CNI's, our team evaluated the options and decided that our best
course of action was to create `Netavark` and Aardvark and tailor them to the needs of Podman's users. -- [Podman 4.0's new network stack: What you need to know](https://www.redhat.com/sysadmin/podman-new-network-stack)

For rootless podman we also need a way to connect our user-mode container networks to the Internet in an unprivileged way, which can be done with [`slirp4netns`](https://github.com/rootless-containers/slirp4netns).

For rootless OverlayFS support, `fuse-overlayfs` is required. Unfortunately, as a user-space file system, it offers significantly lower performance than native OverlayFS, the team [warns](https://www.redhat.com/sysadmin/podman-rootless-overlay).

On Arch Linux, all required packages are hosted in the [Community](https://archlinux.org/packages/community/x86_64/podman/) repository.

~~~{.bash caption=">_"}
$ sudo pacman -S netavark aardvark-dns slirp4netns fuse-overlayfs podman
~~~

You can verify your installation by starting a basic container. Note that rootless won't work just yet, so we're using `sudo` for the time being.

~~~{.bash caption=">_"}
$ sudo podman run busybox echo "Hello World"
  Resolved "busybox" as an alias (/etc/containers/registries.conf.d/00-shortnames.conf)
  Trying to pull docker.io/library/busybox:latest...
  Getting image source signatures
  Copying blob 50e8d59317eb done  
  Copying config 1a80408de7 done  
  Writing manifest to image destination
  Storing signatures
  Hello World
~~~

### Installing on Other Distros

You can start by looking at podman's [installation instructions](https://podman.io/getting-started/installation), however bear in mind that it's very likely that the latest podman package for your (not rolling release) OS is for an older version (e.g. at the time of writing this article, the latest release for Ubuntu 22.04 is [3.4](https://packages.ubuntu.com/jammy/podman)), so you will likely have to build all components from scratch. Also, note that the guide on the above page for building from source is for version 3 too, so it might not be 100% applicable.

## System Configuration for Rootless

For rootless podman, unprivileged users must be able to create namespaces. Check the value of `kernel.unprivileged_userns_clone` by running:

~~~{.bash caption=">_"}
$ sysctl kernel.unprivileged_userns_clone
~~~

If it is currently set to 0, enable it by setting 1 via [`sysctl`](https://wiki.archlinux.org/title/Sysctl) or [kernel parameter](https://wiki.archlinux.org/title/Kernel_parameters).

Furthermore, [`subuid`](https://man.archlinux.org/man/subuid.5) and [`subgid`](https://man.archlinux.org/man/subgid.5) must be set for each user that wants to run rootless podman. `/etc/subuid` and `/etc/subgid` do not exist by default. If they do not exist yet in your system, create them and add the subuids and subgids with usermod.

~~~{.bash caption=">_"}
$ sudo touch /etc/subuid /etc/subgid
$ sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
~~~

See more about [Configuration](https://wiki.archlinux.org/title/Podman#Configuration) on the Arch wiki.

## Setting Up Image Registries

You might have noticed an interesting line in the output of `podman run` earlier:

~~~{.bash caption="Output"}
Resolved "busybox" as an alias (/etc/containers/registries.conf.d/00-shortnames.conf)
~~~

podman discourages using unqualified image names, as it always entails an inherent risk that the image
being pulled is spoofed. Instead, podman's default distribution includes a predefined set of aliases in
`/etc/containers/registries.conf.d/00-shortnames.conf` to resolve the fully qualified names of some widely used images.
However, the files under `/etc/containers` is only considered when running podman as root. So when running rootless, you will receive the following error:

~~~{.bash caption=">_"}
$ podman run busybox echo "Hello World"
  Error: short-name "busybox" did not resolve to an alias and no unqualified-search registries are defined in "/home/user/.config/containers/registries.conf"
~~~

This issue can be resolved by using the fully qualified image name, i.e `docker.io/library/busybox`. However, this would require modifying all existing
scripts that already use short image names. Instead you can copy `00-shortnames.conf` to your user config directory and assign the necessary permissions.

~~~{.bash caption=">_"}
$ mkdir -p ${XDG_CONFIG_HOME}/containers/registries.conf.d
$ sudo cp /etc/containers/registries.conf.d/00-shortnames.conf ${XDG_CONFIG_HOME}/containers/registries.conf.d/00-shortnames.conf
$ sudo chown $UID:$GID ${XDG_CONFIG_HOME}/containers/registries.conf.d/00-shortnames.conf
~~~

Afterwards, you should be able to refer to the image via its short name:

~~~{.bash caption=">_"}
$ podman run busybox echo "Hello World"
  Resolved "busybox" as an alias (/home/user/.config/containers/registries.conf.d/00-shortnames.conf)
  Trying to pull docker.io/library/busybox:latest...
  Getting image source signatures
  Copying blob 50e8d59317eb done  
  Copying config 1a80408de7 done  
  Writing manifest to image destination
  Storing signatures
  Hello World
~~~

However, if you run an image that doesn't have an alias in this list, you will still get an error:

~~~{.bash caption=">_"}
$ podman run curlimages/curl earthly.dev
  Error: short-name "curlimages/curl" did not resolve to an alias and no unqualified-search registries are defined in "/home/user/.config/containers/registries.conf"
~~~

This means you have to extend this list with each alias you want to allow.

The second approach is (if you aren't worried about spoofing) to add docker.io as an unqualified search registry in [`${XDG_CONFIG_HOME}/containers/registries.conf`](https://man.archlinux.org/man/containers-registries.conf.5).

This file can also be used for setting up mirrors, e.g an internal company mirror for DockerHub or Quay, or the public GCR mirror of DockerHub, as in the following snippet. Note that I eventually left it commented as it doesn't contain the Earthly images I'll be using later in this tutorial.

~~~{.bash caption=">_"}
$ cat >>$HOME/.config/containers/registries.conf <<EOF
unqualified-search-registries = ['docker.io']

# [[registry]]
# # Ref: https://cloud.google.com/container-registry/docs/pulling-cached-images
# prefix="docker.io"
# location="mirror.gcr.io"
EOF
~~~

Running `curlimages/curl` should output something like this now:

~~~{.bash caption=">_"}
$ podman run curlimages/curl earthly.dev
  Resolving "curlimages/curl" using unqualified-search registries (/home/user/.config/containers/registries.conf)
  Trying to pull docker.io/curlimages/curl:latest...
  Getting image source signatures
  Copying blob 28867d2f810e done  
  Copying blob 3aa4d0bbde19 done  
  Copying blob 968ce6b2fb58 done  
  Copying blob 701f5fe5d595 done  
  Copying blob 9c3e0e9fd2ff done  
  Copying blob 1082a46b0d76 done  
  Copying blob 610724250ccf done  
  Copying blob a8b5e80ef070 done  
  Copying blob b518d4c718b9 done  
  Copying config 375c62ad36 done  
  Writing manifest to image destination
  Storing signatures
    % Total % Received % Xferd  Average Speed   Time Time  Time  Current
                                Dload  Upload   Total   Spent Left  Speed
  100 35  100 35 0  0  73   0 --:--:-- --:--:-- --:--:-- 73
  Redirecting to https://earthly.dev/%
~~~

## Authenticating to Private Registries

Podman's authentication mechanisms are compatible with Docker including support for credential helpers. Basic authentication
works exactly the same, e.g. `podman login $MY_REGISTRY -u $MY_DOCKER_USER -p $MY_DOCKER_PASSWORD` can be used to login through the CLI.
Podman uses a credential file in JSON format, located at `${XDG_CONFIG_HOME}/containers/auth.json`, and falls back to `$HOME/.docker/config.json` if the former can't be found, so that Docker's authentication configuration can be directly reused.
If you are using [credential helpers](https://docs.docker.com/engine/reference/commandline/login/#credential-helpers) with Docker, you can continue to use them with podman too.
For instance, I am using [`docker-credential-acr-env`](https://github.com/chrismellard/docker-credential-acr-env) for unattended login to a
private Azure Container Registry. I have placed the `docker-credential-acr-env` executable on my `$PATH`, and the following in my `auth.json`:

~~~{.json caption="auth.json"}
{
 "credHelpers": {
     "mycompany.azurecr.io": "acr-env"
 }
}
~~~

This continues to work with podman without any change.

You can find out more about authentication configuration on the manual page of [containers-auth.json](https://man.archlinux.org/man/containers-auth.json.5).

## Using an Init

When you run a container with the `--init` flag it will fail with the following error message:

~~~{.ini caption="Output"}
Error: container-init binary not found on the host: stat /usr/libexec/podman/catatonit: no such file or directory
~~~

This happens because podman doesn't provide an init executable out of the box. Installing the
`catatonit` package will provide it as the default init binary for podman and resolve the issue.

~~~{.bash caption=">_"}
$ sudo pacman -S catatonit
~~~

If you would like to use a different init, e.g [`tini`](https://github.com/krallin/tini) (which is the default for docker), you can provide it with `--init-path`. Remember that it should be built as a static binary, as it is executed in the container.

~~~{.bash caption=">_"}
$ podman run --init --init-path="/usr/bin/tini" --rm php:cli bash -c "ls -al /"
~~~

## Docker Compose

There are two ways to use the lightweight orchestration framework. podman can serve as the [backend for `docker-compose`](https://fedoramagazine.org/use-docker-compose-with-podman-to-orchestrate-containers-on-fedora/). In a rootless setup, this requires you to start the `podman.service` user unit, and set the `DOCKER_HOST` variable to point to the userland podman socket:

~~~{.bash caption=">_"}
$ systemctl --user enable podman.service
$ systemctl --user start podman.service
$ export DOCKER_HOST=unix://${XDG_RUNTIME_DIR}/podman/podman.sock
~~~

You most likely want to export the variable in your `.bashrc` or equivalent.

Let's try it out with a basic WordPress application:

~~~{.yaml caption="wp.yaml"}
version: "3.9"
    
services:
  db:
 image: mysql:5.7
 volumes:
   - ./db_data:/var/lib/mysql
 restart: always
 environment:
   MYSQL_ROOT_PASSWORD: somewordpress
   MYSQL_DATABASE: wordpress
   MYSQL_USER: wordpress
   MYSQL_PASSWORD: wordpress
    
  wordpress:
 depends_on:
   - db
 image: wordpress:latest
 volumes:
   - ./wordpress_data:/var/www/html
 ports:
   - "8000:80"
 restart: always
 environment:
   WORDPRESS_DB_HOST: db
   WORDPRESS_DB_USER: wordpress
   WORDPRESS_DB_PASSWORD: wordpress
   WORDPRESS_DB_NAME: wordpress
~~~

Start it up:

~~~{.bash caption=">_"}
$ docker-compose up
~~~

You can verify that it's running by visiting `localhost:8000`:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4610.png %}
</div>

Note that at the time of writing there's an [unresolved issue](https://github.com/containers/podman/issues/11717#issuecomment-932992780) causing containers to fail on named mounts with the following message:

~~~{.ini caption="Output"}
Error response from daemon: fill out specgen: /var/lib/mysql: duplicate mount destination
~~~

Hopefully it gets fixed soon.

Alternatively to running docker-compose, there's a [`podman-compose`](https://github.com/containers/podman-compose) utility that uses a daemon-less process model that directly executes podman.

~~~{.bash caption=">_"}
$ sudo pacman -S podman-compose
~~~

The CLI is similar to docker-compose, e.g `podman-compose up` will bring up the services. However, I noticed that sending the keyboard interrupt signal will not necessarily shut them down, so make sure you run `podman-compose down` if you don't want the processes lingering around in the background.

## Using Earthly

Note: Make sure you are on v0.6.15 or later for cgroups v2 support.

Earthly runs BuildKit in a container which requires the cgroups CPU controller to set CPU limits. On some systemd-based systems using cgroups v2 (including Arch), non-root users do not have CPU delegation permissions, which causes enabling the CPU controller to fail. As a consequence, when running Earthly you might get the following error right in the beginning:

~~~{.bash caption=""}
sh: write error: No such file or directory
~~~

or

~~~{.bash caption=""}
buildkitd: operation not permitted
Error: buildkit process has exited
~~~

If rootless, check that your user has permissions to delegate at least `cpu` and `pids`:

~~~{.bash caption=">_"}
$ cat "/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/cgroup.controllers"
~~~

If the permissions are missing, you can add these for all users by creating or modifying the file at `/etc/systemd/system/user@.service.d/delegate.conf`

~~~{.ini caption="delegate.conf"}
[Service]
Delegate=memory pids cpu io
~~~

After a reboot, you should see these permissions and successfully run Earthly.

~~~{.Dockerfile caption="Earthfile"}
VERSION 0.6
FROM python:3

build:
  RUN mkdir -p /src && echo "print('Hello World')" >> /src/hello.py
  SAVE ARTIFACT src /src

docker:
  COPY +build/src src
  ENTRYPOINT ["python3", "./src/hello.py"]
  SAVE IMAGE python-example:latest
~~~

When running Earthly, you should see in the logs that it uses podman

~~~{.bash caption=">_"}
$ earthly +docker
~~~

~~~{.ini .merge-code caption="Output"}
 1. Init 🚀
————————————————————————————————————————————————————————————————————————————————

        buildkitd | Found buildkit daemon as podman container (earthly-buildkitd)


 2. Build 🔧
————————————————————————————————————————————————————————————————————————————————

         python:3 | --> Load metadata linux/amd64
            +base | --> FROM python:3
            +base | [       ]   0% resolve docker.io/library/python:3@sha256:48d2ed838ff2f27066f550cdb2887f9f601[██████████] 100% resolve docker.io/library/python:3@sha256:48d2ed838ff2f27066f550cdb2887f9f601af8921a72e1f0366c37a0ee4e5d3a
           +build | --> RUN mkdir -p /src && echo "print('Hello World')" >> /src/hello.py
~~~

You should be able to run the created image with podman:

~~~{.bash caption=">_"}
$ podman run python-example:latest
Hello World
~~~

## Conclusion

As you can see there's much we can do today using the latest version of podman in rootless mode. Additionally to being a substitute for Docker's core functionality, we can to run docker-compose services and use the containerized build tool, Earthly, to build images. There are definitely some rough edges which hopefully get smoothened out as podman gradually gains more traction; just make sure to expect some bumps along the way when you give it a try :).

{% include_html cta/bottom-cta.html %}