---
title: "What makes Earthly fast"
categories:
  - Articles
toc: true
author: Vlad

internal-links:
 - how is earthly fast
 - what makes earthly fast
 - earthly is fast
 - earthly performing fast
last_modified_at: 2023-10-20
excerpt: |
    Earthly makes CI/CD builds faster by reusing computation from previous runs for unchanged parts of the build. It is particularly effective in speeding up CI builds that involve redundant tasks, monorepos, and polyrepos, while also improving local builds in certain circumstances.
---
<!--sgpt-->**Check out [Earthly](https://earthly.dev/). We simplify and speed up software builds using containerization. Ideal for those who value quick, open-source tools for continuous integration. [Give us a try](/).**

Earthly makes CI/CD builds faster by reusing computation from previous runs for parts of the build that have not changed. This can be a game changer in terms of developer productivity gained.

Think about your typical CI/CD pipeline. You generally rely on it to run some tests for you, but until it gets to actually doing that, the following has to happen:

* You git commit and push some new changes to GitHub/Gitlab
* You wait for the CI to kick in
* The CI boots up a fresh new instance of the runner
* The CI downloads and installs some OS dependencies
* The CI pulls some container images
* The CI compiles dependencies (if needed)
* The CI compiles the main code
* The CI executes the tests

Only the last two steps described above are actually affected by the changes of the code, and yet the process repeats all the other steps on every run. This is a relatively simple example. When you think about real-world complex CI/CD pipelines, with many project interdependencies, or when you look at the CI builds of monorepos, it gets much more inefficient. Earthly addresses this problem and more.

In this article I'll walk through the types of situations in which Earthly is faster and also the ones it isn't, and I'll also talk about exactly how we achieve this.

## In What Situations is Earthly Faster?

The word "build" can mean many things across many different contexts. When we say that it makes builds faster, we generally mean CI/CD builds.

Here are contexts in which Earthly does a particularly good job in:

* Making CI builds faster, especially in these circumstances
  * The CI performs many redundant tasks upfront, like installing dependencies and pulling container images.
  * The CI is a sandboxed CI, where no state is transferred over from one run to the next without explicitly uploading / downloading on each run (e.g. GitHub Actions, Circle CI)
  * Monorepos and Polyrepos: The CI builds multiple interconnected projects or sub-projects at a time
* Making local builds faster, especially in these circumstances
  * The build being executed is the CI build itself (and not just of the component you're working on)
  * The build is complex, involving multiple projects or sub-projects at a time, possibly using multiple programming languages, where some of the projects could be rebuilt with a lot of cache shared with the CI or with teammates
  * Your internet connection is slow, and you need to perform a lot of image pushes and/or pulls

Here are examples where Earthly doesn't improve performance:

* Local builds, when you're iterating in a tight loop in a single programming language. Usually the tools of that programming language are already highly optimized for this use-case and often work better natively.
* CI builds, when the environment is shared between runs (unsafe), and you're building programming languages with good built-in caching.
* CI builds, when the redundant parts of the build, like installing dependencies, are cached, AND the CI setup preserves the cache well, WITHOUT the need for downloading or uploading.
* CI builds that involve working with large files (i.e. >1 GB files), due to some internal transferring of files that Earthly relies on.

Now all this might be too complicated to remember, so here's a simplified version.

Earthly is:

* Almost always faster in CI, and especially faster in sandboxed CI environments.
* Usually not faster for local builds where you're iterating in a single programming language in a tight loop.
* Often faster locally, when intending to run the same build as the CI.

## How Earthly Works

![How]({{site.images}}{{page.slug}}/how.png)\

Earthly makes things fast using a combination of techniques:

* Holistic layer caching
* Build graphs
* Well-known dependencies
* Automatic parallelization
* Instantly available cache provided via remote runners (Earthly Satellites)
* Other features to further optimize execution

### Holistic Layer Caching

If you've used Dockerfiles before, you're probably already familiar with how layer caching works. Earthly takes that idea and expands its use cases such that it doesn't just apply to container images, but it also applies to building artifacts (regular files, generated source code, binaries, libraries etc) and executing tests (unit tests, linting, integration tests etc). This allows vastly wider use of the caching benefits in your builds.

If you're unfamiliar with Dockerfile layer caching, you can think of it like a layered cake where you can reuse layers of the cake in future cakes (or future runs of the build), if the ingredients of that layer haven't changed. This mechanism allows Docker image builds to reuse work from previous runs, thus speeding up the build process. Earthly takes this same idea to the next level, by making it applicable to the entire build, and not just to the builds of container images.

### Build Graphs

Once layer caching can be used throughout the entire build, we're no longer limited to relatively simple build structures like we're used to in most Dockerfile builds. The structure of the build can become a graph, and it can get as complex as necessary.

For example, you might generate some protobuf definitions then reuse that generated code across multiple packages, possibly compile some common libraries, and a number of microservices, and then finally put together an integration test with those microservices working together. This can become complex and interconnected. And yet the layer caching algorithm allows us to reuse everything that has not changed - hence we're not going to recompile all those dependencies unless something changed in them, or if perhaps a common component has changed (like the protobuf definition).

Although these types of graphs are also available when building just images, because of the focused applicability of Dockerfiles, the ability to use layer caching at this scale is never achieved.

### Well-Known Dependencies

In a complex build graph, if you understand what has changed, and the build's internal dependencies with high precision, then you can infer what to rebuild and, crucially, what not to rebuild.

Compared to a Bash script, or to the YAML of a CI system, Earthly has the unique advantage that it understands dependencies well. Similar to how a Dockerfile understands which layer uses which source files, thanks to the COPY operations, Earthly takes that same idea to the next level via the build graph. Besides understanding which source file is used in each build target, it also understands how the build targets depend on each other.

This is particularly helpful when you have complex interdependencies between projects or subprojects. Earthly deals with these really well - whether they are across a single monorepo, or across multiple code repositories. Earthly is Git SHA-aware, and uses additional various hashing algorithms to determine whether a target has new inputs or not.

This is how Earthly can determine that it only needs to rebuild that one microservice you're working on, and not the other 6 components that are part of a complex build, but finally re-run the entire integration test that everything feeds into.

### Automatic Parallelization

Earthly has a few key advantages that allow for automatic inference of parallelism.

* Every target in Earthly has clear, explicit interdependencies. Nothing is implicit, hidden, or environment-dependent.
* Earthly is able to understand complex build graphs - particularly when the graph fans-out across multiple independent targets, and when a graph fans-in such that a single target depends on multiple previous results.
* All operations are isolated thanks to the containerization, so there are no surprises.

With these restrictions in place, Earthly is able to automatically infer what may run in parallel and what may not. If no direct relation exists between two operations, and they are ready to be executed, Earthly will simply run them at the same time.

Although this happens on a single machine only today, future versions of Earthly will permit executing these across compute clusters for added speed and scalability. We believe that this clustered version will yield another order of magnitude speed improvement for large enough builds.

### Instantly Available Cache

The caching techniques above would be for nothing, if Earthly did not have a way to pass on the stored cache between CI runs with high efficiency.

In typical sandboxed CI/CD systems, you might be familiar with cache directories that you can upload at the end of the build, and then restore in the next run by downloading back those contents. The problem with this approach is that in most cases, due to the additional upload/download time added to the build, the CI can end up being slower with the cache than without it.

Some sandboxed CI systems support Dockerfile layer caching, but because the execution rotates between different machines (and thus different caches), it is not guaranteed that you'll actually end up with a machine that actually has the cache you need. The hit rate is very inconsistent. Plus, again, Dockerfile layer caching only applies to the builds of container images, missing out on all the other operations that take place in CI.

There is no efficient way to pass along cache from one run to the next in a sandboxed CI. For this reason, Earthly is able to use remote execution via Earthly Satellites. Satellites are remote runners managed by Earthly that are connected to an instantly available cache storage.

Although not immediately intuitive, the main reason to use Earthly Satellites to speed up builds is not because the CPU, memory, or network might be faster. It is because the cache is there instantly, with no need for a download and an upload. And because of the way Earthly works, it is also very rich, yielding a high hit rate for the parts of the build that change rarely.

In addition, because Satellite builds can be triggered from both the CI and your laptop just as easily as running a local build, it allows for a very quick way to verify that your CI build works fine straight from your development machine, without having to commit any code to GitHub. It will also allow you to reuse cache with the CI and with other colleagues on the team.

### Other Features to Further Optimize Execution

Besides the strategies described above, Earthly also has a number of additional features that allow for further tuning of performance in specific circumstances: cache mounts, auto-skip (coming soon), and remote caching.

**Cache mounts** are directories you can mount in specific places within your build to reuse files across different runs. This is useful when the layer caching paradigm doesn't quite capture the level of granularity that you need. You might use cache mounts for programming-language-specific caching, like the `.m2` directory in Java, the Rust compilation cache, or the `GOCACHE` directory in Go.

An upcoming feature of Earthly is **auto-skip**. This feature short circuits large parts of an Earthly build if the source files changed do not impact the result of the build in any way. While this is somewhat similar to the graph-based layer caching described above, it differs from that in a few ways:

* Determining whether a build needs to execute can be done without the need of an Earthly Satellite, thus allowing to save time to wake up the satellite (if needed) and saving compute expenses.
* Analyzing the layer cache contents can be time-consuming for very large builds. Auto-skip is based on a more focused and centralized database of input hashes (hashes of all the files involved in a build).
* Certain deployment operations ignore layer caching altogether. Auto-skip still applies to them, however. So, for example, if you are producing the same container image for the purpose of pushing it to production, there is no need to redeploy it if nothing has changed.

Another feature is **remote caching**. This feature allows you to store Earthly cache in a container registry, such as DockerHub, AWS ECR, GCP AR, or GitHub Container Registry. While this gives you cheap caching, it does have the drawback that it requires uploading and downloading of the contents. It is slightly smarter than a traditional CI cache directory, however, in that it only uploads layers that are different, and it only downloads layers that will actually be used. For the fastest experience, Earthly Satellites outperforms remote caching by a wide margin.

## How Fast Is Fast?

![Fast]({{site.images}}{{page.slug}}/fast.png)\

We generally say that Earthly can get **up to** 2-20X faster compared to not using Earthly. These are the typical ranges that we hear from our customers. The reason this range is so wide is because it is highly dependent on the setup. It is difficult to come up with a single real-world benchmark that is fair toward the very high diversity of tools and languages that Earthly is being used with. In some cases, we even go way beyond 20X, if you compare an emulated cross-platform build vs a native build. We don't typically factor in emulation slowness as we don't think it is a fair comparison.

While possible, it is rare that we hear Earthly not speeding up builds at least by 2X. In situations where Earthly is not a great fit - as highlighted above - the builds could also be slower. In our experience, these tend to be niche use-cases.

The other thing to note is that the comparison is for entire CI runs, not just for a small portion of a run. While other tools might report X times faster Docker builds, or X times faster JS script builds, and so on it is important to understand that speedup is for a smaller portion of the entire CI build, and thus it might not be quite so impactful when looking at the entire pipeline. In our material, we always compare the entire CI/CD pipeline speedup.

## The ROI of Fast

![ROI]({{site.images}}{{page.slug}}/roi.png)\

Fast is great, but is it useful?

Many people often think of CI efficiency as an exercise in infrastructure cost optimization. While Earthly can indeed save you significant infrastructure money, by reducing your CI bill at scale (even if having to pay some of the savings on Earthly Satellite infrastructure), I would consider this as a short-sighted measure of Earthly's true impact.

The most important component of Earthly's return-on-investment (ROI) is the developer time saved. When engineers can get fast feedback on CI failure or success, it saves precious engineering time that compounds across the repeated nature of the CI activity and the number of people on the team benefiting from the time saved.

Besides the developer time saved, imagine what fast feedback cycles does to the general velocity of feature delivery for your team. How you can ship faster, in tighter feedback loops with your customers (internal or external), and what that does to the bottom line of your business. This part is harder to quantify, so I'm not going to try to.

I wrote an entire article about the [ROI of fast builds](https://earthly.dev/blog/the-roi-of-fast/), if you want to read more.

## Conclusion

The reason I started writing this article is because many people we were talking to couldn't believe that Earthly could actually speed up builds that much and they thought it's just marketing fluff. Perhaps I would also think that, not knowing how that might even be possible.

Earthly addresses many of the inefficiencies found in traditional CI/CD pipelines. By leveraging techniques such as holistic layer caching, build graphs, and Earthly Satellites, it offers a more streamlined and efficient build process that rebuilds on what has actually changed. The results often show build times reduced by factors ranging from 2 to 20X. Beyond the obvious benefits of reduced infrastructure costs and faster feedback loops, our approach leads to improved developer productivity that you can measure. We operate in a developer landscape where efficiency and time are crucial. It's time we rethink how CI/CD should work and allow developers to focus more on coding and less on waiting.

{% include_html cta/bottom-cta.html %}
