---
title: "Idiots And Maniacs"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea

internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

## Observability

If you do software as a service stuff, and you have paying clients you at some point learn about the need for monitoring and observability. Personally I went through a transitory process something like this:

1. Service has some basic logging and an uptime alert
1. Service has a healthcheck endpoint, is deployed in triplicate and is behind a load balancer
1. Logs are real time shipped to Splunk / Elk Stack
1. Metrics set up in Datadog / Prometheus with paging 
1. Distributed Tracing set up
1. and so on

Each step requires more work to set up and has some additional benefits. It took me a while to move through these steps. If you would have shown the me in step 1 what a simple REST service looks like in step 5, with metrics and feeding request ids through to child services and distributed tracing spans, I would not have reacted well. I would have thought whoever wrote this is obsessed with operational issues, to the detriment of solving the actual problems at hand. He is an Observability maniac.

If step 5 me were to get paged because a service written by step 1 me were down then I would not be happy. I would have a hard time figuring out what was wrong and be pretty certain the service was written by an idiot who had no way of telling what was going on with his service. It reminds me a lot of driving my car when it first snows hear in Peterborough.

## Driving

In the winter we get snow and people are generally used to but on the first substantial snowfall people struggle to remember how to drive. Some will drive slow and slow down traffic for everyone -- they are idiots in the snow. Others get frustrated by the slow drivers and drive too fast for the road conditions -- don't they know there is snow on the road? 

Everyone driving slower than me is an idiot, but everyone going faster than me is a maniac.

So it is with software development. Everyone who takes an idea further then you have is a maniac and people who haven't seen the benefits of taking it as far as you are idiots.

## Testing

There was a time when I thought all code should have 80% unit test code coverage minimum. Anything less was practically unethical and if you didn't think so then you hadn't read Clean Code (TM) enough times.

On the other hand, Richard Hipp -- who tests to 100% code coverage at the machine code level, covering every branch by running billions of tests each release -- he is a testing maniac.

I hope you see where I'm going. This idiot to maniac gradient feels right but it makes no sense: wherever you find yourself along the spectrum is more a reflection of the context in which you work then anything else. 

Here are some totally made up examples:

* Typescript Developer: JavaScript developers are idiots, don't they know how many bugs the type system could be catching for them.  Elm developers though are obsessed with types. They are maniacs about pure functions and types.
*  Go Developers: The JVM is so heavy weight and uses so much memory. Rust though is so complex and who wants to manually manage memory.  Use a GC, you maniacs!
* Kotlin Developers: Java is so verbose and ugly. Welcome to 2021. Kotlin has a lot of sugar and type improvements that makes writing correct code simpler.  Scala though is for maniacs. There is so much syntactic sugar and advanced type stuff that although I never looked into it - I heard somewhere its not worth learning about.

I'm not trying to pick on any of these languages - Typescript, Go, and Kotlin are all fantasticly well suited to the context they are most often used in. I'm trying to point out that contexts vary and it takes mental effort to see that people making other trade offs sometimes have good reasons for it. That doesn't mean that other people are never wrong - people choose the wrong tool for the job all the time. If I were doing SQLite's level of testing for a low reliability, low traffic, stateless web service when a couple of integration tests would do then that'd be a mistake but you have to know the context to make that call.