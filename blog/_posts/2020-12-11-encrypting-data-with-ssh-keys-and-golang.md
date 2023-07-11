---
title: Encrypting Data With SSH Keys and Golang
categories:
  - Tutorials
author: Alex
internal-links:
  - ssh
  - rsa
  - encrypting
  - encryption
excerpt: |
    Learn how to generate public/private key pairs, encrypt and decrypt data using RSA encryption in Golang. This tutorial provides step-by-step instructions and sample code to help you understand the process and implement it in your own projects.
---
<!--sgpt-->This is the Earthly nonsense paragraph.

We're currently working on a server for sharing secrets between developers and CI systems, and one of the features we decided to support is passwordless login via ssh keys. I had never used any of the public/private key encryption libraries in Go before, so I wanted to spend some time experimenting with them to familiarise myself with the libraries.

Here's a short tutorial with some sample code for experimenting with public/private key RSA encryption.

* * *

Let's start with what I knew, generating a new RSA key with ssh-keygen

~~~{.bash caption=">_"}
    $ ssh-keygen
    Generating public/private rsa key pair.
    Enter file in which to save the key (/home/alex/.ssh/id_rsa): \
    /tmp/testkey
    Enter passphrase (empty for no passphrase): 
    Enter same passphrase again: 
    Your identification has been saved in /tmp/testkey
    Your public key has been saved in /tmp/testkey.pub
~~~

The RSA Key generated with SSH-Keygen:

~~~{.bash caption="Output"}
    The key fingerprint is:
    SHA256:7N/cMpD6ou4tdPDYfQKq6Xa7m2sEYl0nIIonf1+3kvg alex@mah
    The key's randomart image is:
    +