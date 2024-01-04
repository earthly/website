---
title: "Put Your Best Title Here"
categories:
  - Tutorials
toc: true
author: Gavin Johnson

internal-links:
 - just an example
excerpt: |
    This markdown content provides a checklist for writing and publishing an article, including steps such as outlining, drafting, proofreading, creating a header image, and adding internal links. It also includes a checklist for optimizing an article for external publication, including adding an author page, optimizing images, and incorporating external links.
---

Earthly was featured on star-history.com’s Starlet List.

<block-quote>
Earthly is like a combination of Docker and Make, running build scripts in Docker containers for consistent results in any environment - local, remote, and CI. It even blends Dockerfile and Makefile syntaxes for ease of use. It has advanced caching, like Docker layer caching on steroids, that speeds up builds significantly, especially in CI. Additionally, Earthly is designed for easy integration with any CI, helping you ensure fast, consistent builds everywhere…
</block-quote>

## Outside Article Checklist

- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include_html cta/bottom-cta.html %}`
