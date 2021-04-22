#!/usr/bin/env python3
# see https://github.com/LaurentRDC/pandoc-plot/issues/24
from pandocfilters import toJSONFilter, Image

path_from = "_site/assets/images/"
path_to = "/blog/assets/images/"

def reroute(key, value, format, meta):
  if key == 'Image':
    attrs, alttext, (url, title) = value
    if url.startswith(path_from):
        newurl = path_to + url.split(path_from)[-1]
        return Image(attrs, alttext, (newurl, title))

if __name__ == "__main__":
  toJSONFilter(reroute)