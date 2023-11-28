---
title: "Creating and hosting your own rpm packages and yum repo"
categories:
  - Tutorials
toc: true
author: Alex
bottomcta: false
internal-links:
  - rpm
  - yum
  - dnf
excerpt: |
    
last_modified_at: 2023-07-19
---
**In this article, you'll master RPM package creation. If you know RPM packaging, Earthly simplifies and improves your build process with containers. [Discover Earthly's benefits](/).**

<div class="narrow-code">

This tutorial is a follow up to [creating and hosting your own deb and apt repo](/blog/creating-and-hosting-your-own-deb-and-apt-repo), but
is written for creating rpm packages for redhat-based Linux distributions such as Fedora, CentOS, and Rocky Linux.

## Prerequisites

This tutorial assumes you are using CentOS 8, and that the following packages are installed:

```bash
sudo yum install -y createrepo rpm-build rpm-sign wget gcc python3 yum-utils
```

<div class="notice--info">
If you don't have a CentOS machine, you can still follow along using docker, just run

```bash
docker run -ti --rm centos:8 /bin/bash
```

to create a temporary CentOS environment to follow along with.
</div>

## Step 0: Creating a Simple Hello World Program

We will be using the same basic hello world program that was used in the [previous tutorial](/blog/creating-and-hosting-your-own-deb-and-apt-repo).
In this tutorial, we will assume you have a binary located under `~/example/hello-world-program/hello-world`.

To quickly create a hello world binary using C, run:

```bash
mkdir -p ~/example/hello-world-program
echo '#include <stdio.h>
int main() {
    printf("Hello World!\\n");
    return 0;
}' | gcc -o ~/example/hello-world-program/hello-world -x c -
```

This tutorial will only cover distributing binaries in rpm packages and will not cover creating source-based `rpm`s.
There's other [tutorials](https://www.thegeekstuff.com/2015/02/rpm-build-package-example/) that cover creating spec files --
the main goal of this tutorial is to document how to package a pre-compiled binary, and show how to generate your own self-hosted
yum repository.

## Step 1: Creating a `rpm` Package

Redhat-based Linux distributions use `.rpm` packages to package and distribute programs.

let's start by making a directory to work out of:

```bash
mkdir -p ~/example/rpm-work-dir
```

Inside this directory, we will create a `spec` file which contains package metadata such as the name, and summary of the package:

```bash
cd ~/example/rpm-work-dir
echo "Summary: A simple program that prints hello
Name: hello-world
Version: 1.0.0
Release: 1
URL: https://example.com
Group: System
License: example # https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Software_License_List
Packager: Example Team
Requires: bash
BuildRoot: ~/example/rpm-work-dir # this should be replaced with your working directory where the spec is saved

%description
An example package containing a hello-world binary

%install
mkdir -p %{buildroot}/usr/bin/
cp ~/example/hello-world-program/hello-world %{buildroot}/usr/bin/hello-world

%files
/usr/bin/hello-world

%changelog
* Thu Jun 17 2021 alex <alex@earthly.dev>
- initial example
" > hello-world.spec
```

Next, we will use `rpmbuild` to produce the `rpm`:

```bash
rpmbuild --target "x86_64" -bb hello-world.spec
```

This will output an rpm under `/root/rpmbuild/RPMS/x86_64/hello-world-1.0.0-1.x86_64.rpm`.

We can inspect the contents with:

```bash
rpm -qpivl --changelog --nomanifest /root/rpmbuild/RPMS/x86_64/hello-world-1.0.0-1.x86_64.rpm
```

which will output something similar to:

```
Name        : hello-world
Version     : 1.0.0
Release     : 1
Architecture: x86_64
Install Date: (not installed)
Group       : System
Size        : 10832
License     : example # https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Software_License_List
Signature   : (none)
Source RPM  : hello-world-1.0.0-1.src.rpm
Build Date  : Fri 18 Jun 2021 09:21:39 PM UTC
Build Host  : 83f4a9d4e295
Relocations : (not relocatable)
Packager    : Example Team
URL         : https://example.com
Summary     : A simple program that prints hello
Description :
An example package containing a hello-world binary
* Thu Jun 17 2021 alex <alex@earthly.dev>
- initial example

-rwxr-xr-x    1 root    root                    10832 Jun 18 21:21 /usr/bin/hello-world
drwxr-xr-x    2 root    root                        0 Jun 18 21:21 /usr/lib/.build-id
drwxr-xr-x    2 root    root                        0 Jun 18 21:21 /usr/lib/.build-id/b9
lrwxrwxrwx    1 root    root                       31 Jun 18 21:21 /usr/lib/.build-id/b9/fea765874fcd0863841bc8f5d1aa1d65396751 -> ../../../../usr/bin/hello-world
```

<div class="notice--info">

You can also inspect the content via `less /root/rpmbuild/RPMS/x86_64/hello-world-1.0.0-1.x86_64.rpm`.
Under the hood `less` will invoke `/usr/bin/lesspipe.sh`. You can perform a global regular expression print (grep)
against the script to find the same command being used:

```bash
grep rpm /usr/bin/lesspipe.sh
```

This should print the line where the same `rpm -qpivl ...` command is being invoked:

```bash
*.rpm) rpm -qpivl --changelog --nomanifest -- "$1"; exit $? ;;
```

</div>

Next, we can install our `rpm` via:

```
yum install -y /root/rpmbuild/RPMS/x86_64/hello-world-1.0.0-1.x86_64.rpm
```

Then finally, we can test it was installed by running

```bash
hello-world
```

which should print

```
Hello World!
```

## Step 2: Creating a `yum` Repository

Next we're going to create a yum repository which can be uploaded to a server to make it easier to share your package with other users.

Our first step will be to import a pgp key which we will be using to sign our rpm packages and repo, to allow our users to verify the packages have not been tampered.
Creating pgp keys was covered in our [previous tutorial](/blog/creating-and-hosting-your-own-deb-and-apt-repo); in particular, we will assume you have public and private keys stored
under `~/example/pgp-key.public` and `~/example/pgp-key.private` respectively.

First let's import our private key, so we have access to it for signing the repo:

```bash
gpg --import ~/example/pgp-key.private
```

This should output something similar to:

```
gpg: directory '/root/.gnupg' created
gpg: keybox '/root/.gnupg/pubring.kbx' created
gpg: /root/.gnupg/trustdb.gpg: trustdb created
gpg: key E1933532750E9EEF: public key "example <example@example.com>" imported
gpg: key E1933532750E9EEF: secret key imported
gpg: Total number processed: 1
gpg:               imported: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

We will then configure the rpm tools to use this key for signing our packages and repository:

```bash
echo "%_signature gpg
%_gpg_name E1933532750E9EEF" > /root/.rpmmacros
```

<div class="notice--info">
Don't forget to replace `E1933532750E9EEF` with your key's ID.
</div>

Let's create a directory for our packages:

```bash
mkdir -p ~/example/packages/
```

Then copy our rpm(s) into this directory:

```bash
cp /root/rpmbuild/RPMS/x86_64/hello-world-1.0.0-1.x86_64.rpm ~/example/packages/.
```

Since we didn't configure a key in step 1, the rpm we created was not signed. We can add a signature to it by running:

```bash
rpm --addsign ~/example/packages/*.rpm
```

<div class="notice--info">

If you forgot to create `/root/.rpmmacros`, or forgot to update the key ID, you might see an error such as
`You must set "%_gpg_name" in your macro file` or `gpg: signing failed: No secret key`.

</div>

Once all the packages are signed, we will use `createrepo` to create the repository:

```bash
cd ~/example/packages/
createrepo .
```

Finally, we will sign the repodata metadata by running:

```bash
gpg --detach-sign --armor repodata/repomd.xml
```

## Step 3: Testing the Repository

We are going to use python to temporarily create a web server to serve the contents of our repository:

```bash
cd ~/example
python3 -m http.server
```

We will create a config for this server:

```bash
echo "[example-repo]
name=Example Repo
baseurl=http://127.0.0.1:8000/packages
enabled=1
gpgcheck=1
gpgkey=http://127.0.0.1:8000/pgp-key.public" > ~/example/example.repo
```

Next let's configure our machine to use this new repository:

```bash
yum-config-manager --add-repo http://127.0.0.1:8000/example.repo
```

Then we can install our package from the self-hosted repository with:

```bash
yum install -y hello-world
```

<div class="notice--info">
In this example, we were hosting the entire contents of `~/example`, which may include your private key
if you followed this tutorial completely and created it under `~/example/pgp-key.private`. In practice, you would never serve
a directory containing your private key.
</div>

## Appendix A: A Complete Example using Earthly

A complete example has been created under [github.com/earthly/example-yum-repo/Earthfile](https://github.com/earthly/example-yum-repo/blob/main/Earthfile).

This Earthfile contains all the above steps from this tutorial in a single location, which can be run directly in a single shot with:

```bash
earthly -P github.com/earthly/example-yum-repo:main+test
```

Alternatively, you can clone the repo and run `+test` directly.

</div>