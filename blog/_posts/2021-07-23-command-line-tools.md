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

## Fortune
Alright, this one isn't really that useful. but I'm going to use this for fun in this article

## BRoot
I'm not sure how I came across BRoot, but its pretty handy. If are in a small directory structure and want to see the lay of the land `tree` is great.

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
However if the directory is large `tree` becomes much less useful: you only see the last screen full of information as files scroll past you:
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

## Funky
If you live in the terminal and you want to (use UNIX as an IDE)[https://blog.sanctum.geek.nz/unix-as-ide-files/] then its helpful to have your terminal change based on the currect directory. There are many ways to do this.  [`DirEnv`](https://direnv.net/) loads and unload `.env` files as you enter directories.  [`smartcd`](https://github.com/cxreg/smartcd) is similar it lets you run a shell script as you enter and leave each directory, which can be used to start and stop services, change the prompt or really anything.  

However, my favorite shell customizing tool is the strangely named [`funky`](https://github.com/bbugyi200/funky), which "takes shell functions to the next level by making them easier to define, more flexible, and more interactive."

The way `funky` works is simple, as you enter a directory `funky` looks for a `.funky` file which contains a list of bash functions. It loads those and when you leave it unloads them.

This means when I'm in the directory for this Jekyll blog I have aliases loaded for creating a new post, linting my markdown and so on. I can list these by typing `funky`

```
$ funky
lint() { markdownlint --fix "./_posts/*.md"; }
new-post() {  cat ./blog/_posts/2029-01-01-checklist.md > ./blog/_posts/$(date -v +7d +"%Y-%m-%d")-$1.md }
```
`funky` can do more than this. It has nice features for interactively adding and editing functions and you can also registry global functions. What I like though it just being able to quickly give a command, in a specific context, a short alias.

## Fuzzy Finder (FZF)
When asked people for recommendations for command line tools they found useful this one came up quite a bit. [FZF](https://github.com/junegunn/fzf) is a command line fuzzy finder. It's fast and it interactively lets you filter options down based on a fuzzy keyword match in many places in your commandlining.

If you install the included shortcuts (`/usr/local/opt/fzf/install`), you can use `**` anywhere and get an interactive fuzzy finder to narrow down to the desired path. It's really nice. FZF also makes searching your `history` much faster. 
There are a number of other users and Alexey Samoshkin's [video](https://www.youtube.com/watch?v=qgG5Jhi_Els) is an excellent tutorial on it.

## McFly
`FZF` is great for filtering files in a command like `vim **` but for commad line completetion there is actually more information available then just a raw history file and [`McFly`](https://github.com/cantino/mcfly/) attempts to use this extra information provide more relevant results.

What extra information you ask? To start with McFly considers these options when deciding what to show you:
* The commands you typed before the command
* How often you run the command
* How recently you ran the command

It does this by tracking these in a specific SQLite database. But it doesn't stop there, it also weighs its suggestions by:
* The commands exit status
* The directory you ran the command in
* If you have selected it in McFly before

These three are a game changer. Being suggested previsouly failed commands is a pet pevve of mine but I never even considered narrowing the choice based on the current directory and down ranking items that are never selected.

`McFly` uses a neural net to do its ranking and one possible downside is the lag in coming up with suggestion if your history is very large.  `McFly` is working on pruning history to allieveate this though.

I've only been using it for a couple days, so I'm not totally certain how great it is but the concept makes me pretty hopeful. This seems like a fruitful area for using the techniques of machine learning. 




 here are tools that 
- I'm not sure about the name here, but funky is really nice.
- if gives you a zsh aliases that are specific to a path
- this way I can have simple aliases, to create a new blog post

## Rename
 2423  rename s/markdown/md/ *.markdown
 2807  rename -n "s/action.jpg/action.png/ **/action.jpg
 2808  rename -n "s/action.jpg/action.png/" **/action.jpg
 2809  rename -n "s/action.jpg/action.png/" action.jpg

## Better CD
`FZF` works nicely for some path completions but I didn't find it very useful for changing directories with `cd`: After typing `cd **TAB` from my home directory, it takes a while for `FZF` to build up the full list options to choose from. It was actually much faster to just use the ZSH completions of `cd TAB <choose a dir> TAB <choose a dir>` to navigate to a folder.  

However, many tools suggest better ways to navigate then traditional CD. [autojump], [z] and [Fasd](https://github.com/clvv/fasd) all track directory usage and give you a single key shortcut for changing to a commoning access directory.  [zoxide](https://github.com/ajeetdsouza/zoxide) is a rewrite of z in Rust and promises blaizng speed. 



- zoxide
https://github.com/ajeetdsouza/zoxide
- Autojump
https://github.com/wting/autojump
- fasd 
https://github.com/clvv/fasd
- reddit questions:
https://www.reddit.com/r/commandline/comments/94ivmk/z_autojump_or_fasd/



https://ctop.sh/
dstat





FZF
https://www.youtube.com/watch?v=qgG5Jhi_Els

## The replacements

> Freemasen  12 minutes ago
> I have not, though I do use ripgrep over grep , bat over cat and fd  over find

## RipGrep (rg)
etc


## Others
## Mitmproxy
## pstree
- used in this post about buildkit
## Sox 
- this one I use for my podcast all the time. This is a utility knife for audio. That probably needs its own 
## Vale
## Earthly
## Pandoc
## JQ

 
## 

## Resources
- https://stackify.com/top-command-line-tools/
- https://opensource.com/article/20/6/modern-linux-command-line-tools
- https://www.tecmint.com/cool-linux-commandline-tools-for-terminal/


## More to look into 
https://github.com/nikitavoloboev/gitupdate
https://github.com/cantino/mcfly
