---
title: Can We Build Better?
date: '2020-09-10 19:46:37'
toc: true
categories:
  - Tutorials
---

Have you ever had a test fail in the build but not locally? I have. Have you ever then burnt half a day pushing small changes and waiting for your build to get queued so that you could see if you had isolated the breaking change? &nbsp;Well I have, and I find the slow feedback process to be painful and I'd like to propose a solution.

## Solving Reproducible Builds

Whenever I have some failure in the build pipeline that I can't reproduce locally the culprit ends up being something environmental. &nbsp; That is there is some difference between running the test suite in Jenkins vs running in locally.

Earthly is an open-source tool designed to solve this problem. &nbsp;It's also pretty easy to use. &nbsp;You might be able to get it in place in your current build process in the time you'd normally spend tracking down problems with a flaky build.

## A Scala Example

Earthly uses Earthfiles to encapsulate your build. &nbsp;If you imagine a dockerfile mixed with a makefile you wouldn't be far off. &nbsp;

Let's walk through creating an Earthfile for a scala project:


```
├── build.sbt 
└── src/main
    ├── Main.scala
└── src/test
    ├── Test.scala </code></pre>
```

We have a main that we would like to run on startup:

``` scala
object Main extends App {
  println("Hello, World!")
}
```
<figcaption>Main.scala</figcaption>


And some unit tests we would like to run as part of the build:

``` scala
import org.scalatest.FlatSpec

class ListFlatSpec extends FlatSpec {
  "An empty List" should "have size 0" in {
    assert(List.empty.size == 0)
  }
}
```
<figcaption>Test.scala</figcaption>

There are several steps involved in the build process for this project:

1. Compiling
1. Testing
1. Containerizing

Let's encapsulate these into an Earthfile, so that I can run the exact same build process locally and eliminate any reproducibility issues.

## Setup

The first step is to create a new Earthfile and copy in our build files and dependencies: &nbsp;

``` dockerfile
FROM hseeberger/scala-sbt:11.0.6_1.3.10_2.13.1
WORKDIR /scala-example

deps:
    COPY build.sbt ./
    COPY project project
    RUN sbt update
    SAVE IMAGE
```
<figcaption>Earthfile</figcaption>

The first line is declaring the base docker image our build steps will run inside. &nbsp;All earthly builds take place within the context of a docker container. &nbsp;This is how we ensure reproducibility. &nbsp;After that, we set a working directory and declare our first target `deps` and copy our project files into the build context.

> You may have noticed the first time you build an sbt project, it takes a while to pull down all the project dependencies. &nbsp;This `deps` target is helping us avoid paying that cost every build. &nbsp; Calling `sbt update` and then `SAVE IMAGE` ensures that these steps are cached and can be used in further build steps. &nbsp;Earthly will only need to be rerun this step if our build files change.

We can test out the deps step like this:

{% include imgf src="run.gif" alt="running earthly at command line" caption="Running `earthly +deps`" %}

## Build It

Next, we create a `build` target. This is our Earthfile equivalent of `sbt compile`.

``` dockerfile
build:
    FROM +deps
    COPY src src
    RUN sbt compile
```    
<figcaption>earthfile continued</figcaption>

Inside the `build:` target we copy in our source files, and run our familiar `sbt compile`. &nbsp;We use `FROM +deps` to tell earthly that this step is dependent upon the output of our `deps` step above.

We can run the build like this:

{% include imgf src="run2.gif" alt="running earthly at command line" caption="Running `earthly +build`"%}

## Test It

We can similarly create a target for running tests:

``` dockerfile
test:
    FROM +deps
    COPY src src
    RUN sbt test</code></pre>
```
<figcaption>Earthfile continued</figcaption>

We can then run our tests like this:

{% include imgf src="run3.gif" alt="running earthly +test" caption="Running `earthly +test`" %}

## Containerize It

The final step in our build is to build a docker container, so we can send this application off to run in Kuberenetes or EKS or whatever production happens to look like.

``` dockerfile
docker:
	COPY src src
	RUN sbt assembly
	ENTRYPOINT ["java","-cp","build/bin/scala-example-assembly-1.0.jar","Main"]
 	SAVE IMAGE scala-example:latest
```
<figcaption>Earthfile continued</figcaption>

Here we are using `sbt assembly` to create a fat jar that we run as our docker container's entry point.

We can test out our docker image as follows:

{% include imgf src="run4.gif" alt="building docker image using earthly" caption="Running `earthly +docker`" %}

You can find the [full example here](https://github.com/earthly/earthly-example-scala/blob/simple/simple/earthfile). Now we can adjust our build process to call earthly and containerization ensures our builds are not effected by environmental issues either locally or on the build server. &nbsp;

## Did we solve it?

We now have our `deps`, `build`, `test` and `docker` targets in our Earthfile. All together these give us a reproducible process for running our build locally and in our CI builds. &nbsp;We used earthly to encapsulate the build steps.

{% include imgf src="diagram.png" alt="diagram of earthly usage" caption="Encapsulation build steps" %}

If a build fails in CI, we can run the same process locally and reproduce the failure. &nbsp;Reproducibility solved, in a familiar dockerfile-like syntax .

## But wait there's more 

We haven't solved all the problems of CI, however. &nbsp;What about build parallelization? &nbsp;What about caching intermediate steps? &nbsp;How about multi-language builds with complicated interdependencies? &nbsp;Earthly has some solutions for those problems as well and I'll cover them in future tutorials. &nbsp;

For now, you can find more details, such as how to install earthly and many more examples on **[github](https://github.com/earthly/earthly/blob/master/README.md). &nbsp;**

