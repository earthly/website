---
title: "Achieving Repeatability in Continuous Integration"
categories:
  - Tutorials
toc: true
author: Allan MacGregor
internal-links:
 - repeatability
 - reusability
 - reliability
excerpt: |
    Learn how to achieve repeatability in your continuous integration pipeline and improve the reliability, reproducibility, reusability, and speed of your builds. Discover best practices for test automation, adopting continuous integration, and fixing broken builds immediately.
last_modified_at: 2023-07-19
---
**This article delves into Continuous Integration practices. If you're committed to improving your CI workflows, Earthly can help. [Discover Earthly's role](https://cloud.earthly.dev/login).**

<!-- vale HouseStyle.EG = NO -->
> In software engineering, continuous integration is the practice of merging all developers' working copies to a shared mainline several times a day. Grady Booch first proposed the term CI in his 1991 method, although he did not advocate integrating several times a day. —[Wikipedia](https://en.wikipedia.org/wiki/Continuous_integration "Wikipedia article on continuous integration")

Continuous Integration (CI) and continuous delivery (CD) are some of the best practices that any DevOps team can implement. You could argue that they're necessary for teams looking to ship quality products fast and with confidence.

CI and CD are two pieces of a whole, the former dealing with the task to automate the process of building, testing, and integrating new features and code changes into the codebase mainline; and the latter dealing with automating the process of delivering the changes to the defined environments.

The implementation of both methodologies is often referred to as a **CI/CD pipeline**; it is worth noting that both for CI and CD, the operating principles and coding philosophy are equally as important as the technical aspect of the implementation.

CI's technical goal is to provide consistent and automated results to build, package, and test applications. This repeatable flow and process allows teams to commit and merge changes more frequently, thus reducing the risk of conflicts or getting stuck in **Integration Hell**.

> Integration Hell refers to the point in production when members on a delivery team integrate their individual code. In traditional software development environments, this integration process is rarely smooth and seamless, instead resulting in hours or perhaps days of fixing the code so that it can finally integrate. Continuous Integration (CI) aims to avoid this completely by enabling and encouraging team members to integrate frequently (e.g., hourly, or at least daily).  —[SolutionsIQ](https://www.solutionsiq.com/agile-glossary/integration-hell/ "Accenture | SolutionsIQ's definition of Integration Hell")

This article focuses on the concepts, tools, and best practices that will allow you to achieve a high degree of repeatability and consistency on your CI/CD pipeline.

## CI Repeatability Principles

One of the critical aspects of a successful and healthy CI pipeline is having repeatable builds, which guarantee consistent and reliable results. Four fundamental principles are essential to observe to achieve repeatability:

- Reliability
- Reproducibility
- Reusability
- Speed

### Reliability

Reliability in continuous integration comes from knowing that the systems involved in testing the application are both available and capable of performing the complete set of tests that we need. This also means that the system has to produce consistent builds.

Reliability gives the confidence to deliver shippable working code at any time during the application lifetime.

### Reproducibility  

CI infrastructure and pipelines can be—and more often than not, are—software assets on their own. The work done to create and implement CI runners and pipelines for our software projects can also be built, tested, and packaged just like any other software build.

Examples of this are containerizing the environments used to run your test suites, including dependencies such as a database or ancillary applications for the end-to-end test suites.

Treating the CI pipelines as another software project also allows the development team to reproduce the same results from the CI pipeline locally and shorten the feedback loop.

### Reusability

With reproducible builds, we can achieve reusability, meaning that the same tools and process can be used in more than one project. Having a system in which we are not building a special custom CI pipeline for each project allows us to find patterns that we can apply to many projects.

The type of reusable resources greatly varies depending on the type of applications and tests on each organization, from simple reusable scripts to containerized environments.

### Speed

One of the primary benefits of a good and effective CI process is the feedback loop it provides to the developers working on a project. Feedback loops start losing their value and [detract from developer effectiveness as they get slower](https://martinfowler.com/articles/developer-effectiveness.html "Tim Cochran's article on maximizing developer effectiveness at MartinFowler.com").

We need to consider several factors when building a support CI pipeline, from the underlying hardware and test runners to the structure of the unit tests themselves as a larger unit. Integration tests do add to the overall testing time, and it's important to keep that time short to make the value of the tests high.

## Best Practices

Now that we understand why **reusability**, **reproducibility**, **reliability**, and **speed** are important for building repeatable and effective continuous integration pipelines, let's talk about specific practices and processes that can help achieve them.

### Test Automation and Coverage

To leverage the full value of continuous integration, you will need to automate all your tests and make sure they run for every change made to the repository. It's also advisable to leverage the following:

- **Unit tests** to verify the behavior of small methods and functions
- **Integration tests** to make sure multiple components work together
- **Acceptance tests** to cover behavior required on the business specifications
- **End-to-end tests** to validate the behavior of the application as a whole from the user perspective

### Adopting Continuous Integration

While automation and observability of our pipelines are important, the cultural aspects of working with continuous integration and ensuring that the team adopts the continuous integration principles are equally as important.

#### Integrate Early and Often

A crucial cultural aspect of continuous integration is building the habit and cadence of the team committing their code every day and multiple times per day. By pushing their code frequently, developers can quickly find conflicts between two changes and also become aware of other work.

Additionally, pushing their commits often allows developers to get feedback from the full CI pipeline running and allow them to identify defects in the code much sooner.

The rule of thumb is that developers should commit their code every day, whether it is to the mainline branch on a feature branch. The more frequently you commit, the less opportunity there will be for conflict, errors, or broken tests, significantly increasing the team's speed.

#### Fail Early and Fail Fast

The whole point of continuous integration is providing rapid feedback. Nothing is more frustrating than a build that takes hours to complete, only to fail because of errors in some of the initial test suites.

It is possible that due to the size of the application, the complete set of tests (unit, integration, end-to-end) might take a while to run. To help things go smoothly, you should consider the following processes:

- Breaking tests into groups (per module, per domain, and so forth) and running them in parallel
- Run critical path tests first (core or fundamental logic)
- Fail and stop the entire build if critical tests fail
- Integrate with notifications systems (Slack, email) to let developers know as soon things fail

#### Make It Visible

A core tenet of continuous integration is communication, so you want to ensure that everyone can easily see the state of the system and the changes that have been made to it.

Information such as the states of integration branches and the state of the mainline build become a priority. Back in the day, engineering teams would go as far as hooking up physical traffic lights to signal the state of the mainline branch.

![Semaphore CI]({{site.images}}{{page.slug}}/anBo2up.png)

Nowadays, with cloud solutions being more prevalent and deeply integrated with source control systems, it's much easier to give all developers a high degree of visibility. A perfect example is CI pipelines with [GitHub Actions](https://github.com/features/actions "GitHub Actions workflow automation"), which provides feedback directly on pull requests and allows you to visualize the state of a pipeline at every given step.

![GitHub Actions CI]({{site.images}}{{page.slug}}/twM26E6.png)

#### Fix Broken Builds Immediately

A crucial part of implementing continuous integrations is that if the mainline build fails, it needs to be fixed right away. One of the key points of working with CI is having a trusted, stable code base to develop against.

The mainline build breaking is not necessarily a bad thing on its own. Still, it might highlight gaps in how the team works, like people not being careful enough about updating and building locally before committing.

The fastest way to fix a broken build is to roll back to the last known good commit and review what happened. By all means, we should avoid debugging on the broken mainline; this becomes especially true when multiple teams are working on the same code base.

## Conclusion

Continuous integration (CI) is a game-changer! It helps find bugs quicker, speeds up the feedback loop, removes integration issues, and boosts team communication and pace. To ace your CI/CD pipeline, remember these principles:

- Ensure your environments are **reliable** and **speedy** to keep development moving.
- Aim for **reproducible** builds for developer confidence.
- **Reusability** allows us to leverage the tools, patterns, and environments for continuous integration across projects.

Speaking of reproducible builds, if you're looking to improve your CI/CD pipeline, you might want to give [Earthly](https://cloud.earthly.dev/login) a spin. It's a tool designed for speedy, reproducible builds, which can significantly enhance your CI/CD process.

CI also paves the way for **continuous deployment** and combined with continuous delivery, it helps ship and test features faster.

Want to dive deeper into CI? Check out [Martin Fowler's book](https://www.martinfowler.com/books/duvall.html) on it!
