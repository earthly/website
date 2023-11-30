---
title: "Store VS Code `Settings.json` in Git"
categories:
  - Tutorials
toc: true
author: Adam
excerpt: |
    Learn how to store your VS Code settings in Git to easily manage and share your customizations. Keep all your settings in one place and avoid breaking anything when customizing your VS Code experience.
last_modified_at: 2023-07-19
---
**This article explains how to sync your VS Code settings effortlessly. Earthly improves your CI builds. [Learn how](https://cloud.earthly.dev/login).**

VS Code is very extensible and you can customize it in a thousand ways using many extensions.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/1110.png --alt {{ Tons of Extensions }} %}
<figcaption>Tons of Extensions</figcaption>
</div>

You can also customize keybindings and even the CSS used to [render VS Code itself](https://itnext.io/easy-enhancements-for-vs-codes-terminal-6dda2c22ee5c).

This is all great, but the more you customize the more likely you are to break something. So how to keep all these settings in one place? VS Code has a sync settings feature that can do just that, but for me the solution is always going to be git.

## `Settings.json` in `git`

First, create a new git repository. I'm creating mine in `/Users/adam/sandbox/vs-code-styles/`. Initialize it with 'git init' and add a readme.md you can use for documentation purposes.

Next, locate your settings.json file by opening it in VS Code (Ctrl-Shift-P or Command-Shift-P) and then use `copy path` to get its disk location. Repeat this same process for keybindings.json. (If you can't find it, its in the same folder.)

{% picture {{site.pimages}}{{page.slug}}/1440.png --alt {{ VS Code copy path }} %}
<figcaption>VS Code copy path</figcaption>

## Copy Over

In your terminal, simply copy your settings and keybindings files into your new settings repo. After committing them (`git add . && git commit -a -m "settings.json"`), remove the old copies. Next, symlink the new versions in their place. Make sure VS Code is closed during this process. Now, any changes you make to your settings will be saved in the repo, allowing you to commit or undo changes as needed.

Once you've got your settings optimized, you might want to consider streamlining your build process as well. Check out [Earthly](https://www.earthly.dev/) for efficient build automation. It could be the perfect complement to your newly optimized VS Code settings.

Here's where my [settings](https://github.com/adamgordonbell/vs-code-styles) live on GitHub.

{% include cta/cta1.html %}
