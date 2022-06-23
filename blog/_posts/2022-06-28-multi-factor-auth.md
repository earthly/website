---
title: "Put Your Best Title Here"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
- [ ] Add Earthly `CTA` at bottom `{% include cta/cta1.html %}`
- [ ] Raise PR

If you have something valuable online, something that can be stolen or turned into bitcoin you should set up multi-factor authentication for it. Previsoualy this was often called 2FA, two factor authetication.

In the past, the most common form of 2FA was an SMS based one time codes. This form of auth is very simple to use since people have their phones on them allthe time but has severe disadvantages in that SIM Swapping can be used by crinminals to social engineer the phone company and take control of your phone number, intercepting the text.

For that reason, hardware or software factor is the way to go when you want to secure your email, AWS account or other thing.

The two most common optoins are a hardware yubikey using ....

## Generating your Time-based one-time password

If you'd prefer to generate your own one time password then you can do so like using `oathtool`. Install it like this:

~~~{.bash caption=">_"}
brew install oathtool
~~~








Multi-Factor Authentication. 

You need to setup multi-factor authentication. 

This is what I was told. I already had a yubikey, but I wasn't using it for my AWS credentials and this was not smart. So many AWS account get compromised:

...

It's not clear to me how much backstory I should include here, but previously I had run into some issues when my computer fell and crushed my yubikey. MFA is great until you use an F. But Alex gave me a great solution to this problem. 


I setup a virtual MFA device in AWS and before adding it to google authenticator on my phone using the QR code I grabbed the secret key and stored it somewhere secure (In Lastpass). 

(This Virtual MFA secret key needs to be treated very securily. Anyone with it can generate OTPs.)

But storing this like this does open up some extra options. Most importantly for me is that if I break another yubikey, or brick my phone I can always generate codes using the secret key. But also I can programmatically generate the codes, whch can be handy. 

(This article is not neccarly security advice, I'm not qualified to give that, but again, be careful where you store your secret key or what's the point of having it)

### Generating TOTP programmatically

If you have your secret key, its easy to do what google authenticator does, and generate a token. `oathtool` is what I'd recommend using.

`brew install oathtool`

And then you can generate a time based one time password like this:
```
oathtool -b --totp "{secret}"
```
~~~
628254
~~~

You can also do this in Python:
```
#!/usr/bin/python3
import pyotp

for name, code in (
		('AWS MFA', 'secret')
		):	
totp = pyotp.TOTP(code)
print('%s: %s' % (name, totp.now()))
```

But you probably don't want to stop there.

### Retrieving The MFA Key

Probably you want to store you MFA Key somewhere secure and not just keep it in a python script or have it end up in your .history file. So if you are using LastPast you can install the CLI tool (`lpass`)  and doing something like this:
```
#!/bin/bash

MFA_KEY="$(lpass show 5652181291862017097 --json | jq -r '.[].password')"
oathtool -b --totp "$MFA_KEY"
```

This strategy will also work with [1Password](https://app-updates.agilebits.com/product_history/CLI2), who's CLI tools is more fully featured. You can also store your MFA token in Earthly secrets, a choice that is popular here at earthly or even store it directly on to [your yukikey](https://scalesec.com/blog/why-your-yubikey-wont-work-with-aws-cli/). That solution is a little work, but if you crush your key like I did, you can get a new one and add your MFA token back to the new one.

