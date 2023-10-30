---
title: "Poetry Build and Publish"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "pypi"
---
# Intro

[Last time]() I showed you how to publish a package to pypi using setup.py. But if you are using poetry, and [I think you should be]() then there is an even easier way. Let me walk you all the way through it, including how to push to test.pypi for testing purposes. But if you want to skip ahead, know you just have to run `poetry publish --build` on a properly configured poetry project.

# Code

Starting for the top, I have this python code I want to get on pypi:

~~~{.python caption="core.py"}
def merge(list1, list2):
    merged_list = []
    i, j = 0, 0
    
    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged_list.append(list1[i])
            i += 1
        else:
            merged_list.append(list2[j])
            j += 1
    
    # Add any remaining elements from list1 or list2
    while i < len(list1):
        merged_list.append(list1[i])
        i += 1
        
    while j < len(list2):
        merged_list.append(list2[j])
        j += 1
    
    return merged_list

~~~

To create a poetry project for this:

~~~{.bash caption=">_"}
pip install poetry
poetry new mergefast 
~~~

Doing that creates the structure for my package:

~~~{.bash caption=">_"}
.
├── README.md
├── mergefast
│   └── __init__.py
├── pyproject.toml
└── tests
    └── __init__.py
~~~

Copying my code into `core.py` and adding my [test.py] into the project I get:

~~~{.bash caption=">_"}
.
├── README.md
├── mergefast
│   ├── __init__.py
│   └── core.py
├── poetry.lock
├── pyproject.toml
└── tests
    ├── __init__.py
    └── test.py

~~~

Let's look at the `pyproject.toml`:

~~~{.toml caption="pyproject.toml"}
[tool.poetry]
name = "mergefast"
version = "0.1.1"
description = ""
authors = ["Adam Gordon Bell <adam@corecursive.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
~~~

You can see that name, version and other details traditionally configured in a setup.py are already here. That makes building easy.

## Poetry Build

To build a package with poetry:

~~~{.bash caption=">_"}
> poetry build 
Building mergefast (0.1.1)
  - Building sdist
  - Built mergefast-0.1.1.tar.gz
  - Building wheel
  - Built mergefast-0.1.1-py3-none-any.whl
~~~

This will build both a source distribution and a wheel. To build each seperatatily use `poetry build --format sdist` and `poetry build --format wheel`.

## Testing The Package

Because of Poetry's focus on virtual environments, it's easy to test the package without even building it.

~~~{.bash caption=">_"}
> poetry shell
Spawning shell within /Users/adam/Library/Caches/pypoetry/virtualenvs/mergefast-MrBSzehX-py3.11
> pip list
Package            Version   Editable project location
------------------ --------- ---------------------------------------
certifi            2023.7.22
charset-normalizer 3.3.0
docutils           0.20.1
idna               3.4
importlib-metadata 6.8.0
jaraco.classes     3.3.0
keyring            24.2.0
markdown-it-py     3.0.0
mdurl              0.1.2
mergefast          0.1.0     /Users/adam/sandbox/mergefast/mergefast
~~~

<figcaption>Package installed as editable project package inside poetry shell</figcaption>

We can also test the packages the same way as in the [previous article](), using `pip install mergefast-0.1.1.tar.gz` and using using an Earthfile to test installation in a clean container.

That's a great practice. But another testing method available to us it is using `https://test.pypi.org/` to test the publish process end to end.

## Using Test pypi

To use test pypi, go through the same registration and key creation process as on pypi.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4660.png --alt {{  }} %}
<figcaption></figcaption>
</div>
<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4830.png --alt {{  }} %}
<figcaption></figcaption>
</div>

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/4890.png --alt {{  }} %}
<figcaption></figcaption>
</div>

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5400.png --alt {{  }} %}
<figcaption></figcaption>
</div>

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5510.png --alt {{  }} %}
<figcaption></figcaption>
</div>

`poetry publish` can take your API token from `POETRY_PYPI_TOKEN_TESTPYPI`

~~~{.bash caption=">_"}
export POETRY_PYPI_TOKEN_TESTPYPI=pypi-redacted
~~~

Or as a parameter:

~~~{.bash caption=">_"}
poetry publish  --repository testpypi -u __token__ -p your_generated_token
~~~

//Todo -- need to publish mergefast to test
Either way, the key is to tell `poetry publish` to use `--repository testpypi` and your package will publish to [TestPyPi](https://test.pypi.org/project/mergefast/).

~~~{.bash caption=">_"}
> poetry publish --build --repository testpypi -n
There are 2 files ready for publishing. Build anyway? (yes/no) [no] y 
Building mergefast (0.1.1)
  - Building sdist
  - Built mergefast-0.1.1.tar.gz
  - Building wheel
  - Built mergefast-0.1.1-py3-none-any.whl

Publishing mergefast (0.1.1) to PyPI
 - Uploading mergefast-0.1.1-py3-none-any.whl 100%
 - Uploading mergefast-0.1.1.tar.gz 100%

~~~

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/0900.png --alt {{  }} %}
<figcaption>Published as `mergefast`[^1]</figcaption>
</div>

Once that package is up on test pypi, you can test it end to end with `pip install --index-url https://test.pypi.org/simple/ mergefast`. Or as I'm fond of doing wrapping the whole thing up in a Earthfile target, so I can test it end to end.

~~~{.dockerfile caption="Earthfile"}
poetry-test-publish:
    FROM +build
    RUN poetry config repositories.testpypi https://test.pypi.org/legacy/
    RUN poetry publish --build --repository testpypi -n

test-pypi-install:
    FROM python:3.11-buster
    RUN pip install --index-url https://test.pypi.org/simple/ mergefast
    COPY tests .
    RUN python test.py
~~~

Then I can always test the latest test published package on a clean container like this:

~~~{.bash caption=">_"}
> earthly +test-pypi-install
+test-pypi-install | --> COPY +build/dist dist
+test-pypi-install | --> expandargs ls ./dist/*.tar.gz
+test-pypi-install | --> RUN pip install --index-url https://test.pypi.org/simple/ mergefast
...
+test-pypi-install| --> COPY tests .
+test-pypi-install | --> RUN python test.py
+test-pypi-install | timsort took 6.349711754999589 seconds
+test-pypi-install | mergefast took 27.499190239999734 seconds
~~~

# The final poetry publish

And now that we have tested our package end to end, we can publish it with a simple `poetry publish --build`

~~~{.bash caption=">_"}
> poetry publish --build
There are 2 files ready for publishing. Build anyway? (yes/no) [no] y 
Building mergefast (0.1.1)
  - Building sdist
  - Built mergefast-0.1.1.tar.gz
  - Building wheel
  - Built mergefast-0.1.1-py3-none-any.whl

Publishing mergefast (0.1.1) to PyPI
 - Uploading mergefast-0.1.1-py3-none-any.whl 100%
 - Uploading mergefast-0.1.1.tar.gz 100%

~~~

For a simple package like this, this whole teesting workflow might be overkill. But if your package has users and you want to make sure you don't break their worflow I think it makes sense to sanity test your packages.

There is not a lot of ways for packging to o wrong with a single file package, but in the next article we'll look at how to package a c extension, and then testing end to end is really warranted.

[^1]: That actual package shown here is being published as `mergefast`, because it's python only implementation is slow. The fast version is published as `fastmerge` and covered in the third article on packaging c extensions. All code is on [github](https://github.com/earthly/mergefast).

{% include_html cta/bottom-cta.html %}
