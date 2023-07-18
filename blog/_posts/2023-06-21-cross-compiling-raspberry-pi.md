---
title: "Cross-Compiling for Raspberry Pi: Getting Started and Troubleshooting"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea

internal-links:
 - Cross-Compiling
 - Raspberry Pi
 - Troubleshooting
 - Debian
 - Raspbian
excerpt: |
    Learn how to cross-compile programs for Raspberry Pi using a more powerful PC with this step-by-step tutorial. Discover how to set up the development environment, write a C++ program, and debug it using GDB.
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article covers cross compiling. If you're someone who builds software often, you might want to [check us out](/) and see if Earthly can help you build faster and easier.**

Thanks to its Debian-based OS, Raspberry Pi offers a robust developer experience. However, at times, it can be difficult to compile programs. For instance, maybe your project is large and your board doesn't have enough resources to compile it at a reasonable speed, especially if you're using a low-end board like the Raspberry Pi Zero. Or maybe your Virtual Network Computing (VNC) session is lagging, or the Raspberry Pi is in a location where it's not possible to attach a keyboard, mouse, or display. In these situations, you can use a readily available and efficient development machine, such as a laptop or another PC, to compile programs for the Raspberry Pi using a process known as cross-compilation.

With cross-compilation, you can compile an executable that can run on Raspberry Pi using ARM architecture but on a machine that is using a different architecture, such as x86.

In this article, you'll learn how to cross-compile a simple C++ program for a Raspberry Pi and link it to a shared library. You'll also learn how to debug and troubleshoot common issues that can arise during the compilation process.

## Setting Up a Cross-Compiling Environment

![Setting Up]({{site.images}}{{page.slug}}/setup.png)\

Before you get started with this tutorial, make sure you have the following:

* **A machine running Ubuntu**: This is where you'll compile the program and is often referred to as the host machine. Note that although it's possible to cross-compile from any Linux distribution, for simplicity, this article will use some Debian- and Ubuntu-based tools. If you don't have an Ubuntu machine, it's recommended to spin up an Ubuntu virtual machine (VM) to follow along. This tutorial was tested with Ubuntu 22.04.

* **A Raspberry Pi**: This should be connected to the local network and accessible using the Secure Shell Protocol (SSH) from the host machine. This article was tested on a Raspberry Pi 4B running Raspbian 10. If you have another board, such as a Raspberry Pi Zero, you need to tweak the commands appropriately. The Raspberry Pi used in this article was available in the local network with `pi.local` hostname and had a `pi` user.

### Setting Up SSH

To begin, you need to set up SSH on the host machine so that you can SSH into the Raspberry Pi without having to type the username, hostname, or password every time.

Run the following command from the `Host` machine:

~~~{.bash caption=">_"}
cat >> ~/.ssh/config << 'EOF'
Host rpi
    HostName pi.local
    User pi
EOF
~~~

Replace `pi.local` with the hostname of your Raspberry Pi board and `pi` with the username of your user on the Raspberry Pi. Finally, copy your SSH key into the Raspberry Pi:

~~~{.bash caption=">_"}
ssh-copy-id -i ~/.ssh/id_rsa.pub rpi
~~~

This command assumes that you already have an SSH key. If you don't, you can create one using the following command:

~~~{.bash caption=">_"}
ssh-keygen -t rsa
~~~

Make sure that you can SSH into the Raspberry Pi with only `rpi`:

~~~{.bash caption=">_"}
ssh rpi
~~~

### Setting Up the Development Machine

After setting up the SSH, it's time to get the host machine ready for development. You need to install a few programs first:

~~~{.bash caption=">_"}
sudo apt install ubuntu-dev-tools cmake curl
~~~

The [ubuntu-dev-tools](https://packages.ubuntu.com/bionic/ubuntu-dev-tools) package contains the tools necessary to build a Raspbian OS root file system, which you'll do in a moment.

#### Creating a Raspbian Root File System

When you're cross-compiling a program, you need to link to different libraries. These could be standard libraries, such as the C++ standard library, or a third-party library, such as [Boost](https://www.boost.org/).

You can't link the executable to libraries present on your host machine as it's likely to use a different architecture. To solve this issue, you need to create a Raspbian root file system, which mimics the file system of the Raspberry Pi. You can install libraries in this root file system (referred to as the `sysroot` from now on) and link to them. However, don't forget to install the libraries on the actual Raspberry Pi!

Import the necessary keys into the GNU Privacy Guard (GPG) and export them to a file:

~~~{.bash caption=">_"}
curl -sL http://archive.raspbian.org/raspbian.public.key | gpg --import -
gpg --export 9165938D90FDDD2E > $HOME/raspbian-archive-keyring.gpg
~~~

These keys will be used to verify the integrity of the packages that will be installed soon.

Create `rpi.sources` with the list of package mirrors:

~~~{.bash caption=">_"}
cat > $HOME/rpi.sources <<EOF
deb http://archive.raspbian.org/raspbian/ RELEASE main contrib non-free rpi
deb-src http://archive.raspbian.org/raspbian/ RELEASE main contrib non-free rpi
EOF
~~~

And then create `.mk-sbuild.rc` with the necessary settings:

~~~{.bash caption=">_"}
cat > $HOME/.mk-sbuild.rc <<EOF
SOURCE_CHROOTS_DIR="$HOME/chroots"
DEBOOTSTRAP_KEYRING="$HOME/raspbian-archive-keyring.gpg"
TEMPLATE_SOURCES="$HOME/rpi.sources"
SKIP_UPDATES="1"
SKIP_PROPOSED="1"
SKIP_SECURITY="1"
EATMYDATA="1"
EOF
~~~

This file adds some settings for `mk-sbuild`. Specifically, `$HOME/chroots` is set as the directory where the root file system will be stored. The GPG file and the sources files created in the previous steps are also used here.

Before you continue to create the root file system, you need to know the architecture and Raspbian release version of your Raspberry Pi. Run the following command on the Raspberry Pi to do so:

~~~{.bash caption=">_"}
$ dpkg --print-architecture
armhf
~~~

And run the following command to get the Raspbian release version:

~~~{.bash caption=">_"}
$ cat /etc/os-release
PRETTY_NAME="Raspbian GNU/Linux 10 (buster)"
NAME="Raspbian GNU/Linux"
VERSION_ID="10"
VERSION="10 (buster)"
VERSION_CODENAME=buster
ID=raspbian
ID_LIKE=debian
HOME_URL="http://www.raspbian.org/"
SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
~~~

> Note the `VERSION_CODENAME` (*ie* `buster`).

For the next two commands, you need to come back to the host machine.

For ease of use, export these as variables:

~~~{.bash caption=">_"}
export ARCH=armhf
export RELEASE=buster
~~~

Then run the following command:

~~~{.bash caption=">_"}
mk-sbuild --arch=$ARCH $RELEASE \
--debootstrap-mirror=http://archive.raspbian.org/raspbian/ \
--name=rpi-$RELEASE
~~~

If you're running `mk-sbuild` for the first time, you'll be prompted to edit the `.sbuildrc` file. Accept the defaults, and it will add your user to the `sbuild` group. You need to log out and log in again for the changes to take effect. Don't forget to export the `$ARCH` and `$RELEASE` variables again.

After logging in again, repeat the command:

~~~{.bash caption=">_"}
mk-sbuild --arch=$ARCH $RELEASE \
--debootstrap-mirror=http://archive.raspbian.org/raspbian/ \
--name=rpi-$RELEASE
~~~

This command runs the `mk-sbuild` tool which creates the root file system. It's named `rpi-$RELEASE` (*ie* `rpi-buster`).

After a while, you should have the sysroot ready with the following output:

<div class="wide">
![sysroot ready]({{site.images}}{{page.slug}}/7rBUoVW.png)
</div>

#### Installing the Toolchain

Once the sysroot is compiled, you'll need to install a [toolchain](https://en.wikipedia.org/wiki/Toolchain) that can cross-compile for Raspberry Pi. A toolchain is simply a collection of tools (compiler, linker, or debugger) that is used to compile and debug programs. For cross-compilation, you need a special toolchain that can compile programs into executables specifically for the target architecture.

The cross-compilation toolchains in the Ubuntu repository are not compatible with Raspberry Pi boards, so you need to build your own or get them from elsewhere. In this article, you'll use the ones found in [this GitHub repo](https://github.com/tttapa/docker-arm-cross-toolchain). For Raspberry Pi 4 specifically, you need to use the `armv8-rpi3-linux-gnueabihf` toolchain. If you have another board, you need to choose the appropriate toolchain for your use case. You can check out the `README` file in the repo for more info.

For easy access, make sure you store the toolchain name in a variable:

~~~{.bash caption=">_"}
export TC=armv8-rpi3-linux-gnueabihf
~~~

And download and install the toolchain:

~~~{.bash caption=">_"}
mkdir -p ~/opt
wget -qO- https://github.com/tttapa/docker-arm-cross-toolchain/releases/latest/download/x-tools-$TC.tar.xz | tar xJ -C ~/opt
~~~

This code installs the toolchain in `!/opt/x-tools/armv8-rpi3-linux-gnueabihf`. You need to add it to your `PATH` so that you can run the compilers from there:

~~~{.bash caption=">_"}
export PATH="$HOME/opt/x-tools/$TC/bin:$PATH"
~~~

Next, verify that you can run `g++` from this toolchain:

~~~{.bash caption=">_"}
armv8-rpi3-linux-gnueabihf-g++ --version \
# Replace armv8-rpi3-linux-gnueabihf with your chosen toolchain name
~~~

<div class="wide">
![Verifying that you can run`g++`]({{site.images}}{{page.slug}}/uU16OmX.png)
</div>

Out of the box, the Raspbian OS uses an older compiler and C++ standard library version. So install the standard library from the toolchain into the Raspberry Pi. Run the following command on the host machine:

~~~{.bash caption=">_"}
scp ~/opt/x-tools/$TC/$TC/sysroot/lib/libstdc++.so.6.0.30 rpi:~
ssh rpi bash << 'EOF'
    sudo mkdir -p /usr/local/lib/arm-linux-gnueabihf
    sudo mv libstdc++.so.6.0.30 $_
    sudo ldconfig
EOF
~~~

> **Note:** Change `6.0.30` to whatever version your toolchain is using.

This command installs the newer standard library to `/usr/local` so that it doesn't interfere with the system-installed standard library.

Next, you need to install the standard library to the sysroot as well. Ensuring that the library is installed both on the Raspeberry PI and the sysroot is crucial. This is because during development, the libraries in the sysroot are used for the linking process.

Run the following command to install the newer standard library into the sysroot. Note that it is also installed in `/usr/local`:

~~~{.bash caption=">_"}

sudo mkdir -p /var/lib/schroot/chroots/rpi-$RELEASE-$ARCH/usr/local/lib/arm-linux-gnueabihf
sudo cp ~/opt/x-tools/$TC/$TC/sysroot/lib/libstdc++.so.6.0.30 $_
sudo schroot -c source:rpi-$RELEASE-$ARCH -u root -d / ldconfig
~~~

#### Installing the Libraries

After you've installed your toolchain and updated the standard library version, you need to add them to the sysroot as well as the actual Raspberry Pi so that you can link the shared libraries. The program in this article uses the [GMP library](https://gmplib.org/) as an example.

Start by installing the GMP library in the sysroot:

~~~{.bash caption=">_"}
sudo sbuild-apt rpi-$RELEASE-$ARCH apt-get install libgmp-dev
~~~

And then install it on the Raspberry Pi:

~~~{.bash caption=">_"}
ssh rpi sudo apt install -y libgmp-dev
~~~

### Writing the Program and Setting Up CMake

Once you've installed the GMP library, you're at the heart of the project: writing the actual code.

Create a directory named `cross-compile` and `cd` into it. Then create a file `main.cpp` with the following code:

~~~{.cpp caption="main.cpp"}
#include <iostream>
#include "gmpxx.h"
 
mpz_class fact(mpz_class n) {
    mpz_class f = 1;
    for (mpz_class i = 1; i <= n; i++) {
        f *= i;
    }
    return f;
}
 
int main() {
    mpz_class n = 1000;
    mpz_class f = fact(n);
    std::cout << "The factorial of " << n << " = " << f << std::endl;
    return 0;
}
~~~

This code uses the GMP library to calculate the factorial of `1000`, which is out of bounds using regular long integers.

To compile the code [using CMake](/blog/using-cmake), you need to tell CMake how to build the project. Create `CMakeLists.txt` with the following code:

~~~{ caption="CMakeLists.txt"}
cmake_minimum_required(VERSION 3.16)
project(fact VERSION 0.1.0 LANGUAGES C CXX Fortran)
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} \
"${CMAKE_SOURCE_DIR}/cmake/modules/")
find_package(GMP REQUIRED)
 
add_executable(fact main.cpp)
target_link_libraries(fact gmp gmpxx)
 
include(GNUInstallDirs)
install(TARGETS fact
        RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
~~~

Here's a brief explanation of the most important parts of this code:

* **`set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/modules/")`** sets the `CMAKE_MODULE_PATH` to `cmake/modules`. You use this directory to write a module that helps CMake find the GMP libraries.
* **`find_package(GMP REQUIRED)`** tells CMake that GMP is required to build this project.
* **`add_executable(fact main.cpp)`** tells CMake that `main.cpp` is compiled into an executable named `fact`.
* **`target_link_libraries(fact gmp gmpxx)`** tells CMake to link the executable to `libgmp` and `libgmpxx`.
* **`install(TARGETS fact RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})`** tells CMake to install the executable to the `bin` folder of the staging directory.

Next, create the `cmake/modules` directory and create a file named `FindGMP.cmake` inside it with the following code:

~~~{ caption="FindGMP.cmake"}
include(FindPackageHandleStandardArgs)
 
# Try to find libraries
find_library(GMP_C_LIBRARIES
  NAMES gmp
  DOC "GMP C libraries"
)
find_library(GMP_CXX_LIBRARIES
  NAMES gmpxx
  DOC "GMP C++ libraries"
)
 
# Try to find headers
find_path(GMP_C_INCLUDES
  NAMES gmp.h
  DOC "GMP C header"
)
 
find_path(GMP_CXX_INCLUDES
  NAMES gmpxx.h
  DOC "GMP C++ header"
)
 
# Handle QUIET and REQUIRED and check the necessary \
variables were set and if so
# set ``GMP_FOUND``
find_package_handle_standard_args(GMP
    REQUIRED_VARS GMP_C_LIBRARIES GMP_C_INCLUDES \
    GMP_CXX_LIBRARIES GMP_CXX_INCLUDES)
 
if (GMP_FOUND)
  set(GMP_INCLUDE_DIRS "${GMP_C_INCLUDES}" "${GMP_CXX_INCLUDES}")
  list(REMOVE_DUPLICATES GMP_INCLUDE_DIRS)
 
  if (NOT TARGET GMP::GMP)
    add_library(GMP::GMP UNKNOWN IMPORTED)
    set_target_properties(GMP::GMP PROPERTIES
      INTERFACE_INCLUDE_DIRECTORIES "${GMP_C_INCLUDES}"
      IMPORTED_LOCATION "${GMP_C_LIBRARIES}")
  endif()
endif()
~~~

This script simply tells CMake how to find the GMP headers and libraries.

Now comes the important part: the way you tell CMake to cross-compile using a specified toolchain is to use a [toolchain file](https://cmake.org/cmake/help/latest/manual/cmake-toolchains.7.html#cross-compiling). The following command creates `cmake/armv8-rpi3-linux-gnueabihf.cmake` (or `<your toolchain name>.cmake`):

~~~{.bash caption=">_"}
cat > cmake/$TC.cmake << EOF
# https://cmake.org/cmake/help/book/mastering-cmake/chapter/Cross%20Compiling%20With%20CMake.html
 
# Cross-compilation system information
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
 
# The sysroot contains all the libraries we might need to link against and
# possibly headers we need for compilation
set(CMAKE_SYSROOT /var/lib/schroot/chroots/rpi-buster-armhf)
set(CMAKE_FIND_ROOT_PATH ${CMAKE_SYSROOT})
set(CMAKE_LIBRARY_ARCHITECTURE arm-linux-gnueabihf)
set(CMAKE_STAGING_PREFIX $ENV{HOME}/RPi-dev/staging-armv8-rpi3)
 
# Set the compilers for C, C++ and Fortran
set(RPI_GCC_TRIPLE "armv8-rpi3-linux-gnueabihf")
set(CMAKE_C_COMPILER ${RPI_GCC_TRIPLE}-gcc CACHE FILEPATH "C compiler")
set(CMAKE_CXX_COMPILER ${RPI_GCC_TRIPLE}-g++ CACHE FILEPATH "C++ compiler")
set(CMAKE_Fortran_COMPILER ${RPI_GCC_TRIPLE}-gfortran CACHE FILEPATH "Fortran compiler")
 
# Set the architecture-specific compiler flags
set(ARCH_FLAGS "-mcpu=arm1176jzf-s")
set(CMAKE_C_FLAGS_INIT ${ARCH_FLAGS})
set(CMAKE_CXX_FLAGS_INIT ${ARCH_FLAGS})
set(CMAKE_Fortran_FLAGS_INIT ${ARCH_FLAGS})
 
# Don't look for programs in the sysroot (these are ARM programs, they won't run
# on the build machine)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# Only look for libraries, headers and packages in the sysroot, don't look on
# the build machine
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
 
set(CPACK_DEBIAN_PACKAGE_ARCHITECTURE armhf)
EOF
~~~

Let's break this code down: `set(CMAKE_SYSTEM_PROCESSOR arm)` tells CMake that the target process is using ARM instructions. Then `set(CMAKE_SYSROOT /var/lib/schroot/chroots/rpi-buster-armhf)` sets the `CMAKE_SYSROOT` variable to the sysroot location. Make sure you replace `rpi-buster-armhf` with your sysroot name.

Finally, `set(CMAKE_STAGING_PREFIX $ENV{HOME}/RPi-dev/staging-armv8-rpi3)` creates a staging directory on the host machine where the final file is installed.

~~~{ caption=""}
set(RPI_GCC_TRIPLE "armv8-rpi3-linux-gnueabihf")
set(CMAKE_C_COMPILER ${RPI_GCC_TRIPLE}-gcc CACHE FILEPATH "C compiler")
set(CMAKE_CXX_COMPILER ${RPI_GCC_TRIPLE}-g++ CACHE FILEPATH "C++ compiler")
set(CMAKE_Fortran_COMPILER ${RPI_GCC_TRIPLE}-gfortran CACHE FILEPATH "Fortran compiler")
~~~

This code tells CMake where to find the compilers. Make sure you replace `armv8-rpi3-linux-gnueabihf` with your toolchain name.

### Compiling the Program

Now that you've written the program and have set up CMake, it's time to compile the program with the following commands:

~~~{.bash caption=">_"}
cmake -S . -B build -DCMAKE_TOOLCHAIN_FILE=cmake/$TC.cmake
cmake --build build -j
cmake --install build
~~~

If it executes properly, you should have a file named `fact` in `~/RPi-dev/staging-armv8-rpi3/bin`.

### Transferring and Running the Program

To transfer and run the program after compiling it, copy the executable over to the Raspberry Pi:

~~~{.bash caption=">_"}
scp ~/RPi-dev/staging-armv8-rpi3/bin/fact rpi:~
~~~

SSH into the Raspberry Pi:

~~~{.bash caption=">_"}
ssh rpi
~~~

And run the executable:

~~~{.bash caption=">_"}
./fact
~~~

If you did everything correctly, it should run without errors and produce the following output:

~~~{ caption="Output"}
The factorial of 1000 = \
402387260077093773543702433923003985719374864210714632543 \
7999104299385123986290205920442084869694048004799886101971 \
9605863166687299480855890132382966994459099742450408707375 \
9918823627727188732519779505950995276120874975462497043601 \
4182780946464962910563938874378864873371191810458257836478 \
4997701247663288983595573543251318532395846307555740911426 \
2417474349347553428646576611667797396668820291207379143853 \
7195882498081268678383745597317461360853795345242215865932 \
0192809087829730843139284440328123155861103697680135730421 \
6168747609675871348312025478589320767169132448426236131412 \
50878020800026168315102734182…….
~~~

### Debugging

To debug the program using the GNU Debugger (GDB), you need to install `gdbserver` on the Raspberry Pi. The `gdbserver` runs on the Raspberry Pi and allows GDB to connect with it via SSH from the host machine. The toolchain already includes the `gdbserver` binary, which you need to copy to the Raspberry Pi:

~~~{.bash caption=">_"}
scp ~/opt/x-tools/$TC/$TC/debug-root/usr/bin/gdbserver rpi:~
ssh rpi sudo mv gdbserver /usr/local/bin
~~~

Make sure you verify the installation:

~~~{.bash caption=">_"}
ssh rpi gdbserver --version
~~~

<div class="wide">
![Verify the installation]({{site.images}}{{page.slug}}/3L152a5.png)
</div>

The Raspbian OS also uses a custom `memcpy` implementation, which GDB needs to be present in the sysroot. For that, you need to install the `raspi-copies-and-fills` package to the sysroot:

~~~{.bash caption=">_"}

echo "deb http://archive.raspberrypi.org/debian/ buster main" \
| sudo tee /var/lib/schroot/chroots/rpi-$RELEASE-$ARCH/etc/apt/sources.list.d/raspi.list
wget -qO- https://archive.raspberrypi.org/debian/raspberrypi.gpg.key \
| sudo schroot -c source:rpi-$RELEASE-$ARCH -u root -d / -- apt-key add -
sudo sbuild-apt rpi-$RELEASE-$ARCH apt-get update
sudo sbuild-apt rpi-$RELEASE-$ARCH apt-get install raspi-copies-and-fills
~~~

You can debug the program with the ARM version of GDB that is bundled in the toolchain:

~~~{.bash caption=">_"}
armv8-rpi3-linux-gnueabihf-gdb ./build/fact \
# Replace armv8-rpi3-linux-gnueabihf with your toolchain name
~~~

> **Note:** If you run into an error regarding missing Python 3.6 libraries, check out the following ["Troubleshooting Common Errors" section](#troubleshooting-common-errors) for a solution.

Inside the GDB session, set the sysroot and connect to `gdbserver` on the Raspberry Pi:

~~~{.bash caption=">_"}
(gdb) set sysroot /var/lib/schroot/chroots/rpi-buster-armhf
(gdb) target remote | ssh rpi gdbserver - '~/fact'
(gdb) continue
~~~

<div class="wide">
![Connect to `gdbserver`]({{site.images}}{{page.slug}}/zAsVpNC.png)
</div>

## Troubleshooting Common Errors

![Troubleshooting]({{site.images}}{{page.slug}}/troubleshoot.png)\

When cross-compiling for Raspberry Pi, you can run into several different errors. Following are some common errors and their fixes:

### Compiler Not Found

If you see the following error when running the CMake commands, it indicates that the toolchain is not installed correctly or it isn't added to `$PATH`:

~~~{.bash caption=">_"}
The CMAKE_C_COMPILER:
 
     armv8-rpi3-linux-gnueabihf-gcc
 
   is not a full path and was not found in the PATH.
~~~

If you have already restarted the shell or the machine, you need to run the command again.

### Library Not Found

You may also encounter the following issue when running the binary on the Raspberry Pi:

~~~{.bash caption=">_"}
./fact: error while loading shared libraries: libgmpxx.so.4: \
cannot open shared object file: No such file or directory
~~~

This means you did not install the `libgmp` library on the Raspberry Pi. Remember that any library you link against must be installed both in the `sysroot` as well as on the Raspberry Pi.

### Python Not Found

The GDB binary bundled with the toolchain has a dependency against Python 3.6, and if Python 3.6 isn't installed, you may see an error like this:

~~~{.bash caption=">_"}
armv8-rpi3-linux-gnueabihf-gdb: error while loading shared libraries: \
libpython3.6m.so.1.0: cannot open shared object file: No such \
file or directory
~~~

To fix this, you need to install Python 3.6 on your system. If you're using Ubuntu 22.04 or later, it isn't available in the repositories anymore. You can [build it from the source](https://stackoverflow.com/questions/72102435/how-to-install-python3-6-on-ubuntu-22-04/72135545#72135545), but a better approach is to use the `gdb-multiarch` package instead of the bundled GDB. For instance, you can install it with the following code:

~~~{.bash caption=">_"}
sudo apt install gdb-multiarch
~~~

And run it with this:

~~~{.bash caption=">_"}
gdb-multiarch ./build/fact
~~~

## Conclusion

Raspberry Pi's simplicity can be a limitation, but with a cross-compilation toolchain, you can utilize a stronger PC to compile programs for Raspberry Pi. 

This article walked you through setting up a cross-compilation environment, creating a CMake toolchain file, compiling a C++ program, linking it to a shared library, and debugging using GDB. 

To delve deeper into cross-compilation with CMake, read the [official documentation](https://cmake.org/cmake/help/book/mastering-cmake/chapter/Cross%20Compiling%20With%20CM). And if you're looking to further fine-tune your cross compile process, you might want to give [Earthly](https://www.earthly.dev/) a try!

{% include_html cta/bottom-cta.html %}
