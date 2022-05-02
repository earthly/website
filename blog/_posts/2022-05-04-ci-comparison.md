---
title: "CI Showdown"
categories:
  - Tutorials
toc: true
author: Josh

internal-links:
 - just an example
---

## How Much Can You Get For Free?

Here at Earthly we care about your CI/CD dollar. That's why we decided to pit the free offerings of four of the top CI/CD platforms against each other to find out which one provides the most bang for no bucks. In this post we'll compare four of the top CI/CD SASS offerings. We'll give a brief intro to each service and talk about some the things that make them unique. We'll talk about the documentation and ease of setup. 

Next we'll compare each service head to head in a number of different catagories. Lastly, we'll see how long each service takes to build and run a benchmark test and compare the performance.

## Setup and Documentation

### Circle CI

![]({{site.images}}{{page.slug}}/circleci-logo.png)

[Getting set up](/blog/circle-ci-with-django/) and running with [Circle Ci's free tier](https://circleci.com/docs/2.0/plan-free/index.html) was pretty straight forward. Just create an account and link it to your Github account. After that all it took was adding a `.circleci/config.yml` file to our git repo and we were up and running. The docs for Circle Ci were also among the best we've seen with lots of complete code examples.

The docs were among the best we looked at. Information was well organized and it was easy to find answers when we encountered issues. Best of all, nearly every page of the docs included code examples, unusually entire example files. This was great when trying to learn about the different options and settings Circle CI offers. The search functionality worked well, delivering relevant results each time we used it.

### Travis CI

![]({{site.images}}{{page.slug}}/travis-logo.jpg)

Of the four services we looked at, [Travis CI](https://www.travis-ci.com/pricing/) has been around the longest. The documentation was informative and we could ususally find what we were looking for but not without a great deal of digging. Pages are densse with text, which can be helpful, but code examples were usually limited to a few relavant lines and as a new comer it was sometimes unclear where the code fit into the larger config file. Travis's free tier was also the only one among the four that expired. One month after sign up there is no way to use Travis for free. 

### Github Actions

![]({{site.images}}{{page.slug}}/githubactions-logo.png)

Github Actions the new comer among the group, but it's grown quickly since its launch in 2018. Unlike Travis CI or Circle CI, which both allow you to connect projects from Gitlab and Bitbucket, Github Actions requires that your code be hosted on Github. Since your code is already on Github, there's no additional sign in or service you need to include. Just add the appropriate config file to your repo and you're up and running. Having your pull requests and CI in one place was covient when debugging and removed some the frustration that can come from jumping back and forth from the code to another service that holds the build logs. 

The docs were extremely easy to use and offered in-depth code examples, screen shots, and charts that made learning to use the service a breeze.

### GitLab

![]({{site.images}}{{page.slug}}/gitlab-logo.png)

Gitlab, like Github, is a git repository that also offers CI services. Also like Github, you'll need to have your code hosted on Gitlab in order to use their CI services. Once you have a repo set up, getting started with Gitlab CI was just as easy as the rest: add your config file and your ready to go. 

The Gitlab documentation was challenging to use when your primary focus is their SASS offering. Gitlab seems to be putting most of their efforts toward being a hosted solution, either on prem or in the cloud. As a result, a lot of the tutorials and documentation are written for users who are hosting their own runners. The first step in their [getting started](https://docs.gitlab.com/ee/ci/quick_start/#cicd-process-overview) section tells you to install and register a runner before getting started, but these steps are not necessary if you want to use runners hosted by Gitlab. It took a little more digging and some outside sources to get started without having to hose our own runner.

## So How Do They Compare?

### Compute Power
![CPU and RAM breakdown.]({{site.images}}{{page.slug}}/cpu.png)

When it came down to available hardware Circle CI was way ahead of the others. It was also the only service that offered [multiple resource sizes](https://circleci.com/docs/2.0/executor-types/) ranging from 1vCPU / 2GB of RAM to 4 vCPU / 8GB of RAM.  

### Available Disk Space
![Shows disk space available at the time the job ran.]({{site.images}}{{page.slug}}/diskspace.png)

For this metric we simply ran `df -h` as part of our builds. We focused on available space, not total space. Here Circle CI won out again. Not only did it offer the most available space, it offered the highest percentage with 94% of the disk available for your job. Compare that to Github Actions which showed 32GB available of 84GB totally, or 37% of total disk space. Gitlab's measly 15.6GB was not enough to accommodate our build or our benchmark run and ultimately secured it as our dead last pick when it came free CI/CD offerings currently available.

### Build Minutes

![How much can you build for free?]({{site.images}}{{page.slug}}/buildminutes.png)

With one exception, all the services we looked at limited usage by allotting a certain amount of build minutes per month. Run out of build minutes and you'll be forced to pay for more. Again Circle CI won out by offering three times the build minutes as Github Actions which came in second. Travis does not use the concept of build minutes. Instead it offers build credits. The amount of credits you use for each build [depends on a number of factors](https://docs.travis-ci.com/user/billing-overview/#usage---credits), but we saw about 10 credits deducted per run when conducting our benchmark tests. It's hard to say just how exactly this compares to, say, the 400 build minutes offered by Gitlab, but since you have to use your free 10,000 credits within the first month of signing up for Travis CI, we considered it to be the least valuable, since there is no way to use Travis beyond the first month without purchasing more credits or signing up for a monthly plan.

### Speed Test

![Average total run times for our benchmark test.]({{site.images}}{{page.slug}}/speedtest.png)

To test each services performance, we needed something to build. We wanted something open source that also showcased a variety of programming languages. With those criteria in mind, we landed on this [benchmarks project](https://github.com/kostya/benchmarks). This repo contains a handful of different benchmark tests that run on over two dozen languages and frameworks. 

The project is built via docker, which is how most engineers are building projects these days. Once built, it offers several benchmark tests. We chose to run the Base64 string transformation algorithm, because it was a relatively quick test to run. 

For each service we ran a build that then pushed an image to Dockerhub. Next, we ran a separate job that pulled the image and ran the Base64 encode / decode test. We performed each test 5 times to get an idea of how each service varied in performance over multiple runs. 

For each service you'll see three sets of data. 

- Build: The amount of time it took to build all the benchmark tests from the included Dockefile.
- Base64: The amount of time it took to pull and run the base64 benchmark for all languages.
- Total Time: How long did the entire process take **including the time it took to spin up the environment**.

![Circle CI Benchmark Test Results]({{site.images}}{{page.slug}}/circle-table.png)

![Github Actions Benchmark Test Results]({{site.images}}{{page.slug}}/github-table.png)

![Travis CI Benchmark Test Results]({{site.images}}{{page.slug}}/travis-table.png)

<div class="notice--info">

### Where is Gitlab?

Gitlab CI's free [SASS offering](https://docs.gitlab.com/ee/ci/runners/saas/linux_saas_runner.html) is was the weakest of the bunch across the board. As a result, we were unable to build the benchmarks nor run the Base64 test.

If you'd like to get some idea of how Gitlab performs, see we were able to get it to run the Earthly examples in the next section.
</div>

## With Earthly
At Earthly our goal has always been better builds. We build Earthly so it can run anywhere, so naturally we were curious how Earthly ran on each services free tier. Thankfully the Earthly repo contains dozens of examples in Python, Go, Ruby, C and many more. In this case Github Actions had the slight advantage over Circle CI. Gitlab CI was able to run the job to completion, but it came in dead last, nearly doubling the time our second runner up, Travis CI, took.

![Even though it came in second in our benchmark test, Github ended up running Earthly the fastest.]({{site.images}}{{page.slug}}/earthly-run-table.png)


## Conclusion
Over all if speed is your primary concern and you're on a budget, then Circle CI is the clear choice. If you're not looking to run a ton of builds each month and your code is already in Github, then Github actions can offer similar performance with the added convenience of having everything under one service. 

{% include cta/cta1.html %}


 
### Writing Article Checklist

- [X] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [X] Create header image in Canva
- [X] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [X] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR
