---
title: "Git Branching Strategies and The Greek Revival"
categories:
  - Tutorials
toc: true
author: Adam
internal-links:
 - merging
 - branching
 - merge
 - git
 - branch
---

## Writing Article Checklist

- [x] Write Outline
- [x] Write Draft
- [x] Read Outloud
- [ ] Fix Grammarly Errors
- [ ] Write 5 or more titles and pick the best on
- [ ] Create header image in canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to frontmatter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

## Introduction 

Some modern development practices are easiest to understand from a historical perspective: things started a certain way, and then steps were added or removed as conditions changed. Git branching, for example, is like that.

I'm going to explain various git branching strategies with a story. We will start with something straightforward and add complexity as we go.  Eventually, we will end up back simple again. 

I hope that explaining things this way will give you a deeper understanding of when to use specific branching and merging strategies.  So instead of telling you how to cherry-pick a bug fix into a hotfix branch using gitflow work, I can describe the conditions that would lead to adopting that process. Once you understand the whys, the hows will be easier. 

## AshelySoft 2006

The year is 2006, and Ashely Protagonist starts a software business. She builds and sells an eCommerce solution she wrote in PHP. It's just her building and selling it, but she uses a new source control solution called git to store her software. She starts with trunk-based development.

## Trunk Based Development

Trunk-based development is working on the main, or trunk branch. Ashely commits her code right into the main branch on her local machine and, when she has complete a feature, she pushes her code to the source control server.  

Customers pay for her software, and she emails them a link to the current version as an archive file using [git archive](https://git-scm.com/docs/git-archive). She is a PHP developer, so she whips up a simple PHP script that returns the git archive for the branch requested.

{% picture content-wide {{site.pimages}}{{page.slug}}/email2.png --picture --alt {{ grab you copy of ashelysoft }} %}

<figcaption>Simple Release Distribution</figcaption>

Her customers then install her software on their web servers, where they use it to run their eCommerce businesses.

<div class="notice--info">

## MainLine Development

**ℹ️ Fun Fact: Trunk VS. Main**

If Ashely had chosen subversion or CVS, which were more prevalent in 2006, she would have called her branch `trunk` because every branch is branched off the trunk like a real-world tree. This is where the term trunk-based development comes from. However, Ashely uses `main`, so she may prefer the term mainline development. It's the same thing, just a different name.
</div>

## Release Branches / Cutting a Release

Ashely's business succeeds. She acquires many more customers and hires more developers and a customer-support person.  Support becomes problematic, though, as some customers are very slow to upgrade, and it's unclear what version any given customer is on. Additionally, customers can't keep up with the latest version when every commit is a new version, and there are no version numbers.

So she decides to batch up the changes into monthly releases and create a new release branch for each revision. Of course, she could use tags for these releases, but branches and tags are pretty similar, and she already has her release script in place.  

Now her support people can ask customers what version they are on. If its more than 2 releases back, they ask them to upgrade. That is, AshelySoft only supports the current release and the two previous versions.

## HotFixing and The Multiverse

This is all working great. Ashely starts scaling the development team and they start shipping more features. Unfortunately, while each monthly release now contains more cool new features, more regressions and bugs start slipping into the releases as well.

Some customers respond to this by not upgrading right away. If they are well-served by the current product they can stay two releases back and get active support while giving the latest release time to stabilize. Bugs do show up in the old versions, though, and this is where things get interesting.

Up until now, time, as viewed by AshelySoft's source control, moves forward in a single line. There is one `main` branch that represents one linear release timeline. But now, when bugs are found, they need to be addressed in multiple versions of the product. And you can't simply ask people to upgrade because they are still on a supported version, and they are correctly worried about the quality of the latest release.  They want the release they have plus the bug fixes, with no new development.

You are now in the hot fixing multiverse. AshelySoft has to fix bugs in the latest version and all other active versions. Each release is a separate timeline where active development ceased at the release date, but bugs continued to be fixed.

If you've seen any time travel movies, you probably realize that this can get complex. What if a bug fix to back release introduces a bug of its own?  Thankfully AshelySoft is only supporting two active versions back and only supporting them for a couple of months. Suppose they were supporting back versions for several years. In that case, they might find themselves spending more and more time maintaining all these versions, and the various versions would slowly drift away from each other.

Nevertheless, release branches are an enormous help for AshelySoft. They help customers stay on a version that works for them, while AshelySoft can still push new features. However, it does increase the amount of effort that fixing bugs requires, and dealing with that will lead to Ashelysoft's next innovation.

## Develop Branch and Fixing things

The cost of shipping bugs has now increased for AshelySoft. In the worse case, a bug isn't discovered until it's in all active versions of the software and the code between versions has changed enough that the fix is slightly different in each version, tripling the bug fix cost.

Fortunately, a solution for this does exist: Continuing with our time travel/multiverse analogy, we need to travel back in time and stop the bug before our releases branches off the main timeline. Unfortunately, AshelySoft does not have access to literal time travel machines, but Ashely has a more straightforward idea: Catch the bugs before they are released.

## GitFlow To The Rescue

A popular branching method called [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) has great suggestions for how to achieve this: you create a `develop` branch. So now all new work goes into `develop,` and instead of 4 weeks of development in each release, you spend the last week stabilizing `develop`. You make sure `develop` has no bugs as best you can, and when it seems stable, you merge it into main and then cut a release branch off main.

> "We consider origin/develop to be the main branch where the source code of HEAD always reflects a state with the latest delivered development changes for the next release. Some would call this the "integration branch". This is where any automatic nightly builds are built from."
>
> "When the source code in the develop branch reaches a stable point and is ready to be released, all of the changes should be merged back into master somehow and then tagged with a release number."
>
> GitFlow Explanation 

This whole process adds more overhead to the branching and release process, but it's a fixed cost overhead, and it saves a lot of HotFixing bugs on release branches. AshelySoft, following the git-flow model, also adds a continuous integration service. When new code shows up in `develop`, automated tests are run.


This setup, git-flow and CI on develop branch, with release branches and hot fixing serves AshelySoft for several years. However, it is a complicated process and thankfully, from here on out, AshelySoft's process will only get simpler. The first thing help to simplify things is `The Cloud`.

## The Cloud

AshelySoft customers want to run an eCommerce store. However, they don't want to run a web server.  After repeatedly getting this feedback, Ashely shifts the company to be a sass product company.  It takes some extensive work, but AshelySoft eCommerce becomes a multi-tenant eCommerce platform.  No more `git archive` releases. Now the release process is deploying the latest version of the main branch onto the production server.

There are downsides to this SAAS model. AshelySoft now owns the uptime of all their customers, and this is eCommerce, so real money is lost when things go down. But, the customers are willing to pay more for AshelySoft to worry about these problems. They no longer have to support multi releases at a time - no more hot fixing bugs back into old versions, no more multiverse of drifting branches to update, and no more release branches.  To make this work, AshelySoft works off a simple rule: `main` must be releasable.  Before they merge `develop` into `main` they make sure the continuous integration build is passing, and if they find problems that the CI process missed, they do their best to make sure CI will catch it in the future.

## GitHub Flow

Around this time, GitHub private repos appear and AshelySoft moves from their own git hosting to github and starts following a Pull Request process. Instead of pushing code straight into `develop` and then ensuring they didn't break the build, developers now create pull requests.  Other team members review the pull requests and the continous integration service runs its suite of tests right on the PR.  The speed of getting code into develop has decreased but with each PR being manually reviewed and automatically tested, the quality of code that makes it into the develop branch is way up.  

## Death to Develop

With the quality of develop now increased AshelySoft is able to increase their release velocity.  They even adopt a continous deployment model where a merge into main causes the software to be automatically deployed.  From there they move to a Canary deployment model where a new release is tested on the a small portion of web traffic before its fully rolled out.  Once a PR is merged the only branch maintenance that needs to be done is merging develop into main to perform a release.

But what is the point of having develop and merging it into main? It was introduced to prevent the releasing of bugs by giving the software time to 'integrate' but AshelySoft is doing all the integration as part of the PR processs. So AshelySoft drops the develop branch.  

At this point Ashely and her company have come along way but sometimes what is old is new again. They are now back to doing trunk based or mainline development. Just like when Ashely built the first version, new features go into main and the HEAD of main is being constantly released.

## Lessons Learned

There is a lot about git merging strategies, continous integration and deployment that doesn't seem to make sense without understanding a historical context.  

For instance, calling software the runs tests on new code continous integration only makes sense when you understand the idea of a develop branch that was used as place to hold a release until it was 'integrated' - that is until is was stable enough to release.

Ashely's story is fictional and history didn't neccarily unfold this way for all or even most software shops but I think its helpful to understand the where we are coming from and how cloud and SAAS workflows influence branching models.

Some software always had an extensive review process and much software is not cloud based and must continue to deal with release branches and backporting fixes. But some software has moved to the cloud and yet hasn't yet embrassed the simplified workflows that cloud deployment can enable.



## Appendix: Develop and The Greek Revival Style


{% picture content-wide {{site.pimages}}{{page.slug}}/greek-columns.jpg --picture --alt {{ The Parthenon }} %}

The Parthenon was built in ancient greece using columns of marble. These columns of marble help hold it up.

{% picture content-wide {{site.pimages}}{{page.slug}}/greek-revival.jpg --picture --alt {{ A Greek Revival House }} %}

This is a greek revival style house. These columns are not about function but about form.  They are unnecessary and choosen for asthetics purposes.  

If you don't need to maintain and support multiple versions of your software and if your software only runs on servers control, then you might have a purely decorative develop branch. You may be using a git branching model that is very effective for a software lifecycle that you yourself are not in fact practising. Those might not be load bearing columns, you might be copying the visual appearance of the ancients, without understanding their architectural perspective.

The creator of GitFlow offers similar thoughts:

>  Web apps are typically continuously delivered, not rolled back, and you don't have to support multiple versions of the software running in the wild.
>
>  If your team is doing continuous delivery of software, I would suggest to adopt a much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team.
>
>  Vincent Driessen Gitflow Creator

The closer you can stay to trunk based or mainline development the less overhead you will have and the smaller batches you'll be able to release in. 
