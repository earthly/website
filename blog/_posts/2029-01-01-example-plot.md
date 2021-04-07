---
title: "Example Graphs"

categories: 
  - Tutorials
toc: true # Include for tutorials
last_modified_at: 2020-01-07
author: Adam
---
You can embedded graphs into the markdown like this:

### Simple Graph
``` matplotlib
import matplotlib.pyplot as plt

plt.figure()
plt.plot([0,1,2,3,4], [1,2,3,4,5])
plt.title('This is an example figure')
```

### More Complex
``` matplotlib
from matplotlib import colors
import matplotlib.pyplot as plt
import numpy as np

np.random.seed(19680801)
Nr = 4
Nc = 3

fig, axs = plt.subplots(Nr, Nc)
fig.suptitle('Multiple images')

images = []
for i in range(Nr):
    for j in range(Nc):
        # Generate data with a range that varies from one plot to the next.
        data = ((1 + i + j) / 10) * np.random.rand(10, 20)
        images.append(axs[i, j].imshow(data))
        axs[i, j].label_outer()

# Find the min and max of all colors for use in setting the color scale.
vmin = min(image.get_array().min() for image in images)
vmax = max(image.get_array().max() for image in images)
norm = colors.Normalize(vmin=vmin, vmax=vmax)
for im in images:
    im.set_norm(norm)

fig.colorbar(images[0], ax=axs, orientation='horizontal', fraction=.1)


# Make images respond to changes in the norm of other images (e.g. via the
# "edit axis, curves and images parameters" GUI on Qt), but be careful not to
# recurse infinitely!
def update(changed_image):
    for im in images:
        if (changed_image.get_cmap() != im.get_cmap()
                or changed_image.get_clim() != im.get_clim()):
            im.set_cmap(changed_image.get_cmap())
            im.set_clim(changed_image.get_clim())


for im in images:
    im.callbacksSM.connect('changed', update)

```

## How to install pandoc-plot
If you are using the docker container and jekyll, it should just work.  

Manual Mac setup:

* `brew install pandoc`
* `brew install pandoc-plot`
* install specific libs: `pandoc-plot toolkits` to list
  * `pip3 install matplotlib` for matplotlib 

## How to run pandoc-plot
The site will run pandoc-plot itself, but if you want to run it manually here is how:
```
 pandoc blog/_posts/2029-01-01-example-plot.md --filter pandoc-plot -f markdown -t html -s -o plot.html
```