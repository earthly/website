---
title: "CircleCI with Python and Django "
categories:
  - Tutorials
toc: true
author: Josh

internal-links:
 - just an example
---
Go to circleci and start a new account. You can sign up with your email or use an existing github account. Follow the steps to connect your github or bitbucket account. I used github.

Once you are signed in Click projects in the menu on the left. You should see a list of repos. 

Select Setup Project. 
Circleci uses a config.yml file to know what to do. You can create this file in the repo yourself, or you can have circleci create a template file for you by selecting the option Commit a starter CI pipeline to a new branch. I decided to go this route. After clicking setup project you'll be taken to a dashboard. 

Above your pipleline you should see three drop down menus. The first lets you select pipelines by owner. This is useful if you are working on a team and you want to give permissions for certain pipelines to certian teams. Very helpful if you are looking to get developers to own their own builds. In a new account there will only be two options, everyone, and your user. The drop down lets you select a specific pipeline and the last one lets you select which branch you'd like to see builds for. Select your project from the drop down menu. If the branch drop down is set to all branches you should see an execution of your pipeline.

Now select `circleci-project-setup` from the drop down. This is the branch that Circleci made when we set up our project and told it to create the config.yml for us.

From here we have a couple of options. You could pull down the branch circleci created and start to edit the file locally, or you can click Edit Config in the top right which opens up an editor in your browser. This is nice becuase circle ci has a linter built in that will let you know if any of hte code you write is invalid. Either way, you should see a template file that looks something like this:

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
We can start by thinking of the file as containing three seperate pieces. First is the Version of cirlceci we want to use. After that we have job definitions. Jobs are templates for tasks we want to perform. We can define as many jobs as we want and each job can have several steps. It's important to know that jobs do not run on their own. Simply defining a job does nto mean it will run.

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

## Outline
Create a Django application
attach it to a postgresql db
create 2 models:
  Movies
  Formats
  
create a page to view the data:
  route
  view
  template

create some tests
  Write a couple unit tests for the model
  write a couple integration tests to determine a route returns the correct html.

Install a linter:
  hopefully this is pretty straight forward and won't require a ton of configuration
  pylint --load-plugins pylint_django --django-settings-module=my_media.settings

Create a `.circleci/config.yml`. For now just add `version: 2.1`

Create a git repo and push the code. 

In circleci, connect to the project.

From here we can build the yml through trial and error.
It will need to:
  lint - run the linter and pass
  test - install postgres, run migrations, run tests

  add the store_test_results step

  build a docker image - so probably need to create a dockerfile?
  push the image to docker hub - never done this.

### Writing Article Checklist

- [ ] Write Outline
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
