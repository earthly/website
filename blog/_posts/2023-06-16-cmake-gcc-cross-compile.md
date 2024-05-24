---
title: "Using CMake and GCC to Cross-Compile Binaries"
toc: true
author: Rubaiat Hossain
editor: Bala Priya C
sidebar:
  nav: "makefile"
internal-links:
 - CMake
 - GCC
 - Cross-Compile Binaries
 - Cross-compilation
 - C++
excerpt: |
    Learn how to cross-compile binaries for different architectures using CMake and GCC in this tutorial. Discover the process of building a simple C++ program and then cross-compiling it for ARM64-based devices, along with troubleshooting tips for common issues.
last_modified_at: 2023-07-19

categories:
  - cli
---
**The article provides insights into cross-compiling for ARM64 architectures. Earthly simplifies the process of cross-compilation for those who use CMake. [Learn how](https://cloud.earthly.dev/login).**

Cross-compilation is the process of compiling your program on a different host than the target system. This enables developers to build binaries for different architectures without using those specific architectures themselves. For example, with cross-compilation, you can compile a binary for ARM-based devices like a Raspberry Pi on your standard x86-64 development machine.

When cross-compiling your software, [CMake](https://cmake.org/) and the [GNU Compiler Collection (GCC)](https://gcc.gnu.org/) can be helpful. CMake is a robust build system generator that uses configuration files to create cross-compiled binaries, and GCC is a toolchain that includes compilers for various programming languages, including C, C++, Objective C, and Fortran.

In this tutorial, you'll learn how to build a simple C++ program and then cross-compile it for AArch64 or ARM64-based devices using [CMake](/blog/using-cmake) and GCC.

## Building a Simple C++ Program

To start, you need to create a simple C++ program and then build it using [Makefiles](https://opensource.com/article/18/8/what-how-makefile) and GCC. To do this, you need two tools: the [GNU make](https://www.gnu.org/software/make/) utility and GCC.

### Installing GNU Make and GCC

You can install GCC on Debian/Ubuntu using the following command:

~~~{.bash caption=">_"}
sudo apt update && sudo apt install build-essentials
~~~

For Red Hat Enterprise Linux (RHEL) and Fedora, use the following command:

~~~{.bash caption=">_"}
sudo dnf groupinstall 'Development Tools'
~~~

GNU make comes preinstalled on most Linux distributions. You can check if it's installed on your machine using the following command:

~~~{.bash caption=">_"}
make --version
~~~

If make is not installed, use the following command to install it on Debian/Ubuntu:

~~~{.bash caption=">_"}
sudo apt-get install make
~~~

Or for RHEL or Fedora, use this command:

~~~{.bash caption=">_"}
sudo dnf install make
~~~

Now that the necessary tools are set up, go ahead and create your C++ program.

### Creating and Compiling a C++ Program

Create a new file named `hello.cpp` and populate it with the following code:

~~~{.cpp caption="hello.cpp"}
// hello.cpp
#include<iostream>

int main() {
    std::cout << "Hello, World!" << std::endl;

    return 0;
}
~~~

This program prints the string `Hello, World!` onto your console.

#### Compiling With `g++`

You can compile the `hello.cpp` file using g++, the C++ compiler component of GCC:

~~~{.bash caption=">_"}
g++ -o hello hello.cpp
~~~

This command generates a new binary executable called `hello` in your current directory. If you don't use the `-o` flag, g++ generates an executable file named `a.out` instead.

Next, run your program:

~~~{.bash caption=">_"}
./hello
~~~

This command should print out the string on your screen:

<div class="wide">
![`hello` binary]({{site.images}}{{page.slug}}/LviXqVY.png)
</div>

#### Compiling With Make

Now that you've compiled your program with GCC, compile the program with Make, a popular build automation tool that provides granular control over the build process by defining dependencies between files and targets. In doing so, Make can determine the correct order of operations needed to build a project efficiently.

The working procedure of Make revolves around a simple text file called the Makefile. It contains rules that tell Make how to build the project from scratch:

<div class="wide">
![Make diagram]({{site.images}}{{page.slug}}/SshQwn3.png)\
</div>

To build your simple C++ program using a Makefile, create a `Makefile` and populate it with the following:

~~~{.makefile caption=""}
# Makefile
hello: hello.cpp
    g++ -o hello hello.cpp

clean:
    rm -f hello
~~~

This Makefile contains two rules. The first rule specifies that the target is the `hello` executable and that it depends on `hello.cpp`. This rule has a single command that uses `g++` to compile and link the source file into an executable binary named `hello`.

The second rule specifies that the target is `clean`, which uses the `rm` command to remove the `hello` executable. It's important to note that Makefiles use tabs for indentation, not spaces.

Once you verify that your Makefile is formatted correctly, you can run the `make` command to generate the binary:

~~~{.bash caption=">_"}
make
~~~

Make goes through the Makefile and compiles the `hello.cpp` program using the specified g++ command. Next, delete the generated executable:

~~~{.bash caption=">_"}
make clean
~~~

## Cross-Compiling With CMake and GCC

Now that you have a simple C++ program running, it's time to cross-compile it to run on a different architecture using CMake. [CMake](/blog/using-cmake/) is a popular tool for managing the build process of C and C++ projects, and it has built-in support for cross-compiling.

Cross-compiling involves configuring CMake to use a cross-compiler and setting the appropriate build settings for the target platform. Once you've done that, you can build your project and produce a binary that can be run on the target platform.

To begin, you need to make sure that CMake is installed in your system. If not, you can install it using the following command in Debian/Ubuntu:

~~~{.bash caption=">_"}
sudo apt-get install cmake
~~~

Or if you're working with RHEL or Fedora, use the following command:

~~~{.bash caption=">_"}
sudo dnf install cmake
~~~

After you've installed CMake, you need to install the following two cross-compilers to produce the target binary for your selected architecture. Here, the selected architecture the target executable runs on is AArch64 and the host that we've compiled on thus far is x86-64.

Use the following command to install these compilers on Debian or Ubuntu:

~~~{.bash caption=">_"}
sudo apt-get install gcc-aarch64-linux-gnu
sudo apt-get install g++-aarch64-linux-gnu
~~~

Or use this command if you're using RHEL or Fedora:

~~~{.bash caption=">_"}
sudo dnf install epel-release
sudo dnf install gcc-aarch64-linux-gnu
sudo dnf install gcc-c++-aarch64-linux-gnu
~~~

Before using CMake to cross-compile your program, you need to obtain the prebuilt root file system for the ARM64 target system. This contains the libraries, headers, and other files needed to build and run software on the target system. Here, you'll use the Ubuntu ARM64 image, but you can download a prebuilt image or build one yourself using a tool like [debootstrap](https://wiki.debian.org/Debootstrap).

[Download the ISO image](https://cdimage.ubuntu.com/releases/) to your local machine and extract the content of this image to get the Ubuntu ARM64 root file system:

~~~{.bash caption=">_"}
sudo mkdir /mnt/iso
sudo mount -o loop /path/to/iso /mnt/iso
sudo cp -r /mnt/iso/* /path/to/rootfs/
~~~

Substitute `/path/to/iso/` with the actual path of the downloaded ISO image. The final copy command extracts the contents of this image to `/path/to/rootfs`. Make sure you use the exact paths for these on your machine.

After extracting the content of the image, the cross-compilation environment should now be set up. To cross-compile your C++ program with CMake, create a new file called `CMakeLists.txt` and fill it with the following:

~~~{ caption="CMakeLists.txt"}
# CMakeLists.txt

cmake_minimum_required(VERSION 3.0)

project(Hello)

set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR aarch64)

set(CMAKE_C_COMPILER /usr/bin/aarch64-linux-gnu-gcc)
set(CMAKE_CXX_COMPILER /usr/bin/aarch64-linux-gnu-g++)

set(CMAKE_FIND_ROOT_PATH /path/to/rootfs/)

add_executable(hello hello.cpp)
~~~

The first line sets the minimum version of CMake required to build this project to version 3.0. The second line sets the project name to `Hello`, and the following two lines set the target system name and processor architecture. The target system is `Linux`, and the target processor is `aarch64` (ARM64).

The following two lines set the C and C++ compilers to be used for cross-compiling the code to the target system. Make sure to use the correct path for the cross-compiler based on your system. The second to the last line sets the root directory to `/path/to/rootfs/`, and finally, you tell CMake to create the `hello` executable when this project is built.

Save and close this file. Then create a new directory to hold the build files generated by CMake:

~~~{.bash caption=">_"}
mkdir build
cd build
~~~

Run CMake using the following command:

~~~{.bash caption=">_"}
cmake ..
~~~

<div class="wide">
![CMake cross-compilation]({{site.images}}{{page.slug}}/ZhUWs93.png)
</div>

Now, CMake generates the build files, including a Makefile for your project. Use the following code to build the target binary:

~~~{.bash caption=">_"}
make
~~~

This creates the binary executable `hello` in the build directory:

<div class="wide">
![Make for cross-compilation]({{site.images}}{{page.slug}}/7qwn2o7.png)
</div>

## Testing the Executable

Now that you've cross-compiled your C++ program for an ARM64 system, see if it works. To verify that the binary produced by CMake is what you want, run the following command:

~~~{.bash caption=">_"}
file hello
~~~

<div class="wide">
![`hello` binary]({{site.images}}{{page.slug}}/xqjStAZ.png)
</div>

This should show that the `hello` executable is an `ELF 64-bit LSB` executable based on the ARM AArch64 architecture.

You can test this program in multiple ways: copying it to a 64-bit ARM device like a Raspberry Pi or transferring the binary to an ARM64 virtual machine (VM).

A VM based on ARM64 has been set up on Microsoft Azure to test the binary. You have the option to choose any cloud provider or self-host the VM. However, it's important to ensure that the file permissions are properly configured:  

<div class="wide">
![Cross-compiled `hello`]({{site.images}}{{page.slug}}/oMNapDN.png)
</div>

As you can see, this cross-compiled `hello` executable is running as expected on an ARM64 VM.

## Troubleshooting Common Issues During Cross-Compiling

![Troubleshooting]({{site.images}}{{page.slug}}/troubleshoot.png)\

Even with the help of tools like CMake and GCC, cross-compiling C++ programs can be challenging.

During cross-compiling, common issues you may encounter include compiler incompatibility, lack of readily available libraries, and toolchain conflicts. If you're facing some of these issues, here are a few tips:

* Make sure you've installed the correct cross-compilation toolchain for your target platform. If you use a different toolchain or an older version, you may encounter compatibility issues.
* Check that your CMake configuration is correct and make sure you set the right paths and compilers in your `CMakeLists.txt` file.
* Ensure you have all the necessary libraries and dependencies for your target platform. Sometimes, specific libraries or dependencies are unavailable for a particular platform, which can cause build errors.
* Check that your code is compatible with your target platform. For example, if you use assembly code or platform-specific features, you may need to modify your code to make it work on a different platform.
* Make sure you have the necessary permissions and access rights to write to the build directory and install the binary on your target platform.

## Conclusion

This tutorial showed you the basics of cross-compiling a C++ program for ARM64 devices using CMake and GCC. Remember to install the right toolchain, check your CMake setup, make your code compatible with the target platform, and look out for required libraries to avoid build mishaps.

Want to delve deeper into cross-compiling? Check out the official [CMake](https://cmake.org/documentation/) and [GCC](https://gcc.gnu.org/onlinedocs/) docs, or explore [platform-specific resources](https://github.com/topics/cross-compilation?o=desc&s=stars) and [forums](https://stackoverflow.com/questions/tagged/cross-compiling?sort=MostVotes&edited=true). Happy cross-compiling!

And if you are looking for ways to further simplify your cross compile build process, you might want to check out [Earthly](https://cloud.earthly.dev/login). It's a tool that can make cross complication simpler.

{% include_html cta/makefile-cta.html %}
