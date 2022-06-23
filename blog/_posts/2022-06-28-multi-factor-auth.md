---
title: "Programmatic Multi Factor Auth and Time Based One Time Passwords"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - mfa
---

"You need to setup multi-factor authentication."

This is what I was told. I already had a YubiKey, but I wasn't using it for my AWS credentials and this was not smart. So many AWS account get compromised:

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/2090.png --alt {{ MFA troubles on reddit AWS }} %}
</div>

Previously, I'd had a slightly bad time with YubiKeys: My computer fell and crushed my YubiKey. MFA is great until you lose an F. But [Alex](/blog/authors/alex/) gave me a great solution to this problem – securely store the MFA secret key.

<div class="notice--info">

### Side Note: You Should MFA

If you have something valuable online, something that can be stolen or turned into bitcoin you should set up multi-factor authentication for it. Previously this was often called 2FA, two-factor-authentication.
</div>

## MFA Setup in AWS

I set up a virtual MFA device in AWS and before adding it to google authenticator on my phone using the QR code, I grabbed the secret key and stored it somewhere secure.  

{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/2220.png --alt {{ MFA In Amazon }} %}

I stored it in LastPass but it could have been stored on paper in a safe or in [Earthly Secrets](https://docs.earthly.dev/docs/guides/cloud-secrets). This Virtual MFA secret key needs to be treated securely because anyone with it can generate the one-time-passwords I'm using for multi-factor authentication.

Now if I break another YubiKey, or brick my phone, I can always generate codes using the secret key or easily re-add it to my new phone. But, also now a new option is open for me. I can programmatically generate the OTP codes.

(This article is not security advice, I'm not qualified to give that, but again, be careful where you store your MFA secret key or what's the point of having it)

<div class="notice--info">
### Side Note: You Shouldn't Use SMS

In the past, the most common form of 2FA/MFA was an SMS based one time codes. This form of auth is simple to use since people have their phones on them all the time, but has a severe disadvantages in that [SIM Swapping](https://blog.mozilla.org/en/internet-culture/mozilla-explains/mozilla-explains-sim-swapping/) can be used by criminals to social engineer the phone company and take control of your phone number, intercepting the text.

For that reason, if security matters its best to avoid SMS based MFA.
</div>

### Generating TOTP Tokens Programmatically

If you have your secret key, its straightforward to do what google authenticator does, and generate a token. `oathtool` is a tool for doing this. You can install it with brew on a mac:

~~~{.bash caption=">_"}
brew install oathtool
~~~

Or use whatever package manager is right for you ( `sudo apt install oathtool` ... ). And then you can generate a time based one time password like this:

~~~{.bash caption=">_"}
oathtool -b --totp "{secret}"
~~~

~~~
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

You're going to want to store you MFA Key somewhere secure and not just keep it in a python script, or copy and paste it into your terminal and have it end up in your `.history` file. I'm using LastPass so I can install their CLI tool (`lpass`) and do something like this:

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

~~~{.bash caption=">_"}
$ mfa
654334
~~~

This strategy will also work with [1Password](https://app-updates.agilebits.com/product_history/CLI2), who's CLI tool is more fully featured. And you can also store your MFA token in Earthly secrets, a choice that is popular here at Earthly, or even store it directly on  [your YukiKey](https://scalesec.com/blog/why-your-yubikey-wont-work-with-aws-cli/). That solution is a little work, but if you crush your key like I did, you can get a new one and add your MFA token back.

{% include cta/cta1.html %}
