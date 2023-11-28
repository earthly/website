---
title: "Linux Security Modules"
categories:
  - Tutorials
toc: true
author: Anurag Kumar
editor: Mustapha Ahmad Ayodeji

internal-links:
 - security modules
 - linux security modules
 - linus system security
excerpt: |
    This blog post discusses Linux Security Modules (LSMs) and how they can be used to enhance the security of Linux systems. It specifically focuses on AppArmor, one of the popular LSMs, and provides examples of creating profiles to restrict file and network access.
last_modified_at: 2023-10-06
---
**Explore the ins and outs of Linux Security Modules in this article. If you advocate for tools like AppArmor, Earthly can integrate seamlessly into your secure CI pipelines. [Discover how](/).**

Linux is used by millions of people around the world. It is the most popular operating system if measured by active devices. It is used in almost every industry and is used in almost every type of device. With this wide usage of Linux, comes the responsibility of keeping the system secure. In this blog, We will be talking about the Linux Security Module and how we can use it to secure our system.

## What are Linux Security Modules (LSMs)?

Linux security modules are [kernel modules](<https://linux-kernel-labs.github.io/refs/heads/master/labs/kernel_modules.html#:~:text=A%20kernel%20module%20(or%20loadable,the%20form%20of%20kernel%20modules>) that provide a framework for implementing mandatory access control (more on this soon) on various resources inside our Linux system. They allow us to configure fine-grained access control to files, network interfaces, etc.

## History and Evolution of LSMs

![History]({{site.images}}{{page.slug}}/history.png)\

Linux security module (LSM) was added in the kernel in [version](https://en.wikipedia.org/wiki/Linux_Security_Modules#History) 2.6. LSM is a standard and it has different implementations. One of the first implementations was [SElinux](https://selinuxproject.org/) which was developed by NSA and later other implementations were also developed. Other notable implementations include [AppArmor](https://apparmor.net/), [smack](https://docs.kernel.org/admin-guide/LSM/Smack.html), etc. In this article, we will talk about `AppArmor`.

## Why Do We Need LSMs?

We already have granular control in Linux via [file permissions, user permissions, and group permissions](https://www.redhat.com/sysadmin/manage-permissions), why do we need LSMs?
Linux security modules are a way to make our system more secure by adding an extra layer of security. It comes into the picture when we want to have very specific control over the resources and kernel objects that one can access.

In the next section, we will explore these different access control mechanisms in Linux.

### DAC and MAC

There are two different access control mechanisms used in Linux for controlling access to resources such as files, directories, devices, and system operations. They are the Discretionary Access Control (DAC) and Mandatory Access Control (MAC).

DAC permissions are standard Linux permissions that we use and encounter daily. The DAC permissions are the property of the files and directories in Linux. These permissions are set by the owner of the file or the corresponding directory. DAC permissions cover permissions like read, write, and execute permissions. The DAC permissions allow anyone to read, write, or execute the file based on the permission assigned to them as a user or to the group they belong to.

Here's an image illustrating DAC permissions:

<div class="wide">
![Image link]({{site.images}}{{page.slug}}/PkhTj9m.png)\
</div>

In the example above, the owner can read and write the file (`rw-`), the group can read the file (`r--`), and others can also read the file (`r--`).

In the case of MAC permissions, the permissions are not property of the file, they are attributes or settings that are configured and managed by the system administrator. These permissions are not inherently associated with the file itself, but rather they are defined at the system level and govern the access rights and restrictions for various resources, including files, directories, devices, and system operations. The implementation of MAC permissions includes SELinux, AppArmor, etc. With the help of the MAC policy, even if the user has permission to access the file or other resources, the system administrator can restrict the accessibility of the resource.

Please note that DAC checks come first in the order of access control and after DAC checks are successful only then, MAC checks are executed.

## AppArmor

AppArmor is one of the most popular LSMs that is being used in Linux. It provides mandatory access control and restricts the capabilities of individual applications and processes. It's primarily used in Debian-based systems. It was designed to enforce MAC policies in Linux-based systems. It ships default with Ubuntu, openSUSE, and other Debian-based distributions. Apparmor gives us a lot of flexibility when it comes to writing profiles.

The fundamental unit of AppArmor is profiles. Think of profiles as a contract that we write in a high level [domain-specific language(DSL)](https://www.jetbrains.com/mps/concepts/domain-specific-languages/). [Profiles](https://gitlab.com/apparmor/apparmor/-/wikis/Profiles) are the means of communication between what we want to enforce and AppArmor. These profiles serve as sets of instructions that define the security policies for specific resources. Once created, these profiles are loaded into the kernel. The kernel then uses these profiles to enforce the security policies.

### Writing AppArmor Profiles

We need to understand the AppArmors's DSL syntax to write AppArmors's profiles. However, there are tools like [`aa-genprof`](https://manpages.ubuntu.com/manpages/xenial/man8/aa-genprof.8.html) that allow us to generate these profiles instead of writing them from scratch. In the next section, we will learn about generating boilerplate profiles with `aa-genprof`, and then we will write and enforce those profiles on a Linux system.

#### Using `aa-genprof` To Generate Apparmor Profiles

The AppArmor community provides a bunch of utility tools that are quite helpful when it comes to writing our custom AppArmor profiles. We can leverage these tools instead of writing from scratch. The `aa-genprof` tool is part of the `apparnor-util` package that is used to generate an AppArmor profile.

The `apparmor-utils` is a collection of binaries that will help us write, list, and validate profiles. It will assist us when operating Apparmor on our system.

To understand how to generate the profile, let's use the following example.

> Note: As mentioned earlier, AppArmor is mostly used in Debian-based systems, so for illustrative purposes, this tutorial will use the Ubuntu 22.04.

In this example, we will install a tool called [`bat`](https://github.com/sharkdp/bat). After installing `bat`, we will install the `apparmor-utils` and we will generate an AppArmor profile for the `bat` command using the `aa-genprof` command. The profile will deny the `bat` command access to the files in `/etc/group` directory.

To install the `bat` command, we can pick the binary for our system from the [GitHub releases page](https://github.com/sharkdp/bat/releases/tag/v0.23.0):

~~~{.bash caption=">_"}

curl -LO https://github.com/sharkdp/bat/releases/download/v0.23.0/bat_0.23.0_amd64.deb
~~~

After installing it, we will have to unpack it on our system:

~~~{.bash caption=">_"}
sudo dpkg -i bat_0.23.0_amd64.deb
~~~

Output:

~~~{ caption="Output"}
[sudo] password for k7:
(Reading database ... 179774 files and directories currently installed.)
Preparing to unpack bat_0.23.0_amd64.deb ...
Unpacking bat (0.23.0) over (0.22.1) ...
Setting up bat (0.23.0) ...
Processing triggers for man-db (2.10.2-1) ...
~~~

Next, we need to install the `apparmor-utils` that provides the `aa-genprof`:

~~~{.bash caption=">_"}
sudo apt update
sudo apt install apparmor-utils
~~~

Once installed, we can use the [`aa-enabled`](https://manpages.ubuntu.com/manpages/focal/en/man1/aa-enabled.1.html) command to confirm that the AppArmor software is enabled. The command will output `Yes` if it is enabled.  

~~~{.bash caption=">_"}
$ sudo aa-enabled
Yes
~~~

Next, we will generate a profile with the `aa-genprof` command for the `bat` command that we installed earlier. The profile will restrict the `bats`'s command access to the files in the `etc/group` directory *i.e.*, users will not be able to use the command on the, etc/group files irrespective of the type of permission that the user has).  

Invoke the command below to generate the profile for the bat binary:

~~~{.bash caption=">_"}
$ sudo aa-genprof /usr/bin/bat
~~~

The command above will ask us to select an option whether to scan the application activity or finish the profile with a baseline profile:

~~~{ caption="Output"}
Please start the application to be profiled in
another window and exercise its functionality now.

Once completed, select the "Scan" option below in 
order to scan the system logs for AppArmor events. 

For each AppArmor event, we will be given the 
opportunity to choose whether the access should be 
allowed or denied.

[(S)can system log for AppArmor events] / (F)inish
~~~

Input F for noninteractive mode.

In the above step, we've generated an AppArmor profile. The profile that was created will be in the `/etc/apparmor.d` directory in the  `usr.bin.bat` file. Let's check the content of this file:

~~~{.bash caption=">_"}
$ sudo cat /etc/apparmor.d/usr.bin.bat 
~~~

Output:

~~~{ caption="Output"}
# Last Modified: Fri May  5 20:06:38 2023
abi <abi/3.0>,

include <tunables/global>

/usr/bin/bat {
  include <abstractions/base>

  /usr/bin/bat mr,

}
~~~

Please note that on its own the profile does not have any effect, we will add the configuration to deny the `bat` command to read the /etc/group file by editing this profile as shown below:

~~~{.bash caption=">_"}
deny /etc/group rw,
~~~

Here's an image illustrating the profile the whole profile:

<div class="wide">
![image]({{site.images}}{{page.slug}}/gMNtdRe.png)\
</div>

We will be explaining the content of this profile in detail in the upcoming section.

We can check whether the profile is enforced or not by running `sudo aa-status`:

~~~{.bash caption=">_"}
$ sudo aa-status
# truncated output
34 profiles are in enforce mode.
   /snap/snapd/17883/usr/lib/snapd/snap-confine
   /snap/snapd/17883/usr/lib/snapd/snap-confine//mount-namespace-capture-helper
   /snap/snapd/18357/usr/lib/snapd/snap-confine
   /snap/snapd/18357/usr/lib/snapd/snap-confine//mount-namespace-capture-helper
   /usr/bin/bat
~~~

Right now, when we execute the bat command on the /etc/group files, we will get a permission denied error which indicates that the profile is enforced:

~~~{.bash caption=">_"}
$ bat /etc/group
~~~

Output:

~~~{ caption="Output"}
[bat error]: '/etc/group': Permission denied (os error 13)
~~~

We are unable to read the file even though we have read access to the file as a user:

~~~{.bash caption=">_"}
$ ls -la /etc/group
~~~

Output:

~~~{ caption="Output"}
-rw-r--r-- 1 root root 895 Nov 21 20:48 /etc/group
~~~

We'll be able to read the content of the file if we use any other command (like `cat`, `head`, `tail` etc):

~~~{.bash caption=">_"}
$ head /etc/group
~~~

Output:

~~~{ caption="Output"}
# truncated output 
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:
adm:x:4:syslog,ubuntu
~~~

### Understanding the Content of the Profile

Profiles in AppArmor are a set of rules that restrict what an application or a process can do on a Linux system.

Let's consider the profile that we created earlier for the `bat` command:

~~~{.bash caption=">_"}
# Last Modified: Fri May  5 20:06:38 2023
abi <abi/3.0>,

include <tunables/global>

/usr/bin/bat {
  include <abstractions/base>

  /usr/bin/bat mr,
deny /etc/group rw,

}
~~~

The first line is a comment that tells us when this profile was last modified:

~~~{.bash caption=">_"}
# Last Modified: Fri May  5 20:06:38 2023
~~~

After this, we include the `abi` file:

~~~{.bash caption=">_"}
abi <abi/3.0>,
~~~

This is a file that contains the version of the AppArmor profile. This is used by the Apparmor kernel module to check the version of the profile.

~~~{.bash caption=">_"}
include <tunables/global>
~~~

The file also includes the `tunables/global` file. This file contains the global tunables that are used by the AppArmor kernel module to adjust the level of enforcement. However, from the policy author's perspective, it doesn't matter much as it's auto-generated.

~~~{.bash caption=">_"}
/usr/bin/bat {
  include <abstractions/base>

  /usr/bin/bat mr,
deny /etc/group rw,
~~~

After this, is the main part of the profile. This includes the definition of the application on which we want to apply the AppArmor profile. In our case, we want to apply the apparmor profile on the `/usr/bin/bat` binary.

We have used the `rw` directive which indicates that we are denying read and write file permissions. There's more granular control that we can have on file via LSM. we can read more about other file permissions on AppArmor [wiki](https://gitlab.com/apparmor/apparmor/-/wikis/QuickProfileLanguage#file-permissions)

### Network-Related Profile

Now let's take another example where we will attempt to write a profile to block the network. Let's try to block the network access for the `[wget](https://www.gnu.org/software/wget/)` command that is used to install binaries from the Internet.

To begin, we will use `aa-genprof` command to generate the profile for the `wget` command:

~~~{.bash caption=">_"}
sudo aa-genprof $(which wget)
~~~

The command above will prompt us whether to scan the application activity or finish the profile with a baseline profile as shown earlier:

~~~{.bash caption=">_"}
Please start the application to be profiled in
another window and exercise its functionality now.

Once completed, select the "Scan" option below in 
order to scan the system logs for AppArmor events. 

For each AppArmor event, we will be given the 
opportunity to choose whether the access should be 
allowed or denied.

[(S)can system log for AppArmor events] / (F)inish
~~~

This time around, we want to proceed with an interactive prompt, so we will open up another terminal as indicated in the instruction above and invoke the `wget` command:

~~~{.bash caption=">_"}

$ wget https://github.com/sharkdp/bat/releases/download/v0.23.0/bat_0.23.0_amd64.deb
# truncated output
Length: 2285756 (2.2M) [application/octet-stream]
Saving to: 'bat_0.23.0_amd64.deb'

bat_0.23.0_amd64.deb             
100%[============================>]   2.18M  --.-KB/s    in 0.07s   

2023-05-05 19:12:02 (30.5 MB/s) - 'bat_0.23.0_amd64.deb' 
saved [2285756/2285756]
~~~

We downloaded the `bat` binary using the `wget` command. Now let's go back to the terminal where we were generating the profile using the `aa-genprof` command. If we type `S` which is short for scan then we'll be asked to allow or deny a specific file:

~~~{.bash caption=">_"}
[(S)can system log for AppArmor events] / (F)inish
Reading log entries from /var/log/syslog.
Complain-mode changes:

Profile:  /usr/bin/wget
Path:     /etc/wgetrc
New Mode: r
Severity: unknown

 [1 - /etc/wgetrc r,]
(A)llow / [(D)eny] / (I)gnore / (G)lob / Glob with (E)xtension 
/ (N)ew / Audi(t) / Abo(r)t / (F)inish
Adding deny /etc/wgetrc r, to profile.
~~~

We'll deny this and AppArmor will write this path to the profile that it's generating. It will again ask us for a bunch of other files. we can deny all of them and then we'll be asked to save the profile. When we finish the action we'll see the following message:

~~~{.bash caption=">_"}
= Changed Local Profiles =

The following local profiles were changed. 
Would we like to save them?

 [1 - /usr/bin/wget]
(S)ave Changes / Save Selec(t)ed Profile / [(V)iew Changes] 
/ View Changes b/w (C)lean profiles / Abo(r)t
~~~

Now that the profile is ready we can view the profile by typing `V` and then we can save the profile by typing `S`.

Let's check the profile that was generated:

~~~{.bash caption=">_"}
$ sudo cat /etc/apparmor.d/usr.bin.wget
# Last Modified: Fri May  5 19:14:38 2023
abi <abi/3.0>,

include <tunables/global>

/usr/bin/wget {
  include <abstractions/base>

  deny /etc/host.conf r,
  deny /etc/hosts r,
  deny /etc/nsswitch.conf r,
  deny /etc/wgetrc r,
  deny /run/systemd/resolve/stub-resolv.conf r,
  deny owner /home/*/.wget-hsts rwk,

  /usr/bin/wget mr,

}
~~~

In essence, this AppArmor profile restricts the `wget` command from reading various system configuration files and limits write access to the `.wget-hsts` file in user home directories. These files are typically necessary for its normal operation.

Now let's try to download the `bat` command binaries again:

~~~{.bash caption=">_"}

$ wget https://github.com/sharkdp/bat/releases/download/v0.23.0/bat_0.23.0_amd64.deb
Failed to Fopen file /etc/wgetrc
wget: Cannot read /etc/wgetrc (Permission denied).
Failed to Fopen file /home/cloud_user/.wget-hsts
ERROR: could not open HSTS store at '/home/cloud_user/.wget-hsts'. HSTS will be disabled.
--2023-05-05 19:37:29--  https://github.com/sharkdp/bat/releases/download/v0.23.0/bat_0.23.0_amd64.deb
Resolving github.com (github.com)... failed: Temporary failure in name resolution.
wget: unable to resolve host address 'github.com'
~~~

You can see that the `wget` command is failing because we have denied its access to the files that are required for its normal operations.

Once we're done experimenting with the AppArmor profiles we can use the `apparmor_parser --remove <path-of-the-profile>` to remove the profile from the system. We can also use the short form `-R` instead of  `--remove`.

Please note that the profile will still be there in the `/etc/apparmor.d` directory but it's not loaded hence it's not effective. To verify this, we can use the `aa-status` command.

~~~{.bash caption=">_"}
$ sudo apparmor_parser --remove /etc/apparmor.d/usr.bin.wget
$ sudo aa-status | grep wget
~~~

Since we didn't get any output from the above commence it means that the profile is not loaded.

## AppArmor Modes

![Modes]({{site.images}}{{page.slug}}/modes.png)\

There are two modes when it comes AppArmor:

* Enforce mode
In enforce mode, AppArmor profiles are loaded into the kernel and the kernel enforces the security policies. In this mode, the kernel will not allow anyone to access the resources that are denied by the AppArmor  profiles. If we try to access the resource then we'll get an error.

* Complain mode
In complain mode, the profiles are not enforced, but if an application or program violates any rule, its activity will be logged in the system logs. This is a good way to test our profiles before we put them into enforce mode.

### How to  Change the Modes of AppArmor Profiles

If we have a profile that is in enforce mode, and we want to change it to complain mode, we can do that by using the `aa-complain` command.

Let's see how it works:

~~~{.bash caption=">_"}
$ sudo aa-complain /etc/apparmor.d/usr.bin.bat 
Setting /etc/apparmor.d/usr.bin.bat to complain mode.
~~~

Now if we look at the profile, we'll notice there's a `complain` flag next to the `/usr/bin/bat` program:

~~~{.bash caption=">_"}
# Last Modified: Fri May  5 20:06:38 2023
abi <abi/3.0>,

include <tunables/global>

/usr/bin/bat flags=(complain) {
  include <abstractions/base>
  
  deny /etc/group rw,
  /usr/bin/bat mr,

}
~~~

Similarly, we can use `aa-enforce` to change the mode from complain mode to enforce mode.

Here's a high-level syntax of `aa-enforce` command:

~~~{.bash caption=">_"}
$ sudo aa-enforce <path-of-the-profile>
~~~

In the above examples, we have dealt with file paths and network access and restricted the permissions using AppArmor. Apart from this, AppArmor also supports other options like mount, capabilities and rlimits that we can include in the profile.

### Some Limitations of AppArmor

AppArmor is a great tool to secure our system, but it has some limitations. Some of the limitations are as follows:

* AppArmor employs the potent `SYS_ADMIN` capability to load profiles into the kernel through `apparmor_parser`. However, this capability is powerful and versatile, posing a security risk. Unauthorized access to this capability could result in significant damage to our system. In containerized environments, it's advisable to exercise caution and limit its use.

* AppArmor uses its domain-specificific language to write profiles, and this can be a little hard to understand when we start understanding/writing profiles.

### Conclusion

In this blog, we have talked about Linux security modules and how they can be used to secure our system. We have also talked about AppArmor which is one of the most popular LSMs that is being used in Linux. We looked at two examples of network andand file-based AppArmor profiles. In addition to that, we listed some of the limitations of AppArmor.

{% include_html cta/bottom-cta.html %}