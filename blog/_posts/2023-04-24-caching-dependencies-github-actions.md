---
title: "Caching Dependencies on GitHub Actions"
categories:
  - githubactions
toc: true
sidebar:
  nav: github-actions
author: Cameron Pavey
editor: Bala Priya C
last_modified_at: 2023-06-26
internal-links:
 - cache github actions
 - caching github actions
 - github actions cache
 - github actions caching
excerpt: |
    Learn how to cache your package manager dependencies in GitHub Actions to save time and improve the efficiency of your workflows. This article provides step-by-step instructions on using the `cache` action and explores how caching can be combined with Earthly for even more advanced caching capabilities.
last_modified_at: 2023-07-11
---
**This article explains how to optimize GitHub Actions pipelines using caching. Earthly provides powerful caching capabilities. [Check it out](https://cloud.earthly.dev/login).**

GitHub Actions is a [continuous integration](/blog/continuous-integration), continuous delivery (CI/CD) platform that allows you to build, test, and deploy your code with simple YAML-based configurations. While GitHub Actions, like many other CI/CD platforms, is powerful enough to handle most use cases, it's important to consider the cost and time associated with frequently running workflows.

These issues are especially impactful if you're on a large team with numerous developers and an already lengthy build workflow. In cases like this, you need to try to save time in CI/CD wherever you can.

One way to save time is to cache your package manager dependencies in your GitHub Actions rather than download fresh packages for every workflow you run. In this article, you'll learn how to use the `cache` action to do this and improve the efficiency of your workflows.

## How The GitHub Actions Cache Works

![How]({{site.images}}{{page.slug}}/how.png)\

Initially, caching dependencies for GitHub Actions might seem insignificant, especially when starting a new project or working with a smaller team of developers. However, as your CI workflow grows in size and duration, the prospect of simplifying tasks wherever you can becomes increasingly appealing.

Thankfully, caching package manager dependencies is a quick and easy way to save a nontrivial amount of time on many of your workflow runs. New dependencies will only need to be fetched when you change the installed packages.

Caching dependencies in this way is common practice, so much so that GitHub offers several actions that allow you to set up and cache the dependencies of various popular languages with minimal config. At the time of writing, these actions are as follows:

- **[`setup-node`](https://github.com/actions/setup-node#caching-global-packages-data)** for npm, Yarn, and pnpm
- **[`setup-python`](https://github.com/actions/setup-python#caching-packages-dependencies)** for pip, pipenv, and Poetry
- **[`setup-java`](https://github.com/actions/setup-java#caching-packages-dependencies)** for Gradle and Maven
- **[`setup-ruby`](https://github.com/ruby/setup-ruby#caching-bundle-install-automatically)** for RubyGems
- **[`setup-go`](https://github.com/actions/setup-go#caching-dependency-files-and-build-outputs)** for Go

These actions are a good choice if you work with a supported technology. For everything else, or if you want finer control over the caching process, there is the [`cache`](https://github.com/actions/cache) action, which is what this article will focus on.

### What You Need to Know About GitHub Action Caches

Before diving into the specifics of the `cache` action, it's important to understand the terminology used. GitHub Actions allow for two ways of saving files that originated in a workflow job: *caching* and *artifacts*. Both these mechanisms enable you to store files on GitHub. However, they're not interchangeable and are intended for different use cases.

Caching is a good fit for saving and reusing files that don't change too often such as third-party dependencies. In comparison, artifacts are more suitable for when you want to save and potentially download files that were generated as the output of a job, such as log files, binaries, and application builds. This article will focus only on caching, but it's important to know the difference.

Another thing you need to know prior to starting this tutorial is how access restrictions work for caches. Generally speaking, a workflow run will only be able to access a cache that was created in the current branch, the base branch of a pull request, or the default branch of the repository (or the repository it was forked from).

In practice, this means that if you have a branch called `feature-b` that is based on another branch, `feature-a`, which in turn was based on the default branch `main`, a workflow run in `feature-b` will be able to access caches created in `feature-b`, `feature-a`, and `main`. Whereas a workflow run in `feature-a` will only be able to access caches created in `feature-a` and `main`. You can see a visual representation of this below:

![Diagram of cache control]({{site.images}}{{page.slug}}/rUk6C0W.png)

This is because the cache access restrictions do not allow workflow runs to use caches created in sibling or child branches. Realistically, these restrictions shouldn't impede your use of the caching mechanism, as it's unlikely you would need to pull a cache from a branch other than your current, base, or default branch in most cases.

## Using the Cache Action: `actions/cache@v3`

This section will show you how to configure the `cache` action for a GitHub workflow. As with any other action, there are a few input parameters that you can define to control the behavior of the action. These include the following:

- **`key` (required)** is the key that will be used to identify the cache when it's created. It's also used to search for the cache when looking for an appropriate one to restore.
- **`path` (required)** is the path(s) on the runner that you would like to cache. It will typically point to wherever your dependencies are stored.
- **`restore-keys` (optional)** represents additional keys that GitHub can use to restore your cache if no hits are found for the `key`. Defining this allows for tiered caching, where the `key` is the priority, followed by each of the `restore-keys` in the order they are defined.

After the `cache` action has finished running, it exposes a single output parameter, the `cache-hit`. This parameter is a Boolean value representing whether GitHub found an exact match for the specified `key`. If `true`, this is considered a cache hit, and the action will restore whatever files it has cached to the `path` directory. However, if `false`, a cache miss has happened, and GitHub will create a new cache after the current job. To generate the files that need to be cached, you can use the `cache-hit` output parameter to conditionally run your package manager in case of a cache miss.

### Implementing the Cache

![How]({{site.images}}{{page.slug}}/implement.png)\

To consolidate your understanding of how GitHub Actions caches work, you can follow along with this tutorial to set up a simple Yarn cache in a few minutes.

#### Creating a Project

Start by creating a new project. Because caching is the focus of this exercise, the project itself doesn't matter as long as it has some dependencies to cache. This tutorial will use a simple bare-bones [vite](https://vitejs.dev/) app, which you can create by running the following command:

~~~{.bash caption=">_"}
yarn create vite cache-action-demo --template react-ts
~~~

#### Installing the Required Dependencies

Once your project has been generated, navigate into the newly created `cache-action-demo/` directory and install your dependencies:

~~~{.bash caption=">_"}
cd cache-action demo
yarn install
~~~

This command will trigger the creation of the `yarn.lock` file once the dependencies are installed. This file represents the currently installed versions of your project's dependencies, which you can use to generate an appropriate `key` for your cache action. This approach works because the cache will be rebuilt when the `key` changes, and if the `key` is based on your `yarn.lock` file, it will only change when your dependencies change.

Before configuring the cache action, you should upload your project to GitHub. Create a new repository on GitHub, [and push your local repository to it](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github).

#### Creating a Workflow File

Next, create a new workflow file in your repository by running the following commands:

~~~{.bash caption=">_"}
mkdir -p .github/workflows
touch .github/workflows/cache-action-demo.yml
~~~

##### Creating and Parsing the Config File

In your editor, open the `cache-action-demo.yml` file and add the following content:

~~~{.yml caption="cache-action-demo.yml"}
name: Caching with yarn
on: push
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Get yarn cache directory path
        id: yarn-cache-dir-path
        run: echo "::set-output name=dir::$(yarn cache dir)"

      - name: Cache node modules
        id: cache-yarn
        uses: actions/cache@v3
        env:
          cache-name: cache-node-modules
        with:
          path: $ {% raw %}{{ steps.yarn-cache-dir-path.outputs.dir }}{% endraw %}
          key: ${% raw %}{{ runner.os }}{% endraw %}-build-${% raw %}{{ env.cache-name }}{% endraw %}\
          -${% raw %}{{ hashFiles('**/yarn.lock') }}{% endraw %}
          restore-keys:
            ${% raw %}{{ runner.os }}{% endraw %}-build-${% raw %}{{ env.cache-name }}{% endraw %}-
            ${% raw %}{{ runner.os }}{% endraw %}-build-
            ${% raw %}{{ runner.os }}{% endraw %}-

      - if: ${% raw %}{{ steps.cache-yarn.outputs.cache-hit != 'true' }}{% endraw %}
        name: List the state of node modules
        continue-on-error: true
        run: yarn list

      - name: Install dependencies
        run: yarn install

      - name: Build
        run: yarn run build

~~~

This config is a modified version of the [official npm example](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows#example-using-the-cache-action), tweaked slightly to work with Yarn. The most important part of this file to understand is the `cache-node-modules` step. Here, you can see that the `path` is set to the output of the `yarn cache dir` command from the previous step, which will point to Yarn's local global cache on the runner. Then the `yarn.lock` file is used to generate the hash for the `key`, so if any dependencies change, this hash will also change.

You may also notice the `restore-keys` that use shortening forms of the `key`. Even if GitHub cannot find the hash changes and an exact match, it can still restore the cache to serve as a base for the `Install dependencies` step that will run. When you're defining your `key` and `restore-keys`, you can [make](/blog/makefiles-on-windows) use of any of GitHub's [contexts](https://docs.github.com/en/actions/learn-github-actions/contexts) or [expressions](https://docs.github.com/en/actions/learn-github-actions/expressions).

Using contexts gives you more control over how your keys are created, but for most cases, simply hashing your dependencies or a lock file that represents your dependencies should be more than adequate.

Because you're targeting Yarn's global cache instead of the `node_modules/` directory, you can safely run the `yarn install` command regardless of whether or not a cache miss occurred. If GitHub restores a cache, the install command will run faster than it otherwise would, even if some dependencies still need to be fetched.

If it was restored because of a `restore-key`, and there was no exact match because the `yarn.lock` file has changed, the restored cache can be used for all the unchanged files, and Yarn will download new files for whatever packages have changed since the cache was saved. This is powerful because it means that even on a cache miss, you're still saving time and only downloading the difference. However, this might not be the case for all package managers, so in cases where you don't want a step to run if there is a cache hit, you can add a condition to the step, as seen in the `List the state of node modules` step, which only runs on a cache miss.

#### Committing the Workflow File

You can see this workflow in action by committing the workflow file and pushing it to GitHub:

~~~{.bash caption=">_"}
git add .
git commit -m "add workflow file"
git push
~~~

#### Viewing the Workflow Run

Once the push is complete, navigate to your repository on GitHub and go to the **Actions** tab. You should see your workflow running (or completed). Click on it, and you should see something like this:

<div class="wide">
![Initial workflow]({{site.images}}{{page.slug}}/TjBAYiw.png)
</div>

Here, you can see that the initial `Cache node modules` step could not find a suitable cache (as it is the first run). Consequently, the `Install dependencies` step took seven seconds, as it needed to download all the new packages. Finally, because the workflow was completed without issues, GitHub cached the packages with your specified key.

#### Analyzing Subsequent Workflow Runs

Next, return to your terminal, and run the following command to add and commit a new package:

~~~{.bash caption=">_"}
yarn add axios
git add .
git commit -m "add package"
git push
~~~

In your browser, view the new workflow run, and you should see something like this:

<div class="wide">
![Subsequent workflow run]({{site.images}}{{page.slug}}/ndNd9Q4.png)
</div>

If you compare the cache keys, you will notice that it's restored from your previously created cache even though you added a new dependency. This is because of the aforementioned `restore-keys`. Notably, the `Install dependencies` step was much faster this time, as it only had to deal with one new dependency (and its subdependencies). You can see a new cache was created with a different cache key, confirming that the `yarn.lock` file did indeed change.

## Next Level Caching

GitHub Actions cache can do a great job of holding onto files from previous runs. As we've shown, this means that if your tools are cache aware they can often skip significant amounts of rework. But there are ways to get more aggressive caching done in your GitHub Actions without risky flaky builds from stale cache keys.

You can transform your build to use Earthly.

~~~{.dockerfile caption="Earthfile"}
VERSION 0.7
FROM alpine:latest
WORKDIR /app

build:
  CACHE /app/cache/
  COPY . .
  RUN yarn list
  RUN yarn install
  RUN yarn run build
~~~

And then call Earthly from your Github Action:

~~~{.diff caption="workflow.yml"}
    steps:
      - uses: FranzDiebold/github-env-vars-action@v2
      - name: Checkout code
        uses: actions/checkout@v3
+     - name: Download released earth
+       run: "sudo /bin/sh -c 'wget https://github.com/earthly/earthly/releases/download/v0.7.0/earthly-linux-amd64 -O /usr/local/bin/earthly && chmod +x /usr/local/bin/earthly'"
+     - name: Build Site
+       run: earthly +build
~~~

And with that, most of the GitHub Actions logic can be replaced with Earthly. You can then get caching of yarn dependencies and you'll be able to run the build locally as well.

## Conclusion

In this article, you learned how to configure GitHub Actions workflows to use the `cache` action. This action allows you to save and restore files that don't change very often, like package dependencies, which enable you to speed up your workflow runs, saving you time and money.

If you're using a language that GitHub maintains a `setup-*` action for, you can use that to get a low-config caching solution. Otherwise, if you want more control over the caching process or are using a language that doesn't have first-class support, you can use the `cache` action and get something up and running with a small amount of configuration.

If you're looking for ways to take your caching to the next level consider combining [Earthly with GitHub Actions](/earthly-github-actions). With Earthly you can run your GitHub workflows locally the same way they would run in the cloud, greatly simplifying the process of developing and testing. And you also get layer based caching that can help speed up your builds.

{% include_html cta/gha-cta1.html %}
