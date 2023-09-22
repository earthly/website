---
title: "Resolving Deprecation Errors in GitHub Actions Due to the `set-output`, `save-state`, `add-path` and the `set-env` Workflow Commands"
categories:
  - Tutorials
toc: true
author: Mustapha Ahmad Ayodeji

internal-links:
 - resolving deprecation errors
 - errors in gitHub actions
 - errors workflow commands
 - gitHub actions workflow commands
 - set-output save-state add-path set-env workflow commands
---

<div class="wide">
![Disabled and Deprecated Workflow Commands Errors and Warnings]({{site.images}}{{page.slug}}/KyJZvzC.png)
</div>

Have you encountered failed GitHub Actions (GA) workflow runs accompanied by the error messages above? Or perhaps you've come across those unsettling warnings displayed in the screenshot? If so, you are probably wondering what these errors meant, how can you resolve them, the purpose of the environment files suggested in the warnings, and why are these actions even being deprecated.

This article will address all these concerns. However, this article assumes that you are already familiar with Github Action.

The errors and warnings are shown because GitHub has deprecated and disabled the `set-env` and `add-path` workflow commands and the `set-output` and the `save-state` workflow commands are also on the deprecation list and they will soon be disabled.

Before you dive into how you can fix the errors and warnings, and the rationale behind their deprecation, let's take a short review of what these workflow commands do.

> If you like to just take the fix and move on, you can find them in [this section](#fix-for-workflow-authors)

## The `save-state` and `set-output` Workflow Command

The steps in your workflow jobs run sequentially, one after the other and your workflow jobs run in parallel, however, a job can depend on another in which the dependent job runs after the job it depends on. The `save-state` and `set-output` were previously ways to pass data across from one step to another and from one job to another in a workflow.

Despite their shared functionalities, they served different purposes and the data that they stored was available in different scopes.

### The `save-state` Command

The `save-state` was used to persist data across different steps in the same job or different jobs (not necessarily depending on each other) in the same workflow file and the data persisted was available for the entire duration of the workflow run.

It had the following syntax:

~~~
echo "::save-state name=<state_name>::<state_value>"
~~~

For example, you could persist a Go version environment variable as shown below:

~~~
echo "::save-state name=build_version::$VERSION"
~~~

The `build_version` state would then be available throughout the workflow run.

### The `set-output` Command

The `set-output` was used to set the output for a workflow job. This output would be available in the steps that follow the step that sets it and in the steps of the jobs that depend on the job that sets it, where it could be accessed with the [`needs` context](https://docs.github.com/en/actions/learn-github-actions/contexts#needs-context).

An example of using this command is shown below:

~~~
echo "::set-output name=<output_name>::<output_value>"
~~~

For example, you could set an output of an already defined timestamp variable as shown below:

~~~
echo "::set-output name=build_timestamp::$TIMESTAMP"
~~~

The `build_timestamp` would then be available in the steps that follow and the steps of other jobs that depend on the job that sets the output.

The choice of whether to use the `save-state`  or the `set-output` depends on whether you want the data to persist throughout the workflow run or within a job and its dependent jobs.

## The `add-path` and `set-env` Workflow Command

The `set-env` command was used to set environment variables that could be used in subsequent steps.

It had the following syntax:

~~~
echo ::set-env:: name="<env_name>::<env_value>
~~~

The `add-path` command was used to add a directory to PATH to make it available for use without the need to specify the full path when executing the command.

It had the following syntax:

~~~
echo "::add-path::/usr/local/mytool"
~~~

So, what were the problems with them and why were they deprecated?

## Why Were They Deprecated ?

The `save-state` and the `set-output` command were deprecated (although not yet disabled at the time of writing this article) as part of security enhancement for GitHub action against a potential security breach.

As outlined in the [changelog post](https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/) that introduced this changes:

>" To avoid untrusted logged data to use `save-state` and `set-output` workflow commands without the intention of the workflow author we have introduced a new set of environment files to manage state and output."

These suggested new sets of environment files will be discussed later on in the article.

Similarly, the `add-path` and `set-env` workflow commands, which have also been deprecated, and have now been disabled, due to a [moderate security vulnerability](https://github.com/actions/toolkit/security/advisories/GHSA-mfwh-5m23-j46w) that was identified in the GitHub Actions runner that could allow environment variable and path injection in workflows that log untrusted data to `STDOUT`. This could potentially result in the introduction or modification of environment variables without the workflow author's intention.

All these deprecated commands are now being replaced by environment files. The following section provides a brief introduction to this newly recommended alternative.

## Environment Files

[Environment Files](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#environment-files) are temporary files that the action runners generate during the execution of workflows. The path to these files is exposed by [default environment variables](https://docs.github.com/en/actions/learn-github-actions/variables#default-environment-variables) that have a naming convention of `GITHUB_*`. These environment variables cannot be overridden by user-defined environment variables.

These environment files offer a highly secure and user-friendly method of managing states, setting outputs, manipulating the PATH variable, and defining additional environment variables.

An example of how they can be used to set environment variables is shown below:

~~~{.bash caption=""}
echo "{key}={value}" >> "$GITHUB_ENV"
~~~

They also support the use of multiline with the syntax

~~~{.bash caption=""}
{name}<<{delimiter}
{value}
{delimiter}
~~~

An example of this is the step below that saves a multiline encoded data as an environment variable:

~~~{.yaml caption="build-and-deploy.yaml"}
​​steps:
  - name: Set the value in bash
    id: step_one
    run: |
      # Encode some sensitive data (e.g., a secret key)
      ENCODED_DATA=$(echo "my_secret_key" | base64)

     # Generate a random delimiter
     EOF=$(dd if=/dev/urandom bs=15 count=1 status=none | base64)

      # Store the encoded data in a multiline environment variable
      echo "ENCODED_SECRET<<EOF" >> "$GITHUB_ENV"
      echo "$ENCODED_DATA" >> "$GITHUB_ENV"
      echo "EOF" >> "$GITHUB_ENV"
~~~

The content that will be saved in the environment file will look as shown below:

~~~{.bash caption=""}
ENCODED_SECRET<<EOF
bXlfc2VjcmV0X2tleQ==
EOF

~~~

So now that you understand why you are seeing these errors and warnings, what they meant, and how to use the suggested environment files, You can now move on to fixing the warnings and the errors.

The fixes that will be discussed will be for both workflow authors and action authors.

## Fix for Workflow Authors

As a workflow author, you write workflow files. A simple fix for your workflow files that uses the commands above is to make the following changes in your workflow files.

For the warning below:

~~~{ caption="Output"}
The `save-state` command is deprecated and will be disabled soon. 
Please upgrade to using Environment Files. For more information see:
https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/
~~~

Replace the syntax below:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Save state 
  run: echo "::save-state name={state_name}::{state_value}"
~~~

With:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Save state 
  run: echo "{state_name}={state_value}" >> $GITHUB_STATE
~~~

For the warning below:

~~~{ caption="Output"}
The `set-output` command is deprecated and will be disabled soon. 
Please upgrade to using Environment Files. For more information see:
https://github.blog/changeloq/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/
~~~

Update your workflow files to replace the syntax below:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Set output
  run: echo "::set-output name={output_name}::{output_value}"
~~~

With:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Set output 
  run: echo "{name}={value}" >> $GITHUB_OUTPUT
~~~

For the error below:

~~~{ caption="Output"}
The `add-path` command is disabled. Please upgrade to using 
Environment Files or opt into unsecure command execution by setting the
`ACTIONS_ALLOW _UNSECURE_COMMANDS` environment variable to `true`. 
For more information see: https://github.blog/changelog/2020-10-01-github-actions-deprecating-set-env-and-add-path-commands/
~~~

Update your workflow files by replacing the syntax below:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Add Path
  run echo "::add-path::/usr/local/mytool"
~~~

With:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Add Path
   run echo "{:/usr/local/mytool}" >> $GITHUB_PATH
~~~

For the error below:

~~~{ caption="Output"}
The `set-env` command is disabled. Please upgrade to using 
Environment Files or opt into unsecure command execution by 
setting the `ACTIONS_ALLOW_UNSECURE_COMMANDS` environment 
variable to 'true. For more information see: https://github.blog/changelog/2020-10-01-github-actions-deprecating-set-env-and-add-path-commands/
~~~

Update your workflow files by replacing the syntax below:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Set Env
  run echo "::set-env name={output_name}::{output_value}"
~~~

With:

~~~{.yaml caption="build-and-deploy.yaml"}
- name: Set Env
  run: echo "{name}={value}" >> $GITHUB_ENV
~~~

To do a quick hands-on of making these fixes in an actual workflow file, let's make use of the workflow file that generated the errors and warnings in the image at the beginning of this article. The workflow file is available in this [GitHub repository](https://github.com/DrAnonymousNet/gh-actions/blob/master/.github/workflows/build-and-deploy.yaml).

The workflow is as shown below:

~~~{.yaml caption="build-and-deploy.yaml"}
name: Build and Deploy
on:
  workflow_dispatch:


jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check Out
        uses: actions/checkout@v3

      - name: Setup Go
        uses: actions/setup-go@v3
        with:
          go-version: 1.x

      - name: Build Go App
        run: go build -o dra_app main.go

      - name: Save the binary as an artifact
        uses: actions/upload-artifact@v3
        with:
          name: dra_app-binary
          path: dra_app

      - name: Save an Environment version as output
        run: |
          DRA_ENV="This is from GA"
          echo "::set-output name=draenv::$DRA_ENV"

      - name: Save Timestamp as State
        run: |
          TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          echo "::save-state name=build_timestamp::$TIMESTAMP"

      - name: Set Go version as env value 
        run: echo "::set-env name=GO_VERSION::$(go version \
        | awk '{print $3}')"


  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: always()  # Ensure the job runs always, regardless of the \
    first job's status

    steps:
      - name: Download Artifact
        uses: actions/download-artifact@v2
        with:
          name: dra_app-binary
      
      - name: Set executable permissions
        run: chmod +x dra_app
 
      - name: Deploy Go App
        run: ./dra_app
        
      - name: Retrieve the Timestamp
        run: |
          TIMESTAMP=${{needs.build.outputs.build_timestamp}}
          DRA_ENV=${{needs.build.outputs.draenv}}
          echo "Deployment completed at timestamp $TIMESTAMP and \
          environment variable $DRA_ENV was setups"

      - name: Install jq and add to PATH
        run: |
          sudo apt-get update
          sudo apt-get install jq -y
          echo "::add-path::/usr/bin"
~~~

The workflow file is designed to build and run a simple Go app. This workflow is triggered by a `workflow_dispatch` event and consists of two distinct jobs.

The first job, which is executed on an Ubuntu machine, performs the following steps:

Checks out the repository.
Sets up the Go environment.
Builds the Go app and saves the build output artifact.
Utilizes the deprecated `set-output` command to set an output.
Employs the deprecated save-state command to retain a timestamp as a state.
Utilizes the deprecated and disabled `set-env` command to set the Go version as an environment variable.

The second job is dependent on the outcome of the first job and is also executed on an Ubuntu machine. This job runs regardless of whether the first job succeeded or encountered any failures. The primary tasks of this workflow job are as follows:

Downloads the build artifact that was preserved during the first job.
Sets the downloaded file as an executable.
Attempts to retrieve values from the `TIMESTAMP` output and the `DRA_ENV` environment variable.
Downloads the [`jq`](https://jqlang.github.io/jq/) command-line tool.
Tries to add `jq` to the list of PATH variables using the `add-path` command.

To fix the errors and the warning that you will get from executing this workflow file, you need to change each of these deprecated commands to the new syntax.

The first one is the step below that sets a value as an output:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Save an Environment version as output
        run: |
          DRA_ENV="This is from GA"
          echo "::set-output name=draenv::$DRA_ENV"
~~~

Here, you will change the `set-output` command to use the new environment file for setting output:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Save an Environment version as output
        run: |
          DRA_ENV="This is from GA"
          echo "draenv=$DRA_ENV" >> $GITHUB_OUTPUT
~~~

The second one is the step that saves the timestamp as a state:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Save Timestamp as State
        run: |
          TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          echo "::save-state name=build_timestamp::$TIMESTAMP"
~~~

You can fix this by using the new environment file for saving the state:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Save Timestamp as State
        run: |
          TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
          echo "build_timestamp=$TIMESTAMP" >> $GITHUB_STATE
~~~

The third error was from the step that sets the Go version as an environment variable with the disabled `set-env` command:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Set Go version as env value 
        run: echo "::set-env name=GO_VERSION::$(go version \
        | awk '{print $3}')"
~~~

This can be fixed as shown below:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Set Go version as env value 
        run: echo "GO_VERSION=$(go version \
        | awk '{print $3}')" >> $GITHUB_ENV
~~~

Finally, the last error was from the step that installed the `jq` command and added it to the path:

~~~{.yaml caption="build-and-deploy.yaml"}
      - name: Install jq and add to PATH
        run: |
          sudo apt-get update
          sudo apt-get install jq -y
          echo "/usr/bin" >> $GITHUB_PATH
~~~

This [github branch](https://github.com/DrAnonymousNet/gh-actions/tree/patch-1/.github/workflows) contains these changes. The highlighted changes can be found in this GitHub [commit](https://github.com/DrAnonymousNet/gh-actions/pull/6/commits/afdb5b80acfde957d2f3b62e4511d1463b855747).

If you rerun this workflow file in this new branch:

<div class="wide">
![Rerun build]({{site.images}}{{page.slug}}/zuhAgU0.png)
</div>

The run will be successful without any warnings or errors:

<div class="wide">
![Successful build without any warnings]({{site.images}}{{page.slug}}/UAPpQGK.png)
</div>

In your GitHub repositories, you have probably used these commands in multiple places in a workflow file, it can be a little bit hard looking for the usage of these commands in the file. You can make use of the GitHub editor's find and replace features to make this a little bit easier.

### Searching for the Command Usage in a Single File

You can search for the instances of these deprecated commands in a single file by using the GitHub editor's find and replace feature.

To use this, open the workflow file in edit mode and click on `Command`+`F` (Mac) or
`Ctrl`+`F` (Windows/Linux). This will bring up a panel that allows you to search for the instances of these commands:

<div class="wide">
![image]({{site.images}}{{page.slug}}/SPGtAtD.png)\
</div>

Using the replace feature might not be efficient here due to the dynamics of the usage of these commands. However, you can manually edit the file to effect the new changes.

The demonstration above involves fixing the usage of these deprecated commands in a single workflow file. You have probably used these commands in multiple workflow files. In the next section, you will learn how to find the usage of these commands across multiple workflow files in different repositories so that you can know where you need to change.

### Searching for Command Usage with GitHub Code Search Syntax

To look for all the instances of the above-deprecated commands in your repositories, you can make use of the [GitHub code search syntax](https://docs.github.com/en/search-github/github-code-search/understanding-github-code-search-syntax) which allows you to build search queries for these commands by using specialized code qualifiers, regular expressions, and boolean operations.

To use it, click on the search icon from anywhere in your GitHub account:

<div class="wide">
![image]({{site.images}}{{page.slug}}/0Jggjx9.png)\
</div>

Add your search query in the search bar. The query below searches for the use of any of the `save-state`, `add-path`, `set-env`, and `set-output` in the file path of `.github/workflows`  in any repository owned by `DrAnonymousNet` (replace with your GitHub username:

~~~{ caption=""}
owner:DrAnonymousNet  path:/^\.github\/workflows\// save-state \
OR add-path OR set-env OR set-output
~~~

This search query returns the following result in my repository:

<div class="wide">
![image]({{site.images}}{{page.slug}}/P8ixXzA.png)\
</div>

From the result, you can identify the files where these commands are used. In the next section, you will see how you can fix all the instances of these commands in a file at once with the [`sed`](https://www.gnu.org/software/sed/manual/sed.html) command.

### Fixing All Instances of the Commands Usage with the `sed` Command

To fix all instances of these commands in a file, you can execute this `sed` command in a bash-based workflow:

~~~{.bash caption=">_"}
sed -i '' \
  -e 's/echo "::set-output name=\([^:]*\)::\([^"]*\)"/echo "\1=\2" >> $GITHUB_OUTPUT/g' \
  -e 's/echo "::set-env name=\([^:]*\)::\([^"]*\)"/echo "\1=\2" >> $GITHUB_ENV/g' \
  -e 's/echo "::save-state name=\([^:]*\)::\([^"]*\)"/echo "\1=\2" >> $GITHUB_STATE/g' \
  -e 's/echo "::add-path::\([^"]*\)"/echo "\1" >> $GITHUB_PATH/'

 file_name
~~~

The command searches all syntax that matches the deprecated syntax and replaces them with the new syntax of the environment files.

Replace the `file_name` placeholder with your workflow file.

After running the command, inspect the output of `git diff` and make any final touches that aren't perfect.

The following is the output of executing the command on the workflow file used in this article:

<div class="wide">
![Output of git diff]({{site.images}}{{page.slug}}/JeTyTxx.png)
</div>

Another instance of this `sed` command is suggested by [kcgen](https://github.com/kcgen) in this [GitHub community discussion](https://github.com/orgs/community/discussions/35994#discussioncomment-3881150
)

### Fix for Errors and Warnings Due to Workflow Dependencies

The fixes discussed above are applicable when you get these errors and warnings because you use these commands directly in your workflow files. It is also possible that you get these errors and warnings due to an action that your workflow file depends on.

Take this workflow file that uses the [`setup-python`](https://github.com/actions/setup-python) action pinned to an old commit sha:

~~~{.yaml caption="build-and-deploy.yaml"}
name: My Workflow

on:

  workflow_dispatch:

jobs:
  my_job:
    runs-on: ubuntu-latest
    steps:
      - name: Set up Python 3.10
        uses: actions/setup-python@bdd6409dc13e625e6c1c0ad857bd591804786f7b
        with:
            python-version: "3.10"
~~~

When you dispatch this workflow, you will get the errors and warnings below due to the deprecated commands even though you don't directly use them:

<div class="wide">
![image]({{site.images}}{{page.slug}}/S6eiaoS.png)\
</div>

To fix this, you need to switch to an updated version provided by the action author where they have fixed the issue. If there is no updated version, you can raise an issue in their repository to notify them of the errors and warnings.

## Fix for Action Authors

As an action author that writes custom actions that workflow files depend on, If the users of your custom actions are raising GitHub issues due to the deprecation of the commands above, you need to update the [`@actions/core`](https://github.com/actions/toolkit/blob/45c49b09df04cff84c5f336f07d5232fa7103761/packages/core/README.md#L4) package to the latest version. The latest version of this package provides the updated version of the code that provides the workflow commands.

## Conclusion

In this tutorial, you learn about how to fix the warnings and errors in your workflow files due to the deprecation of the `set-env`, `add-path`, `set-output`, and the `save-state` command. You learn about the reasons for these deprecations, what the suggested environment files meant, and how to use the environment file.

For action authors, you have also learned about how to fix the custom action that you provide when users that depend on your action get this error.

In order to stay updated with the latest changes like deprecation or features introduction on GitHub products generally, you can always visit the [changelog page](https://github.blog/changelog).

{% include_html cta/bottom-cta.html %}
