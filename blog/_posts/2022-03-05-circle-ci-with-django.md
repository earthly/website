---
title: "CircleCI with Python and Django "
categories:
  - Tutorials
toc: true
author: Josh

internal-links:
 - just an example
---

If you're looking for a reliable CI/CD platform to deploy your Python Django project, CircleCi offers a lot. It's easy to set up, comes with tons of reusable set ups called Orbs, and best of all, offers up to 6,000 build minutes per month for free, so it's great for small projects, but can certainly scale to accommodate large enterprise level workflows with paid accounts.

I'm currently working on a project comparing different CI/CD pipelines, trying to get a better idea of what each offers, how they run, and how much it takes to get them set up. My first stop was CircleCi. To get familiar with it I spun up a small sample DJango project to use for this tutorial. The idea behind the Django project is an app to help me keep track of all of my physical copies of movies (blu-ray, dvds, etc), but really it is just an example project to have something to test and build in CircleCi.

NOTE ON Media inventory:
As I'm sure you guessed there are dozens of apps that do this very well already, but I am required by tutorial writers law to choose something that already exists and build a worse version of it. If you want a great working version checkout [MovieBuddy](https://apps.apple.com/us/app/moviebuddy-movie-tv-library/id965645508). If you want to learn about how to build and test Django with CircleCi, read on.

## CircleCi Sign Up

One thing I really liked was that it was easy to sign up and get started with CircleCi since it offers a completely free tier, there's no credit card necessary. Other products I've tried offer a month or two free, but charge after that, so you can't even sign up without a credit card. As part of the signup process you'll be given the option to  follow steps to connect your github or bitbucket account, which you'll need to do to give CircleCi permission to pull your code. I used github for this tutorial.

![Projects](../assets/images/circle-ci-with-django/menu.png)

Once you are signed in click `projects` in the menu on the left. You should see a list of repos from your github account.

## Creating a Project

Select `Setup Project` next to the repository that contains the Django project you want to build. In order to define a pipeline for your project, you'll need to create `.circleci/config.yml` in the root of your repository. You can create this file in the repo yourself, or you can have CircleCi create a template file for you by selecting the option `Commit a starter CI pipeline to a new branch`. 
![Repo](../assets/images/circle-ci-with-django/create_config.png)

Either way, after clicking `setup project` you'll be taken to a dashboard similar to the one pictured below. The only difference is that the bottom section where the pipeline runs are list will be blank, since you haven't run any pipelines yet.

![Repo](../assets/images/circle-ci-with-django/dashboard.png)

For now, take a look at the three drop down menus. The first lets you select pipelines by owner. This is useful if you are working on a team and you want to give permissions for certain pipelines to certain teams. Very helpful if you are looking to get developers to own their own builds. In a new account there will only be two options, everyone, and your user. 

The next drop down lets you select a specific pipeline. For now it will only have the one pipeline we just created.

The most important one to take note of is the last one, which allows you to select pipelines by branch. This will become very useful as we develope.

Now select `circleci-project-setup` from the drop down. This is the branch that CircleCi made when we set up our project and told it to create the config.yml for us.

From here we have a couple of options. You could pull down the branch CircleCi created and start to edit the file locally, or you can click Edit Config in the top right which opens up an editor in your browser. This is nice becuase circle ci has a linter built in that will let you know if any of hte code you write is invalid. Either way, you should see a template file that looks something like this:

```yml
# Use the latest 2.1 version of CircleCI pipeline process engine.
# See: https://circleci.com/docs/2.0/configuration-reference
version: 2.1

# Define a job to be invoked later in a workflow.
# See: https://circleci.com/docs/2.0/configuration-reference/#jobs
jobs:
  say-hello:
    # Specify the execution environment. You can specify an image from Dockerhub or use one of our Convenience Images from CircleCI's Developer Hub.
    # See: https://circleci.com/docs/2.0/configuration-reference/#docker-machine-macos-windows-executor
    docker:
      - image: cimg/base:stable
    # Add steps to the job
    # See: https://circleci.com/docs/2.0/configuration-reference/#steps
    steps:
      - checkout
      - run:
          name: "Say hello"
          command: "echo Hello, World!"

# Invoke jobs via workflows
# See: https://circleci.com/docs/2.0/configuration-reference/#workflows
workflows:
  say-hello-workflow:
    jobs:
      - say-hello
```
We can start by thinking of the file as containing three seperate pieces. First is the Version of CircleCi we want to use. After that we have job definitions. Jobs are templates for tasks we want to perform. We can define as many jobs as we want and each job can have several steps. It's important to know that jobs do not run on their own. Simply defining a job does nto mean it will run.

Workflows are where we tell circle ci which jobs to run and in what order. We can define several workflows that run under different circumstances. For example, we can have a workflow that runs whenever someone pushes a new branch to our repo. I may run some tests, run our linter, and build our app. Then we might have another workflow that fires whenever there is a merge to master. In this case we may want to do all the same steps again, but add a step where we push the built image to a repositior like AWS ECR or Dockerhub. 

Lets start by creating a job called `build_and_test`.

```yml
version: 2.1

jobs:
  build-and-test:
    docker:
      - image: cimg/python:3.10.1
    steps:
      - checkout
      - run:
          name: install dependancies
          command: pip install -r requirements.txt
      - run:
          name: run tests
          command: python manage.py test

workflows:
  build-and-test-workflow:
    jobs:
      - build-and-test
```

After we name our job we need to specify an enviorment for it run in. In this case, we'll use a docker image. We can pull docker images from dockerhub, or, in this case, we can use [images provided by circleci](https://circleci.com/docs/2.0/circleci-images/). These are images that circleci maintains and that "include tools especially useful for CI/CD". You can search for available images [here](https://circleci.com/developer/images).

Next we define our steps. the `checkout` step tells circleci to to checkout the repo code into the steps working directory. After that we can install the dependancies using pip and then run our tests. Lastly, we need to create a workflow and tell it to run the job we just created.

If you're updating the code locally you'll need to push every time you make a change. Another reason why making edits in the circleci browser editor is super conveient

If you're in the editor you can just click `Save and Run` in the top right corner. This will trigger a 

At the bottom, under the lllll tab you can click on `build-and-test` or go to your dashboard and click on the currently running build. You'll be able to see all the steps for the running build. Oh no! Looks like our build failed when trying to run our tests. If we take a look at the error it looks like Django is having trouble connecting to postgres. 

No worries, we can set up a postgres image to fix this issue.

```yml
  build-and-test:
    docker:
      - image: cimg/python:3.10.1
      - image: cimg/postgres:14.1
        environment:
          POSTGRES_USER: example
```
Next let's take a look at the `settings.py` file in our Django project. In order for our app to be able to connect to postgresql in circleci, we'll need to set have `HOST` set to `localhost`. Also make sure that the `POSTGRES_USER` in your circleci.yml matches the `USER` in your `settings.py` file. In this case I went with the generic `example`. 

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_media',
        'USER': 'example',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
Now rerun the build and it should pass. There's a lot more we can do, including saving our test results, but for now, let's commit these changes. Now circleci will listen for changes to your repo. It will run a new build whenever you push a new branch, push changes to a branch or merge to main. You'll be able to see the status of the build on your PR.

Circleci allows you to save the results of your tests so you can view them in the UI. This is helpful when debugging and also allows you to take advantage of CircleCi's [test insights](https://circleci.com/docs/2.0/collect-test-data/) feature.

CircleCi reads the test data from xml files, so in order to take advantage of this feature we'll need to make an update to our Django project to tell it to save our test results to an xml file.  We are using the build in Unnittest sweet to run our tests. We can export those results to xml easily by installing the [unittest-xml-reporting](https://pypi.org/project/unittest-xml-reporting/) package with `pip install unittest-xml-reporting`

Next we need to tell Django to use the new package and where to save the test results. We can do that by adding the following to the `settings.py` file.

```python
# XML test runner
TEST_RUNNER = 'xmlrunner.extra.djangotestrunner.XMLTestRunner'
TEST_OUTPUT_DIR = './test_results'
TEST_OUTPUT_FILE_NAME = 'results.xml'
```
NOTE Before you push to github. 
1. Don't forget to add `unittest-xml-reporting` to your requirements.txt file. `pip freeze > requirements.txt`
2. Be sure to add `test_results/` to your `.gitignore` file.

You can tests that everything is running locally. Run your tests as normal with `python manage.py test`. YOu should see a test_results/ directory show up in the root of your project with a `results.xml` file in it.

Now we just need to tell CircleCi where to look for the test results by add the following to the config.yml file.

```yml
      - run:
          name: run tests
          command: python manage.py test
      - store_test_results:
          path: test_results
```

With these changes in place, rerun the pipeline. Now, under the tests tab in build view you should see your test results. There won't be much output if all you tests pass. But if any fail, you'll be able to see them in the UI. 

Let's go back and add a step to run our linter before our tests.

```yml
    steps:
      - checkout
      - run:
          name: install dependancies
          command: pip install -r requirements.txt
      - run:
          name: lint
          command: pylint my_media/ media_organizer/
      - run:
          name: run tests
          command: python manage.py test
```
Each time we make an update to our yml file, Circleci will ask if we want to commit to an existing branch or create a new one. In this case I created a new branch.

Now if you run the pipeline again you'll should be able to see some information under tests tab.

![successful test run](../assets/images/circle-ci-with-django/successful_test_run.png)

Green tests are great, but the real benifit of setting this all up is being able to see when tests fail.

![successful test run](../assets/images/circle-ci-with-django/failed_test.png)

TIP:
You can also use CircleCi's Test Insights feature which gives you a window into how your tests are performing overall across multiple runs. The data can help you identify things like flaky tests or tests that are taking too long to run.

## Pushing to Dockerhub
Automatically running our tests with each pull request is great, but what we really want to move toward is deploying our code. If you're using Docker or kubernettes, you'll want to be able to build an image for deployment. Circleci makes that process easy.

In this case we'll build an image and push it to Dockerhub, though it is possible to push to other container management services like AWS ECR. 

First, make sure you have a Dockerhub account and access to your username and password. You'll need to create a repository in Dockerhub. This will be where your images will get pushed to and live.

### Enviorment Variables

In order to push to Dockerhub we'll need to provide a password. Naturally we don't wasnt to put senesaivte information directly into our code, so instead we can take advantage of CircleCi's Enviromant variables.

In the upper right corner of the project screen there will be a button with a gear on it that says Project Settings. Clicking this will bring you to a new page with a new menu on the left. Clcick the button for Environment Variables.

From here you should be able to add your dockerhub user name and password. If you're using the same code as in this tutorial you'll want to name the variables `DOCKERHUB_PASSWORD` and `DOCKERHUB_USERNAME`.

Once set, you can access the enviorment variables at any step in a job by using `$` followed by the variable name. For example `$DOCKERHUB_PASSWORD`. We'll do just that in the next section.

### Updating Our YML file.

Now that we have a repository on Dockerhub and our password and user name set as envs, we can update our config.yml file with a new job to build and push the image ot the remote repository.

CircleCi offers support for running docker commands inside of jobs with the [setup_remote_docker](https://circleci.com/docs/2.0/building-docker-images/)

```yml
build-and-push-to-dockerhub:
    docker:
      - image: cimg/python:3.10.1
    steps:
      - checkout
      - setup_remote_docker:
          version: 19.03.13
          docker_layer_caching: true
      - run: |
          echo "$DOCKERHUB_PASSWORD" | docker login --username $DOCKERHUB_USERNAME --password-stdin
      - run: docker build -t user_name/circle_ci_python_example:$CIRCLE_BRANCH .
      - run: docker push user_name/circle_ci_python_example:$CIRCLE_BRANCH

```
In the code above we create a new job called `build-and-push-to-docker-hub`. The initial setup looks a lot like our `test-and-lint` job. We start with a docker image for python. We don't need postgresql in this step because we won't be running any tests.

Next we need to checkout the code. (look this up to provide more details). When we add the `setup_remote_docker` step to our job, this tells CircleCi to setup a new environment that "is remote, fully-isolated and has been configured to execute Docker commands."

From there we can run our docker commands just as we would from the command line if we were developing locally.

In this case we run three commands. First, we take advantage of the environment variables we set up earlier to login to Dockerhub. The next command builds the docker image and tags it with `user_name/circle_ci_python_example:$CIRCLE_BRANCH`.

The final command pushes the image to Dockerhub.

Last thing we need to do is add this new job to our workflow.

```yml
workflows:
  build-and-test-workflow:
    jobs:
      - test-and-lint
      - build-and-push-to-dockerhub
```

## Order of Execution

Unless you tell CircleCi otherwise, it will attempt to run the jobs in a workflow in parrallell. This comes in handy when you have large workflows or a lot of tests that take a  long time to run. You could split your test runs into seperate jobs and then CircleCi wouuld run them at the same time, saving you time.

But the way we have our current workflow set up, I don't want to push any builds with failing tests up to Dockerhub, so in this case I don't want to run the jobs in parrellel. Instead, I only want to push to Dockerhub after I know all the tests have passed.

No problem. I can tell CircleCi to wait by altering the `config.yml` like this.

```yml
workflows:
  build-and-test-workflow:
    jobs:
      - test-and-lint
      - build-and-push-to-dockerhub:
          requires:
            - test-and-lint
```
By adding the `requires` field to the `build-and-push-to-dockerhub`, CircleCi now knows that I want it to wait until `test-and-lint` finishes and finishes successfully, before running `build-and-push-to-dockerhub`.

## Conclusion


### Writing Article Checklist

- [x] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

## Draft.dev Article Checklist

- [ ] Add in Author page
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
  - Would any images look better `wide` or without the `figcaption`?
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
