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
last_modified_at: 2023-07-14
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. Interested in efficient, high-quality software development? Earthly can help with that. [Check us out](/).**

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
| ------------- | -------- |
| #1      | Jan 3rd |
| #2     | Jan 25 |

Mean Time Between Failures =

  : 30 days / 2 Incidents = 15 days
</div>

## Mean Time to Recovery (MTTR)

Something funny happens when you start releasing more frequently. You may end up with a higher count of issues in production, but resolving them will happen much faster. If each change is released separately using a continuous delivery model, then recovering gets easier -- often, all that is required is hitting a rollback button.

If you are measuring MTBF, your software may be getting much better, but your numbers will be getting worse. Enter mean time to recovery. Mean time to recovery is just what it sounds like: you start a timer when the incident begins and stop it when production is healthy again - even a simple rollback counts. Average this number across incidents, and you have MTTR. You now have a metric that captures the health of your incidence response process.

<div class="notice--big--primary">

### Calculating Mean Time to Recovery

| Incident #1   |          |
| ------------- | -------- |
| Reported      | 10:00 am. |
| Recovered     | 12:00 pm. |
| Recovery Time | 2 Hours  |

| Incident #2   |          |
| ------------- | -------- |
| Reported      | 10:00 am. |
| Recovered     | 2 days later at 10:00 am. |
| Recovery Time | 48 Hours  |

Mean Time To Recovery =

  : 2 hour + 48 hours / 2 failures = 25 hours

</div>

## Mean Time to Resolve (MTTRe)

<div class="notice--info">

### Acronyms Collision Alert

Mean Time To Resolve, MTTRe, differs from Mean Time To Recover, MTTR, but some resources use MTTR for both. To avoid confusion, ensure you are using the correct terminology for your metric.
</div>

Rolling back to address an incident is a great idea: it's often the quickest way to get things back in a good place. But there are other types of incidents. Imagine your application deadlocks every once in a while, and you have to restart it to unlock. You may have an excellent mean time to recovery, but you've never actually addressed the root cause. This is what MTTRe measures, not the time to get the service back up and running but to resolve the root cause and ensure the problem never happens again.  

The never-happens-again part is hard to achieve but vital. If you are responding quickly but never getting to the root cause, you will be living in a stressful world of constant fire fighting. However, if you are resolving the root cause of each incident, then quality will increase over time.

<div class="notice--big--primary">

### Calculating Mean Time To Resolve

| Incident #3   |          |
| -------------------- | -------- |
| Reported             | day 1    |
| Addressed            | day 1    |
| Root Cause Analysis  | day 2    |
| Root Cause Addressed | day 31   |
| **Resolve Time**       | **30 days**  |

| Incident #4   |          |
| -------------------- | -------- |
| Reported             | day 1    |
| Addressed            | day 1    |
| Root Cause Analysis  | day 2    |
| Root Cause Addressed | day 11   |
| **Resolve Time**       | **10 days**  ||

Mean Time To Resolve =

: 30 days + 10 days / 2 incidents = 20 days

</div>

## Mean Time to Acknowledge (MTTA)

An essential part of good incident management is an on-call rotation. You need someone around to respond to incidents when they occur. Our previous metrics would be unable to differentiate between an incident that took 3 hours to recover from and one that was recoverable in 5 minutes but took two hours and 55 minutes to be acknowledged.  

MTTA highlights this difference. It is a metric for measuring the responsiveness of the on-call person to any alerts.

<div class="notice--big--primary">

### ️Calculating Mean Time To Acknowledge

| Incident #5   |          |
| -------------------- | -------- |
| Reported             | 10 am    |
| Acknowledged         | 10: 05 am    |
| Recovered            | 12:00 pm   |
| **Acknowledge Time**       | **5 minutes**  |

| Incident #6   |          |
| -------------------- | -------- |
| Reported             | 10 am    |
| Acknowledged         | 11: 55 am    |
| Recovered            | 12:00 pm   |
| **Acknowledge Time**       | **115 minutes**  |

Mean Time To Acknowledge =

: 5 minutes + 115 minutes / 2 incidents = 60 minutes

</div>

## Summary

There are many ways to measure the quality of your software as a service product. MTBF, MTTR, MTTRe, and MTTA can each offer a different lens for viewing your software release life cycle. As you improve your Software Development Life Cycle, find ways to collect aggregate metrics like these and choose one or two to target for improvement.

Invest in improving these metrics, and you'll make up for it in time saved fighting fires. Also, focusing on aggregate metrics can be an effective way to move the discussion from blame about specific incidents to a higher-level debate around changing the process to better support the company's goals.

If your build pipeline is taking more than 15 minutes and therefore negatively affecting your metrics, then take a look at Earthly's [free and open build tool](http://earthly.dev/).
