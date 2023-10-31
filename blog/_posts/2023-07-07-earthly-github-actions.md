---
title: "Better Together - Earthly + Github Actions"
categories:
  - Articles
toc: true
author: Evan Pease
topic: earthly
funnel: 3
internal-links:
 - Earthly
 - Github Actions
 - Github
excerpt: |
    Learn how Earthly and Github Actions can work together to improve your Continuous Integration (CI) process. Discover the benefits of Earthly's local CI pipeline execution, simplicity in writing Earthfiles, and support for monorepos. See how Earthly can significantly speed up your builds and enhance developer productivity.
last_modified_at: 2023-08-23
---
## Introduction

I joined Earthly at the beginning of 2023. I lead solution architecture. One of my primary roles is helping potential customers figure out how they can best leverage Earthly. That often requires building demonstrations that show how developers might use Earthly in their projects. So when I first started at Earthly, I set out to build a project that I could use to highlight Earthly's strengths as a Continuous Integration (CI) solution. Namely that it enables consistent, repeatable builds, is simple to work with, is fast, and works great with monorepos. I wanted the project to be a resource I could use to help explain Earthly to someone brand new to it. At the same time I was having a lot of conversations with developers in and outside of the Earthly community and it seemed that many of them were using Github Actions to run at least some part of their build process. So, I thought it would be a good exercise to set up my test project with Github Actions as well as with Earthly to see how the two compare. I ended up learning a lot about how they performed when it came to build consistency, developer experience, and monorepo support. I've used Github Actions a lot over the past few years and so have many Earthly users. There are some things that I really love about Github Actions. For one, it has a generous free tier and is tightly integrated with Github (obviously). This makes it an obvious choice when starting out if you're already pushing code to Github. But it definitely has many limitations especially as your builds grow in size and complexity. It's not a problem unique to Github Actions by a long shot. Finding the solution is [why Earthly exists](https://earthly.dev/blog/new-fundings-at-earthly/) in the first place.

## What We Are Building

For the project, I chose to build an application using a polyglot monorepo layout. This is one of the more challenging types of repo layouts for traditional CI systems to handle (more on this later) so it seemed like a good way to put the capabilities of Earthly and Github Actions to the test. You can see what I ended up building by checking out the [earthly-vs-gha repository on Github](https://github.com/earthly/earthly-vs-gha/). The application itself is not very complicated. It is just 4 REST services returning a random quote to 1 React front-end. Developing the build for this, however, is far more complex. There's 4 separate run times (Go, Node, Python, and Rust) which also means 4 separate build tools and a lot of dependencies. There's also a dependency that's shared by all 4 of the backend services.

Obviously an application with 4 separate backends that do the same thing is not very practical. But the pattern does mirror many of the challenges that larger, multi-team projects encounter with monorepos and polyrepos.

<div class="wide">
![diagram]({{site.images}}{{page.slug}}/diagram.png)\
</div>

- Project root/
- Go_server/ (Go server package)
- Node_server/ (Node.js server package)
- Python_server/ (Python server package)
- Rust_server/ (Rust server package)
- Quote_client/ (React front-end package)
- Quote_generator/ (Generates a text file of quotes used by the servers)

And here is what the front-end looks like with everything running:

<div class="wide">
![app]({{site.images}}{{page.slug}}/app.png)\
</div>

Let's take a look at the project the following lenses: build consistency, simplicity, Monorepo support, and speed.

## Build Consistency

### **Github Actions**

### Push, Wait, Iterate

One of the main pain points with CI systems is the speed of iteration. With Github Actions, for example, you don't know if your workflows work until you push your code to your repository. Once pushed, you have to wait for the runner to start, the code to clone, the dependencies to install, and the plugins to load. This can take seconds to minutes, depending on your project, and the problem can scale with the size and complexity of your codebase. And if something doesn't work, you need to sift through logs in your web browser to see what went wrong (note: it is possible to retrieve logs with the gh CLI tool but you still need to check the web UI for the job ID).

This is where the real pain of traditional CI workflows lies, as it slows down the speed of iteration. I have several pages of this in my Github actions history from when I started working on porting my CI pipeline to Github Actions for this article:

<div class="wide">
![gha-builds]({{site.images}}{{page.slug}}/gha-builds.png)\
</div>

We've all run into this before, at least to some degree, regardless of the CI system. And that's ok! Especially when you're learning something new or refactoring your pipeline. What's not ok though, is the delay and friction in between iterations. This is a real drag on developer productivity.

### Is This Thing Even On?

Another problem I ran into with Github Actions (and one we hear repeatedly from customers) is the inconsistency of caching behavior. In order to get the best performance out of my workflow, I implemented caching everywhere I could by using the official [cache](https://github.com/actions/cache) plugin and the official Docker [build-push-action](https://github.com/docker/build-push-action) with caching. Occasionally I ran into timeout errors on builds that should have been fully cached. In this particular case I had to wait 7 minutes to find out. I'll touch on caching again later in the article.

<div class="wide">
![node-timeout]({{site.images}}{{page.slug}}/node-timeout.png)\
</div>

When it works, it can complete the build in as low as 2 minutes but it varies wildly between 2 and 8 minutes as of this writing.

### **Earthly**

Earthly approaches this problem differently by allowing you to run your CI pipeline locally. You don't have to commit a change to your repo. Once you know it works locally, you can take it to your CI and have a high degree of confidence that it will work there or anywhere Earthly can be installed (including another developer's machine!) . Also, because of Earthly's layer-based caching, only the parts of your build that actually need to run are run (more on this later). This means that there is far less waiting in between iterations, and you don't have to leave your IDE or terminal to build, test, and debug CI pipelines.

For my project, I trigger the pipeline from the project's root directory with the Earthly CLI in my terminal:

`earthly +main-pipeline`

This is especially useful when working on a monorepo because I'm often only working in one package (sub-directory) at a time. I can still run the main-pipeline from my root directory and I don't have to worry about wasted code execution rebuilding the parts that I didn't touch. The Earthly logs show me explicitly what parts of the build are cached:

<div class="wide">
![earthly-cached]({{site.images}}{{page.slug}}/earthly-cached.png)\
</div>

In larger teams, a developer may only work within one package or subdirectory for long periods of time. Having the ability to quickly test the entire pipeline locally before pushing code reduces the risk of introducing changes that break CI or other team member's builds - further improving productivity.

### Simplicity

### **Github Actions**

For this project the CI pipeline needs to do 4 things for each package in the monorepo: 1) build the code, 2) run the unit tests, 3) containerize, and 4) push each container to Docker Hub. For Github Actions, this meant writing Dockerfiles for each package and one rather long YAML file to orchestrate everything. In total, that meant writing 160 lines of YAML and 86 lines of Dockerfile. Don't get me wrong, I love YAML for many things, but it does not feel like the best tool for this kind of task (see "[On YAML Discussions](https://earthly.dev/blog/on-yaml-discussions/)").

Also, Github Actions relies on plugins for certain tasks like setting up runtimes or caching. Depending on the plugin, there can be quite a few nuances that you have to learn and consider. The caching plugin, for example, requires you to specify which directories should be cached and how they should be keyed for cache hits. If you configure either of these incorrectly, there may be nothing in the logs that will tell you. For example, here I have the caching plugin configured for the Rust server with **a directory that does not exist**:

~~~{.yaml caption="ci-actions-only.yml"}
    - uses: actions/cache@v2
        with:
          path: |
            ~/.cargo/registry
            ~/.cargo/git
            ~/.you/dont/exist
            examples/polyglot-repo/rust_server/target
          key: ${{ runner.os }}-cargo-{% raw %}${{ hashFiles('**/Cargo.lock') }}{% endraw %}
~~~

Not only does the build still work, **it provides no feedback** that the caching may not be set up properly.

These are details that Earthly figures out automatically or simplifies dramatically depending on the caching behavior that you want. Some Github Actions plugins are quite useful and powerful. But they do make things a little less simple, and again the problem can scale with the size and complexity of your codebase.

### **Earthly**

With Earthly, I only have to worry about writing Earthfiles - no YAML or Dockerfiles. This means less code to write overall (if you count YAML as code). My Earthfiles do more than just my CI pipeline, and the total is **100 lines less** than my Github Actions pipeline (YAML and Dockerfiles).

For the sake of conciseness, here is the code required to orchestrate the steps for the Node service only in Github Actions on the left column and Earthly on the right column. For Github Actions, I had to write the YAML workflow and a Dockerfile. For Earthly, it's just a single, concise Earthfile and that orchestrates all of the steps I need (including building the Docker image) with extremely efficient caching.

<table>
  <tr>
    <th>GHA YAML</th>
    <th>EARTHLY CODE</th>
  </tr>
  <tr>
    <td>~~~{.yaml}
# Node service snipped from GHA yaml
  node_service_build:
    environment: "Actions Demo"
    runs-on: ubuntu-latest
    steps:
      - name: Set up QEMU
        uses: docker/setup-qemu-action@v2
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      - uses: actions/checkout@v3
      - name: Copy shared dependency
        working-directory: node_server
        run: cp ../quote_generator/in.txt quotes.txt
      - uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - uses: docker/build-push-action@v4
        with:
          context: "node_server"
          push: true
          tags: ezeev/earthly-node-example:gh-actions-only
          cache-from: type=gha
          cache-to: type=gha
      - uses: actions/cache@v2
        with:
          path: node_server/node_modules
          key: ${{ runner.os }}-node-{% raw %}${{ hashFiles('**/package-lock.json') }}{% endraw %}
      - uses: actions/setup-node@v3
        with:
          node-version: "19.x"
      - name: Node Service Build
        working-directory: node_server
        run: npm install
      - name: Node Service Test
        working-directory: node_server
        run: npm test
+
~~~
~~~{.dockerfile caption=""}
# Dockerfile for node service
FROM node:19-alpine3.16

WORKDIR /app
COPY package.json ./
COPY src/ ./src
RUN npm install
COPY quotes.txt ./quotes.txt
EXPOSE 8003
ENTRYPOINT [ "node", "src/index.js" ]

~~~

</td>
<td>~~~{.dockerfile caption=""}
# Node service Earthfile

VERSION 0.7
FROM node:19-alpine3.16
WORKDIR /node-server

deps:
  COPY package.json ./ 
  RUN npm install

build:
  FROM +deps 
  COPY src src 
  # Overwrite quotes
  COPY ../quote_generator+artifact/quotes.txt quotes.txt

test:
  FROM +build
  RUN npm test

docker:
  ARG --required tag
  FROM +build 
  EXPOSE 8003 
  ENTRYPOINT ["node", "src/index.js"]
  SAVE IMAGE --push ezeev/earthly-node-example:$tag

~~~

</td>
  </tr>
</table>

While there is a learning curve to Earthly's language, the syntax is very similar to Dockerfile and Makefile which were very familiar to me and easy to learn. And the few unique primitives that Earthly's language has, while simple and intuitive on the surface, are extremely powerful when put into practice. It allows you to compose your pipelines in a way that feels much more elegant than YAML.

Another way to frame "simplicity" is to say it reduces complexity. I think one of the best ways to demonstrate this is to take a look at how Earthly works with monorepos.

## Monorepo Support

### **Github Actions**

Monorepos have historically been a challenge for CI systems for a variety of reasons. The main one being that they simply were not designed for the extra layer of complexity that goes with them. Github Actions has added some features that attempt to help with some monorepo-related challenges. The [workflow-syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpaths) supports concurrency and enables developers to watch for changes in specific paths during builds. It supports [reusing workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows), which if you can use it, may reduce the total amount of YAML that you need to write and maintain.

While these features can help to some extent, they add more complexity and don't solve the underlying problems. This is why many users end up writing their own scripts or finding other solutions (like Earthly) for building their monorepos.

### **Earthly**

In contrast, Earthly was designed with monorepos in mind. You obviously don't need to have one to see the benefits, but when you do it becomes clear quite quickly. For my project, I have an Earthfile in the root directory of each package. Each package's build logic is self-contained and local to the code that is actually being built.

But, I mentioned in the beginning of this article that there is a shared dependency (as is usually the case in monorepos). At build time, I need to make sure the quotes text file (quotes.txt) is generated and copied into the builds for each of my servers. I can do that with this line:

~~~{.bash caption=">_"}
COPY ../quote_generator+build/quotes.txt quotes.txt
~~~

Each of the server's Earthfiles have this line. This single line of code is doing much more than just copying a file from another subdirectory. It is executing a build from a different directory and then copying an artifact from that build into the current target. It doesn't look like much but this is a major part of the magic that makes Earthly great at handling monorepos. And if the `+build` target in `../quote_generator` was already run - this line will only be copying a cached file.

In this case, I'm using the relative path of the dependency that needs to be built within the monorepo - but I could also use a path to another Github repository or branch (in a polyrepo scenario). Earthly handles either automatically. This ability to reference targets in other Earthfiles, whether local or remote is what makes Earthly great for composing pipelines for both monorepos and polyrepos.

In the root directory of the monorepo I have the "main" Earthfile where the `+main-pipeline` I referenced earlier is defined. `+main-pipeline` is once again referencing other targets - this time targets from the same Earthfile, which are then referencing the targets of specific packages. All build logic is local to its respective package with the root Earthfile orchestrating the monorepo build. The `BUILD` commands are executed in parallel. This approach allows you to layout your build logic in a way that matches the layout of your repository and Earthly automatically figures out what is cached, what needs to be run and the order of execution.

~~~{.dockerfile caption=""}
main-pipeline:
  BUILD +all-test
  ARG tag=ci-demo
  BUILD +all-build --base_url=http://localhost
  BUILD +all-docker --tag=$tag --base_url=http://localhost

all-test:
  BUILD ./rust_server/+test
  BUILD ./go_server/+test
  BUILD ./python_server/+test
  BUILD ./node_server/+test
  BUILD ./quote_client/+test

all-build:
  ARG base_url=http://localhost
  BUILD ./quote_client/+build --base_url=$base_url
  BUILD ./rust_server/+build
  BUILD ./go_server/+build
  BUILD ./node_server/+build
  BUILD ./python_server/+build
  
all-docker:
  ARG --required tag
  ARG base_url=http://localhost
  BUILD ./quote_client/+docker --tag=$tag --base_url=$base_url
  BUILD ./rust_server/+docker --tag=$tag
  BUILD ./go_server/+docker --tag=$tag
  BUILD ./python_server/+docker --tag=$tag 
  BUILD ./node_server/+docker --tag=$tag
~~~

### Speed

### **Github Actions**

Build speed is one of the less subjective dimensions to look at for this comparison. In my tests, for this project, I was able to get builds to complete in about 2 minutes and 15 seconds on Github Actions with caching and concurrency fully configured. Although times fluctuate wildly between as low as 1 minute and 30 seconds to 6 minutes for identical builds. And as mentioned early, occasionally Github Action's Docker caching times-out and fails the build at around 6 minutes.

Developer speed is also an important dimension to consider. As I mentioned earlier in this article, the lag time in between iterations is a drag on developer productivity. And it just takes more lines of YAML to do what Earthly can do in fewer lines. YAML is a very easy language to write in. But there is definitely a learning curve to mastering Github Actions and the nuances of its various plugins. Especially when applied to a more complex pattern like a monorepo.

### **Earthly**

With Earthly, executing the same pipeline locally completes in 7 seconds consistently. With [Earthly Satellites](https://earthly.dev/earthly-satellites) (our managed remote build runners), it also completes in 7 seconds. This is another data point that speaks to the reproducibility and consistency that Earthly offers.

<div class="wide">
![7-secs]({{site.images}}{{page.slug}}/7-secs.png)\
</div>

When it comes to developer speed. There really is no comparison. Composing my CI pipeline in Earthly felt natural and elegant compared to writing it out in YAML. If you've ever written Dockerfiles or Makefiles, Earthly's language is easy to learn. And the ability to run my pipeline locally before shipping to CI meant that I was able to iterate really fast and not make a bunch of commits to test my CI pipelines.

### Better Together: Earthly + Github Actions

Because you can use Earthly pretty much anywhere where the Earthly CLI can be installed, there are quite a few Earthly users running [Earthly on Github Actions](https://docs.earthly.dev/ci-integration/vendor-specific-guides/gh-actions-integration). This is a very convenient option for anyone who wants the best of both worlds. You can also use [Earthly Satellites](https://earthly.dev/earthly-satellites) – our managed remote build runners – and self-hosted [remote runners](https://docs.earthly.dev/docs/remote-runners#how-remote-runners-work) with GitHub Actions. Both of these options let you run Earthly commands from your local machine or Github Actions but actually have the execution take place on a remote server dedicated to your organization. This also gives your team the added benefit of a shared cache they can use locally as well. This pattern has become popular as Github Actions users run into challenges with Github's free runners or want to reduce costs for paid Github Actions.

As part of this project I also created a Github Actions workflow that uses an Earthly Satellite. Below you can see a comparison of the performance. Using a Satellite cuts the build time by more than half (conservatively) and the performance is extremely consistent relative to building with Github Actions only. Because the cache on Earthly Satellites is local to the runner, it is instantly available (no upload/download is necessary).

The other major benefit is that using Earthly in any form with GitHub Actions greatly reduces the complexity and amount of YAML needed in the Github Actions workflow. You can see it on [GitHub](https://github.com/earthly/earthly-vs-gha/blob/main/.github/workflows/ci-satellites.yml).

<div class="wide">
![side-by-side]({{site.images}}{{page.slug}}/side-by-side.png)\
</div>

### Building and Running the Project

If you're interested in running this build yourself - you can find everything at the [earthly-vs-gha repository on Github](https://github.com/earthly/earthly-vs-gha/). The readme includes instructions on how to run it locally as well as on Github Actions. Please note that this project may evolve over time as Earthly and Github Actions release new features and updates or we see opportunities to make improvements.

### Next Steps

Thank you for taking the time to read our article about Github Actions and Earthly. If you're interested in learning more, please [schedule](https://calendly.com/d/y22-s9m-cqn/earthly-demo) a demo or conversation with us. Or, skip the call and try [Earthly Satellites](https://earthly.dev/earthly-satellites). They are remote build runners that make builds fast with an automatic and instantly available build cache. Builds can be triggered by GitHub Actions (or any CI) as well as from your laptop. And they're super simple to use. Get started by following [the steps in our documentation to self-serve Satellites](https://docs.earthly.dev/earthly-cloud/satellites).

{% include_html cta/bottom-cta.html %}
