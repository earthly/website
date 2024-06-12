---
title: "Setting Up an iOS Continuous Integration Pipeline"
toc: true
author: Marsel Tzatzos
internal-links:
 - fastlane
 - ios build
 - ios ci
 - io pipeline
excerpt: |
    Learn how to set up a continuous integration pipeline for your iOS app using fastlane and GitHub Actions. Automate your build, test, and deployment phases to streamline your development process and focus on writing code.
last_modified_at: 2023-07-19
categories:
  - deployment
---
**Explore the essentials of iOS CI/CD setup in this article. If you're enhancing your pipelines with fastlane and GitHub Actions, discover how Earthly can elevate your build consistency and speed. [Learn how](https://cloud.earthly.dev/login).**

When I started writing applications in 2010, things were simple. I would write the code, perform merges, run tests (if any), build, and upload to the App Store. The test, build, and upload process didn't require much mental effort, but those tasks took time away from coding.

Today there are a plethora of tools for automating these tasks, which allows you to focus on what matters: writing code.

In this article, I'll show you how to set up your iOS app's CI/CD pipelines. You'll use fastlane and GitHub Actions to automate your build, test, and [deploy](/blog/deployment-strategies) phases and run these tasks on GitHub cloud.

## What Is CI/CD?

Continuous integration/continuous delivery or deployment (CI/CD) is the practice of automating the processes and steps required to push your code into production, as many times as needed depending on your business or application.

The purpose of CI/CD is to quickly provide updated software to your users in an efficient and reliable manner.

## What Is [GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions)?

GitHub Actions is an event-driven utility that lives within your repo and allows you to automate your software development lifecycle via [workflows](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions).

## What Is Xcode?

Xcode is the IDE Apple uses to develop and build software for its platforms. It includes command line tools that allow you to perform all tasks via command line as well. The latter will be used throughout this tutorial to run your workflows.

## What Is [`fastlane`](https://fastlane.tools/)?

fastlane is an open-source platform aimed at simplifying Android and iOS deployment. It consists of a set of built-in [actions](https://docs.fastlane.tools/actions/) and
[plugins](https://docs.fastlane.tools/plugins/available-plugins/) that allow you to perform tasks such as building, testing, and releasing your apps.

## Set Up Fastlane

To install fastlane, use `homebrew` and type `brew install fastlane` in your terminal. This will install fastlane without you needing to worry about the Ruby version.

Open a terminal, navigate into your project's root folder, and type `fastlane init`. You will be asked, "What would you like to use fastlane for?" Select **4. Manual setup – manually set up your project to automate your tasks** and hit **Enter**. This will create a `fastlane` folder, containing two files (Appfile and Fastfile).

Now open your Appfile and replace its content with `app_identifier("your.app.identifier")`.

Fastfile will store the automation configuration that can be run with fastlane.

## Set Up App Store Connect API Integration

The [App Store Connect API](https://developer.apple.com/app-store-connect/api/) is a standards-based REST API that allows you to perform operations found on either the [developer portal](https://developer.apple.com/) or [App Store Connect](https://appstoreconnect.apple.com/).

The [app_store_connect_api_key](https://docs.fastlane.tools/app-store-connect-api/) will handle API authentication.

## Create an API Key

Navigate to [App Store Connect](https://appstoreconnect.apple.com/access/api) and create a new API key. Download the file (.p8) before refreshing or leaving the page, since it won't be available afterward.

You need the contents of the .p8 file in base64 encoding. Run `cat AuthKey_12345.p8 | base64`.

Get the `key id` and `issuer id`.

![Active API keys]({{site.images}}{{page.slug}}/9230.png)

Now set (export) the following environment variables:

``` bash
export APP_STORE_CONNECT_API_KEY_KEY_ID={API_KEY}
export APP_STORE_CONNECT_API_KEY_ISSUER_ID={ISSUER_ID}
export APP_STORE_CONNECT_API_KEY_IS_KEY_CONTENT_BASE64=true
export APP_STORE_CONNECT_API_KEY_KEY={content of the .p8 file base64 encoded}
```

`app_store_connect_api_key` will read these values when we invoke it.

Note that we first used the Appfile to provide our lanes with variables, then switched to environment variables. Later we might pass the properties directly into the action, like `test(skip_build: true)`.

Some other tips: use environment variables when you pass sensitive data, and use anything between config file (Appfile, Matchfile, etc.) variables and function properties for the rest. To check fastlane documentation, search `fastlane action action_you_are_interested_in`; for example, `fastlane action app_store_connect_api_key`.

## Set Up Provisioning Profiles

To build and distribute your app, you will need a production certificate and a provisioning profile. This can be done manually for your local dev environment, but for GitHub Actions, you will have to install them.

For this, you can use [match](https://docs.fastlane.tools/actions/match/). This tool helps you generate your certificates and provisioning profiles and store them centrally, so that they're accessible by your whole team.

## Set Up `match`
  
Create a private GitHub repo. Make sure you can access it via SSH.

Navigate to the root folder of your project and run `fastlane match init`. Go through the initialization wizard by typing **Enter**. This creates a Matchfile in your fastlane folder.

Now it's time to glue things together.

Open the Matchfile and replace its content with the following:

``` js
git_url("git@github.com:myusername/mycertsrepo.git")
storage_mode("git")
type("appstore")
```

Match will need a password to securely encrypt your data into your git. Do this via an environment variable. Type `export MATCH_PASSWORD='MyUltraSecurePassword'`.

Now open your Fastfile and paste the following code inside the `platform :ios do ... end` block.

``` ruby
lane :sync_certificates do
    app_store_connect_api_key
  match(force: true,
      force_for_new_devices: true)
end
```

The lane you created will use `app_store_connect_api_key` to authenticate with the API, and match will handle the creation and storage of your GitHub certificates.

Run the lane by typing `fastlane sync_certificates`. Tip: Run your lanes with the verbose flag if you want to see what goes on behind the scenes; for example, `fastlane sync_certificates --verbose`.

## Run Unit Tests

For this, you'll be using the [scan](https://docs.fastlane.tools/actions/scan/) tool.
  
To set up scan, open your `Fastfile` and paste the following:

``` ruby
lane :test do |options|
  scan(code_coverage: true,
       clean: true,
       skip_build: options[:skip_build] ||= false,
       output_directory: ".scan_result",
       reset_simulator: true)
end
```

Running this lane will build and run the tests, then generate test reports (JUnit, HTML, or
JSON) inside the `.scan_result` folder.

## Run a GitHub Actions Workflow

Workflows are the pipelines that run on GitHub events like push or issue creation. Workflows reside in your repo, inside the `.github/workflows` folder, and are written in YAML.

This first workflow will run the `test` lane we previously created on every PR. As a bonus, on every run the action will post (or update) the test results on your PR's comments.

Create a new file under `.github/workflows` named `test.yml` and paste the following in it:

``` yaml
name: Run tests

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the main branch
  pull_request:

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

  # A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: macos-10.15

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v2
      
      # Setup Xcode version we need for our build
      - name: Setup - Xcode
        run: sudo xcode-select -s /Applications/Xcode_12.4.app
      
      # Setup ruby
      - name: Setup - Ruby and bundler dependencies
        uses: ruby/setup-ruby@v1.57.0
        with:
          ruby-version: 2.7.2
          bundler-cache: true

      # Runs test lane created earlier
      - name: Run tests
        run: bundle exec fastlane test
      
      # Publish the test results even in case of failure
      - name: Publish Scan Report
        uses: EnricoMi/publish-unit-test-result-action/composite@v1
        if: always()
        with:
          files: '.scan_result/*.junit'
```

GitHub Actions offer a variety of runners for your workflows. This example uses Mac OS x 10.15 runner and Xcode 12.4, but you can choose what works for your project. For more info, check [GitHub-hosted runners](https://docs.github.com/en/actions/using-github-hosted-runners/about-github-hosted-runners).

Also, on the [GitHub Marketplace](https://github.com/marketplace?category=deployment&type=actions) you can find actions for all kinds of integrations, or you can [write your own](https://docs.github.com/en/actions/creating-actions).

## Build With `gym`

`Gym` will generate our signed iOS application archive file (`ipa`) file.

Open your Fastfile and add an empty lane.

``` ruby
lane :build do

end
```

Now add these variables inside your lane:

``` ruby
# Reads the value defined in the Appfile
app_target_bundle_identifier = CredentialsManager::AppfileConfig.try_fetch_value(:app_identifier)
project = "MyWallet.xcodeproj"
keychain_name = "MyWallet"
```

Add the following code block in your lane:

``` ruby
# Delete keychain if exists
delete_keychain(name: "MyWallet") if File.exist? File.expand_path("~/Library/Keychains/#{keychain_name}-db")

# Create new keychain & make it default
create_keychain(name: keychain_name,
                default_keychain: true,
                unlock: true,
                timeout: 3600,
                lock_when_sleeps: true)

# Install repo certificates and profiles on our new keychain
match(keychain_name: keychain_name,
      readonly: true)
```

Disable automatic code signing for your project and provide your certificate and profile. This can be done by adding the following code:

``` ruby
app_target_profile_name = ENV["sigh_gr.marseltzatzo.MyWallet_appstore_profile-name"]

# Set manual signing method & update code signing properties for your target
# If multiple targets then we have to repeat for each target with its identifier
update_code_signing_settings(use_automatic_signing: false,
                             targets: "MyWallet",
                             profile_name: app_target_profile_name,
                             code_sign_identity: ENV['APP_STORE_CERT_NAME'],
                             path: project)
```  

`code_signing_identity` is provided via environment variable and can be found in the `match` output (`sync_certificates`).
  
![Certificate common name – match output]({{site.images}}{{page.slug}}/9280.png)

So all you have to do is provide the value `export APP_STORE_CERT_NAME="Your Certificate's Common Name"`.

Now you can build and package your app. This will generate the signed `ipa` and the `dSYM` and save it in the directory you specified (`.archives`).

``` ruby
output_directory = '.archives'
output_name = 'MyWallet-AppStore.ipa'
output_file_path = "#{output_directory}/#{output_name}"

# Build
gym(project: project,
    silent: true,                             
    clean: true,                             
    export_method: "app-store",
    export_options: {
      provisioningProfiles: { 
        app_target_bundle_identifier => app_target_profile_name
      }
    },
    output_directory: output_directory,
    output_name: output_name)
```

## Upload to App Store With `fastlane` [`pilot`](https://docs.fastlane.tools/actions/pilot/)

Pilot can manage your testers as well as provide information about devices. Right now, it will upload your build into TestFlight.

First run your test suite to make sure your build is operating as expected. We previously wrote a lane to run our test suite, and we're going to reuse it on the build
lane. After the `gym` action in our `build` lane, add: `test(skip_build: true)`.

To upload, add the following at the end of your build lane:

``` ruby
# Connect to app store api
app_store_connect_api_key

# Upload to app store
pilot(app_platform: 'ios',
      ipa: output_file_path,
      skip_submission: true,
      skip_waiting_for_build_processing: true,
      reject_build_waiting_for_review: true)
```

Assuming that your environment contains all variables we have set earlier, you can run your action by typing `fastlane build`.

## Set Up Build Action

To run your `build` lane, first set up [secrets](https://docs.github.com/en/actions/reference/encrypted-secrets).

We have been using [environment variables](/blog/understanding-bash) to provide sensitive information to our lanes, but secrets in GitHub Actions store that information securely for use within your workflow.

Go to your GitHub repo > Settings > Secrets and add the following secrets:

``` yaml
APP_STORE_CERT_NAME={your certificates common name}
APP_STORE_CONNECT_API_KEY_KEY_ID={API_KEY}
APP_STORE_CONNECT_API_KEY_ISSUER_ID={ISSUER_ID}
APP_STORE_CONNECT_API_KEY_IS_KEY_CONTENT_BASE64=true
APP_STORE_CONNECT_API_KEY_KEY={content of the .p8 file base64 encoded}
CERTS_SSH_PRIVATE_KEY={the private key to access your certificate repo}
FASTLANE_TEAM_ID={TEAM_ID}
KEYCHAIN_PASSWORD={A Password for the temp keychain your build lane will create}
MATCH_PASSWORD={the password used to encrypt your certificates repo}
```

It should look something like this.

![GitHub UI with secrets]({{site.images}}{{page.slug}}/9420.png)

## Write Your Build Workflow

Finally, create a new workflow, `.github/workflows/build.yml`, and paste the following code inside:

``` yaml
# This is a basic workflow to help you get started with Actions

name: Deploy

# Controls when the workflow will run
on:
  # Triggers the workflow on push events but only for the release branches
  push:
    branches:
      - 'releases/**'

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: macos-10.15

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v2
    
      # Setup Xcode version we need for our build
      - name: Setup - Xcode
        run: sudo xcode-select -s /Applications/Xcode_12.4.app
      
      # Setup ruby
      - name: Setup - Ruby and bundler dependencies
        uses: ruby/setup-ruby@v1.57.0
        with:
          ruby-version: 2.7.2
          bundler-cache: true
      
      # Setup our ssh key to access the private repo with the certificates
      - uses: webfactory/ssh-agent@v0.5.3
        with:
          ssh-private-key: ${{ secrets.MATCH_GIT_PRIVATE_KEY }}

      # Runs a single command using the runners shell
      - name: Build
        run: bundle exec fastlane build
        # Export the needed environment variables
        env:
          APP_STORE_CONNECT_API_KEY_ISSUER_ID: ${{ secrets.APP_STORE_CONNECT_API_KEY_ISSUER_ID }}
          APP_STORE_CONNECT_API_KEY_IS_KEY_CONTENT_BASE64: ${{ secrets.APP_STORE_CONNECT_API_KEY_IS_KEY_CONTENT_BASE64 }}
          APP_STORE_CONNECT_API_KEY_KEY: ${{ secrets.APP_STORE_CONNECT_API_KEY_KEY }}
          APP_STORE_CONNECT_API_KEY_KEY_ID: ${{ secrets.APP_STORE_CONNECT_API_KEY_KEY_ID }}
          FASTLANE_TEAM_ID: ${{ secrets.FASTLANE_TEAM_ID }}
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
          MATCH_KEYCHAIN_PASSWORD: ${{ secrets.KEYCHAIN_PASSWORD }}
          APP_STORE_CERT_NAME: ${{ secrets.APP_STORE_CERT_NAME }}
```

## Conclusion

CI/CD pipelines are key to smooth development, but they need some upkeep. Enter GitHub Actions, which eases this workload so you can zero in on your workflows. We hope our tutorial sets you up for creating the perfect workflow for your project, even if it's not an exact fit.

If you've enjoyed automating with fastlane and GitHub Actions, then you might love exploring [Earthly](https://cloud.earthly.dev/login) for even more streamlined build automation. It's another tool that can further enhance your development process.

The example code for our tutorial is accessible on [GitHub](https://github.com/tzatzosm/MyWallet). Happy coding!
