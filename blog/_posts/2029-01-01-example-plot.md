---
title: "Example Overlay Headline"
categories: 
  - Tutorials
toc: true # Include for tutorials
last_modified_at: 2020-01-07T13:05:25-05:00
---
## How to use pandoc-plot
Mac setup:
* `brew install pandoc`
* `brew install pandoc-plot`
* install specific libs: `pandoc-plot toolkits` to list
  * `pip3 install matplotlib` for matplotlib 

## How to run pandoc-plot
* 


### graph (not working)
```{
  .matplotlib
  format=SVG
  source=false
  }
import matplotlib.pyplot as plt

plt.figure()
plt.plot([0,1,2,3,4], [1,2,3,4,5])
plt.title('This is an example figure')
```
