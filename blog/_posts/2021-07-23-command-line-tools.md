---
title: "Command Line Tools"
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
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

Tools are powerful. A good tool makes work easier and faster and a great tool unlocks new abilities: Things that were previous impossible or at least so difficult that it wasn't worth the effort become possible and sometimes easy. 

Here are some command line tools I've found useful.

## BRoot

I'm not sure how I came across BRoot, but its pretty handy. If you are in a small directory and want to see the lay of the land `tree` is great.

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
However if the directory is large `tree` becomes much less useful: you only see the last screen full of information as files scroll past you.
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
**ℹ️ Install BRoot **

Install on MacOS using `brew` or follow [installation instructions](https://dystroy.org/broot/install/) for other environments.

``` bash
brew install broot
```

</div>

## Funky
If you live in the terminal and you want to [use your terminal as an IDE](https://blog.sanctum.geek.nz/unix-as-ide-files/) then its helpful to have your terminal change based on the current directory. There are many ways to do this.  [`DirEnv`](https://direnv.net/) loads and unloads `.env` files as you enter directories.  [`smartcd`](https://github.com/cxreg/smartcd) is similar it lets you run a shell script as you enter and leave each directory, which can be used to start and stop services, change the prompt or anything else you want.  

However, my favorite shell customizing tool is the strangely named [`funky`](https://github.com/bbugyi200/funky), which "takes shell functions to the next level by making them easier to define, more flexible, and more interactive."

The way `funky` works is simple, as you enter a directory `funky` looks for a `.funky` file which contains a list of bash functions. It loads those and when you leave it unloads them.

This means when I'm in the directory for this Jekyll blog I have aliases loaded for creating a new post, linting my markdown and so on. I can list these by typing `funky`

```
$ funky
lint() { markdownlint --fix "./_posts/*.md"; }
new-post() {  cat ./blog/_posts/2029-01-01-checklist.md > ./blog/_posts/$(date -v +7d +"%Y-%m-%d")-$1.md }
```
`funky` can do more than this though. It has nice features for interactively adding and editing functions and you can also registry global functions. What I like though it just being able to quickly give a command, in a specific context, a short alias.

<div class="notice--info">
**ℹ️ Install Funky **

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

If Funky and Broot improved my productivity then more tools could only improve it more right? I headed over to [Lobste.rs]() and asked what other tools people were using.  `FZF` came up quite a bit and I've started using it myself now.

[FZF](https://github.com/junegunn/fzf) is a command line fuzzy finder. It's fast and it interactively lets you filter options down based on a fuzzy keyword match in many places where you need to input a value at the command-line. 

If you install the included shortcuts (`/usr/local/opt/fzf/install`), you can use `**` anywhere and get an interactive fuzzy finder to narrow down to the desired path. `FZF` also makes searching your `history` much faster. 

> This `fzf` video is pretty amazing. The man's voice is so calm and pleasant and the piano that keeps fading up and down just makes everything feel very relaxing
> [Freemasen](https://freemasen.com/blog/) on CoRecursive Slack Channel

It's a unix filter that reads in input, shows you an interactive list that you filter down and then sends the selected item out the side but describing that way unsells its usefulness I recommend watching this video from Alexey Samoshkin's [video](https://www.youtube.com/watch?v=qgG5Jhi_Els) where he walks through many possible uses for it with a soothing piano playing in the background.

<div class="notice--info">
**ℹ️ Install FZF **

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
`FZF` is great for filtering file paths in a command line when you want to open a file (`vim **`) but for command line completion there is more information available then just a raw history file and [`McFly`](https://github.com/cantino/mcfly/) attempts to use this extra information provide more relevant results.

What extra information you ask? To start with McFly considers these options in its ranking heuristics:

* The commands you typed before the command
* How often you run the command
* How recently you ran the command

It tracks all this in a SQLite database. But it doesn't stop there, it also weighs suggestions by:

* The commands exit status
* The directory you ran the command in
* If you have selected it in McFly before

Being suggested failed commands is a pet peeve of mine but I never even considered narrowing the choice based on the current directory and down ranking items that are never selected.

`McFly` uses a neural net to do its ranking and one possible downside is the lag in coming up with suggestion if your history is very large.  `McFly` is working on pruning history to address this.

I've only been using it for a couple days, so I'm not totally certain how great it is but the concept makes me pretty hopeful. This seems like a fruitful area - using extra information to customize towards real world usage.

<div class="notice--info">
**ℹ️ Install McFly **

McFly can be installed [several ways](https://github.com/cantino/mcfly/#installation). Here is brew: :

``` bash
brew tap cantino/mcfly
brew install mcfly
```
Then add hooks to your `.zshrc`, `bashrc` or equivalent:
``` bash
eval "$(mcfly init zsh)"
``` 
The binary emitting the init script is a nice touch. I found that `FZF` was interferring with the `CTRL-R` of McFly and had to comment out [this line](https://github.com/junegunn/fzf/blob/764316a53d0eb60b315f0bbcd513de58ed57a876/shell/key-bindings.zsh#L109) in the `FZF` init script to get McFly working.
</div>

## Better CD
`FZF` works nicely for some path completions but I didn't find it very useful for changing directories with `cd`: After typing `cd **TAB` from my home directory, it takes a while for `FZF` to build up the full list options to choose from. It was much faster to just use the ZSH completions of `cd TAB <choose a dir> TAB <choose a dir>` to navigate to a folder.  

However, many tools exist which attempt to improve upon `cd`. [`autojump`](https://github.com/wting/autojump), [`z`](https://github.com/rupa/z) and [`Fasd`](https://github.com/clvv/fasd) all track directory usage and give you a single key shortcut for changing to commonly accessed directories. [`r/commandline`](https://www.reddit.com/r/commandline/comments/4v5nlt/what_cd_tool_do_you_use_if_any_autojump_j_z_etc/) has a great discussion of these various `cd` replacements but the one that seems like it has the most momentum is `zoxide`. [zoxide](https://github.com/ajeetdsouza/zoxide) is a rewrite of z in Rust and promises improved speed. 

After you install it, you can use it just like `cd` (`z ~/path/foo/bar`) but you can also change directories based on ranked text matches of the path (`z bar` ~= `cd ~/path/foo/bar` ). Instead of needing to supply the full path to change locations, you just have to provide a unique substring of the path and `zoxide` will use its history of locations to get you where you want. 

For ease of adoption, I've choosen to just have `zoxide` replace `cd`, which is as simple as using the `--cmd` flag when you add the initialization shell code (`eval "$(zoxide init zsh --cmd cd)"`). 


<div class="notice--info">
**ℹ️ Install zoxide **

zoxide can be installed [several ways](https://github.com/ajeetdsouza/zoxide#step-1-install-zoxide). Here is brew: :

``` bash
brew install zoxide
```
Then add hooks to your `.zshrc`, `bashrc` or equivalent:
``` bash
eval "$(zoxide init zsh --cmd cd)"
``` 
</div>

## GitUpdate


## Other Tools
There are many other helpful command line tools. More than can be covered well in a single article. JQ, MITMProxy, Vale, Pandoc, and PSTree are some I use frequently. There is also a whole class of Rust rewrites of common POSIX tools that warrant an article of their own.  

Of course, [Earthly](https://earthly.dev/) itself is a command line tool and one I use constantly for gluing together various bits of development into repeated steps that I can call locally or on a build server. It has definitely become a standard part of how I do things at the command line. 

What less common command line tools do you use? If you have tool suggestions I'd love to hear them. You can find my twitter account and email below.