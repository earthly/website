---
title: "Incident Management Metrics and Key Performance Indicators"
categories:
  - Tutorial
toc: true
author: Adam
internal-links:
 - mtbf
 - mttr
 - mtta
 - metrics
 - incident management
excerpt: |
    Learn about the essential metrics and key performance indicators (KPIs) for incident management in software development. Discover how Mean Time Between Failures (MTBF), Mean Time to Recovery (MTTR), Mean Time to Resolve (MTTRe), and Mean Time to Acknowledge (MTTA) can help improve the quality of your software releases and enhance your incident response process.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about incident management metrics and key performance indicators. Earthly is a powerful build tool that can greatly enhance the software development process by providing efficient and reliable CI/CD workflows. [Check us out](/).**

<!-- markdownlint-disable MD024 -->
In 2008, I got my first job at a software-as-a-service company. We built learning management software and ran it on servers in the small data center connected to our office.

We released new software onto these production servers monthly and measured quality by counting bugs per release. We also had account managers who kept us informed of how many large clients seemed upset about the last release.  

Occasionally, when something went wrong, we would do a stability release and spend a month only fixing bugs.  [Testing](/blog/unit-vs-integration) was not a part of our build process but a part of our team: every feature team had quality assurance people who tested each feature before it was released.

This wasn't that long ago, but cloud software development has matured a lot since this time. Incident management has become standard practice, and many great metrics and Key Performance Indicators (KPIs) exist for measuring release quality. Let's review some of them.

## Mean Time Between Failures (MTBF)

When software is being released only once a month, on a fixed timeline, with extensive manual testing, counting the number of bugs might work. But once you start releasing many times per week or per day, this won't work, and another way to measure software quality is required.

Mean time between failures is a metric from the field of [reliability](/blog/achieving-repeatability) engineering. Calculating it is simple: it is time over the number of failures that occurred during that time. If in the last 30 days you have had two production incidents, then the mean time between failure is 15 days.

<div class="notice--big--primary">

### Calculating MTBF

| Incidents in last 30 days   |          |
|