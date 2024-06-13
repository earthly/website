---
title: "Updates and Enhancements to the Earthly Cloud UI"
slug: earthly-cloud-ui-updates
categories:
  - news
toc: true
author: Gavin
topcta: false

internal-links:
 - earthly cloud ui
 - updates to the earthly cloud ui
 - enhancements to earthly cloud ui
 - earthly cloud ui more enhanced
excerpt: |
    Earthly Cloud has announced updates and enhancements to its UI, including a revamped home dashboard and a new Build Details screen that provides more information about builds. The Build Details screen includes tabs for overview, timings, graph, and logs, allowing users to easily track the status and performance of their builds.
---

Over the past several months, we've been working on revamping the UI of Earthly Cloud to better meet the needs of our users. Previously, our interface allowed you to view your satellites, their instance details, and status, and you could see build logs, but we knew there was room for improvement. We recognized the need to include build details and received valuable feedback from our users requesting features like build timings and build graphs. Today, we're thrilled to announce a series of updates and enhancements to the Earthly Cloud UI.

## Home Dashboard

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-01.png)\
</div>

The Earthly Cloud home dashboard isn't new, but it's a great entry point to Earthly Cloud's UI. It has an Active Builds section with information about each currently running build and a Builds section with all of the builds across your org represented by visual indicators that make it easy to determine if individual builds were successful, failed, or canceled. If you hover your cursor over any of these build icons, additional details about the build are displayed. Clicking any of these build icons will take you to the new Build Details screen which will be detailed later in this post. The dashboard also has a Satellites section listing all satellites in your org, their status, and instance details.

## New Build Details Screen

The new Build Details screen aims to give you more information about your builds, including what commands were executed, how long different parts of the build took to execute, the build graph, and build logs. It has 4 tabs:  Overview, Timings, Graph, and Logs.

### Overview

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-02.png)\
</div>

The first and default tab is the Overview tab. It is a quick look at the status and performance of a build. It shows details like build status, duration, the percentage of the build that was cached, and a high-level build timeline.

### Timings

#### Target Timings

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-03.png)\
</div>

The second tab is the Timings tab which has 2 sub-tabs. The first is Target Timings. Target Timings show how long each target run as part of the build took to execute. Clicking any of the targets takes you to its Target Detail screen.

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-04.png)\
</div>

The Target Detail screen shows you the build logs for the target next to the commands that were executed for the target.

#### Command Timings

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-05.png)\
</div>

The second sub-tab on the Timings tab is Command Timings. This screen gives a detailed breakdown of how long each command run as part of the build took to execute. Clicking any of the commands takes you to its Target Detail screen with the command you clicked highlighted.

### Build Graph

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-06.png)\
</div>

The third tab on the Build Details screen is the Graph tab. This tab shows a graph visualization of each target run as part of the build and which relied on which others. Clicking any of the targets takes you to its Target Detail screen.

### Build Logs

<div class="wide">
![Image]({{site.images}}{{page.slug}}/earthly-cloud-ui-updates-07.png)\
</div>

The last tab on the Build Details screen is the Logs tab. This shows the logs for your build. If you've ever used Earthly's Cloud logs, this should look very familiar.

## Sign Up for Earthly Cloud and Start Using the New UI Today

[Sign up for Earthly Cloud](https://cloud.earthly.dev/login) to start using the new UI and all of the features included with it. It's available to all Earthly Cloud users. Try it out, then let us know how it works for you and if you have any suggestions for other enhancements to the Earthly Cloud UI that you'd like to see us build.

{% include_html cta/bottom-cta.html %}
