---
title: "Making the Most of Concurrency in GitHub Actions"
categories:
  - Tutorials
toc: true
author: Mdu Sibisi

internal-links:
 - concurrency in github
 - making most in github actions
 - using concurrency in github actions
---

The `concurrency` keyword was introduced to [GitHub Actions](https://earthly.dev/blog/github-actions-and-docker/) in early 2021. While there are other ways to control and restrict the number of jobs running (per workflow) at any given time, the `concurrency` keyword is a cleaner solution that can be applied at both the job and workflow levels. Paired with techniques such as workflow triggers, job matrixes, and caching, GitHub Actions gives you all you need to develop a comprehensive concurrency strategy.

A well-implemented concurrency strategy can lead to faster job and workflow execution, increased scalability, and improved resource utilization. However, you need to utilize it efficiently to fully reap its benefits. In this guide, you'll learn about various tactics that you can use to get more performant builds in GitHub Actions with concurrency. You'll also learn about some pitfalls to avoid while doing so.

> Before you dive in, it's important to note that the terms *parallelism* and *concurrency* in the context of GitHub Actions can be viewed synonymously.

## How to Control and Optimize Concurrency in GitHub Actions

Concurrency describes the process of running multiple overlapping and/or unrelated jobs simultaneously—in parallel. Using the `concurrency` key, along with an [expression](https://docs.github.com/en/actions/learn-github-actions/expressions) or a string value, workflows and jobs can be assigned to specific concurrency groups.

By default, GitHub Actions tries to run as many concurrent jobs as possible. It can generate and execute as many as 256 jobs per workflow run. However, this isn't ideal for many use cases or workflows. For example, you may face reference clashes, locking glitches, and version disparities if you don't properly manage the concurrency of your workflows.

To adhere to the [GitHub Actions best practices](https://exercism.org/docs/building/github/gha-best-practices), it's strongly recommended that you formulate a well-defined concurrency strategy. When you're constructing this strategy, make sure you consider the following:

### Optimize Your Workflow Dependencies

Typically, your workflows may have references to files or source code that must be compiled. In fact, it's highly likely that you're using your workflows to compile, build, and deploy projects that have dependencies.

Your workflow and project dependencies are important factors to consider as you're designing your concurrency strategy. If GitHub Actions is instructed to run your workflows unencumbered, it may cause resource and dependency clashes.

There are a few ways to optimize your workflow dependencies and prevent this from occurring. The first involves understanding your dependencies.

#### Identify and Understand Your Dependency

Visualization tools, such as dependency graphs, often go unnoticed by developers despite their significant value. Yet integrating these tools into your documentation is crucial, regardless of the size of your project. Additionally, it's equally important to distinctly pinpoint and chart out pipeline dependencies. This strategic approach streamlines the process of devising your concurrency strategy as it enables you to design it around your dependencies. Consequently, this approach proves instrumental in sidestepping issues related to references.

This means you should spend some time diagramming and/or charting the interconnectedness of your workflows and jobs. Fortunately, GitHub has a large variety of tools to help you document your repositories, including [this diagramming documentation](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams).

#### Use Build Tools That Feature Caching

Most build automation tools, including [Apache Maven](https://maven.apache.org/), come with build dependencies. However, some (including Maven) may not have a dependency or [build caching](https://maven.apache.org/extensions/maven-build-cache-extension/) out of the box. In comparison, build and test tools such as [Earthly](https://earthly.dev/) can optimize the build process by caching dependencies and only build what's absolutely necessary (after the initial build).

If you want to improve how quickly concurrency slots are freed up with each run, you must examine what tools you're using to compile and build your projects through GitHub Actions.

When it comes to [GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners), they inherently download and/or build dependencies each time they're initialized. However, you can configure your workflows and jobs to mimic similar behavior through the GitHub [`cache` action](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows).

#### Enable Caching in GitHub Actions

Manually adding caching to each workflow may not be necessary if you're using one of the GitHub-supported language-specific package managers or builders. Given that most of these tools integrate built-in caching capabilities, you can instruct them to manage caching for you using their corresponding `setup-` action.

Take, for example, [setup-dotnet](https://github.com/actions/setup-dotnet), which scaffolds a .NET CLI environment tailored to your project's requirements. This process encompasses downloading and caching a user-specified version of the dotnet SDK. Additionally, it caches your [NuGet](https://www.nuget.org/) packages, albeit with the stipulation that you need to instruct it to do so using the cache input or cache option.

If you choose to use the `input` option, your code will look like this:

~~~
uses: actions/setup-dotnet@v3.0.1
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}
          cache: true
     
~~~

Or if you elect to use the `cache` option, your code would look more like this:

~~~{.YAML caption=""}
 uses: actions/setup-dotnet@v3.0.1
        with:
          dotnet-version: ${{ env.DOTNET_VERSION }}      
      - uses: actions/cache@v3
        with:
         path: ~/.nuget/packages
~~~

Ultimately, you can decide how much control you want over how your dependencies and reusable files are cached.

Since .NET only uses NuGet as its package manager, there isn't much configuration required. However, languages like [Java](https://www.java.com/) (`setup-java`) and [Node.js](https://nodejs.org/en/) (`setup-node`) have multiple package managers to choose from, and their `cache` options accept the type of package manager as a value:

~~~
- uses: actions/setup-node@v3
  with:
    node-version: 20
    cache: 'npm'
~~~

You can reduce the time needed to execute workflows and enhance concurrency efficiency by properly utilizing caching.

Now that you know how to enable caching, look at other ways to manage and take advantage of concurrency in GitHub Actions.

### Create Dependent Jobs

Creating dependent jobs allows you to interrupt the asynchronous nature of how jobs are run in your GitHub Actions workflow. By defining dependencies between jobs, you gain the ability to orchestrate which jobs should be executed and when they should be triggered. Ultimately, this empowers you to manage the concurrency of jobs within your workflow.

The mechanism to achieve this is the [`needs`](https://docs.github.com/en/actions/using-jobs/using-jobs-in-a-workflow#defining-prerequisite-jobs) keyword (found under `jobs.<job_id>.needs`), which lets you create jobs that only execute when another specified job is complete.

It's important to note that the `needs` expression operates at the job level. To illustrate this, consider a scenario involving two workflows: workflow A and workflow B, both containing three jobs. While workflow A features job dependencies (jobs that use the `needs` expression), workflow B does not. In this setup, both workflows can still operate concurrently. However, the jobs in workflow A execute sequentially, while workflow B's execute in parallel. This particular feature can help prevent reference clashes, represent sequential phases of your pipeline, or make your pipeline more system resource-friendly.

### Consider Setting Up and Utilizing Self-Hosted Runners

The total number of concurrent workflows and jobs you can run is limited by your plan as well as the runners you use. For instance, [GitHub Free users](https://github.com/pricing) are allowed a maximum of twenty non-macOS concurrent jobs and only five macOS concurrent jobs if they're using GitHub-hosted runners. In comparison, GitHub Pro gives you forty concurrent job slots, and GitHub Team gives you sixty. However, both paid plans have a maximum of five concurrent macOS jobs.

For those looking to increase this number, GitHub Enterprise allows you to run 500 total concurrent jobs and 50 concurrent macOS jobs.

You may also find using [self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) to be more ideal, as their usage limits are based on your available capacity. In fact, you can dynamically scale the number of runners and concurrent jobs using [webbooks](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/autoscaling-with-self-hosted-runners).

Ultimately, using self-hosted runners enables you to manage the number of available concurrency slots, which in turn saves money while you maintain full control of your continuous integration, continuous delivery (CI/CD) pipeline. You can further maximize its benefits by adding job matrixes, which you'll learn more about soon.

### Create Dependent Workflows

You can control the concurrency of your orchestrations by creating dependent workflows using the [`workflow_run`](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflow_run) event trigger. This feature allows you to view workflows as different major points of your pipeline as opposed to them representing singular orchestrations. This can potentially boost code reusability and make editing easier.

Additionally, dependent workflows can be executed sequentially, which is important when dealing with workflows that share references. For instance, if you want to create a (unit test) workflow that runs only after a deployment is complete, the first few lines of your workflow file will look like this:

~~~
on:
  workflow_run:
    workflows: [Deploy]
    types: [completed]

~~~

The workflow dependencies are specified in the third line: (`workflows:[Deploy]`). You can have multiple references here, but only one needs to meet the activity type (on the next line) to trigger the current workflow. The `types` parameter specifies what sort of workflow state should trigger your workflow (*ie* `completed`, `in-progress`, or `requested`).

Unfortunately, there's a limit to the number of dependent (sequentially running) workflows. At the time of writing this article, GitHub Actions limits users to three levels. If your workflows have loosely coupled references and dependencies, you should consider them concurrently. This feature should be reserved for situations that require you to run workflows successively.

### Leverage a Workflow Matrix Strategy

Job/workflow matrices work similarly to [method arguments](https://www.w3schools.com/java/java_methods_param.asp) from object-oriented programming languages like Java and C#. They allow you to pass a list of variables to your jobs. Each variable launches a unique job that executes concurrently.

These job/workflow matrices can generate up to 256 job executions per workflow run, and matrices are defined and managed using the [GitHub Action Matrix Strategy feature](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs) (`jobs.<job_Id>.strategy.matrix`). In addition to allowing you to run more concurrent jobs, you can also reduce redundancy and improve the conciseness of your workflow files.

Without matrices, you'd have to create a unique job for each variable you want to perform a task on. This would be wasteful if all the variables/entities fell under a single category. For instance, instead of defining separate jobs for each job runner you need to launch, you can simply define and use an array for all the variables the job needs to perform a task on:

~~~
jobs: 
  build-and-test: #<job_id>
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]

    runs-on: ${{ matrix.os }}     
~~~

GitHub Actions parallelly runs the jobs in this example (for the latest version of Windows, Ubuntu, and macOS). Matrix strategies are particularly useful when you're running a job with (or on) builders or software with multiple version types, as they make testing easier.

The matrix strategy generates a job for each variable in the array. By default, these jobs are run in parallel. However, you can limit the number of concurrent jobs that are running using the `max-parallel` keyword:

~~~
jobs: 
  build-and-test: #<job_id>
    strategy:
      max-parallel: 1    
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        
    runs-on: ${{ matrix.os }}
~~~

Adding `max-parallel: 1` ensures that there is only a single job running at any given time.

In contrast, employing [multidimensional matrix strategies](https://docs.github.com/en/actions/using-jobs/using-a-matrix-for-your-jobs#example-using-a-multi-dimension-matrix), which function similarly to an array of arrays (resembling [jagged arrays](https://learn.microsoft.com/en-us/dotnet/csharp/programming-guide/arrays/jagged-arrays)), may warrant the use of concurrency control. This approach to organizing and executing jobs enhances traceability while still maintaining the benefits of concurrency.

This framework proves advantageous for failure detection and troubleshooting. By utilizing `jobs.<job_id>.strategy.fail-fast`, you can control how your matrix-related jobs handle failures. If set to `true` and a single job in the matrix fails, GitHub abandons all jobs that have not been completed, both pending and in progress. Conversely, if set to `false`, GitHub logs an error and continues executing all the other jobs in the queue.

For the other jobs, you can use `jobs.<job_id>.continue-on-error`, which is a slightly more flexible option than `fail-fast`, as it can be used in a job, [`concurrency`](https://docs.github.com/en/actions/using-jobs/using-concurrency), or matrix strategy context.

When used in conjunction with concurrency groups, the `max-parallel` keyword offers you more nuanced control over how and when your workflows and jobs run.

### Monitor and Optimize Usage

Tracking and monitoring your jobs can prove quite challenging, especially within the context of large-scale applications. Thankfully, GitHub Actions offers a solution by enabling you to conveniently track and monitor your jobs via its user interface.

However, it's worth noting that this functionality is limited to self-hosted runners and those using the GitHub Enterprise plan.

To view runner and job status, click on **Settings** from your repository or the GitHub Enterprise main page:

<div class="wide">
![GitHub **Settings**]({{site.images}}{{page.slug}}/DSStBMR.jpeg)
</div>

Next, expand the **Actions** item on the left panel and click on **Runners**. The main panel displays a list of all your self-hosted or enterprise-level runners. You can view the job activity of each runner by clicking on an individual runner's name:

<div class="wide">
![Runners settings]({{site.images}}{{page.slug}}/QlDCgMy.jpeg)
</div>

The next window reveals a list of queued and in-progress jobs. Similarly to the previous screen, you can get more information about a specific job by clicking on its name:

<div class="wide">
![Screenshot of the individual job]({{site.images}}{{page.slug}}/rJkwZ01.jpeg)
</div>

Once you click on the job's name, it takes you to the **Actions** section, where you can access details related to your job runs. This includes the usage details and the workflow file the job belongs to:

<div class="wide">
![Job usage details]({{site.images}}{{page.slug}}/8LP1NrQ.jpeg)
</div>

You can use this data to inform and fine-tune your concurrency strategy. You should ask yourself questions like the following: Are jobs failing because you're running out of concurrency slots? How long do jobs take to run? Are there any unnecessary, redundant, or dead workflows you should be removing?

By answering these questions, you can refine your workflows and optimize concurrency. For instance, when you find out how long your jobs are taking to run, you can reduce overhead and improve concurrent job utilization using some of the tips and techniques covered (like caching).

## Using Concurrency Groups

[Concurrency groups](https://docs.github.com/en/actions/using-jobs/using-concurrency) in GitHub Actions let you control the parallelism of your pipelines on both a job and a workflow level. Only a single workflow or job in a concurrency group can run at any given time. Concurrency groups can go as far as allowing you to disable concurrency. But why would you want to?

### Why You Need Concurrency Groups

Managing concurrency in GitHub Actions can be arduous, even with tools such as job matrices, caching, and dependent workflows. Ensuring that your parallel processes are performing accordingly takes considerable planning and effort. As previously discussed, it should be approached with the same care as system architecture design. This means diagramming and documenting the connections between your concurrent workflows and jobs.

Concurrency has benefits, but coordinating and synchronizing parallel tasks can feel like performing a complex [domino toppling](https://www.bbvaopenmind.com/en/science/physics/the-physics-of-domino-toppling/) exercise.

You can try to limit the number of jobs running using the `needs` keyword. However, it only works at the job level. This means you can still have multiple workflows (along with their jobs) running concurrently. Consequently, conflicts, such as deadlocks, [race conditions](https://www.techtarget.com/searchstorage/definition/race-condition), data corruption, and version mismatches, can arise as your workflows and jobs compete for resources.

#### Debugging

Concurrency introduces more points of failure. As such, enterprises and developers running hundreds of daily concurrent jobs may find it extremely difficult to troubleshoot, trace, and debug errors related to their pipelines largely because of the transient nature of job runs.

This means that in addition to extensive planning, pipelines that use complex concurrency strategies must be thoroughly tested. This process requires additional time and resources. When weighed against the benefits of concurrency, it may not be worth it.

#### Financial Feasibility

As previously discussed, GitHub Actions imposes restrictions on the number of parallel executions based on your account type and usage limits. If you exceed the allocated concurrency slots, any additional workflows you have are queued and processed when more concurrency slots become available. This can negatively impact the speed and efficiency of your CI/CD pipelines, particularly during peak usage periods when multiple pulls and pushes are executed.

In truth, unless you're using self-hosted runners, there are no advantages to processing simple or short jobs concurrently. It seems that one of the many ways Microsoft has made GitHub so profitable is by fleecing GitHub Enterprise users through [hidden costs](https://betterprogramming.pub/the-hidden-cost-of-parallel-processing-in-github-actions-63f25b2d5f6a).

You're essentially billed for each job you run on a per-minute basis. Your billable time is then rounded up to the next minute. So whether your job takes one minute and two seconds to complete or one minute and forty-nine seconds, you are billed for two minutes. Additionally, the GitHub paid plans have minute and storage limits. If you exceed these limits, you're liable to incur additional costs.

However, the GitHub paid plans offer a plethora of advantages, such as increased security, additional collaborative tools, and scalability. If you do run concurrent jobs constantly, you can use the [GitHub pricing calculator](https://github.com/pricing/calculator) to help you anticipate costs. It's also recommended that you keep a close eye on your usage reports.

### How to Use Concurrency Groups

Along with the `concurrency` keyword, you need to define concurrency groups using the context they're allowed to run under. You can define a concurrency group using the following context expressions:

* [`github`](https://docs.github.com/en/actions/learn-github-actions/contexts#github-context)
* [`inputs`](https://docs.github.com/en/actions/learn-github-actions/contexts#inputs-context)
* [`vars`](https://docs.github.com/en/actions/learn-github-actions/contexts#vars-context)
* [`needs`](https://docs.github.com/en/actions/learn-github-actions/contexts#needs-context)
* [`strategy`](https://docs.github.com/en/actions/learn-github-actions/contexts#strategy-context)
* [`matrix`](https://docs.github.com/en/actions/learn-github-actions/contexts#matrix-context)

If you want to limit workflows to a single run per user, you can use the `github.actor` expression. This scenario might arise when dealing with a repository or project featuring numerous branches. To disable concurrency and limit your runs to a single workflow execution, you would need to add the following line to the top of each YAML/YML workflow file:

~~~
concurrency: ci-${{ github.actor }}
~~~

<div class="wide">
![Forked branch snippet]({{site.images}}{{page.slug}}/3Hsid8C.jpeg)
</div>

This is what your master branch would look like:

<div class="wide">
![Master branch code snippet]({{site.images}}{{page.slug}}/IMaG9R3.jpeg)
</div>

> **Please note:** You can find your `Workflow`/`Actions` file in the `/.github/workflows/` folder of your repository.

After you push or run both workflows, one should be in progress (or queued), and the other should be pending:

<div class="wide">
![Workflow progress]({{site.images}}{{page.slug}}/Hnqzbp0.jpeg)
</div>

Clicking on the pending job's name takes you to a screen with the following message:

<div class="wide">
![Learn more about concurrency]({{site.images}}{{page.slug}}/eamQHaP.jpeg)
</div>

This workflow only starts processing once the workflow on the top of the concurrency group queue has been executed.

This type of concurrency restriction can be applied to all the projects (and their branches) in your repository on both workflow and job levels. Moreover, not only does it apply to different workflow files and runs, but it also prevents duplicate runs of the same workflow file from executing concurrently.

## Conclusion

There are numerous ways to control and optimize the concurrency of your [GitHub Actions CI/CD pipeline](https://earthly.dev/blog/cicd-build-github-action-dockerhub/), and you can't rely on the GitHub Actions default concurrency behavior. It isn't good practice, and it can lead to system resource issues or deadlocking and sluggish pipelines.

Go modules make managing packages in the Go programming language easier.

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images

