---
title: "What Is Continuous Integration?"
categories: 
  - Build
toc: true 
author: Deborah Ruck
internal-links:
 - continuous integration
 - circleci
 - github actions
 - azure
excerpt: |
    Learn the basics of continuous integration, the differences between CI and CD, and common CI tools in this informative article. Discover how CI can help developers catch bugs earlier, increase productivity, and deliver higher-quality releases.
last_modified_at: 2023-07-14
---
**In this article, you'll learn the principles of continuous integration. Earthly can improve this process. [Check it out](https://cloud.earthly.dev/login).**

Continuous integration has become prevalent in software development, but it's still a complex and wide-ranging topic. In this post, we'll cover the basics of continuous integration, the differences between CI and CD, and common CI tools. You'll also find some tips for the best way to set up CI in your environment.

## What Is Continuous Integration?

Continuous integration (CI) is a set of operating principles and practices in the DevOps process that helps software development teams release faster and more reliable application updates. With the advancement of modern tooling, most CI processes center around automated tests, static analysis, and building releasable software. This process is helpful for teams that want to ensure each update to their software is working, stable, and ready to deploy before they integrate it into their production environment.

For example, if a team member makes a change to a project, they might make updates on a new branch (assuming they're using [git for version control](https://git-scm.com/)). When complete, they *push* these changes to a shared [repository](/blog/monorepo-vs-polyrepo) where a continuous integration workflow will automatically install dependencies, run tests, and check for linting errors before merging the changes into the main branch.

## The Relationship Between Continuous Integration and Continuous Delivery/Deployment

Continuous integration is the first part of the CI/CD process. The *CD* stands for either *continuous delivery* or *continuous deployment*. Although these terms are sometimes used interchangeably, they are not quite the same.

In both cases, code is released in short cycles. However, with continuous delivery, code changes are automatically deployed through the development and [testing stages](/blog/unit-vs-integration), but must be manually reviewed and approved before being batched and released to production.

With continuous deployment, code changes that successfully pass through all stages of the development process are automatically released to production without human intervention. A failed test along the pipeline is the only event that will prevent a change from reaching production.

### Why CI Is Important to Software Development

> "Continuous integration doesn't get rid of bugs, but it does make them dramatically easier to find and remove." – [Martin Fowler](http://www.thoughtworks.com/continuous-integration?utm_source=Codeship&utm_medium=CI-Guide  "CI explainer at ThoughtWorks"), Chief Scientist, ThoughtWorks

Before continuous integration became an industry standard, developers' changes were tested less frequently, often only when it was time to release a new version of the software. This meant the team had to spend unnecessary hours fixing bugs that could have been caught earlier in the process with a robust continuous integration process.

CI helps developers avoid such problems while increasing productivity. Because code changes are automatically and continuously tested, verified, and built, developers should not have to manually check for integration issues. Because testing in CI is frequent and automated, developers can find and address bugs faster and earlier in the software development life cycle. This promotes a culture that delivers faster, higher-quality releases into production.

## How CI Works

CI validates changes upon check-in using an automated build process that also runs validation and integration tests. The continuous integration process aims to detect bugs and errors faster and eliminate the integration issues that occur when developers work in isolation, resulting in higher quality software releases and faster delivery times.

### A Typical CI Build Process

![Earthly integration diagram]({{site.images}}{{page.slug}}/r80Ri4R.png)

In a typical CI build process, developers push code changes from a branch to a central repository such as GitHub. CI automation servers such as Jenkins and CircleCI continuously monitor the repository to check for code updates.

Once it detects a change, the automation server triggers the build process to compile and build the code, then run validation and integration tests. CI automation servers interface with compilation tools such as Docker, Bash, and Makefile to create deployable artifacts such as binaries, packages, or Docker images. When [continuous deployment](/blog/deployment-strategies) is employed, the built application is then deployed and run on subsequent testing or production environments. Other developers can also pull down the resulting image and test locally.

If the build fails, the development team will typically receive an alert, allowing them to fix any errors that occur.

### How Has CI Changed in the Past Few Years?

CI became popular as an integral part of agile software development but has since developed into one of the pillars of the DevOps process. Guided by key principles such as revision control, software integration, and build automation, it is now an industry standard in software development.

As DevOps practices [continue to evolve](https://www.novelvista.com/blogs/project-management/3-devops-trends-in-2020 "NovelVista blog on DevOps changes in 2020"), we see trends moving toward self-service and a more cloud-centric model to give developers more autonomy. Because of COVID-19, CIOs and other IT leaders have recognized the need to adjust and adapt to support more cloud-based workflows and applications. Moving forward, cloud-native approaches, including multi-cloud solutions, will become the standard for hosting, pipelines, storage, and load balancing.

As part of the self-service trend, developers will no longer have to wait for a separate operations team to dispatch new applications or updates, but will instead be able to build DevOps infrastructure that allows them to deploy updates themselves. Self-service capabilities are already available today for several DevOps processes, including development environments, CI/CD workflows, and audit logging.

## Common Tools for CI

Your choice of CI tools will largely depend on your business requirements, the tech stack you already have or plan to implement, and your daily workflow. There are many CI tools and solutions to choose from. Let's look at four of them.

### Jenkins

[Jenkins](https://www.jenkins.io/) is the most well-known continuous integration tool and has a reputation for reliability. Written in Java, it's an open-source cross-platform tool with a large community following that contributes to its development.

Jenkins works as a standalone CI server or a continuous delivery platform and offers several features to support the entire software development life cycle, including automated builds and testing, code debugging and analysis, and project deployment.

It can run on any operating system including Windows, OS X, and Unix, and you can easily configure it via a web GUI interface or console commands. Jenkins is highly extendable; thanks to its robust ecosystem of almost 1400 plugins, you can add several features for user interface, platform integration, source code management and builds, and administrative tasks.

- **Where is it hosted?** Self-hosted; cloud
- **What platform does it run?** Containers; virtual machines
- **What is its pricing model?** Open source

![Jenkins CI/CD Tool]({{site.images}}{{page.slug}}/xoiqawt.png)

### CircleCI

[CircleCI](https://circleci.com/) is an excellent platform for build automation and testing along with a branch-focused deployment process. It integrates seamlessly with several version control systems, container systems, and delivery mechanisms, including GitHub and Bitbucket as well as build tools such as Gradle and Apache Maven. You can host CircleCI on premise or integrate it with AWS, Google Cloud, and other cloud services. It's highly customizable and performance-optimized for quick builds, and it also provides analytics to measure build performance.

- **Where is it hosted?** Self-hosted; cloud
- **What platform does it run?** Containers; virtual machine
- **What is its pricing model?** Free entry-level version; Premium starts at $30

![Circle CI CI/CD tool]({{site.images}}{{page.slug}}/HmA7mZy.png "Circle CI CI/CD tool")

### GitHub Actions

Introduced in 2018, [GitHub Actions](https://github.com/features/actions) is one of the newer tools in the CI/CD tech stack. It is fully integrated within GitHub, making it manageable from a single place.

Integration with GitHub means you can build, test, and deploy code directly from your GitHub repository. GitHub manages the execution and provides feedback and security for the entire CI process.

GitHub Actions offers a wide range of automation tasks and actions that allow you to create, share, reuse, and branch software development workflows directly in your GitHub repository. It also supports Docker for multi-container testing and offers several CI templates.

- **Where is it hosted?** Self-hosted; cloud
- **What platform does it run?** Container; virtual machine
- **What is its pricing model?** Free for public repositories and self-hosted runners. For private repositories, build minutes/month depend on account type and spending limits

![GitHub Actions CI/CD tool]({{site.images}}{{page.slug}}/Gu0ruur.png "GitHub Actions CI/CD tool")

### Azure DevOps

[Azure DevOps](https://azure.microsoft.com/en-us/services/devops/) by Microsoft is a platform for creating a CI/CD pipeline to Azure. It provides several advanced features and services that support the software development cycle from planning to deployment. Azure DevOps integrates with both Team Foundation Version Control and Git for version control, code repository management, and build automation.

Azure DevOps also integrates with major languages and platforms, allowing you to build, test, and deploy in Java, .Net, Android, or iOS. It also runs parallel on Linux, macOS, and Windows and on both virtual machines and containers.

One standout feature of Azure DevOps is that it supports automated load testing, which can simulate thousands of users using your app at the same time. This helps your developers uncover bottlenecks and improve throughput before an application is released.

- **Where is it hosted?** Self-hosted; cloud
- **What platform does it run?** Container; virtual machine
- **What is its pricing model?** Free up to a specific number of builds, but build servers can be reserved at a cost for higher volumes

![Azure DevOps CI/CD Tool]({{site.images}}{{page.slug}}/iIfItCx.png "Azure DevOps CI/CD Tool")

## Continuous Integration Best Practices

To get the most out of your CI process, you'll need to set it up with the following best practices: consistency between environments, disciplined use of the CI/CD pipeline (no sidestepping it for special cases), prioritizing tests by speed, and the "Build Once" practice.

### Strive for Consistency Between Environments

We've all had it happen: code that works perfectly in your development environment throws a hissy fit in production.

Your CI environment should either match production exactly or be customized in a way that mitigates any bugs that might happen due to the difference in the two environments. The wider the difference between your development or staging and production environments, the less accurate your tests will be in showing how the code will perform in the real world.

A few ways to make sure that your environments are consistent are as follows:

- Using [blue-green deployments](https://www.redhat.com/en/topics/devops/what-is-blue-green-deployment). This release strategy involves running two parallel versions of the production environment and involves using a load balancer to swap production traffic between two environments alternately designated as production (green) and staging (blue).
- Deploy a scaled-down version of your production environment to your development or staging environment. If you're using this method, ensure that the code is consistent and that differences between the two environments are well-documented.
- Use a clone of the production environment to make sure that your CI environment is an exact match.

### All Deployments Must Go Through CI

CI acts as a watchman to enforce best practices in the development process and ensure that changes are in line with your company's standards and procedures. A failure during integration is flagged immediately and prevents the affected code from moving forward into other parts of the development process. This protects subsequent environments like production from untrusted or error-prone code.

For CI to be successful, you'll need to make sure that the CI/CD pipeline is the only mechanism through which code enters your production environment. This could be via continuous delivery with manual approval processes and batched releases or through automated continuous deployment practices.

Development teams may feel pressured to make exceptions and circumvent the CI process when problems arise. It's tempting to bypass the system to mitigate excessive downtime and fix other issues as soon as possible, but adhering to the CI/CD pipeline helps ensure that the changes being made won't worsen the current problem or introduce new ones.

Sending all changes through the CI/CD pipeline helps to protect the integrity of your deployments and prevents ad hoc fixes from being erased by subsequent updates.

### Run Your Fastest Tests/Checks First

The general goal of the CI/CD process is to provide rapid feedback to developers and promote rapid software delivery to users. You want to keep the entire pipeline fast, but the reality is that some parts will be faster than others. If developers have to wait too long to get feedback from testing, they might look for ways around the process.

Because you want to discover failures as early as possible, prioritize, and run the tests that complete quickest first and leave longer running tests until later.

This usually means running your unit tests first, as those are faster, make up most of your tests, and can give you immediate feedback on bugs and errors introduced by the latest update. After unit testing is complete, run integration tests next to see how different parts of your code interact. Then follow up with system-wide tests such as GUI, performance, load, and security tests, and manual acceptance tests.

### Build Only Once and Promote the Result Through the Pipeline

One aim of CI/CD is to ensure that your end product is robust and won't produce unexpected results. This is why it's important to perform your build step only once and then advance resulting binaries through the entire pipeline. Software builds that occur separately at each new stage of the pipeline can introduce inconsistencies, and tests completed in earlier environments become invalid because they may not be targeting the same software that is eventually deployed.

In the "Build Once" best practice, the build process always occurs as the first step in the pipeline, and the resulting artifact is versioned and uploaded to the central repository where it can be pulled and used in the later stages. This ensures that the build does not change as it moves through the pipeline.

## What's Next?

Continuous integration speeds up the software development process and helps development teams avoid common pitfalls such as broken application builds, and chaotic release cycles. Rather than catching issues just before (or even after) they're released, continuous integration allows you to mitigate errors *while* you're working on a feature.

[Earthly](https://cloud.earthly.dev/login) is a free and open-source build automation tool that works with your existing build systems to create repeatable, containerized, language-agnostic builds. It acts as a layer between language-specific tools such as Gradle and Apache Maven and the CI buildspec and allows for faster iteration on build scripts and easier debugging. You can discuss automation and other topics in the [Earthly Community on Slack](https://earthly.dev/slack).

To find out more about how Earthly can help you simplify your CI systems, check us out on [GitHub](https://github.com/earthly/earthly "Earthly build automation tool documentation and download"). With CI automation in place, developers can push changes more frequently, get faster feedback, and ensure that every change is integrated, tested, and verified.
