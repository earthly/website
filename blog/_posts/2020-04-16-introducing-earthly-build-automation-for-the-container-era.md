---
title: 'Introducing Earthly: build automation for the container era'
featured: true
author: Vlad
categories:
  - News
internal-links:
   - build automation
topic: earthly
funnel: 3
# banner: Example - Page specific banner. <a href="https://earthly.dev/blog/" onclick="bannerLinkClick()">Banner Link</a>.
# mobileBanner: Example - Page specific banner for mobile. <a href="https://earthly.dev/blog/" onclick="bannerLinkClick()">Banner Link</a>.
excerpt: |
    Introducing Earthly, a build automation tool for the container era. Learn how Earthly brings modern capabilities like reproducibility, determinism, and parallelization to your builds without the need for a complete rewrite.
---
We live in an era of continuous delivery, containers, automation, rich set of programming languages, varying code structures (mono/poly-repos) and open-source. And yet, our most popular CI/CD platform was started 15 years ago when the industry looked very different. CI systems have not changed much since — they are still largely glorified bash scripts, and the limitations are starting to show their age. For context, Docker's first release was 7 years ago and Kubernetes is only 5 years old. There is no way Jenkins ("Hudson" back then) could have been built with containers in mind, as Docker didn't even exist at the time.

{% include imgf src="adoption.png" alt="graph of CI usage" caption="Source [Lawrence Hecht](https://medium.com/u/d3b222569e15?source=post_page
