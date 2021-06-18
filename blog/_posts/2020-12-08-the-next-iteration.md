---
title: The Next Iteration of Earthly
featured: true
categories:
  - News
author: Vlad
excerpt: We've been working with many of you to better understand your pains and use-cases when it comes to builds.
internal-links:
  - road map
  - roadmap
---

Dear Earthly community,

We've been working with many of you to better understand your pains and use-cases when it comes to builds.

We have heard that

- Repeatable builds are key
- You like the idea of combining a Makefile with a Dockerfile (the ethos of Earthfiles)
- Integration tests are painful, in general - especially if they only fail in [CI](/blog/continuous-integration)
- Performance is important to you
- Migrating between CI vendors is a pain. However, it's much easier via Earthly, as it can be used as a lift-and-shift framework for builds.
- You would like to complete all your local development flows through Earthly, but for some of you, this is not yet possible (eg run commands directly on the host, use the host Docker daemon, support watch mode)
- You would like it if GitHub Actions + Earthly had some sort of cache, to prevent repeating steps on every build.
- New Apple Silicon launch spurred interest in multi-platform builds
- Many other, finer points

## Roadmap

Following many feedback sessions, we have come up with a number of possible improvements and directions for the Earthly project. We have summarized this in a **roadmap** , which we plan to maintain on an ongoing basis.

[![Roadmap (click to view)]({{site.images}}{{page.slug}}/roadmap.png)](https://github.com/earthly/earthly/projects/1)  
_Roadmap (click to view)_

## What Earthly Needs From You

Feedback, feedback, feedback!

Tell us which of these proposals you would like to see implemented first by up-voting them. Tell us if we're on the right track or if you'd like to suggest improvements. Tell us if there is something else that is bothering you that none of the proposals address.

If you're feeling like you'd like to bounce some ideas, find us on [Slack](https://join.slack.com/t/earthlycommunity/shared_invite/zt-ix9rtuv8-DUFl8uxe5bFULxyCGGbqJQ).

Our #1 priority is making our users happy and productive. There is no other way to achieve this without constant iteration and feedback.

Thank you for being part of the Earthly community!
