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

Here are some made-up and exaggerated examples:

- **Typescript Developer:** JavaScript developers are **idiots**. Don't they know how many bugs the type system could have caught for them.  
- **Typescript Developer:** Elm developers are obsessed with types. They are **maniacs** about using types to catch things at compile time.
- **Go Developer:** The JVM is such a heavyweight runtime and uses so much memory.
- **Go Developer:** Rust is so complex! Who wants to manage memory manually. Use a GC, you **maniacs**!
- **Kotlin Developer:** Java is so verbose and ugly. Welcome to 2021. Kotlin has a lot of sugar and type improvements that make writing correct code simpler.
- **Kotlin Developer:** Scala is for **maniacs**. There is so much syntactic sugar and type stuff that it's not worth learning about.

I'm not trying to pick on any of these languages - Typescript, Go, and Kotlin are exceptionally well suited to their niche. But contexts vary[^3], and it takes mental effort to see that people making other trade-offs sometimes have good reasons for it.

That doesn't mean that other people are never wrong, though. People choose the wrong tool for the job all the time. For example, if I were doing SQLite's level of testing for a low-reliability, low-traffic, state-less web service when a couple of integration tests would do, then that'd be a mistake, but you'd have to know the context to make that call.

{% include_html cta/bottom-cta.html %}

[^1]: Richard is the creator of SQLite. See my [interview](https://corecursive.com/066-sqlite-with-richard-hipp/#billions-of-tests) with him for a discussion of his testing approach.
[^2]: **Article Update:** Apparently I've unintentionally stolen this idiot to maniac spectrum idea from [George Carlin](https://www.youtube.com/watch?v=XWPCE2tTLZQ). Thanks to tjones21xx on Reddit for pointing this out. All credit for this idea goes to Carlin.

[^3]: Personal and team familiarity can also be part of the context. PHP may not seem to be the best choice for building a command-line tool, but if it's a small tool used by a team of PHP developers, then it might be the best choice.
