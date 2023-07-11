---
title: Migrating Your Open Source Builds Off Of Travis CI
featured: true
categories:
  - Articles
author: Adam
internal-links:
   - travis
   - travis ci
   - travisci
topic: ci
funnel: 2
excerpt: |
    Learn about the recent migration of open-source projects off of Travis CI and discover alternative options for hosting your builds, such as Circle CI and GitHub Actions. Find out why this migration is important for the open-source community and how you can minimize the effort of moving your builds in the future.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

Starting in early December, a mad dash has been underway to migrate open-source projects off of Travis CI. What happened and where should you move your project to?

{% include imgf src="quote1.png" alt="TravisCI is no longer providing open source credits" caption="Jame's Hilliard on Twitter" %}

If you're not familiar with Travis CI, it's a build company that has been powering the continuous integration (CI) of many open source projects since it launched in 2011. &nbsp;It was the first build solution that was free for open source use and that easily integrated into GitHub.

## What Happened?

In 2019 Travis was acquired by a private equity group and many engineers were let go.

<blockquote class="twitter-tweet" data-width="550">
<p lang="en" dir="ltr">So apparently Travis CI is being strip-mined immediately after their acquisition by Idera. Sorry, I mean after "joining the Idera family" 🙄 <a href="https://t.co/CE5ERp1RsY">https://t.co/CE5ERp1RsY</a> A bunch of talented people are waking up to termination letters. Absolutely shameful. <a href="https://t.co/BbBRPdnswe">https://t.co/BbBRPdnswe</a></p>— Senior Oops Engineer (@ReinH) <a href="https://twitter.com/ReinH/status/1098663375985229825?ref_src=twsrc%5Etfw">February 21, 2019</a>
</blockquote>
<script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>

Then, on Nov 2, 2020, Travis CI announced the end of its unlimited support for open-source projects:

> For those of you who have been building on public repositories (on travis-ci.com, with no paid subscription), we will upgrade you to our trial (free) plan with a 10K credit allotment.
>
> **When your credit allotment runs out - we'd love for you to consider which of our plans will meet your needs.** - [Travis CI blog post](https://blog.travis-ci.com/2020-11-02-travis-ci-new-billing)

The reason behind the change is stated to be abuse by crypto-miners:

> However, in recent months we have encountered significant abuse of the intention of this offering (increased activity of cryptocurrency miners, TOR nodes operators etc.).

However, many feel the real reason is that the acquirer is aiming for profitability at all costs and supporting the open-source community represents a significant cost.

> My previous company was on Travis, and as soon as I saw that Travis was purchased by private equity, I knew the downward spiral had begun and I recommended we move to something else. Not surprised that this is happening a couple of years later...my understanding is that private equity will tend towards slowing/stopping development after acquisition to cut costs/headcount, and then squeeze the remaining value from what's left, so this is in-line with that playbook. &nbsp;- [rpdillion on hacker news](https://news.ycombinator.com/item?id=25340486)

## Why It Matters

> The open source movement runs on the heroic efforts of not enough people doing too much work. They need help. - [CLIVE THOMPSON](https://www.wired.com/author/clive-thompson)

Many open-source projects are still using Travis and open-source maintainers are notoriously overworked. &nbsp;Time spent migrating builds is time not spent on other things. &nbsp;Large well-maintained projects will likely quickly transition but for many smaller projects, an abrupt change in a service they depend on is a huge challenge.

## Where To Move To

{% picture content-wide {{site.pimages}}{{page.slug}}/dartboard.png --picture --img width="1200px" --alt {{ Pins on a Map }} %}

If you maintain an open-source project that uses TravisCI and are hoping to get off it, then assuming you have the time to migrate, there are actually many viable options.

### Option: Run Your Own Builds

You can find some [scattered](https://medium.com/google-developers/how-to-run-travisci-locally-on-docker-822fc6b2db2e) [instructions](https://stackoverflow.com/a/35972902) [online](https://stackoverflow.com/a/35972902) for running Travis builds yourself. There are mixed reports on the stability and feasibility of this approach, but if your adventurous, you could try to set up your own Travis CI build executor on your own hardware.

A better option, if you want to run the builds on your own hardware is to look at something like [Buildkite](https://buildkite.com/) or [GitLab CI](https://about.gitlab.com/stages-devops-lifecycle/continuous-integration/https://about.gitlab.com/stages-devops-lifecycle/continuous-integration/).

### Option: Circle CI

A better option is [Circle CI](/blog/continuous-integration#circleci) , a Travis CI competitor which still offers a free plan. &nbsp;

Circle CI offers 400,000 build credits per month to any open-source public repository. &nbsp;This is their free plan and limits concurrency to 1 job at a time. They also have an easy GitHub integration and no application process. &nbsp;

They also allow use of the [free plan](https://circleci.com/open-source/) with private repositories. This makes it a great choice if your project is not actually open-source.

### Best Option: GitHub Actions

{% picture content {{site.pimages}}{{page.slug}}/trophy.png --picture --img width="800px" --alt {{ A Trophy }} %}

An even better option is [GitHub Actions](/blog/continuous-integration#github-actions), a cloud CI system directly from GitHub. &nbsp;GitHub is at the center of many open source projects and this makes it a natural choice for CI. &nbsp;

GitHub Actions (GHA) is newer than either TravisCI or Circle CI, having launched in late 2018.

GHA offers very generous build credits, 20 concurrent build jobs per project and no limit on build time used. &nbsp; If your pipeline can be run in parallel this concurrency can really be a great enabler. &nbsp;The only limitation I was able to find is that the build may last no longer than 6 hours in total.

If your project is hosted on GitHub and is open source then the [GHA open source plan](https://docs.github.com/en/free-pro-team@latest/actions/reference/usage-limits-billing-and-administration) seems like the best bet right now.

### Summary of Open Source Plans

| Service | Open Source Offering |
|