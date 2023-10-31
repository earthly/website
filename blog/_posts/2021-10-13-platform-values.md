---
title: "The Platform Values of Earthly"
categories:
  - Articles
toc: true
author: Vlad
internal-links:
 - platform values
excerpt: |
    Learn about the platform values of Earthly, a new approach to build automation. Discover the principles that guide Earthly's design, including versatility, approachability, and reproducibility, and how they prioritize these values to create a tool that is user-friendly and adaptable.
as_related: true
topic: earthly
funnel: 3
last_modified_at: 2023-07-11
---

As creators of [a new approach to build automation](https://earthly.dev), we have always strived to create products that we ourselves would have wished we had. While this may sound easier than it actually is, the reality of the matter is that as creators it is hard to put ourselves in the shoes of a first-time user.

As experts of Earthly ourselves, it is too easy for us to just incrementally add more complexity, more primitives, more constructs that address the immediate issue at hand, but ultimately create a more difficult tool to use over time.

To address this tendency, we've put together some design principles that we want to stay true to as we continue to evolve Earthly. This is a way to keep our thinking in check and to continuously challenge ourselves to stay true to our roots.

This has been inspired by a talk given by [Bryan Cantrill](https://twitter.com/bcantrill), the then CTO of [Joyent](https://www.joyent.com/) (now cofounder and CTO at [Oxide Computer](https://oxide.computer/)) on [Platform Values, Rust, and the implications of System Software](https://www.slideshare.net/bcantrill/platform-values-rust-and-the-implications-for-system-software). The point that Bryan makes is that "all [platform values] are important". There is no question about that. However, these values are "in tension" - you need to prioritize and trade values off of each other. And as users are considering the right tool for the job, they are actually considering the right values for the job.

As a tangible example, here is a comparison between the values of **C** vs the values of **C++**:

{% picture content-nocrop {{site.pimages}}{{page.slug}}/values-c.png --picture --alt {{ Platform core values of C }} %}
<figcaption>Platform core values of C</figcaption>

{% picture content-nocrop {{site.pimages}}{{page.slug}}/values-cpp.png --picture --alt {{ Platform core values of C++ }} %}
<figcaption>Platform core values of C++</figcaption>

As you can see, C++ sacrificed **interoperability** and **simplicity** in favor of **expressiveness**. So much of where C++ succeeded at replacing C and where it didn't can be traced back to that decision.

Before jumping into talking about Earthly's platform values, I should preface this by saying that we're not there yet. For now, this is merely our north star and not yet our description. However, Earthly has been evolving fast since its initial launch in April last year and we hope that one day we can truly say that these values are 100% representative of what Earthly is.

## 1. Versatility

<!-- markdownlint-disable MD036 -->
*Interoperability, Configurability, Extensibility*

{% picture content-nocrop {{site.pimages}}{{page.slug}}/header-versatility.jpg --picture --alt {{ Versatility }} %}

The ultimate goal for Earthfiles is to completely replace CI scripts, while also serving the use-cases of local development.

Because CI scripts historically have been used for general automation, not just for building and testing software, we have to assume that Earthfiles will also be used in that manner too. Every company has that one weird build in the corner that isn't quite like all the others for various reasons. Maybe it's building a mobile app, while everything else is building Docker images for the cloud. Maybe it's executing on a different OS or CPU architecture. Or maybe it is shared with third parties. Whatever the case, Earthly should eventually be able to handle it.

In addition, the scripting language provided through Earthfiles should be complete enough and not require any subsequent wrapping nor repeated invocation of Earthly. The moment Earthfiles require wrapping we've already lost the repeatability advantage because then the wrapper can become a vector for inconsistency.

And finally, Earthly should work immediately with tools developers already use. There is no single tool that can become the best build system for all programming languages. The world of development is too fragmented between varying opinions for anyone to be able to satisfy all of them fully. For this reason, Earthly is not meant to replace any such language-specific tool. It's only meant to be a tool for glueing together various build tools into a repeatable process.

## 2. Approachability

<!-- markdownlint-disable MD036 -->
*Readability, Intuitiveness, First-time ease of use*

{% picture content-nocrop {{site.pimages}}{{page.slug}}/header-approachability.jpg --picture --alt {{ Approachability }} %}

A key issue in modern complex development environments is that not many people on the team fully understand the build. Oftentimes one engineer puts the scripts together and then they are the only ones who end up maintaining them. We call this person the "build guru" - because they know everything about the build, and nobody else does. (Does your team know the difference between `=`, `:=`, `?=` and `::=` in that Makefile you've just written? Can your team make sense of the gnarly groovy in your Jenkinsfile?)

This creates a contribution bottleneck. Improvements such as speeding up the build process as a whole, making the build less flaky, or maintaining consistency of style become harder to accomplish. And because builds are often at the heart of the automation of a team's development processes, a bottleneck in contributing to builds can easily become a bottleneck of the team's productivity.

For these reasons, Earthly aims to make builds as approachable, readable, and intuitive as possible, even if you are looking at an Earthfile with no prior experience with Earthfiles. In fact, even if you have prior experience with Earthly, you may have forgotten most of it by the time you come back to look at an Earthfile after a few weeks. And so once again you are a new user. As Guido van Rossum, the creator of Python, says "Code is read much more often than it is written." There is no reason for us not to treat build scripts in a similar manner as any other piece of code. It needs to be understandable first and foremost in order for the team to be productive, and in order for builds to be truly democratized.

Another consideration we made was the prioritization of these values. As **Approachability** is below **Versatility**, we plan to make Earthly as simple as possible, but not simpler. A common example here is the difference between Docker Swarm and Kubernetes. Swarm is really simple to use as it follows the Docker client API for the most part. So if you know how to use Docker, you will also know how to use Swarm. That's great, except that Swarm doesn't quite capture the complexity of real-world distributed systems. And even though Kubernetes is far more complicated, it is also far more suited for the real world. The lesson here is that we should design for the real world and within those constraints attempt to create a system as simple to use and understand as possible. But we should generally not trade-off real-world use-cases for ease of use alone.

## 3. Reproducibility

<!-- markdownlint-disable MD036 -->
*Repeatability, Portability*

{% picture content-nocrop {{site.pimages}}{{page.slug}}/header-reproducibility.jpg --picture --alt {{ Reproducibility }} %}

Reproducibility is the ability to consistently get the same result from the platform given the same inputs. Although Earthly doesn't yet provide full [reproducibility](​​https://reproducible-builds.org/) -- i.e. byte-for-byte deterministic output -- it does achieve what we call **repeatability**: a level of guarantee that the execution environment is isolated from host-specific characteristics or customizations.

Because we value repeatability, Earthly has been designed around container technology and just about every build step takes place isolated from one another and from the host itself. Repeatability is, for example, the reason for which we don't allow host mounts. Host mounts are… well… host-dependent. So they can be a source of inconsistency.

However, our other values, **versatility** and **approachability** mean that we need to allow people to bring their own tools to use in conjunction with Earthly and it has to be easy. Many of these tools are not deterministic. They might include timestamps, or they might download things from the internet that are not pinned to a specific hash. There is no reason for Earthly to block usage entirely if a build isn't deterministic. It is far better for Earthly to be versatile (usable at all in such cases) and approachable (not requiring fiddly configuration related to obscure timestamps) first. However, even in such cases, Earthly does provide container isolation of the build, to help with maintaining a consistent execution environment, regardless of the computer or operating system Earthly sits on top of.

We have found that in the real world the vast majority of projects benefit from this tradeoff between the ease of onboarding new builds onto Earthly and the level of reproducibility of the builds across environments. Reproducibility is important to us, but not important enough to prevent the vast majority of build tools from working out of the box with Earthly.

## Other Values

Besides the above top 3 platform values, we also wanted to put together a set of background values that we want to embody, but which aren't necessarily competing with one another. The order matters less here.

### Speed

<!-- markdownlint-disable MD036 -->
*Performance, Computation reusability*

{% picture content-nocrop {{site.pimages}}{{page.slug}}/header-speed.jpg --picture --alt {{ Speed }} %}

The number one complaint we hear about people's builds is that they take too long. And this isn't about the difference between 5 minutes vs 3 minutes. It's much more about 30 minutes vs 10 minutes. Builds that take longer than 15-20 minutes really slow down engineering productivity. It's like this great wall that eventually everyone faces and all of a sudden makes build performance a top priority.

In that sense, Earthly should aim to be performant, cache as much as possible, and also parallelize to the extent possible.

### User Respect

<!-- markdownlint-disable MD036 -->
*Integrity, Transparency*

{% picture content-nocrop {{site.pimages}}{{page.slug}}/header-user-respect.jpg --picture --alt {{ User respect }} %}

If users trust Earthly with running it on their computers, or in their build automation infrastructure, then Earthly should abide by the highest integrity standards. The overall theme is to not do to our users what we wouldn't wish to be done to ourselves.

This is probably a value that should go without saying. We decided to put this in writing as a constant reminder as we grow as a community and as we evolve the use-cases of Earthly.

### Consistency of Experience

<!-- markdownlint-disable MD036 -->
*Simplicity*

{% picture content-nocrop {{site.pimages}}{{page.slug}}/header-consistency-of-experience.jpg --picture --alt {{ Consistency of experience }} %}

High-quality products tend to be robust, consistent, intuitive, and simple. The fact that some language concepts can be reused across the Earthly experience makes the tool easier to understand and therefore more accessible. This helps with always knowing what to expect of the tool even in areas that the user is unfamiliar with.

## Non-Values

As mentioned before, coming up with platform values is much more an exercise in trading off certain values over others. All values are important - it's much more a question of prioritization more than anything.

With that in mind, by having chosen the above values, we are also consciously deprioritizing others. Here's what we are sacrificing.

### Non-Value: Expressiveness

Expressiveness could be interpreted as the ability to specify complex behavior through compounding a few highly versatile language primitives. In here, highly versatile could also be interpreted as "magical", but also as "having more than one way to do the same thing". We make a conscious decision to avoid non-obvious inferences in the Earthfile language. The main reason being that things that are not very explicit often translate to behavior that first-time users would not understand. In fact, the more explicit the language is, the better. Even if it takes more lines of code, even if it's sometimes a bit repetitive.

To quote another great software engineer,

> "Indeed, the ratio of time spent reading versus writing is well over 10 to 1. We are constantly reading old code as part of the effort to write new code. ...[Therefore,] making it easy to read makes it easier to write."
>
> ― Robert C. Martin, Clean Code: A Handbook of Agile Software Craftsmanship

As an example, in Earthly we don't have short-hand flag options as part of the Earthfile commands. A new user would not be able to tell what `BUILD -P +my-target` does, however, they should be able to intuitively figure out `BUILD --allow-privileged +my-target`.

### Non-Value: Velocity

Users don't like to upgrade their build scripts. It's a thankless job. For that reason, evolving Earthly itself fast isn't a priority. It is much more preferable for build scripts to stay repeatable for a long time, rather than to have to constantly update them to stay in sync with the very latest version of Earthly.

In fact, in a future version of Earthly, the very latest version will be able to also run scripts of older versions, with some guarantees that they will work the same as that older versions. See [Proposal: VERSION](https://github.com/earthly/earthly/issues/991).

### Non-Value: Opinionated

On a spectrum from **Versatile** to **Opinionated**, we prefer to be on the versatile side. Opinionated tools often help with simplicity and consistency of experience. However, they often make the sacrifice of not being compatible with some workflows or technologies. For the reasons stated under **Versatility**, we made a conscious decision to prefer flexibility over strictness.

You might say here "but wait a minute, in Earthly, everything is a container. Aren't you being opinionated?". Yes - to some extent. But also, in Earthly, there is also [LOCALLY](https://docs.earthly.dev/docs/earthfile#locally-experimental), which executes commands directly on the local host. So here you can see we have preferred being flexible in order to address use-cases specific to local development.

## Conclusion

Hopefully, this prioritization exercise will help us as a community to more easily reason about the design of new features, but also help new users decide whether Earthly is the right tool for their job.

Note that these principles aren't meant as hard and fast rules - they are mainly guidelines. There may be occasions when the sensible thing to do is to make an exception.

If you're new, come give [Earthly a spin to experience Repeatable and Understandable builds](https://earthly.dev).

{% include_html cta/bottom-cta.html %}
