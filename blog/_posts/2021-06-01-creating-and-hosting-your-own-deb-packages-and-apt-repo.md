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
bottomcta: false
excerpt: |
    Learn how to create and host your own deb packages and apt repository in this tutorial. You'll discover the step-by-step process of creating a deb package, setting up an apt repository, signing it with a PGP key, and testing it with apt commands.
last_modified_at: 2023-07-19
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. If you're creating and hosting your own deb packages, Earthly can help you build them. [Check it out](/).**

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
the armoured text: `-----BEGIN PGP PUBLIC KEY BLOCK-----`.

#### Creating a New Public/Private PGP Key Pair

Let's start with generating a PGP key pair. We will use the `--batch` feature of `gpg` rather than using the interactive prompt.
This has the benefit of generating keys in a repeatable way. First create a batch template by copying and pasting the following into your terminal:

```bash
echo "%echo Generating an example PGP key
Key-Type: RSA
Key-Length: 4096
Name-Real: example
Name-Email: example@example.com
Expire-Date: 0
%no-ask-passphrase
%no-protection
%commit" > /tmp/example-pgp-key.batch
```

then we will generate it under a new temporary gpg keyring:

```bash
export GNUPGHOME="$(mktemp -d ~/example/pgpkeys-XXXXXX)"
gpg --no-tty --batch --gen-key /tmp/example-pgp-key.batch
```

Since we overrode the GNUPGHOME to a temporary directory, we can keep this key separate from our other keys.
Let's take a quick look at the contents of the directory:

```bash
ls "$GNUPGHOME/private-keys-v1.d"
```

will show something along the lines of

```
A3FB218BA1929542FF110C7D1B077B6469F769C9.key
```

which contains binary data. We can also view all of our loaded keys with:

```bash
gpg --list-keys
```

which will show something similar to

```
/home/alex/example/pgpkeys-pyml86/pubring.kbx
-------------------------------
pub   rsa4096 2021-05-18 [SCEA]
      B4D5C8B003C50A38A7E85B5989376CAC59892E72
uid           [ultimate] example <example@example.com>
```

This PGP key is comprised of both a public key, and a private key. Let's start with exporting the public key:

```bash
gpg --armor --export example > ~/example/pgp-key.public
```

Alternatively, you can reference the key by the email address or even the associated hex code. This should result in a public key that looks like:

```
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBGCkNmcBEADjEcDdne3ti5derY+hSPnhrBWeBba/1gb3S7lKwsysFlxeAApU
mROTk7gijH84GofOkZzQw9PJEA4u4kkF6EFfOr+VS3JDt5kYjpGorXMD8iRtJAIq
Y6hX7vqNDHpXFHSEEBIFCUF9E3yf8p7Wrohe0/6HVz1m/XAcU34zWY3a4zfgntsd
r4hj1h3E/GkZEI8UpB+/LshzbIoZMEDy+EB3EX/oCstZc9aKTUZLP9q5r3CvbrJU
s3354N+XFxCocVv4c/UFtcUI14EfQv7LVB2JRWYrit65DAHx87V4xcajqbkswvYn
4ela0DCW/Bw2jz1DaEHLGzn9me6z+YYH8VWbYqUJ/hrHHHSqjjSZ3S5E8gLVzTuf
IpoWUCSNeZlltBqoWf4ei7Q4nhzFi7AkvLABSkmx7R1+7fOH0ZIN+M2G6lOgcHEU
IiS7v6ygyj1U2h+38xn66dDH/gUhjp0zJfivMnC1c7pz7R4zNhFxyv1cyekP1nJA
wmpW+Y5ja3qSJYCHGmrtNaQIVMo2Ho1aXZiMysaTXKp4CYluoUsh97GjLtksq834
y3+FHdGMt8dGFBCRlZ9BFr1B++FZvuovbLoS+ZREmXTQPXYhN0TinpmnSFJsY6DK
5zFOU9j3Mtmf77MxUA+xsKBQrDgGM76uN7ADTc0jrUo4hECxnXQkOGyYrQARAQAB
tB1leGFtcGxlIDxleGFtcGxlQGV4YW1wbGUuY29tPokCTgQTAQoAOBYhBLTVyLAD
xQo4p+hbWYk3bKxZiS5yBQJgpDZnAhsvBQsJCAcCBhUKCQgLAgQWAgMBAh4BAheA
AAoJEIk3bKxZiS5yTUMP/1nlYpQTf8tQgSwSVUM8jhBhdOEEzmsXy/90KgpjX9WF
ABSC61SnGRonO60dn5CHT4oi0yJRKtsjJ3ZXLyxJY4Myop4ZCoJCcJw6sBOc3rvl
GN4J4O3+DZn7KRGUKFmLgeuxie2tSHdWYkonlpGPQ34xLgKT6Uf1NQOcCLZpMBim
2kxNXnnQXLEKXlbm9xmi/koub1qpko01T9DT9g9mlkv56660+sOw0XNwGmPy6HJ2
2IND53LYDNQv4qbt00ws29AUmZ6WmlUB9oP/nMx56Urgvmn6p/CLB9vbwIAb6egq
ZouUKsFAFyO5oVH3JoNBYbT84QewQv9BnJVQjuh0wK3OdCBjzT3YcBuRVwVJubKv
nSjvkJtq20tgxDSPc5ostzMpT5ZnBV+VQa6fwqBgb7VIGEPQklo6IZRwDH0rX1IA
Xpe2dZOvUICqvg17ol29uQ81BRpB7UynPDbgPDhBbELELPQN/GfaL+op8AB+cbga
JgC1JcX08nOqnT9TMpfig4TEpL/BKO+3cFy0Sttm44zMrR1f1SiyXdjZTS715LM/
nmAQWCZFMqN+5nHfT6lwJlqmtRCvjvHPdZla8Ah6B9oB+vJs1cClYJLSZuun89P/
bmQ5z+qJwCUOEVhVcVPTHAkqCTX2apQBeAszcmk54bGc/Q6UKncOgvOkELS7VuPt
=DYDE
-----END PGP PUBLIC KEY BLOCK-----
```

<div class="notice--info">
If the exported key is much larger than this, you may have exported multiple keys which can cause issues with some repositories.
</div>

You can verify only a single key was exported by running:

```bash
cat ~/example/pgp-key.public | gpg --list-packets
```

and checking that only a single `:public key packet:` entry exists. It should look something like this:

```
# off=0 ctb=99 tag=6 hlen=3 plen=525
:public key packet:
    version 4, algo 1, created 1621374567, expires 0
    pkey[0]: [4096 bits]
    pkey[1]: [17 bits]
    keyid: 89376CAC59892E72
# off=528 ctb=b4 tag=13 hlen=2 plen=29
:user ID packet: "example <example@example.com>"
# off=559 ctb=89 tag=2 hlen=3 plen=590
:signature packet: algo 1, keyid 89376CAC59892E72
    version 4, created 1621374567, md5len 0, sigclass 0x13
    digest algo 10, begin of digest 4d 43
    hashed subpkt 33 len 21 (issuer fpr v4 B4D5C8B003C50A38A7E85B5989376CAC59892E72)
    hashed subpkt 2 len 4 (sig created 2021-05-18)
    hashed subpkt 27 len 1 (key flags: 2F)
    hashed subpkt 11 len 4 (pref-sym-algos: 9 8 7 2)
    hashed subpkt 21 len 5 (pref-hash-algos: 10 9 8 11 2)
    hashed subpkt 22 len 3 (pref-zip-algos: 2 3 1)
    hashed subpkt 30 len 1 (features: 01)
    hashed subpkt 23 len 1 (keyserver preferences: 80)
    subpkt 16 len 8 (issuer key ID 89376CAC59892E72)
    data: [4095 bits]
```

Next let's export the private key so we can back it up somewhere safe.

```bash
gpg --armor --export-secret-keys example > ~/example/pgp-key.private
```

You should never share this key with anyone. If you look at the output file, it should look similar to this:

```
-----BEGIN PGP PRIVATE KEY BLOCK-----

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
=+Tgf
-----END PGP PRIVATE KEY BLOCK-----
```

<div class="notice--info">
The above is a burner-key I created for this article. It's never been used
for anything aside from this article. You should be generating your own key,
don't use this one.
</div>

Now that we've generated a PGP key pair, let's move on to signing files with them.

#### Signing the Release File

Before we start signing with out keys, let's make sure that we can import the backup we made.
To do that, we will create a new GPG keyring location:

```bash
export GNUPGHOME="$(mktemp -d ~/example/pgpkeys-XXXXXX)"
```

and then verify that it is empty:

```bash
gpg --list-keys
```

which should show something similar to:

```
gpg: keybox '/home/alex/example/pgpkeys-e7u1Ad/pubring.kbx' created
gpg: /home/alex/example/pgpkeys-e7u1Ad/trustdb.gpg: trustdb created
```

Next we will import our backed up private key:

```bash
cat ~/example/pgp-key.private | gpg --import
```

which should show a similar imported message:

```
gpg: key 4E793BC948F34C6F: public key "example <example@example.com>" imported
gpg: key 4E793BC948F34C6F: secret key imported
gpg: Total number processed: 1
gpg:               imported: 1
gpg:       secret keys read: 1
gpg:   secret keys imported: 1
```

and now if we run `gpg --list-keys`, we should see it is now available:

```
/home/alex/example/pgpkeys-e7u1Ad/pubring.kbx
---------------------------------------------
pub   rsa4096 2021-05-18 [SCEA]
      CFBFFC9CCD163CC7E1768BFF4E793BC948F34C6F
uid           [ unknown] example <example@example.com>
```

Ok, let's get around to signing the `Release` file now.

```bash
cat ~/example/apt-repo/dists/stable/Release | gpg --default-key example -abs > ~/example/apt-repo/dists/stable/Release.gpg
```

The contents of `Release.gpg` should be similar to this:

```
-----BEGIN PGP SIGNATURE-----

iQJIBAABCgAyFiEEz7/8nM0WPMfhdov/Tnk7yUjzTG8FAmCkTYYUHGV4YW1wbGVA
ZXhhbXBsZS5jb20ACgkQTnk7yUjzTG+f2g//QpVA4RP5qp2mAlolhqKCqLr6r7DX
mUC5ueSISXlRwVK7l0xFADqw4uHsl+T0DIeX7K/efHyyqIYq+t8fCA8HbB5CmWFk
2rOa9jFR4G+afJ1mdfQYUHshwEzY+NIScg3suO0ZeILFXcTW6a6AzlwqI3pVy/b8
o/FCjj4hBnaPysDS1BmPqxjWvt5ilQR3RTodsFahr2FncmgZI8zvrbCey630O/Cs
ELLp9fqBQj//FEje/JgHtG6E85qjsod0Nstu5h2yEs9iwMP1+peMB80NLpyeacpS
CWbZmFgxqKL7JNSx04T8epL23Zg6trrzhvOzOiVp2+Ilg438LBrErSVO+3puWT2e
bR3jpFSg9ej0+90QnG3IIkZW1RSkitlpNiFGFrUvlBRE9tSjZMK10EofPtzENEWN
uXYqjcWTJxp6R7d1IW/lTFzwdCPorgBPBbjmJ7Ux5YWZP7jjJmFpF9jSHVz6xDcp
oUBQcF4jHn5ewh0yKZQbqA3ZRXpPBDSNSraIDFToeFzhV94FQR2f5A5FgBR8n/Kr
Gfb76dsKabwVJlr7z8+W2C8gHmOe4dlVVUje3bxo05VNwZEBPbRldFox4GKIWT46
FbXyzB/EfRR7rzmaRfIpDfQa6hLOoivlat1no6akT7bK2mE7Y0L+Kae1dP+BpBUe
BqY84ZTkmQiOL0c=
=Dqab
-----END PGP SIGNATURE-----
```

Now when an apt client performs an update, it will fetch both `Release` and `Release.gpg` and will verify
the signature is valid; However to increase the speed, we will create a third file `InRelease` which will combine both the
contents of `Release` and the PGP signature:

```bash
cat ~/example/apt-repo/dists/stable/Release | gpg --default-key example -abs --clearsign > ~/example/apt-repo/dists/stable/InRelease
```

The contents of `InRelease` should be similar to this:

```
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA512

Origin: Example Repository
Label: Example
Suite: stable
Codename: stable
Version: 1.0
Architectures: amd64 arm64 arm7
Components: main
Description: An example software repository
Date: Tue, 18 May 2021 01:17:46 +0000
MD5Sum:
 d47739655e6312da85a96711f78c78db 405 main/binary-amd64/Packages
SHA1:
 d6aa46cf29cca1b01af6e9e256bf963ff5dfdaeb 405 main/binary-amd64/Packages
SHA256:
 3b888d4257fcf475fc06f74bd46045c3f1d667562fdb37e86f5bea642efa49f8 405 main/binary-amd64/Packages
-----BEGIN PGP SIGNATURE-----

iQJIBAEBCgAyFiEEz7/8nM0WPMfhdov/Tnk7yUjzTG8FAmCkT1wUHGV4YW1wbGVA
ZXhhbXBsZS5jb20ACgkQTnk7yUjzTG8w/RAAwB6HRyZWVOWT1A0OJAt+RlLREjev
gfRZVLZRDv18QRZKCcj71v0Ki1hX3xWE8WVjIR9eSXNf1wJvqza+/FBGN00NY1Bk
AFmypZP/04kjwGeUtULopLB1KrCaFdWuC9W49zUyeElIz1owX9tk+SsoLB7hGLQE
jtweFjxhaMeCHgSJIXDoR0RpmKBuydtB3UTHjCQJBvErkYfKrAJQCDYDz+XVPLh6
XPAohVb6SO4qBCxX30QcQpUVDRtMMRKbIOD5B+hjCP5cupvej1fBlzlFh4lBIywj
eUXrwBxmOiO/yrsYNoJJB+mV9u1mEpQDo7yRDCICsY2c/Io/Q0CxiEIIwoEfHCb/
WOFYYmUj1Sh9YARi74eTblMyr/Ay/9+opEr54uAixecJyC/kqsC3uptH4ZpOSwTw
hdj24Cl2veYmiCimPB4QCLOsCU5A1phwEkgADUOh4iRaszuzGkh/NZ0al0dCF0HY
/UsDuiMzEQGOP6ByILt1zoPrnwZKFDEbYjzSbjSXfkU9LKfrp5PWgeeq5iD58sQW
ZCE34ksK8W67GOtQuzy0Z8NlTJY1Mkzp7IsUt60owyv6dQVZFIPYwGEisGFSOCNk
3VZ66m1D6HtDZ60CZEJUhfu+WTC1K95cKYkhYArBR9pDecygYomLQVFO2T1ENxCA
BKaAtOSl2Jcb4eA=
=3Hft
-----END PGP SIGNATURE-----
```

#### Testing It Out

We need to tell apt which public pgp key to use when verifying the apt repository. We will add a new `signed-by` attribute
to our apt config:

```bash
echo "deb [arch=amd64 signed-by=$HOME/example/pgp-key.public] http://127.0.0.1:8000/apt-repo stable main" | sudo tee /etc/apt/sources.list.d/example.list
```

<div class="notice--info">
note that `$HOME` should be expanded to the absolute path of the pgp key.
</div>

Next start back up your web server:

```bash
cd ~/example
python3 -m http.server
```

Then finally try updating and re-installing our hello-world package:

```bash
sudo apt-get clean
sudo apt-get update
sudo apt-get install hello-world
```

This time you shouldn't see any security warnings.

#### Keeping Your Private Key Secure

If you followed this tutorial to the tee, and your web server is still running, what happens if we try running:

```bash
curl http://127.0.0.1:8000/pgp-key.private
```

Oh no! we just leaked our private key. Now's the time to regenerate it but using a real name and email address other than `example@example.com`.
Maybe you can store it in earthly's [secret store](https://docs.earthly.dev/docs/guides/cloud-secrets) instead?

## Appendix A: A Complete Example using Earthly

A complete example has been created under [github.com/earthly/example-apt-repo/Earthfile](https://github.com/earthly/example-apt-repo/blob/main/Earthfile).

This Earthfile contains all the above steps from this tutorial in a single location, which can be run directly in a single shot with:

```bash
earthly -P github.com/earthly/example-apt-repo:main+test
```

Alternatively, you can clone the repo and run `+test` directly.
<!-- vale HouseStyle.TLA = YES -->
<!-- vale HouseStyle.ListStart = YES -->
