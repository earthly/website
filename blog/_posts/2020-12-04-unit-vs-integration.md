---
title: Unit Testing vs Integration Testing
toc: true
categories:
  - Articles
author: Adam
internal-links:
  - integration testing
  - unit test
  - unit testing
excerpt: |
    Learn the differences between unit testing and integration testing and when to use each approach. Discover how unit tests focus on small, isolated pieces of code, while integration tests ensure that different components of your software work together seamlessly.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about the differences between unit testing and integration testing. Unit testing and integration testing are two different approaches to testing software. [Check us out](/).**

In 1998, Kent Beck wrote sUnit, a unit testing framework for SmallTalk. Beck later ported this framework to Java as jUnit. From there, xUnit frameworks spread to the most popular languages. Newer languages, like [GoLang](/blog/top-3-resources-to-learn-golang-in-2021) and Rust, have incorporated testing into the compiler and standard library directly.

But unit testing is not the only game in town. There are also integration tests and performance tests and much more. In my mind, though, Integration tests and unit tests are the foundations of resilient software. So today let's look at the differences between the two and when you might prefer one or the other.

## What Is a Unit?

{% include imgf src="unit.png" alt="A unit is the smallest piece of code that is logically separate" caption="A unit is the smallest piece of code that is logically separate" %}

A unit test is a test that is testing the smallest possible pieces of code in isolation. What then is a unit?

The term unit comes from mathematics. The number 1 is considered the unit as it is the smallest natural number. It is the smallest positive yet whole number. By analogy, a unit of your source code is the smallest piece of code that is logically separate from the rest of the code. It is a whole piece, a logically distinct area code, and it is the smallest possible such piece.

In most programming languages your unit is going to be a function or method call.

The great thing about unit testing is that if your code is structured in small independent pieces then writing tests for them can be quite easy. This ease of writing means that unit testing can be done as you develop features.

In comparison to other forms of testing, the execution time of unit tests is quite small. This means that you can run unit tests very frequently. As software matures a suite of unit tests is a powerful tool for preventing regressions and easing maintenance costs.

## Retroactive Unit Testing

> When considering an effort to add unit tests to existing software, costs, as well as benefits, need to be considered.

A key assumption of unit testing is that the software under test easily separates into distinct units. In software written without unit testing in mind, this assumption rarely holds. Adding unit tests to existing software is often a great way to stabilize it and prevent future regressions, but refactoring the code to support easy unit testing may require substantial effort and could even introduce new defects. When considering an effort to add unit tests to existing software, costs, as well as benefits, need to be considered. If you have working code, and if the code rarely needs to change, and if the code is not easily unit-testable the benefits may not warrant the costs. In such cases, consider leaning on integration tests to prevent defects in that area.

## What Is an Integration Test?

{% include imgf src="integration.png" alt="Integration tests focus on the whole of the software stack" caption="Integration tests focus on the whole of the software stack" %}

If the philosophy of unit testing is based on the insight that testing small independent pieces of code is a great way to prevent regressions then integration tests are based on the understanding that things often go wrong at the edges. The outside world is a messy place, and where it interacts with your code is usually where surprises happen.

You can achieve 100% code coverage with your unit tests but still, find your software fails. You might be trying to read a file from the wrong location, or your software might get unexpected output from a service that calls it or it might call a database in an invalid way.

Whereas unit tests should be quick to run and numerous, a great integration testing strategy should focus on a lesser number of high impact tests.

Those tests should cross all the lines that unit tests won't, writing to the file system, reaching out to external resources, and so on.

## When Integration Testing Gets Tricky

Certain truly external systems may be difficult to integrate into tests. This is because they have side effects in the real world that cannot be undone: A financial transaction, an email send, physically moving a paint robot. Before you give up and sidestep them in your testing, look around for solutions.

Many external systems will have a documented way to use them in an integration test. Payment processors often have test credit card numbers, and test users with test email accounts can be set up for testing delivery.

The closer integration tests are to real-world interactions the more likely they are to catch problems and provide real value.

| Service | Integration Test Strategy |
|