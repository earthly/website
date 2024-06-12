---
title: "chown: Changing File and Directory File in Linux"
toc: true
author: Thinus Swart

internal-links:
 - Linux
 - Directory Ownership
 - File Ownership
 - chown
 - Permissions
excerpt: |
    Learn how to change file and directory ownership in Linux using the `chown` command. This article explains the importance of ownership in Linux, how permissions work, and provides examples of using `chown` to change ownership.
last_modified_at: 2023-07-19
categories:
  - linux
---
**This article explains the basics of managing ownership in Linux. Earthly provides advanced build automation for CI/CD pipelines. [Learn more about Earthly](https://cloud.earthly.dev/login).**

In Linux, file, and directory ownership is a core aspect of the operating system's security and file management model. Each file and directory has an *owner* and a *group* assigned to it. The owner of a file or directory is the user who created it, and the group is a collection of users who share the same permissions for that file or directory.

The `chown` command, which stands for "change owner", has been the de facto tool in the Unix operating system for changing the owner of a file or directory. During the 1990s, as Linux was being developed, many Unix commands were ported over to the new operating system, including `chown`.

Understanding file and directory ownership is important for managing and securing a Linux system. Proper ownership ensures that only authorized users have access to sensitive files and directories, and can help prevent data breaches and security vulnerabilities.

In this article, software developers can learn everything they need to know about Linux file and folder ownership. This includes discussing different methods for changing ownership (including `chown`) and how this topic relates to file permissions.

Before you begin to use `chown`, you need to learn how to read and interpret Linux file ownership and permissions.

## How Linux Permissions Work

![How]({{site.images}}{{page.slug}}/how.png)\

The operating system grants file and directory owner's certain permissions. For files, the *read* permission allows the owner to view the contents of the file, the *write* permission allows them to modify the contents of the file, and the *execute* permission allows them to run the file as a program.

For directories, the *read* permission allows the owner to list the contents of the directory; the *write* permission allows them to add, remove, and rename files and directories within the directory; and the *execute* permission allows them to access the contents of the files in the directory.

Other (non-owner) users and groups may also have permission to read, write, or execute a specific file, depending on the permissions set on the file or directory.

Linux permissions can seem confusing at first, but there are a lot of resources that can [help you understand them better](https://www.redhat.com/sysadmin/linux-file-permissions-explained).

To see the permissions of any given file, you can use the `ls` command.

### Listing File and Directory Permissions

![File]({{site.images}}{{page.slug}}/file.png)\

`ls` is a command used on Linux operating systems for listing files and directories on any system.

On most modern Linux desktop systems, like [Ubuntu Desktop](https://ubuntu.com/desktop) or [Fedora](https://getfedora.org), you're typically given a standard user that you set up and name during the installation process. For example, here, the user is called `demo`:

~~~{.bash caption=">_"}
demo@localhost:~$ ls
docs  downloads  photos  todo.txt
~~~

The `ls` command lists all the files and directories in your user's home directory. However, this isn't very useful. Try adding the `-l` argument to our `ls` command like this:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l
total 16
drwxrwxr-x 2 demo demo 4096 Apr 12 22:23 docs
drwxrwxr-x 2 demo demo 4096 Apr 12 22:23 downloads
drwxrwxr-x 2 demo demo 4096 Apr 12 22:23 photos
-rw-rw-r-- 1 demo demo   39 Apr 12 22:24 todo.txt
~~~

Using the preceding code, you get a lot more information about each file and directory. The relevant parts of the output are broken down as follows:

* **`drwxrwxr-x`:** This section describes the permissions for the file or directory. The first character, `d`, indicates that this is a directory. The next nine characters are broken up into three groups of three characters each. The first three characters describe the permission level that the file owner currently has, the next three characters display the permission level that the assigned group has, and finally, the last three characters describe the permissions that everyone else has (in other words, a user who is not the file owner and/or does not belong to the assigned group).
* **`demo demo`:** The first instance of `demo` is the file owner, a user called `demo`; while the second instance is the assigned group, also called `demo`.
* **`4096`:** This indicates the size of the file in bytes or the size of the directory metadata in bytes.
* **`Apr 12 22:23`:** This shows us the last time that the file or directory was modified.
* **`docs`:** This is the name of the directory.

## Using `chown` to Change Owners

Once you get the hang of listing and reading the permissions of a file or directory, you can start experimenting with the `chown` command.

Take a look at an example of a `chown` command in the format `chown <newowner-username> <filename>`:

~~~{.bash caption=">_"}
chown notdemo todo.txt`
~~~

If your command executes successfully, then you've changed the owner of the `todo.txt` file, thanks to the robust way that Linux handles file ownership.

However, look at this next example:

~~~{.bash caption=">_"}
demo@localhost:~$ chown notdemo todo.txt
chown: changing ownership of 'todo.txt': Operation not permitted
~~~

You see `chown` typically requires administrative-level access to the system. While it may seem like an inconvenience, it's actually an intentional safeguard that prevents users from making unauthorized changes to someone else's files.

So whether you're installing a new software package or fixing permissions on a particular directory, it's extremely likely that you'll be running this command as the [root](https://tldp.org/LDP/lame/LAME/linux-admin-made-easy/root-account.html) user.

Try the `chown` command as the root user:

~~~{.bash caption=">_"}
demo@localhost:~$ sudo -i
root@localhost:~# chown notdemo /home/demo/todo.txt
root@localhost:~# exit
~~~

<div class="notice--info">
Your Linux configuration or distribution may have a different method for interacting with or becoming the `root` user. Consult with your specific online documentation on how to use the [`sudo`](https://tldp.org/LDP/GNU-Linux-Tools-Summary/html/c6239.htm) command properly.
</div>

Notice how you now need to specify the full path to the file. That's because the root user gets logged into its own home directory and not the home directory of the demo user. The `exit` command breaks you out of the root shell and back into your standard user shell.

Take a look and see whether your changes have taken hold:

~~~{.bash caption=">_"}
root@localhost:~$ ls -l
total 16
drwxrwxr-x 2 demo    demo 4096 Apr 12 22:23 docs
drwxrwxr-x 2 demo    demo 4096 Apr 12 22:23 downloads
drwxrwxr-x 2 demo    demo 4096 Apr 12 22:23 photos
-rw-rw-r-- 1 notdemo demo   39 Apr 12 22:24 todo.txt
~~~

The owner of the file is no longer `demo` and is now `notdemo`. But see if you can still read the file:

~~~{.bash caption=">_"}
root@localhost:~$ cat todo.txt 
* Feed the cat!
* Mow the lawn
* Chill
~~~

Yes! But why? It all comes down to read, write, and execute permissions.

### Managing Read, Write, and Execute Permissions

The `rwx` pattern shows us the permission level that the owner, group, and everyone else has. Take a look at the pattern for the `todo.txt` file:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l todo.txt 
-rw-rw-r-- 1 notdemo demo 39 Apr 12 22:24 todo.txt
~~~

The `-rw-rw-r--` string shows you that the file owner (`notdemo`) can read from and write to the file. The `demo` group has the same permissions. Everyone else can only read the file.

Test this by trying to add another task to the file using the append operator (`>>`):

~~~{.bash caption=">_"}
demo@localhost:~$ echo "* Sleep" >> todo.txt 
demo@localhost:~$ cat todo.txt 
* Feed the cat!
* Mow the lawn
* Chill
* Sleep
~~~

That worked, and for a good reason. You executed the `echo` command as the `demo` user, but the `demo` user still belongs to the `demo` group as well:

~~~{.bash caption=">_"}
demo@localhost:~$ cat /etc/passwd | grep ^demo
demo:x:1001:1001:,,,:/home/demo:/bin/bash

demo@localhost:~$ cat /etc/group | grep ^demo
demo:x:1001:
~~~

The `demo` user belongs to group ID `1001`, which is indeed the `demo` group. For argument's sake, change the group of the file to `notdemo` as well:

~~~{.bash caption=">_"}
demo@localhost:~$ sudo -i
root@localhost:~# chown notdemo:notdemo /home/demo/todo.txt
~~~

Notice how the first argument for the `chown` command changed slightly. It's using a `<username>:<groupname>` format to specify both the username and the group that the file now belongs to:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l
total 16
drwxrwxr-x 2 demo    demo    4096 Apr 12 22:23 docs
drwxrwxr-x 2 demo    demo    4096 Apr 12 22:23 downloads
drwxrwxr-x 2 demo    demo    4096 Apr 12 22:23 photos
-rw-rw-r-- 1 notdemo notdemo   47 Apr 12 23:14 todo.txt

demo@localhost:~$ echo "* Wake up" >> todo.txt 
-bash: todo.txt: Permission denied
~~~

Now the file cannot be modified by the `demo` user because they don't have owner- or group-level write permissions on the file. However, the `demo` user can still read the file:

~~~{.bash caption=">_"}
demo@localhost:~$ cat todo.txt 
* Feed the cat!
* Mow the lawn
* Chill
* Sleep
~~~

That's because the *everyone* part of the set permissions still allows read operations on the file.

Now that you've got the basics of `chown` down, take a look at some other arguments and examples.

### Changing Ownership of Multiple Files

To change the ownership of multiple files at once, you can include wildcard characters.

In the following example, you can see that your home directory contains three `.txt` files, all owned by the `demo` user and group:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l *.txt
-rw-rw-r-- 1 demo demo 0 Apr 12 23:29 today.txt
-rw-rw-r-- 1 demo demo 0 Apr 12 23:29 tomorrow.txt
-rw-rw-r-- 1 demo demo 0 Apr 12 23:29 yesterday.txt
~~~

As the `root` user, change the owner of all the files starting with `to*`:

~~~{.bash caption=">_"}
demo@localhost:~$ sudo -i
root@localhost:~# chown notdemo:notdemo /home/demo/to*.txt
root@localhost:~# exit
~~~

Now you can confirm that the file owner has been changed to `notdemo` for those specific files but not the others:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l *.txt
-rw-rw-r-- 1 notdemo notdemo 0 Apr 12 23:29 today.txt
-rw-rw-r-- 1 notdemo notdemo 0 Apr 12 23:29 tomorrow.txt
-rw-rw-r-- 1 demo    demo    0 Apr 12 23:29 yesterday.txt
~~~

### Recursively Changing All File Owners in a Directory and Its Subdirectories

In the following example, you have a `2023` directory containing some assignments you did in `Jan` and `Feb`, each in their own respective directories:

~~~{.bash caption=">_"}
demo@localhost:~$ ls
2023
demo@localhost:~$ ls -lR
.:
total 4
drwxrwxr-x 4 demo demo 4096 Apr 12 23:36 2023

./2023:
total 8
drwxrwxr-x 2 demo demo 4096 Apr 12 23:39 Feb
drwxrwxr-x 2 demo demo 4096 Apr 12 23:39 Jan

./2023/Feb:
total 4
-rw-rw-r-- 1 demo demo 28 Apr 12 23:39 feb_assignment.txt

./2023/Jan:
total 4
-rw-rw-r-- 1 demo demo 60 Apr 12 23:39 jan_assignment.txt
~~~

Recursively change the owner of all the files and directories in the `2023` directory:

~~~{.bash caption=">_"}
demo@localhost:~$ sudo -i
root@localhost:~# chown -R notdemo:notdemo /home/demo/2023
root@localhost:~# exit
~~~

Then take a look at the results again:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -lR
.:
total 4
drwxrwxr-x 4 notdemo notdemo 4096 Apr 12 23:36 2023

./2023:
total 8
drwxrwxr-x 2 notdemo notdemo 4096 Apr 12 23:39 Feb
drwxrwxr-x 2 notdemo notdemo 4096 Apr 12 23:39 Jan

./2023/Feb:
total 4
-rw-rw-r-- 1 notdemo notdemo 28 Apr 12 23:39 feb_assignment.txt

./2023/Jan:
total 4
-rw-rw-r-- 1 notdemo notdemo 60 Apr 12 23:39 jan_assignment.txt
~~~

As you can see, all the directories, subdirectories, and files in the subdirectories now have a different username and group assigned to them.

## Other Ownership and Permission-Related Commands

Here are a few brief examples of other commands that you might run into when managing file and directory permissions on a Linux file system:

### `chgrp`

[`chgrp`](https://linuxhint.com/chgrp-command-linux/) is very similar to `chown`, as it allows you to change only the group assigned to the file. Currently, the command isn't as useful as it once was because the newer `chown` syntax allows you to change groups as well by using the `<username>:<group>` format for the first parameter.

### `chmod`

The `chmod` command allows you to add or remove certain permissions to any file that already has a username and group defined. For example, you might have a file that needs to be able to be written to by everyone. Everyone can read the following file because the last three characters of the permissions string only have an `r` in that position:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l *txt
-rw-rw-r-- 1 demo demo 0 Apr 12 23:55 writehere.txt
~~~

But you can change that:

~~~{.bash caption=">_"}
demo@localhost:~$ sudo -i
root@localhost:~# chmod o+w /home/demo/writehere.txt
root@localhost:~# exit
~~~

Then go back and view the file permissions:

~~~{.bash caption=">_"}
demo@localhost:~$ ls -l *.txt
-rw-rw-rw- 1 demo demo 0 Apr 12 23:55 writehere.txt
~~~

Now you can see that the `w` flag has been set for everyone else. The `o` in the command means "other" or "everyone else". If you want to expand your knowledge of the `chmod` command, check out [these other examples](https://www.computerhope.com/unix/uchmod.htm).

### The Root User Has Special Permissions

![Permissions]({{site.images}}{{page.slug}}/permission.png)\

As you may have noticed, many of the permissions-related commands require you to execute the relevant commands as the root user. The root user on a Linux system is the account with the highest level of system privileges. It can perform any action on the system, including installing and removing software, modifying system files and configurations, and creating and deleting user accounts.

Because the root user has unrestricted access to the system, it's highly recommended to only use this account when absolutely necessary. For all other day-to-day activities, a normal user account should be utilized.

## Conclusion

In this quick guide, you've got the hang of using `ls`, `chown`, `chgrp`, and `chmod` to manage Linux file permissions and ownership. Sure, it can be tricky, but there are loads of resources to help you out, like official docs, online tutorials, and forums. Some cool places to start could be [Linux Documentation Project](https://tldp.org), [LinuxQuestions.org](https://www.linuxquestions.org), or the [Ubuntu Community Help Wiki](https://help.ubuntu.com/community/CommunityHelpWiki).

Now that you've mastered Linux permissions, why not level up your build automation game with [Earthly](https://cloud.earthly.dev/login)? It's a great tool to streamline your development process.

{% include_html cta/bottom-cta.html %}
