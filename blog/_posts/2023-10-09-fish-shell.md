---
title: "Fish Shell"
categories:
  - Tutorials
toc: true
author: Anurag Kumar

internal-links:
 - fish shell
 - what is fish shell
 - introduction to fish shell
 - learning fish shell
 - features of fish shell
excerpt: |
    Fish Shell is a user-friendly and interactive shell that can be used for daily tasks and scripting. It offers features like auto suggestions, tab-based completion, syntax highlighting, setting aliases and abbreviations, customization options, and the ability to write custom functions.
last_modified_at: 2023-10-06
---
**This article introduces the Fish shell. Fish shell is pretty sweet. Guess what else is? Earthly. Earthly is a powerful tool to optimize your CI pipeline. [Check it out](/).**

What Is a Shell? Essentially, it's the place where you execute all your terminal commands. A shell goes beyond this simple definition – and you can create sub-shells to run your scripts and whatnot – but from a user perspective, I would like to keep it simple and think of it as a place where you invoke all your commands using your keyboard via text input.
There are many types of shells out there. Bash is one of the oldest, and it ships by default in most Linux distributions.
There are other shells as well, and these shells were developed after the bash shell. Some of the more common ones include:

1. `zsh`
2. `fish`
3. `nushell`

<div class="wide">
![Image Credits: Behind 'Hello World' on Linux notes]({{site.images}}{{page.slug}}/lgozFIn.png)
</div>

## Why Learn a New Shell?

One of the reasons I switched from bash to zsh and then later to fish is because I was feeling productive in fish shell and could do things faster. After using fish shell for a while, I didn't want to go back to bash aside from scripting. Zsh - along with oh-my-zsh - is an outstanding shell, but replicating the same features on a remote instance was challenging. So I switched to fish shell and haven't looked back.

The main advantage of fish shell is that it is easy to set up and use out of the box. The default behavior of fish shell is pretty good, and it's extensible too, so that you can customize it to your needs. You can customize how your shell looks very quickly.

## Introduction to Fish Shell

Fish shell is a friendly and interactive shell you can use for daily tasks. Besides being a shell, fish is a scripting language, which you can use to write and run scripts.

## Installation and Setup

For Debian-based distros, you can install fish shell by running the following command.

~~~{.bash caption=">_"}
sudo apt install fish
~~~

If you're using a different distro, you can find the [installation instructions](https://fishshell.com/docs/current/index.html#installation).

## Features of Fish Shell

Here are my favorite features, in order of impact they've had on my workflow.

### Auto Suggestions out of the Box

Fish provides you with very smart autosuggestion as you type in the terminal. You can also auto-complete the suggested command using the right arrow.

#### Tab-Based Completion

Tab-based completion is also very powerful with fish shell. For example, I was done with working with ssh-agent, and I wanted to kill the process. Now I had to find the PID associated with the `ssh-agent`. One way to do that would be to use `ps` command in conjunction with grep, but with fish you can just type the name of the process.

~~~{.bash caption=">_"}
kill ssh<tab>
~~~

<div class="wide">
![`process-kill`]({{site.images}}{{page.slug}}/BY2RGSi.gif)
</div>

#### Helpful Flag Options

Unix commands have a lot of flags, and it's good because they give you a lot of flexibility. With time, it becomes hard to recall all the flags of each command. Fish generates descriptive completion considering man-pages into account. This gives you an excellent descriptive message for each command.
For example, consider `git` command output.

~~~{.bash caption=">_"}
git <tab>
~~~

<div class="wide">
![`git`]({{site.images}}{{page.slug}}/7YHcrN4.gif)
</div>

### Fish Syntax Highlighting

Syntax highlighting will give you colorful syntax and sometimes indications if you're typing a wrong command or a correct command that doesn't exist in the system now.

<div class="wide">
![`highlight`]({{site.images}}{{page.slug}}/SAl1V3X.gif)
</div>

### Setting Aliases

Setting aliases in fish shell is the same as setting aliases in bash. You can set aliases in fish shell by using `alias` command.

~~~{.bash caption=">_"}
alias cat='bat -pP'
~~~

This is a simple alias that I use, and it gives me syntax highlighting when I use `cat` command.
While this sounds similar to bash, I really like that the alias command in fish shell provides you the flag to save the alias permanently without opening your `~/.config/fish/config.fish` file.
For example, You're on a remote instance and want to set a permanent alias for `kubectl` command. You can do that by running the following command.

~~~{.bash caption=">_"}
alias -s k kubectl
~~~

Under the hood, this command will create a function named `k`, which will be stored at `~/.config/fish/functions/k.fish`.

You can look at this function by invoking the following command.

~~~{.bash caption=">_"}
$ type k
~~~

~~~{.bash caption=">_"}
k is a function with definition
# Defined in /root/.config/fish/functions/k.fish @ line 1
function k --wraps=kubectl --description 'alias k kubectl'
  kubectl $argv;
end
~~~

If you have a longer command for which you want to create an alias, you can enclose it within brackets.

~~~{.bash caption=">_"}
alias -s kgp 'kubectl get pods'
~~~

Note that we are enclosing our command inside single quotes.

To view the git logs in a colorful manner, I use the following alias in my system.

~~~{.bash caption=">_"}
alias glo 'git log --pretty=format:"%Cred%h%Creset \
-%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset" \
--abbrev-commit'
~~~

<div class="wide">
![`alias`]({{site.images}}{{page.slug}}/D4imVif.gif)
</div>

### Setting Abbreviations

Abbreviations are unique to fish shell. To set abbreviations, you can use the following syntax. The recommended way is to add the abbreviations in your ~/.config/fish/config.fish file.

~~~{.bash caption=">_"}
abbr --add gst 'git status'
~~~

You can write a few keywords and hit space to complete the command. For example, you can write `gst` and hit space afterward. This will complete the command to `git status`.
This way, your history will look cleaner when you're traversing through your history to find any difficult command that you rarely execute sometimes.

Even if you don't put a space, the command will expand itself first, and then run.

<div class="wide">
![`abbr`]({{site.images}}{{page.slug}}/gVid01k.gif)
</div>

### Setting Variables

In fish, You might need to set environment variables at some point in time.
When you install go on a new system, you're required to set the GOPATH environment variable. You can set the same in fish using the following command.

~~~{.bash caption=">_"}
set -U GOPATH ~/go
~~~

You can use `-l` flag to set local environment variables, which will only persist till the life of the current shell.

~~~{.bash caption=">_"}
set -l VAR foo
~~~

### Private Mode

In fish shell, you can use `fish -P` or `fish --private` command to enter private mode. In private mode, your shell history will not be saved. You'll also not get autosuggestion for the command you've invoked previously.

I use this whenever I need to share my terminal with someone during a meeting.

Sometimes, it's also helpful when passing a token/secret to any command as an argument. For example, I'll run the following command in private mode because this involves passing a secret password as an argument.

~~~{.bash caption=">_"}
docker login -u randomuser -p randompassword
~~~

You can simply type `exit` on the terminal to move out of private mode.

## Customization

### Web-Based Customization

The easiest way to customize your fish shell if you want a GUI-based customization is web-based. Invoke `fish_config` or `fish_config browse` command via your terminal, and it'll open up a page in your default browser. You can use this page to customize your fish shell.

<div class="wide">
![`prompt_fish`]({{site.images}}{{page.slug}}/x5kFYoU.png)
</div>

GUI-based customization is good because it allows you to change colors and shows you how it looks on the console when modifying itself.

You can see that you can customize your color, prompt, functions, variables, history, and bindings.

### CLI-Based Customization

Fish support customization through CLI. You can use `fish_config` command to customize your fish shell.
To customize your prompt, you can use `fish_config prompt show` command to get all the prompts, and based on your choice, you can use `fish_config prompt save <prompt-name>` to save the prompt.
You can also choose and update themes with the `theme` sub-command. For example, to show all the themes, you can use `fish_config theme show`

<div class="wide">
![`fish_config_theme_show`]({{site.images}}{{page.slug}}/eC5AlEp.png)
</div>

## Functions in Fish

In every programming language, how you define functions are one of the most integral parts of the language. Fish is no different. You can write your own functions to use in your shell at the startup or by manually invoking them.

### Builtin Functions

These functions come built-in with fish shell. You can see the list of built-in functions by running `functions` command.

~~~{.bash caption=">_"}
$ functions 
# truncated output
N_, abbr, alias, bg, cat, cd, cdh, contains_seq, diff, dirh, dirs, \
disown, down-or-search, e, edit_command_buffer, export, fg, \
fish_add_path, fish_breakpoint_prompt, fish_clipboard_copy, \
fish_clipboard_paste, fish_command_not_found, fish_commandline_append,
~~~

### Writing Custom Functions

You can write custom function in fish shell. I wrote a custom function to create a new directory and cd into it.

~~~{.bash caption=">_"}
function mkcd 
    mkdir $argv && cd $argv
end
~~~

I often used this when I needed a temporary place to test something.

~~~{.bash caption=">_"}
mkcd some_dir_name
~~~

There's also an easy way to write this in fish shell. You can use the `funced` command to start writing a function and then save the function using the `funcsave` command.

Let's see how it works with an example. Let's write a function that prints the active connection that our system is connected to. Let's call the function `connection`

Let's start writing it.

~~~{.bash caption=">_"}
funced conn
~~~

This will open up an editor in your system.

> Note: You need to set the `EDITOR` environment variable or use the command `funced conn -e nvim` to open up the function in neovim.

You'll have the following template ready with you.

~~~{.bash caption=">_"}
function conn

end
~~~

Now you'll have to fill this template to complete the function. You can do a lot of this here, using text manipulation to get output or a simple command that will show you something. Let's use `nmcli` command to show all our device's active network connections.

~~~{.bash caption=">_"}
# Defined via `source`
function conn
    nmcli connection show --active
end
~~~

I've added a simple command showing us the active connection when you type `conn` on your terminal.
To test it out, save the file and close the editor. You can type `conn` in your terminal to test the above function.

~~~{.bash caption=">_"}
$ conn
NAME             UUID                                  TYPE      DEVICE
Aruba            4be15729-63ec-4e2a-83d7-63a9615da59b  wifi      wlp0s20f3
br-6066492249de  009488ec-ebd0-4990-8ddd-46cc2c079980  bridge    br-6066492249de
docker0          98af806f-defa-42c8-8dec-e811bd03a905  bridge    docker0
lo               773c166b-4785-49fb-8252-1dfa1e9c84f3  loopback  lo
~~~

This is the output of the `conn` command. Now, if you think your function needs more changes, you can go back to the function using `funced conn` command, edit the function, and test afterward until you get the desired result.

If you think the results are as expected, then you can use `funcsave conn` to save this function.

~~~{.bash caption=">_"}
$ funcsave conn
funcsave: wrote /home/k7/.config/fish/functions/conn.fish
~~~

This will write the function at the configuration directory of fish and now if you manage your dotfiles with git, you can version control this function and keep using on other devices too.

You can also see this function in the web-based view if you prefer to look at things in the browser.

<div class="wide">
![`browser_fn`]({{site.images}}{{page.slug}}/6Mc1M8E.png)
</div>

## Some Caveats of Using the Fish Shell

### `!!` & `!$`

In bash, you can use !! to repeat the last command and !$ to get the last argument of the previous command. For someone transitioning from bash to fish, the absence of this feature in fish can be disorienting.

You can use the following [function](https://fishshell.com/docs/current/cmds/abbr.html#examples) to make `!!` work in fish shell.

~~~{.bash caption=">_"}
function last_history_item
    echo $history[1]
end
abbr -a !! --position anywhere --function last_history_item
~~~

If you want the last argument of the previous command then you can use `Alt` combined with upper arrow to achieve that.

If you want to add `sudo` to you current command then you can use `Alt + S`

### Brace Expansion

In bash shell, we use `$(command)` and whatever is under this is replaced by the actual value of the command but in fish shell that is not supported. You must use the same thing without the `$` sign.

~~~{.bash caption=">_"}
$ sudo apt install linux-tools-$(uname -r)
fish: $(...) is not supported. In fish, please use '(uname)'.
sudo apt install linux-tools-$(uname -r)
~~~

Look at the unambiguous error message that fish shell gives you. It tells you that you can't use `$(...)` in fish shell. You have to use `'(...)'` instead.
Let's try to run the same command with `'(...)'` instead of `$(...)`.

~~~{.bash caption=">_"}
$ sudo apt install linux-tools-(uname -r)
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following additional packages will be installed:
  linux-aws-tools-5.15.0-1028
The following NEW packages will be installed:
  linux-aws-tools-5.15.0-1028 linux-tools-5.15.0-1028-aws
0 upgraded, 2 newly installed, 0 to remove and 70 not upgraded.
Need to get 7645 kB of archives.
After this operation, 25.7 MB of additional disk space will be used.
Do you want to continue? [Y/n]
~~~

So, this is another thing you should remember while using fish shells.

### `bash`

Bash is not going anywhere. I've not seen a single instance where fish or any other shell except bash being used in CI-CD pipelines. So if you are working in a team where you have to work with bash scripts, you should be aware of the differences between bash and fish. I write scripts in bash. You can still write scripts that you'll consume yourself in fish, but if you're contributing to an open-source project or working with a team, chances are some of the team-members or community might not have used fish shell, and you should prefer bash over fish.

## Miscellaneous

### Exporting Variables

Above, we talked about exporting variables with `-x`, but fish also supports `export` syntax to be compatible with bash. To set you EDITOR variable to nvim, you can also use the bash syntax.

~~~{.bash caption=">_"}
export EDITOR=nvim
~~~

from an implementation perspective, it used [set](https://github.com/fish-shell/fish-shell/blob/7534572d9953fa855ad75ad52502d6fec2014e24/share/functions/export.fish) under the hood to export variables.

#### `fish_add_path`

This is yet another useful function that will help in updating your `PATH`
for example, say you installed Go programming language on your system, and to add go bin directory to the path, you can use the following:

~~~{.bash caption=">_"}
fish_add_path -U ~/go/bin
~~~

#### `vared`

`vared` stands for variable edit. Let's set a variable using `set` command. For example, `set -x EDITOR code`. Now let's say you want to switch your EDITOR to `nvim` you can invoke the `vared EDITOR` command here. It'll open up an interactive EDITOR where you can update the value.

~~~{.bash caption=">_"}
$ vared EDITOR
EDITOR
> code
~~~

You can update the value from `code` to `nvim`

<div class="wide">
![`vared`]({{site.images}}{{page.slug}}/fZI1yoO.gif)
</div>

#### `cdh`

`cdh` is very handy for moving to directories you've recently visited. It'll open up an interactive menu and ask you to choose the directory you want to enter.

<div class="wide">
![`fish_cdh`]({{site.images}}{{page.slug}}/uYksSJk.png)
</div>

You can then select the directory from the options and hit enter to go into that directory.

## Conclusion

Fish is an outstanding shell if you work a lot in your terminal and care about productivity.
If you do a lot of work in the command line, I'm sure that fish will help you be more productive. I'm not saying that this is the best shell out there, but it definitely has some great features.

{% include_html cta/bottom-cta.html %}
