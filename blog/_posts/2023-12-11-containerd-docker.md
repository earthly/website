---
title: "Getting Started with containerd in Docker"
categories:
  - Tutorials
toc: true
author: James Walker

internal-links:
 - starting with containerd
 - containerd in docker
 - how to use containerd in docker
---

[`containerd`](https://containerd.io) is a leading container runtime that manages the complete lifecycle of the containers running on your system. It provides an interface that higher-level tools like Docker can use to start and manage containers.

Originally, Docker used its own container runtime to perform these functions. However, this approach proved restrictive as the container ecosystem grew. Projects such as Kubernetes had to wrap the full Docker application, even though they only needed the subset of features used to run containers. As a result, Docker [spun its runtime out](https://www.docker.com/blog/introducing-containerd) into a separate [CNCF-maintained](https://www.cncf.io) containerd project at the end of 2016.

Docker uses containerd as its [default container runtime](https://earthly.dev/blog/containerd-vs-docker). However, the containerd project has expanded beyond container runtime functionality to include image store capabilities such as pushes, pulls, and snapshots. In this article, you'll explore these newer containerd features and how you can use them with Docker.

## Why Use `containerd`?

`containerd` started as a means to decouple container lifecycles from the Docker application. Docker popularized the containerized software movement, but it didn't create the concept of a container. At a low level, containers are implemented using existing Linux kernel features such as [chroot](https://man7.org/linux/man-pages/man2/chroot.2.html), [cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html), and [namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html). containerd provides a higher-level interface to these features.

Splitting containerd out of Docker led to faster, more consistent innovation in the container space. The standardization introduced by the [Open Container Initiative (OCI) runtime specification](https://github.com/opencontainers/runtime-spec) means that container tools like Docker and Kubernetes can work with any compatible runtime, of which containerd is the most popular example. You're no longer constrained to Docker's portion of the ecosystem.

In addition to its core container runtime functionality, containerd now also includes an image store that can be used to pull, push, and save container images. Compared with Docker's default store, containerd provides several benefits:

- `containerd` understands multiplatform images, where a single image tag can refer to different variants covering a range of operating systems and hardware architectures (such as AMD64 vs. ARM64).
- `containerd` supports efficient, swappable container [snapshotters](https://github.com/containerd/containerd/tree/main/snapshots) that function as storage subsystems.
- [Lazy pulling](https://github.com/containerd/stargz-snapshotter) of image content can accelerate container startups. It allows containers to begin running with a minimal set of required image chunks and then fetch the remaining chunks on demand.
- Other types of [OCI artifacts](https://github.com/opencontainers/artifacts) can be stored in addition to regular Linux container images. These include containers based on [WebAssembly](https://docs.docker.com/desktop/wasm) (Wasm).

Docker [doesn't plan](https://github.com/docker/roadmap/issues/371) to add these features to its own image store. Instead, it's [integrating containerd's store](https://www.docker.com/blog/extending-docker-integration-with-containerd) to provide the functionality without having to increase the code complexity of Docker Engine and Docker Desktop.

## How to Get Started With the `containerd` Image Store

To use these new image store features, you must enable the containerd image store in Docker's settings. Otherwise, Docker's image store will continue to be used until it's removed in an eventual future update. The containerd store is currently *experimental*—some features could be missing, broken, or removed in new releases, so keep this in mind when using the integration.

### Enabling the `containerd` Image Store in Docker Engine

The containerd image store has been available in the standalone Docker Engine for Linux since [the version 24 release](https://docs.docker.com/engine/release-notes/24.0/#2400). To enable it, you must manually edit your Docker daemon config file found at `/etc/docker/daemon.json` (go ahead and create it if it doesn't already exist). Set the `features.containerd-snapshotter` field in the top-level config object to `true`:

~~~{.json caption="daemon.json"}
{
    "features": {
        "containerd-snapshotter": true
    }
}
~~~

Next, restart the Docker daemon to apply the change:

~~~{.bash caption=">_"}
$ sudo systemctl restart docker
~~~

You can verify that the containerd image store is enabled by running the following command:

~~~{.bash caption=">_"}
$ docker info -f '{% raw %}{{ .DriverStatus }}{% endraw %}'
[[driver-type io.containerd.snapshotter.v1]]
~~~

This output confirms that containerd is being used. For reference, the default output without containerd will look like this:

~~~{ caption="Output"}
[[Backing Filesystem extfs] [Supports d_type true] 
[Using metacopy false] [Native Overlay Diff true] [userxattr false]]
~~~

Running `docker images` also lets you verify that the containerd image store is being used. Your image list will be empty after you switch to containerd because your existing images aren't automatically copied into the containerd store. (They still exist on your machine, so you can recover them by disabling the containerd integration.)

### Enabling the `containerd` Image Store in Docker Desktop

Docker Desktop added support for the containerd image store in [version 4.12.0](https://docs.docker.com/desktop/release-notes/#4120). To enable it, click the settings cog icon in the desktop app's title bar, then switch to the **Features in development** settings tab using the left sidebar. Select the **Use containerd for pulling and storing images** checkbox, then press the blue **Apply & restart** button:

<div class="wide">
![Enabling the containerd image store in Docker Desktop]({{site.images}}{{page.slug}}/DrfQCA5.png)
</div>

Docker Desktop will take several seconds to restart. Once it's running again, you'll see that your existing containers and images have disappeared. This is because Docker is now using the containerd image store, which will be empty until you've added some content.

### Using the `containerd` Image Store with Docker

Once you've activated the containerd image store, Docker commands that interact with images will use containerd. This includes the following operations:

- `docker run`: Images fetched to run containers will be pulled and stored using containerd.
- `docker build`: Newly built images will be added to the containerd image store.
- `docker commit`: Images created from existing containers will be stored in containerd.
- `docker push` and `docker pull`: Registry operations will affect the images in containerd.
- `docker save`: Image export operations will target images stored in containerd.

Now, let's see this in action by creating a simple multiplatform image build.

#### Building a Multiplatform Image with Docker and `containerd`

To build a multiplatform image with Docker and containerd, copy the following code and save it as `Dockerfile` in your working directory:

~~~{.dockerfile caption="Earthfile"}
FROM nginx:latest

RUN echo "<h1>Example site</h1><p>This is an example</p>" > \
/usr/share/nginx/html/index.html'
~~~

This trivial image builds upon the official Nginx base image to serve a simple web page.

Next, run the following command to build the image for both AMD64 and ARM64 Linux systems, after replacing `<your_docker_hub_username>` with your username:

~~~{.bash caption=">_"}

$ docker buildx build --platform linux/arm64,linux/amd64 -t <your_docker_hub_username>/containerd-example:latest .
[+] Building 41.0s (9/9) FINISHED                                                                                          docker:default
 => [internal] load build definition from Dockerfile              0.1s
 => => transferring dockerfile: 150B                              0.1s
 => [linux/amd64 internal] load metadata for docker.io/library/nginx:latest     4.3s
 => [linux/arm64 internal] load metadata for docker.io/library/nginx:latest     4.7s
 => [internal] load .dockerignore                                 0.1s
 => => transferring context: 2B                                                                                                      0.0s
 => [linux/arm64 1/2] FROM docker.io/library/nginx:latest@sha256:add4792d930c25dd2abf2ef9ea79de578097a1c175a16ab25814332fe33622de   26.8s
...
 => [linux/amd64 1/2] FROM docker.io/library/nginx:latest@sha256:add4792d930c25dd2abf2ef9ea79de578097a1c175a16ab25814332fe33622de   28.7s
...
 => [linux/arm64 2/2] RUN echo "<h1>Example site</h1><p>This is an example</p>" > /usr/share/nginx/html/index.html                   1.9s
 => [linux/amd64 2/2] RUN echo "<h1>Example site</h1><p>This is an example</p>" > /usr/share/nginx/html/index.html                   0.7s
 => exporting to image                                                                                                               2.0s
...
~~~

The output shows that the `linux/amd64` and `linux/arm64` variants of the base image were pulled. Docker uses your Dockerfile to build a new image for each variant. You'll see the two created variants when you run `docker images`:

~~~{.bash caption=">_"}
$ docker images
REPOSITORY                   TAG      IMAGE ID       CREATED          SIZE
ilmiont/containerd-example   latest   b6aa383eea99   11 minutes ago   272MB
ilmiont/containerd-example   latest   b6aa383eea99   11 minutes ago   67.2MB
~~~

This workflow isn't possible without the containerd integration. If you tried to run the same command using Docker's image store, you'd see the following error message:

~~~{ caption="Output"}
ERROR: Multiple platforms feature is currently not supported for 
docker driver.
~~~

The successful image build demonstrates that containerd was used to pull the base image, build your new image, and store the result on your machine. Now, you can try exporting the image to a local tar archive using `docker save`:

~~~{.bash caption=">_"}
$ docker save <your_docker_hub_username>/containerd-example:latest > \
containerd-example-image.tar
~~~

This operation should complete successfully without any differences between the Docker-specific and containerd-provided image store implementations.

#### Pushing the Image to Docker Hub

You can now push your image to your Docker Hub account:

~~~{.bash caption=">_"}
$ docker push <your_docker_hub_username>/containerd-example:latest
~~~

You should see the push complete successfully, with both image variants being uploaded to your Docker Hub registry.

You can verify this by logging in to Docker Hub and viewing the pushed image:

<div class="wide">
![The pushed demo image in the author's Docker Hub account]({{site.images}}{{page.slug}}/d6VrWs0.png)
</div>

As you can see, using containerd provides a simpler build experience without causing any compatibility issues with familiar Docker commands. You'll also benefit from the behind-the-scenes performance improvements that the containerd image store provides.

## What's Next for `containerd` and Docker?

Much of the core functionality of Docker's containerd image store integration is now complete. There are a few outstanding issues [in the roadmap](https://github.com/moby/moby/projects/13), but these primarily concern snags and minor compatibility problems rather than large areas of missing feature parity with Docker's image store.

Docker intends for containerd to become the [default image store](https://www.docker.com/blog/extending-docker-integration-with-containerd) in a future release. Before that happens, all of Docker's existing storage graph drivers—used to store file system layers—will be converted to containerd snapshotters, the equivalent containerd concept.

Docker will then implement an automated migration for Docker Desktop and Docker Engine that allows you to upgrade your existing installation to use containerd. It's expected that the migration will enable the containerd image store for you, then import your existing images. This does not happen in the current experimental release.

## Conclusion

`containerd` is a lightweight, OCI-compliant container runtime that's been used by Docker since it was split out of the project in late 2016. Docker is now transitioning to also use containerd's image store features instead of its own implementation (the current default in Docker Engine and Docker Desktop).

Using the containerd image store allows you to access more powerful image management functionality, including support for multiplatform images, Wasm, and lazy pulling of image content. containerd's pluggable model also lets you use additional features implemented by adjacent projects, such as image encryption with [imgcrypt](https://github.com/containerd/imgcrypt). None of these capabilities are available in Docker's image store.

For the time being, the containerd image store remains an experimental Docker feature. You can stay informed on what's happening by checking the issues on the [public integration roadmap](https://github.com/moby/moby/projects/13) and following the release notes for [Docker Engine](https://docs.docker.com/engine/release-notes) and [Docker Desktop](https://docs.docker.com/desktop/release-notes).

{% include_html cta/bottom-cta.html %}
