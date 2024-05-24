---
title: "Getting Started With CMake"
toc: true
author: Kasper Siig
sidebar:
  nav: "makefile"
internal-links:
 - make
 - makefile
 - cmake
excerpt: |
    Learn how to use CMake, a popular tool for building applications in the C++ community. This tutorial provides a step-by-step guide on using CMake to configure a build pipeline and compile a simple C++ application.
last_modified_at: 2023-07-14
categories:
  - cli
---
**This article explains how to use CMake in C++ projects. Earthly improves C++ builds with CMake integration. [Learn how](https://cloud.earthly.dev/login).**

When it comes to packaging an application, there are many ways to do it. However, with languages that have been around as long as C and C++, the community has converged around some de facto standards. Especially in the C++ community, the standard is to use [CMake](https://cmake.org) when building your applications.

There are other options to use for building applications, including [autoconf](/blog/autoconf/) and [BJam](https://www.boost.org/doc/libs/1_43_0/doc/html/jam/usage.html); however, as mentioned before, CMake helps build applications—*help* being the keyword. It's very important to note that CMake does *not* build any applications; that's a job for the compiler. Instead, CMake provides a way for developers to configure a build pipeline easily, as well as make sure it works cross-platform.

In this tutorial, you'll be giving an overview of how to use CMake in general, using a simple `C++` application as an example. Once the basic use case has been covered, you'll also be introduced to how you can take CMake implementations to the next level.

If you want to clone the project and follow along in your own editor, here is the link to the [GitHub repo](https://github.com/KSiig/cmake-tutorial).

## The Simplest Way to Use CMake

Since CMake is a tool that's meant to aid you in building your applications, you need to have an application to begin with. For this tutorial, you're going to build a very simple two-file application that can add two numbers together.

### Creating the Application

Start off by creating an empty directory and then enter it. In here, you want to create a folder called `src`, in which you create two files: `main.cpp` and `add.cpp`. In `main.cpp`, add the following code:

~~~{.bash caption=">_"}
#include <iostream>

int add(int x, int y);

int main()
{
    std::cout << "Adding 2 and 9 together gives you: " << add(2, 9) << '\n';
    return 0;
}
~~~

And in `add.cpp`, add the following:

~~~{.bash caption=">_"}
int add(int x, int y)
{
    return x + y;
}
~~~

Now that you have the two files needed for your application, you need to manually compile them to make sure everything is working as expected:

~~~{.bash caption=">_"}
gcc src/main.cpp src/add.cpp -lstdc++
~~~

> Note: It's assumed that you're using [Linux](https://www.linux.org) and, by extension, [GCC (the GNU Compiler Collection)](https://gcc.gnu.org) for this part; however, please compile for your specific OS. For the rest of this tutorial, your OS should be irrelevant.

The previous command should be able to run without any issues. If you do run into any issues, please check that your compiler is the latest version and that you've correctly copied the code.

### Adding CMake

Now that you've created the sample application, it's time to add CMake to the project.

To begin, you need to create the file `CMakeLists.txt` in the root directory of your application. This file defines everything related to your use of CMake. Here, you'll define the name of your application, what files are included, if any libraries are needed, and more. The `CMakeLists.txt` file has a very long list of possibilities, but there are a few things that every `CMakeLists.txt` file *needs* to have. The first of these is the `cmake_minimum_required()` line.

As can likely be assumed from the name of the command, this specifies the lowest version that you want to support. The general rule of thumb is that you want to specify a version of CMake that is later than your compiler. This is because CMake needs to know the various options and flags of your compiler. This article uses GCC v9.3 to compile, which came out in March 2020. The next version of CMake to come out is v3.17, which is the minimum version needed here:

~~~{.bash caption=">_"}
cmake_minimum_required(VERSION 3.17)
~~~

Now you need to add some information about your application using the `project()` command:

~~~{.bash caption=">_"}
project(CMakeTutorial
    VERSION 1.0
    DESCRIPTION "A CMake Tutorial"
    LANGUAGES CXX)
~~~

Here, you define four things: the name of the application (`CMakeTutorial`), the defined version (`1.0`), a description of the application (`A CMake Tutorial`), and the language of the application (`CXX` meaning C++). If you want to, you can also add `HOMEPAGE_URL` to the options in case you want something like the link to your GitHub repo directly embedded in your project.

The last thing to put into the `CMakeLists.txt` file before you can execute `cmake` is some information about the executable you want to be generated. You need to first tell CMake what you want the name of the binary to be, followed by the files that need to be included in the compilation:

~~~{.bash caption=">_"}
add_executable(add
    src/main.cpp
    src/add.cpp)
~~~

Now, you've created a complete, albeit very basic, `CMakeLists.txt` file, and you can finally run `cmake`. To do this, create a `build` folder in your root directory and enter it. From here, execute `cmake ..`. This tells `cmake` to execute, and `..` communicates that it should look in the parent directory for the `CMakeLists.txt` file.

> Note: It's not required, but it's recommended to create a `build` directory. Doing so makes it easy to wipe clean all the files generated by CMake.

After running `cmake ..`, you should find that the `build` directory has been filled with a bunch of files but not any executables. This is where the important distinction mentioned in the introduction comes into play: *CMake does not build your application; it*helps*you build your application.*

The specific files generated will depend on your operating system (which is the entire point of using CMake). If you're using CMake on Linux, you'll find a `Makefile` in your `build` directory. This means you can run `make`, and you should find the binary executable in the `build` directory.

## Advancing With CMake

At this point, you've seen everything that you need in order to start adding CMake to your projects. At its core, CMake isn't an extremely complicated tool to use; however, it does provide a lot of options for you to choose from and use to customize your build process. The two main things to learn more about are the options you can provide when invoking `cmake` and CMake Modules.

### CMake Modules

![modules]({{site.images}}{{page.slug}}/modules.png)\

You're probably familiar with the fact that in most programming languages, it's a lot easier to get something implemented if someone else has already done a lot of the work for you. In `.NET` it's [NuGet Packages](https://www.nuget.org/packages); in `Node.js`, it's [modules](https://nodejs.org/api/modules.html); and in CMake, it's also [modules](https://cmake.org/cmake/help/latest/manual/cmake-modules.7.html).

Modules, at their core, are helpers that others (or perhaps yourself) have made to either make the execution of some functionality easier or to make the `CMakeLists.txt` file easier to read. They are generally split into two types: [find modules and utility modules](https://cmake.org/cmake/help/book/mastering-cmake/chapter/Modules.html). There are [a lot of modules](https://cmake.org/cmake/help/latest/manual/cmake-modules.7.html) that natively come with CMake, but you'll also find that the community has created modules that you can use, like those found in [this GitHub repo](https://github.com/rpavlik/cmake-modules).

Once you're familiar with CMake, it's definitely worth it to look into modules, as you can find a lot of helper commands that will make your life easier and make your `CMakeLists.txt` files prettier. An example of this could be the [CheckFunctionExists](https://cmake.org/cmake/help/latest/module/CheckFunctionExists.html) module, which quite simply checks if a function exists, allowing you to avoid errors in execution.

### CMake Options

A lot of the things you have to worry about when it comes to CMake have to do with the contents of the `CMakeLists.txt` file, like what you've seen earlier in terms of defining the name of the executable and identifying the files to include. However, you can implement variability by using options when invoking the `cmake` command, and you can check all of them by running `cmake --help`. Some of the most useful ones to know are `-B`, `-S`, and `-G`:

* **`-B`** lets you explicitly specify a build directory. This can be useful if you're in the habit of running all your commands in the root directory of your project. With this option, you can choose to run `cmake -B build .` to specify the build directory as being the one you're currently in.

* **`-S`** lets you specify the source directory explicitly. This is a useful option to have if your `CMakeLists.txt` file is not in the correct place relative to what's specified inside the file. Or it can be used if you have an alternative source folder you want to test the build on.

* **`-G`** lets you choose what generator you want to use. [Generators](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html#manual:cmake-generators(7)) haven't been mentioned so far in this article because, by default, you don't need to know about them. Simply put, a generator is a utility responsible for creating the files inside the `build` directory. You can see a list of available generators on your system by running `cmake --help`.

## Conclusion

As you can see, CMake can be a great aid when you want to create a build process around your application. With CMake, you only have to write a `CMakeLists.txt` file to ensure that your application can be built and executed on any platform. This is a big advantage to many and, without a doubt, is one of the reasons the tool has gained popularity.

{% include_html cta/makefile-cta.html %}

<!-- If you like the format of using CMake and Makefiles, in general, but have a hard time seeing how to specifically fit it into your application, check out [Earthly](https://cloud.earthly.dev/login). Earthly is a tool that takes the best parts of Makefiles and combines them with Docker to make builds easier.
 -->
