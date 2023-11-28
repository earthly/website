---
title: Monorepo vs Polyrepo
featured: true
categories:
  - Articles
sidebar:
  nav: monorepos
tags:
- monorepo
- polyrepo
- tech-strategy
author: Vlad
internal-links:
  - mono repo
  - poly repo
  - monorepo
  - polyrepo
topic: monorepo
funnel: 2
excerpt: |
    This article explores the debate between using a monorepo or a polyrepo structure for source code. It discusses the benefits and challenges of each approach, as well as the hybrid option. Whether you're interested in ease of importing, contributions within and across projects, viewing diffs, structure of releases, builds and CI, open-source considerations, or issue tracking, this article provides insights to help you make an informed decision.
last_modified_at: 2023-07-11
---
**In this article, we'll examine the key choices in organizing repositories. Struggling with monorepo builds? Earthly's containerized method can streamline your continuous integration process. [Learn more](/).**

The decision of whether to use a monorepo or a polyrepo structure for your source code can be a very emotional (maybe even religious!) battle. On its surface, it's not much different than "tabs vs spaces" or "vim vs emacs". Or is it?

In the following, I will attempt to draw objective, logical arguments for both approaches and also throw in a very popular third option: the hybrid.

## A Quick Intro To Monorepos

The **monorepo layout** consists of a single code repository where multiple projects coexist in a hierarchical directory structure. For example:

```
├── lib
|   ├── lib
|   └── lib
├── lib
├── lib
├── lib
├── app
|   ├── lib
|   └── lib
|       ├── lib
|       └── lib
├── app
|   └── lib
└── big-project
|   ├── lib
|   ├── app
|   |   ├── lib
|   |   └── lib
|   └── app
|       └── lib
└── big-project
    ├── lib
    ├── lib
    ├── app
    |   └── lib
    └── app
        ├── lib
        └── lib
```

Each `lib` and each `app` would contain various other sub-directories to house the source code itself, depending on the language it is written in. You get the idea.

In **polyrepo layout** (sometimes also called **multi-repo layout**), on the other hand, the code is spread across... well multiple repositories. The degree to which the separation between logical pieces of code can vary from language to language and from style to style. [^1]

Here's an example possible structure.

```
github.com/myorg/app1
├── docs
├── examples
├── src
└── tests

github.com/myorg/app2
├── docs
└── src

github.com/myorg/app3
├── lib
|   └── src
├── lib
|   └── src
└── lib
    └── src

github.com/myorg/lib1
└── src
```

Each repository is focused on specific functionality. The structure of the repository is usually heavily influenced by the best practices of the language they host.

A third alternative that some people use is the **hybrid repository layout**, whereby some components coexist in one or more monorepos, while others are separated in their own isolated, smaller repositories. Deciding which component goes where may be influenced by team ownership, the language of the code, whether the component is open or closed source, and other factors.

## Judging Criteria

The structure of your source code empowers or impedes various engineering processes. It is the lifeblood of your technical product and it needs to account for all the possible ways it can be used. To avoid boiling the ocean with this article, however, we will focus on the most popular use-cases and characteristics:

* Ease of importing
* Ease of contributing within and across projects
* Viewing diffs
* Structure of releases
* Builds and CI
* Open vs closed source
* Issue tracking

Further, we will make certain assumptions about the underlying technologies used: for example, we will assume that you are using GitHub for the repositories and the issue tracking. The considerations typically apply to most other setups that do not necessarily use these technologies. They work similarly.

## Let's Take a Look

### Imports

![Overhead view of shipping containers]({{site.images}}{{page.slug}}/kyCNGGKCvyw.jpg)\

You can't talk about the code layout, without looking primarily at how code can be imported and reused. Different languages can vary wildly in the way code can be imported.

For example, in Go, you have the freedom to reference just about any package (directory) in any repository with ease. There are mechanisms to automatically download any remote code and use it, via the new [modules features](https://blog.golang.org/using-go-modules). For Go, it is just as easy to use monorepos or polyrepos for code imports.

In Java, on the other hand, you cannot simply import a GitHub repository - you have to first publish a JAR to an repository, and then reference that JAR in your Java-specific build file. So it becomes far easier to reference a package in the same repository than across repositories setup-wise. But the code can become unwieldy. For this reason, some Java monorepo layouts tend to stick with segmenting the code across separate modules, each possibly producing separate artifacts. See for example [multi-module Maven builds](https://maven.apache.org/guides/mini/guide-multiple-modules.html).

JavaScript tends to be spread across multiple repositories typically. To use a package from one repository to another, however, the package needs to be published to npm. It's less popular to use a monorepo layout with JavaScript, however, if you would like to experiment, there are a number of tools to help out with the directory organization, such that each project gets its own separate `package.json`. [Lerna](https://github.com/lerna/lerna) is one such tool.

**Verdict**: It depends heavily on the language. Even if the language requires a package repository in the middle when referencing code across source repositories, it still seems like polyrepos are more popular. When using a monorepo layout, it's often preferable to create distinct modules of each project and some communities have developed tools to help with that.

### Contributions Within the Same Project

![People talking around a table]({{site.images}}{{page.slug}}/cKQkMFzXHAI.jpg)\

Making changes to source code can be isolated to one specific area, or it can span multiple functional concerns and thus need to cross-project boundaries. The developer experience may vary depending on how the code is laid out.

When viewing changes to a single project, it is easier to visualize the history of changes in GitHub in a polyrepo setup, by simply navigating the list of pull requests. In a monorepo setup, however, all the pull requests are mixed together; your best bet, in that case, is to first open the specific sub-directory you are interested in and then clicking the **History** link. If you have squash merges enabled, you can easily navigate the PR from the commit message.

![Click on History]({{site.images}}{{page.slug}}/history.png)\

**Verdict**: Managing contributions within the same project is easier with a polyrepo layout, as it is easier to track the history of changes per-repository rather than per-directory.

### Contributions Across Projects

![Two people working at a whiteboard]({{site.images}}{{page.slug}}/26MJGnCM0Wc.jpg)\

When making contributions across multiple projects, there is a significant distinction. Arguably, this is one of the main reasons to use the monorepo layout. When everything is in a single repository, many cross-cutting concerns can be modified and submitted as a single, atomic PR. For example, you could write code for a new feature and make adjustments end-to-end: UI, backend, API, DB schema migration, documentation, etc. The simplicity of the dev-test and contribution process really shines in monorepos, when done right [^2]. Atomic PRs also help to visualize changes for review. It is easier to see a feature take shape when the changes across projects are visible in one place.

In polyrepos, cross-cutting changes need to be performed as separate distinct PRs. Although it is more work to open separate PRs, it's sometimes useful to create the mindfulness that the components are landing asynchronously in production (for example, if these are separate microservices talking to each other).

One of the challenging aspects of contributing across multiple repositories is that the dependencies are often referenced as a pinned version number. If you change project B on the `main` branch and it is referenced by project A as `v1.2.3`, then you will need to work out a way to test project A with the latest of project B for development, or, as a workaround, perform a release of project B and update project A to now point to `v1.2.4`. This creates possible significant hurdles for the developer to go through and for this reason, developers get discouraged to contribute to other team's codebases unless they really have to.

Another possible side-effect of dependency version pinning is what I call *delayed integration breaking*: the `main` branch of project B no longer works with project A due to some change performed in the past. Project A has been pointing to `v1.2.3` for a long time, while project B has been evolving independently. The first time this is discovered is when a developer attempts to make a change to B, which is needed in A. This, again, contributes to the hurdles developers face when contributing across repositories and creates hidden technical debt.

Dependency version pinning is not a bad thing in and of itself. If the two projects are well separated and the team maintaining the dependency is aware of maintaining compatibility (and enforces this with proper testing), then this is often preferred. After all, the way we typically consume open-source software relies on this model and it is very successful. However, if two projects need to evolve together tightly, then a possible alternative might be always referencing the `main` branch version (in Java, this is known as the [`SNAPSHOT` version](https://www.tutorialspoint.com/maven/maven_snapshots.htm)) as the dependency and thus being able to catch integration regressions much more quickly. During a release, all `SNAPSHOT` references would need to be updated to pinned versions, however.

Another option might be to use a bot that regularly updates dependencies. The support for such a bot may be language-specific, however. Here's an [example of Scala Steward in action](https://github.com/tenable/Kastle/pull/165).

Finally, in polyrepo setups developers have the option to use staggered dependency upgrades: the ability to update a dependency gradually across other projects and thus control the way a change is rolled out. In a monorepo setup, this would be achieved through other means, such as [feature flagging](https://martinfowler.com/articles/feature-toggles.html).

**Verdict**: Managing contributions across projects is usually easier in a monorepo layout, as PRs can make changes across several components at the same time and there is no need to constantly update the referenced version of dependencies. In addition, integration breakages are obvious immediately.

### Releases

![Container Ship At Sea]({{site.images}}{{page.slug}}/y8TMoCzw87E.jpg)\

One of the key deciding factors of the source code layout is the structure of the releases. Depending on the deliverable type (library, app), the release might have multiple forms: an artifact, a language-specific package, a Docker image, an installer, etc.

For polyrepo layouts, you typically have one deliverable per repository. Whether that's a repository for microservice (for example a Docker image) or a library to perform some reusable functionality (like an artifact), you typically only have one of these. This allows for each repository to have its own release cycle and to manage its own tags. This is especially great when different projects are managed by different teams, each with their own distinct style or release requirements.

In monorepo layouts, a typical tendency is to release everything at the same time. This is usually a mistake. It is not mandatory for monorepo setups to use this tactic, but it is an especially attractive one due to its apparent simplicity. In such a situation, the entire repository is tagged once for everything, and pushed to production at the same time. This type of monolithic releasing can be very problematic for release agility, and for maintaining a low mean-time-to-resolution (MTTR), in case of failures. In modern cloud development, releases need to happen weekly, daily, or even on every merge to main. If something critical is broken, you also want to be able to ship fixes in less than an hour - maybe even less than 10 minutes. If you have a critical fix to push to production, but some unrelated test is failing in a different project, then a monolithic release cycle is getting in the way. In larger teams, monolithic releases are virtually impossible due to the ever-changing state of the build across projects. (The only thing a big bang guarantees is a big boom!)

An alternative approach to monolithic releases is for each project in a monorepo to have its own release cycle, despite coexisting in the same repository. This is key to allowing releases in monorepos to work properly. This might mean that you have independent tags for each project (for example `projecta-v1.2.3`, `projectb-v4.5.6`, or `projectc-v7.8.9`) or no tags at all - just use `main` branch commit hashes - or a global auto-incrementing tag, that increases the version number on each commit (really, this last option is similar to using `main` commit hashes, except that more human-readable tags are used instead). In this case, each project executes a release based on the tags on independent schedules. This strategy relies on every merge to `main` to be considered as "ready for production", however, this is generally a good practice anyway.

The takeaway here is that for monorepos, you should not think that atomic PRs mean atomic releases. That is unrealistic in typical production environments. At the development level, yes you get to group together cross-cutting changes and merge as an atomic unit. At the release and production level, however, you still need another layer of indirection for allowing services to be updated independently. A very common such layer is the Docker image repository (or in more traditional environments, a package repository). If each `main` branch build produces tagged Docker images, then these images can be pushed to production separately, according to independent schedules.

Of course, with any set of related changes that go out independently across multiple microservices, care must be taken such that the changes are forwards and backwards compatible. In a polyrepo setup, the need for such compatibility guarantees is typically more intuitive to the developer. In a monorepo setup, however, the developer needs to be aware, again, that an atomic PR does not mean an atomic release.

**Verdict**: Multiple factors can influence your decision here: team layout, release frequency requirements, MTTR requirements, level of cohesion of separate projects, and so on. Generally, polyrepos have the added benefit that the better engineering process decisions fall in place more naturally. In addition, the collection of tags usually make more sense for polyrepos.

### Builds and CI

![Cranes building skyscraper]({{site.images}}{{page.slug}}/8Gg2Ne_uTcM.jpg)\

The Achilles' heel of the monorepo is often the build. Most open-source build tooling handles builds project-by-project and does not deal with cross-project builds out of the box. For this reason, building multiple projects in a monorepo setup usually ends up in a complex do-it-yourself scripting endeavor. Where this usually falls apart is the ability to scale the size of the monorepo while maintaining reasonable build times (say less than 15 minutes).

A number of monorepo build solutions exist out there, such as [Bazel](/blog/monorepo-with-bazel), [Pants](https://www.pantsbuild.org/) or [Buck](https://buck.build/). Some of them are very advanced, however, they require a huge commitment towards maintaining the setup and compromising interoperability with other open-source tools. These setups are preferable in very large development teams (1000+) where a dedicated build team can support specific needs of the engineering organization. Google, Facebook, and Twitter are examples of teams that have adopted such systems. For the rest of us, the options are more limited.

Of the popular [CI vendors](/blog/continuous-integration) (GitHub Actions, Circle CI, Jenkins), few of them offer triggers based on [subdirectories](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#onpushpull_requestpaths) (to help minimize unnecessary builds) and, in addition, caching needs to be handled manually for each project. In a monorepo setup, arguably CI caching is absolutely critical to get right in order to be able to scale the repository size, and yet no silver bullet type of solution exists.

Polyrepos have generally been much better supported by build systems and by CIs. Dealing with each repository completely independently renders the scale issue irrelevant.

However, there are still use-cases that cannot be easily accommodated: for example, if you make a change in a dependency, it is difficult to automatically rebuild all the dependants to ensure that nothing was affected. This additional verification needs to be performed manually in practice (and more often than not, it is never done at all). This particular limitation becomes apparent when needing to develop [integration testing](/blog/unit-vs-integration) or end-to-end testing. A collection of microservices might be started altogether to perform a complex task as part of a test. If the test resides in repository A, and the microservices reside in repositories B, C, and D, then changes to B, C and D should automatically trigger the integration test to be re-run. To achieve this automated interoperability, each of these dependencies needs to be manually wired via [custom API calls](https://docs.github.com/en/rest/reference/repos#create-a-repository-dispatch-event) (if these are supported by your CI vendor).

A third possibility also exists, which I call the *hybrid layout*. Because monorepo builds are difficult to scale, some development teams reach a compromise in the middle: keep some projects grouped together in a single repository and others separately. Criteria for grouping together repositories may include language, level of inter-dependencies, team ownership, and others. As a distinct example, if a group of projects evolves closely together and there is high interoperability between them (for example, they use a set of common routines or data structures), it might make sense to group them in a single repository, while keeping everything else separately. If the monorepo does not grow to an endless number of projects, then traditional build tools meant for polyrepo setups could still fair well enough.

**Verdict**: If you are a very large organization, systems like Bazel and others can offer a platform for very advanced build features in a monorepo setup - assuming that the entire engineering team adopts it. Small and medium organizations, or large organizations with fragmented builds generally benefit from polyrepo setups more, due to the existing build ecosystem available as open-source or commercial-off-the-shelf (COTS). Hybrid setups could also be used as a compromise, assuming the monorepo(s) are not too large to require special build considerations.

#### A Note on Earthly

[Earthly](https://earthly.dev) supports cross-project builds for either monorepo and polyrepo layouts. It solves for some of the challenges outlined above. In fact, these challenges were the main [source of inspiration](https://earthly.dev/blog/introducing-earthly-build-automation-for-the-container-era/) when Earthly was started.

### Code Ownership

> "Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization's communication structure." — [Melvin E. Conway](https://en.wikipedia.org/wiki/Conway%27s_law)

When deciding the source code layout, some key questions that come to mind are "who is responsible for each piece of code" and "how can that be enforced".

GitHub features for managing access are far richer at the repository level - you can use [permissions](https://docs.github.com/en/github/setting-up-and-managing-organizations-and-teams/repository-permission-levels-for-an-organization) like **read**, **triage** (like read, but can also manage issues and PRs), **write**, **maintain** (like admin, but no destructive actions possible) and **admin**. In addition, you can also control a number of miscellaneous behavior independently, such as whether to allow squash commits or the specific way to enforce [branch protection](https://docs.github.com/en/github/administering-a-repository/managing-a-branch-protection-rule) (code reviews, CI passing, etc). A polyrepo setup gives each project the power to make such access decisions more independently and provides very fine-grained access controls that can be managed per-team.

If however, you would like to enforce certain rules across all teams, polyrepo setups can get in the way. Currently, the only way to enforce certain repository configurations across multiple repositories in GitHub is to use the API - so you have to develop your own in-house tooling to achieve that. Example use-cases include enforcing code reviews across the entire organization. Or enforcing squash commits.

To turn to monorepo setups, although you don't have the same level of permission granularity, GitHub provides a [CODEOWNERS](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/about-code-owners) feature. Via CODEOWNERS, you could develop different access rights for each directory. The owners of that directory get push rights, while others need to seek code reviews from the owners. A common setup is to use a branch protection rule of one code review minimum, plus the code owners (sometimes a single code owner can satisfy both of these constraints). For example, if two microservices need to be changed to add a certain feature, a cross-cutting PR would require reviews from both teams in order to allow for that feature to make it into the main branch.

If for any reason certain parts of your codebase are highly confidential, there is no way to hide a subdirectory from the rest of the team in a monorepo setup.

**Verdict**: It depends. If you would like to leave control of the engineering process enforcement to the individual teams, then polyrepo gives the most granular permission flexibility. If, on the other hand, you would like to enforce certain rules for everyone, a monorepo setup makes that the easiest.

### Issue Tracking

![Team sprint planning in front of a white board]({{site.images}}{{page.slug}}/Oalh2MojUuk.jpg)\

In a polyrepo setup, each repository gets its own issue tracking. This is often preferable so that issues related to separate projects can be tracked in independent pools. Sometimes issues need to be tracked across projects too - in such cases, you could use another repository that is only used for issue tracking and where all the higher-level issues are tracked. The challenge with this setup is often the lack of discoverability of issues. The GitHub issue search across repositories is significantly inferior to the one that can be used within a single repository. In addition, it is hard to reuse certain labels, as each repository needs to (re-)define its own set.

On the other hand, in a monorepo setup, all issues are mixed in a single pool. This can become confusing after a certain scale, at which point you would likely need a more specialized issue tracking service. If the team is not too large, however, GitHub issues in a single monorepo can help with bringing everyone together.

**Verdict**: For medium and large organizations, monorepo issue tracking does not scale well. For small organizations, monorepo issue tracking helps the team coordinate better.

### Open-Source

![People's hands placed together]({{site.images}}{{page.slug}}/fkFNBCQ6kQA.jpg)\

If your organization develops a mix of closed source and open-source code, there is absolutely no way to make a monorepo work. It is impossible to only show a subdirectory of the code to the outside world. You might think you could perhaps create a mirror of a subdirectory from the monorepo to a public repository, however, this does not go truly with the open-source spirit. How would you merge external contributions back to the main repository?

If you are hell-bent on monorepo, perhaps a hybrid approach is more appropriate for you: the open-source parts are separated in public repositories, while the closed source parts remain as part of the monorepo.

Polyrepos on the other hand, fall much more naturally in the general pattern of typical open-source. In fact, to present open-source better to the external world, it's often best if the open-sourced software itself is scattered across repositories based on the [unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy#Do_One_Thing_and_Do_It_Well): do one thing and do it well.

**Verdict**: Polyrepos are more natural for splitting open-source code from closed source code. Hybrid setups allow largely monorepo setups to open-source some components. Pure monorepo setups are incompatible with mixed open and closed source use-cases.

## Conclusion

As you can see from the multitude of concerns and use-cases that need to be addressed by the source code layout, there is no single right answer. Usually, the decision depends on a wide-ranging set of factors including engineering culture, type of software being developed, team layout, team size, software architecture, and so on.

In general, open-source and COTS tooling is far better suited for polyrepo setups. Monorepo builds, in particular, are difficult to scale and sometimes require the adoption of specialized build technology that is very alien to the rest of us.

Although the tooling to work with monorepos is more limited or sometimes more difficult to manage, it encourages cross-team collaboration as the hurdles specific to contributing across repositories and managing the dependency chain is lifted.

Hybrid setups tend to come as a compromise between the two approaches. They can be useful when a few projects present a higher level of cohesion: usually when they need to evolve together quickly and they are written in the same language. Hybrid setups can also be the answer when some parts need to be open-sourced and thus cannot be part of the main monorepo.

### My Own Take

As a bit of personal opinion, I have always aimed to optimize for cross-team collaboration in my engineering teams. Developers don't naturally gravitate towards unknown code or unknown technologies, so anything you can do to encourage close collaboration helps bridge this gap. The result can be a really agile engineering organization.

It is usually the integration of components together that is the most time-consuming, the most prone to bugs, and the cause for unexpected surprises when working in production. If everyone is left to contribute in their own little box, they will not build the right tools and processes to effectively contribute across. As Andy Grove suggests in [High Output Management](https://www.amazon.com/dp/0679762884/ref=cm_sw_em_r_mt_dp_d.4bGbH1VS8VW) to design around the [limiting factor](https://charles.io/high-output-management/) (in this case, the limiting factor being cross-team contribution), I have always gravitated towards monorepo whenever possible. However, realistically pure monorepo hasn't always been truly feasible, so for one reason or another, we always ended up with a hybrid. This is one of the reasons I started [Earthly](https://earthly.dev).

[^1]: In some extreme cases, the segmentation can be so aggressive, that you end up with micro-repos: repositories that perform specific functions. See for example this [collection of micro npm packages](https://github.com/parro-it/awesome-micro-npm-packages). There's a package for checking if an array is sorted?? Huh...

[^2]: Care must be taken, however, as even though a PR is merged as a single atomic change, the way this lands in production is never atomic. Certain considerations still apply as usual.

{% include_html cta/bottom-cta.html %}