---
title: On YAML Discussions
tags:
- news
categories:
  - Articles
author: Adam
excerpt: |
    Learn about the pitfalls and discussions surrounding the use of YAML as a programming language, including the challenges of config traps, alternative solutions like Dhall and HCL, the creation of DSLs, and the benefits of using a full programming language for configuration files. Dive into the lively discussions on Reddit, Hacker News, and Lobste.rs to gain insights from the programming community.
last_modified_at: 2023-07-11
---
**The article examines YAML's limitations in CI configurations. Earthly provides clear and reproducible build definitions that overcome YAML's limitations. [Learn more about Earthly](https://cloud.earthly.dev/login).**

My article about how [YAML makes a bad programming language](https://earthly.dev/blog/intercal-yaml-and-other-horrible-programming-languages/) [^1] generated a lot of great discussions online.

Here are some highlights, lightly edited:

## Config Traps

[dkarl](https://news.ycombinator.com/item?id=26276420) pointed out that putting things in config files that shouldn't be there happens for many reasons:

> **Reason:** Pride in creating a "generic" system that can be configured to do all kinds of new things "without touching the code."
>
> **Reality check:**
> only one or two programmers understand how to modify the config file, and changes have to go through the same life cycle as a code change, so you haven't gained anything. You've only made it harder to onboard new programmers to the project.
>
> **Reason:** Hope that if certain logic is encoded in config files, then it can never get complicated.
>
> **Reality check:**
> Product requirements do not magically become simpler because of your implementation decisions.
>
> **Reason:** Hope that you can get non-programmers to code review your business logic.
>
> **Reality check:** the DSL you embedded in your config file isn't as "human readable" as you think it is.

## Dhall Is Strange

[AndyC](https://lobste.rs/s/1nxt6g/intercal_yaml_other_horrible#c_pc0dt6) thought that Dhall was not the right answer to the YAML problem:

> I agree with the problem, but disagree with the solution. Total languages don't give you any useful engineering properties, but lack of side effects do (and Dhall also offers that).
>
> From the surface, it seems like HCL, jsonnet, and Cue, are just as suitable as Dhall, and probably more familiar (to varying degrees).

This is an excellent point.  [HCL](https://github.com/hashicorp/hcl) does look a bit less strange to outsiders, and HashiCorp already has mind share in the DevOps community, and it certainly beats config templates.

## DSL Creation Story

reddit user [XANi_](https://www.reddit.com/r/programming/comments/ls6tgm/intercal_yaml_and_other_horrible_programming/gopf8fj/?utm_source=reddit&utm_medium=web2x&context=3) explained how DSL's embedded in YAML keep getting created:
> The vicious cycle of
>
> * We don't want config to be Turing complete, we just need to declare some initial setup
>
> * Oops, we need to add some conditions. Just code it as data, changing config format is too much work
>
> * Oops, we need to add some templates. Just use <primary language's popular templating library>, changing config format is too much work.
>
> * And congratulations, you have now written a DSL
>
>If you need conditions and flexibility, picking existing language is by FAR superior choice.

## Rake, Webpack, and Groovy
<!-- markdownlint-disable MD028 -->
Many readers pointed out that their development community skipped right by this DSL dead end by using a full programming language for build and config needs:

> I always thought it was weird that a lot of web technologies take config files that are executable JavaScript. (Thinking of webpack). But it makes a lot of sense now, and I much prefer that approach. - [Bunny](https://www.reddit.com/r/programming/comments/ls6tgm/intercal_yaml_and_other_horrible_programming/gopq0uv/?utm_source=reddit&utm_medium=web2x&context=3)

> It's fairly common in Pythonland \[ to just use Python\] ...
>
> It's an ideal solution for technically-savvy users in non-security sensitive contexts. - [crakers](https://www.reddit.com/r/programming/comments/ls6tgm/intercal_yaml_and_other_horrible_programming/gopy30z/?utm_source=reddit&utm_medium=web2x&context=3)

> I'm not convinced that just using programming language for your configuration files is actually that bad. For instance, with node, if you just use JS files that export an object instead of. JSON files, you end up with a lot more programmable and flexible thing. I don't actually see the problem. - [light24bulbs](https://www.reddit.com/r/programming/comments/ls6tgm/intercal_yaml_and_other_horrible_programming/goqm3z0/?utm_source=reddit&utm_medium=web2x&context=3)

## Writing a Parser

Hillel Wayne wrote a [great newsletter](https://buttondown.email/hillelwayne/archive/a3fe2688-464d-4f98-ae6b-207e7b5a1255) on YAML, and the ways it's abused. He pointed out that the main competition for embedding your DSL into YAML is writing a parser, and using YAML is just easier.

>[YAML] pre-parses the content for us. This isn't a big enough draw to YAMLize complex programming languages, but it's a huge deal for small DSLs. I suspect that's the main reason why semgrep uses YAML for its rules and why so many technologies jury-rig it into a configuration language

You can see the full commentary on the original article on [reddit](https://www.reddit.com/r/programming/comments/ls6tgm/intercal_yaml_and_other_horrible_programming/), on [Hacker News](https://news.ycombinator.com/item?id=26271582) and on [Lobste.rs](https://lobste.rs/s/1nxt6g/intercal_yaml_other_horrible).

[^1]: To clarify, YAML, when used as the syntax frontend for a domain-specific, vendor-specific, programming language is a bad idea. I am aware YAML is not a programming language itself.
