---
title: "Python C Extension pypi Package"
categories:
  - Tutorials
toc: true
author: Adam
sidebar:
  nav: "pypi"
---

In covering [publishing my mergefast package with setuptools](/blog/create-python-package/) and [publishing with poetry](/blog/poetry-publish/) I lied about something: that the python code I showed was actually a fast way to merge. The code I showed is slower than just resorting the whole list. ( See [TimSort](/blog/python-timsort-merge) for an explanation. )

I did this for a reason though. To make mergefast fast, we need to write it as a c extension, which significantly complicates publishing. But now we are ready to tackle publishing a c extension to PyPi.

## The Code

To move our code to C, core.py is now going to become core.c ( and core.h ) and this is our central function declaration:

~~~{.c caption="core.h"}
PyObject* merge( PyObject*, PyObject* );
~~~

<figcaption>Here is a our header. ( [full source](https://github.com/earthly/mergefast/tree/v2/mergefast) )</figcaption>

We also have a bind.c, where there are a lot of little details to get right. Lets go slowly through them, as this is where I initially got stuck.

### 1. Declaring Our PyMethodDef Function

~~~{.c caption="bind.c"}
#include "core.h"

PyMethodDef merge_funcs[] = {
    {
        "merge", /* function name */
        (PyCFunction)merge,
        METH_VARARGS,
        "merge two sorted lists" /* function docs */
    },
    { NULL }
};
~~~

- We declare an array of `PyMethodDef` structures named `merge_funcs`.
- Each `PyMethodDef` structure represents a method that will be made available in our Python module. We just have one for now.
- The structure has the following elements:
  - `"merge"`: The name of the function as it will appear in Python.
  - `(PyCFunction)merge`: The actual C function that implements this method.
  - `METH_VARARGS`: A flag indicating the calling convention of our function.
  - `"merge two sorted lists"`: A documentation string for the function.
- The `{ NULL }` entry serves as a sentinel, signaling the end of the method definitions.

### 2. Defining Our Module

~~~{.c caption="bind.c"}
PyModuleDef merge_mod = {
    PyModuleDef_HEAD_INIT,
    "core", /* library name */
    "core module", /* module docs */
    -1,
    merge_funcs,
    NULL,
    NULL,
    NULL,
    NULL
};
~~~

- Next we define a module (`PyModuleDef`) structure named `merge_mod` representing the module we are creating.
- `PyModuleDef_HEAD_INIT`: A required boilerplate initialization.
- `"core"`: The name of our module.
- `"core module"`: A documentation string for our module.
- `-1`: Refers to the size of the module state in bytes, with `-1` indicating module-level state only.
- `merge_funcs`: The previously defined array of methods.

Everything, after that is optional, so we pass NULL for now.

### 3. Defining Our Init Function

~~~{.c caption="bind.c"}
PyMODINIT_FUNC PyInit_core( void )
{
    return PyModule_Create( &merge_mod );
}
~~~

Next up is Init. And guess what, it initializes our module.

- `PyMODINIT_FUNC` is a macro that ensures that the function has the correct return type and visibility to be used as a module initialization function.
- `PyInit_core`: The name is significant. If our module is named "X", then the initialization function must be named `PyInit_X`.

Python calls this when the module is imported. We then use `PyModule_Create` to create and return a new module object based on our `merge_mod` definition above.

## C Extension Building With SetupTools

Now we are ready to build our extension. Even though we are using poetry, which has a nice built in build and publish functionality, I found using setup tools directly with a setup.py the easiet way to build.

( It's possible to configure some of setuptools via pyproject.toml, but it's tricky and beyond our scope here. )

So, create a `setup.py`:

~~~{.c caption="setup.py"}
from setuptools import setup, Extension, find_packages

merge_module = Extension(
    "mergefast.core",
    sources=["mergefast/bind.c", "mergefast/core.c"],
    include_dirs=["mergefast"],
    extra_compile_args=["-O3"]
)
~~~

1. **`"mergefast.core"`**:

   This is the name of the extension module we are building. `mergefast.core` will be a submodule of `mergefast`.

1. **`sources=["mergefast/bind.c", "mergefast/core.c"]`**:

  These are the source files that need to be compiled to produce or extension.

1. **`include_dirs=["mergefast"]`**:

   This specifies directories where the compiler should look for header files during the compilation process. Without this `core.h` won't be found.

1. **`extra_compile_args=["-O3"]`**:

   Here we are just using the `-O3` flag to apply high-level optimizations to improve performance. We are aiming for maximum execution speed.
  
Next, we call `setup()`:

~~~{.python caption="setup.py"}
setup(
    name="mergefast",
    version="1.1.3",
    packages=find_packages(),
    ext_modules=[merge_module],
)
~~~

Most of this is straight-forward. The first two lines, we are naming our package and versioning it. `ext_modules=[merge_module]` tells setuptools to compiler our `mergefast.core` package previously defined.

The third line, `packages=find_packages()`, is a bit trickier. The find_packages() function is a utility from setuptools that automatically discovers all Python packages in your project directory. This is essential for getting our `__init__.py` file into the final package.

Our `__init__.py` imports core, so `import mergefast.merge` works and without `find_packages()` it won't be included in our package.

~~~{.python caption="__init__.py"}
from mergefast.core import merge_int, merge_float, merge_latin, merge

~~~

Without that, our package will work fine locally as a project location based package in poetry, but `import mergefast` won't work when install as a package.

( Highlighting the value of testing the package installation process. )

## Build and Test in Place

With that setup.py setuptools code in place, we can compile and test our solution.

~~~{.bash caption=">_"}
> poetry install
Installing dependencies from lock file
...
> poetry shell
Creating virtualenv mergefast-95GN-TFI-py3.11 in /Users/adam/Library/Caches/pypoetry/virtualenvs
Spawning shell within /Users/adam/Library/Caches/pypoetry/virtualenvs/mergefast-95GN-TFI-py3.11
Traceback (most recent call last):
  File "/Users/adam/sandbox/mergefast/mergefast/tests/test.py", line 1, in <module>
    import mergefast
  File "/Users/adam/sandbox/mergefast/mergefast/mergefast/__init__.py", line 1, in <module>
    from mergefast.core import merge_int, merge_float, merge_latin, merge
ModuleNotFoundError: No module named 'mergefast.core'
~~~

Oh no. More work to do. You see we have our `mergefast` package, but we need to compile our `core` module.

~~~{.bash caption=">_"}
> python setup.py build_ext --inplace
python setup.py build_ext --inplace
running build_ext
building 'mergefast.core' extension
creating build
creating build/temp.macosx-13-arm64-cpython-311
creating build/temp.macosx-13-arm64-cpython-311/mergefast
clang -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX13.sdk -Imergefast -I/Users/adam/Library/Caches/pypoetry/virtualenvs/mergefast-95GN-TFI-py3.11/include -I/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/include/python3.11 -c mergefast/bind.c -o build/temp.macosx-13-arm64-cpython-311/mergefast/bind.o -O3
clang -Wsign-compare -Wunreachable-code -fno-common -dynamic -DNDEBUG -g -fwrapv -O3 -Wall -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX13.sdk -Imergefast -I/Users/adam/Library/Caches/pypoetry/virtualenvs/mergefast-95GN-TFI-py3.11/include -I/opt/homebrew/opt/python@3.11/Frameworks/Python.framework/Versions/3.11/include/python3.11 -c mergefast/core.c -o build/temp.macosx-13-arm64-cpython-311/mergefast/core.o -O3
creating build/lib.macosx-13-arm64-cpython-311
creating build/lib.macosx-13-arm64-cpython-311/mergefast
clang -bundle -undefined dynamic_lookup -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX13.sdk build/temp.macosx-13-arm64-cpython-311/mergefast/bind.o build/temp.macosx-13-arm64-cpython-311/mergefast/core.o -o build/lib.macosx-13-arm64-cpython-311/mergefast/core.cpython-311-darwin.so
copying build/lib.macosx-13-arm64-cpython-311/mergefast/core.cpython-311-darwin.so -> mergefast
~~~

And then we test run our c based merge

~~~{.bash caption=">_"}
python tests/test.py
timsort took 2.2706818750011735 seconds
merge took 2.0606187919911463 seconds
~~~

And we are faster then [timsort](/blog/python-timsort-merge)!

## Binary Package Woes

It's worth noting the above build produces `core.cpython-311-darwin.so` on my M1 mac. It will produce something different if you are on windows or linux and this adds challenges when it becomes time to produce our `.whl`.

~~~{.bash caption=">_"}
> python setup.py bdist_wheel
running bdist_wheel
running build
running build_py
...
creating 'dist/mergefast-1.1.3-cp311-cp311-macosx_13_0_arm64.whl'
~~~

The created wheel file is `mergefast-1.1.3-cp311-cp311-macosx_13_0_arm64.whl`

Because the c extension functionality is closely tied to the python version, this shared object file is just for 3.11 `cp311-cp311`. And because this wheel contains native code, its specific to the OS and architecture its compiled for (`macosx_13` and `arm64`).

Want to pip install from PyPi on different systems, like not arm64 or not macOS x? Good news: You just have to build a wheel for each system and then upload them all. But, there's a catch. Even with things like `manylinux`, you'll need the right machines. Virtual or real ones with the systems you're building for.

Many use GitHub actions matrix builds to accomplish this:

~~~{.yaml caption="workflow.yaml"}
  build_wheels:
    name: Build wheels on ${{ matrix.os }}  - ${{ matrix.vers }}
    runs-on: ${{ matrix.os }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - vers: i686
            os: ubuntu-20.04
          - vers: aarch64
            os: ubuntu-20.04
          - vers: auto64
            os: ubuntu-20.04
          - vers: arm64
            os: macos-10.15
          - vers: auto64
            os: macos-10.15
          - vers: auto64
            os: windows-2019
~~~

<figcaption>matrix wheel build of [poloaroid](https://github.com/Daggy1234/polaroid/blob/main/.github/workflows/publish.yml) package.</figcaption>

Let's skip all that for now, though, by doing a source build.

## Source Build to the Rescue

When you use pip install, pip picks the best format for your package. It likes wheels because they often have pre-compiled code. This makes installation faster and skips the build step.

If pip can't find a wheel, it uses the source distribution and compiles during installation.

The downside? The user needs a C compiler. But, as long as you have the python.h header file, that's the only constraint for our small extension. No need for a complex matrix build. Let's proceed with that approach.

~~~{.bash caption=">_"}
> python3 setup.py sdist
...

producing mergefast-1.1.3.tar.gz
~~~

We can test this package with a `pip install dist/mergefast-1.1.3.tar.gz`. I, of course, do this [Earthly](/), for reproducibility sake:

~~~{.dockerfile caption="Earthfile"}
test-dist-install:
    FROM python:3.11-buster
    COPY +build/dist dist
    ENV TARFILE=$(ls ./dist/*.tar.gz)
    RUN pip install "$TARFILE"
    COPY tests .
    RUN python test.py

~~~

Which gives:

~~~
> pip install dist/mergefast-1.1.3.tar.gz
 Building wheel for mergefast (pyproject.toml) did not run successfully.
  │ exit code: 1
  ╰─> [21 lines of output]
      running bdist_wheel
      ... 
      gcc -pthread -Wsign-compare -DNDEBUG -g -fwrapv -O3 -Wall -fPIC -Imergefast -I/usr/local/include/python3.11 -c mergefast/bind.c -o build/temp.linux-x86_64-cpython-311/mergefast/bind.o -O3
      mergefast/bind.c:1:10: fatal error: core.h: No such file or directory
       #include "core.h"
~~~

Failure! You can see that on installation pip runs the `bdist_wheel` process which works ok, until we try to include our header file core.h.  

## MANIFEST.in

You see, the python `sdist` process knows to include all the python files in a package into the source distribution, but it really has no idea about what other files are needed to build the project. In my perfect world, it would be able to infer from some heuristics to include_dirs=["mergefast"].

That's not the world we live in though, so setuptools supports a `MANIFEST.in` file, where you describe all the extra files your package needs.

~~~{.ini caption="MANIFEST.in"}
include mergefast/*.c
include mergefast/*.h
include mergefast/*.py

~~~

With that in place, installing from a source distribution works:

~~~
  > earthly +test-dist-install
  ...
  +test-dist-install | --> RUN python test.py
  +test-dist-install | timsort took 5.315027578999434 seconds
  +test-dist-install | merge_int took 1.7830523350021394 seconds
  +test-dist-install | merge took 4.74845955499768 seconds
~~~

Now all I need to do is publish:

~~~{.bash caption=">_"}
> poetry publish -n
Publishing mergefast (1.1.3) to pypi
 - Uploading mergefast-1.1.3.tar.gz 100%
~~~

And just like that we have our package on PyPi:

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/9880.png --alt {{ package on pypi }} %}
<figcaption>[And it's up](https://pypi.org/project/mergefast/)</figcaption>
</div>

( If you'd like to see how to test the package before pushing see the earlier article on [TestPyPi(/blog/poetry-publish).)

## Conclusion

All the code for `mergefast`, and its earlier python implementation `mergeslow` are up on [github](https://github.com/earthly/mergefast). Of course, I have wrapped all these stages of building, local package installing, pushing to TestPyPi and pushing to actual PyPi inEarthfile targets.

That way I don't need to head back to this tutorial each time to remember how to run each step.

I hope this three part series is useful. This last stage, the python extension packaging was a little trickier then I thought it would be, but now that I've walked myself through it all makes a good amount of sense.

It goes to show that behind the ease of `pip install` there is lots of unsexy but needed packaging, building and distribution work happening.  

( Take a look at the pip packaging code for a lib like [TensorFlow](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/tools/pip_package) sometime to see how complex things can get. )

And if you want to know about the next article in the series, subscribe to the newsletter. I'm probably going to attempt a python extension in Rust soon.

{% include_html cta/bottom-cta.html %}
