---
title: "Install `matplotlib` In A Docker Container"
categories:
  - Tutorials
author: Adam
internal-links:
 - matplotlib
excerpt: |
    Learn how to install `matplotlib` in a Docker container and quickly generate graphs and visualizations. Discover the differences between installing `matplotlib` in Alpine Linux and Ubuntu, and why the process can be slower in Alpine.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about installing `matplotlib` in a Docker container. Earthly is a powerful build tool that can greatly simplify the process of building and managing Docker containers. [Check us out](/).**

`matplotlib` is an excellent library for creating graphs and visualizations in Python. For example, I used it to generate the performance graphs in [my merging article](/blog/python-timsort-merge), and internally, we use it now and again for visualizing any metrics we produce. It is a bit hard to install inside a docker container, though.

## Installing Matplotlib in Alpine Linux

On Alpine, or an Alpine-based docker image, it's _possible_ to install `matplotlib`; however it will involve compiling it from source as pip does not provide any pre-compiled binaries -- this will take quite a bit of time. If you don't mind compiling from source, you will need to have its dependencies in place to make this work:

``` Docker
 FROM python:3.6-alpine
 RUN apk add g++ jpeg-dev zlib-dev libjpeg make
 RUN pip3 install matplotlib
```

## Installing Matplotlib in Ubuntu

On Ubuntu, or a Ubuntu-based docker image, the process is much simpler:

``` Docker
 FROM ubuntu:20.10
 RUN apt-get update && apt-get install -y python3 python3-pip
 RUN pip3 install matplotlib
```

In either case, after you've installed it, you can quickly generate great graphs and visualizations:

``` Python
import numpy as np
from scipy.interpolate import splprep, splev

import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch

N = 400
t = np.linspace(0, 3 * np.pi, N)
r = 0.5 + np.cos(t)
x, y = r * np.cos(t), r * np.sin(t)
fig, ax = plt.subplots()
ax.plot(x, y)
plt.xlabel("X value")
plt.ylabel("Y value")
plt.savefig('1.png')
```

![Simple Graph]({{site.images}}{{page.slug}}/1.png)\

## Appendix: Alpine vs Ubuntu Pip Install

Why is the Ubuntu process fast and simple and the Alpine process slow? The reason is `glibc`. The pip wheels for `matplotlib` are compiled c/c++ programs that dynamically link to `glibc` and Alpine does not have `glibc`.  

Alpine tries to stay small and so uses `musl-libc` instead. Unfortunately, this means compiling from source on Alpine, which can be a lengthy process.  

[ThisGuyCantEven](https://stackoverflow.com/questions/49037742/why-does-it-take-ages-to-install-pandas-on-alpine-linux/58210701#58210701) on Stack Overflow has more details:

> Pip looks first for a wheel with the correct binaries, if it can't find one, it tries to compile the binaries from the c/c++ source and links them against `musl`. In many cases, this won't even work unless you have the python headers from python3-dev or build tools like make.
>
> Now the silver lining, as others have mentioned, there are `apk` packages with the proper binaries provided by the community, using these will save you the (sometimes lengthy) process of building the binaries.