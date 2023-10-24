---
title: "Python C Extension pypi Package"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---

In covering [publishing my mergefast package with setuptools]() and [publishig it with poetry]() I lied about something: that is was actually a fast way to merge. The python code I showed can't compete with just resorting the list. ( See [TimSort]() for a lengthly explanation. )

I did this for a reason though. To make mergefast actually fast, we need to write it as a c extension, which significantly complicates publishing. But now we are ready to tackle publishing a c extension to pypi.

## The Code

To move our code to C, core.py is now going to become core.c ( and core.h ) and and defines this new merge call:

```
PyObject* merge( PyObject*, PyObject* );
```

We also have a bind.h, where there are a lot of little details to get right. Lets go slowly through them, as this is where I initially got stuck.


### 1. Declaring our function in a null-terminated list

```c
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
```

- This snippet declares an array of `PyMethodDef` structures named `merge_funcs`.
- Each `PyMethodDef` structure represents a method that will be made available in our Python module. We just have one for now.
- The structure has the following elements:
  - `"merge"`: The name of the function as it will appear in Python.
  - `(PyCFunction)merge`: The actual C function that implements this method. 
  - `METH_VARARGS`: A flag indicating the calling convention of our function. In this case, it suggests that our function accepts any number of arguments packed into a tuple.
  - `"merge two sorted lists"`: A documentation string for the function.
- The `{ NULL }` entry serves as a sentinel, signaling the end of the method definitions.

### 2. Defining our module

```c
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
```

- This snippet defines a `PyModuleDef` structure named `merge_mod`.
- `PyModuleDef` represents the module we're creating.
- The elements in this structure are:
  - `PyModuleDef_HEAD_INIT`: A required boilerplate initialization.
  - `"core"`: The name of our module.
  - `"core module"`: A documentation string for our module.
  - `-1`: Refers to the size of the module state in bytes, with `-1` indicating module-level state only.
  - `merge_funcs`: The previously defined array of methods.
- The remaining `NULL` optional values. 

### 3. Defining our init function

```c
PyMODINIT_FUNC PyInit_core( void )
{
	return PyModule_Create( &merge_mod );
}
```

- This function is the initialization function for our module.
- It's crucial as Python calls this function when the module is imported. 
- `PyMODINIT_FUNC` is a macro that ensures that the function has the correct return type and visibility to be used as a module initialization function.
- `PyInit_core`: The name of this function is significant. If our module is named "core", then the initialization function must be named `PyInit_core`.
- Within this function, we use `PyModule_Create` to create and return a new module object based on our `merge_mod` definition above.

## C Extension Building With SetupTools

Now we are ready to build our extension. Now even though we are using poetry which has a nice built in build funcitonality us pyproject.toml, I found using setup tools directly with a setup.py the easiet way to build. [^1]


```

```
Insert here:
https://chat.openai.com/c/51d7ce67-cbc8-4177-acda-6ba63d7033ff


[^1]: It's possible to tell poetry to build via setuptools. And configure in pyproject.toml

```
[tool.setuptools]
name = "mergefast"
version = "1.1.3"

[tool.setuptools.extension."mergefast.core"]
sources = ["mergefast/bind.c", "mergefast/core.c"]
include_dirs = ["mergefast"]
extra_compile_args = ["-O3"]
```
