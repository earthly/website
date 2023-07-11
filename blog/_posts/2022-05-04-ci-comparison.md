---
title: "CI Free Tier Showdown"
categories:
  - Articles
toc: true
author: Josh

internal-links:
 - github
 - gitlab
 - CI/CD
 - Integration
 - Circle CI
 - Travis CI
excerpt: |
    In this article, we compare the free tiers of four popular CI/CD platforms - Github Actions, GitLab CI, Circle CI, and Travis CI. We evaluate their documentation, compute power, available disk space, free build minutes, and speed and performance. Find out which platform offers the most value for your CI/CD needs.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about comparing the free tiers of four popular CI/CD platforms. Earthly is a powerful build tool that can greatly enhance your CI/CD workflows. [Check us out](/).**

## How Much Can You Get For Free?

Here at Earthly, we care about your CI/CD dollar. That's why we decided to pit the **free tiers** of four of the top CI/CD platforms against each other to find out which one provides the most bang for no bucks. In this post we'll compare [Github Actions](https://github.com/features/actions) vs [GitLab CI](https://docs.gitlab.com/ee/ci/) vs [Circle CI](https://circleci.com/) vs [Travis CI](https://www.travis-ci.com/) using the following criteria:

- Quality of Documentation
- Compute Power
- Available Disk Space
- Free Build Minutes
- Speed and Performance

### Documentation

![Docs]({{site.images}}{{page.slug}}/docs.png)\

#### Github Actions

![Github]({{site.images}}{{page.slug}}/githubactions-logo.png)\

[Github Actions](https://github.com/features/actions) is the newcomer among the group, but it's grown quickly since its launch in 2018. Unlike Travis CI or Circle CI, which both allow you to connect projects from GitLab and Bitbucket, Github Actions requires that your code be hosted on Github. Once your code is on Github, though, there's no additional sign-in or service you need to include. Having our pull requests and CI in one place was convenient when debugging and removed some of the frustration that can come with jumping back and forth from the code to another service that holds the build logs.

Similar to Circle CI, the docs were extremely easy to use and offered in-depth code examples, screenshots, and charts that made learning to use the service quick and easy.

#### Circle CI

![Circle CI]({{site.images}}{{page.slug}}/circleci-logo.png)\

[Getting set up](/blog/circle-ci-with-django/) and running with [Circle Ci's free tier](https://circleci.com/docs/2.0/plan-free/index.html) was pretty straightforward. Create an account and link it to your Github, Bitbucket, or GitLab account. After that, all it took was adding a `.circleci/config.yml` file to our project repo and we were up and running.

The [docs](https://circleci.com/docs/) were among the best we looked at. Information was well organized and it was easy to find answers when we encountered issues. Best of all, nearly every page of the docs included code examples, usually entire example files.

#### Travis CI

![Travis CI]({{site.images}}{{page.slug}}/travis-logo.jpg)\

Like Circle CI, [Travis CI](https://www.travis-ci.com/pricing/) also supports Github, [Bitbucket](/blog/bitbucket-ci/), and GitLab. Once signed in, we were able to connect a repo with a few button clicks, add a `travis.yml` to the root of the project, and we were good to go.

The [documentation](https://docs.travis-ci.com/) was informative and we could usually find what we were looking for, but sometimes not without a great deal of digging. Pages are dense with text, which can be helpful, but code examples were usually limited to a few lines, and it was sometimes unclear where the code fit into the larger config file.

#### GitLab

![GitLab]({{site.images}}{{page.slug}}/gitlab-logo.png)\

GitLab, like Github, is an online git repository that [offers CI/CD services](https://docs.gitlab.com/ee/ci/runners/saas/linux_saas_runner.html). Also, like Github, you'll need to have your code hosted on GitLab to create pipelines. Once you have a repo set up, getting started with GitLab CI was just as easy as the rest: add your config file and you're ready to go.

We found the GitLab documentation challenging to use when our primary focus was their SaaS offering. GitLab seems to be putting most of its efforts toward being a self-hosted solution, either on-prem or in the cloud. As a result, a lot of the tutorials and documentation are written for users who are hosting their own GitLab runners. The first step in their [getting started](https://docs.gitlab.com/ee/ci/quick_start/#cicd-process-overview) section tells you to install and register a runner before you can start building, but these steps are not necessary if you want to use runners hosted by GitLab, and there's little information on the getting started page about this option. It took a little more digging and some outside sources to get started without having to host our own runner.

### Compute Power

![CPU and RAM breakdown.]({{site.images}}{{page.slug}}/cpu.png)

When it came down to available hardware Circle CI was way ahead of the others. It was also the only service that offered [multiple resource sizes](https://circleci.com/docs/2.0/executor-types/) ranging from 1vCPU / 2GB of RAM to 4 vCPU / 8GB of RAM.  

### Available Disk Space

![Shows disk space available at the time the job ran.]({{site.images}}{{page.slug}}/diskspace.png)

For this metric, we simply ran `df -h` as part of our builds and noted the available space. Here Circle CI won out again. Not only did it offer the most available space, but it also offered the highest percentage with 94% of the disk available for our job. Compare that to Github Actions which showed 32GB available of 84GB totally, or 38% of total disk space. Gitlab's measly 15.6GB was not enough to accommodate our build or our benchmark run. More on that in below.

### Build Minutes

![How much can you build for free?]({{site.images}}{{page.slug}}/buildminutes.png)

With one exception, all the services we looked at limited usage by allotting a certain amount of build minutes per month. Run out of build minutes and you'll be forced to pay for more. Again Circle CI won out by offering three times the build minutes as Github Actions, which came in second.

Travis does not use the concept of build minutes. Instead, it offers build credits. The amount of credits you use for each build [depends on several factors](https://docs.travis-ci.com/user/billing-overview/#usage