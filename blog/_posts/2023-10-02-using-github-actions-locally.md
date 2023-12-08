---
title: "How to Test and Run GitHub Actions Locally"
categories:
  - Tutorials
toc: true
author: Kumar Harsh

internal-links:
 - test and run gitHub actions
 - how to run github actions locally
 - using github actions locally
 - testing github actions locally
 - how does github actions run locally
excerpt: |
    This tutorial explains how to test and run GitHub Actions locally using a tool called `act`. It covers the installation of `act`, exploring its features, and discusses the limitations of using `act` for local GitHub Actions development.
last_modified_at: 2023-10-06
---
**The article explains how act can be used to run GitHub Actions locally. The limitations of that approach lead many towards Earthly. Earthly ensures consistent and reliable builds that run in GitHub Actions and locally. [Check it out](https://cloud.earthly.dev/login).**

[GitHub Actions](https://docs.github.com/en/actions) is GitHub's approach to automating development workflows, enabling you to create, build, test, and deploy software. Additionally, with GitHub Actions, you can build automation around GitHub's offerings, such as triaging GitHub issues and creating GitHub releases.

However, developing a GitHub Actions workflow can be time-consuming. The process involves committing and pushing your changes to your workflows to the remote repository repeatedly to test them. This not only increases the time spent in perfecting your workflows but also adds unnecessary commits and logs to your repo's version history.

Fortunately, several workarounds exist to facilitate local execution and testing of GitHub Actions. For instance, you could use a parallel identical repo to test your workflows before adding them to the main repository, or you could use the official [GitHub Actions Runner](https://github.com/actions/runner) in a self-hosted environment. However, a more seamless and widely used solution is a tool called [`act`](https://github.com/nektos/act) that uses [Docker](https://www.docker.com/) containers to run and test your actions locally. In this article, you'll learn all about `act` and how to use it to quickly build and test GitHub Actions workflows.

## How to Run GitHub Actions Locally

![how]({{site.images}}{{page.slug}}/how.png)\

Before installing `act`, you need to have Docker ([Docker Desktop](https://www.docker.com/products/docker-desktop/) for Mac and Windows, and [Docker Engine](https://docs.docker.com/engine/) for Linux) set up on your system.

You'll also need to [clone this repository](https://github.com/krharsh17/hello-react.git) with the following command:

~~~{.bash caption=">_"}
git clone https://github.com/krharsh17/hello-react.git
~~~

This repository contains a sample React app that was created using [Vite](https://vitejs.dev/) and defines three GitHub Actions workflows. You'll use them later when exploring the `act` CLI.

### Install `act`

Once you've cloned the repository, it's time to install `act` on your system. The specific instructions for various operating systems are available in the [official GitHub documentation](https://github.com/nektos/act#installation).

If you're on a Mac, you can use [Homebrew](https://brew.sh/) to install it by running the following command in your terminal:

~~~{.bash caption=">_"}
brew install act
~~~

To ensure `act` was installed correctly, run the following command:

~~~{.bash caption=">_"}
act --version
~~~

This should print the version of the installed `act` tool:

~~~{.bash caption=">_"}
act version 0.2.49
~~~

This indicates that the tool was installed correctly, and you can proceed to testing the workflows.

> Make sure that Docker is running on the system when using the `act` tool.

### Explore `act`

`act` offers a user-friendly interface for running workflows. You can begin by running the following default command to run all workflows that are triggered by a [GitHub push event](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#push):

~~~{.bash caption=">_"}
act
~~~

If this is the first time you're running the tool, it asks you to choose the default Docker image you'd like to use:

~~~{.bash caption=">_"}
% act
? Please choose the default image you want to use with act:

  - Large size image: +20GB Docker image, includes almost all tools used on GitHub Actions (IMPORTANT: currently only ubuntu-18.04 platform is available)
  - Medium size image: ~500MB, includes only necessary tools to bootstrap actions and aims to be compatible with all actions
  - Micro size image: <200MB, contains only NodeJS required to bootstrap actions, doesn't work with all actions

Default image and other options can be changed manually in ~/.actrc (please refer to https://github.com/nektos/act#configuration for additional information about file structure)  [Use arrows to move, type to filter, ? for more help]
  Large
> Medium
  Micro
~~~

If you want to build complex workflows that make use of multiple actions and other features from GitHub Actions, you should choose the `Large size image`. However, using this image takes up a large amount of your system's resources. In most cases, the medium-sized image is the optimal choice. You can always switch between the image types by updating your `.actrc` file (more on this later).

After you select the image type, you'll notice that all three workflows are triggered (take note of the prefix of each line of the logs):

~~~{.bash caption=">_"}

[Create Release/release       ] 🚀  Start image=catthehacker/ubuntu:act-latest
[Create Production Build/build] 🚀  Start image=catthehacker/ubuntu:act-latest
[Run tests/test               ] 🚀  Start image=catthehacker/ubuntu:act-latest
[Create Release/release       ] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[Run tests/test               ] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[Create Production Build/build] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
...
~~~

All three workflows are triggered because they define the `push` event as their trigger. Some workflows may complete running successfully, while some may fail (due to a lack of some extra configuration that you may need to add to run them locally). In the next section, you'll learn how to use the `act` tool to test various types of workflows.

### Useful Options to Help You Test Various Types of Workflows

In this section, you'll learn of some of the useful options that the `act` CLI offers to help you test various types of workflows and jobs easily.

#### List All Jobs

One of the basic options provided by `act` is `-l`. The `-l` flag enables you to list all jobs in your repository.

Run the following command in the sample repository to view a list of all the jobs in it:

~~~{.bash caption=">_"}
% act -l
Stage  Job ID   Job name  Workflow name            Workflow file       Events
0      build    build     Create Production Build  build-for-prod.yml  push  
0      release  release   Create Release           create-release.yml  push  
0      test     test      Run tests                run-tests.yml       push  
~~~

This code defines the ID and name of the job, the name of the workflow it belongs to, and its file, as well as the events that can trigger it. In repos that have a large number of workflows, this command is helpful to quickly list and find workflows.

#### Run Workflows Triggered by Specific Events

`act` also enables you to trigger workflows on the basis of the event that they're triggered by. As you learned previously, simply running `act` implements all workflows that are set to be triggered by the `push` event. To run workflows associated with any other event, you can run `act <event name>`. Or to run all workflows set to be triggered on a pull request, you can run the following command:

~~~{.bash caption=">_"}
act pull_request
~~~

You'll notice that the tool doesn't print anything because the sample repo doesn't have any eligible workflows.

#### Run Specific Jobs

Apart from running workflows on the basis of their trigger event, you can also run a specific job directly using the `-j` flag followed by the name of the job. For instance, to run the `test` job, you can use the following command:

~~~{.bash caption=">_"}
act -j test
~~~

This runs the `test` job and prints its output on the terminal. Your output looks like this:

~~~{.bash caption=">_"}

[Run tests/test] 🚀  Start image=catthehacker/ubuntu:act-latest
[Run tests/test] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[Run tests/test] using DockerAuthConfig authentication for docker pull
[Run tests/test] 🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Run tests/test] 🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Run tests/test] ⭐ Run Main Checkout
[Run tests/test] 🐳  docker cp src=/Users/kumarharsh/Work/Draft/hello-react/. dst=/Users/kumarharsh/Work/Draft/hello-react
[Run tests/test] ✅  Success - Main Checkout
[Run tests/test] ⭐ Run Main Set up dev dependencies
[Run tests/test] 🐳  docker exec cmd=[bash --noprofile --norc -e -o pipefail /var/run/act/workflow/1] user= workdir=
| 
| added 246 packages, and audited 247 packages in 6s
| 
| 52 packages are looking for funding
|   run `npm fund` for details
| 
| found 0 vulnerabilities
[Run tests/test] ✅  Success - Main Set up dev dependencies
[Run tests/test] ⭐ Run Main Run tests
[Run tests/test] 🐳  docker exec cmd=[bash --noprofile --norc -e -o pipefail /var/run/act/workflow/2] user= workdir=
| 
| > hello-react@0.0.0 test
| > vitest
| 
| 
|  RUN  v0.34.1 /Users/kumarharsh/Work/Draft/hello-react
| 
|  ✓ src/App.test.jsx  (2 tests) 1ms
| 
|  Test Files  1 passed (1)
|       Tests  2 passed (2)
|    Start at  02:56:29
|    Duration  167ms (transform 18ms, setup 0ms, collect 8ms, tests 1ms, environment 0ms, prepare 45ms)
| 
[Run tests/test]   ✅  Success - Main Run tests
[Run tests/test] 🏁  Job succeeded
~~~

#### Do a Dry Run

`act` also allows you to do a dry run of your workflows, meaning you can check the workflow configuration for correctness. However, it doesn't take into account whether the jobs and steps mentioned in the workflow will work at runtime. That means you can't fully rely on dry runs to know if your workflow will perform as expected when deployed. However, it's a good way to find and fix any silly syntactical mistakes. To see this in action, run the following command:

~~~{.bash caption=">_"}
act -j release -n
~~~

Here's what your output looks like:

~~~{.bash caption=">_"}

*DRYRUN* [Create Release/release] 🚀  Start image=catthehacker/ubuntu:act-latest
*DRYRUN* [Create Release/release] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
*DRYRUN* [Create Release/release] 🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
*DRYRUN* [Create Release/release] 🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
*DRYRUN* [Create Release/release] ☁  git clone 'https://github.com/actions/create-release' # ref=v1
*DRYRUN* [Create Release/release] ⭐ Run Main Checkout code
*DRYRUN* [Create Release/release] ✅  Success - Main Checkout code
*DRYRUN* [Create Release/release] ⭐ Run Main Create Release
*DRYRUN* [Create Release/release] ✅  Success - Main Create Release
*DRYRUN* [Create Release/release] 🏁  Job succeeded
~~~

This shows that the workflow is syntactically correct. However, if you try running this workflow using the `act -j release` command, you'll face the following error:

~~~{.bash caption=">_"}
 % act -j release   
[Create Release/release] 🚀  Start image=catthehacker/ubuntu:act-latest
[Create Release/release] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[Create Release/release] using DockerAuthConfig authentication for docker pull
[Create Release/release] 🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Create Release/release] 🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Create Release/release] ☁  git clone 'https://github.com/actions/create-release' # ref=v1
[Create Release/release] ⭐ Run Main Checkout code
[Create Release/release] 🐳  docker cp src=/Users/kumarharsh/Work/Draft/hello-react/. dst=/Users/kumarharsh/Work/Draft/hello-react
[Create Release/release] ✅  Success - Main Checkout code
[Create Release/release] ⭐ Run Main Create Release
[Create Release/release] 🐳  docker cp src=/Users/kumarharsh/.cache/act/actions-create-release@v1/ dst=/var/run/act/actions/actions-create-release@v1/
[Create Release/release] 🐳  docker exec cmd=[node /var/run/act/actions/actions-create-release@v1/dist/index.js] user= workdir=
[Create Release/release] ❗  ##[error]Parameter token or opts.auth is required
[Create Release/release] ❌  Failure - Main Create Release
[Create Release/release] exitcode '1': failure
[Create Release/release] 🏁  Job failed
Error: Job 'release' failed
~~~

This failure occurred because the **Parameter token or opts.auth is required** and was not provided. This value is provided to GitHub Actions workflows by the GitHub Actions Runner automatically on the cloud. However, you need to pass it in manually when using `act`, which you'll learn how to do in the next section.

#### Pass Personal Access Tokens

Some actions in the GitHub Actions workflows, such as interacting with a GitHub API or services, may require a GitHub Personal Access Token (PAT). While the GitHub Actions runtime provides your workflows with a token from your account using the `${{  secrets.GITHUB_TOKEN }}` variable, you need to pass in this value manually to the `act` tool when needed.

To do so, you can pass it in using the `-s` option with the variable name `GITHUB_TOKEN`. You can either directly input your token in the command line or make use of the `gh` CLI by GitHub to retrieve and supply the token on the fly using the following command:

~~~
act -j release -s GITHUB_TOKEN="$(gh auth token)"
~~~

#### Pass Secrets

In the same way you used the `-s` flag to pass in the GitHub token, you can use it to pass other variables as well. Try running the following command to invoke the `release` job and pass in the release description using secrets:

~~~{.bash caption=">_"}
act -j release -s GITHUB_TOKEN="$(gh auth token)" -s \
RELEASE_DESCRIPTION="Yet another release"
~~~

> Running this command may not work for you since your GitHub token doesn't have permission to create releases in the repo you've cloned. To fix that, fork the repo and then clone your fork. After which, this command runs successfully.

### Collect Artifacts

There are workflows that generate or consume artifacts, such as build outputs or executable binaries. GitHub provides a means to upload these artifacts through the [`actions/upload-artifact@v3`](https://github.com/actions/upload-artifact) action to a temporary path in the GitHub Actions runtime where your workflow is running.

However, when it comes to executing and testing workflows locally, there isn't a GitHub Actions runtime available. That means if you try to run the `build` job in the sample repo, it will fail:

~~~{.bash caption=">_"}
% act -j build
[Create Production Build/build] 🚀  Start image=catthehacker/ubuntu:act-latest
[Create Production Build/build] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[Create Production Build/build] using DockerAuthConfig authentication for docker pull
[Create Production Build/build] 🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Create Production Build/build] 🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Create Production Build/build] ☁  git clone 'https://github.com/actions/upload-artifact' # ref=v3
[Create Production Build/build] ⭐ Run Main Checkout repository
[Create Production Build/build] 🐳  docker cp src=/Users/kumarharsh/Work/Draft/hello-react/. dst=/Users/kumarharsh/Work/Draft/hello-react
[Create Production Build/build] ✅  Success - Main Checkout repository
[Create Production Build/build] ⭐ Run Main npm install & build
...[truncated]
| Starting artifact upload
| For more detailed logs during the artifact upload process, enable step-debugging: https://docs.github.com/actions/monitoring-and-troubleshooting-workflows/enabling-debug-logging#enabling-step-debug-logging
| Artifact name is valid!
[Create Production Build/build] ❗  ::error::Unable to get ACTIONS_RUNTIME_TOKEN env variable
[Create Production Build/build] ❌  Failure - Main Archive production artifacts
[Create Production Build/build] exitcode '1': failure
[Create Production Build/build] 🏁  Job failed
Error: Job 'build' failed
~~~

The error message says `ACTION_RUNTIME_TOKEN` is missing. This token provides the workflow instance with access to the GitHub Actions Runner runtime, where it can upload and download files. You can give your local runner environment this ability by passing in the `--artifact-server-path` flag. Here's what the output looks like when you pass in a path using this flag:

~~~{.bash caption=">_"}

% act -j build --artifact-server-path /tmp/artifacts
INFO[0000] Start server on http://192.168.1.105:34567   
[Create Production Build/build] 🚀  Start image=catthehacker/ubuntu:act-latest
[Create Production Build/build] 🐳  docker pull image=catthehacker/ubuntu:act-latest platform= username= forcePull=true
[Create Production Build/build] using DockerAuthConfig authentication for docker pull
[Create Production Build/build] 🐳  docker create image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Create Production Build/build] 🐳  docker run image=catthehacker/ubuntu:act-latest platform= entrypoint=["tail" "-f" "/dev/null"] cmd=[]
[Create Production Build/build] ☁  git clone 'https://github.com/actions/upload-artifact' # ref=v3
[Create Production Build/build] ⭐ Run Main Checkout repository
[Create Production Build/build] 🐳  docker cp src=/Users/kumarharsh/Work/Draft/hello-react/. dst=/Users/kumarharsh/Work/Draft/hello-react
[Create Production Build/build] ✅  Success - Main Checkout repository
[Create Production Build/build] ⭐ Run Main npm install & build
...[truncated]
[Create Production Build/build] 💬  ::debug::A gzip file created for /Users/kumarharsh/Work/Draft/hello-react/dist/vite.svg helped with reducing the size of the original file. The file will be uploaded using gzip.
| Total size of all the files uploaded is 50041 bytes
| File upload process has finished. Finalizing the artifact upload
[Create Production Build/build] 💬  ::debug::Artifact Url: http://192.168.1.105:34567/_apis/pipelines/workflows/1/artifacts?api-version=6.0-preview
[Create Production Build/build] 💬  ::debug::URL is http://192.168.1.105:34567/_apis/pipelines/workflows/1/artifacts?api-version=6.0-preview&artifactName=artifact
[Create Production Build/build] 💬  ::debug::Artifact artifact has been successfully uploaded, total size in bytes: 150909
| Artifact has been finalized. All files have been successfully uploaded!
| 
| The raw size of all the files that were specified for upload is 150909 bytes
| The size of all the files that were uploaded is 50041 bytes. This takes into account any gzip compression used to reduce the upload size, time and storage
| 
| Note: The size of downloaded zips can differ significantly from the reported size. For more information see: https://github.com/actions/upload-artifact#zipped-artifact-downloads 
| 
| Artifact artifact has been successfully uploaded!
[Create Production Build/build] ✅  Success - Main Archive production artifacts
[Create Production Build/build] 🏁  Job succeeded
~~~

The `act` runner is now able to upload the production app artifacts to a storage location on the server. This option can help you test and develop workflows that rely on upload and download actions to complete their process.

### The `.actrc` File

If you find yourself regularly passing too many options into the `act` CLI, you can make use of the `.actrc` file to define the default options and their values that are passed every time the `act` CLI is called. You might recall that during your initial `act` usage, you selected the default container image for local runner execution. The option that you chose was stored in the `actrc` file and is passed into `act` with every call. This is what the `.actrc` file looked like after you chose the default image:

~~~{.bash caption=">_"}
-P ubuntu-latest=catthehacker/ubuntu:act-latest
~~~

You can use this file to load a set of environment variables by default every time you run the `act` CLI, such as passing in the `GITHUB_TOKEN` variable from the `gh` CLI automatically:

~~~{.bash caption=">_"}
-P ubuntu-latest=catthehacker/ubuntu:act-latest
-s GITHUB_TOKEN="$(gh auth token)"
~~~

You can, of course, set more default options using this file. Feel free to explore the [docs](https://github.com/nektos/act#example-commands) for available options that you can set as defaults when running the `act` CLI.

This completes the tutorial on `act`. You can find all the code used here [in this GitHub repo](https://github.com/krharsh17/hello-react).

## Limitations of `act`

![Limitations]({{site.images}}{{page.slug}}/limit.png)\

While `act` is a great tool for setting up a local GitHub Actions workflow development environment, you might run into some issues when working with it. Following are some of the limitations you should be aware of before you get started with it in a project:

* **Limited environment replication:** `act` doesn't fully replicate the GitHub Actions environment by default. It simulates the workflow runs but doesn't provide exact replicas of the GitHub-hosted runner environments. This can lead to discrepancies when actions rely on specific runner configurations or dependencies. You can consider using images by [`nektos/act-environments`](https://github.com/nektos/act-environments) if you need the closest match of GitHub runners. However, note that these images are quite large in size and might still throw unexpected results if your workflow runs into any [other known issues](https://github.com/nektos/act#known-issues).
* **External services and resources:** Actions that interact with external services or resources may not work as expected when run locally with `act`. For instance, services like databases or cloud resources might not be accessible, impacting the behavior of related actions. In such cases, the output logs might not be descriptive enough.
* **Limited OS support:** `act` primarily supports Linux-based containers. Support for Windows and macOS based platforms is [under discussion](https://github.com/nektos/act/issues/97), but it's unclear how long it will take to implement those.
* **Workflow dependency resolution:** Handling workflow dependencies can be challenging with `act`. If your workflow includes cross-repository dependencies or relies on the behavior of other workflows, `act` may not fully support these scenarios. In such a situation, it's best to set up a test GitHub repo with such workflows and test them on it.
* **Custom actions and workflows:** `act` may not fully support custom actions or workflows that are not part of the official GitHub Actions ecosystem. Due to this, some actions may not behave as expected when run locally. If you notice such a situation, it's best to move to a dedicated GitHub repo to be able to access the complete GitHub Actions runner environment when testing.
* **Limited debugging features:** While `act` provides a way to run workflows locally, it doesn't offer the same debugging capabilities as running actions on GitHub, where you can access logs, artifacts, and other diagnostic information easily. You only get the logs that are printed on the terminal as output, and there's no way to access the intermediate or final artifacts of a workflow. Once again, for workflows that heavily rely on these features, it might be best to switch to a dedicated remote testing GitHub repository.

A different approach to testing GitHub Actions locally is to write your workflow as an [Earthfile](https://cloud.earthly.dev/login/) that you run inside GitHub Actions. Earthly's Earthfile's can always be run locally due to containerization.

{% include_html cta/bottom-cta.html %}
