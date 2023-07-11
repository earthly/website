---
title: "Using Homebrew on M1 Mac"
categories:
  - Articles
toc: true
author: Josh
tags:
- apple-silicon
- m1
- arm64
- aarch64
internal-links:
 - homebrew
 - apple silicon
 - m1
 - arm
topic: cli
last_modified_at: 2023-04-17
excerpt: |
    Learn about the changes in Homebrew installation on M1 Macs and how to migrate your packages from an Intel Mac. Discover the reasons behind the change and the potential issues you may encounter. Plus, get insights into updating old and third-party code to ensure smooth functioning.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster. This article is about Homebrew and some quirks of using it on the Mac M1. If you doing things at command line you might like [Earthly](https://earthly.dev/). It's a pretty great open-source build tool.**

Homebrew made some changes to where it installs packages if you are running it on a new M1 Mac, and these changes may throw you for a loop if you're moving over to an M1 from Intel. In this article I'll talk about what changed and why it changed. I'll also walk you through getting all your Homebrew packages from your Intel Mac reinstalled on your M1, and share a couple of issues I came across after migrating that will hopefully help you with any gotchas you encounter in the future.

## So What Changed?

The big change is where things are.

On Intel Macs, Homebrew, and any packages you install using Homebrew, go in `/usr/local/bin`.

<div class="narrow-code">

~~~{.bash caption=">_ Intel"}
$ which brew
/usr/local/bin/brew
~~~

</code>

Homebrew chose `/usr/local/bin` because it is already in your `PATH` by default.

~~~{.bash caption=">_ Intel"}
$ echo "${PATH//:/$'\n'}"
'/usr/local/bin$'
'/usr/bin$'
'/bin$'
~~~

One of the reasons Homebrew has become so popular is that it just works right out of the box, and installing in `/usr/local/bin` is at least part of the reason why.

But if you install Homebrew on an M1 Mac running Apple Silicon, then Homebrew gets installed in `/opt/homebrew/bin`.

~~~{.bash caption=">_M1"}
$ which brew
/opt/homebrew/bin/brew
~~~

Since `/opt/homebrew/bin` is not included in your `PATH` by default, there is some extra configuration needed to allow you to use packages installed with Homebrew.

## Why the Change?

The the main motivation for the change was to allow the transition from Intel to Apple Silicon.

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">In #9117, we switched to a new prefix of <code>/opt/homebrew</code> for installations on Apple Silicon. This was written and shipped with heroic speed to help prevent strange issues with bleeding edge users on the first consumer Apple Silicon Macs.</p>&mdash;Misty De Méo - Homebrew Maintainer </blockquote>

It could be possible to move everything back to `/usr/local/bin` in the future, but there are [other reasons](https://github.com/Homebrew/brew/issues/9177) for sticking with `/opt/homebrew` even after the Intel Macs are long gone.

1. Homebrew is not the only tool that installs things in `/usr/local/bin` and so the potential for conflicts has always been an issue.
2. There are [security concerns](https://applehelpwriter.com/2018/03/21/how-homebrew-invites-users-to-get-pwned/) with using `/usr/local/bin`.
3. Other package managers have been using `/opt/<manager_name>` for a while now.

So in the long run this is a positive change, but not without a few growing pains along the way.

## Migrating From Intel Mac

If you're coming to M1 Mac fresh, without any old projects or profiles, you probably won't notice; Homebrew will work as it always has. But if you're trying to migrate from an Intel Mac you won't be able to just move packages that were once in `/usr/local` over to `/opt/homebrew`. No need to worry though, reinstalling everything on M1 is easy, it just may take a bit of time.

### Create a Brewfile

Th first thing you'll want to do is run `brew bundle dump` on your Intel Mac. This will create a `Brewfile`, which is just a list of all packages that have been installed with brew. Here's part of mine to give you an idea of what it looks like.

~~~{.bash caption=">_"}
tap "earthly/earthly"
tap "homebrew/bundle"
tap "homebrew/core"
brew "python@3.10"
brew "asciinema"
brew "python@3.9"
brew "glib"
...
~~~

### Install Homebrew

Now, on your new M1 Mac, you can install Homebrew with `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`.

After the install is complete you'll see a message similar to the one below.

~~~{.bash caption=">_"}
==> Next steps:
- Run these two commands in your terminal to add Homebrew to your PATH:
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/joshalletto/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh
~~~

Remember, Homebrew is now going to install packages in `/op/homebrew/bin`. This new location is not part of your default `PATH`, so you'll need to add it. The easiest way to do that is to follow the instructions Homebrew spits out after installation.

Add `eval "$(/opt/homebrew/bin/brew shellenv)"'` to your `.zshrc` or `.bashrc`. Now this command will run each time you start a new shell instance. It creates a series of environment variables, including `HOMEBREW_CELLAR="/opt/homebrew/Cellar"` and `HOMEBREW_REPOSITORY="/opt/homebrew"` and several others.

Most importantly, it adds `/opt/homebrew/bin` to your path: `export PATH="/opt/homebrew/bin:/opt/homebrew/sbin${PATH+:$PATH}";`.

### Install Packages on M1

Once this is done, you'll need to copy over your `Brewfile` from your Intel Mac. You can tell brew to install everything with `brew bundle install --file /path/to/Brewfile`. This may take a while if you have a lot of packages so probably best to have an actual beer nearby.

That should be it. After that I recommend going over any config files or profile files you have that might contain any references to Homebrew or Homebrew packages you have installed.

## Moving Pains

![Moving sucks]({{site.images}}{{page.slug}}/moving.jpg)\

I encountered a couple issues with this new installation, both related to the fact that Homebrew had moved from `/usr/local/bin`. They are pretty specific to my set up, but hopefully a quick description of each one will help you track down similar issues if you encounter them.

### Update Old Code

The first problem I ran into came after pulling my old `.zshrc` file over from my Intel Mac onto my M1. I had been using `gnu-sed`, installed with brew. In order to get it to override the existing `sed` command on my machine I needed to point directly to it in my `PATH` which meant adding `export  PATH="/usr/local/opt/gnu-sed/libexec/gnubin:$PATH"` to my `.zshrc` file. (There may have been a better workaround for this but this worked so I stuck with it.)

I'm pretty sure you can see the problem right away. Obviously, the package was no longer in `/usr/local/opt/gnu-sed`. The fix was easy enough, just needed update my `PATH` in my `.zshrc` to the new location. The hard part was actually remembering that I had set up this override. For a very long while I could not figure out why my machine was using the default version of `sed` and it was driving me insane.

### Update Third Party Code

The second problem I had was the same idea. We run the Earthly blog with [Jekyll](https://jekyllrb.com/). Several of the third party libraries in our project rely on the [ffi](https://github.com/ffi/ffi/) Ruby gem. You can read more about [Foreign function interfaces](https://en.wikipedia.org/wiki/Foreign_function_interface) if you're interested, but what is relevant here is that if some bit of Ruby code in our blog needs to interact with a package installed by brew, it uses ffi to do it.

The problem I encountered was that ffi did not add `/opt/homebrew/lib/` to its list of search paths until [version 1.15.2](https://github.com/ffi/ffi/blob/master/CHANGELOG.md#1152--2021-06-16). We were running v1.15.0 ,so every time I tried to run the blog I kept getting `no such file or directory` errors because ffi wasn't updated to check `/opt/homebrew/lib`. Again, this was frustrating until I realized what was going on. The rabbit hole I went down because of this error is the reason I wrote this article.

Luckily, the gem had already been patched to fix this issue, so once I did realize what was going on, all I needed to do was update it.

## Conclusion

So this was a lot of information but the main take away is: Homebrew moved and if you're having issues with it or any of its packages, the reason might be because other tools haven't been made aware of Homebrew's new location. If you suspect that's the case, make sure you check that `/opt/homebrew/bin` is part of your PATH, and confirm that any third party software you're using has been updated to look in `/opt/homebrew/bin`.

One of the reasons people love Homebrew is because it just works. And on Apple Silicon, that's still true, but you might encounter a couple of hiccups along the way. I ended up learning a lot about Homebrew and how it works while digging a little deeper into this issue. If you want to learn more about Homebrew you can checkout their website, or this excellent [getting started tutorial](https://mac.install.guide/homebrew/3.html). And if you haven't already, it's worth reading a bit about [Rosetta 2](https://screenrant.com/apple-rosetta-2-explained/), since it's at the heart of what makes the switch to Apple Silicon possible, not just for Homebrew, but for all software switching over from Intel to M1.

Also, If you're homebrew, you probably and you haven't heard of [Earthly](/), then you should probably check it out. It's a open source tool for building linux software regardless of your host environment.  

{% include_html cta/bottom-cta.html %}
