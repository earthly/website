---
title: "Better Dependency Management in Python"
toc: true
author: Vlad
topic: python
funnel: 3
topcta: false
excerpt: |
    Learn how Earthly can simplify dependency management in Python projects, ensuring consistency across different environments and streamlining the build and deployment process. Say goodbye to the "it works on my machine" problem and focus on the core functionality of your application.
last_modified_at: 2023-07-11
categories:
  - python-tooling
  - Python
---
<!-- markdownlint-disable MD036 -->

Story time.

I remember working on a data visualization project that involved Django and gevent. Don't ask... as the project grew it's dependencies kept growing. And then others had to contribute to the project and things got messy.

One specific issue was managing the dependencies in a consistent manner across different environments – my local development machine, my teammates' machines, and the production environment. We often encountered the dreaded "it works on my machine" problem, where the code ran flawlessly on one system but failed on another.

These were almost always because of non-Python dependencies, libraries required by Matplotlib for rendering images or whatever. These dependencies varied across platforms.

<div>
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/0230.png --alt {{ XKCD joke about Python }} %}
<figcaption>How I used to manage my python packages.</figcaption>
</div>

We tried to address these challenges by using virtual environments and manually managing the dependencies. And while this approach worked at first, was error-prone and time-consuming, as each team member had to set up and maintain their environment. It was easy for subtle differences to creep in.

It feels like Python works great a certain scale but as the dependencies grow – as the lines of code and the team grows – things get increasingly hard.

What we needed was a solution that could simplify the dependency management process, ensure consistency across different environments, and streamline the build and deployment process, so we could focus on the core functionality of our application without worrying about the underlying infrastructure.

## The Solution

The solution I use today for this problem is [Earthly](https://cloud.earthly.dev/login). I use it for testing, CI, building container images and sometimes the local development workflow.[^1]

[^1]: 'Use' is probably an understatement. I created the first version of Earthly, not only to deal with these build and dependency problems but also to make my life easier. I open-sourced Earthly, built a company around it, and I'm even considering getting an Earthly tattoo. In fact, I'm so into Earthly that I've been contemplating changing my name to "Earthling" and adopting "Build, Test, Deploy" as my personal motto. So yeah, you could say I'm a fan.

Every team I've introduced Earthly to, once it clicks for them, ends up finding it an essential part of their python CI workflow.

Let me show you a simplified example of how I'd introduce Earthly to a python project.

### The Example Code

Here is some very simplified Python code:

~~~{.python caption="src/app.py"}
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
~~~

The testing happens with something like this:

~~~{.python caption="tests/test_app.py"}
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
~~~

We also have a `requirements.txt` and all the [normal python stuff](https://github.com/earthly/earthly/tree/main/examples/python).

### The EarthFile

The nice thing about the Earthfile is it works with all our standard Python tooling, and the way I normally install packages, I just do it inside the Earthfile.

First I pick my python version and working directory:

~~~{.dockerfile caption="Earthfile"}
# Use a specific Python version
FROM python:3.8
WORKDIR /code
~~~

Then, I have a specific `target` in Earthly parlance where I install my system level dependencies and then python packages. I call this `deps` copying the Earthly docs but I think you can call it anything.

~~~{.dockerfile caption="Earthfile"}
deps:
    # Install system-level dependencies
    RUN apt-get update && apt-get install -y libpq-dev

    # Install python packages
    COPY requirements.txt ./
    RUN pip3 install -r requirements.txt

    # Copy in code
    COPY --dir src tests
~~~

You can see I just use apt-get to install whatever system packages I need. It works just like a dockerfile in this way. Next I have a unit test step:

~~~{.dockerfile caption="Earthfile"}
test:
  FROM +deps
  RUN python -m unittest tests/test_app.py
~~~

Then I can run tests from the command-line with `earthly +test` and it will run the tests in a environment configured with just the dependencies I installed. I'm on a mac book air mostly, it works the same for me as for [Corey](https://earthly.dev/blog/authors/corey/) when he's one windows or PopOS.

Running the app and packaging it up into a container for prod all follow the same pattern.

~~~{.dockerfile caption="Earthfile"}
# Build the target and start the application
docker:
  ENV FLASK_APP=src/app.py
  ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=3000"]
  SAVE IMAGE my-python-app:latest
~~~

You get the idea. Earthly can also be great for integration tests.

## Integration Tests

Before we role code out into production, we have some relatively large 'integration' tests. These tests don't just touch the python code but its dependencies as well. Database writes and read happen. Earthly makes it easy to do these in CI.

First I have a docker compose with all my service dependencies in it. Then I just have a target in my Earthfile that starts everything up and tears everything down, running the tests in-between.

~~~{.dockerfile caption="Earthfile"}
integration-tests:
    FROM +deps 
    RUN apk update && apk add postgresql-client
    WITH DOCKER --compose docker-compose.yml 
        RUN python test_db_end_to_end.py
    END
~~~

<figcaption>Simplified Integration Test (see [full tutorial](https://docs.earthly.dev/basics/part-6-using-docker-with-earthly) for detailed breakdown)</figcaption>

With that in place, I can run integration tests locally and in CI and they will always work the same. For a more detailed breakdown checkout the [Earthly docs](https://docs.earthly.dev/) or online [example folder](https://docs.earthly.dev/docs/examples).

## Conclusion

As a Python developer, I'd experienced several challenges during the development and deployment process. Earthly helps to address some of these pain points. Here are some specific issues I've faced that Earthly has helped with:

* **Dependency management:** In my Python projects, I often require a variety of libraries and packages. This can lead to dependency conflicts and difficulties in maintaining consistent environments across different stages of development. Earthly has helped me isolate dependencies and ensure that the same versions are used throughout the build process, regardless of the host system.

* **Virtual environments:** To manage dependencies and create isolated environments, I've used virtual environments like `venv` or `conda`. However, setting up and maintaining these environments was cumbersome. Earthly simplified this process by creating isolated environments automatically.

* **Build consistency:** I've experienced situations where my Python projects behaved differently across various environments, causing issues when deploying applications. Earthly has ensured that my builds are consistent across different systems by using containerization, which helps me avoid the "it works on my machine" problem.

* **Deployment to multiple platforms:** I've had to deploy my Python applications to various platforms and various machine architectures. Earthly allows me to built consistently and with the correct dependencies for each platform.

* **Build speed and caching:** Earthly's caching mechanism has helped speed up the build process by reusing intermediate build steps when dependencies or code haven't changed. This has been particularly beneficial for larger Python projects or those with many dependencies.

* **Integration with CI/CD platforms:** Earthly easily integrates with various CI/CD platforms. And using Earthly means you can debug your CI process locally. For some that is reason enough to embrace Earthly.

* **Multi-language projects:** As python project grow, it becomes more likely they have to make gRPC request against a Go service, or they need to use a native C lib. Different languages have different tools and toolchains. Earthly's language-agnostic nature has been helpful in managing builds for such projects, allowing me to create a unified build process.

Overall, Earthly helps streamlines Python projects as they mature and build steps get more complex. Adding Earthly makes things more consistent, faster, and easier to manage, particularly when working with complex dependencies or in a team setting. And it's open source! That's why so many teams are investigating using Earthly.

So [try it out](https://cloud.earthly.dev/login/) and let me know what you think. We have a [slack channel](/slack) if you have questions or feedback to share.

{% include_html cta/bottom-cta.html %}
