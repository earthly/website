#!/usr/bin/env python3
from pandocfilters import toJSONFilter, RawInline

def embed_svg(key, value, format, meta):
  if key == 'Image':
    attrs, caption, (url, title) = value
    if url.endswith('.svg'):
        svg_content = open(url, mode='r').read()
        return RawInline("html5", f"{svg_content}") # requires python 3.6 for f-strings

if __name__ == "__main__":
  toJSONFilter(embed_svg)