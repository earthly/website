---
title: "Incident Management Metrics"
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
---
## Intro
In 2008, I got my first job at a software as a service company. We released new software onto the production servers monthly and measured quality by counting bugs. We also had account managers who kept us informed of how many large clients seemed upset about the last release.  

Occasionally, when something went wrong, we would do a stability release and spend a month only fixing bugs.  Testing was not a part of our build process but a part of our team: every feature team had quality assurance people who tested each feature before it was released.

Cloud software development has matured since this time. Incident management has become standard practice, and many great metrics exist for measuring release quality.  Let's review some of them.

## MTBF: Mean Time Between Failures
When the software was being released on a fixed timeline, counting the number of bugs per release may have worked. But if it's released many times per week or per day, then this won't work, and another way to measure is required.

Mean-time between failures is a metric from the field of reliability engineering.  Calculating it is simple: it is time over the number of failures that occurred during that time. If in the last 30 days you have had two production incidents, then the mean time between failure is 15 days.

T = some time period 
F = the count of failures 
MTBF = T / F

## MTTR: Mean Time To Recovery
Something funny happens when you start releasing much more frequently. You may end up with a higher count of issues in production, but resolving them will happen much faster. If each change is released separately using a continuous delivery model, then recovering gets easier -- often, all that is required is hitting a rollback button. 

If you are measuring MTBF, your software may be getting much better, but your numbers will be getting worse. Enter mean time to recovery. Mean time to recovery is just what it sounds like, you start a timer when the incident begins and stop it when production is healthy again - even a simple rollback counts. Average this number across incidents, and you have MTTR. You now have a metric that captures the health of your incidence response process. 

Incident #1 = Reported 10:00 am
Incident #1 = Addressed 12:00 pm
Recovery Time = 2 hours

Incident #2 = Reported 10:00 am 
Incident #2 = Addressed  2 days later at 10:00 am 
Recovery Time = 48 hours

Mean Time To Recovery:
48 + 2 / 2 = 25 hours


## MTTRe: Mean Time To Resolve
Rolling back to address an incident is a great idea: it's often the quickest way to get things back in a good place.  But there are other types of incidents. Imagine your application deadlocks every once in a while, and you have to restart it to unlock. You may have a really great mean time to recovery, but you've never actually addressed the root cause. This is what MTTR measures, not the time to get the service back up and running but to resolve the root cause and ensure the problem never happens again.  

The never-happens-again part is hard to achieve but vital. If you are responding quickly but never getting to the root cause, you will be living in a stressful world of constant fire fighting. However, if you are resolving the root cause of each incident, then quality will increase over time.

Incident #3 = Reported day 1
Incident #3 = Addressed day 1
Incident #3 = Root Cause Analysis day 2
Incident #3 = Root Cause Addressed day 31
Resolve Time = 30 days

## MTTA: Mean Time To Acknowledge
An essential part of good incident management is an on-call rotation. You need someone around to respond to incidents when they occur.  Our previous metrics would be unable to differentiate between an incident that took 3 hours to recover from and one that was recoverable in 5 minutes but took two hours and 55 minutes to be acknowledged.  

MTTA would highlight the difference.  It is a metric for measuring the responsiveness of the on-call person to any alerts.

Incident #1 = 
Mean time to acknowledge
calculating

## Summary
There are many ways to measure the quality of your software as a service product. MTBF, MTTR, MTTRe, and MTTA can each offer a different lens for viewing your software release life cycle. As you improve your SDLC, find ways to collect aggregate metrics like these and choose one or two to target for improvement. It is likely that you already have a sense of which area needs improvement in your organization.

Focusing on aggregate metrics can be an effective way to move the discussion from blame about specific incidents to a higher-level debate around changing the process to better support the company's goals. If your build pipeline is taking more than 15 minutes and therefore negatively affecting your metrics, then take a look at Earthly's [open source build tool](http://earthly.dev/).
