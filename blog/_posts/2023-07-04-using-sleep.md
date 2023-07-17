---
title: "Shell Scripting with sleep: Using Delays Strategically"
categories:
  - Tutorials
toc: true
author: James Konik

internal-links:
 - Shell
 - Scripting
 - sleep
 - Command
 - Delays
 - Linux
excerpt: |
    Learn how to strategically use the `sleep` command in shell scripting to introduce delays and control the timing of actions in your Linux scripts. Discover its various use cases, alternatives, and how it can help you simulate delays and test your applications under different conditions.
---
**We're [Earthly](https://earthly.dev/). We make building software simpler and faster using containerization. [Check it out](/).**

Timing is key to many applications, but making things happen at the right time can be challenging. For instance, sometimes you need to introduce a delay to a script to make sure actions are taken precisely when you want them to. The good news is that the `sleep` command lets you do that. With it, you can pause your Linux scripts, ensuring everything happens when it should.

There are all kinds of use cases for the `sleep` command, including helping you with alarms, timing user output, or simulating delays when testing software. It can also help when coordinating multiple services.

In this article, you'll learn more about the `sleep` command, how it works, and what you can do with it. You'll also learn about a few alternatives for when its functionality isn't quite what you need.

## Understanding the `sleep` Command

![Understanding]({{site.images}}{{page.slug}}/understand.png)\

The `sleep` command works by introducing pauses into your scripts. When you use `sleep`, the system waits before moving on to the next command. The exact time to wait is specified as an argument to the command.

By default, `sleep` works in seconds. [On some systems, such as macOS and FreeBSD](https://www.cyberciti.biz/faq/linux-unix-sleep-bash-scripting/), that's all you can use.
Other versions, such as GNU and Linux, accept decimals, allowing you to specify values, such as `sleep 0.1`, to give you a delay of a tenth of a second.

There are several options you can use with `sleep` to specify what it does. For instance, affixing suffixes to the value you provide lets you use values other than seconds. `sleep` accepts commands such as the following:

* **`sleep 5m`** (*ie* five minutes)
* **`sleep 10h`** (*ie* ten hours)
* **`sleep 3d`** (*ie* three days)

Small delays can be useful if you want to give a service more of a chance to complete or if you want to make the output more parsable. It can also be used to delay actions until an appropriate time.

In addition to affixing suffixes, you can also specify multiple arguments to `sleep`, which are then added together to determine how long to wait. If you want to use a single `sleep` command to wait for a multistage process, you could add the required waits together in bash.

For more information on the parameters available, consult `sleep`'s manual page, by typing the following:

~~~{.bash caption=">_"}
man sleep
~~~

Here's a screenshot of the manual output:

<div class="wide">
![Screenshot showing the `sleep` manual page in bash]({{site.images}}{{page.slug}}/bKR0y4c.png)
</div>

## Using the `sleep` Command

There are several use cases for `sleep`. Let's run through a few of them.

### Adding Delays Between Commands

`sleep` lets you introduce delays between commands and can allow time for a command to complete before moving on to the next one. This can help give a user the chance to read a display, or it could simply schedule an activity that you want to happen at a specific time (*ie* taking a daily snapshot of a company share price).

In addition, web-based services take time to complete. You can utilize `sleep` if you want to allow time for that to happen before moving on with your program. It can also help if you have computationally expensive tasks running, [allowing time for them to finish](https://phoenixnap.com/kb/linux-sleep) before continuing.

### Using `sleep` to Pace a Script's Execution

There are all kinds of reasons you may want to pace a script's execution, and the `sleep` command can help you do that. For instance, if a script consumes resources, then pacing it can limit its consumption, leaving sufficient resources available for other tasks. Or for commands that don't need to be run frequently, such as monitoring [an alert](https://www.tecmint.com/linux-sleep-command-examples/) or checking if a website is online, it may be beneficial to space out their execution.

In addition, you may want to leave a delay so that other parts of the system can catch up. For instance, if you're ingesting data for some kind of processing, then you might want to slow down your processing to match the pace of the data ingestion. You could do that with an arbitrary wait or a conditional check to determine if the pause is necessary.

You can also add timing effects to scripts that require user interaction. You can give people a second or so to see that a particular service has been installed before continuing with configuration. If you're writing a text adventure, you could add a dramatic pause or you could simply thank users after providing input, pausing for a couple of seconds before moving on.

### Simulating Slow Network Connections

![Simulating]({{site.images}}{{page.slug}}/simulate.png)\

In addition to adding delays and pausing a script's execution, `sleep` lets you simulate problems. If you want to know how your stack is affected if a process takes longer than usual, then an artificial delay can help. Simply add a `sleep` command to the script that runs when your service is called.

The `sleep` command really becomes particularly useful in testing scenarios, especially when network problems or system faults cause unexpected delays. Slow connections and service failures can lead to prolonged wait times for your applications.

Testing how services deal with slow or failing services is harder than it sounds. Running `sleep` as part of your testing lets you check for issues that might be overlooked if the rest of your tests take place under perfect network conditions that don't accurately reflect the real world.

### Interrupting `sleep` With a Signal

You may run into a situation where you need to wake up a sleeping system. For instance, if you have a system regularly performing a delayed action, you might want to stop it either because its task is no longer necessary or because you want to modify its behavior. Or you may want to change or reduce the sleep delay if conditions change. Perhaps there's an emergency and you want to monitor something more regularly.

To exit `sleep`, just press the **Ctrl+C** keys at the same time. However, that may not work on some older systems, so be sure to test that it works for you before relying on it.

In such cases, it's possible to run `sleep` in the background while using `wait` to wait for it to complete. You can read how to do that on this [Stack Overflow page](https://stackoverflow.com/questions/32041674/linux-how-to-kill-sleep).

### Using `sleep` with Loops and Conditions

The `sleep` command becomes more powerful if used as part of other programming constructs, allowing for dynamic adjustments in its behavior. You can even set scripts to run a specific number of times before moving on. For instance, you can use `sleep` to take the reading from a thermometer or other sensor hourly, and then pipe that to a log at the end of the day.

You can also use conditionals to choose whether to pause. If a service may not finish before your script needs it, you could check for that and pause it to give it another chance to complete.

Following is an example using a loop to give the user a countdown. This is a trivial example, but it could easily be expanded for use as an alarm or a regular task reminder, or adapted to trigger any kind of code regularly:

~~~{.bash caption=">_"}
count=5
declare -i count
echo "Prepare to launch"
while [[ $count -gt 0 ]]; do
    sleep 1
    echo "$count"
    count=$count-1
done
sleep 1
echo "Lift Off"
~~~

Here's what that looks like when running in the Linux command line:

<div class="wide">
![Output of Linux countdown script]({{site.images}}{{page.slug}}/TYuWTQ5.png)
</div>

## Alternative Commands to `sleep`

![Alternate]({{site.images}}{{page.slug}}/alternate.png)\

`sleep` isn't the only tool in your toolbox when it comes to pacing your scripts. Let's look at some other commands and learn when they're helpful.

### The `wait` Command

Whereas `sleep` creates a pause between commands, `wait` [waits for a process to finish](https://linuxhint.com/bash-wait-command-linux/) or, more precisely, to change its state. That's useful if you want to run a command in the background and have several things going on at once. For instance, you may want to launch a background process and then do some other things in your main script before waiting for the background process to finish before moving on.

The following code, adapted from [an example on ItsLinuxFOSS](https://itslinuxfoss.com/bash-wait-command-explained/), shows you how to run the process out of order using `wait`:

~~~{.bash caption=">_"}
echo "Background" &
echo "Foreground"
wait
echo "After"
~~~

The `&` after the first line makes that command run in the background.

Without the `wait` command, the commands output order is `Foreground, After, Background`, but with `wait`, the order becomes `Foreground, Background, After`.

You can specify the process being waited for as well as the state to wait for.

### The `read` Command

Linux doesn't include a pause command, but you can [create pauses using `read`](https://www.cyberciti.biz/tips/linux-unix-pause-command.html) by adding the `-p` flag followed by a message. This allows you to instruct Linux to wait for user input before continuing:

~~~{.bash caption=">_"}
read -p "Hello"
~~~

That's a good way to make sure the user has read input or to request they take an action or even make a decision. You can also use `read` if you want a user to be able to start something at a specific time; for instance, if you want to launch process when the user presses a button.

Using the `-t` flag lets you specify the number of seconds to wait. However, in this case, you won't wait for user input:

~~~{.bash caption=">_"}
read -t 3 -p "Hello"
~~~

This lets you give users a chance to read important output; however, here, the script continues after a delay, with no further action on their part.

## Conclusion
<!--sgpt-->
The `sleep` command is your handy tool in script pacing. It's great for resource conservation, task scheduling, and timing tasks perfectly. But remember, it's more than just supplying an integer, so dive into all its features for max benefits. Also, be aware of other tools like `wait` and `read` for situations where `sleep` doesn't quite fit.

Bash is powerful and can do wonders for Linux users. If you're looking to supercharge your Linux scripting even further, you might want to give [Earthly](https://earthly.dev/) a spin!

For more insights on `sleep`, check out the [official docs](https://man7.org/linux/man-pages/man1/sleep.1.html) or our [Bash series](https://earthly.dev/blog/series/bash/) for more Bash goodness.

{% include_html cta/bottom-cta.html %}
