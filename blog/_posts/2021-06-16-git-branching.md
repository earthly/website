---
title: "The Develop Branch Must Die - Git Branching Strategies"
categories:
  - Tutorials
toc: true
author: Adam
internal-links:
 - just an example
---

### Writing Article Checklist

- [x] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read Outloud
- [ ] Write 5 or more titles and pick the best on
- [ ] Create header image in canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to frontmatter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR


## Outline

# Git Branching and Greek Revival Style

Some things about modern development are just left overs from earlier eras. They are ways to do things that were suited to a particular time and place and now times have changed but no one has noticed yet.

I'm going to explain git branching strategies starting with something very simple and moving to add complexity as we go.  Eventaully we will end up back simple again. My hope is that you can find whereever you best fit along this continum and if your practises are more complicated then I describe then hopefully you have a good reason for it. 

You almost certainly know more about the best way to branch things in your project then I do, since I know nothing about your situation, but sometimes all it takes is random nudging from someone on the internet to cause the you to reconsider your workflow.  

And if your workflow involves a develop branch and you build SAAS software, I hope I can convince you to ditch it.

The develop branch, if you are doing cloud hosted stuff and don't need to patch bad versions is probably not what you want. You might be following some historical process that no longer serves a purpose. 

## The Story

The year is 2006 and Ashely starts a software business. She builds and sells a ecommerce solution she wrote in PHP. It's just her building an selling it but she uses a new source control solution called git to store her software. She starts out with Trunk based development.

# Trunk Based Development - Mainline Development

Trunk based development is working on a main, or trunk branch. Ashely commits her code right into the main branch and pushed it to the server where see setup her git remote.  

Sidenote: If she had choosen subversion or CVS, which we more popular in 2006, since git was fairly new, then her main branch would have been called `trunk` because every branch is branched off of the trunk, but like a real world tree. This is where the term trunk based development comes from. She is using `main` though so may prefer the term mainline development. 

Customers pay for her software and she emails them a link to the current head as a archive file using [git archive](https://git-scm.com/docs/git-archive). She is a php developer, so we whips up a simple script that called git archive for the branch reqested and returns an archive.

```
Thanks for paying for AshelySoft Ecommerce. Download you licensed copy here:
AshelySoft.com/release.php?branch=main

```

Customers then install her software on their servers where they run their ecommerce sites.

# Release Branches / Cutting a Release

Ashely's business succeeds, she has many more customers and hires more developers and a support person.  Support becomes difficult though as some customers are very slow to upgrade and its unclear what version any given customer is on. Additionally, its impossible for customers to keep up with the latest version when every commit is a new version and there are no version numbers.

So she decides to batch up the changes into montly releases and create a new release branch for each revision.  She could use tags for these releases, but branches and tags are pretty similar anyhow and she already has her cgi script for downloading a release.  Now her support people ask customers what version they are on and if its more then 2 releases in the past they have to upgrade to get their bugs fixes.  That is AshelySoft only supports the current release and two version backs.

## HotFixing and The Multiverse

This is all working great. Ashelys starts scaling the development team so that they can ship more features and the software velocity starts to really pick up. Unfortunately more bugs and regressions start to creep into the release because each monthly release contains more changes. 

Customers respond to this by not upgrading right away.  Smart customers who are well servered by the current product stay 2 releases back constantly, so that they can still get active support while letting the early adopters and new customers find most of the bugs.  Bugs do show up in the old version though and this is where things get interesting.

Up until now time as viewed by AshelySoft Ecommerce moves in a single strand forward in time. There is one `main` timeline. But now when bugs are found they need to be addressed in multiple versions of the product. And you can't simply ask people to upgrade, as they are back several version specifically because they are worried about the quality of the latest release.  They want the version they have plus the bug fixes, with no new development.

You are now in the hotfixing multiverse. Any bug found needs to be addressed in the lastest version, but also in all active version. Each release is a seperate timeline where active development ceased at the release date but bugs continued to be fixed. 

If you've seen any time travel movies, you probably releaze that this can get complex. What if a bug fix to back release introduces a bug of its own?  Thankfully AshelySoft is only supporting two active versions back and only supporting them for a couple of months. If she were supporting back version for several years she might find herself spending more and more time mainting several versions and the various versions would slowly drift away from each other.

Never the less release branches are huge help, it helps customers stay on a version that works for them while AshelySoft can still push new features. It increases the amount of effort fixing bugs but dealing with that will lead to Ashelysofts next innovation.

## Develop Branch and Fixing things

The cost for shipping bugs has now increased for AshelySoft. In the worse case a bug is not discovered until its in all active versions of the software and the code between version has changed enough that the fix is slightly different in each version, tripling the bug fix cost.

A solution for this does exist: Continuing with our timetravel / multiverse metaphore we need to travel back in time and stop the bug our releases branched off the main timeline.  AshelySoft does not have access to literal timetravel machines, but Ashely has an idea for achieving the end result: Catch the bugs before they are released.

A popular branching method called [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) has great suggestions for how to acheive this: you create a `develop` branch. Now all new work goes into `develop` and instead of 4 weeks of development in each release, you spend the last week stablizing `develop`. That is you make sure `develop` has no bugs as best you can and when it seems `stable` you merge it into main and then cut a release branch of off main.

> We consider origin/develop to be the main branch where the source code of HEAD always reflects a state with the latest delivered development changes for the next release. Some would call this the “integration branch”. This is where any automatic nightly builds are built from.
>
> When the source code in the develop branch reaches a stable point and is ready to be released, all of the changes should be merged back into master somehow and then tagged with a release number.

This whole process adds more overhead to the git and release process but its a fixed cost overhead and it saves a lot of HotFixing. AshelySoft, following the gitflow model also adds a continous intergration service, that runs automated tests on `develop` whenever new code is commited.

This setup, gitflow and CI on develop branch, with release branches and hotfixing serves AshelySoft for several years and while industry standard for the time it is complicated.  Thankfully, from here on out AshelySoft's process will only get simpler and the first thing to simplify things is `The Cloud`.

## The Cloud
AshelySoft customers want to run an ecommerce store, they do want to run a web server.  Ashely shifts the company to be a sass product and after some extensive work AshelySoft ecommerce becomes a multi-tenant ecommerce platform.  No more `git archive` releases, now the release process is deploying the latest version of main branch onto the production server.

There are downsides to this. AshelySoft now owns the uptime of all their customers and this is ecomerce so real money is lost when things go down. But, and its a huge but, they no longer have to support multi releases and they never have to hot fix bugs back into old versions.  No more multiverse of drifting branches to support -- no more release branches.  AshelySoft works off a simple rule, `main` must be releasable.  Before they merge `develop` into `main` they make sure the continous integration build is passing and if they find problems that CI missed they do their best to make sure CI will catch it in the future.

## GitHub Flow 

Around this time github private repos appear and AshelySoft moves from their own git hosting to github and starts following a Pull Request process. Instead of pushing code straight into `develop` and then ensuring they didn't break the build developers now create requests.  Other team members review the pull requests and the continous integration service runs its suite of tests on it.  The speed of getting code into develop has decreased but the quality of the develop branch is way up.  

## Death to Develop

With the quality of develop now increased AshelySoft is able to increase their release velocity.  They even adopt a continous deployment model where a merge into main causes the software to be automatically deployed.  From there they move to a Canary depolyment model where a new release is tested on the a small portion of web traffic before its fully rolled out.  Once a PR is merged the only branch merging that needs to be done is merging develop into main.

But what is the point of having develop and merging it into main? It was introduced to prevent the releasing of bugs by giving the software time to 'integrate' but AshelySoft is doing all the integration as part of the PR processs. So AshelySoft drops the develop branch.  

At this point Ashely and her company have come along way but sometimes what is old is new again. They are now back to doing trunk based or mainline development. Just like when Ashely built the first version, new features go into main and the HEAD of main is being constantly released.

### Lessons Learned

There is a lot about git merging strategies, continous integration and deployment that doesn't seem to make sense without understanding a historical context.  

For instance, calling software the runs tests on new code continous integration only makes sense when you understand the idea of a develop branch that was used as place to hold a release until it was 'integrated' - that is until is was stable enough to release. 

Ashely's story is fictional and history didn't neccarily unfold this way for all or even most software shops but I think its helpful to understand the where we are coming from. 

Some software, like the linux kernel, always had an extensive review process and much software is not cloud based and must continue to deal with release branches and backporting fixes.

But some software has moved to the cloud and yet hasn't yet embrassed the simplified workflows that cloud deployment can enable.

## Death To Develop

<<The Parthenon>>

The Parthenon was built in ancient greece using columns of marble. Theses columns of marble help hold it up. 

<<Greek Revival Style>>

This is a greek revival style house. These columns don't do anything.  

If you don't need to maintain and support multiple versions of your software and if your software only runs on your own servers then you might have a purely decorative develop branch. You may be using a git branching model that is very effective for software development practises that you are doing. Those are not load bearing columns, you are copying the visual appearnce of ancient greeks, not there architectural insights. 
<!-- 

don't have some testing process that is too expensive to do on each PR, then you probably just have a decorative develop branch and not a load baring develop branch. The cost may be small, but 


-----

If the software you are releasing is run by customers on their own hardware then things get more complex.  You can't simple produce a new release for every new commit into `main`. Customers won't be able to, nor be interested in upgraded that often.  And if your releases ever have regressions, customers start being cautions about upgrades and potentially even testing releases on their own before moving to them.  So you batch up the changes, making a release once a month, or once a week or at some frequency.  It's at this point that things start to get complex.

## Some heading

The problem is once you start batching up commits into releases and customers start upgrading and installing things at their own pace then you need to support more than one version of your software. A common practice is to support two versions back.  

A customer who is cautois about bugs may always stay two releases back, only upgrading when they are forced to to stay on a supported version. Their reason for using this strategy is simple, you've shipped releases with problems in them before, which only get straightened out after some time, so by handing back a release or two they try to avoid being the people discovering whatever the new regressions are.  

Unfortunately this sucks for you, because you now need to fix bugs in old versions of softwrae. Your linear software moving forward one step at a time has now changed.  If mainline development is a simple linear history then release branches bring us into the multi-verse of parellel branches. 

If you discover a bug in your existing softwrae you not only need to fix it in `main` you also need to hot-fix it back into your last two releases.  

Note: Tags vs Branches. Tags and branches are different, very slightly. They are both just pointers to a commit but one moves along with each commit and the other stays put. For the purposes of this article tags are ignored, but you could easily use a tag for a release and move it to hot fix. 




# GitFlow
# GitHub Flow
# Releasing stuff
  use a blue - green deploy, or rolloing deploy or canary deplot -->


