---
title: "Using Cron Jobs to Run GitHub Actions on a Timer"
categories:
  - Tutorials
toc: true
author: Kumar Harsh

internal-links:
 - running github actions on a timer
 - cron jobs for github actions
 - use cron jobs for timely github actions
 - runnning github actions on timer
excerpt: |
    This tutorial explains how to use cron jobs to schedule and run GitHub Actions workflows on a timer. It covers setting up the cron expressions, creating the workflows, and considerations for using cron in GitHub Actions.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We simplify and speed up software building with containerization. Ideal for automating workflows with GitHub Actions and cron jobs. [Check it out](/).**

[GitHub Actions](https://github.com/features/actions) is a simple solution for setting up build (CI/CD) pipelines for your projects hosted on GitHub. Thanks to GitHub's generous free tier, you can use GitHub Actions in both public and private projects, making GitHub Actions one of the most widely used CI/CD platforms in the industry.

When working with CI/CD pipelines, you may need to set up pipelines to automatically run on set intervals or according to a fixed schedule, such as Unix's popular scheduling utility, [cron](https://en.wikipedia.org/wiki/Cron). Cron-based scheduling is helpful for the following:

* Regular automated tasks, such as generating reports, performing backups, cleaning up temporary files, or executing routine maintenance operations
* CI workflows at specific intervals, such as unit tests or code quality checks on a regular schedule
* Periodic deployments for apps that require scheduled updates, data syncing, or environment provisioning
* Compliance and security checks, such as vulnerability scans, license audits, or security assessments

GitHub Actions supports running workflows on a timer through its [`schedule`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule) trigger. In this article, you'll learn how to use the `schedule` trigger to run GitHub Actions on a timer via cron expressions. You'll also learn about an alternative to the `schedule` trigger to run GitHub Actions on a timer (using the same cron expressions).

## How to Use a Cron Job to Trigger a GitHub Actions Workflow

In this section, you'll learn how to set up a GitHub Actions workflow to run load tests on your deployed API periodically using [K6](https://github.com/grafana/k6), a load-testing tool for apps and APIs. You'll deploy your API on [Render](https://render.com/), a cloud app hosting platform that offers a generous free tier for hobbyists and learners.

To follow along with this tutorial, you need the following:

* A GitHub account (to host your project and run GitHub Actions workflows)
* A Render account (to deploy your project and run load tests on it)

You'll develop and commit the GitHub Actions workflow to your repo directly through the GitHub web app, which means you don't need to worry about setting up a local development environment.

### Fork the Sample Repo and Deploy the API

To get started, fork [this repo](https://github.com/krharsh17/gh-actions-cron) to your GitHub account. Once you fork the repo, you'll see the following set of files in your forked version:

<div class="wide">
![Files in the sample repo]({{site.images}}{{page.slug}}/c2S7oh7.png)
</div>

The repo contains a [Node.js](https://nodejs.org/en/) application that's composed of four files: the `package.json` and `package-lock.json` files are used to manage the dependencies of the app (which is just `express`); the `index.js` file contains the source code of the API (built using `express`); and the `.gitignore` file is used to exclude the `node_modules` folder from being checked into the version control system.

The app (written in the `index.js` file) makes use of `express` to build a simple HTTP server that exposes two GET endpoints: `/` and `/fact`. The API functions as a simple dog facts generator. When a client sends a GET request to the `/fact` route, the API returns a random dog fact from a static array of dog facts stored in the source code. The `/` route returns a `Hello world!` message, similar to a very primitive version of health check endpoints commonly integrated into APIs. This facilitates a swift assessment of their operational status.

Now that you have your own copy of the repo, you can set up deployments for the application by heading over to the [Render dashboard](https://dashboard.render.com/). On the dashboard, click on the **New Web Service** button:

<div class="wide">
![Render dashboard]({{site.images}}{{page.slug}}/H4B08IY.png)
</div>

On the **Create a new Web Service** page, click on **Configure account** under the **GitHub** column on the right and connect the GitHub account where you just forked the repo:

<div class="wide">
![**Create a new Web Service** page]({{site.images}}{{page.slug}}/FSPa81Q.png)
</div>

Once you've connected the account, you will be redirected back to the same page, and you will see a list of your repos. Search for `gh-actions-cron` and click **Connect**:

<div class="wide">
![Searching for the repo]({{site.images}}{{page.slug}}/UpeGoG9.png)
</div>

You are asked to provide some basic details about your app to set up its deployment. Use the following information to complete the form:

* **Name:** gh-actions-cron
* **Region:** Any region closest to your location
* **Build command:** npm i
* **Start command:** node index.js

Leave the rest of the fields blank. When completed, your form will look like this:

<div class="wide">
![Fill out the new web service form]({{site.images}}{{page.slug}}/71cjUmj.png)
</div>

At the bottom of the form, you are asked to choose an instance type to run your app on. You can leave the **Free** instance type as the selected one and select **Create Web Service**:

<div class="wide">
![Choose instance and create web service]({{site.images}}{{page.slug}}/QzD2EeK.png)
</div>

This creates a new web service on the Render platform and starts deploying your app:

<div class="wide">
![Deployment started]({{site.images}}{{page.slug}}/I22EJcQ.png)
</div>

Once the deployment finishes, your page will look like this:

<div class="wide">
![Deployment completed]({{site.images}}{{page.slug}}/pqP8qwu.png)
</div>

Click on the link provided below the web service name and repo to access your API (which, in this case, is `https://gh-actions-cron.onrender.com/`). You'll use this URL to send requests to your API and configure the load tests.

You've now completed all the setup that are needed before you write the workflows that run load tests on your deployed app. Next, you'll learn how to create a new GitHub Actions workflow.

### Create a New GitHub Actions Workflow

To create your GitHub Actions workflow, you need to create a configuration file that K6 uses to set up the right load test for your API.

Head back to your forked repo and click on **Add file > Create new file**:

<div class="wide">
![Create a new file]({{site.images}}{{page.slug}}/nNliVO1.png)
</div>

Name this file `load-test-config-home.js` and paste the following code in it:

~~~{.js caption="load-test-config-home.js"}
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  duration: '1m',
  vus: 50,
  thresholds: {
    http_req_failed: ['rate<0.01'], 
    // to check that http errors are less than 1%
    http_req_duration: ['p(95)<500'], 
    // to check that 95 percent of response times are below 500ms
  },
};

export default function () {
  const res = http.get('https://gh-actions-cron.onrender.com/');   
  // <================ Enter your deployed app's URL here
  sleep(1);
}
~~~

> When working on your local machine, you would normally create the file at the root of your repo and paste the code into it. You would then need to commit and push the file to the main branch of your remote repo.

This script imports the required functions and modules from K6 and defines a set of options to pass to it. Make sure you substitute your deployment's URL in the default function of the script and commit your file to the repo.

Now, it's time to write the workflow. Create a new file (using the same method as shown previously) at `.github/workflows/` and name it `load-test.yaml`. Save the following code in it:

~~~{.yaml caption="load-teste.yaml"}
name: Load test
on:
  schedule:
    - cron: '*/5 * * * *'

jobs:
  load-test-home:
    name: Run load test at /
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run k6 local test
        uses: grafana/k6-action@v0.3.0
        with:
          filename: load-test-config-home.js
~~~

> When working on your local machine, you would normally create the directory `.github/workflows` at the root of your project directory and create the file `load-test.yaml` inside it to save the workflow. You would then need to manually commit and push the changes to the main branch of your remote repo so that GitHub Actions can pick up the newly created workflow file. To keep things simple here, the web UI has been used which directly commits and pushes your workflow file to the remote repo.

This workflow defines one job, `load-test-home`. This job runs a load test for the `/` route of the API. It checks out the code from the repo (to be able to access the `load-test-config-home.js` file you created earlier to load the test options) and makes use of the [`grafana/k6-action`](https://github.com/grafana/k6-action) to run a load test according to the given options.

At the top of the workflow file, you'll notice a `schedule` node under the `on` node. This is how you define the schedule trigger in a workflow. You must pass a [cron expression](https://en.wikipedia.org/wiki/Cron#Cron_expression) to the trigger to configure how often your workflow runs.

A cron expression is a string of five characters, each representing a frequency of reoccurrence in a particular period (such as minutes in an hour, hours in a day, or days in a month). Here's what the five characters in a cron expression signify:

~~~{ caption=""}
┌───────────── minute of the hour (0 - 59)
│ ┌───────────── hour of the day (0 - 23)
│ │ ┌───────────── day of the month (1 - 31)
│ │ │ ┌───────────── month (1 - 12)
│ │ │ │ ┌───────────── day of the week (0 - 6) (Sunday to Saturday)
│ │ │ │ │                       
│ │ │ │ │
│ │ │ │ │
* * * * *
~~~

The expression used in this YAML file is `*/5 * * * *`. This means it runs every fifth minute of the hour, every hour of the day, every day of the month, every month of the year (and every day of the week). The `*/5` signifies it runs every fifth minute starting from the beginning of the hour. To make this possible, the `/` operator is used. The `/` operator helps you create step values in the form of nth minute, hour, or day. There are three other operators that you can use to write cron expressions:

| Operator | Description | Example Usage |
| ---- | --- | ---- |
| `*` | Wildcard for `every` | `* * * * *` runs every minute of every hour of every day of every month |
| `,` | Separator | `2,5 * * * *` runs at the second and fifth minute of every hour every day |
| `-` | Range | `2-5 * * * *` runs from the second through fifth minutes of every hour every day |
| `/` | Step values | `10/5 * * * *` runs at every fifth minute of every hour every day, starting from the tenth minute forward (*ie* the fifth minute of the hour is skipped, but the expression runs on the tenth, fifteenth, twentieth, and so on) |

While cron has a fairly straightforward syntax, sometimes, writing expressions can get complicated. Manually writing an expression like "At the zeroth minute of every zeroth and twelfth hour of the first day of every second month" can be troublesome. To solve this problem, you can make use of the popular online cron expression tool [crontab guru](https://crontab.guru/), which helps you understand your cron expression as you write it.

Here's what the expression "At the zeroth minute of every zeroth and twelfth hour of the first day of every second month" would look like in crontab guru:

<div class="wide">
![crontab guru]({{site.images}}{{page.slug}}/ux2K3DD.png)
</div>

The GitHub Actions runtime supports the standard cron syntax, as shown here. It's important to note that it does not support the nonstandard syntax `@yearly` or `@monthly`, so make sure you don't use them when writing your cron expression.

Coming back to the tutorial, now that you have the `load-test.yaml` file ready, commit it to your repo. Then head over to the **Actions** tab on your forked GitHub repo to see the workflow run:

<div class="wide">
![Workflow run]({{site.images}}{{page.slug}}/Hnn9zKy.png)
</div>

You'll notice that the run says, "Load test #1: Scheduled". This means that it was triggered as part of a schedule. You can click on the run to view its details, including the results of the load test:

<div class="wide">
![Load test results]({{site.images}}{{page.slug}}/mQIqcbb.png)
</div>

This demonstrates a successful schedule and completes the setup of a very simple schedule that triggers a workflow using a cron expression.

## Considerations for Cron

When working with cron in GitHub Actions, there are a few considerations you must keep in mind, including the following:

### The Minimum Interval for Scheduled Events

The minimum interval for scheduling events (via the `schedule` trigger) in GitHub Actions is every five minutes. This is why expressions like `*/4 * * * *` do not give you the desired effect.

### Time Zones

GitHub Actions uses Coordinated Universal Time (UTC) for scheduling, and you need to be mindful of this when writing your cron expressions. For instance, if you run a workflow at 9 a.m. every day in the Indian Standard Time (which is five and a half hours ahead of UTC), you need to use the expression `30 3 * * *' and not '0 9 * * *`.

### Multiple Schedules

There can be multiple schedule triggers for the same workflow. This allows you to combine and use multiple schedules in the same workflow while being able to selectively run jobs on a subset of those schedules as needed.

To understand this better, consider a scenario where you need to add another load test to your API, but this time, it's for the `/fact` endpoint. However, you don't want the test to run every five minutes, as it can be a resource-intensive task for your backend. Additionally, you don't want to create a separate workflow for this test as it only requires one job with two steps, and it would make more sense to add this as another job in the `load-test.yaml` workflow for better maintainability in the future. Here's how you can do it.

Start by creating another file, `load-test-config-fact.js`, in your repo and save the following contents in it:

~~~{.js caption="load-test-config-fact.js"}
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  duration: '1m',
  vus: 50,
  thresholds: {
    http_req_failed: ['rate<0.01'], 
    // http errors should be less than 1%
    http_req_duration: ['p(95)<500'], 
    // 95 percent of response times must be below 500ms
  },
};

export default function () {
  const res = http.get('https://gh-actions-cron.onrender.com/fact');   
  // <======= Enter your deployed app's URL with the fact endpoint here
  sleep(1);
}
~~~

This defines a similar config file as you defined earlier but for the `/fact` endpoint. Next, update the `.github/workflows/load-test.yaml` file to make it look like this:

~~~{.yaml caption="load-test.yaml"}
name: Load test
on:
  schedule:
    - cron: '*/5 * * * *'
    - cron: '*/30 * * * *' # This schedule has been added

jobs:
  load-test-home:
    name: Run load test at /
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run k6 local test
        uses: grafana/k6-action@v0.3.0
        with:
          filename: load-test-config-home.js

  load-test-fact:       # This job has been added
    name: Run load test at /fact
    if: github.event.schedule != '*/5 * * * *'  
    # This job does not run on the 'every fifth minute' schedule
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Run k6 local test
        uses: grafana/k6-action@v0.3.0
        with:
          filename: load-test-config-fact.js
~~~

This YAML file now defines another job `load-test-fact` that runs a load test on the `/fact` endpoint. You'll notice that the `schedule` node now has two cron entries, and the `load-test-fact` job uses an `if` node to skip running when the workflow is triggered by the `*/5 * * * *` schedule. This is how you can use multiple schedules in a workflow.

When triggered by the `every fifth minute` cron expression, your workflow will look like this:

<div class="wide">
![Workflow run]({{site.images}}{{page.slug}}/LXMNIrm.png)
</div>

Notice that the `Run load test at /fact` has been skipped by the workflow.

### Schedule Strictness

One of the biggest downsides of using the `schedule` trigger in GitHub Actions is that [it's not guaranteed](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule:~:text=Note%3A%20The%20schedule,of%20the%20hour.) that the action is executed according to the set schedule, especially in times of high traffic to the GitHub servers. This is why you should never rely on the `schedule` trigger to run critical workflows in your project.

An alternative to this is to use the `workflow_dispatch` event to allow manually triggering your workflows and then trigger it via the GitHub API using external scheduling solutions, such as [IFTTT](https://ifttt.com/), [Google Cloud Scheduler](https://cloud.google.com/scheduler), or even the local crontab on your *nix machine.

Doing that is simple; you just need to add the `workflow_dispatch` trigger to the `on` node in your workflow:

<div class="wide">
![Adding the `workflow_dispatch` event]({{site.images}}{{page.slug}}/eTXquqr.png)
</div>

Now, you can use [the GitHub API](https://docs.github.com/en/free-pro-team@latest/rest/actions/workflows?apiVersion=2022-11-28#create-a-workflow-dispatch-event) to create a workflow dispatch event using the following curl call:

~~~{.bash caption=""}
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <GITHUB_AUTH_TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/repos/<GITHUB_USERNAME>/<GITHUB_REPO_NAME>/actions/workflows/load-test.yaml/dispatches \
  -d '{"ref":"main"}'
~~~

You can [create a new GitHub token (legacy)](https://docs.github.com/en/enterprise-server@3.6/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) in your profile or use the command `gh auth token` to retrieve a token via the [GitHub CLI](https://cli.github.com/) and set the values for your GitHub profile and repo name in the command. You need to save this command in a Bash script file with a name (and location) like `~/load-test.sh`. Finally, you can use the following command to open up your local system's crontab:

~~~{.bash caption=""}
crontab -e
~~~

Then add your Bash script to be executed every minute by adding the following line in your crontab file:

~~~{.bash caption=""}
*/1 * * * * sh ~/load-test.sh
~~~

Save the file, and you'll notice that the workflow is now triggered via the API according to the schedule you have set in your local crontab file:

<div class="wide">
![Locally triggered workflows]({{site.images}}{{page.slug}}/Gz3MJLW.png)
</div>

This appears to be better aligned with the schedule and allows you to run the workflow as frequently as once every minute.

> Note that crontab files make use of the host system's time and calendar settings, not UTC necessarily.

You can also set up the same Bash script to be executed as part of a schedule by any third-party scheduling service, such as [Google Cloud Scheduler](https://cloud.google.com/scheduler) or [IFTTT](https://ifttt.com/), if your local/development machine can't support a schedule around the clock.

## Conclusion

The `schedule` trigger offers a potent solution for automating workflow on a scheduled basis. By integrating scheduling with software builds, you can streamline workflows, automate routine processes, and maintain project consistency. Whether it's regular backups, scheduled deployments, or periodic checks, the combination of cron jobs and GitHub Actions empowers users to efficiently manage their projects.

{% include_html cta/bottom-cta.html %}