---
title: "How To Use Makefiles on Windows"
categories:
  - Tutorials
toc: true
author: Kasper Siig
sidebar:
  nav: "makefile"
internal-links:
 - make
 - makefile
 - windows
 - cpp
topic: make
last_modified_at: 2023-04-17
excerpt: |
    
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster. This article is about `make` and `Makefile`s but if you're interested in a different approach to building software then [check us out](/).**

As the field of DevOps and build release engineering continues to grow, many new tools are being developed to help make building and releasing applications easier. One of the tools that has been in use for many years is [Make](https://en.wikipedia.org/wiki/Make_(software)), which is still heavily used by engineers today.

A *Makefile* is a simple text file consisting of targets, which can invoke different actions depending on what has been configured. For example, with a Makefile, you can invoke a build of your application, deploy it, or run automated tests and it can dramatically increase the efficiency of your workflow.

Initially, it was Stuart Feldman who began working on the Make utility [back in 1976](https://en.wikipedia.org/wiki/Make_(software)#Origin) at Bell Labs. However, the version of Make most commonly used today is [GNU Make](https://www.gnu.org/software/make/), which was introduced in the late 1980s.

While the tool was originally meant to run on [Linux](https://www.linux.org), Make's popularity has interested those working on other operating systems as well. There are several ways to run Makefiles on Windows, and in this article you'll be introduced to each option and learn about their strengths and weaknesses.

## Using Make on Windows

![windows]({{site.images}}{{page.slug}}/windows.jpg) \

Before looking at the different options available, you should know why you want to run Makefiles on Windows in the first place. Or rather, if you're working on Windows, why are you even interested in Makefiles?

Historically, the biggest reason for wanting Makefiles to run on Windows is that the developers in your organization are working on Windows. Seeing as how the de facto standard for languages like C and C++ is to use Make, it's no wonder that Windows users want the ability to use Make as well.

As applications and infrastructure become more modern, the cloud is another reason for wanting Makefiles on Windows. Many infrastructure engineers want their applications to be run on Linux, likely led by the adoption of tools like [Docker](https://www.docker.com) and containerization in general. Additionally, on Linux, a Makefile is the primary tool to use in many cases, especially when it comes to building native Linux applications. However, many engineers are still using Windows on their workstations, leading to the question of how to run Makefiles on Windows. Let's dive into the possible answers.

### Chocolatey

![chocolatey]({{site.images}}{{page.slug}}/chocolatey.png) \

Linux users have been using package managers for decades, yet they've never gained much traction on Windows. Up until the release of [winget](https://docs.microsoft.com/en-us/windows/package-manager/winget/), the concept of a package manager was never something that was natively included on Windows. Instead, Rob Reynolds started working on an independent package manager back in 2011 that would come to be known as [Chocolatey](https://blog.chocolatey.org/2016/03/celebrating-5-years/). Chocolatey is now widely used on Windows to install packages, and you can use it to install `make` as well.

To do so, run the following command in an Administrative PowerShell window:

~~~{.bash caption=">_"}
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
~~~

> You can find the newest installation instructions at any time [on the Chocolatey website](https://chocolatey.org/install).

Once Chocolatey is installed, you may have to close down the PowerShell window and open it back up. After that, run the following command:

~~~{.bash caption=">_"}
choco install make
~~~

Once the script is done running, `make` will be installed. You may need to restart the PowerShell window again, but at this point you are ready to use Makefiles on Windows.

Chocolatey will likely be the most popular option for those who want to stick to a pure Windows installation. It's easy to install, easy to use, and you don't need to jump through any hoops or workarounds to get it working.

At this point, you can use `make` just like you otherwise would, and you can test it by running `make -v`.

### Cygwin

Historically, one of the most popular ways of running any type of Linux functionality on Windows has been to use [Cygwin](https://www.cygwin.com/index.html). Cygwin aims to give a Linux feeling to Windows by holding a large collection of GNU and open source tools. It's important to note that this does *not* mean it will give you native Linux functionality. However, it does allow you to use Linux tools on Windows. There's a big difference between the two; for instance, Cygwin does not have access to Unix functionality like signals, PTYs, and so on. It's a great tool for when you want to use familiar Linux commands but still want them to be run on Windows.

To use Cygwin for Makefiles, start by [downloading and installing](https://www.cygwin.com/install.html) Cygwin. During the installation, you'll see a window popping up asking you what packages you want to install. In the top left corner, make sure to select **Full** and then search for `make`.

![Searching for "make"]({{site.images}}{{page.slug}}/Vx2tzwc.png)

Your search will give you a list of several different packages. You want to choose the one that's labeled just as `make`. Change the dropdown menu where it says **Skip** to the latest version.

![Choosing "make"]({{site.images}}{{page.slug}}/ElSKczz.png)

Now you can finish the installation by clicking **Next** in the bottom right corner. Once the installation is done, you can open up Cygwin and verify that `make` has been installed by executing `make --version`.

### NMAKE

One of the alternatives that you'll often hear about regarding running Makefiles on Windows is [NMAKE](https://docs.microsoft.com/en-us/cpp/build/reference/nmake-reference?view=msvc-170). While it is an alternative to `make`, note that you cannot simply take your existing Makefiles from Linux and run them using NMAKE; they have to be ported.

First of all, the compilers are different on Windows and Linux, so if you are specifying your compiler in your Makefile, you'll have to change that to whatever is relevant on Windows. At the same time, you'll have to change the flags that you send to the compiler, because Windows typically denotes the flags using `/` instead of `-`.

On top of that, it doesn't recognize all the syntax that you're used to from GNU Make, like `.PHONY`. Lastly, Windows obviously doesn't recognize the commands that work on Linux, so if you have specified any Linux-specific commands in your Makefiles, you'll also have to port them.

All in all, if your entire organization uses Windows and you simply want the typical functionality of GNU Make, then NMAKE is a viable solution. However, if you just want to quickly run your traditional Makefiles on Windows, NMAKE is not the answer.

### CMake

![cmake]({{site.images}}{{page.slug}}/cmake.jpg) \

As with NMAKE, [CMake](/blog/using-cmake) is not a direct way to run your Makefiles on Windows. Instead, [CMake](https://cmake.org) is a tool to generate Makefiles, at least on Linux. It works by defining a `CMakeLists.txt` file in the root directory of your application. Once you execute `cmake`, it generates the files you need to build your application, no matter what operating system you're on.

On Linux, this means that it creates Makefiles for you to run, but on Windows it may mean that it creates a [Visual Studio solution](https://docs.microsoft.com/en-us/visualstudio/get-started/tutorial-projects-solutions?view=vs-2022).

CMake is a great solution if you don't care too much about running Makefiles specifically, but you want the functionality, namely the ease of use in a build process, that you can get from Makefiles.

### Windows Subsystem for Linux

The [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about) (WSL) is an honorable mention. It's cheating a bit to say that it's a way to run Makefiles "on Windows," as your Makefiles won't actually be running on Windows.

If you haven't heard of WSL before, here's an extremely oversimplified explanation: It uses [Hyper-V](https://docs.microsoft.com/en-us/windows-server/virtualization/hyper-v/hyper-v-technology-overview) to create a hyper-optimized virtual machine on your computer, in which it runs Linux. Basically, you get a native Linux kernel running on your Windows computer, with a terminal that feels as if it's part of Windows.

You should look into WSL if what you care about most is having Windows as your regular desktop environment, but you're fine with all of your programming and development going on inside of Linux.

## Conclusion

As you can see, there are a few different ways you can be successful in running Makefiles on Windows. However, you do need to be wary of the fact that it will never be a perfect solution. Every solution is in some way a workaround, and the closest you'll get to feeling like you're using native Makefiles while using Windows is to install something like WSL.

{% include_html cta/makefile-cta.html %}

<!-- If all this becomes too tedious for you and you're looking for an easier alternative to optimize your builds, then check out [Earthly](https://earthly.dev/). Earthly has taken all the best parts of Makefiles and combined them with the best parts of Dockerfiles to help make your build processes more streamlined and effective. -->