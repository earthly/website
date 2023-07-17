---
title: "Manage dotfiles from anywhere with Git"
categories:
  - Tutorials
toc: true
author: Talha Khalid

internal-links:
 - Dotfile
 - Git
 - Github
 - Gitlab
 - Bash
excerpt: |
    Learn how to manage your dotfiles using Git and make your environment configuration easier to maintain and synchronize across multiple machines. Say goodbye to the hassle of manually reinstalling programs and customizing settings every time you switch computers.
---
**We're [Earthly](https://earthly.dev/). We simplify software building using containerization. [Check it out](/).**

Have you ever found yourself in a situation where you had to format your computer and manually reinstall all the programs you were using? Or did you change machines and have to go to the page of each of the software you use and download and run the installer one by one? Or even customize some mouse/keyboard settings?

This is a bit of work for everyone, but it's even more work for devs. We have a series of environment configuration files, variables, binary configurations, and shells that need to be configured the way we want them to be so we can be as productive as possible!

Let's understand how dotfiles will solve this problem and how you will be much more productive when you start versioning them using Git.

## What Are Dotfiles?

Dotfiles is the name given to the set of hidden files used to store the state configuration or the preferences configuration of a tool.

The term "dotfiles" comes, like most things in computing, from the old Unix kernels that adopted the practice of adding the prefix`.` in front of the filename to [make](/blog/makefiles-on-windows) that file, by default, a hidden file, i.e., a file that is not shown in the listing for `ls.` For example, `/home/.hushlogin'it is a common file in Linux nowadays to remove the login message when accessing [SSH](/blog/encrypting-data-with-ssh-keys-and-golang).

As any Unix based system has a very strong relationship with files, since most modules and even devices or network interfaces are shown as files within the file system, they are highly important for software development.

Nowadays, the vast majority of tools use dotfiles to maintain configuration files:

- Bash:`.bashrc`
- Git: `.gitconfig`,`.gitexcludes`
- Vim:`.vimrc`

## The Problem With Dotfiles

![Problems]({{site.images}}{{page.slug}}/prob.jpg)\

You can save a copy of dotfiles on some online storage service like Dropbox. This is not a problem as long as you only save one file, but what about when you start saving multiple files? How to manage it from several programs, in several folders, and worse, how to restore it all later?

There are [several projects](https://dotfiles.github.io/utilities/) to solve the problem of how we can keep our dotfiles synchronized on machines with the same operating system. One solution is to put your dotfiles under version control.

If you use several machines, they may have specific configurations. It is therefore not desirable to synchronize all files. With its branching system, Git can help you overcome this problem. You can create a master branch containing files common to different systems and branches specific to each system. It is then possible to use a logical operator in the Bash configuration file to apply the correct files according to the machine's name, for example.

Git also allows to use submodules. This way, you can have repositories inside the repository, which gives you more flexibility and modularity to maintain the repository, including other people's repositories within our repo.

Git, therefore, seems perfectly adapted to our needs since it allows you to save, synchronize, and create specific branches.
  
_Note:_ _It is important to say that if your files contain sensitive data, like passwords, keys, etc., then you may need to manage them in a private repository or use tutorials like this one to make them encrypted._

## Managing Your Dotfiles

![Managing]({{site.images}}{{page.slug}}/mng.png)\

The idea of ​​managing configuration files using git and submodules is to [make](/blog/makefiles-on-windows) the configuration easier to segment. Being segmented makes it easier to maintain and find the configuration we are looking for. In our case, the structure is:

- Dotfiles calling repos
- Repo with app configuration as a submodule
- Plugins for the app as submodules

Using this structure, we only have files with a few lines that call the file that consolidates the configuration of the entire repo. For example, .bashrc:

~~~{.bash caption=">_"}
##!/bin/bash
## shellcheck disable=1090
source ~/.shell_config/bash/bashrc

~~~

The file named above takes care of loading:

- Alias
- Command settings
- Custom commands
- Environment Variables
- Prompt configuration

This can be done with all applications. Having a more segmented configuration makes it easier to find the specific configuration we are looking for. This also helps make it harder to break the configuration and easier to debug. Another benefit of this segmentation is the ease of reusing code if we use more than one terminal (bash, zsh, etc.) or want to migrate between them.

### And How Do We Do?

![How]({{site.images}}{{page.slug}}/how.png)\

The process is fairly simple. With git already installed, you can start the repository by executing:

`git init --bare $HOME/.cfg`

Before you can use it, you must make some configurations:

_Let's avoid loops in versioning_  `echo ".cfg" >> ~/.gitignore`

_Set up the alias temporarily to make it easier to work on the repo_  `alias gitdot='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'`

_Note:_ the alias can also be persisted in the .bashrc

_Hide files that are not being versioned_  `gitdot config --local status.showUntrackedFiles no`

Now you just have to push to move configuration files in the repository.

#### Exporting the Configuration With Dotfiles

Once the repository is created, you can clone it anywhere where you want it. For that, you must:

`git clone --bare --depth 1 --recurse-submodules --shallow-submodules url-repo $HOME/.cfg`

In this way, you can clone the repository in bare format with the submodules. Fetching only the latest commit from each repository. This allows you to save space and increase the download speed since you do not need the project's complete history in the local repository. Once you have recreated the repository, you must check it to recreate the files. This process must be done in several parts, considering:

- Configuration files may already exist in that path; you must back them up and move them
- If you use submodules, you have to start and update them
- You must apply the configuration

~~~{.bash caption=">_"}
alias gitdot='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
mkdir -p .config-backup && \
gitdot checkout 2>&1 | egrep "\s+\." | awk {'print $1'} | \
xargs -I{} mv {} .config-backup/{}
gitdot checkout
gitdot submodule init
gitdot submodule update
source .bashrc

~~~

_Note:_ _If the submodules also have submodules, the start and update process must be repeated._

## Difference Between Hard And Soft Links

![Difference]({{site.images}}{{page.slug}}/diff.png)\

After moving all the files to a structure that you are happy with in your repository, you can use the _hard links_ functionality of Unix-based systems so that you can create a connection between your original file and the location where the dotfile will exist.

The difference between _hard links_ and _soft links_ is the fact that _hard links_ will be a pointer to the file itself; that is, it is a different name for the same original file that is independent of any other system resource; it is as if you were talking about a file having multiple names.

This creates a great facility when you have to back up these files because hard links are direct pointers to the original file content, so if you change the hard link, let's change the original file, too, you can perform a test by doing the following:

~~~{.bash caption=">_"}
export temp=$(mktemp -d)
touch $temp/original
ln $temp/original ~/hardlink
~~~

Now you just have to edit the file present in `~/hardlink,` which is the link itself, and run `cat $temp/original` to see that the content is also present there.

If you want to delete the original file, you will also need to delete the link, so it's of no use running only `rm -rf $temp`; it's necessary to run `rm -rf ~/hardlink` too.

Soft links do not allow you to do this, as they are just files that point to other files. So for dotfiles, it is much better to have a hard link that allows you to directly edit a dotfile wherever it is, and those changes are reflected in your Git repository.

## Creating the Hard Link

![Creating]({{site.images}}{{page.slug}}/create.png)\

Now that you have the repository with the files, all that's left is to link them to their original locations.

For this, you will have to use the command `ln`; the syntax of this command is:

~~~{.bash caption=">_"}
ln <original file> <link location>
~~~

It is important to note that the link's location may need to be an absolute path; that is, it cannot be a path of type `../`or `~/` on some systems.

The command does not display any output if everything went well, so the way to identify it is by checking if the file is also present when executing a command `ls -la` in your destination directory.

 In the case of symlinks, when running a listing, the command output shows a path of type `file -> original file`.

### Conclusion
<!--sgpt-->
Keeping Dotfiles on platforms like [Github](/blog/ci-comparison) or [Gitlab](/blog/gitlab-ci) streamlines configuration syncing and makes setup and collaboration a breeze. Remember, _dotfile_ files aren't just for system admin geeks. They're great tools to fine-tune your dev environment and boost your productivity. 

Looking to further streamline your dev setup? Take a look at [Earthly](https://www.earthly.dev/), for your build automation needs! With Earthly, you can simplify your build configuration and ensure consistent builds across different environments. Let's get optimizing!

{% include_html cta/bottom-cta.html %}