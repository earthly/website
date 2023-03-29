---
title: "Better Dependency management in Python"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---



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


# The EarthFile

The nice thing about the Earthfile is it works with all our standard python tooling, and the way I normally install packages, I just do it inside the Earthfile.

First I pick my python version and working directory:
```
# Use a specific Python version
FROM python:3.8
WORKDIR /code
```

Then, I have a specific `target` in Earthly parlance where I install my system level dependencies and then python packages. I call this `deps` copying the Earthly docs but I think you can call it anything.

```
deps:
    # Install system-level dependencies
    RUN apt-get update && apt-get install -y libpq-dev

    # Install python packages
    COPY requirements.txt ./
    RUN pip3 install -r requirements.txt

    # Copy in code
    COPY --dir src tests
```

You can see I just use apt-get to install whatever system packages I need. It works just like a dockerfile in this way. Next I have a unit test step:

```

```



## Conclusion

As a Python developer, I've experienced several challenges during the development and deployment process. Earthly has helped me address some of these pain points. Here are some specific issues I've faced that Earthly has helped with:

* **Dependency management:** In my Python projects, I often require a variety of libraries and packages. This can lead to dependency conflicts and difficulties in maintaining consistent environments across different stages of development. Earthly has helped me isolate dependencies and ensure that the same versions are used throughout the build process, regardless of the host system.

* **Virtual environments:** To manage dependencies and create isolated environments, I used virtual environments like venv or conda. However, setting up and maintaining these environments was cumbersome. Earthly simplified this process by using containers to manage and isolate environments automatically.

* **Build consistency:** I've experienced situations where my Python projects behaved differently across various environments, causing issues when deploying applications. Earthly has ensured that my builds are consistent across different systems by using containerization, which helps me avoid the "it works on my machine" problem.

* **Deployment to multiple platforms:** I've had to deploy my Python applications to various platforms, such as Linux, Windows, or macOS. With Earthly, I can create build targets for different platforms, ensuring that my application is built consistently and with the correct dependencies for each platform.

* Build speed and caching: Earthly's caching mechanism has helped speed up the build process by reusing intermediate build steps when dependencies or code haven't changed. This has been particularly beneficial for larger Python projects or those with many dependencies.

* Integration with CI/CD platforms: My Python projects often utilized continuous integration and deployment systems. Earthly has been easily integrated with various CI/CD platforms, making it simpler to automate my build and deployment processes.

* Multi-language projects: In some projects, I had to work with components in multiple languages or using different build systems. Earthly's language-agnostic nature has been helpful in managing builds for such projects, allowing me to create a unified build process.

Overall, Earthly has helped me streamline my Python projects' build processes, making them more consistent, faster, and easier to manage, particularly when working with complex dependencies or in a team setting.

### Writing Article Checklist

* [ ] Write Outline
* [ ] Write Draft
* [ ] Fix Grammarly Errors
* [ ] Read out loud
* [ ] Write 5 or more titles and pick the best on
* [ ] First two paragraphs: What's it about? Why listen to you?
* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images
* [ ] Verify look of article locally
* [ ] Run mark down linter (`lint`)
* [ ] Add keywords for internal links to front-matter
* [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
* [ ] Add Earthly `CTA` at bottom `{% include_html cta/cta2.html %}`
* [ ] Raise PR

## Outside Article Checklist

* [ ] Add in Author page
* [ ] Create header image in Canva
* [ ] Optional: Find ways to break up content with quotes or images
* [ ] Verify look of article locally
  * Would any images look better `wide` or without the `figcaption`?
* [ ] Run mark down linter (`lint`)
* [ ] Add keywords for internal links to front-matter
* [ ] Run `link-opp` and find 1-5 places to incorporate links
* [ ] Add Earthly `CTA` at bottom `{% include_html cta/cta2.html %}`
