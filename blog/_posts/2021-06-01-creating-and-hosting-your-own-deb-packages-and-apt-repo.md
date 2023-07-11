---
title: "Creating and hosting your own deb packages and apt repo"
categories:
  - Tutorials
toc: true
author: Alex
internal-links:
  - apt
  - pgp
  - gpg
  - deb
  - signing
  - digital signature
  - apt repo
  - public key
  - private key
  - rsa
topic: packaging
excerpt: |
    Learn how to create and host your own deb packages and apt repository in this tutorial. You'll discover the step-by-step process of creating a deb package, setting up an apt repository, signing it with a PGP key, and testing it with apt commands.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

<!-- vale HouseStyle.TLA = NO -->
<!-- vale HouseStyle.ListStart = NO -->
<!-- vale HouseStyle.EG = NO -->
<!-- markdownlint-disable MD032 -->
As an Ubuntu user, I find myself typing `apt install ...` frequently as a way to install software on my system.
But what if I wanted to distribute my code to others via an apt repository? In this post I'll cover how to
1) create a deb package, 2) create an apt repo, 3) signing that apt repo with a PGP key, and 4) putting it all together
with some tests.
<!-- markdownlint-enable MD032 -->

## Prerequisites

This tutorial assumes you are using Ubuntu, and that the following packages are installed:

<div class="narrow-code">

```bash
sudo apt-get install -y gcc dpkg-dev gpg
```

</div>

## Step 0: Creating a Simple Hello World Program

Before getting started with packaging, let's create a basic hello world program
under `~/example/hello-world-program`. To do this, you can copy and paste the following commands
into your terminal:

<div class="narrow-code">

```bash
mkdir -p ~/example/hello-world-program

echo '#include <stdio.h>
int main() {
    printf("hello packaged world\n");
    return 0;
}' > ~/example/hello-world-program/hello.c
```

</div>

Then, you can compile it with:

<div class="narrow-code">

```bash
cd ~/example/hello-world-program
gcc -o hello-world hello.c
```

</div>

There's no technical reason for picking C for this example -- the language doesn't matter.
It's the binary we will be distributing in our deb package.

## Step 1: Creating a `deb` Package

Debian, and Debian-based Linux distributions use `.deb` packages to package and distribute programs.
To start we will create a directory in the form:

```
<package-name>_<version>-<release-number>_<architecture>
```

where the

- `package-name` is the name of our package, `hello-world` in our case,
- `version` is the version of the software, `0.0.1` in our case,
- `release-number` is used to track different releases of the same software version; it's usually set to `1`, but hypothetically if there
  was an error in the packaging (e.g. a file was missed, or the description had an error in it, or a post-install script was wrong), this number
  would be increased to track the change, and
- `architecture` is the target architecture of the platform, `amd64` in this example; however if your package is architecture-independent (e.g. a python script),
  then you can set this to `all`.

<div class="notice--info">
Theoretically, the directory doesn't have to follow this naming convention; however some of the tools we will use later in the tutorial
require this directory naming convention.
</div>

So for this example, we'll create the directory with:

```bash
mkdir -p ~/example/hello-world_0.0.1-1_amd64
```

This directory will be the root of the package. Since we want our `hello-world` binary to be installed system wide, we'll have to store it under
`usr/bin/hello-world` with the following commands:

```bash
cd ~/example/hello-world_0.0.1-1_amd64
mkdir -p usr/bin
cp ~/example/hello-world-program/hello-world usr/bin/.
```

Each package requires a `control` file which needs to be located under the `DEBIAN` directory. You can copy and paste
the following to create one:

```bash
mkdir -p ~/example/hello-world_0.0.1-1_amd64/DEBIAN

echo "Package: hello-world
Version: 0.0.1
Maintainer: example <example@example.com>
Depends: libc6
Architecture: amd64
Homepage: http://example.com
Description: A program that prints hello" \
> ~/example/hello-world_0.0.1-1_amd64/DEBIAN/control
```

Note that we're assuming an amd64 Architecture for this tutorial, if your binary is for a different architecture, adjust accordingly.
If you're distributing a platform-independent package, you can set the architecture to `all`.

By this point you should have created two files:

```
~/example/hello-world_0.0.1-1_amd64/usr/bin/hello-world
~/example/hello-world_0.0.1-1_amd64/DEBIAN/control
```

To build the .deb package, run:

```bash
dpkg --build ~/example/hello-world_0.0.1-1_amd64
```

This will output a deb package under `~/example/hello-world_0.0.1.deb`.

You can inspect the info of the deb by running:

```bash
dpkg-deb --info ~/example/hello-world_0.0.1.deb
```

which will show:

```bash
new Debian package, version 2.0.
size 2832 bytes: control archive=336 bytes.
    182 bytes,     7 lines      control
Package: hello-world
Version: 0.0.1
Maintainer: example <example@example.com>
Depends: libc6
Architecture: amd64
Homepage: http://example.com
Description: A program that prints hello
```

You can also view the contents by running:

```bash
dpkg-deb --contents ~/example/hello-world_0.0.1.deb
```

which will show:

```
drwxrwxr-x alex/alex         0 2021-05-17 16:21 ./
drwxrwxr-x alex/alex         0 2021-05-17 16:18 ./usr/
drwxrwxr-x alex/alex         0 2021-05-17 16:18 ./usr/bin/
-rwxrwxr-x alex/alex     16696 2021-05-17 16:18 ./usr/bin/hello-world
```

<div class="notice--info">
It's also possible to run `less ~/example/hello-world_0.0.1.deb` which will output the above information, thanks to `/bin/lesspipe`.
</div>

This package can then be installed using the `-f` option under `apt-get install`:

```bash
sudo apt-get install -f ~/example/hello-world_0.0.1-1_amd64.deb
```

Then once installed, you can verify it works with commands like:

```bash
which hello-world
```

and

```
hello-world
```

which should output `/usr/bin/hello-world` and `hello packaged world` respectively.

Finally, if you want to remove it, you can run:

```bash
sudo apt-get remove hello-world
```

This concludes the first step of building a `.deb` package.
If you have access to an existing apt repository, you could submit
the deb to the repository maintainer, and call it a day.

## Step 2: Creating an `apt` Repository

In this step, we will show how to create your own apt repository which can be used to host one or more deb packages.

Let's start with creating a directory to hold our debs:

```bash
mkdir -p ~/example/apt-repo/pool/main/
```

Then copy our deb(s) into this directory:

```bash
cp ~/example/hello-world_0.0.1-1_amd64.deb ~/example/apt-repo/pool/main/.
```

<div class="notice--info">
Larger apt repositories create sub-directories for each program or project. For example, the official Ubuntu apt repository stores all vim
related packages under `/ubuntu/pool/main/v/vim/`.
</div>

Once you've copied in all of your debs, we will create a different directory to contain a list of all available packages and corresponding
metadata:

```bash
mkdir -p ~/example/apt-repo/dists/stable/main/binary-amd64
```

<div class="notice--info">
If you want to support multiple architectures, make a directory above for each type (e.g. `i386`, `amd64`, etc).
</div>

Next, we will generate a `Packages` file, which will contain a list of all available packages
in this repository. We will use the `dpkg-scanpackages` program to generate it, by running:

```bash
cd ~/example/apt-repo
dpkg-scanpackages --arch amd64 pool/ > dists/stable/main/binary-amd64/Packages
```

It's also good practice to compress the packages file, as apt will favour downloading compressed data whenever available.
Let's do this by running:

```bash
cat dists/stable/main/binary-amd64/Packages | gzip -9 > dists/stable/main/binary-amd64/Packages.gz
```

<div class="notice--info">
_Note: A reader has reported supplying a compressed file might be a required step rather than optional; either way it's best to
create a compressed file. Apt repositories can support more than just `gzip` compression, e.g. `bzip2`, `lzma`, or `uncompressed`.
In order to support other compression types, one must adjust the previous command for each desired compressed file format.
The [apt.conf man page](http://manpages.ubuntu.com/manpages/trusty/man5/apt.conf.5.html) has details on configuring apt
to prefer one format over the other via the `CompressionTypes` option; it is also possible to temporarily override it on
the command-line (e.g. `apt-get -o Acquire::CompressionTypes::Order::=bz2 update`)._
</div>

Let's take a quick look at the contents of the Packages file:

```
Package: hello-world
Version: 0.0.1
Architecture: amd64
Maintainer: example <example@example.com>
Depends: libc6
Filename: pool/main/hello-world_0.0.1-1_amd64.deb
Size: 2832
MD5sum: 3eba602abba5d6ea2a924854d014f4a7
SHA1: e300cabc138ac16b64884c9c832da4f811ea40fb
SHA256: 6e314acd7e1e97e11865c11593362c65db9616345e1e34e309314528c5ef19a6
Homepage: http://example.com
Description: A program that prints hello
```

<div class="notice--info">
if you had multiple deb files, you would have an entry for each package
</div>

The contents of the Packages file is a list of all available packages along with metadata from the `DEBIAN/control` file, and some hashes which can be used to
validate the integrity of the package.

Next we will create a Release file. Unfortunately `dpkg-scanpackages` does not create Release files. Some people use programs like `apt-ftparchive`;
however in this example I'll cover an alternative to `apt-ftparchive` by using a small bash script.

First let's look at an example of a Release file, which can be broken up into two parts:

1. Metadata about the repository, for example:

    ```
    Origin: Example Repository
    Label: Example
    Suite: stable
    Codename: stable
    Version: 1.0
    Architectures: amd64 arm64 arm7
    Components: main
    Description: An example software repository
    ```

2. A list of all `Packages` files and their corresponding hashes and file size, for example:

    ```
    MD5Sum:
     9eb0c0528a0647daf18c7e225ac68f45 667 main/binary-amd64/Packages.gz
     628682afa8a0208e08b5a208a4c4c85b 1685 main/binary-amd64/Packages
     b5bef2199e86a43ae02adc0b7b38bc8a 556 main/binary-arm7/Packages.gz
     81c53db3b9c5e9de44d3ca9fc4487995 1289 main/binary-arm7/Packages
     15258b054124639f0641c399f291af17 557 main/binary-arm64/Packages.gz
     dc597a0815aebb56b25a4ad979682f49 1292 main/binary-arm64/Packages
    SHA1:
     a4074284eb528e5d16c2c94e203d61dd825fa774 667 main/binary-amd64/Packages.gz
     ee86dd9061967232e6e68104a695f7d45d191b41 1685 main/binary-amd64/Packages
     a6f4897bcf6a4b068c5b8fafca01fc89761106dc 556 main/binary-arm7/Packages.gz
     43171192ce84dcb43bba99828fe7493ff23e0b0e 1289 main/binary-arm7/Packages
     9f353a909a9a3dab0a9cae1a3c7ccb879ff18d32 557 main/binary-arm64/Packages.gz
     da15c24e51a028ff591656eef0d1da0dbb85ba97 1292 main/binary-arm64/Packages
    SHA256:
     dee57f6f4a2209b63301984acb4b279f694648915fd559287a414365884c1842 667 main/binary-amd64/Packages.gz
     7d82e5929d909d10d9f2d7129df3f6754946397caf1c08e9e4a65713f4ac39ff 1685 main/binary-amd64/Packages
     2b3c611305e096ef246d77d2bc5fcfa807034dd200f8f99005ab640cf2c014a4 556 main/binary-arm7/Packages.gz
     d03d5192e24e098a91465ab37d34e0a2c539f50a430eb3262a543e7bd11212a1 1289 main/binary-arm7/Packages
     f96316ff77e96d246447f0ca8383472acefc0744d9b49d2be1d214d174bba38a 557 main/binary-arm64/Packages.gz
     58120a7b5ceb57ab4faca01adac3d62009a52962e0d0a6f4b7ceb1b8faedf280 1292 main/binary-arm64/Packages
    ```

And that's it for what a `Release` file looks like. How hard could it be? let's [write some bash](/blog/understanding-bash).
Just copy and paste the following in your terminal to get a copy of the script:

```bash
echo '#!/bin/sh
set -e

do_hash() {
    HASH_NAME=$1
    HASH_CMD=$2
    echo "${HASH_NAME}:"
    for f in $(find -type f); do
        f=$(echo $f | cut -c3-) # remove ./ prefix
        if [ "$f" = "Release" ]; then
            continue
        fi
        echo " $(${HASH_CMD} ${f}  | cut -d" " -f1) $(wc -c $f)"
    done
}

cat << EOF
Origin: Example Repository
Label: Example
Suite: stable
Codename: stable
Version: 1.0
Architectures: amd64 arm64 arm7
Components: main
Description: An example software repository
Date: $(date -Ru)
EOF
do_hash "MD5Sum" "md5sum"
do_hash "SHA1" "sha1sum"
do_hash "SHA256" "sha256sum"
' > ~/example/generate-release.sh && chmod +x ~/example/generate-release.sh
```

Next let's run the `generate-release.sh` script with:

```bash
cd ~/example/apt-repo/dists/stable
~/example/generate-release.sh > Release
```

At this point, you can try hosting this repo for yourself. In this example we'll use python's simple HTTP server; however in practice you'll want
to use a production-ready server. Here's how you can start it up for testing:

```bash
cd ~/example
python3 -m http.server
```

Then configure this apt repository:

```bash
echo "deb [arch=amd64] http://127.0.0.1:8000/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/example.list
```

Then finally update apt and install our new hello-world package:

```bash
sudo apt-get update --allow-insecure-repositories
sudo apt-get install hello-world
```

Note that the `--allow-insecure-repositories` will print the following warning message:

```
W: The repository 'http://127.0.0.1:8000/apt-repo stable Release' is not signed.
N: Data from such a repository can't be authenticated and is therefore potentially dangerous to use.
N: See apt-secure(8) manpage for repository creation and user configuration details.
```

That flag should never be used in a production environment. In the next section we'll cover how to sign the repository,
so it can be used in a trusted manor. Similarly when we install `hello-world`, we are asked if we want to proceed with
an un-authenticated package:

```
WARNING: The following packages cannot be authenticated!
  hello-world
Install these packages without verification? [y/N]
```

Fortunately in the next section we'll cover generating a PGP key, and signing our repository with it, which will
allow users to verify the repository contents have not been tampered with.

## Step 3: Signing your `apt` Repository With GPG

In the previous step, we generated a `Release` file, which referenced one or more `Packages` files
along with it's corresponding md5, sha1, and sha256 hashes. The `Packages` file in turns references a
deb package along with it's md5, sha1, and sha256 hashes.

As of 2021, md5, and sha1 hashes are no longer considered secure; however sha256 is still considered to be secure. Therefore if a user can verify that the initial Release file has not been tampered with, then they could make use of the sha256 to verify the Packages file, then use the sha256 contained in the Packages file
to verify the deb file.

In order to sign the apt repo, all we must do is sign the Release file.

### PGP, GPG, and GnuPGP

*PGP, OpenPGP, GnuPG, GPG, (and careful not to typo PHP).*

Software has a lot of acronyms, and this extends into digital signatures.
"Pretty Good Privacy" (PGP), was created in 1991 by Phil Zimmermann and eventually became the main product of non other than PGP Inc.
To encourage adoption of PGP, the company created an open standard unsurprisingly called OpenPGP.

OpenPGP is only a specification, that's where GNU Privacy Guard (GPG) fits in: GPG is an implementation of (Open)PGP. So is it a PGP key,
or a GPG key? I don't know, I've seen it called both, I'm going to call it a PGP because that's what is contained in the first line of
the armoured text: `