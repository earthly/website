---
title: "Merge Queues: What You Need to Know"
categories:
  - Tutorials
toc: true
author: Carlos Inocencio

internal-links:
 - learn about merge queues
 - what is merge queues
 - introduction to merge queues
 - merge queues for pull requests 
last_modified_at: 2023-09-08
---

What is a Merge Queue, and how to use it? Merge queues (or trains, if you use GitLab) are created in order to arrange multiple pull requests consecutively. Each pull request is individually reviewed before being merged into the target branch. GitHub and GitLab offer in-house solutions for this process, but there are also third-party companies, like [Mergify](https://mergify.com/), that offer this service.

Generally speaking, merge queues are helpful for organizations with high-traffic repositories where merge conflicts occur frequently. In this article, you'll learn all about merge queues, including what they are, when they're helpful, and how to manage them.

## When You Need a Merge Queue

To figure out if merge queues are a good fit for your organization, you need to understand how merges typically operate in Git. For instance, if you have a standard repository with a main branch, by default, creating and merging feature branches is relatively simple. You create a new branch from the main one, modify the code with your feature, create a pull request (PR), and if the code passes every check, you can bring your changes into the main branch:

<div class="wide">
![Simple feature branch diagram, courtesy of Carlos Inocencio]({{site.images}}{{page.slug}}/Cv1tW5O.png)
</div>

> In this diagram (and the following diagrams), every "C" represents a commit in each branch.

When multiple features are in development, each can be merged individually into the main branch regardless of when they were created, as long as they pass the merge checks established in the PR:

<div class="wide">
![Two-feature branch diagram]({{site.images}}{{page.slug}}/vasjR9X.png)
</div>

As more feature branches are created, the possibility of two or more branches conflicting increases. One branch may delete a reference the other needs, causing conflicts in the main branch. Or, if you're running a continuous integration (CI) pipeline, it might not catch the conflict since each PR can merge back to the main branch, but they can implicitly conflict with each other. These types of conflicts are called [syntax and semantic errors](https://www.learncpp.com/cpp-tutorial/syntax-and-semantic-errors/) and are more common with larger groups working on the same codebase.

One possible solution to this issue is to require every feature branch to be "up to date" (*ie* have a linear history) with the main branch before you try to merge it back. This setting ensures that the main branch will remain stable. In this scenario, a developer would have to [rebase the code](https://git-scm.com/docs/git-rebase), pass all the CI checks, and then merge their changes into main:

<div class="wide">
![Two-feature branch rebase diagram]({{site.images}}{{page.slug}}/hXWRtVE.png)
</div>

The primary drawback of this approach is speed. As you run the CI checks for every merge into main, every developer must rebase to the latest head. If several developers try to do this, it becomes a race to rebase and merge before further changes occur.

This might sound like a minor issue, especially if your team is small or if changes to the main branch are not frequent, which is the case for a lot of microservices or small developer teams. However, if having constant merge conflicts or the hassle of continuous "rebases" sounds like a familiar pain point, merge queues can help.

## How a Merge Queue Works

A merge queue, when implemented, is an automation that binds several pull requests into a PR group. It achieves this by looking for a label that indicates the PR is ready to be added to the queue. The exact configuration needed to accomplish this varies from provider to provider.

When enough PRs have been added or enough time has passed since the last merge, it runs the merging process for the group. This approach ensures stability in the main branch without running the checks after every single change.

Once the merging process is complete, the group is merged into a new temporary branch created from the head of the main branch. If any of the PRs in the group fail the CI checks, they're removed from the group, and the rest of the PRs will continue with the merge process:

<div class="wide">
![Merge queue diagram]({{site.images}}{{page.slug}}/f4lr5kk.png)
</div>

This automation means that your developers aren't responsible for constantly staying up to date with the current build of the main branch and can focus their time on modifying the code only when necessary.

Now that you know how merge queues work, it's time to look at the different options available for handling the new code once it reaches the main branch.

### Merge Methods for a Queue

There are several ways PR branches can be merged back into the main branch, including the following:

* **Merge** is the default behavior. It keeps the exact commit history of the changes made in the feature branch and merges it into the main one. Such an approach allows a detailed history of the changes that were made, but it can make the commit history challenging to follow, especially when there are several feature branches.
* In the **rebase** method, before you add the PR, you need to rebase the commits to the head of the main branch. The commit history is linear and easy to follow, but you're essentially rewriting the commit history of the feature branch. When multiple branches share commits, it can make the commit history confusing. However, the drawbacks are typically minimized if you keep feature branches short-lived because they'll only have a few commits to add to the history.
* **Squash** is by far the easiest method to follow; everything done in the feature branch gets condensed into a single commit in the target one. The drawback is that you lose the whole commit history. If something breaks down the line, you'll have a harder time figuring out what happened.

Once you figure out what merge queue method is best for your use case, you need to consider a few other settings that will affect when and how your queue operates.

### Queue Triggers and Configuration

As previously mentioned, the queue needs to know which PRs are ready to be included. The details might differ depending on your provider, but generally, a CI job should run once the PR is created. This first CI job will help reduce the probability of other errors occurring in the pipeline and is generally a shorter job than the full suite of tests required for the merge to the main. Once the job is successful, the PR is marked as ready for the queue.

For the most part, queues are first come, first serve, but different providers could give you more complex rules for the order of inclusion in the queue, like comparing commits in the history.

Another important aspect of merge queues is that they won't run all the time. Your provider will give you the option to wait for a certain number of PRs or a time frame, at which point the group will close and the full suite of tests will run for the whole group.

This small shift might not seem like a big deal, but it offers a significant advantage for your developers. Thanks to this automation, they're no longer solely responsible for their PRs and testing.

In addition to deciding when a PR is ready for the queue and how often your merge queues should run, there are a few other configuration options you need to consider that will vary depending on the project. Let's take a look at a few of these considerations:

* **Build concurrency:** This is only relevant for high-traffic repositories. You need to define how many groups can run in parallel. Parallel runs allow for faster processing of PRs but are more complex since they introduce parallel changes back into the build process.
* **Merge limits:** This was touched upon a bit before, but bears repeating. For most queue providers, you can configure the following aspects:
  * **The minimum number of PRs to include in a group:** This helps avoid running the pipeline all the time and defeating the whole purpose of the groups.
  * **The maximum number of PRs to include in the group:** It's important not to have too many changes at the same time to keep build time manageable.
  * **Wait time:** If, after a specific time, the maximum number of PRs has not been reached, do not make everyone wait indefinitely.
  * **Timeout time:** A lack of success status is likely an issue even if the pipeline has not explicitly failed for a PR in the queue. You should decide how long to wait for a PR to pass the whole test suite before declaring it a failure.
* **Failure response:** A queue's default and most fundamental behavior is that after a PR has failed a test for any reason, the PR is removed from the queue. When the PR is removed, a reason must be given, and the rest of the queue should continue. You can change this behavior and allow for a failed PR to be included in the final merge as long as the last PR in the queue passes all the tests. This is a risky move, but it can reduce rework for your developers if the final result is valid anyway.

These attributes are the most important aspects of configuring a queue for correct functioning. However, depending on the provider, you may have access to other parameters as well. You can find even more information about the types of additional configurations in GitHub's [official documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

## Merge Queue Example

To help illustrate how the lack of a merge queue could affect day-to-day work, let's consider a scenario with an organization that has a very busy repository with three developers—A, B, and C—all working on various features of the app.

Developer A checks out the code and develops a new feature. While that happens, the code changes from another push to the main branch. Developer B checks out the code and develops their own feature. Both developers create a PR and get a green check, as neither breaks the main branch.

Unfortunately, what the two developers don't know is that even though their code is compatible with the main branch, they won't work with each other. When developer B merges to the main branch and developer A merges to the main branch, the resulting code will be incompatible because developer B changed a system that developer A's code depends on. Since developer A never pulled the code again, the app doesn't compile, even though both were "okay" in theory:

<div class="wide">
![Two conflicting branches]({{site.images}}{{page.slug}}/P0ttBGW.png)
</div>

At this point, there are already two conflicting branches, but it's time to introduce developer C. Developer C was asked to deliver a fix for a bug, but the main branch is in an inoperable state, so they have to wait until the error is found, the code is rolled back, or a hotfix is deployed.

Someone could argue that it's developer A's responsibility to pull before merging, which might not be entirely wrong. However, their CI passed its initial tests, and as far as they could tell, it was perfectly fine to proceed.

In this type of scenario, you can see how the "force up-to-date" feature mentioned previously is helpful. With just a click, the repository administrator makes it so that everyone has to be "up to date" with the latest version of the main branch before they can merge.

This works in this hypothetical scenario where three people are contributing, but in a scenario where ten developers are working on the same codebase, the costs only increase. A developer team of that size could easily spend hours of work trying to keep their codebase up to date, only to figure out that someone managed to merge before them, and now they have to run the whole thing again.

### How to Implement a Merge Queue

To avoid the previous scenario, let's implement a merge queue.

If all three developers mark their code as ready to merge after they pass the initial checks against the main branch, the three PRs will be lined up in the queue where the checks are performed incrementally:

<div class="wide">
![Merge queue removes failure]({{site.images}}{{page.slug}}/DqWzuZi.png)
</div>

Here, main+B passes, and main+B+A fails, which means A is removed and main+B+C passes. B and C are merged into the main branch, which never breaks, and developer A gets a log stating the reason for the removal of their PR. Rework and a production-down ticket are avoided, and the developers can keep working on new features instead of hunting down a bug.

As previously mentioned, several different providers provide this functionality, but for simplicity's sake, let's look at how GitHub manages the process.

Queues aren't available for individual contributors, so you'll need an organization. Go to the repository's **Settings** and select **Code and automation** in the sidebar. Click **Branches**, find **Branch protection rules**, and then click **Add rule**. You'll see a field called **Branch name pattern**; put the name of the main branch, and select **Require merge queue**.

And that's all you have to do to create a merge queue. Of course, you can play with the rest of the settings discussed here, but the main setup is done. For more information on merge queues in GitHub, check out the [official documentation](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

## Conclusion

In this article, you learned all about merge queues, including how they operate and when they're helpful. With this information, you're better equipped to decide if merge queues would be a valuable addition to your workflow and how to easily add one.

{% include_html cta/bottom-cta.html %}
