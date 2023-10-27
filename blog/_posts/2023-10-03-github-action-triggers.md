---
title: "Exploring GitHub Actions Triggers"
categories:
  - Tutorials
toc: true
author: Ivan Kahl

internal-links:
 - exploring github
 - whats in github action triggers
 - how to use github action triggers
 - github actions triggers
 - working with github actions triggers
excerpt: |
    GitHub Actions is a powerful CI/CD platform that allows you to automate various tasks in your GitHub repository. This article explores different triggers, such as `create`, `delete`, `deployment`, `issues`, `issue_comment`, `page_build`, `pull_request`, `pull_request_review`, `push`, `registry_package`, `release`, `schedule`, `workflow_call`, and `workflow_dispatch`, and provides examples of how to use them to create automated workflows.
last_modified_at: 2023-10-18
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you're dabbling with GitHub Actions, Earthly can simplify your continuous integration workflows. [Give it a whirl](/).**

[GitHub Actions](https://github.com/features/actions) is a continuous integration, continuous delivery (CI/CD) platform by GitHub that lets you automate, build, test, and deploy software directly in GitHub. A key component of GitHub Actions are triggers—events that start off an automated workflow. Triggers make it easy to execute workflows on demand or in response to an event in your GitHub repository.

In this roundup, you'll explore the most common GitHub Actions triggers, see how each is typically used, and look at common mistakes one might make when using each trigger and how to avoid them. By the end, you'll have a solid grasp of how to leverage triggers to create automated workflows in GitHub.

## The `create` Trigger

[Git References](https://git-scm.com/book/en/v2/Git-Internals-Git-References) can be used to point to a particular commit in the repository. This lets you refer to a commit using a memorable name instead of its SHA-1 hash.

Git References are the building blocks of branches and tags. When you create a new branch in your Git repository, a corresponding Git Reference is created. Likewise, when you tag a commit, a Git Reference is created for the tag that points to the commit.

In GitHub Actions, you can use the `create` trigger to start a workflow when a Git Reference is created:

![The `create` trigger is fired when a new branch is created]({{site.images}}{{page.slug}}/bLzECkA.png)

The `create` trigger is also fired when a new tag is created in the repository:

![The `create` trigger is fired when a new tag is created in the repo]({{site.images}}{{page.slug}}/TI88gEC.png)

The following workflow file is activated by the `create` trigger to send an email whenever a new tag is created in the repository:

~~~{.yaml caption=""}
name: Send Email On Tag Creation

on:
  create:

jobs:
  send_email:
    if: {% raw %}${{ contains(github.ref, 'refs/tags/') }}{% endraw %}
    runs-on: ubuntu-latest
    steps:
      - name: Send email
        uses: dawidd6/action-send-mail@v3.8.0
        with:
          server_address: {% raw %}${{ secrets.SERVER_ADDRESS }}{% endraw %}
          server_port: {% raw %}${{ secrets.SERVER_PORT }}{% endraw %}
          username: {% raw %}${{ secrets.MAIL_USERNAME }}{% endraw %}
          password: {% raw %}${{ secrets.MAIL_PASSWORD }}{% endraw %}
          subject: New Tag Created
          to: {% raw %}${{ vars.EMAIL_RECIPIENTS }}{% endraw %}
          from: {% raw %}${{ vars.EMAIL_SENDER }}{% endraw %}
          body: |
            Hi there,

            This is just to let you know that a new tag called \
            {% raw %}${{ github.ref_name }}{% endraw %} in the \ 
            [{% raw %}${{ github.repository }}{% endraw %}] \ 
            (https://github.com/{% raw %}${{ github.repository }}{% endraw %}) repository.

            That's all for now!

            Kind regards,
            Cat
          convert_markdown: true
~~~

The file configures the workflow triggers in the `on` property. The workflow starts when the `create` trigger fires and first checks what kind of Git Reference was created. If the Git Reference starts with `/refs/tags/, then it points to a new tag, and the workflow constructs and sends an email notifying the user that a new tag was created in the repository.

It's important to note that the `create` trigger will [not be fired if you delete more than three tags at once](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#create). For most automation, this won't be an issue. However, depending on your use case, this could be a limitation.

It's also common for developers to forget to check if the `create` trigger is for a new branch or tag. Oftentimes, you only want to execute the workflow for one of the two actions, so remember to add an `if` in your workflow that looks at the `github.ref` variable to determine if a tag or branch was created.

## The `delete` Trigger

You can also trigger a workflow on the `delete` trigger. Like the `create` trigger, this trigger is based on Git References in your repository and is triggered whenever a Git Reference is deleted. A Git Reference is deleted when you delete a tag or branch.

The following snippet adds a comment to a related [Jira](https://www.atlassian.com/software/jira) ticket when a branch is deleted in the repository:

~~~{.yaml caption=""}
name: Add Jira Comment on Branch Deletion

on:
  delete:

jobs:
  add_comment:
    if: github.event.ref_type == 'branch'
    runs-on: ubuntu-latest
    steps:
      # Authenticate with Jira first
      - name: Jira Login
        uses: atlassian/gajira-login@v3
        env:
          JIRA_BASE_URL: {% raw %}${{ secrets.JIRA_BASE_URL }}{% endraw %}
          JIRA_USER_EMAIL: {% raw %}${{ secrets.JIRA_USER_EMAIL }}{% endraw %}
          JIRA_API_TOKEN: {% raw %}${{ secrets.JIRA_API_TOKEN }}{% endraw %}
      # Find the Jira issue ID in the branch name
      - name: Find Jira Key in Branch Name
        id: find_issue_key
        uses: atlassian/gajira-find-issue-key@v3
        with:
          from: branch
      # Add a comment to the issue if found
      - name: Comment on issue
        uses: atlassian/gajira-comment@v3
        with:
          issue: {% raw %}${{ steps.find_issue_key.outputs.issue }}{% endraw %}
          comment: The {% raw %}${{ github.event.ref }}{% endraw %} branch was deleted in GitHub.
~~~

In this code, the workflow makes sure that the `delete` trigger is for a branch using the `if` property. Then it logs into Jira using an API token and finds the ticket key in the branch name. The workflow adds a comment to that Jira ticket mentioning that the branch was deleted in GitHub.

Similar to the `create` trigger, the `delete` trigger is not triggered when deleting more than three tags at once. The workflow also only runs if the workflow file exists on the default branch in GitHub (usually `main` or `master`).

When working with the `delete` trigger, remember to check if the event is for a deleted tag or branch. When using the `delete` trigger, you must use the `github.event.ref` and `github.event.ref_type` variables to get the Git Reference name and type. This is different from the `create` trigger, where you use the standard `github.ref` variable to determine the Git Reference type.

## The `deployment` Trigger

GitHub lets you run workflows when a deployment is created. A deployment can be created on any tag, branch, or commit in your GitHub repository. This tag, branch, or commit can then be deployed in a test or production environment using an external CI/CD pipeline. You can trigger a workflow when a deployment is created using the `deployment` trigger.

The following snippet defines a workflow that gets executed when a new deployment is created. When executed, the workflow sends a notification message on Slack alerting the Slack channel about the new deployment:

~~~{.yaml caption=""}
name: Notify Slack of New Deployment

on:
  # Will trigger this workflow when a new deployment is created
  deployment:

jobs:
  slack-notification:
    runs-on: ubuntu-latest
    steps:
      # Sends slack message to a channel
      - name: Send Slack Message
        uses: archive/github-actions-slack@v2.7.0
        with:
          slack-bot-user-oauth-access-token: 
          {% raw %}${{ secrets.SLACK_BOT_USER_ACCESS_TOKEN }}{% endraw %}
          slack-channel: {% raw %}${{ vars.SLACK_CHANNEL }}{% endraw %}
          slack-text: |
            Hi there 👋🏻

            A new deployment has been created in the {% raw %}${{ github.repository }}{% endraw %} /
            repository on the `{% raw %}${{ github.ref }}{% endraw %}` branch/tag \
            (SHA: `{% raw %}${{ github.sha }}{% endraw %}`).
~~~

When you create a new deployment, you can deploy a branch, tag, or commit.

Please note that if you choose to deploy a commit, then the `github.ref` variable will be null inside your workflow since no Git Reference points to that commit.

Additionally, the `deployment` trigger is used to listen and respond to existing deployment events coming from an internal or external CI/CD pipeline. If you want to create a new deployment, you should start a new deployment in your CI/CD pipeline using a workflow triggered by the `create` or `push` trigger.

Once a deployment starts in your CI/CD pipeline, it sends a request to GitHub to create a deployment, triggering your workflow attached to the `deployment` trigger. Avoid triggering additional deployments in your CI/CD pipeline from a workflow triggered by the `deployment` trigger, as you might end up with recursive, unending deployments in your CI/CD pipeline.

## The `deployment_status` Trigger

Once a deployment has started, you can also trigger workflows when the status updates on the deployment using the `deployment_status` trigger. This can be used to send notifications or create tasks if the deployment succeeds or fails.

The following workflow sends an update message on a Slack channel with the latest deployment status:

~~~{.yaml caption=""}
name: Notify Slack of New Deployment

on:
  # Will trigger this workflow when a deployment status changes
  deployment_status:

jobs:
  slack-notification:
    runs-on: ubuntu-latest
    steps:
      # Sends a Slack message with the updated deployment status
      - name: Send Slack Message
        uses: archive/github-actions-slack@v2.7.0
        with:
          slack-bot-user-oauth-access-token: ${{ secrets.SLACK_BOT_USER_ACCESS_TOKEN }}
          slack-channel: {% raw %}${{ vars.SLACK_CHANNEL }}{% endraw %}
          slack-text: |
            The deployment in the {% raw %}${{ github.repository }}{% endraw %} repository on \
            the `{% raw %}${{ github.ref }}{% endraw %}` branch/tag (SHA: `{% raw %}${{ github.sha }}{% endraw %}`) \
            now has the status: `{% raw %}${{ github.event.deployment_status.state }}{% endraw %}`.
~~~

This workflow posts a status update message to a Slack channel every time the status of a deployment changes. This is useful for monitoring whether a deployment is successful.

Keep in mind that, like the `deployment` trigger, if the deployment does not point to a tag or branch in the repository, then the `github.ref` variable will be empty in the workflow. Additionally, if the deployment status changes to `inactive`, the `deployment_status` trigger won't trigger any workflow.

## The `issues` Trigger

GitHub lets users create issues in repositories to report bugs and suggest features. These issues can then be discussed by maintainers and users until a solution is found.

You can use GitHub Actions to add useful automation to issues using the `issues` trigger. For instance, you may want to automatically create a ticket for an issue in your private project management system, such as Jira. The following workflow demonstrates how to implement this automation:

~~~{.yaml caption=""}
name: Create Jira Ticket for Opened Issue

on:
  # Will trigger the workflow when a new issue is opened
  issues:
    types: opened

jobs:
  create_jira_ticket:
    permissions: write-all
    runs-on: ubuntu-latest
    steps:
      # Authenticate with Jira first
      - name: Jira Login
        uses: atlassian/gajira-login@v3
        env:
          JIRA_BASE_URL: {% raw %}${{ secrets.JIRA_BASE_URL }}{% endraw %}
          JIRA_USER_EMAIL: {% raw %}${{ secrets.JIRA_USER_EMAIL }}{% endraw %}
          JIRA_API_TOKEN: {% raw %}${{ secrets.JIRA_API_TOKEN }}{% endraw %}
      # Create the new Jira ticket
      - name: Create Jira ticket
        id: create_jira_ticket
        uses: atlassian/gajira-create@v3
        with:
          project: TEST
          issuetype: Bug
          summary: {% raw %}${{ github.event.issue.title }}{% endraw %}
          description: {% raw %}${{ github.event.issue.body }}{% endraw %}
      # Add the Jira ticket ID in the issue
      - name: Update issue body
        uses: actions/github-script@v6.4.1
        env:
          owner: {% raw %}${{ github.repository_owner }}{% endraw %}
          repo: {% raw %}${{ github.event.repository.name }}{% endraw %}
          issue_number: {% raw %}${{ github.event.issue.number }}{% endraw %}
          body: {% raw %}${{ github.event.issue.body }}{% endraw %}
          jira_ticket_id: {% raw %}${{ steps.create_jira_ticket.outputs.issue }}{% endraw %}
        with:
          script: |
            github.rest.issues.update({
              owner: process.env.owner,
              repo: process.env.repo,
              issue_number: process.env.issue_number,
              body: process.env.body + "\n\n---\n\n**Jira Ticket ID:** " + \
              process.env.jira_ticket_id
            })
~~~

This workflow is triggered by the `opened` activity type on the `issues` trigger. The GitHub Actions workflow then logs into Jira, creates a new ticket in the Jira project, and saves the Jira ticket ID in the description of the issue so that future automation can locate the Jira ticket.

When using the `issues` trigger in your workflow, it's important to know that the `github.ref` and `github.sha` variables always point to the latest commit on your default branch (usually `main` or `master`). The workflow is also only triggered if the workflow file is on the default branch of the repository. This is particularly important to remember; otherwise, you'll get confused when your workflow doesn't trigger correctly.

[If you look at the documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#issues) for the `issues` event, you'll notice that it has many activity types associated with it. This means you'll probably want to limit which activity types the workflow should run for. You can do this by listing the activity types to run for in the `types` property in the previous workflow, where you define the trigger event.

## The `issue_comment` Trigger

GitHub also lets users discuss issues by commenting on them. This is useful for clarifying missing details for a bug report or planning an implementation for a new feature. In the same way you're able to write automation for issues themselves, you can trigger workflows when comments are left on an issue.

Coming back to the use case of adding your issues to your private project management system, you may also want to send all the comments that were made on the GitHub issue to your project management system, such as Jira. This is easy to accomplish using a workflow that gets triggered by the `issue_comment` trigger:

~~~{.yaml caption=""}
name: Add Jira Comment for Issue Comment

on:
  # Will trigger the workflow when a new comment is created on an issue
  issue_comment: 
    types: created

jobs:
  create_jira_comment:
    if: {% raw %}${{ !github.event.issue.pull_request }}{% endraw %}
    runs-on: ubuntu-latest
    steps:
      # Authenticate with Jira first
      - name: Jira Login
        uses: atlassian/gajira-login@v3
        env:
          JIRA_BASE_URL: {% raw %}${{ secrets.JIRA_BASE_URL }}{% endraw %}
          JIRA_USER_EMAIL: {% raw %}${{ secrets.JIRA_USER_EMAIL }}{% endraw %}
          JIRA_API_TOKEN: {% raw %}${{ secrets.JIRA_API_TOKEN }}{% endraw %}
      # Retrieve ticket ID from the issue body
      - name: Get Jira Ticket ID
        id: get_jira_ticket_id
        uses: atlassian/gajira-find-issue-key@v3
        with:
          string: {% raw %}${{ github.event.issue.body }}{% endraw %}
      # Create the new Jira comment
      - name: Create Jira comment
        uses: atlassian/gajira-comment@v3
        with:
          issue: {% raw %}${{ steps.get_jira_ticket_id.outputs.issue }}{% endraw %}
          comment: |
            {% raw %}${{ github.event.comment.user.login }}{% endraw %} said: 
            
            {% raw %}${{ github.event.comment.body }}{% endraw %}
~~~

This workflow gets triggered by any new comments that are created on an issue. It does this by subscribing to the `created` activity type on the `issue_comment` trigger. When the workflow runs, it also checks to make sure that the comment was left on an issue and not a pull request. The reason for this is that issues and pull requests are very similar in certain places, such as the API, and you can access comments on both using the same webhook or event. The workflow then logs into Jira, uses the body of the current issue to find the Jira ticket ID, and then adds a comment to that Jira ticket with the contents of the GitHub comment in the Jira comment.

Similar to the `issues` trigger earlier, the `issue_comment` trigger only runs if the workflow file is on the default branch in your repository. The `github.sha` and `github.ref` variables in the workflow also always point to the default branch.

Finally, as you can see, it's important to see whether the comment was left on an issue or a pull request. You probably only want to build automation for issue comments *or* pull request comments, not both.

While the `issue_comment` trigger has fewer activity types than the `issues` trigger, it's still a good idea to specify exactly which activity types your workflow should react to using the `types` property.

## The `page_build` Trigger

Most repositories require some form of documentation or marketing so that other developers can learn about the project and how to implement it. GitHub offers [GitHub Pages](https://pages.github.com/), which lets you create static websites for your repositories. You can either use one of the predesigned templates or upload your own static site.

Typically, your GitHub Pages files would sit on a different branch in your repository (*ie* the `pages` branch), or you would store the static site files in a subdirectory in your repository (*ie* `.docs`).

When you push new changes to the branch used for GitHub Pages in your repository, GitHub fires a `page_build` trigger that can start a workflow every time your GitHub Pages are deployed.

An instance where the `page_build` event comes in handy is to trigger email notifications to various recipients every time the static website is deployed. This could serve the purpose of allowing recipients to test the new website or serve as a reminder for them to share it in their workflows. The following workflow achieves this:

~~~{.yaml caption=""}
name: Send Email on Page Build

on:
  # Will trigger the workflow when a new GitHub Pages build occurs
  page_build: 

jobs:
  send_email:
    runs-on: ubuntu-latest
    steps:
      # Sends an email using SMTP
      - name: Send email
        uses: dawidd6/action-send-mail@v3.8.0
        with:
          server_address: ${{ secrets.SERVER_ADDRESS }}
          server_port: ${{ secrets.SERVER_PORT }}
          username: ${{ secrets.MAIL_USERNAME }}
          password: ${{ secrets.MAIL_PASSWORD }}
          subject: GitHub Pages Build Executed with Status of \
          {% raw %}${{ github.event.build.status }}{% endraw %}
          to: {% raw %}${{ vars.EMAIL_RECIPIENTS }}{% endraw %}
          from: {% raw %}${{ vars.EMAIL_SENDER }}{% endraw %}
          body: |
            Hey,

            Just thought to let you know that a GitHub Pages build ran on \
            the ${{ github.repository }} repository. The build executed with \
            the following result: ${{ github.event.build.status }}.

            Please navigate to GitHub to see more.

            All the best,
            Cat
          convert_markdown: true
~~~

Here, you specify that the workflow should be triggered by the `page_build` trigger in the `on` property. The workflow then runs a job that creates an email notifying recipients that a new GitHub Pages build ran and sends it using an SMTP server.

When using the `page_build` trigger for your workflow, the `github.sha` variable always points to the latest commit on your default branch (either `main` or `master`), and the `github.ref` variable is empty. It's important to keep this in mind if your workflow needs to interact with any of the branches or commits in your repository after being triggered by the `page_build` trigger. Similar to other workflows, this trigger only runs the workflow if the workflow file exists on the default branch of your repository.

Another thing to note is that there are no activity types associated with this event, meaning you can't specify that the workflow should only be run when GitHub Pages are successfully built (or fail). However, you can use the `github.event.build.status` variable in your workflow to see if the build was successful.

## The `pull_request` Trigger

Pull requests make it easy for different users to collaborate on source code in a repository. They allow each user to develop on their own branch and then pull those changes into one of the main branches of the repository. When pulling changes into the repository's main branches, a pull request is created that often needs to be approved by other contributors in the repository.

There are several reasons you might want to configure automation on a pull request. You may want to update the status of a task in your project management system when a pull request is opened for that ticket, delete a branch when a pull request is accepted and merged, or notify other contributors of the new pull request when it's created. The following workflow file is triggered by the `pull_request` trigger:

~~~{.yaml caption=""}
name: Notify Slack of Pull Request Actions

on:
  # Will trigger the workflow whenever a pull request is opened or 
  # a review is requested
  pull_request: 
    types: [opened, review_requested]

jobs:
  send_opened_notification:
    # Will run this job when a pull request is opened.
    if: {% raw %}${{ github.event.action == 'opened' }}{% endraw %}
    runs-on: ubuntu-latest
    steps:
      - name: Send Slack Message
        uses: archive/github-actions-slack@v2.7.0
        with:
          slack-bot-user-oauth-access-token: \
          {% raw %}${{ secrets.SLACK_BOT_USER_ACCESS_TOKEN }}{% endraw %}
          slack-channel: {% raw %}${{ vars.SLACK_CHANNEL }}{% endraw %}
          slack-text: |
            {% raw %}${{ github.event.pull_request.user.login }}{% endraw %} opened a new \
            pull request titled: "{% raw %}${{ github.event.pull_request.title }}{% endraw %}". \
            You can view the pull request \
            [here]({% raw %}${{ github.event.pull_request.url }}{% endraw %}).
  send_review_requested_notification:
    # Will run this job when a review is requested for a pull request
    if: {% raw %}${{ github.event.action == 'review_requested' }}{% endraw %}
    runs-on: ubuntu-latest
    steps:
      - name: Send Slack Message
        uses: archive/github-actions-slack@v2.7.0
        with:
          slack-bot-user-oauth-access-token: \
          {% raw %}${{ secrets.SLACK_BOT_USER_ACCESS_TOKEN }}{% endraw %}
          slack-channel: {% raw %}${{ vars.SLACK_CHANNEL }}{% endraw %}
          slack-text: |
            {% raw %}${{ github.event.sender.login }}{% endraw %} requested \
            {% raw %}${{ github.event.requested_reviewer.login }}{% endraw %} review the pull \
            request titled: "{% raw %}${{ github.event.pull_request.title }}{% endraw %}". You \
            can view the pull request \
            [here]({% raw %}${{ github.event.pull_request.url }}{% endraw %}).
~~~

You'll notice that there are two activity types associated with the `pull_request` trigger and two jobs in the workflow. If the `pull_request` trigger's activity type is `opened`, the first job will execute, and the workflow sends a Slack message to a channel of contributors mentioning that a new pull request has been created. The second activity type the workflow subscribes to on the `pull_request` trigger is the `review_requested` type. This occurs when a user requests another user in the repository to review the pull request. In this case, the second job in the workflow is triggered, which sends a Slack message asking a particular user to review the pull request.

When a workflow is triggered by the `pull_request` trigger, the `github.ref` variable points to the latest commit of the merge branch for the pull request, which is called `refs/pull/:prNumber/merge`, and the `github.sha` variable points to the latest Git Reference of the merge branch in the `github.ref` variable. Additionally, if you create a pull request but the pull request has merge conflicts in it that need to be resolved, the conflicts need to be resolved before the workflow runs.

There are several activity types associated with the `pull_request` trigger that you should be aware of. It's good practice to always specify exactly which activity types your workflow should be triggered by. You can see a full list of all the activity types [in the official GitHub documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull_request).

## The `pull_request_review` Trigger

When you create a pull request and another user reviews it, a `pull_request_review` trigger is fired when that user submits their review. A review can either approve, request changes, or reject a pull request.

You can build an automation that performs certain logic when a pull request is reviewed. For instance, you may want to add another reviewer to a pull request if a reviewer rejects it, ensuring that the rejection is warranted. Alternatively, you could automatically close a pull request that's rejected by multiple reviewers or send a notification to the pull request author once a reviewer completes their review.

The following workflow file sends a Slack message notifying the author of a pull request that a reviewer has submitted their assessment of the pull request:

~~~{.yaml caption=""}
name: Notify Slack of Pull Request Review

on:
  # Will trigger the workflow when a review is submitted for 
  # the pull request
  pull_request_review: 
    types: submitted

jobs:
  send_review_submitted_notification:
    runs-on: ubuntu-latest
    steps:
      # Sends a Slack message to a channel
      - name: Send Slack Message
        uses: archive/github-actions-slack@v2.7.0
        with:
          slack-bot-user-oauth-access-token: \
          {% raw %}${{ secrets.SLACK_BOT_USER_ACCESS_TOKEN }}{% endraw %}
          slack-channel: {% raw %}${{ vars.SLACK_CHANNEL }}{% endraw %}
          slack-text: |
            {% raw %}${{ github.event.review.user.login }}{% endraw %} has submitted a review \
            for {% raw %}${{ github.event.pull_request.user.login }}{% endraw %}'s pull request \
            titled: "{% raw %}${{ github.event.pull_request.title }}{% endraw %}". You can view \
            the pull request [here]({% raw %}${{ github.event.pull_request.url }}{% endraw %}).
~~~

The file specifies that the workflow should be triggered on the `submitted` activity type of the `pull_request_review` trigger. The workflow then sends a neatly formatted message to a Slack channel.

When the `pull_request_review` trigger is fired, the `github.ref` variable points to the merge branch for the pull request called `refs/pull/:prNumber/merge`. The `github.sha` variable points to the most recent commit on the merge branch.

Please note that GitHub Actions won't run in forked repositories by default. The user that owns the forked repository [needs to enable it](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#workflows-in-forked-repositories-1).

Additionally, note that on a public GitHub repository, pull requests from forked repositories by [first-time contributors need a user with write access to the main repository](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#pull-request-events-for-forked-repositories-1) so that they can approve the workflow for that pull request.

A common mistake is to look at the activity type that triggered the workflow to determine if the pull request review was approved. However, whenever a review is submitted, approving or rejecting the pull request, the activity type is always `submitted`. If you want to see if the review was approved or rejected, use the `github.event.review.state` variable in the workflow.

## The `push` Trigger

The `push` trigger is fired when you push a commit or tag to the repository. This includes actions such as publishing a new branch from your local repository to GitHub, tagging a commit locally and pushing that tag to GitHub, creating a release in GitHub that creates a tag, or merging a pull request. Any change to the source code in a Git repository executes the `push` trigger.

Because the `push` trigger executes when any code is changed, it's one of the more common triggers you'd use to run a build or deployment pipeline. You can also use the `push` trigger to run automated tests on the code in the repository every time changes are made.

The following workflow file demonstrates how you can deploy a website to [Vercel](https://vercel.com/) every time a new change is pushed to the `master` branch:

~~~{.yaml caption=""}
name: Deploy to Vercel on Push

on:
  # Will trigger the workflow whenever a commit is pushed to
  # the master branch
  push:
    branches: [master]

jobs:
  deploy_to_vercel:
    permissions: write-all
    runs-on: ubuntu-latest
    # Skips the job if the string "[skip ci]" is present in the 
    # commit message
    if: {% raw %}${{ !contains(github.event.head_commit, '[skip ci]') }}{% endraw %}
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: BetaHuhn/deploy-to-vercel-action@v1.9.12
        with:
          GITHUB_TOKEN: {% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}
          VERCEL_TOKEN: {% raw %}${{ secrets.VERCEL_TOKEN }}{% endraw %}
          VERCEL_ORG_ID: {% raw %}${{ secrets.VERCEL_ORG_ID }}{% endraw %}
          VERCEL_PROJECT_ID: {% raw %}${{ secrets.VERCEL_PROJECT_ID }}{% endraw %}
~~~

This workflow is configured to run whenever a `push` trigger is fired on the `master` branch. The workflow then checks out the latest commit on the `master` branch and deploys it to Vercel using another GitHub Action.

It's important to note that a workflow will not run for the `push` trigger if more than three tags are pushed at a time. When the workflow runs, the `github.ref` variable points to the branch on which the push occurred (or the default branch if the branch was deleted), and the `github_sha` variable points to the latest commit referenced by the `github.ref` variable.

While the `push` trigger doesn't have any activity types, there are a number of filters you can use with the trigger to ensure you only run workflows for the correct changes. You can choose to trigger a workflow when files are changed on a certain branch, when files are changed in a certain directory in the repository, or when a certain tag is updated. You can also combine the previous filters so that a workflow only executes when, for example, the files are changed in a certain directory on the `master` branch. You have very granular control with this trigger.

## The `registry_package` Trigger

GitHub Packages lets you host software packages for different package managers, such as [npm](https://www.npmjs.com/), [RubyGems](https://rubygems.org/), [NuGet](https://www.nuget.org/), [Docker](https://www.docker.com/), [Apache Maven](https://maven.apache.org/), and [Gradle](https://gradle.org/). This lets you host your source code and redistributable packages in one place.

GitHub Actions can be run using the `registry_package` trigger. This trigger executes whenever a new package or package version is published to GitHub Packages or when an existing package version is updated. This lets you write automation that should occur after a new package version is created.

The following snippet demonstrates an automation that creates a Jira ticket every time a package version is published or updated so that the developers can update any related documentation:

~~~{.yaml caption=""}
name: Create Jira Ticket for New Package Release

on:
  # Will trigger the workflow when a package is published or updated 
  # in the GitHub Registry
  registry_package: 
    types: [published, updated]

jobs:
  create_jira_ticket:
    runs-on: ubuntu-latest
    steps:
      # Logs into Jira
      - name: Jira Login
        uses: atlassian/gajira-login@v3
        env:
          JIRA_BASE_URL: ${{ secrets.JIRA_BASE_URL }}
          JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
      # Creates a new Jira ticket for the package
      - name: Create new Jira ticket
        uses: atlassian/gajira-create@v3
        with:
          project: TEST
          issuetype: Task
          summary: Update package documentation for \
          {% raw %}${{ github.event.registry_package.name }}{% endraw %} \
          {% raw %}${{ github.event.registry_package.package_version }}{% endraw %}
          description: A new version, \
          {% raw %}${{ github.event.registry_package.package_version }}{% endraw %} \
          was released and the documentation needs to be updated for the \
          new package.
~~~

This workflow subscribes to `published` and `updated` activity types on the `registry_package` trigger. It then logs into Jira and creates a new ticket with details about the new package version that was published or updated, along with a note that related documentation needs to be updated.

When publishing a package, it's usually related to a release in the repository. Since releases generate tags in GitHub, the `github.sha` variable points to the commit that's tagged for that release, and the `github.ref` points to the tag or branch that contains the commit for that release. The workflow also runs only if the workflow file is located in the default branch of the repository (usually `master` or `main`).

There's also an [edge case](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#registry_package) that you should be aware of that might occur while pushing Docker containers to GitHub Packages.

## The `release` Trigger

GitHub lets you create releases in your repository by tagging commits that contain production-ready code. These releases contain a snapshot of the source code at that commit, along with any precompiled binary files.

When a release is created, you may need to trigger a build or deployment pipeline that then deploys that release to a server. You could even send out an email to a mailing list alerting them of the new release.

The following workflow listens to the `release` trigger so it can notify subscribers:

~~~{.yaml caption=""}
name: Send Release Email

on:
  # Will trigger the workflow when a new release is published 
  # in the repository
  release:
    types: [published]

jobs:
  send_release_email:
    runs-on: ubuntu-latest
    steps:
      # Sends an email using SMTP
      - name: Send email
        uses: dawidd6/action-send-mail@v3.8.0
        with:
          server_address: {% raw %}${{ secrets.SERVER_ADDRESS }}{% endraw %}
          server_port: {% raw %}${{ secrets.SERVER_PORT }}{% endraw %}
          username: {% raw %}${{ secrets.MAIL_USERNAME }}{% endraw %}
          password: {% raw %}${{ secrets.MAIL_PASSWORD }}{% endraw %}
          subject: New Tag Created
          to: {% raw %}${{ vars.EMAIL_RECIPIENTS }}{% endraw %}
          from: {% raw %}${{ vars.EMAIL_SENDER }}{% endraw %}
          html_body: file://emails/new_release.html
~~~

This workflow file specifies that the workflow should run on the `published` activity type in a `release` trigger. When the workflow starts, it sends an email to a list of recipients using an email template designed for new releases, which is stored in the repository.

It's important to note that some of the activity types won't trigger if you create a draft release. These include the `created`, `edited`, and `deleted` activity types. The `prereleased` activity type will also not trigger if you publish a prerelease from a draft release. However, in this case, the `published` activity type will trigger. You can find out more about which activity types are triggered [in this documentation](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#release).

Since there are a number of activity types, it's a good idea to specify exactly which activity type should trigger your workflow. Oftentimes, you'll use the `published` activity type to perform some sort of action after a release, but there are other times when you might need to automate another part of the release process. Be sure to look at [all the available types](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#release).

## The `schedule` Trigger

There may be times you need to execute a task on a schedule outside of any other events that might occur. This is where the `schedule` trigger comes in. It lets you schedule when to run a workflow based on a cron expression.

The following workflow is scheduled to run every 6 a.m.:

~~~{.yaml caption=""}
name: Mark Stale Branches

on:
  # Will trigger the workflow every day at 6am using a cron schedule
  schedule: 
    - cron: 0 6 * * *

jobs:
  mark_stale_branches:
    permissions: write-all
    runs-on: ubuntu-latest
    steps:
      # Action that goes through all branches and mark branches older 
      # than 30 days as stale
      - name: Mark Stale Branches
        uses: crs-k/stale-branches@v3.0.0
        with:
          repo-token: {% raw %}${{ secrets.GITHUB_TOKEN }}{% endraw %}
          days-before-stale: 30
          days-before-delete: 90
~~~

In the `on` property, you specify the cron expression for the workflow. You can use a tool like [Cronhub](https://crontab.cronhub.io/) to construct the expression. Once the workflow runs, it goes through all the branches in the repository and marks as stale any branch that hasn't received a new commit in the last thirty days. If a branch hasn't received a commit in over ninety days, it's deleted.

Workflows triggered by a `schedule` trigger run in the UTC time zone. Additionally, the workflow runs on the default branch in your repository. The shortest interval you can configure between workflow executions is five minutes.

When creating a scheduled workflow, it's a good idea to test it manually instead of waiting for the cron schedule to run. To do so, you can add the `workflow_dispatch` trigger (see more later) in the `on` property so you can trigger the workflow manually to test while developing it. Also, remember that cron expressions always run in UTC, so take into account time zone differences and daylight savings when scheduling the workflow.

## The `workflow_call` and `workflow_dispatch` Trigger

GitHub Action workflow files can quickly become large. This is where the `workflow_call` trigger can help. It lets you split your workflows into multiple files. Then you can call a workflow from within another workflow. The `workflow_dispatch` trigger is similar, except it lets you manually trigger a workflow from the GitHub UI or GitHub CLI.

The following workflow file contains a workflow that can be called manually from the GitHub UI or CLI (using the `workflow_dispatch` trigger) or from another workflow (using the `workflow_call` trigger):

~~~{.yaml caption=""}
name: Create Jira Ticket Workflow

on:
  # Will trigger the workflow when called from another workflow. 
  # The other workflow will pass in inputs and secrets.
  workflow_call:
    inputs:
      issuetype:
        description: Issue Type
        type: string
        required: true
      summary:
        description: Summary
        type: string
        required: true
      description:
        description: Description
        type: string
        required: false
        default: 'No description'
    secrets:
      JIRA_BASE_URL:
        required: true
      JIRA_USER_EMAIL:
        required: true
      JIRA_API_TOKEN:
        required: true
  # Will trigger the workflow when called manually from the 
  # GitHub UI or GitHub CLI
  workflow_dispatch:
    inputs:
      issuetype:
        description: Issue Type
        required: true
        default: 'Task'
        type: choice
        options:
          - Task
          - Bug
      summary:
        description: Summary
        type: string
        required: true
      description:
        description: Description
        type: string
        required: false
        default: 'No description'

jobs:
  create_jira_ticket:
    runs-on: ubuntu-latest
    steps:
      # Authenticate with Jira first
      - name: Jira Login
        uses: atlassian/gajira-login@v3
        env:
          JIRA_BASE_URL: {% raw %}${{ secrets.JIRA_BASE_URL }}{% endraw %}
          JIRA_USER_EMAIL: {% raw %}${{ secrets.JIRA_USER_EMAIL }}{% endraw %}
          JIRA_API_TOKEN: {% raw %}${{ secrets.JIRA_API_TOKEN }}{% endraw %}
      # Create the new Jira ticket
      - name: Create Jira ticket
        id: create_jira_ticket
        uses: atlassian/gajira-create@v3
        with:
          project: TEST
          issuetype: {% raw %}${{ inputs.issuetype }}{% endraw %}
          summary: {% raw %}${{ inputs.summary }}{% endraw %}
          description: {% raw %}${{ inputs.description }}{% endraw %}
~~~

This workflow, when executed, creates a Jira task using the provided inputs and secret values. These secret values are inputted in the UI if the workflow is triggered using the `workflow_dispatch` trigger. Following is a screenshot of the UI for this particular workflow:

![A screenshot of the UI for triggering the workflow manually]({{site.images}}{{page.slug}}/trSrJtR.png)

When calling the workflow from another workflow using the `workflow_call` trigger, you need to pass in the inputs and secrets, as shown here:

~~~{.yaml caption=""}
name: Create Jira Ticket for Pull Request

on:
  # Will trigger the workflow when a new pull request is opened.
  pull_request: 
    types: opened

jobs:
  # Calls another workflow and passes in secrets and inputs
  create_ticket:
    # Pass in the path to the workflow file to call
    uses: ivankahl/github-actions-demo/.github/workflows/workflow_call_dispatch_create-jira-ticket.yml@master
    secrets:
      JIRA_BASE_URL: {% raw %}${{ secrets.JIRA_BASE_URL }}{% endraw %}
      JIRA_USER_EMAIL: {% raw %}${{ secrets.JIRA_USER_EMAIL }}{% endraw %}
      JIRA_API_TOKEN: {% raw %}${{ secrets.JIRA_API_TOKEN }}{% endraw %}
    with:
      issuetype: Task
      summary: "Review Opened Pull Request: \
      {% raw %}${{ github.event.pull_request.title }}{% endraw %}"
~~~

When referring to the workflow to call, you must include the repository name, the path to the workflow file in the repository, and the branch containing the workflow file (in this case, `main`).

The `workflow_call` trigger can help you reduce the complexity and duplication of workflow code in your repository. However, make sure you keep your workflow files well-organized and clearly named so that you can easily navigate between workflows and subworkflows.

## Conclusion

In this article, you learned all about the different GitHub Actions triggers you can use when building workflows for your repository. While some might seem similar, it's a good idea to gain a thorough understanding of how each trigger works so you can choose the most appropriate one for your workflow.

GitHub Actions is a powerful and cost-effective tool for building automation in your repository. It can be used for a wide variety of tasks, from code management and automated testing to project management and external notifications like email and Slack. There are also many actions that offer integrations into numerous external systems, and these actions are available for free on the [GitHub Marketplace](https://github.com/marketplace?type=actions). Give it a try and see how automation can simplify your development and deployment processes.

{% include_html cta/bottom-cta.html %}
