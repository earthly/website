---
title: "Programmatic Multi Factor Auth and Time Based One Time Passwords"
categories:
  - cli
toc: false
author: Adam
internal-links:
 - mfa
excerpt: |
    Learn how to set up multi-factor authentication and generate time-based one-time passwords programmatically using MFA secret keys. Discover different methods for securely storing and retrieving MFA keys, including using LastPass, 1Password, Earthly secrets, or even your YubiKey.
last_modified_at: 2023-07-14
---
**This article explains the complexities of implementing Multi-Factor Authentication (MFA) for Amazon Web Services (AWS). Earthly simplifies Continuous Integration (CI) builds for AWS users who require MFA. [Learn how](https://cloud.earthly.dev/login).**

"You need to setup multi-factor authentication."

This is what I was told. I already had a YubiKey, but I wasn't using it for my AWS credentials and this was not smart. So many AWS accounts get compromised without MFA:

{% picture {{site.pimages}}{{page.slug}}/2090.png --alt {{ MFA troubles on reddit AWS }} %}

Previously, I'd had a slightly bad time with YubiKeys: My computer fell and crushed my key. MFA is great until you lose an F. But [Alex](/blog/authors/alex/) gave me a great solution to this problem – securely store the MFA secret key.

<div class="notice--info">

### Side Note: You Should MFA

If you have something valuable online, something that can be stolen or turned into bitcoin you should set up multi-factor authentication for it.

(FYI: Previously this was often called 2FA, two-factor-authentication.)
</div>

## MFA Setup in AWS

So here is what I did.

I set up a virtual MFA device in AWS and before adding it to google authenticator on my phone, using the QR code, I grabbed the secret key and stored it somewhere secure.  

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2220.png --alt {{ MFA In Amazon }} %}
</div>

I stored it in LastPass but it could have been stored on paper in a safe, or in [Earthly Secrets](https://docs.earthly.dev/earthly-cloud/cloud-secrets). This Virtual MFA secret key needs to be treated securely because anyone with it can generate the one-time-passwords that I'm using for multi-factor authentication.

Now if I break another YubiKey, or brick my phone, I can always generate codes using the secret key, or easily re-add it to my new phone. But also, now a new option is open for me: I can programmatically generate the OTP tokens.

(This article is not security advice, I'm not qualified to give that, but again, be careful where you store your MFA secret key or what's the point of having it!)

<div class="notice--info">

### Side Note: You Shouldn't Use SMS as a Authentication Factor

In the past, the most common form of 2FA/MFA was SMS based one-time codes. This form of auth is simple to use, since people have their phones on them all the time. But it has a severe disadvantages in that [SIM Swapping](https://blog.mozilla.org/en/internet-culture/mozilla-explains/mozilla-explains-sim-swapping/) can be used by criminals to social engineer the phone company into letting them take control of your phone number. If they do this, they can intercept your texts, and all is lost.

For that reason, if security matters its best to avoid SMS based MFA.
</div>

### Generating TOTP Tokens Programmatically

Here is a thing I learned. If you have your secret key, it's straightforward to do what google authenticator does, and generate a token. `oathtool` is a tool for doing this and you can install it with brew on a mac:

~~~{.bash caption=">_"}
brew install oathtool
~~~

Or use whatever package manager is right for you ( `sudo apt install oathtool` ... ). And then you can generate a time-based one-time password (totp) like this:

~~~{.bash caption=">_"}
oathtool -b --totp "{secret}"
~~~

~~~{.merge-code}
628254
~~~

You can also do this in Python:

~~~{.bash caption=">_"}
#!/usr/bin/python3
import pyotp

for name, code in (
  ('AWS MFA', 'secret')
  ): 
totp = pyotp.TOTP(code)
print('%s: %s' % (name, totp.now()))
~~~

But you don't want to stop there. You'd need a way to retrieve the key from somewhere safe.

### Retrieving the MFA Key

So here's what you do.

You're going to want to store you MFA Key somewhere secure, and not just keep it in a python script, or copy and paste it into your terminal. Because then it might end up in your `.history` file.

I'm using LastPass, so I can install their CLI tool (`lpass`) and do something like this:

~~~{.bash caption="mfa.sh"}
#!/bin/bash

mfa(){
  MFA_KEY="$(lpass show {entry_ID} --json | jq -r '.[].password')"
  oathtool -b --totp "$MFA_KEY"
}
~~~

And then I can get my MFA token like this

~~~{.bash caption=">_"}
$ lpass login usename 
...
~~~

~~~{.bash .merge-code caption=">_"}
$ mfa
654334
~~~

This strategy will also work with [1Password](https://app-updates.agilebits.com/product_history/CLI2), who's CLI tool is more fully featured. And also, you can store your MFA token in Earthly secrets, a popular choice here at Earthly. You can even store it directly on [your YukiKey](https://scalesec.com/blog/why-your-yubikey-wont-work-with-aws-cli/). That solution is a little bit more work, but if you crush your key like I did, you can get a new one and add your MFA token back.

So now you know what I know about MFA secret keys and how to store them, and use them to generate tokens and time-based one-time passwords for authentication.

{% include_html cta/bottom-cta.html %}
