---
title: Frequently Asked Questions
layout: page
---
<!-- vale HouseStyle.H2 = NO -->
<style>
span.hide {
    display: none;
    white-space:nowrap;
    width: max-content;
}
    
h2:hover span {
    display: inline-block;
}
</style>

<h2 id="dockerfile">How is Earthly different from Dockerfiles?<span class="hide"><a href="#dockerfile">¶</a></span></h2>

[Dockerfiles](https://docs.docker.com/engine/reference/builder/) were designed for specifying the make-up of Docker images and that's where Dockerfiles stop. Earthly takes some key principles of Dockerfiles (like layer caching), but expands on the use-cases. For example, Earthly can output regular artifacts, run unit and integration tests, and create several Docker images at a time - all outside the scope of Dockerfiles.

Earthly introduces a richer target, artifact, and image [referencing system](https://docs.earthly.dev/guides/target-ref), allowing for better reuse in complex builds spanning a single large repository or multiple repositories. Because Dockerfiles are only meant to describe one image at a time, such features are outside the scope of applicability of Dockerfiles.

<h2 id="usedocker">Why not just use docker and bash/make/python/ruby/etc?<span class="hide"><a href="#usedocker">¶</a></span></h2>

Sure, you can do that. That's how earthly started.

Earthly grew out of a wrapper around Dockerfiles. As your project grows, your build and testing requirements will grow too. You might end up with multiple Dockerfiles, you might need to support running tests and builds on both Linux, MacOS, and Windows, you might run into parallelisation issues, you might need to scale across multiple repositories. Earthly grew out of all of these requirements and is supported by a growing user-base, which (most likely) offers a more battle-tested code-base than your custom in-house wrapper.

Still think you should just write your own wrapper? We have some tips on our [blog](https://earthly.dev/blog/repeatable-builds-every-time/).

<h2 id="multistage">Is Earthly a way to define a Docker multi-stage build?<span class="hide"><a href="#multistage">¶</a></span></h2>

Yes, that is one of its uses.  

Docker Multi-stage builds can get complex and hard to follow as they accumulate steps. The target syntax of earthly is easier to understand.

However Earthly is not only a tool for producing docker containers. Earthly is a tool for building cross platform build specifications. It can produce docker images but it can also be used to produce binary artifacts, to run tests, to lint code, and anything else you would normally do inside of build pipeline in Jenkins, GitHub Actions, Travis CI or your-continous-integration-system-of-choice.

<h2 id="ci">Can I use Earthly with my continuous integration system?<span class="hide"><a href="#ci">¶</a></span></h2>

Yes, if you install Earthly where your builds run, then you can use Earthly with your continuous integration system. We have documented integrations for some [popular CI systems](https://docs.earthly.dev/docs/ci-integration) but it is likely that you will be able to get earthly working with your existing CI System. Hop in our [Slack channel](/slack) and you may find others using your CI system of choice.  

<h2 id="pl">Can I use Earthly with my programming language or command line build tools?<span class="hide"><a href="#pl">¶</a></span></h2>

Yes. If it's possible to create a docker image with your programming language, compiler, and tools of choice installed then its possible to use these with Earthly.

Earthly is especially popular with those who need to work with several languages or tools in a single build pipeline. Earthly can act as a glue layer that holds the various tools together and provides caching and parallelism across them. 

<h2 id="build">Can Earthly build Dockerfiles?<span class="hide"><a href="#build">¶</a></span></h2>

Yes! You can use the command `FROM DOCKERFILE` to inherit the commands in an existing Dockerfile.

```
build:
  FROM DOCKERFILE .
  SAVE IMAGE some-image:latest
```

You may also optionally port your Dockerfiles to Earthly entirely. Translating Dockerfiles to Earthfiles is usually a matter of copy-pasting and making minor adjustments. See the [getting started page](/get-earthly) for some Earthfile examples.

<h2 id="nix">How does Earthly compare to Nix?<span class="hide"><a href="#nix">¶</a></span></h2>

Both [Nix](https://nixos.org/) and Earthly are focusing on improving the way that software is built but we believe they have different goals. 

At a technical level, both Nix and Earthly use Linux namespaces to provide file system isolation. Earthly uses namespaces via Runc, using BuildKit whereas Nix uses them directly. 

At a higher level, though, Earthly is focused on providing an easy to write language for declaring all the steps of a complex build pipeline. This often includes things that may not be a good fix of the Nix build model, such as code linting, starting up and tearing down dependent services, making network calls and running integration tests. 

<h2 id="bazel">How is Earthly different from Bazel?<span class="hide"><a href="#bazel">¶</a></span></h2>

[Bazel](https://bazel.build) is a build tool developed by Google to optimize the speed, correctness, and reproducibility of their internal monorepo codebase. Earthly draws inspiration from some of the principles of Bazel (mainly the idea of repeatable builds), but it is different in a few key ways:

* Earthly does not replace language-specific tools, like Maven, Gradle, Webpack, etc. Instead, it leverages and integrates with them. Adopting Bazel usually means that all build files need to be completely rewritten. This is not the case with Earthly, as it mainly acts as the glue between builds.
* The learning curve of Earthly is more accessible, especially if the user already has experience with Dockerfiles. Bazel, on the other hand, introduces some completely new concepts.
* Bazel has a purely descriptive specification language. Earthly is a mix of descriptive and imperative language.
* Bazel uses tight control of compiler tool chains to achieve true hermetic builds, whereas Earthly uses containers and well-defined inputs.

Overall, by letting you use your existing tool chain, Earthly has an easier adoption curve and is easier to use in non-mono repo settings. This does mean that its possible to do non-repeatable actions in Earthly, but practically at organization scales smaller than Google, we have not found this to be a problem and the ease of adoption out-weighs these concerns. 

<h2 id="bsl">How is Earthly Licensed?<span class="hide"><a href="#bsl">¶</a></span></h2>

Earthly uses a source available [BSL license](https://github.com/earthly/earthly/blob/main/LICENSE) that turns into a fully open-source license after a time delay. You can read about the change on [our blog](https://earthly.dev/blog/every-open-core-company-should-be-a-source-available-company/), read [our licensing FAQ](/bslfaq), or [email us](mailto:support@earthly.dev) for licensing questions. 

<!-- vale HouseStyle.H2 = YES -->
<div class="color2">
  <div class="wrapper">
    {% include index_cta.html %}
  </div>
</div>
