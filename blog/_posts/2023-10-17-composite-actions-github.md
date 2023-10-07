---
title: "Understanding and Using Composite Actions in GitHub"
categories:
  - Tutorials
toc: true
author: Ikeh Akinyemi

internal-links:
 - composite actions in github
 - understanding github actions
 - using github actions
 - using composite actions
---

[GitHub Actions](https://github.com/features/actions) offers a robust set of tools for a number of tasks, but there's an advanced feature that warrants attention for its potential to optimize workflows: [composite actions](https://docs.github.com/en/actions/creating-actions/creating-a-composite-action).

Composite actions are designed to encapsulate a sequence of actions into a singular, reusable entity, enhancing the modularity and efficiency of workflows.

While GitHub Actions has introduced [reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows) to enhance modularity and reusability, they can't call and consume other reusable workflows and can function without a repository checkout. In contrast, composite actions let you bundle multiple workflow steps into a single action and require a repository checkout for utilization.

In this tutorial, you'll learn all about the mechanics of composite actions, including a comprehensive overview of their structure and utility.

## Using Composite Actions in GitHub

In this section, you'll learn how to efficiently use composite actions for a streamlined CI/CD process. Along the way, you'll learn all about composite action mechanics and how best to use them.

### Initialize a New GitHub Repository

Start by creating a new repository on GitHub. This repository serves as the foundation for your actions. Then clone the repo to your local machine:

~~~
$ git clone git@github.com:Ikeh-Akinyemi/composite-github-action.git
~~~

> Make sure you update the repository link to the one you created.

### Implement Your Composite Action

Once you've cloned your repo to your local machine, create an `action.yml` file within the repository's root directory. This file houses the definition and components of your composite action:

~~~
$ touch action.yml
~~~

By convention, this file is placed at the root of a repository. However, it's not mandatory for the file to be named `action.yml` or to be at the top level. You can have multiple composite actions in a single repository by placing them in separate directories, each with its own `action.yml` file.

Now, it's time to progressively build the `action.yml` file for a Database Migration composite action.

#### Action Metadata

Start by defining the name and description of the action:

~~~
name: "Database Migration"
description: "Migrate a Postgres service spinned up for testing purposes."
~~~

This metadata provides a clear identity and purpose for the action.

#### Inputs

Then define the inputs that the action requires. These inputs provide flexibility, allowing users to customize the action's behavior based on their specific needs:

~~~
inputs:
  database_url:
    description: "Connection string for the database. Follows the format: postgres://[user[:password]@][host][:port][/dbname][?options]"
    required: true
    default: "postgres://root:password@localhost:5432/test?sslmode=disable"
  migration_files_source:
    description: "Path or URL to migration files. Can be local, a GitHub repo using 'github://<owner>/<repo>?dir=<directory>', or other formats supported by golang-migrate."
    required: true
    default: "file://db/migrations"
~~~

Here, two inputs are defined: `database_url` and `migration_files_path`. Both have default values, but they can be overridden when the action is used.

#### Outputs

Next, you need to specify the outputs that the action produces. Outputs allow the action to return data that can be consumed by subsequent steps in a workflow:

~~~
outputs:
  migration_report:
    description: "Reports the status of the database migration"
    value: ${{ steps.database-migration-report.outputs.report }}
~~~

This `migration_report` output captures the result of the database migration, which can be used for logging or decision-making in subsequent workflow steps.

#### Steps

Finally, define the sequence of steps the action executes. Each step can run commands or invoke other actions:

~~~
runs:
  using: "composite"
  steps:
    - name: Install golang-migrate
      run: |
        curl -L https://github.com/golang-migrate/migrate/releases/download/v4.15.2/migrate.linux-amd64.tar.gz | tar xvz
        sudo mv migrate /usr/bin/
        which migrate
      shell: bash

    - name: Run database migrations
      run: migrate -source ${{ inputs.migration_files_source }} -database ${{ inputs.database_url }} -verbose up
      shell: bash

    - name: Report migration status
      id: database-migration-report
      run: if [ $? -eq 0 ]; then echo "report=Migrated database successfully" >> $GITHUB_OUTPUT; else echo "report=Failed to migrate database" >> $GITHUB_OUTPUT; fi
      shell: bash
~~~

This code performs the following actions:

* **`golang-migrate`** downloads and installs the [`golang-migrate`](https://github.com/golang-migrate/migrate) tool, which is essential for running database migrations.
* **`Run database migrations`** uses the `golang-migrate` tool to apply migrations to the database, referencing the provided `migration_files_source` as the `-source` flag value.
* **`Report migration status`** checks the exit status of the migration command and produces a report, which is then set as an output for the action.

In the previous snippet, the `using: "composite"` field is pivotal when defining a composite action. It signals to GitHub Actions that the action being defined is not a traditional [Docker](https://docs.github.com/en/actions/creating-actions/creating-a-docker-container-action) or [JavaScript](https://docs.github.com/en/actions/creating-actions/creating-a-javascript-action) action but rather a composite of multiple steps. This distinction is crucial because it allows the action to bundle several commands or even other actions into a single, reusable unit.

The `shell` field in this step is set to `bash`. This means that the commands specified in the `run` fields are executed in a Bash environment. GitHub Actions supports various shells, such as `bash`, `sh`, `pwsh`, and `python`. The choice of shell determines the syntax and features available for the commands.

With this structure, you've successfully defined a composite action that can be reused across multiple workflows, ensuring consistent database migrations.

### Publish Your Action

Once your file is ready for a database migration composite action, you need to push the newly created composite action to GitHub to make it available for use:

~~~
$ git add .
$ git commit -m "Publish composite action"
$ git push origin main
~~~

For better management and to facilitate its use in workflows, tag the action with a version, like `v1`, `v2`, etc.:

~~~
$ git tag -a v1 -m "Initial release of db migration action"
$ git push origin v1
~~~

This versioning approach ensures that you can reference specific versions of your action in workflows, allowing for controlled updates and compatibility management. However, it's not mandatory to use git tags; you can also reference a specific commit or branch.

### Incorporate the Composite Action into a Workflow

Next, in either an existing repository or a new one, create a `test.yml` file within the `./.github/workflows/` folder. While it's possible for a composite action to share a repository with other code, including the workflows that call it, it's recommended keeping the actions in separate repositories for clarity and modularity. In this `test.yml` file, you'll implement a workflow that integrates the composite action you previously defined.

To seamlessly integrate the composite action into a workflow, it's crucial that you understand the structure and purpose of each section within the workflow file, so the process will be dissected in the following section.

#### Workflow Metadata

Every workflow starts with a name and a set of triggering events. This metadata provides context and determines when the workflow should be executed:

~~~
name: Test running composite github action

on:
  push:
    branches: [ main ]
~~~

Here, the workflow is aptly named `Test running composite github action`. It's set to be triggered on a `push` event specifically targeting the `main` branch. This ensures that the workflow runs whenever code is pushed against the `main` branch.

#### Job Definition

The heart of the workflow is its jobs. Each job represents a unit of work and runs in a specific environment:

~~~
jobs:
  database-migration-ci:
    name: A job to spin up a Postgres service and migrate it.
    runs-on: ubuntu-latest
~~~

Here, a job named `database-migration-ci` is defined. The descriptive name indicates its purpose: to spin up a Postgres service and handle its migration. The job is configured to run on the latest version of Ubuntu.

#### Service Configuration

Some workflows require [external services](https://docs.github.com/en/actions/using-containerized-services/about-service-containers), such as databases or cloud storage. Before executing the main steps, these services are configured and initialized.

Spin up a [PostgreSQL service](https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers) using a Docker image with specific environment variables set for authentication:

~~~
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: root
          POSTGRES_PASSWORD: c16bc0af8840ef353a2a51e06b9ef568
          POSTGRES_DB: earthly_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
~~~

This configuration is crucial for the subsequent steps. And the health checks ensure that the service is fully operational before the workflow progresses. The port mapping ensures that the service is accessible on the expected port, `5432`.

#### Steps

As you've previously learned, the steps are the actionable items in the workflow:

1. **Check out the repository**

   To work with the codebase, it's essential to have the repository's content:

   ~~~
       steps:
         - name: Checkout repository
           uses: actions/checkout@v3
   ~~~

   The `actions/checkout@v3` action fetches the content of the current repository, making it available for the following steps.

2. **Migrate the database**

   With the environment set, the next task is to migrate the database:

   ~~~
        steps:
         ...
         - id: postgres-migration
           name: Migrate Postgres DB
           uses: Ikeh-Akinyemi/composite-github-action@v1
           with:
             database_url: 'postgres://root:c16bc0af8840ef353a2a51e06b9ef568@localhost:5432/earthly_db?sslmode=disable'
             migration_files_source: 'file://db/migrations'
   ~~~

   This step invokes the previously defined composite action by referencing it in the workflow. The naming convention for composite actions typically follows the format `{owner}/{repo}@{ref}`. Here, `owner` is the username of a personal or organization GitHub account, `repo` is the name of the repository, and `ref` can be a tag, a commit SHA, or a branch name. For instance, `Ikeh-Akinyemi/composite-github-action@v1` points to version one of the composite action in the `Ikeh-Akinyemi/composite-github-action` repository. Instead of `v1`, you can also use commit SHA, such as `Ikeh-Akinyemi/composite-github-action@4a3ddaf9b2914638ca2be9f4b21af5d01d9d3e22`, or a branch name as in `Ikeh-Akinyemi/composite-github-action@main`. The [docs](https://docs.github.com/en/actions/learn-github-actions/finding-and-customizing-actions#using-release-management-for-your-custom-actions) provide a good overview of all the approaches.

   Make sure you adjust the `uses` value to match the GitHub username, repository, and version where your composite action is located. By passing in the necessary inputs using the `with` field, you can see the power of composite actions in action, transforming complex tasks into a singular, streamlined step.

   The `migration_files_source` points to the `db/migrations` directory. Instead of detailing the SQL migration scripts here, you can find the necessary migration files in this [GitHub repository](https://github.com/Ikeh-Akinyemi/cat-nova-special/tree/main/db/migrations). Ensure you have the `db/migrations` folder set up in your root directory and that it contains the required `000001_init_db.up.sql` and `000001_init_db.down.sql` files.

   With the migration scripts sourced from the repository, you can proceed to the next step of the workflow.

3. **Report the migration status**

   After migration, it's beneficial to capture its outcome:

   ~~~
       steps:
         ...
         - name: Report migration status
           run: echo report-status ${{ steps.postgres-migration.outputs.migration_report }}
           shell: bash
   ~~~

   Using the `id` defined in the previous step, this step fetches the migration report output from the composite action and echoes it, providing visibility into the migration's success or failure.

   Now, as a final step after understanding and implementing each section of this workflow, you can push the workflow to GitHub. This triggers the workflow to be executed, achieving the following results:

<div class="wide">
![GitHub Action](https://imgur.com/PwIlMU4.png)
</div>

## Same Repository vs. Multiple in One Repository

When using composite actions, how you reference them in your workflow depends on where they're located and how they're organized.

### Composite Action in the Same Repository

If your composite action is in the same repository as your workflow, you don't need to specify the full `username/repository@version` format. Instead, you can reference the relative path to the `action.yml` file of the composite action.

For example, if your composite action's `action.yml` is in the root of your repository, you can reference it in your workflow like this:

~~~
uses: ./
~~~

If it's inside a directory named `my-composite-action`, then it would look like this:

~~~
uses: ./my-composite-action
~~~

### Multiple Composite Actions in One Repository

If you have multiple composite actions in a single repository, each composite action should have its own directory, and each directory should contain its own `action.yml` file.

For instance, if you have two composite actions named `action-one` and `action-two`, your repository structure might look like this:

~~~
repository-root
|-- action-one
|   |-- action.yml
|-- action-two
|   |-- action.yml
|-- .github/workflows
|   |-- main.yml
~~~

In your workflow (`main.yml`), you can reference each composite action by its directory path:

~~~
steps:
  - name: Use Action One
    uses: ./action-one

  - name: Use Action Two
    uses: ./action-two
~~~

If these composite actions are in a different repository, you would reference them with the full `username/repository@version` format, followed by the directory path:

~~~
steps:
  - name: Use Action One from External Repo
    uses: username/repository/action-one@v1

  - name: Use Action Two from External Repo
    uses: username/repository/action-two@v1
~~~

More details on the reference pattern can be found on [Github](https://docs.github.com/en/actions/using-workflows/reusing-workflows#calling-a-reusable-workflow). The full format is `{owner}/{repo}/.github/workflows/{filename}@{ref}`

Note that, if you want to [publish your action on the GitHub marketplace](https://docs.github.com/en/actions/creating-actions/publishing-actions-in-github-marketplace), you need to have a single action in one repo.

### Note on Versioning

When you use git tags for versioning, the tag applies to the entire repository. This means, if you update one composite action and tag a new release, that release number will apply to all composite actions in the repository, even if others haven't changed. This is something to keep in mind when managing multiple composite actions in one repo.

## Conclusion

In this deep dive, you've demystified the intricacies of composite actions within GitHub Actions. By now, you should have a solid grasp on crafting and integrating these modular, reusable components into your workflows, optimizing CI/CD processes with precision. As you continue to refine your development pipelines, remember that composite actions are a potent tool in your arsenal, enabling streamlined, maintainable, and efficient workflows.

You can learn more about the GitHub Actions YAML syntax on the [GitHub Docs](https://docs.github.com/en/actions/creating-actions/metadata-syntax-for-github-actions). Additionally, links to the GitHub repositories are available here: [composite-github-action](https://github.com/Ikeh-Akinyemi/composite-github-action) and [cat-nova-special](https://github.com/Ikeh-Akinyemi/cat-nova-special).

{% include_html cta/bottom-cta.html %}

## Outside Article Checklist

* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images
* [ ] Verify look of article locally
  * Would any images look better `wide` or without the `figcaption`?
* [ ] Add keywords for internal links to front-matter
* [ ] Run `link-opp` and find 1-5 places to incorporate links
