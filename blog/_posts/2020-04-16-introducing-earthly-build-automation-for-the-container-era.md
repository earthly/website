---
title: 'Introducing Earthly: build automation for the container era'
featured: true
date: '2020-04-16 19:08:00'
tags:
- news
- article
---

We live in an era of continuous delivery, containers, automation, rich set of programming languages, varying code structures (mono/poly-repos) and open-source. And yet, our most popular CI/CD platform was started 15 years ago when the industry looked very different. CI systems have not changed much since — they are still largely glorified bash scripts, and the limitations are starting to show their age. For context, Docker’s first release was 7 years ago and Kubernetes is only 5 years old. There is no way Jenkins (“Hudson” back then) could have been built with containers in mind, as Docker didn’t even exist at the time.

<figure class="kg-card kg-image-card kg-card-hascaption"><img src="/content/images/2020/09/1_NuZhBAM1CJKFeiidYhOajg.png" class="kg-image" alt srcset="/content/images/size/w600/2020/09/1_NuZhBAM1CJKFeiidYhOajg.png 600w, /content/images/2020/09/1_NuZhBAM1CJKFeiidYhOajg.png 960w" sizes="(min-width: 720px) 720px"><figcaption>Source <a href="https://medium.com/u/d3b222569e15?source=post_page-----55619c63c3e----------------------" rel="noopener">Lawrence Hecht</a> , Source <a href="https://www.cncf.io/wp-content/uploads/2020/03/CNCF_Survey_Report.pdf">CNCF 2019 Survey</a></figcaption></figure>

During this time, tech giants have innovated in parallel and have open-sourced tools like [Bazel](https://bazel.build/) and [Pants](https://www.pantsbuild.org/). They bring modern features, like reproducibility, determinism, the ability to scale in a monorepo and the ability to use cloud-based cache and parallelization.

Although these systems are probably some of the most advanced build automation tools the world has seen, they come at a significant cost: the build config is not compatible with any of the popular open-source tooling that the language communities have gotten so used to. It’s like they come from a parallel universe. For most teams, adopting these tools means completely rewriting all the build configs from scratch and giving up on an entire ecosystem of tooling that they have become so dependent on. As advanced as they are, these solutions have not seen significant adoption beyond tech giants.

# Introducing Earthly
<figure class="kg-card kg-image-card"><img src="/content/images/2020/09/1_ucuMi_MAEgQp4e58dtNN6g.png" class="kg-image" alt></figure>

With the purpose of bringing these modern capabilities to people out in the real world, today we are announcing the release of [Earthly: a build automation tool for the container era](https://www.earthly.dev/).

**Earthly is not meant to replace your existing open-source tooling, but rather to leverage and augment it**. It does not replace your Gradle, your Maven, your NPM, your webpack — you don’t need to rewrite your build. Instead, it leverages these popular technologies and builds on top of them, acting more like the glue.

**Earthly runs all build targets containerized: they get container isolation and layer caching**. Nothing is shared between build targets, other than clearly defined, immutable build artifacts and Docker images.

**No sharing means that you get parallelization for free**. You don’t need to do anything to get it and you never have to debug race conditions. It just works.

**But most importantly, all builds are completely reproducible**. You get a guarantee that the build succeeds on its own and not because of your local dependencies or some environmental config that you’re not aware of. Thus, it becomes an order of magnitude easier to iterate on and debug broken CI builds.

<figure class="kg-card kg-image-card"><img src="/content/images/2020/09/1_NsfCLKr0C5CNlF2ZeMhzzA.png" class="kg-image" alt srcset="/content/images/size/w600/2020/09/1_NsfCLKr0C5CNlF2ZeMhzzA.png 600w, /content/images/size/w1000/2020/09/1_NsfCLKr0C5CNlF2ZeMhzzA.png 1000w, /content/images/2020/09/1_NsfCLKr0C5CNlF2ZeMhzzA.png 1400w" sizes="(min-width: 720px) 720px"></figure>

**A familiar Dockerfile-like syntax is used** , to help new users get up-to-speed quickly. It’s like Dockerfile and Makefile had a baby. However, in contrast to Dockerfiles, you can also output regular artifacts (jars, packages, binaries, arbitrary files), in addition to Docker images.

<!--kg-card-begin: html--><script src="https://gist.github.com/vladaionescu/e5e82edb98496ec9b36de96519f9ec47.js"></script><!--kg-card-end: html-->

Earthly in the future will be about much more: for example, cloud-based build parallelization that has never been possible before. For now, you can run it on top of your existing CI, and you can run it locally for development. You still get the other benefits mentioned above.

There are many other goodies that Earthly provides. For more information and also installation instructions, see the [**Earthly Readme on GitHub**](https://github.com/vladaionescu/earthly#earthly---build-automation-for-the-container-era).

This is the first release of Earthly. We will continue to iterate, make improvements and, most importantly, incorporate user feedback. We can’t wait to see what you build with it!

<!--kg-card-begin: html-->
<script id="asciicast-314104" src="https://asciinema.org/a/314104.js" async></script>
<!--kg-card-end: html-->