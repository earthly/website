---
title: "Install `matplotlib` In A Docker Container"
categories:
  - Tutorials
author: Adam
internal-links:
 - matplotlib
---

`matplotlib` is an excellent library for creating graphs and visualizations in Python. For example, I used it to generate the performance graphs in [my merging article](/blog/python-timsort-merge), and internally, we use it now and again for visualizing any metrics we produce. It is a bit hard to install inside a docker container, though.

## Installing Matplotlib in Alpine Linux

On Alpine, or an Alpine-based docker image, installing `matplotlib` involves compiling it from source, and you need to have its dependencies in place to make this work:

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
plt.savefig('1.png')
```

![Simple Graph]({{site.images}}{{page.slug}}/1.png)\
