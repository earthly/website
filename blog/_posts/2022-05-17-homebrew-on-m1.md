---
title: "Using Homebrew on an M1 Mac"
categories:
  - Tutorials
toc: true
author: Josh
tags:
- docker
- apple-silicon
- m1
- arm64
- aarch64
internal-links:
 - homebrew
 - apple Silicon
 - m1
 - arm
---

Homebrew made some changes to where it installs packages if you are running it on a new M1 Mac. These changes may throw you for a loop if your moving from an Intel Mac to M1. IN this artcle we'll talk about what changed and why it changed. I'll also walk you through getting all your Homebrew packages from your Intel Mac reinstalled on your M1, and share a couple of issues I came across after migrating that will hopefully help you with any gotchyas you encounter in the future.

## So What Changed?

The big change is where things are.

On Intel Macs, Homebrew and any packages you install using Homebrew went in `/usr/local/bin`.

~~~{.bash caption=">_ Intel"}
$ which brew
/usr/local/bin/brew
~~~

One reason Homebrew chose `/usr/local/bin` is because it is already in your `PATH`.

~~~{.bash caption=">_ M1"}
$ echo "${PATH//:/$'\n'}"
'/usr/local/bin$'
'/usr/bin$'
'/bin$'
~~~

One of the reasons Homebrew has become so popular is that it just works right out of the box, and installing in `/usr/local/bin` is at least part of the reason why.
But if you install Homebrew on a Mac running Apple Silicon, then Homebrew gets installed in `/opt/homebrew/bin`. 

~~~{.bash caption=">_"}
$ which brew
/opt/homebrew/bin/brew
~~~

Since `/opt/homebrew/bin` is not included in your `PATH` by default, there is some extra configuration needed to allow you to use packages installed with Homebrew. 

## Why did it change?

<blockquote class="twitter-tweet"><p lang="en" dir="ltr">The prefix /opt/homebrew was chosen to allow installations in /opt/homebrew for Apple Silicon and /usr/local for Rosetta 2 to coexist and use bottles.</p>&mdash; Homebrew Website</blockquote>

The the main motivation for the change was to allow the transition from Intel to Apple Silicon, but there are [other reasons](https://github.com/Homebrew/brew/issues/9177) for sticking with `/opt/homebrew` even after the Intel Macs are long gone.

1. Homebrew is not the only tool that installs things in `/usr/local` and so the potential for conflicts has always been an issue.
2. There are [security concerns](https://applehelpwriter.com/2018/03/21/how-homebrew-invites-users-to-get-pwned/) with using `/usr/local/`.
3. Other package managers have been using `/opt/<manager_name>` for a while now.
4. It gives the user more control.

So in the long run this is a positive change, but not without a few growing pains along the way.

## Migrating from Intel Mac

If you're coming to M1 Mac fresh, without any old projects or profiles, you probably won't notice; Homebrew will work as it always has. But if you're trying to migrate from an Intel Mac you won't be able to just move packages that were once in `/usr/local` over to `/opt/homebrew`. No need to worry though, reinstalling everything on M1 is easy, it just may take a bit of time.

### Create a Brewfile

Th first thing you'll want to do is run `brew bundle dump` on your Intel Mac. This will create a `Brewfile`, which is just a list of everything brew has installed and how to install it again. Here's part of mine to give you an idea of what it looks like.

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

Remember Homebrew is now going to install packages in `/op/homebrew/bin`. This new location is not part of your default PATH, so you'll need to add it. The easiest way to do that is to follow the instructions Homebrew spits out after intallation.

Add `eval "$(/opt/homebrew/bin/brew shellenv)"'` to your `.zshrc` or `.bashrc` file. Now this command will run each time you start a new shell instance. What it does is creates a series of environment variables, like `HOMEBREW_CELLAR="/opt/homebrew/Cellar"` and `HOMEBREW_REPOSITORY="/opt/homebrew"` and several others. In addition, it adds `/opt/homebrew/bin` to your path: `export PATH="/opt/homebrew/bin:/opt/homebrew/sbin${PATH+:$PATH}";`.

### Install Packages on M1

Once this is done, you'll need to copy over your `Brewfile` over from your Intel mac. Then, you can tell brew to install everything with `brew bundle install --file /path/to/Brewfile`. This may take a while if you have a lot of packages so probably best to have an actual beer nearby.

That should be it. After that I recommend going over any config files or profile files you have that might contain any references to Homebrew or packages you have installed. Of course, if you're like me, you're never going to remember all of them, so my best advice is to just keep the new Homebrew path in mind as you start to spin pu projects and use old software.

## Moving Pains

![Moving sucks]({{site.images}}{{page.slug}}/moving.jpg)\

I encountered a couple issues with this new installation, both related to the fact that Homebrew had moved from `/usr/local/bin`.

The first problem I ran into was pulling my old `.zshrc` file over from my Intel Mac onto my M1. I had been using `gnu-sed`, installed with brew. In order to get it to override the existing `sed` command on my machine I needed to point directly to it in my  PATH witch meant adding `export  PATH="/usr/local/opt/gnu-sed/libexec/gnubin:$PATH"` to my `.zshrc` file. (There may have been a better workaround for this but this worked so I stuck with it.) 

I'm pretty sure you can see the problem right away. Obviously the package was no longer in `/usr/local/opt`. The bigger problem was I had set up this work-around and forgotten about it, so it took me a bit to remember to check my `.zshrc` and update the `PATH`.

The second problem I had was the same idea, but took a little longer to debug. We run our blog with [Jekyll](https://jekyllrb.com/). Several of the third party libraries in our project rely on the [ffi](https://github.com/ffi/ffi/) Ruby gem. You can read more about [Foreign function interfaces](https://en.wikipedia.org/wiki/Foreign_function_interface) if you're interested, but what is relevant here is that if some bit of Ruby code in our blog needs to interact with a package installed by brew, it uses ffi to do it.

The problem I encountered was that ffi did not add `/opt/homebrew/lib/` to its list of search paths until [version 1.15.2](https://github.com/ffi/ffi/blob/master/CHANGELOG.md#1152--2021-06-16). We were running v1.15.0 ,so every time I tried to run the blog I kept getting `no such file or directory` errors because ffi wasn't updated to check `/opt/homebrew/lib`.

Again the fix was easy enough. Luckily the gem had already been patched to fix this issue, so all I needed to do was update it.

## Conclusion

So this was a lot of information but the main take away is, Homebrew moved and if you're having issues with it or any of its packages, the reason might be because other tools don't have Homebrew's new address. If you suspect that's the case, make sure you check that `/opt/homebrew/bin` is part of your PATH, and confirm that any third party software you're using has been updated to look in `/opt/homebrew/bin`.

One of the reasons people love Homebrew is because it just works. And on Apple Silicon, that's still true, but you might encounter a couple of hiccups along the way. I ended up learning a lot about Homebrew and how it works while digging a little deeper into this issue. If you want to learn more about Homebrew you can checkout their website, or this excellent [getting started tutorial](https://mac.install.guide/homebrew/3.html). And if you haven't already, it's worth reading a bit about [Rosetta 2](https://screenrant.com/apple-rosetta-2-explained/), since it's at the heart of what makes the switch to Apple Silicon possible.

{% include cta/cta1.html %}

- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] First two paragraphs: What's it about? Why listen to you?
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`lint`)
- [ ] Run `link-opp` and find 1-5 places to incorporate links to other articles
