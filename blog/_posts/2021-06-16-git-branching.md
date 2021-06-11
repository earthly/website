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

Sidenote: If she had choosen subversion or CVS, which we more popular in 2006, since git was fairly new, then her main branch would have been called `trunk` because every branch is branched off of the trunk, but like a real world tree. 

Customers pay for her software and she emails them a link to the current head as a archive file using git archive.
```
Git archive  ...
```

Customers then install her software on their servers where they run their ecommerce sites.


<!-- In subversion and CVS this branch was called trunk and in git this was instead called `master` and now `main`. 

Sidenote: Not using `master` as the main branch name makes total sense to me, but why `main` why not go back to `truck`? -->

<!-- In my early days of software development, a variation on Trunk based development was exactly what we did: when I was done with the feature I was working on it would go into main, where it would get tested and potentially released. From there things got more complex. -->

# Release Branches / Cutting a Release

Ashely's business succeeds, she has many more customers and hires more developers and a support person.  Support becomes difficutl though as some customers are very slow to upgrade and its unclear what version any given customer is on. Addiontionally its impossible for customers to keep up with the latest version when every commit is a new version.

So she decides to batch up the changes into montly releases and create a new release branch for each revision.  She could use tags for these releases, but branches and tags are pretty similar anyhow and she already has her cgi script for downloading a release.  Now her support people ask customers with bugs what version they are on and if its more then 2 releases in the past they have to upgrade first.  That is AshelySoft only supports the current release and two version backs.

## HotFixing and The Multiverse

This is all working great. Ashelys starts scalign the development team so that they can ship more features and the software velocity starts to really pick up. Unfortunately as each monthly release contains more and more changes bugs and regressions start to creep in.

Customers respond to this by not upgrading right away.  Smart customers who are well servered by the current product stay 2 releases back constantly, so that they still get active support but the early adopters find most of the bugs.  Bugs do show up in the old version though and this is where things get interesting.

Up until now time as viewed by AshelySoft Ecommerce moves in a single strand forward in time. There is one `main` timeline. But when bugs are found old supported versions, they need to be addressed. And they need to be addressed in all the supported versions.  You can't simply ask people to upgrade, as they are back several version specifically because they are worried about the quality of the latest release.  They what the version they have plus the bug fixes, with no new development.

You are now in the world of hotfixing and the multiverse. Any bug found need to be in the lastest version, but also in active version, whih can be viewed as a serpate timeline where active development ceased at release time but bugs continued to be fixed. 

If you've seen any time travel movies, you probably releaze that this can get complex. What if a bug fix to back release introduces a bug of its own?  Thankfully AshelySoft is only supporting two active versions back and only supporting them for a couple of months. If she were supporting back version for several years she might find herself slowly being spending more and more time mainting several old versions that slowly drift away from each other.

Never the less release branches are huge help, it helps customers stay on a version that works for them while AshelySoft can still push new features. It increases the amount of effort fixing bugs but dealing with that will lead to Ashelysofts next innovation.

## Develop Branch and Fixing things
Up until 




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
  use a blue - green deploy, or rolloing deploy or canary deplot


