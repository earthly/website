---
title: "Better Dependency management in Python"
categories:
  - Tutorials
toc: true
author: Rebecca Hines
topic: python
funnel: 3
---
<!-- markdownlint-disable MD036 -->

## Welcome to Dependency Hell

As a Python developer, I remember working on a data visualization project that involved a web application built using Flask and data processing with Matplotlib. The project's dependencies quickly became a challenge due to the numerous libraries and packages required for both Flask and Matplotlib, as well as their compatibility with different Python versions.

One specific issue I faced was managing the dependencies in a consistent manner across different environments—my local development machine, my teammates' machines, and the production environment. We often encountered the dreaded "it works on my machine" problem, where the code ran flawlessly on one system but failed on another due to subtle differences in package versions or system libraries.

Another pain point was dealing with non-Python dependencies, such as the libraries required by Matplotlib for rendering images. These dependencies were the core problem because varied across platforms, adding an extra layer of complexity to the project.

<div>
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/0230.png --alt {{ XKCD joke about Python }} %}
<figcaption>How I used to manage my python packages.</figcaption>
</div>

We tried to address these challenges by using virtual environments and manually managing the dependencies. However, this approach proved to be error-prone and time-consuming, as each team member had to set up and maintain their environment, and subtle differences still crept in.

What we needed was a solution that could simplify the dependency management process, ensure consistency across different environments, and streamline the build and deployment process, so we could focus on the core functionality of our application without worrying about the underlying infrastructure.

## The Solution

The solution I ended up with, for testing, CI, building container images and sometimes the local development workflow was Earthly. Once I introduced it, the whole team slowly got on board. Let me show you a simplified example of what we did.

### The Example Code

Here is my python code, which doesn't matter that much for the example:

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

We also have a `requirements.txt` and all the normal python stuff.

### The EarthFile

The nice thing about the Earthfile is it works with all our standard python tooling, and the way I normally install packages, I just do it inside the Earthfile.

First I pick my python version and working directory:

~~~
# Use a specific Python version
FROM python:3.8
WORKDIR /code
~~~

Then, I have a specific `target` in Earthly parlance where I install my system level dependencies and then python packages. I call this `deps` copying the Earthly docs but I think you can call it anything.

~~~
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

~~~
test:
  FROM +deps
  RUN python -m unittest tests/test_app.py
~~~

Then I can run tests from the command-line with `earthly +test` and it will run the tests in a environment configured with just the dependencies I installed. I'm on a mac book, but my colleagues on Windows and that one data engineering person using PopOS get the same result.

Running the app and packaging it up into a container for prod all follow the same pattern.

~~~
# Build the target and start the application
docker:
  ENV FLASK_APP=src/app.py
  ENTRYPOINT ["flask", "run", "--host=0.0.0.0", "--port=3000"]
  SAVE IMAGE my-python-app:latest
~~~

You get the idea. Or checkout the [Earthly docs](https://docs.earthly.dev/) or online [example folder](https://docs.earthly.dev/docs/examples).

Some on my team use Earthly for CI and `pyenv` and manual steps for local and that can work to. But for me, it took a bit for it to all click but not that I get it, I'm not going back.

## Conclusion

As a Python developer, I've experienced several challenges during the development and deployment process. Earthly has helped me address some of these pain points. Here are some specific issues I've faced that Earthly has helped with:

* **Dependency management:** In my Python projects, I often require a variety of libraries and packages. This can lead to dependency conflicts and difficulties in maintaining consistent environments across different stages of development. Earthly has helped me isolate dependencies and ensure that the same versions are used throughout the build process, regardless of the host system.

* **Virtual environments:** To manage dependencies and create isolated environments, I used virtual environments like `venv` or `conda`. However, setting up and maintaining these environments was cumbersome. Earthly simplified this process by using containers to manage and isolate environments automatically.

* **Build consistency:** I've experienced situations where my Python projects behaved differently across various environments, causing issues when deploying applications. Earthly has ensured that my builds are consistent across different systems by using containerization, which helps me avoid the "it works on my machine" problem.

* **Deployment to multiple platforms:** I've had to deploy my Python applications to various platforms, such as Linux, Windows, or macOS. With Earthly, I can create build targets for different platforms, ensuring that my application is built consistently and with the correct dependencies for each platform.

* Build speed and caching: Earthly's caching mechanism has helped speed up the build process by reusing intermediate build steps when dependencies or code haven't changed. This has been particularly beneficial for larger Python projects or those with many dependencies.

* Integration with CI/CD platforms: My Python projects often utilized continuous integration and deployment systems. Earthly has been easily integrated with various CI/CD platforms, making it simpler to automate my build and deployment processes.

* Multi-language projects: In some projects, I had to work with components in multiple languages or using different build systems. Earthly's language-agnostic nature has been helpful in managing builds for such projects, allowing me to create a unified build process.

Overall, Earthly has helped me streamline my Python projects' build processes, making them more consistent, faster, and easier to manage, particularly when working with complex dependencies or in a team setting.

{% include_html cta/cta2.html %}

_This Python and Earthly experience report was written by Rebecca Hines in collaboration with the marketing team at Earthly._
