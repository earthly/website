---
title: Pricing
layout: page
---

<link rel="stylesheet" href="/assets/css/subpage.css">

### Earthly Core

*Achieve build repeatability*

Pricing: Free and Open-source

* Develop builds that run on any CI
* Run builds locally
* Local cache
* Remote shared cache
* Community support

[Get Earthly](./get-earthly.md)

### Earthly Satellites

*Fast remote builds*

Pricing: `$30/developer/month` billed annually + [zero-margin compute](#compute)

* Everything in Core
* Run builds remotely in runners managed by the Earthly team
* Rebuild only what has changed
* Built-in caching available instantly between runs
* Run x86 builds from Apple Silicon machines (Apple M1/M2)

[Get started](https://docs.earthly.dev/earthly-cloud/satellites)

### Earthly CI

*Ridiculously fast CI*

Pricing: Coming soon

* Everything in Satellites
* Rebuild only what has changed
* Built-in caching available instantly between runs
* GitHub integration
* Automatically span builds across a compute cluster

[Contact us](mailto:support+ci@earthly.dev?subject=Earthly%20CI%20Interest)

## FAQ

<h2 class="text-2xl font-semibold mb-5 mt-20" id="compute">How much does compute cost?<span class="hide"><a href="#compute">¶</a></span></h2>

The cost of compute is based on the AWS rack price for the instances that are used underneath, plus the cost of cache storage and the cost of network ingress/egress incurred. We follow a [zero-margin pricing model for the compute](#zero-margin-compute).

| Instance type | Specs | Price per hour | Price per month <br /> if used 3 hours per work day |
| --- | --- | --- | --- |
| `small` | Coming soon | - | - |
| `medium` (default) | 4 CPUs, 16 GB RAM, 90 GB cache | $0.18 | $11.475 |
| `large` | Coming soon | - | - |

<h2 class="text-2xl font-semibold mb-5 mt-20" id="usage-tracked">How is my usage of Satellites tracked?<span class="hide"><a href="#usage-tracked">¶</a></span></h2>

The usage of Satellites is tracked by monitoring the Satellites for active builds. If there are no active builds for 30 minutes, the Satellite goes to sleep automatically. When a Satellite is asleep, it is not billed for compute. When a build is started, the Satellite is woken up automatically and billed for compute.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="zero-margin-compute">What is zero-margin compute?<span class="hide"><a href="#zero-margin-compute">¶</a></span></h2>

Zero-margin compute is a pricing model where the cost of compute is passed on directly to the user, without any profit-generating margin. This allows us, the CI vendor, to better align our incentives with the end-user. Slow builds should not mean more profit for us.

<h2 class="text-2xl font-semibold mb-5 mt-20" id="how-many-satellites">How many Satellites do I need?<span class="hide"><a href="#how-many-satellites">¶</a></span></h2>

The number of Satellites depends on the amount of workload they need to handle. For maximum performance, you can create a different Satellite for each CI pipeline. In some setups, where the CI pipelines are small, that might be an overkill. The best method to determine the number of satellites is to start with one or two, and add more as needed.

Earthly prints information on build startup about how loaded the Satellite is currently. This can be used as a guide to determine if more Satellites are needed.
