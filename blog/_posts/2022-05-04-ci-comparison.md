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

## What We Did
To test each service, we needed something to build. We wanted something open source that also showcased a variety of programming languages. With those criteria in mind, we landed on this [benchmarks project](https://github.com/kostya/benchmarks). This repo contains a handful of different benchmark tests run on over two dozen languages and frameworks. The project is built via docker. Once built, it offers several benchmark tests. We chose to run the Base64 string transformation algorithm, because it was a relatively quick test to run.

For each service we ran a build that then pushed an image to Dockerhub. Next we ran a seperate job that pulled the image and ran the Base64 encode / decode test. We performed each test 5 times to get an idea of how each service varied in performance over multiple runs. 

For each service you'll see three sets of data. 

- **Build**: The amount of time it took to build all the benchmark tests from the included Dockefile.
- **Base64**: The amount of time it took to pull and run the base64 benchmark for all languages.
- **Total Time**: How long did the entire process take **including the time it took to spin up the enviorment**.

## Circle Ci
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/circle-details.png)

https://circleci.com/pricing/

[Circle Ci's free tier](https://circleci.com/docs/2.0/plan-free/index.html) offers up to 6,000 build minutes per month completely free. You can run up to 30 jobs at a time or in parallel. It also won out when it came to our over all speed test, and not by an insignificant amount. Getting set up and running was pretty straight forward. Just create an account, link it to your Github account. After that all it took was adding a `.circleci/config.yml` file to our git repo and we were up and running. The docs for Circle Ci were also among the best we've seen with lots of code examples. You can use it completely for free as long as you don't go over the 6,000 builds minutes per month. It also offers a decent choice as far as resource with 4 options available at no extra cost.

Circle Ci offers a [wide variety of executors](https://circleci.com/docs/2.0/executor-types/) so weather you want to run your builds in a VM or a docker container. In addition Circle Ci also maintains a number of their own Docker images designed specifically with CI/CD in mind. Lastly we loved using Circle CIs [orbs](https://circleci.com/docs/2.0/orb-intro/) which are pre configured elements for common jobs and commands.
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/circle-table.png)

## Travis CI
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/travis-details.png)

https://docs.travis-ci.com/user/billing-overview/
[Travis CI](https://www.travis-ci.com/pricing/) has been around the longest (?) of the services we took a look at. Again set up was pretty easy. Connect your github account and then you can import repos, add a `.travis.yml` file in the root directory and you're ready to start building. Travis's free tier isn't as generous as some others on this list. Instead of build minutes Travis gives you 10,000 build credits. The amount of credits you use for each build [depends on a number of factors](https://docs.travis-ci.com/user/billing-overview/#usage---credits)
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/travis-table.png)

## Github Actions
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/github-details.png)

Github Actions doesn't offer as many resource options or build minutes as CircleCI, but it did come close when it came to performance. Also, if you've got your code already living in Github, it's really nice to have CI and version control right next to each other. Set up was a breeze and we found the docs particularly easy to use. Well organized and
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/github-table.png)

## GitLab
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/gitlab-details.png)

Gitlab CI's free [SASS offering](https://docs.gitlab.com/ee/ci/runners/saas/linux_saas_runner.html) is the weakest of the bunch. In fact, we were unable to run our build or our base64 test on the standard free tier platform. The Gitlab documentation was also a little challenging to use. Gitlab seems to be putting most of their efforts toward being a hosted solution, either on prem or in the cloud. As a result, a lot of the docs that pointed toward solutions to issues we faced with their hosted offering, only contained solutions that would work if you were self hosting. Builds were certainly taking the longest on Gitlab Ci, but what ultimately killed us was the low disk space: we ran out of space trying to execute both the build and, in an entirely separate job, the base64 benchmark test. 
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/gitlab-table.png)


## With Earthly
At Earthly our goal has always been better builds. We built Earthly so it can run anywhere, so natrually we were curious how Earthly ran on each services free tier. For this test we ran the Earthly examples code which includes Python, Go, Ruby, C and many more. The results were pretty similar to our benchmark test, with github actions coming in first place when it came to speed. In this case Gitlab Ci was able to run the job to completion, but it came in dead last nearly doubling the time our second runner up, Travis Ci took.
![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/earthly-run-table.png)


## Conclusion
Over all if speed is your primary concern and you're on a budget, then Github Actions might be the way to go. It's important to note that there are a lot of other things to consider when you choose a CI platform. Each of the ones we looked at scaled slightly differntly. Eventually, as your project grows you'll have to move on to a paid tier, in which case Circle Ci might offer a little more bang for your buck.



## Gitlab
cpu and ram   - 1vcpu 3.75 ram
disk space    - 15.6 GB
build minutes - 400 CI/CD minutes per month
users         - 5 users per namespace
docs? or jobs? concurreny?

## Github Actions
cpu and ram   - 2-core CPU 7 GB of RAM memory 
disk space    - 84 GB
build minutes - 2,000 build minutes per month
users         - unlimited users on public repos
docs? or jobs? concurreny?

## Circle CI
cpu and ram   - Multiple resource sizes ranging from 1vCPU and 2GB of RAM to 4 vCPU and 8GB of RAM
disk space    - 90 gb
build minutes - 6,000 minutes/month 
users         -  unlimited users
docs? or jobs? concurreny?

## Travis
cpu and ram   - 2 vCPU, ~4GB RAM
disk space    - 54G
build minutes - 10,000 but must be used in first month
users         - unlimited amount of users 
docs? or jobs? concurreny?






set up 
speed test
summary
do any free tiers have arm?
  github has arm
### Writing Article Checklist

- [ ] Write Outline
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
