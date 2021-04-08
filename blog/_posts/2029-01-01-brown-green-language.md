---
title: "Brown Vs Green Programming Languages"
author: Adam
tags:
- news
categories:
  - Articles
author: Adam
---
## Brown VS Green Languages

<div markdown="1">

``` matplotlib
import matplotlib.pyplot as plt

labels = 'Brown', 'Green'
dreaded_sizes = [10, 2]
dreaded_total = 12
loved_sizes = [6, 7]
loved_total = 13
explode = (0.1, 0)
colors = ["burlywood", "green"]

fig = plt.figure(figsize=(6, 2))

# Graph one
ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
ax1.set_title('Dreaded Languages')
ax1.pie(dreaded_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * dreaded_total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax1.axis('equal') 

# Graph two
ax2 = fig.add_axes([.5, .0, .5, .5], aspect=1)
ax2.set_title('Loved Languages')
ax2.pie(loved_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * loved_total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax2.axis('equal') 

```
<figcaption>
Stack Overflow Language Love Vs Dread 2020
</figcaption>
</div>

## Including Langagues Not Found in Tiobe
``` matplotlib
import matplotlib.pyplot as plt

labels = 'Brown', 'Green', 'Unknown'
dreaded_sizes = [10, 2,3]
loved_sizes = [6, 7,2]
explode = (0.1, 0, 0)
colors = ["brown", "green", "grey"]
total = 15

fig = plt.figure()

# Graph one
ax1 = fig.add_axes([0, 0, .5, .5], aspect=1)
ax1.set_title('Dreaded Languages')
ax1.pie(dreaded_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax1.axis('equal') 

# Graph two
ax2 = fig.add_axes([.5, .0, .5, .5], aspect=1)
ax2.set_title('Loved Languages')
ax2.pie(loved_sizes, explode=explode, labels=labels, 
        autopct=lambda p: '{:.0f}'.format(p * total / 100),
        shadow=True, 
        startangle=90, 
        colors=colors)
ax2.axis('equal') 

```
## Code written before I hired is the worst

## The Dreaded Green Languages

## The Loved Brown Languages


## References
 * [How Tiobe is measured](https://www.tiobe.com/tiobe-index/programming-languages-definition/)
 * [2017 Tiobe Index](https://web.archive.org/web/20170317170815/https://www.tiobe.com/tiobe-index/)
 * [Stack Overflow]()