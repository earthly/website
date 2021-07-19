---
title: "6 Command Line Tools That make me more Productive"
categories:
  - Tutorials
author: Adam

internal-links:
 - just an example
---

Tools are powerful. A good tool makes work easier and faster, and a great tool unlocks new abilities: Previously impossible things -- or at least so things so complicated that it wasn't worth the effort -- become possible and sometimes easy.

Lately I have been adding some tools to my MacOS command-line toolbox. Many experienced command-line users stick strictly to the POSIX standard [command-line tools](https://en.wikipedia.org/wiki/List_of_Unix_commands) like `grep`,`awk` and `cat` but there are many powerful tools beyond those. Here are a few I'm finding valuable.

## `broot`

I'm not sure how Interesting I came across `broot`, but it's pretty handy. If you are in a small directory and want to see the lay of the land, `tree` is excellent.

```
✗ tree
.
├── dartboard.png
├── header.jpg
├── opensign.png
├── quote1.png
└── trophy.png

0 directories, 5 files
```

However, if the directory has many files or sub-directories, `tree` becomes much less helpful: you only see the last screen full of information as files scroll past you.

```
$ tree 
< scrolling text for a long time >
├── banner.js
└── index.html

328 directories, 2028 files
```

`broot` solves this problem by being aware of the size of your terminal window and sizing to fit it.

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/broot.png --picture --alt {{ bRoot }} %}
</div>

You can navigate around using the arrow keys in `broot` and it is also helpful for tracking down disk space usage by passing in the `-w` flag (`broot -w`):

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/broot2.png --picture --alt {{ broot -w }} %}
</div>

It can do lots of other things, so take a look at the [GitHub guide](https://github.com/Canop/broot) but for me its just a better `tree`.

<div class="notice--info">
**ℹ️ Install BRoot**

Install on MacOS using `brew` or follow [installation instructions](https://dystroy.org/broot/install/) for other environments.

``` bash
brew install broot
```

</div>

## Funky

If you live in the terminal, and you want to [use your terminal as an IDE](https://blog.sanctum.geek.nz/unix-as-ide-files/), then it's helpful to have your terminal change based on the current directory. There are many ways to do this.  [`DirEnv`](https://direnv.net/) loads and unloads `.env` files as you enter directories.  [`smartcd`](https://github.com/cxreg/smartcd) is similar. It lets you run a shell script whenever you change to a certain path -- you can start and stop services, change the prompt, or anything else you want.  

However, my favorite of this genre is the strangely named [`funky`](https://github.com/bbugyi200/funky), which "takes shell functions to the next level by making them easier to define, more flexible, and more interactive."

The way `funky` works is simple: as you enter a directory, `funky` looks for a `.funky` file which contains a list of bash functions. It loads them, and when you leave, it unloads them.

This means when I'm in the directory for this Jekyll blog, I have aliases loaded for creating a new post, linting my markdown, pulling in images, and so on. I can list these by typing `funky`

```
$ funky
lint() { markdownlint --fix "./_posts/*.md"; }
new-post() {  cat ./blog/_posts/2029-01-01-checklist.md > ./blog/_posts/$(date -v +7d +"%Y-%m-%d")-$1.md }
```

`funky` can do more than this, though. It has features for interactively adding and editing functions, and for registering global functions and aliases. What I like, though, is just being able to quickly give a command, in a specific context, a short alias.

<div class="notice--info">
**ℹ️ Install Funky**

Install Funky using pip

``` bash
pip3 install pyfunky
```

Then add hooks to your `.zshrc`, `bashrc` or equivalent:

``` bash
## find where funky.sh was installed by pip and source it
source /usr/local/lib/python3.9/site-packages/scripts/shell/funky.sh
```

</div>

## Fuzzy Finder (FZF)

If `funky` and `broot` improved my productivity then more tools could only improve it more, right? So I headed over to [Lobste.rs](https://lobste.rs/s/yfgwjr/what_interesting_command_line_tools_do) and asked what other tools people were using.  `FZF` came up quite a bit, and I've started using it myself now.

[FZF](https://github.com/junegunn/fzf) is a command-line fuzzy finder. It's fast, and it interactively lets you filter options down based on a fuzzy keyword match in many places where you need to input a value at the command-line.

If you install the included shortcuts (`/usr/local/opt/fzf/install`), you can use `**` anywhere and get an interactive fuzzy finder to narrow down to the desired path. `FZF` also makes searching your `history` much faster.

> This `fzf` video is pretty amazing. The man's voice is so calm and pleasant and the piano that keeps fading up and down just makes everything feel very relaxing
> [Freemasen](https://freemasen.com/blog/) on CoRecursive Slack Channel

It's a unix filter that reads in input, shows you an interactive list that you filter down and then sends the selected item out the other side but describing that way undersells its usefulness. I recommend watching this [video](https://www.youtube.com/watch?v=qgG5Jhi_Els) where Alexey Samoshkin walks through many possible uses for `FZF` with a soothing piano playing in the background.

<div class="notice--info">
**ℹ️ Install FZF**

Install Funky using your [package manager of choice](https://github.com/junegunn/fzf#using-linux-package-managers):

``` bash
brew install fzf
```

Then add hooks to your `.zshrc`, `bashrc` or equivalent:

``` bash
#ZSH
source ~/.fzf.zsh 
#BASH
source ~/.fzf.bash
```

</div>

## McFly

`FZF` is excellent for filtering file paths in a command line when you want to open a file (`vim **`), but for command-line completion, there is more information available than the raw history file. [`McFly`](https://github.com/cantino/mcfly/) attempts to use this extra information to provide more relevant results.

What extra information? To start with, McFly considers these options in its ranking heuristics:

- The commands you typed before the command.
- How often you run the command.
- How recently you ran the command.

It tracks all this in a SQLite database where it also tracks and weighs suggestions by:

- The commands exit status.
- The directory you ran the command in.
- If you have selected it in McFly before.

Being suggested failed commands is a pet peeve of mine, but I never considered narrowing the choice based on the current directory or down-ranking items that are never selected.

`McFly` uses a neural net to do its ranking, and one possible downside is the lag in coming up with suggestions if your SQLite database gets too large. However, `MCFLY_HISTORY_LIMIT` is available to limit this growth.

I've only been using it for a couple of days, so I can't give a fair appraisal of it, but the concept makes me pretty hopeful: using extra information to customize tools towards real-world usage.

<div class="notice--info">
**ℹ️ Install McFly**

You can install McFly [several ways](https://github.com/cantino/mcfly/#installation). Here is brew: :

``` bash
brew tap cantino/mcfly
brew install mcfly
```

Then add hooks to your `.zshrc`, `bashrc` or equivalent:

``` bash
eval "$(mcfly init zsh)"
```

The fact that the binary emits the init script rather than dumping an init script into my home directory is a nice touch. `zoxide` - the following tool - does this as well.

I found that `FZF` was interfering with the `CTRL-R` of McFly and had to comment out [this line](https://github.com/junegunn/fzf/blob/764316a53d0eb60b315f0bbcd513de58ed57a876/shell/key-bindings.zsh#L109) in the `FZF` init script to get McFly working.
</div>

## Better CD

`FZF` works nicely for some path completions, but I didn't find it helpful when changing directories with `cd`: After typing `cd **TAB` from my home directory, it takes a while for `FZF` to build up the full list options. It was much faster to use my existing ZSH completions of `cd TAB <choose a dir> TAB <choose a dir>` to navigate to a folder.  

However, many tools exist which attempt to improve upon `cd`. [`autojump`](https://github.com/wting/autojump), [`z`](https://github.com/rupa/z), and [`Fasd`](https://github.com/clvv/fasd) all track directory usage and give you a single key shortcut for changing to commonly accessed directories. [`r/commandline`](https://www.reddit.com/r/commandline/comments/4v5nlt/what_cd_tool_do_you_use_if_any_autojump_j_z_etc/) has an detailed discussion of these various `cd` replacements, but the one that has the most momentum is `zoxide`. [zoxide](https://github.com/ajeetdsouza/zoxide) is a rewrite of z in Rust and promises improved speed.

After you install it, you can use it just like `cd` (`z ~/path/foo/bar`), but you can also change directories based on ranked text matches of the path (`z bar` ~= `cd ~/path/foo/bar` ). Instead of needing to supply the full path to change locations, you can instead provide a unique sub-string of the path, and `zoxide` will use its usage history to get you where you want.

For ease of adoption, I've chosen to have `zoxide` replace `cd`, which is as simple as using the `--cmd` flag when you add the initialization shell code (`eval "$(zoxide init zsh --cmd cd)"`).

<div class="notice--info">
**ℹ️ Install zoxide**

`zoxide` can be installed [several ways](https://github.com/ajeetdsouza/zoxide#step-1-install-zoxide). Here is brew: :

``` bash
brew install zoxide
```

Then add hooks to your `.zshrc`, `bashrc` or equivalent:

``` bash
eval "$(zoxide init zsh --cmd cd)"
```

</div>

## GitUpdate

This tool is another find from the [Lobste.rs] thread. When working on a git branch, I like to commit my work frequently. For example, before I try to delete some large block of text in a blog post, or before I attempt to refactor some piece of code, I commit my work. Of course, I'll squash, or restructure, these commits later on, but for convenience, I have a git alias called `wip` ('work in progress`) which gives me a low effort way to commit.

```
git wip = !git add --all; git ci -m WIP
```

[`gitupdate`](https://github.com/nikitavoloboev/gitupdate) is a simple improvement on this idea. `gitupdate .` commits your files but uses the file names (but not extensions) of the changed files to create a more meaningful commit message. It's great for times when the commit message doesn't matter.

<div class="notice--info">
**ℹ️ Install GitUpdate**

``` bash
git clone https://github.com/nikitavoloboev/gitupdate
go build
sudo cp gitupdate /usr/local/bin
```

</div>

## Other Tools

There are many other helpful command-line tools. More than can be covered well in a single article. JQ, [`mitmproxy`](/blog/mitmproxy), [Pandoc](https://pandoc.org/), and [PSTree](https://man7.org/linux/man-pages/man1/pstree.1.html) are some I use frequently. There is also a whole class of Rust rewrites of common POSIX tools that warrant an article of their own.  

Of course, [Earthly](https://earthly.dev/) itself is a command-line tool, and one I constantly use for gluing together various development steps together. It, and the tools I use for [linting prose](/blog/markdown-lint) have become a standard part of how I work.

What less common command-line tools do you use? If you have tool suggestions, I'd love to hear them. You can find my Twitter account and email below and I'd love to hear what you are using.
