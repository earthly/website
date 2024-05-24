---
title: Can We Build Better?
toc: true
author: Adam
internal-links:
   - scala build
   - scala builds
topic: earthly
funnel: 3
topcta: false
excerpt: |
    Learn how to solve the problem of reproducible builds with Earthly, an open-source tool that encapsulates your build process in a Docker-like syntax. With Earthly, you can eliminate the pain of slow feedback and easily reproduce build failures, ensuring that your builds are not affected by environmental issues.
last_modified_at: 2023-07-14
categories:
  - Build
---
Have you ever had a test fail in the build but not locally? I have. Have you ever then burnt half a day pushing small changes and waiting for your build to get queued so that you could see if you had isolated the breaking change? Well I have, and I find the slow feedback process to be painful and I'd like to propose a solution.

## Solving Reproducible Builds

Whenever I have some failure in the build pipeline that I can't reproduce locally the culprit ends up being something environmental. That is there is some difference between running the test suite in [Jenkins](/blog/slow-performance-in-jenkins) vs running in locally.

Earthly is an open-source tool designed to solve this problem. It's also pretty easy to use. You might be able to get it in place in your current build process in the time you'd normally spend tracking down problems with a flaky build.

## A Scala Example

Earthly uses Earthfiles to encapsulate your build. If you imagine a [dockerfile](/blog/compiling-containers-dockerfiles-llvm-and-buildkit) mixed with a Makefile you wouldn't be far off.  

Let's walk through creating an Earthfile for a Scala project:

~~~
├── build.sbt 
└── src/main
    ├── Main.scala
└── src/test
    ├── Test.scala </code></pre>
~~~

We have a main that we would like to run on startup:

~~~{.scala caption="main.scala"}
object Main extends App {
  println("Hello, World!")
}
~~~

And some unit tests we would like to run as part of the build:

~~~{.scala caption="test.scala"}
import org.scalatest.FlatSpec

class ListFlatSpec extends FlatSpec {
  "An empty List" should "have size 0" in {
    assert(List.empty.size == 0)
  }
}
~~~

There are several steps involved in the build process for this project:

1. Compiling
1. Testing
1. Containerizing

Let's encapsulate these into an Earthfile, so that I can run the exact same build process locally and eliminate any reproducibility issues.

### Setup

The first step is to create a new Earthfile and copy in our build files and dependencies:  

~~~{.dockerfile caption="Earthfile"}
FROM hseeberger/scala-sbt:11.0.6_1.3.10_2.13.1
WORKDIR /scala-example

deps:
    COPY build.sbt ./
    COPY project project
    RUN sbt update
    SAVE IMAGE
~~~

The first line is declaring the base docker image our build steps will run inside. All earthly builds take place within the context of a docker container. This is how we ensure reproducibility. After that, we set a working directory and declare our first target `deps` and copy our project files into the build context.

> You may have noticed the first time you build a `sbt` project, it takes a while to pull down all the project dependencies. This `deps` target is helping us avoid paying that cost every build.   Calling `sbt update` and then `SAVE IMAGE` ensures that these steps are cached and can be used in further build steps. Earthly will only need to be rerun this step if our build files change.

We can test out the `deps` step like this:

{% include imgf src="run.gif" alt="running earthly at command line" caption="Running `earthly +deps`" %}

### Build It

Next, we create a `build` target. This is our Earthfile equivalent of `sbt compile`.

~~~{.dockerfile caption="Earthfile"}
build:
    FROM +deps
    COPY src src
    RUN sbt compile
~~~

Inside the `build:` target we copy in our source files, and run our familiar `sbt compile`. We use `FROM +deps` to tell earthly that this step is dependent upon the output of our `deps` step above.

We can run the build like this:

{% include imgf src="run2.gif" alt="running earthly at command line" caption="Running `earthly +build`"%}

### Test It

We can similarly create a target for running tests:

~~~{.dockerfile caption="Earthfile"}
test:
    FROM +deps
    COPY src src
    RUN sbt test</code></pre>
~~~

We can then run our tests like this:

{% include imgf src="run3.gif" alt="running earthly +test" caption="Running `earthly +test`" %}

### Containerize It

The final step in our build is to build a docker container, so we can send this application off to run in Kubernetes or EKS or whatever production happens to look like.

~~~{.dockerfile caption="Earthfile"}
docker:
 COPY src src
 RUN sbt assembly
 ENTRYPOINT ["java","-cp","build/bin/scala-example-assembly-1.0.jar","Main"]
  SAVE IMAGE scala-example:latest
~~~

Here we are using `sbt assembly` to create a fat jar that we run as our docker container's entry point.

We can test out our docker image as follows:

{% include imgf src="run4.gif" alt="building docker image using earthly" caption="Running `earthly +docker`" %}

You can find the [full example on GitHub](https://github.com/earthly/earthly-example-scala/blob/simple/simple/earthfile). Now we can adjust our build process to call earthly and containerization ensures our builds are not effected by environmental issues either locally or on the build server.  

### Did We Solve It?

We now have our `deps`, `build`, `test` and `docker` targets in our Earthfile. All together these give us a reproducible process for running our build locally and in our [CI](/blog/continuous-integration)  builds. We used earthly to encapsulate the build steps.

{% include imgf src="diagram.png" alt="diagram of earthly usage" caption="Encapsulating the Build Steps" %}

If a build fails in CI, we can run the same process locally and reproduce the failure. Reproducibility solved, in a familiar dockerfile-like syntax .

## But Wait There's More

We haven't solved all the problems of CI, however. What about build parallelization? What about caching intermediate steps? How about multi-language builds with complicated interdependencies? Earthly has some solutions for those problems as well and I'll cover them in future tutorials.

For now, you can find more details, such as how to install earthly and many more examples on **[Earthly's getting started page](https://cloud.earthly.dev/login)**.

{% include_html cta/bottom-cta.html %}
