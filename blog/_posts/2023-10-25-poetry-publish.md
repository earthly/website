---
title: "Poetry Build and Publish"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "pypi"
---
[Last time](/blog/create-python-package) I showed you how to publish a package to PyPI using setup.py. But if you are using poetry, and [you should be](/blog/python-poetry/), then there is an even easier way. Let me walk you all the way through it, including how to push to `test.pypi.org` for testing purposes. But if you want to skip ahead, know you just have to run `poetry publish --build` on a properly configured poetry project.

## Code

Just like last time, I have this python code I want to get on PyPI as a package:

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
> pip install poetry
...
> poetry new mergefast 
Created package mergefast in mergefast
~~~

Doing that creates the structure for my package:

~~~{.ini}
.
├── README.md
├── mergefast
│   └── __init__.py
├── pyproject.toml
└── tests
    └── __init__.py
~~~

For there I just need to copy my code into `core.py` and add my [test.py](https://github.com/earthly/mergefast/blob/v2/mergefast/tests/test.py) into the project.

Let's look at the `pyproject.toml`:

~~~{.toml caption="pyproject.toml"}
[tool.poetry]
name = "mergefast"
version = "0.1.1"
description = ""
authors = ["Adam Gordon Bell <adam@earthly.dev>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
~~~

You can see that name, version, and other details traditionally configured in a setup.py are already here. That makes building the distribution simple.

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

This will build both a source distribution and a wheel. To build each separately use `poetry build --format sdist` and `poetry build --format wheel`.

## Testing the Package

Because of Poetry's focus on virtual environments, possible to test package without even building it.

~~~{.bash caption=">_"}
> poetry shell
Spawning shell within /Users/adam/Library/Caches/pypoetry/virtualenvs/mergefast.
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

We can also test the packages the same way as in the [setuptools based article](/blog/create-python-package/), using `pip install mergefast-0.1.1.tar.gz` and using an Earthfile to test installation in a clean container.

That's a great practice. But another testing method available to us it is using `https://test.pypi.org/` to test the publish process end to end.

## Using Test PyPi

<div class="align-right">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9020.png --picture --img width="300px" --alt {{ Create an account at test.pypy.org }} %}
<figcaption>Create an account at test.pypy.org</figcaption>
</div>
[TestPyPI](test.pypi.org) is a separate instance of the Python Package Index (PyPI) designed specifically for testing and experimentation. It allows developers to practice the process of packaging and publishing their Python projects without affecting the main PyPI repository.

It's basically a staging release location we can use to test things out.

To use TestPyPI, go through the same registration and key creation process as on PyPI.

- Create an Account
- Setup 2-Factor Auth
- Create an API Key

Once you have your API key, poetry can take your API token in `POETRY_PYPI_TOKEN_TESTPYPI`.

~~~{.bash caption=">_"}
export POETRY_PYPI_TOKEN_TESTPYPI=pypi-redacted
~~~

Or it can be passed as a parameter to `poetry publish`, if you indicate `--repository testpypi` :

~~~{.bash caption=">_"}
poetry publish  --repository testpypi -u __token__ -p your_generated_token
~~~

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
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9660.png --alt {{ Publishing `mergefast` }} %}
<figcaption>Publishing `mergefast`[^1]</figcaption>
</div>

Once that package is up on test PyPI, you can test it end to end with `pip install --index-url https://test.pypi.org/simple/ mergefast`. Or as I'm fond of doing wrapping the whole thing up in a Earthfile target, so I can test it end to end.

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

## The Final Poetry Publish

And now that we have tested our package end to end, we can publish it onto [PyPi.org](https://pypi.org/project/mergefast/) with a simple `poetry publish --build`

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

And there you go, the package is published and you have a [repeatable process](https://github.com/earthly/mergefast/blob/v2/mergeslow/Earthfile) for doing so. For Python only packages, `poetry publish` is a simple way to go. No need for setuptools and `setup.py` at all.

For a simple package like this, this whole testing workflow might be overkill. But if your package has users and you want to make sure you don't break their workflow I think it makes sense to sanity test your packages.

## Next Up: C Extensions

Next up, let's tackle the c version of this code and publish a python c extension on to PyPi. Publishing a native extension is a bit trickier, but we now have the skills to easily tackle this problem. The testing setup we've established here, with Earthly and test.pypy.org and our knowledge of poetry and setup tools will all come together in [part three](/blog/python-c-extension/)

There is not a lot of ways for packaging to wrong with a single file package, but in the next article, testing end to end is will really pay off.

[^1]: That actual current version of `mergefast` is published in [packaging c extensions](/blog/python-c-extension/). This python only implementation is published as `mergeslow`. Both and full source is on [github](https://github.com/earthly/mergefast).

{% include_html cta/bottom-cta.html %}
