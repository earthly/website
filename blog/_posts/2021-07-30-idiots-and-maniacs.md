---
title: "Idiots And Maniacs"
categories:
  - Articles
author: Adam
sidebar:
  nav: "thoughts"
excerpt: |
    In this article, the author explores the concept of "idiots and maniacs" in software development, drawing parallels to driving in the snow. They discuss how different approaches and perspectives can be seen as either idiotic or maniacal depending on one's own context and experience. The article highlights the importance of understanding different trade-offs and contexts in order to make informed decisions in software development.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. In this chaos of software development, Earthly provides you with a straightforward and efficient tool to manage your build processes. No idiocy, just smart, fast builds. [Check it out](/).**

## Observability

If you do software-as-a-service development and you have paying customers, you at some point learn about the need for operational monitoring and observability. Personally, I went through a process something like this:

1. Service has some basic [logging](/blog/understanding-docker-logging-and-log-files) and an uptime alert.
1. Service has a health-check endpoint, is deployed in triplicate behind a load balancer.
1. Logs are real-time shipped to Splunk / ELK Stack.
1. Metrics set up in Datadog / Prometheus with paging.
1. Distributed Tracing set up for debugging across services.
1. And so on.

Each step requires more work to set up and has some additional benefits. I moved through each step by necessity as my service handled more requests and became more important to customers.

If you had shown step-1-me what a simple REST service looks like in step 5, I would have been shocked. The metrics counters and distributed tracing spans, and various operational concerns make the service more complex. I would have thought that whoever wrote the service was obsessed with operational issues, to the detriment of solving the problems at hand. I would have thought the service author was an observability maniac.

On the other hand, if step-5-me were to get paged because a service written by step-1-me was down, he would not be happy. He would have a hard time figuring out what was wrong, and he'd be pretty sure the service author was an idiot who had never been paged in the middle of the night.

It reminds me a lot of driving when it first snows here in Peterborough.

## Driving

 {% picture content-wide {{site.pimages}}{{page.slug}}/9580.png --picture --img width="1200px" --alt {{ Driving in the snow }} %}

In the winter, in Peterborough, we get snow. It's just a fact of life, and people learn how to drive in snowy conditions. But on the first substantial snowfall of the year, people struggle to remember how to drive.

Some will drive way below the speed limit and slow down traffic for everyone. They are idiots in the snow. Others get frustrated by the slow drivers and go too fast for the road conditions. Don't they know there is snow on the road?

Everyone driving slower than me is an idiot, but everyone going faster than me is a maniac.

So it is with software development. Everyone who takes an idea further than I have is a maniac, and people who haven't taken it as far as me are idiots.

## Testing

There was a time when I thought all code should have 80% unit test code coverage as a minimum. Anything less was practically unethical, and if you didn't think so, then you hadn't read Clean Code™️ enough times.

<div class="align-right">
 {% picture grid {{site.pimages}}{{page.slug}}/9770.png --picture --img width="300px" --alt {{ SQLite }} %}
</div>

On the other hand, Richard Hipp -- who tests to 100% code coverage at the machine code level, covering every branch by running billions of tests each release[^1] -- is a testing maniac.

I hope you see where I'm going. This idiot to maniac gradient feels right, but it makes no sense[^2]. How can I be the only the person driving the right speed? Wherever you find yourself along the spectrum is more a reflection of the context in which you work than anything else.

## More Examples
<!--sgpt-->
Here are some exaggerated language biases:

- **Typescript Developer:** Criticizes JavaScript for lack of error-catching type system and Elm for overusing types.
- **Go Developer:** Finds JVM runtime heavy and memory-consuming, and Rust's manual memory management complex.
- **Kotlin Developer:** Considers Java outdated and verbose while finding Scala's syntactic sugar and type system overwhelming.

These statements don't condemn Typescript, Go, or Kotlin; each language excels in its domain. However, it's crucial to remember that different contexts call for different tools and trade-offs. Undoubtedly, people sometimes pick the wrong tool for a task, but this can't be judged without understanding the situation. 

Speaking of tools, if you enjoyed our chat about language bias, consider checking out [Earthly](https://www.earthly.dev/). It's a tool that makes build automation simpler and more versatile, and it could be the right tool for your next project.

{% include_html cta/bottom-cta.html %}
[^1]: Richard is the creator of SQLite. See my [interview](https://corecursive.com/066-sqlite-with-richard-hipp/#billions-of-tests) with him for a discussion of his testing approach.
[^2]: **Article Update:** Apparently I've unintentionally stolen this idiot to maniac spectrum idea from [George Carlin](https://www.youtube.com/watch?v=XWPCE2tTLZQ). Thanks to tjones21xx on Reddit for pointing this out. All credit for this idea goes to Carlin.
[^3]: Personal and team familiarity can also be part of the context. PHP may not seem to be the best choice for building a command-line tool, but if it's a small tool used by a team of PHP developers, then it might be the best choice.