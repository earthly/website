---
title: "Create a Python Package using Setup.py and Poetry"
categories:
  - Tutorials
toc: true
author: Adam
---

# Intro

# My code
```
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

```

# Registrying on pypi and pypi staging

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


# Choosing A Package Name

Orginally I had called this package `PyMerge`. There a number of problems with that, including that this name has been taken already.

When I orginally used twine to push it I got this:

```
HTTP Error 403: The user 'adamgordonbell' isn't allowed to upload to project 'PyMerge'. See https://pypi.org/help/#project-name for more information. | b"<html>\n <head>\n  <title>403 The user 'adamgordonbell' isn't allowed to upload to project 'PyMerge'. See https://pypi.org/help/#project-name for more information.\n \n <body>\n  <h1>403 The user 'adamgordonbell' isn't allowed to upload to project 'PyMerge'. See https://pypi.org/help/#project-name for more information.\n  Access was denied to this resource.<br/><br/>\nThe user &#x27;adamgordonbell&#x27; isn&#x27;t allowed to upload to project &#x27;PyMerge&#x27;. See https://pypi.org/help/#project-name for more information.\n\n\n \n"
```

This forced my to look for a new name and its a good thing I did because it turns out `PyMerge` is a horrible name. When selecting a name for your package, follow these rules set forth by the Python Packaging Authority (PyPA):

- *Keep It Short & Descriptive:* Names should be short, but also give a clear idea of what the package does. For example, requests is a popular library that makes HTTP requests.

- *Avoid Underscores:* Although underscores are allowed, dashes are more common in package names. However, note that the actual module or package inside might use underscores (e.g., the package dateutil on PyPI corresponds to the date_util module when imported in Python).

- *Avoid Uppercase Letters:* Lowercase names are conventional for package names. This makes them easy to type and avoids ambiguity on case-sensitive file systems.

- *Check for Name Availability:* Before finalizing a name, search on PyPI to ensure that the name isn't already taken. Even if it's available, avoid names that are too similar to existing packages to prevent confusion.

- *Avoid Generic Names:* Names that are too generic can be misleading. For example, a package named data would be too vague.

- *Prefixes/Suffixes:* If your package is an extension or related to another package, consider using a prefix or suffix. For instance, flask- is a common prefix for Flask extensions (e.g., flask-login).

- *Avoid "Py" Prefix:* While many packages use the "py" prefix to indicate they are Python packages (e.g., pyspark, pytz), it's become somewhat redundant since the package will be on PyPI, and it's understood that it's for Python. However, it's not a strict rule, and some popular packages still use it.

- *Convey Main Benefit or Feature:* If possible, the name should convey the main benefit or feature of the package. For a merge algorithm that's faster, words like "fast", "speed", "quick", "swift", or "turbo" could be part of the name.

So, you can see `PyMerge` broke almost all of these rules and so I settled on the name `mergefast`[^1] which meets all the rules.

# Setup.py and Twine package publishing

## Setup.py
```
from setuptools import setup, find_packages

setup(
    name='mergefast',
    version='0.1.3',
    packages=find_packages(),
    description='A simple package for merging lists.',
    author='Adam Gordon Bell',
    author_email='adam@earthly.dev'
)
```

## Source Dists and Wheels

```
python3 setup.py sdist
```
Or the newer recommended `python build`

```
python -m build --sdist
```
Or the newer recommended `python build` [^2]

```
python -m build --sdist
```

```
running sdist
running egg_info
creating mergefast.egg-info
writing mergefast.egg-info/PKG-INFO
writing dependency_links to mergefast.egg-info/dependency_links.txt
writing top-level names to mergefast.egg-info/top_level.txt
writing manifest file 'mergefast.egg-info/SOURCES.txt'
reading manifest file 'mergefast.egg-info/SOURCES.txt'
writing manifest file 'mergefast.egg-info/SOURCES.txt'
running check
creating mergefast-0.1.3
creating mergefast-0.1.3/mergefast
creating mergefast-0.1.3/mergefast.egg-info
creating mergefast-0.1.3/tests
copying files to mergefast-0.1.3...
copying README.md -> mergefast-0.1.3
copying pyproject.toml -> mergefast-0.1.3
copying setup.py -> mergefast-0.1.3
copying mergefast/__init__.py -> mergefast-0.1.3/mergefast
copying mergefast/core.py -> mergefast-0.1.3/mergefast
copying mergefast.egg-info/PKG-INFO -> mergefast-0.1.3/mergefast.egg-info
copying mergefast.egg-info/SOURCES.txt -> mergefast-0.1.3/mergefast.egg-info
copying mergefast.egg-info/dependency_links.txt -> mergefast-0.1.3/mergefast.egg-info
copying mergefast.egg-info/top_level.txt -> mergefast-0.1.3/mergefast.egg-info
copying tests/__init__.py -> mergefast-0.1.3/tests
copying tests/test.py -> mergefast-0.1.3/tests
Writing mergefast-0.1.3/setup.cfg
Creating tar archive
removing 'mergefast-0.1.3' (and everything under it)
```

```
mergefast
├── README.md
├── dist
│   └── mergefast-0.1.3.tar.gz
├── mergefast
├── mergefast.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── setup.py

```
We can do the same thing to produce a wheel, which is compiled version of the package.

```
python3 setup.py bdist_wheel
```
Or the newer version of the command

```
python -m build --wheel
```
```
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (setuptools >= 40.8.0, wheel)
* Getting build dependencies for wheel...
running egg_info
creating mergefast.egg-info
writing mergefast.egg-info/PKG-INFO
writing dependency_links to mergefast.egg-info/dependency_links.txt
writing top-level names to mergefast.egg-info/top_level.txt
writing manifest file 'mergefast.egg-info/SOURCES.txt'
reading manifest file 'mergefast.egg-info/SOURCES.txt'
writing manifest file 'mergefast.egg-info/SOURCES.txt'
* Installing packages in isolated environment... (wheel)
* Building wheel...
running bdist_wheel
running build
running build_py
creating build
creating build/lib
creating build/lib/tests
copying tests/__init__.py -> build/lib/tests
copying tests/test.py -> build/lib/tests
creating build/lib/mergefast
copying mergefast/__init__.py -> build/lib/mergefast
copying mergefast/core.py -> build/lib/mergefast
installing to build/bdist.macosx-13-arm64/wheel
running install
running install_lib
creating build/bdist.macosx-13-arm64
creating build/bdist.macosx-13-arm64/wheel
creating build/bdist.macosx-13-arm64/wheel/tests
copying build/lib/tests/__init__.py -> build/bdist.macosx-13-arm64/wheel/tests
copying build/lib/tests/test.py -> build/bdist.macosx-13-arm64/wheel/tests
creating build/bdist.macosx-13-arm64/wheel/mergefast
copying build/lib/mergefast/__init__.py -> build/bdist.macosx-13-arm64/wheel/mergefast
copying build/lib/mergefast/core.py -> build/bdist.macosx-13-arm64/wheel/mergefast
running install_egg_info
running egg_info
writing mergefast.egg-info/PKG-INFO
writing dependency_links to mergefast.egg-info/dependency_links.txt
writing top-level names to mergefast.egg-info/top_level.txt
reading manifest file 'mergefast.egg-info/SOURCES.txt'
writing manifest file 'mergefast.egg-info/SOURCES.txt'
Copying mergefast.egg-info to build/bdist.macosx-13-arm64/wheel/mergefast-0.1.3-py3.11.egg-info
running install_scripts
creating build/bdist.macosx-13-arm64/wheel/mergefast-0.1.3.dist-info/WHEEL
creating '/Users/adam/sandbox/mergefast/mergefast/dist/.tmp-9qcuhgte/mergefast-0.1.3-py3-none-any.whl' and adding 'build/bdist.macosx-13-arm64/wheel' to it
adding 'mergefast/__init__.py'
adding 'mergefast/core.py'
adding 'tests/__init__.py'
adding 'tests/test.py'
adding 'mergefast-0.1.3.dist-info/METADATA'
adding 'mergefast-0.1.3.dist-info/WHEEL'
adding 'mergefast-0.1.3.dist-info/top_level.txt'
adding 'mergefast-0.1.3.dist-info/RECORD'
removing build/bdist.macosx-13-arm64/wheel
Successfully built mergefast-0.1.3-py3-none-any.whl
```

This gives you a wheel:

```
.
├── Earthfile
├── README.md
├── build
├── dist
│   └── mergefast-0.1.3-py3-none-any.whl
├── mergefast.egg-info
│   ├── PKG-INFO
│   ├── SOURCES.txt
│   ├── dependency_links.txt
│   └── top_level.txt
├── setup.py
```

The Wheel `whl` generated tells us a lot about the package:

mergefast: This is the package name.

0.1.3: This is the version number of the package.

py3: This indicates that the package is compatible with Python 3. It doesn't specify an exact version, so the package is expected to work with any Python 3 version. If it were py2.py3, that would mean it's compatible with both Python 2 and Python 3.

none: This refers to the ABI (Application Binary Interface). "None" means that the package does not contain any compiled extensions or is not ABI-specific. If the package contained compiled code specific to a certain ABI, you would see a different tag here.

any: This denotes the platform. "Any" means the package is platform-independent. If the package contained compiled binaries specific to a platform, you might see something like manylinux1_x86_64 (for a specific Linux standard on 64-bit).

We'll get into generating wheels for compiled extensions in the next article, but for now It's interesting to note that this wheel because its python only can be used on any python3 installation. And that is great for users of our package on pypi. We don't even need the source distribution as fallback. 

# Testing The Package

Ok, one of the tricky things about distributing your package to pypi that you should know is that once upload a package to pypi with a version number you cannot change it. 

You can remove it, using the delete button in pypi and there are some otehr tricks but basically once its up there is up there. So you want to make suer you package works before you put it up on pypi. Ideally you'd want to make sure it works even on differnt host operating systems. But how can you test the package? Luckily there are several ways to test it. 

We can test the source distribution locally, after using pip install:

```
> pip install ./dist/mergefast-0.1.3.tar.gz
 Processing /dist/mergefast-0.1.3-py3-none-any.whl
 Installing collected packages: mergefast
 Successfully installed mergefast-0.1.3
```

Then we can test it with [`test.py`](https://github.com/earthly/mergefast/blob/main/mergefast/tests/test.py) or just jump into the python repl and test it out.

```
python test.py
timsort took 5.440176733998669 seconds
mergefast took 3.710623259001295 seconds
```

We can test the `whl` the same way.
```
pip install mergefast-0.1.3.tar.gz
python test.py
timsort took 5.440176733998669 seconds
mergefast took 3.710623259001295 seconds
```

And everything seems to work! But how do we verify that this package is not dependent on some local setup or file that I've forgotten to include? It's easy actually to take things a bit further.

## Earthfile Test

The easiet way to test the package across environments is before pushing to pypi is to use containers. I like to use Earthly for this. All I need to do is wrap the steps we've already covered up into an Earthfile target:

```
test-dist-tar-install:
    FROM python:3.11-buster
    COPY +build/dist dist
    ENV TARFILE=$(ls ./dist/*.tar.gz)
    RUN pip install "$TARFILE"
    COPY tests .
    RUN python test.py
```

In `test-dist-tar-install` I start from a python base image, copy from my [build step]((https://github.com/earthly/mergefast/blob/main/mergefast/Earthfile)), and then install the tar file we build and test it. ( Full Earthfile on [GitHub](https://github.com/earthly/mergefast/blob/main/mergefast/Earthfile). )

Then I can test the package installation at any time by running `earthly +test-dist-tar-install` and seeing the test pass:

```
+test-dist-tar-install | --> COPY +build/dist dist
+test-dist-tar-install | --> expandargs ls ./dist/*.tar.gz
+test-dist-tar-install | --> RUN pip install "$TARFILE"
+test-dist-tar-install | Processing /dist/mergefast-0.1.3.tar.gz
+test-dist-tar-install | --> COPY tests .
+test-dist-tar-install | --> RUN python test.py
+test-dist-tar-install | timsort took 6.349711754999589 seconds
+test-dist-tar-install | mergefast took 27.499190239999734 seconds
```
I can use the same extact process to test the wheel:

```
test-dist-whl-install:
    FROM python:3.11-buster
    COPY +build/dist dist
    ENV WHLFILE=$(ls ./dist/*.whl)
    RUN pip install "$WHLFILE"
    COPY tests .
    RUN python test.py
```

And with that I have a truly solid way to test before I push it to pypi. 

## Twine PyPi Push

Ok, let's push it. To push our package we are going to use [twine](https://pypi.org/project/twine/). 

First thing to do is head back to pypi and setup an API key.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5110.png --alt {{  }} %}
<figcaption></figcaption>
</div>

Setup ENVs for twine with you API Key:

```
export TWINE_USERNAME=__token__
export TWINE_PASSWORD=**************
```
Install twine:
```
pip install twine
```
Then use twine to upload:
```
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
Todo: output
For ease of publishing in the future, I put this whole thing in my Earthfile:

Todo: Add secrets
```
twine-publish:
    FROM +build
    COPY +build/dist dist
    RUN twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

## Testing Again

And with that, our package is on pypi. We can test it by removing our on package and reinstalling from pypi:

```
pip uninstall mergefast --yes
...
pip install mergefast
...
python test.py
 timsort took 5.440176733998669 seconds
 mergeslow took 2.71025900331295 seconds
```

Of course, I put this all as a target in in the Earthfile for ease of testing:
```
test-pypi-install:
    FROM python:3.11-buster
    RUN pip install mergefast
    COPY tests .
    RUN python test.py
```

And with that we have a published package. There is more to cover though. Next up is publishing with Poetry, which simplifies some of this process, publishing to test.pypi.com and publishing python extensions which use C. Native code does complicate things.

IF you want to skip ahead, my code is on [GitHub](https://github.com/earthly/mergefast/tree/main) and the Earthfile that pulls it all together is [there as well](https://github.com/earthly/mergefast/blob/main/mergefast/Earthfile).

{% include_html cta/bottom-cta.html %}


[^1]: That actual package shown here is being published as `slowmerge`, because it's python only implementation is slow. The fast version is published as `fastmerge` and covered in the next article on packaging c extensions. All code is on [github](https://github.com/earthly/mergefast).

[^2]: See [this blog post](https://blog.ganssle.io/articles/2021/10/setup-py-deprecated.html#summary) for details.
