---
title: "Git Branching Strategies and The Greek Revival"
author: Adam
internal-links:
 - git merging
 - git branching
 - git merge
 - source control branch
 - git branch
bottomcta: false
excerpt: |
    Learn about the evolution of git branching strategies and how they have changed over time. Follow the story of Ashley, a software developer, as she navigates different branching models and discovers the benefits and challenges of each approach. Gain insights into the importance of continuous integration, deployment, and the impact of cloud-based workflows on branching strategies.
last_modified_at: 2023-07-19
categories:
  - shell
---
**This article explores git branching strategies. Earthly helps you build faster. [Learn how](https://cloud.earthly.dev/login).**

Some modern development practices are easiest to understand from a historical perspective: things started a certain way, and then steps were added or removed as conditions changed. Git branching, for example, is like that.

I'm going to explain various git branching strategies with a story. We will start with something straightforward and add complexity as we go. Eventually, we will end up back simple again.

I hope that explaining things this way will give you a deeper understanding of when to use specific branching and merging strategies. So instead of telling you how to cherry-pick a bug fix into a hotfix branch using GitFlow work, I can describe the conditions that would lead to adopting that process. Once you understand the whys, the hows will be easier.

## AshelySoft 2006

The year is 2006, and Ashley Protagonist starts a software business. She builds and sells an eCommerce solution she wrote in PHP. It's just her building and selling it, but she uses a new source control solution called git to store her software. She starts with trunk-based development.

## Trunk Based Development

Trunk-based development is working on the main, or trunk branch. Ashley commits her code right into the main branch on her local machine and, when she has complete a feature, she pushes her code to the source control server.  

Customers pay for her software, and she emails them a link to the current version as an archive file using [git archive](https://git-scm.com/docs/git-archive). She is a PHP developer, so she whips up a simple PHP script that returns the git archive for the branch requested.

{% picture content-wide {{site.pimages}}{{page.slug}}/email2.png --picture --alt {{ grab your copy of AshelySoft }} %}

<figcaption>Simple Release Distribution</figcaption>

Her customers then install her software on their web servers, where they use it to run their eCommerce businesses.

<div class="notice--info">

## MainLine Development

### Fun Fact: Trunk VS. Main

If Ashley had chosen subversion or CVS, which were more prevalent in 2006, she would have called her branch `trunk` because every branch is branched off the trunk like a real-world tree. This is where the term trunk-based development comes from. However, Ashley uses `main`, so she may prefer the term mainline development. It's the same thing, just a different name.
</div>

## Release Branches

Ashley's business succeeds. She acquires many more customers and hires more developers and a customer-support person. Support becomes problematic, though, as some customers are very slow to upgrade, and it's unclear what version any given customer is on. Additionally, customers can't keep up with the latest version when every commit is a new version, and there are no version numbers.

So she decides to batch up the changes into monthly releases and create a new release branch for each revision. Of course, she could use tags for these releases, but branches and tags are pretty similar, and she already has her release script in place.  

Now her support people can ask customers what version they are on. If it's more than two releases back, they ask them to upgrade. That is, AshelySoft only supports the current release and the two previous versions.

<div class="notice--info">

## Cutting a Release

There was a time before modern source control when creating a release branch was an expensive process that had to be planned. "Cutting a Release" was the name for this process, which involved locking down the source and starting the lengthy process of 'cutting a release branch off the trunk'. People still use the phrase today.

> "Well, the performance was so bad that when they wanted to cut a branch, they would announce it ahead of time. They would schedule the branching because you didn't want anybody else committing while you were branching, because that would totally screw things up. Right? And I said, "Okay, Friday at 2:00 pm., we're going to cut the branch." Then all activity would stop, access to the server would be cut off."
>
> And it would take 45 minutes to cut this branch. And then you'd say, "Okay, we've opened up the branch. Everybody can start working again."
>
> [Jim Blandy](https://corecursive.com/software-that-doesnt-suck-with-jim-blandy/) creator of Subversion
</div>

## Hot Fixes and the Multiverse

This is all working great. Ashley starts scaling the development team, and they start shipping more features. Unfortunately, while each monthly release now contains more cool new features, more regressions and bugs start slipping into the releases as well.

Some customers respond to this by not upgrading right away. If they are well-served by the current product, they can stay two releases back and get active support while giving the latest release time to stabilize. Bugs do show up in the old versions, though, and this is where things get interesting.

Up until now, time, as viewed by AshelySoft's source control, moves forward in a single line. There is one `main` branch that represents one linear release timeline. But now, when bugs are found, they need to be addressed in multiple versions of the product. And you can't simply ask people to upgrade because they are still on a supported version, and they are correctly worried about the quality of the latest release. They want the version they have plus the bug fixes, with no new development.

You are now in the hot fixing multiverse. AshelySoft has to fix bugs in the latest version and all other active versions. Each release is a separate timeline where active development ceased at the release date, but bugs continued to be fixed.

If you've seen any time travel movies, you probably realize that this can get complex. What if a bug fix to back release introduces a bug of its own? Thankfully AshelySoft is only supporting two active versions back and only supporting them for a couple of months. Suppose they were supporting back versions for several years. In that case, they might find themselves spending more and more time maintaining all these versions, and the various versions would slowly drift away from each other.

Nevertheless, release branches are an enormous help for AshelySoft. They help customers stay on a version that works for them, while AshelySoft can still push new features. However, it does increase the amount of effort that fixing bugs requires, and dealing with that will lead to AshelySoft's next innovation.

## The `develop` Branch

The cost of shipping bugs has now increased for AshelySoft. In the worse case, a bug isn't discovered until it's in all active versions of the software and the code between versions has changed enough that the fix is slightly different in each version, tripling the bug fix cost.

Fortunately, a solution for this does exist: Continuing with our time travel/multiverse analogy, we need to travel back in time and stop the bug before our releases branches off the main timeline. Unfortunately, AshelySoft does not have access to literal time travel machines, but Ashley has a more straightforward idea: Catch the bugs before they are released.

## GitFlow to the Rescue

A popular branching method called [GitFlow](https://nvie.com/posts/a-successful-git-branching-model/) has excellent suggestions for achieving this: you create a `develop` branch. So now all new work goes into `develop,` and instead of 4 weeks of development in each release, you spend the last week stabilizing `develop`. You make sure `develop` has no bugs as best you can, and when it seems stable, you merge it into main and then cut a release branch off main.

> "We consider origin/develop to be the main branch where the source code of HEAD always reflects a state with the latest delivered development changes for the next release. Some would call this the "integration branch". This is where any automatic nightly builds are built from."
>
> "When the source code in the develop branch reaches a stable point and is ready to be released, all of the changes should be merged back into master somehow and then tagged with a release number."
>
> GitFlow Explanation

This whole process adds more overhead to the branching and release process, but it's a fixed cost overhead, and it saves a lot of HotFixing bugs on release branches. AshelySoft, following the git-flow model, also adds a [continuous integration](/blog/continuous-integration) service. When new code shows up in `develop`, [automated tests](/blog/unit-vs-integration) are run.

This setup, git-flow and CI on develop branch, with release branches and hot fixing serves AshelySoft for several years. However, it is a complicated process. Thankfully, from here on out, AshelySoft's process will only get simpler. The first thing that helps to simplify things is `The Cloud`™️.

## The Cloud

AshelySoft customers want to run an eCommerce store. However, they don't want to run a web server. After repeatedly getting this feedback, Ashley shifts the company to be a Software-As-A-Service (SAAS) company. It takes some extensive work, but AshelySoft eCommerce becomes a multi-tenant eCommerce platform. No more `git archive` releases. Now the release process is deploying the latest version of the main branch onto the production server.

There are downsides to this SAAS model. AshelySoft now owns the uptime of all their customers, and this is eCommerce, so real money is lost when things go down. But, the customers are willing to pay more for AshelySoft to worry about these problems. They no longer have to support multi releases at a time - no more hot fixing bugs back into old versions, no more multiverse of drifting branches to update, and no more release branches. To make this work, AshelySoft works off a simple rule: `main` must be releasable. Before anyone can merge `develop` into `main` they must make sure the continuous integration build is passing, and if they find problems that the CI process missed, they do their best to make sure CI will catch it in the future.

## GitHub Flow

Around this time, GitHub private repositories appear, and AshelySoft moves from their own git hosting to GitHub and starts following a Pull Request process. Instead of pushing code straight into `develop` and then ensuring they didn't break the build, developers now create pull-requests. Other team members review the pull-requests, and the continuous integration service runs its suite of tests right on the PR. As a result, the speed of getting code into `develop` has decreased, but with each PR being manually reviewed and automatically tested, the quality of code that makes it into the `develop` branch is way up.  

## Death to `develop`

With the quality of `develop` now increased, AshelySoft can increase its release velocity. They even adopt a continuous deployment model where a merge into `main` causes the software to be automatically deployed. From there, they move to a [Canary deployment model](/blog/deployment-strategies/#canary-deployment) where a new release is tested on a small portion of web traffic before it's fully deployed. Once a PR is merged, Ashley just has to merge `develop` into `main` to perform a release.

But what is the point of having `develop` and merging it into `main`? It was introduced to prevent the release of bugs by giving the software time to 'integrate', but AshelySoft is doing all the integration as part of the PR process. So they drop the `develop` branch.  

Ashley has come a long way but sometimes what is old is new again. She is now back to doing trunk-based or mainline development. Just like when she built the first version: features go into `main`, and the HEAD of `main` is constantly released.

## Lessons Learned

There is a lot about git merging strategies, continuous integration, and deployment that doesn't seem to make sense without going through a long journey like Ashely's.  

For instance, calling software that builds and tests code a continuous integration process only makes sense when you understand what non-continuous integration was. It was spending time manually testing the upcoming release for days or even weeks before feeling confident enough to release it.

Ashely's story is fictional, and history didn't necessarily unfold this way for all or even most software shops, but I think it's helpful to understand where we are coming from and how cloud and SAAS workflows influence branching models.

Some software always had an extensive review process, and much software will never be cloud-based and will continue to deal with release branches and backporting fixes. But some software has moved to the cloud and yet hasn't embraced the simplified workflows that cloud deployment can enable.

## Appendix: Develop and The Greek Revival Style

{% picture content-wide {{site.pimages}}{{page.slug}}/greek-columns.jpg --picture --alt {{ The Parthenon }} %}

The Parthenon was built in ancient Greece using columns of marble. These columns of marble held it up.

{% picture content-wide {{site.pimages}}{{page.slug}}/greek-revival.jpg --picture --alt {{ A Greek Revival House }} %}

This is a greek-revival style house. These columns are not about function but form -- they are unnecessary and were chosen for aesthetic purposes.  

If you don't need to maintain and support multiple versions of your software and it only runs on your servers, then you might have a purely decorative `develop` branch. You may be using a git branching model that is very effective for a software lifecycle that you yourself are not in fact practicing. Those might not be load-bearing functional columns -- you might be copying the visual appearance of the ancients without understanding the purpose they had in mind.

The creator of GitFlow offers similar thoughts:

> Web apps are typically continuously delivered, not rolled back, and you don't have to support multiple versions of the software running in the wild.
>
> If your team is doing continuous delivery of software, I would suggest to adopt a much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team.
>
> GitFlow Creator Vincent Driessen

The closer you can stay to trunk-based or mainline development, the less overhead you will have and the smaller the batches you'll be able to release.
