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
last_modified_at: 2023-07-14
---
**This article explores SSH key encryption. Earthly simplifies your build and test workflows. [Discover how](https://cloud.earthly.dev/login).**

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
    +---[RSA 3072]----+
    |  . ..           |
    |.. . o .        |
    |+ .. . o         |
    | +o o ...        |
    | ..... *So..     |
    |   . .=++o=..    |
    |     =o.+..+     |
    |    + ++oo oo.   |
    |   o.=XBEoo oo.  |
    +----[SHA256]-----+
~~~

Perfect, we can then display my public key with:

~~~{.bash caption=">_"}
    $ cat /tmp/testkey.pub 
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQDBRl0U4mwO/jQ7kYJidSnQy \
    0ci45j1QZ1do7NEC/08cG0jbNCSX6mblFr0JWruLpp6Z1WA/BL+Gng \
    CwATBeEt7dSAHNpOvT0fJ4roWv6/KmOLOCjKq26a0MvMf1g/YFa5 \
    tP5Zi7UW5Hp4vGCTXRPyywNJvh1/cHKuq2j79fUX+4cG9p01a1 \
    Y89/a3Q7L5UkB4JoFuaA9sVzVg4H5A2vRVR/pEIRRFuPuxHD \
    VcNblA6CsKFf0zBoLatXv+aBn86dX8EtwB13HdRsKq+XmBwn \
    WJiS+Cz1GBhnKf4LM/Ca46qy2ExQnOOt49COUOoU6DI7P5bf4I33pN \
    DDLoTvFFKzyXWTRgwg1tiyiRzfIjO+mg0kQM/dZ7+M8W49AQv \
    +MR8Uh0bykECXn6u8yEibEgInYlj0ziWXtf6lPEg+505hDTLlvPWX \
    po8nLluR5COwgFVSbNcMnY9o3KHeog598mQxiqrXWWbGmra7SgXrKmqJGqUbkZqH \
    1z8l6QfFo9nTBlYI0k= alex@earthly
~~~

and since we're all friends here, I'll share my example private key (you should never share your key with anyone, I'm only sharing this as an example -- I won't ever be using this key anywhere).

~~~{.bash caption=">_"}
    $ cat /tmp/testkey
    -----BEGIN OPENSSH PRIVATE KEY-----
    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
    nuAwC6Meoqs1kAAAAIYWxleEBtYWgBAgM=
    -----END OPENSSH PRIVATE KEY-----
~~~

Ok great, now how do we do that with go?

~~~{.go caption="main.go"}
    package main
    
    import (
     "crypto/rand"
     "crypto/rsa"
     "encoding/pem"
     "crypto/x509"
     "fmt"
    
     "golang.org/x/crypto/ssh"
    )
    
    func marshalRSAPrivate(priv *rsa.PrivateKey) string {
     return string(pem.EncodeToMemory(&pem.Block{
      Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(priv),
     }))
    }
    
    func generateKey() (string, string, error) {
     reader := rand.Reader
     bitSize := 2048
    
     key, err := rsa.GenerateKey(reader, bitSize)
     if err != nil {
      return "", "", err
     }
    
     pub, err := ssh.NewPublicKey(key.Public())
     if err != nil {
      return "", "", err
     }
     pubKeyStr := string(ssh.MarshalAuthorizedKey(pub))
     privKeyStr := marshalRSAPrivate(key)
    
     return pubKeyStr, privKeyStr, nil
    }
    
    func main() {
     pubKey, privKey, _ := generateKey()
     fmt.Println("my public key is...")
     fmt.Println(pubKey)
     fmt.Println("my private key is...")
     fmt.Println(privKey)
    }
~~~

Try it out in the [go playground](https://play.golang.org/p/chkKzvcGJcV), you should see something like this:

~~~{.bash caption="Output"}
    my public key is...
    ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC97wOspXmARcUFThWVlNMnw\
    xIiDIW7CrshmPRDfBV7RYlRtiNuSLlFaAIeXUGPWFnKzivScpBntrF\
    qqj+aJRQ27/tsM/n5jT6ERnoJTbyF+jYCx5BxST5lssVSRrXJQ0dLKSD6OE\
    vTKHK50RrxVtdU2E1cknwQWsYC2514xwmWYwEiNfFkO0QrU27BunPO/Gam+GJNTL\
    t7o7diM0GawuqVI1S/hf0T7goMTA9wX7KaIDg5Q1x+/0MJa1kT7LswG8Rw2\
    TFXRqI9Q+4UmmWN1MxBpeVK8VWx7NY9ngXnHUnJdzrXB4+E95Sn\
    KyhzaTlBnWDs9Em606SRb+g+tSYXl8DD
    
    my private key is...
    -----BEGIN RSA PRIVATE KEY-----
    MIIEogIBAAKCAQEAve8DrKV5gEXFBU4VlZTTJ8MSIgyFuwq7IZj0Q3wVe0WJUbYj
    bki5RWgCHl1Bj1hZys4r0nKQZ7axaqo/miUUNu/7bDP5+Y0+hEZ6CU28hfo2AseQ
    cUk+ZbLFUka1yUNHSykg+jhL0yhyudEa8VbXVNhNXJJ8EFrGAtudeMcJlmMBIjXx
    ZDtEK1NuwbpzzvxmpvhiTUy7e6O3YjNBmsLqlSNUv4X9E+4KDEwPcF+ymiA4OUNc
    fv9DCWtZE+y7MBvEcNkxV0aiPUPuFJpljdTMQaXlSvFVsezWPZ4F5x1JyXc61weP
    hPeUpysoc2k5QZ1g7PRJutOkkW/oPrUmF5fAwwIDAQABAoIBAHQGpaT69Q0yEdha
    yf61ioRYuyQHqE4JkSVGDbmH/ItwgCFldaFyVZObpOetqlYJ79hfOA/4IlTpGtqB
    JBdjHUUuNtXzrnoPGaiucPBsB4WEwyfRh2BdEPwJSFcpkPVg3xWAC4AvkcpthCAV
    KDNUDHjtJd0uMxG+kgW+6SSV2jp+NBMjEnL+6vSXQZ/wB6DU8bRa4VlAjA7xSeTX
    +NAS41yPSye/7F2lrSNT4VY8o5k8iRi7K91G1kJn+ewWdQMZEqzz29e1Uk3uxVV9
    XtcJuwsQ9oZ26rsO2PRXTRSE7cZUIhiIZ82ixmbhG1Oe0METpC47dlwwJuJOpJ61
    qszhAvkCgYEAyksKTxrv2pyt08UIRQJykvo72VVGT9IzLXQ07XymIF4m9JHHV13l
    HHbaxuDgzaoEBU3U9aRNi/U7J8o7c9U/sTv6q9JUI28VjrWOFHWafJbpSODy1yfz
    kKlPjXy0UvMHc1DREqDiPQYvdWz4JMp/C6dYS+A300HyUM7423OhHw0CgYEA8Fv0
    qfPoYetGX0Zf47xm0gku2ylj+0OoW0m8H4RXezptoPq0Piz1Lvq0RfubJVSUA9/S
    3epMZ7kFjxZEKfm4wprZpNkpFzbjmDwsx3COcsEcWcMuMf+DEJMsTwuF/I122vPe
    Boe+lTCi+2YWnAilbrQJXtpX3SMhFYtvKla+6w8CgYB1iqSy0jQMEn3uTs4/SuzH
    +h5MagAw4TJbdupKE+Nza0G3Wf06BpTZtTXp2UDGP8OWUWMsWAu3BwcYV6mz5HTd
    xrwgmlXJQQKFqXik6rCZNBbZAdwYqF4d8EMJMyyUBiKOHqdc656JVs68rFSDDCZF
    3zau39mQJwFlct2mpck5AQKBgC6sTIgr+rX478NUcQ5R6U1jxxt7oBSMgMapPMSJ
    +ErPf7ZAuHtSU5H50MO+JdRL5ioSbmn1Mzz46qFsW3QjL8NqOlUObjI50FwhYzif
    HKof4Zd0lSXUTekMCxCWVkBCYBAIRtbRySpDNYLHwiAudaFXiHJIx8MDLUt3tfBs
    w8n1AoGASlCTgmtDfJDcJpCbbHXs0W/Fo7L5ye5qXp6RwOcDnZen0Owt7QXGbEJm
    QjQOuFshp/TZ5jGkv7t2iVBh1whOOpaOmODMKAhueey+NGU47/Ww5vUgwVX/+WJQ
    HddCttBCyHl0vj+Ok4U4JjH05La+7Yrm/5q9wG2KptFe8c+RbeE=
    -----END RSA PRIVATE KEY-----
~~~

Perfect! Now I can generate a public and private key via Go. I wonder how I can encrypt a message using a public key which can only be decrypted by someone with the private key. Let's try out some more code:
<!-- vale off -->
I want to keep my function signature as basic as possible for the purpose of learning, so we will pass in the public key as the regular base64-encoded id\_rsa keyformat, and let that function handle parsing it:
<!-- vale on -->

~~~{.go caption="main.go"}
    func encrypt(msg, publicKey string) (string, error) {
     parsed, _, _, _, err := ssh.ParseAuthorizedKey([]byte(publicKey))
     if err != nil {
      return "", err
     }
     // To get back to an *rsa.PublicKey, we need to first upgrade to the
     // ssh.CryptoPublicKey interface
     parsedCryptoKey := parsed.(ssh.CryptoPublicKey)
    
     // Then, we can call CryptoPublicKey() to get the \
     actual crypto.PublicKey
     pubCrypto := parsedCryptoKey.CryptoPublicKey()
    
     // Finally, we can convert back to an *rsa.PublicKey
     pub := pubCrypto.(*rsa.PublicKey)
    
     encryptedBytes, err := rsa.EncryptOAEP(
      sha256.New(),
      rand.Reader,
      pub,
      []byte(msg),
      nil)
     if err != nil {
      return "", err
     }
     return base64.StdEncoding.EncodeToString(encryptedBytes), nil
    }
~~~

Try out the [complete example](https://play.golang.org/p/KjvwPoJ6wT4)

Finally, how do we decrypt it?

~~~{.go caption="main.go"}
    func decrypt(data, priv string) (string, error) {
     data2, err := base64.StdEncoding.DecodeString(data)
     if err != nil {
      return "", err
     }
    
     block, _ := pem.Decode([]byte(priv))
     key, err := x509.ParsePKCS1PrivateKey(block.Bytes)
     if err != nil {
      return "", err
     }
    
     decrypted, err := rsa.DecryptOAEP(sha256.New(),\
     rand.Reader, key, data2, nil)
     if err != nil {
      return "", err
     }
     return string(decrypted), nil
    }
~~~

[Try it out](https://play.golang.org/p/a5u9PYWEjgs)

So there we have a end-to-end example of how to generate a new public/private key, and encrypt and decrypt data all in [GoLang](/blog/top-3-resources-to-learn-golang-in-2021).

Based on my experimentation with private/public key encryption in go, I put together a small program that allows users to share encrypted data between parties using a rather simple [command line tool on my personal repository](https://github.com/alexcb/secretshare)

Our server's authentication process is slightly different from the above code – we create a digital signature using the private key, which I'll be covering in a future blog post.
