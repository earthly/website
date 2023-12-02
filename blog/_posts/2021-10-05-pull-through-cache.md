---
title: "How I Saved $5,000/mo with a $5 Droplet"
categories:
- Tutorials

toc: true
author: Corey

internal-links:
- dockerhub cost
- docker cost
excerpt: |
    Learn how to save money and improve your developer workflow by setting up a pull-through cache for Docker Hub. This article provides step-by-step instructions and tips for configuring and hosting your own cache, helping you avoid rate limits and reduce costs.
last_modified_at: 2023-07-19
---
**In this article, you'll learn how to handle Docker rate limits. Earthly can optimize your CI builds with effective caching. [Learn more](https://cloud.earthly.dev/login).**

On November 20, 2020 Docker began [rate limiting](https://docs.docker.com/docker-hub/download-rate-limit/) requests to its popular Docker Hub registry. This change applied to all users, anonymous or free. When this change was applied, developer workflows around the world screeched to a halt. Many were just fine after simply logging in (the rate limit is higher for logged-in accounts), but others found themselves needing to pay for a [service account](https://docs.docker.com/docker-hub/service-accounts/). Depending on usage, service accounts don't come cheap.

There's nothing wrong with waving the magic money wand to make the problem go away. Depending on your situation, this may even be the right answer. For others, reality might not be quite so plush.

At Earthly, I was no stranger to these rate limits. And, building a containerized build too means pulling a _lot_ of containers, very often. Running our test suite 2-3 times over the span of a couple hours would trigger the rate limit... and it was getting worse with each new test. Perhaps this situation sounds familiar?

So, rather than pay for a service account; I set up a _pull-through cache_ to middleman all requests to Docker Hub. Once I put this in place, failures from rate-limiting vanished. Additionally, it is cheaper than paying for a service account! So, to save you some time, I've documented and shared what I did.

## What Is A Pull-Through Cache?

Before I dive into specifics about our setup at Earthly, lets build a solid understanding about what a pull-through cache is, and is _not_.

A pull-through cache, from the perspective of a client, is just a normal registry. Well, almost. [You can't push images to it](https://docs.docker.com/registry/configuration/#proxy), for instance. But you can pull from it. The first time an image (or its metadata) is requested from the cache, it will be transparently fetched from the upstream repository. Subsequent requests will use the cached version.

This kind of setup works especially well when the images you are pulling do not change frequently. While it is typically recommended to use specific tags to ensure _repeatability_, following this practice when using a cache will also pay dividends by reducing the number of round trips. As if you needed another reason to avoid `:latest`, right?

Of course, there are additional methods and tools that can be used to cache images. Of particular note is the nifty [`rpardini/docker-registry-proxy`](https://github.com/rpardini/docker-registry-proxy), which uses `nginx` proxy and cache the requests, not unlike [MITM Proxy](/blog/mitmproxy). Other registries offer cache modes, like [Artifactory](https://www.jfrog.com/confluence/display/JFROG/Repository+Management#RepositoryManagement-RemoteRepositories) and [GCP](https://cloud.google.com/container-registry/docs/pulling-cached-images).

For the purposes of this article, I'll focus on the standard Docker registry found in ([`distribution/distribution`](https://github.com/distribution/distribution)), since it is simple and well-documented. If you just want to cut to the chase, [all of our work is on GitHub](https://github.com/earthly/ci-examples/tree/main/pull-through-cache).

## Obtaining the Registry

The canonical registry is [`registry:2`](https://hub.docker.com/_/registry). You can obtain this by simply doing a `docker pull registry:2`. However, there are some caveats detailed below in the [HTTPS](#https) section.

## Configuring the Registry

As I go through the options that you may want to configure for you pull through cache, I'll be sharing snippets from a complete [configuration file example](https://github.com/earthly/ci-examples/tree/main/pull-through-cache/terraform/module/cloud-init.yaml#L38-72). If any of the information shared here isn't quite what you need, the [documentation for configuring the registry](https://docs.docker.com/registry/configuration/) is fairly comprehensive.

### Proxy Mode

To use Distribution's registry as a pull-through cache, you'll need to tell it to function as a cache. Huge surprise there, for sure. You can do this via the top-level [`proxy` key](https://docs.docker.com/registry/configuration/#proxy).

```yaml
proxy:
  remoteurl: https://registry-1.docker.io
  username: my_dockerhub_user
  password: my_dockerhub_password
```

Note that the `username` and `password` in this section are _not_ the credentials you would like to use to log in to the cache; but instead the credentials the cache will use to pull from the upstream in `remoteurl`.

By default, the cache will _not_ authenticate users. This means that without setting up authentication for the mirror (see below), **any private repositories available to `my_dockerhub_user` will effectively become public**. Please ensure you get this right to avoid leaking sensitive information!

### Cache Authentication

Your mirror should be secured with some kind of authentication to prevent others from pulling your private images, or using your precious bandwidth. You can do this with the top-level [`auth` key](https://docs.docker.com/registry/configuration/#auth):

```yaml
auth:
  htpasswd:
    realm: basic-realm
    path: /auth/htpasswd
```

Since I work with a relatively small team, using a static username/password in a standard `htpasswd` file is sufficient. If you need help generating a `htpasswd` file, see the [Apache documentation](https://httpd.apache.org/docs/2.4/programs/htpasswd.html).

Do _not_ use the `silly` authentication type, as it is only meant for development. The name should give this away. We hope.

The `token` system should let you connect it to your existing authentication infrastructure. This is normally present in larger organizations, and could be a better fit in that kind of environment.

### HTTPS

For us at Earthly; our infrastructure resides on a `.dev` domain. The entirety of `.dev` uses [HSTS](https://hstspreload.org/). This means I couldn't just leave our cache on HTTP. Besides, in the era of [Let's Encrypt](https://letsencrypt.org/), its simple enough to set up, right?

Well, kinda. At the time of this writing, there's [an issue with the default image](https://github.com/docker/distribution-library-image/issues/96), and a [similar issue upstream for the registry program itself](https://github.com/distribution/distribution/issues/3041). Because Let's Encrypt turned off the relevant APIs, and the default image is so old, you'll need use one of three approaches:

#### Compile A Registry

[This is the approach I took](https://github.com/earthly/registry). You can simply wrap the existing `registry` image in another Dockerfile using `FROM registry:2` (or use an Earthfile ;)) and replace the binary with another built from the `distribution/registry` source.

After that, it was as simple as configuring it as specified using the [`http.letsencrypt` key](https://docs.docker.com/registry/configuration/#letsencrypt) :

```yaml
tls:
  letsencrypt:
    cachefile: /certs/cachefile
    email: me@my_domain.dev
    hosts: [mirror.my_domain.dev]
```

This will cause Let's Encrypt to issue a certificate for the domains in the `hosts` key, and automatically keep it up to date.

#### Manual Certificates

You can load your own certificates using the [`https.tls` key](https://docs.docker.com/registry/configuration/#tls). This should not rely on the old and broken Let's Encrypt libraries in the default image. You can configure [`certbot` to manually handle these, if desired](https://certbot.eff.org/docs/).

#### Reverse Proxy

This was our second option after compiling our own version. Using something like [Traefik](https://doc.traefik.io/traefik/getting-started/quick-start/) with built-in support for Let's Encrypt is a common approach, and is mentioned in the above issues as a potential workaround.

### Storage

Because this registry is just a cache, and isn't mission critical, I opted to back the cache with just the local disk space on the VPS I deployed this on. Additionally, the metadata for the images is not mission critical, so I opted to place this in memory. For more details on these options, see the [`storage.filesystem`](https://github.com/docker/docker.github.io/blob/master/registry/storage-drivers/filesystem.md)  and the [`storage.cache` keys](https://docs.docker.com/registry/configuration/#cache).

```yaml
storage:
  cache:
    blobdescriptor: inmemory
  filesystem:
    rootdirectory: /var/lib/registry
```

There are other storage drivers available, too. The [`storage` root key](https://docs.docker.com/registry/configuration/#storage) details the available drivers.

### Other Small Tweaks

Because I was _already_ adding many configuration options... what were a few more? Here are the other tweaks I added:

A storage healthcheck (in case the cache starts to run out of space, or other VPC weirdness happens):

```yaml
health:
  storagedriver:
    enabled: true
    interval: 10s
    threshold: 3
```

Configure the port that the registry will listen on. The commented out section configures the debug port; omitting it turns off the debug port. This was useful to have, as it provided evidence that the cache was actually getting hits.

You can access this information over the debug port (if enabled) by visiting `/debug/vars`.

```yaml
http:
  addr: :5000
  # Uncomment to add debug to the mirror.
  # debug:
  # addr: 0.0.0.0:6000
  headers:
    X-Content-Type-Options: [nosniff]
```

Enable info-level logging, which made debugging and testing easy:

```yaml
log:
  level: info
  fields:
    service: registry
```

## Hosting Your Cache

At this point, you could start a registry locally, and even successfully connect to it! The command to do so might look like this:

```
docker run -d -p 443:5000 --restart=always --name=through-cache -v ./auth:/auth -v ./certs:/certs -v ./config.yaml:/etc/docker/registry/config.yml registry:2
```

But, a cache that exists only on your machine isn't as useful as one that can be shared; or one that can sit between Docker Hub and your CI. Fortunately, It's not too difficult to get this up and running on a VPS.

Choosing a VPS for your cache is easy - you should probably just use what your company uses. However, I opted to use Digital Ocean due to their reasonable pricing, simple configuration, and generous bandwidth.

For most of its life, our cache ran fairly well on a single $5 droplet, though additional CI pressure has forced us to step up a tier. If your needs are larger than a single node can provide, there are ways to [run multiple instances behind a load balancer](https://docs.docker.com/registry/deploying/#load-balancing-considerations), or [use a CDN](https://docs.docker.com/registry/configuration/#example-middleware-configuration), if needed.

While it is possible to create a VPS instance by hand, lets take it a step further and fully automate it using [Terraform](https://www.terraform.io/) and [clout-init](https://cloud-init.io/). If you want to cut to the chase, [check out the full example](https://github.com/earthly/ci-examples/tree/main/pull-through-cache/terraform).

Lets start by creating the VPS instance. Unlike the registry examples earlier, I'll leave in the variables I used in our Terraform module.

```hcl
resource "digitalocean_droplet" "docker_cache" {
  image      = "ubuntu-20-04-x64"
  name       = "docker-cache-${var.repository_to_mirror}"
  region     = "sfo3"
  size       = "s-1cpu-1gb"
  monitoring = true
  ssh_keys   = [var.ssh_key.fingerprint]
  user_data  = data.template_file.cloud-init.rendered
}
```

Its a fairly standard, simple configuration to spin up a droplet. But, how do you start our cache on the fresh droplet? Through the cloud-init `user_data` key. We use Terraform to template it out using the same variables provided to our module, and place the result in this HCL section. Here's a (truncated) version of our cloud-init template:

```
#cloud-config

package_update: true
package_upgrade: true
package_reboot_if_required: true

groups:
  - docker

users:
  - name: griswoldthecat
    lock_passwd: true
    shell: /bin/bash
    ssh_authorized_keys:
  - ${init_ssh_public_key}
    groups: docker
    sudo: ALL=(ALL) NOPASSWD:ALL

packages:
  - apt-transport-https
  - ca-certificates
  - curl
  - gnupg-agent
  - software-properties-common
  - unattended-upgrades

write_files:
  - path: /auth/htpasswd
    owner: root:root
    permissions: 0644
    content: ${init_htpasswd}

  - path: /config.yaml
    owner: root:root
    permissions: 0644
    content: |
    # A parameterized version of our registry config...

runcmd:
  - curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
  - add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  - apt-get update -y
  - apt-get install -y docker-ce docker-ce-cli containerd.io
  - systemctl start docker
  - systemctl enable docker
  - docker run -d -p 443:5000 --restart=always --name=through-cache -v /auth:/auth -v /certs:/certs -v /config.yaml:/etc/docker/registry/config.yml registry:2
```

This cloud-init template sets up Docker, configures our registry, and starts the container.

## Using Your Cache

Using a mirror is simple. Simply [add the mirror to your list](https://docs.docker.com/registry/recipes/mirror/#configure-the-docker-daemon), and if configured, `docker login` with the appropriate credentials (the `htpasswd` credentials from earlier). `docker` should start automatically using the mirror.

If your mirror becomes unavailable, `docker` should start using the upstream directly without any additional configuration.

## Conclusion

Setting up our own pull-through cache has been a game-changer - it's not only saved us a bundle but also made our CI immune to rate limits. Our builds are now quicker, reliable, and super consistent. If you loved this caching hack, you might want to take it a step further and speed up your builds with [Earthly]((https://cloud.earthly.dev/login)). It's a tool designed to optimize build performance and consistency. Give it a whirl!
