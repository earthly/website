---
title: "Store VS Code `Settings.json` in Git"
categories:
  - Tutorials
toc: true
author: Adam
excerpt: |
    Learn how to store your VS Code settings in Git to easily manage and share your customizations. Keep all your settings in one place and avoid breaking anything when customizing your VS Code experience.
---
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

In your terminal, copy these files into your new settings repo:

~~~
> cp /Users/adam/Library/Application Support/Code/User/settings.json ↩
  /Users/adam/sandbox/vs-code-styles/settings.json
> cp /Users/adam/Library/Application Support/Code/User/keybindings.json ↩
  /Users/adam/sandbox/vs-code-styles/keybindings.json
~~~

After committing these (`git add . && git commit -a -m "settings.json"`) remove the old copies.

~~~
> rm  /Users/adam/Library/Application Support/Code/User/settings.json
> rm  /Users/adam/Library/Application Support/Code/User/keybindings.json
~~~

Then symlink the new versions into place.

~~~
> ln -s /Users/adam/sandbox/vs-code-styles/keybindings.json ↩
      /Users/adam/Library/Application Support/Code/User/keybindings.json
> ln -s /Users/adam/sandbox/vs-code-styles/settings.json ↩
      /Users/adam/Library/Application Support/Code/User/settings.json
~~~

If you have any issues with that, ensure that VS Code (all copies) are closed. After this change any settings changes you make are written to the repo and you can commit and or revert the changes as needed.

Now my settings are stored on [GitHub](https://github.com/adamgordonbell/vs-code-styles).

{% include cta/cta1.html %}
