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

Here at Earthly we care about your CI/CD dollar. That's why we decided to pit the free offerings of four of the top CI/CD platforms against each other to find out which one provided the most bang for no bucks. In addition to looking comparing hardware, disk space, build minutes offered, and quality of documentation, we pit all four against each other in a speed test to see which one could build and run the fastest.

### Circle CI

![]({{site.images}}{{page.slug}}/circleci-logo.png)

[Circle Ci's free tier](https://circleci.com/docs/2.0/plan-free/index.html)
Getting set up and running was pretty straight forward. Just create an account, link it to your Github account. After that all it took was adding a `.circleci/config.yml` file to our git repo and we were up and running. The docs for Circle Ci were also among the best we've seen with lots of code examples. You can use it completely for free as long as you don't go over the 6,000 builds minutes per month. It also offers a decent choice as far as resource with 4 options available at no extra cost.

Circle Ci offers a [wide variety of executors](https://circleci.com/docs/2.0/executor-types/) so weather you want to run your builds in a VM or a docker container. In addition Circle Ci also maintains a number of their own Docker images designed specifically with CI/CD in mind. Lastly we loved using Circle CIs [orbs](https://circleci.com/docs/2.0/orb-intro/) which are pre configured elements for common jobs and commands.

### Travis CI

![]({{site.images}}{{page.slug}}/travis-logo.jpg)

https://docs.travis-ci.com/user/billing-overview/
[Travis CI](https://www.travis-ci.com/pricing/) has been around the longest (?) of the services we took a look at. Again set up was pretty easy. Connect your github account and then you can import repos, add a `.travis.yml` file in the root directory and you're ready to start building. Travis's free tier isn't as generous as some others on this list. Instead of build minutes Travis gives you 10,000 build credits. The amount of credits you use for each build [depends on a number of factors](https://docs.travis-ci.com/user/billing-overview/#usage---credits)

### Github Actions

![]({{site.images}}{{page.slug}}/githubactions-logo.png)

Github Actions doesn't offer as many resource options or build minutes as CircleCI, but it did come close when it came to performance. Also, if you've got your code already living in Github, it's really nice to have CI and version control right next to each other. Set up was a breeze and we found the docs particularly easy to use. Well organized and

### GitLab

![]({{site.images}}{{page.slug}}/gitlab-logo.png)

Gitlab CI's free [SASS offering](https://docs.gitlab.com/ee/ci/runners/saas/linux_saas_runner.html) is the weakest of the bunch. In fact, we were unable to run our build or our base64 test on the standard free tier platform. The Gitlab documentation was also a little challenging to use. Gitlab seems to be putting most of their efforts toward being a hosted solution, either on prem or in the cloud. As a result, a lot of the docs that pointed toward solutions to issues we faced with their hosted offering, only contained solutions that would work if you were self hosting. Builds were certainly taking the longest on Gitlab Ci, but what ultimately killed us was the low disk space: we ran out of space trying to execute both the build and, in an entirely separate job, the base64 benchmark test. 


## Comparisons

### Compute Power
![CPU and RAM breakdown.]({{site.images}}{{page.slug}}/cpu.png)

When it came down to available hardware Circle CI was way ahead of the others. Not only did it offer you the most, it was the only service that offered multiple resource sizes ranging from 1vCPU / 2GB of RAM to 4 vCPU / 8GB of RAM. Still hardware isn't the only story when it comes to performance, and even though Circle CI won out when it came to numbers, it actually came in second in our overall speed test.

### Disk Space
![Shows disk space available at the time the job ran.]({{site.images}}{{page.slug}}/diskspace.png)

For this metric we simply ran `df -h` as part of our builds. We focused on Available space. Here Circle CI won out again. Not only did it offer the most available space, it offered the highest percentage with 94% available for your job. Compare that to github actions which showed 32GB available of 84GB totally, or 37% of total disk space. Gitlab's measly 15.6GB was not enough to accommodate our build or our benchmark run and ultimately secured it as our dead last pick when it came free CI/CD offerings currently available.

### Build Minutes

![How much can you build for free?]({{site.images}}{{page.slug}}/buildminutes.png)

With one exception, all the services we looked at limited usage per month by allotting a certain amount of build minutes per month. Run out of build minutes and you'll be forced to pay for more. Again Circle CI won out by offering three times the build minutes as Github Actions which came in second. Travis does not use the concept of build minutes. Instead it offers build credits. The amount of credits you use for each build [depends on a number of factors](https://docs.travis-ci.com/user/billing-overview/#usage---credits), but we saw about 10 credits deducted per run when conducting our benchmark tests. It's hard to say just how exactly this compares to say the 400 build minutes offered by Gitlab, but since you have to use your free 10,000 credits within the first month of signing up for Travis CI, we considered it to be the least valuable, since there is no way to use Travis beyond the first month without purchasing more credits or signing up for a monthly plan.

### Speed Test

![Average total runtimes for our benchmark test.]({{site.images}}{{page.slug}}/speedtest.png)

To test each service, we needed something to build. We wanted something open source that also showcased a variety of programming languages. With those criteria in mind, we landed on this [benchmarks project](https://github.com/kostya/benchmarks). This repo contains a handful of different benchmark tests run on over two dozen languages and frameworks. The project is built via docker. Once built, it offers several benchmark tests. We chose to run the Base64 string transformation algorithm, because it was a relatively quick test to run. 

For each service we ran a build that then pushed an image to Dockerhub. Next, we ran a separate job that pulled the image and ran the Base64 encode / decode test. We performed each test 5 times to get an idea of how each service varied in performance over multiple runs. 

For each service you'll see three sets of data. 

- **Build**: The amount of time it took to build all the benchmark tests from the included Dockefile.
- **Base64**: The amount of time it took to pull and run the base64 benchmark for all languages.
- **Total Time**: How long did the entire process take **including the time it took to spin up the environment**.

![Circle CI Benchmark Test Results]({{site.images}}{{page.slug}}/circle-table.png)

![[Github Actions Benchmark Test Results]({{site.images}}{{page.slug}}/github-table.png)

![[Travis CI Benchmark Test Results]({{site.images}}{{page.slug}}/travis-table.png)


## With Earthly
At Earthly our goal has always been better builds. We built Earthly so it can run anywhere, so naturally we were curious how Earthly ran on each services free tier. For this test we ran the Earthly examples code which includes Python, Go, Ruby, C and many more. The results were pretty similar to our benchmark test, with github actions coming in first place when it came to speed. In this case Gitlab Ci was able to run the job to completion, but it came in dead last nearly doubling the time our second runner up, Travis Ci took.

![Even though it came in second in our benchmark test, Github ended up running Earthly the fastest.]({{site.images}}{{page.slug}}/earthly-run-table.png)


## Conclusion
Over all if speed is your primary concern and you're on a budget, then Github Actions might be the way to go. It's important to note that there are a lot of other things to consider when you choose a CI platform. Each of the ones we looked at scaled slightly differently. Eventually, as your project grows you'll have to move on to a paid tier, in which case Circle Ci might offer a little more bang for your buck.







 
### Writing Article Checklist

- [X] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR
