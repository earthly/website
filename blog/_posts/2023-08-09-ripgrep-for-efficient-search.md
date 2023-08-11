---
title: "How to Use `ripgrep` to Improve Your Search Efficiency"
categories:
  - Tutorials
toc: true
author: Sriram Ramanujam
editor: Mustapha Ahmad Ayodeji

internal-links:
 - how to use ripgrep
 - improve search efficiency
 - search efficiency
 - ripgrep to improve search efficiency

excerpt: | 
This article will cover what the ripgrep command-line tool does, what its key features are, how to install it, and how to use its basic and advanced options.

---

**We're [Earthly](https://earthly.dev/). We simplify building software with containerization. This article discusses using the `ripgrep` command-line tool. However, if you are curious about getting better build times by combining ideas from Makefile and Dockerfile? [Check us out.](https://earthly.dev/)**

The [`ripgrep`](https://docs.rs/crate/ripgrep/11.0.2/source/GUIDE.md) (`rg` for short) command is a command-line tool typically used to search a file for a specific text pattern. It is popular amongst developers and sysadmins for its speed and efficiency. One can make use of `ripgrep` for searching code snippets, analyzing log files, debugging issues, and various other purposes. Further, `ripgrep` is written in Rust, which provides high performance, memory safety, and increased concurrency with lightweight threads. Also, it uses optimized algorithms for searching large files quickly with intelligent defaults.

This article will cover – with proper illustrations – what the `ripgrep` command-line tool does, what its key features are, how to install it, and how to use its basic and advanced options. Throughout this article, the commands will be executed on a Linux operating system with Ubuntu distribution. However, the features and syntax of the commands remain the same for other operating systems.
We intend this article for software professionals who work with large volumes of text data and need to perform complex searches and manipulations on top of it. Also, there are no strict prerequisites for working with the `ripgrep` command; however, a basic familiarity with the command-line interface and regular expressions can be helpful.

## Features of the `ripgrep` Command-line Tool

![Features]({{site.images}}{{page.slug}}/features.png)\

Let's have a quick look into some of the essential features of `ripgrep` compared to other alternatives like [grep](https://linux.die.net/man/1/grep), [ack](https://linux.die.net/man/1/ack), and so on:

- **Speed**: `ripgrep` is highly optimized and uses an [advanced searching algorithm](https://cp-algorithms.com/string/aho_corasick.html) to perform quick searches across multiple large files and folders.

- **Compressed File Search**: Beyond the traditional file search, the `ripgrep` command-line tool can search for patterns across compressed zip files.

- **Ease of Use**: It has a simple and interactive command-line interface that can be customized as per our needs.

- **Color-Coded Output**: The `ripgrep` command output has a customizable color-coded scheme. This makes it easier to identify the matches in the search results.

- **Compatibility**: `ripgrep` is available for Windows, Linux, and Mac OS and works well across all platforms

## Installation of `ripgrep`

We can install the `ripgrep` command-line tool using the package manager on the Ubuntu machine. Firstly, let's update all the installed packages to their latest versions. These updated packages will further strengthen the devices from a security perspective. Also, the upgrade commands will provide the new features and related dependencies for the current version of the packages that we have installed before:

~~~{.bash caption=">_"}
$ sudo apt-get update -y
$ sudo apt-get upgrade -y
~~~

Now, let's install the `ripgrep` command-line tool using the `apt-get install ripgrep` command:

~~~{.bash caption=">_"}
$ sudo apt install ripgrep -y
~~~

~~~{ caption="Output"}
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
The following NEW packages will be installed:
  ripgrep
0 upgraded, 1 newly installed, 0 to remove and 3 not upgraded.
...
... output truncated ...
...
Setting up `ripgrep` (13.0.0-2ubuntu0.1) ...
Processing triggers for man-db (2.10.2-1) ...
~~~

Now, let's use the [`which`](<https://linux.die.net/man/1/which>) command to get the installation path of the `rg` (ripgrep) binary:

~~~{.bash caption=">_"}
$ which rg
~~~

~~~{ caption="Output"}
/usr/bin/rg
~~~

Also, we can get the installed version of `ripgrep` using the `--version` option. Here, we are using version 13.0.0 of ripgrep:

~~~{.bash caption=">_"}
$ rg --version
~~~

~~~{ caption="Output"}
ripgrep 13.0.0
-SIMD -AVX (compiled)
+SIMD +AVX (runtime)
~~~

We've successfully installed the `ripgrep` command-line tool on the Ubuntu machine. If you are on a different operating system, here is the [installation guide](https://github.com/BurntSushi/ripgrep#installation) for other operating systems like BSD, Windows, MAC, Debian, and so on.

Let's quickly delve into the `ripgrep` command-line tool usage with examples.

## How to Use the `ripgrep` Command

The basic syntax for using the `ripgrep` command-line tool is `rg <STRING> <PATH>`. The string argument is the text we want to search for in the files or directories. The `PATH` is an optional parameter to set the file or folder path. By default, it takes the current folder as its default path, if no path is specified:

~~~{.bash caption=">_"}
$ rg "EXT4" /var/log/syslog
~~~

Here, we are searching for logs that contain the word `EXT4` from `/var/log/syslog`, which is the central repository for all system log messages:

~~~{ caption="Output"}
3874:Apr  2 12:10:49 ubuntu-2204 kernel: [   15.040728] EXT4-fs (sda3): mounted filesystem with ordered data mode. Quota mode: none.
3932:Apr  2 12:10:49 ubuntu-2204 kernel: [   18.364213] EXT4-fs (sda3): re-mounted. Quota mode: none.
~~~

Special characters in OS terminals have varying execution instructions. Consequently, when searching, specific characters like Backslash (`\`), Asterisk (`*`), Question Mark (`?`), Parenthesis `()`, Square brackets `[]`, Double quotes `""`, and others in the search pattern should be masked with a single backslash (`\`). This prevents them from being treated as regular expression syntax:

~~~{.bash caption=">_"}
$ rg "EXT4-fs \(sda3\):" /var/log/syslog
~~~

Here, we are searching for logs related to the storage device sda3. The search is performed on the file /var/log/syslog, and parentheses around sda3 are escaped using a single backslash (\) to treat them as literal characters.

~~~{ caption="Output"}
3874:Apr  2 12:10:49 ubuntu-2204 kernel: [   15.040728] EXT4-fs (sda3): mounted filesystem with ordered data mode. Quota mode: none.
3932:Apr  2 12:10:49 ubuntu-2204 kernel: [   18.364213] EXT4-fs (sda3): re-mounted. Quota mode: none.
~~~

We can search for patterns in multiple folders and files with a single command by giving the file or folder path.

Here, we are searching for logs that contain the text `EXT4-fs (sda3)` in the `/var/log` folder and the `/var/backups/dpkg.arch.0` file:

~~~{.bash caption=">_"}
$ rg "EXT4-fs \(sda3\)" /var/log/ /var/backups/dpkg.arch.0
~~~

~~~{ caption="Output"}
/var/log/dmesg
1360:[   11.694347] kernel: EXT4-fs (sda3): mounted filesystem with ordered data mode. Quota mode: none.
1416:[   13.540628] kernel: EXT4-fs (sda3): re-mounted. Quota mode: none.

/var/log/syslog.1
1560:Mar 28 19:58:58 ubuntu-2204 kernel: [    9.511322] EXT4-fs (sda3): mounted filesystem with ordered data mode. Quota mode: none.
1618:Mar 28 19:58:58 ubuntu-2204 kernel: [   11.089191] EXT4-fs (sda3): re-mounted. Quota mode: none.
~~~

Furthermore, the `--count` option of the  `ripgrep` command-line tool provides the number of matched lines instead of printing the matched lines. Here, the output indicates that there were ten matched lines in the `kern.log.1` file, two matched lines in `dmesg` and `dmesg.0`, and one matched line in the `syslog` file. It also shows that the search happens in the current folder and its subfolders:

~~~{.bash caption=">_"}
$ rg --count "EXT4-fs \(sda3\)" /var/log/ /var/backups/dpkg.arch.0
~~~

~~~{ caption="Output"}
/var/log/dmesg:2
/var/log/dmesg.0:2
/var/log/installer/syslog:1
/var/log/kern.log.1:10
~~~

The tool also allows us to perform a case-insensitive search using the `-i` or `--ignore-case` option. In the following example, we will ignore case differences and search for `Error` in the syslog file. So this command will match `Error`, `ERROR`, `error`, `eRRor`, and any other variation of the word with different capitalization:

~~~{.bash caption=">_"}
$ rg -i "Error" /var/log/syslog
~~~

~~~{ caption="Output"}
6211:Apr  2 12:15:35 ubuntu-2204 kernel: [    1.986379] RAS: Correctable Errors collector initialized.
26819:Apr  5 19:07:51 ubuntu-2204 pipewire[8265]: mod.rt: RTKit error: org.freedesktop.DBus.Error.AccessDenied
...
... output truncated ...
...
~~~

The tool also has a multi-pattern search option which makes it possible to search multiple patterns simultaneously in a single command. To perform this, we just need to separate the multiple search patterns by the `|` character.

Here, we are getting the lines with matches either `EXT-fs (sda3)` or `Error`:

~~~{.bash caption=">_"}
$ rg "EXT4-fs \(sda3\)|Error: " /var/log/syslog
~~~

~~~{ caption="Output"}
3874:Apr  2 12:10:49 ubuntu-2204 kernel: [   15.040728] EXT4-fs (sda3): mounted filesystem with ordered data mode. Quota mode: none.
3932:Apr  2 12:10:49 ubuntu-2204 kernel: [   18.364213] EXT4-fs (sda3): re-mounted. Quota mode: none.
3978:Apr  2 12:10:49 ubuntu-2204 kernel: [   19.180410] ACPI Error: No handler for Region [SYSI] (0000000012a1600a) [IPMI] (20220331/evregion-130)
~~~

## Advanced Usage of `ripgrep`

We have now covered the fundamental features of the `ripgrep` command-line tool. Let's now take a brief look at its advanced features, which can help us maximize the usage of the tool.

The `ripgrep` command-line tool allows us to get additional lines with the match pattern in the search results, which helps in data sequencing and correlation. The options `-B [before context]` and `-A [after context]` allow for specifying the number of lines before and after the pattern respectively.

The example below displays one line of context before and two lines after each matching line:

~~~{.bash caption=">_"}
$rg "EXT4-fs \(sda3\)" /var/log/syslog -B 1 -A 2
~~~

~~~{ caption="Output"}
3931-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.362418] systemd[1]: Finished Load Kernel Module efi_pstore.
3932:Apr  2 12:10:49 ubuntu-2204 kernel: [   18.364213] EXT4-fs (sda3): re-mounted. Quota mode: none.
3933-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.365877] systemd[1]: Finished Remount Root and Kernel File Systems.
3934-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.366819] systemd[1]: Activating swap /swapfile
---
…
… output truncated …
…
~~~

In this example, the lines containing the pattern "EXT4-fs (sda3)" are shown along with one line before and two lines after each pattern match.

The tool also has an option `-C [context]` which combines the functionalities of the option `-A` and `-B`. The option `-C`, shows the specified number of lines before and after the matched line. It becomes handy while troubleshooting to get the events that happened before and after the matched error.

Consider the example below that searches for the pattern in the current folder and its subfolders and displays two lines before and after each matching line:

~~~{.bash caption=">_"}
$rg "EXT4-fs \(sda3\)" /var/log/syslog -C 2
~~~

~~~{ caption="Output"}
3930-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.362154] systemd[1]: modprobe@efi_pstore.service: Deactivated successfully.
3931-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.362418] systemd[1]: Finished Load Kernel Module efi_pstore.
3932:Apr  2 12:10:49 ubuntu-2204 kernel: [   18.364213] EXT4-fs (sda3): re-mounted. Quota mode: none.
3933-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.365877] systemd[1]: Finished Remount Root and Kernel File Systems.
3934-Apr  2 12:10:49 ubuntu-2204 kernel: [   18.366819] systemd[1]: Activating swap /swapfile
---
…
… output truncated …
…
~~~

### Searching Compressed Files
`ripgrep` can also search for the text in compressed files. As of this writing it supports the follow file formats:

- .lzma
- .bzip2 
- .xz 
- .lz4 
- .gzip
- .zstd

We will use the `--search-zip` or `-z` option to tell the `ripgrep` command-line tool to search for text in compressed files without extracting its contents:

~~~{.bash caption=">_"}
$ rg 'ERST' -z dmesg.1.gz
~~~

~~~{ caption="Output"}
65:[    0.012175] kernel: ACPI: ERST 0x000000007BAFB000 000230 (v01 DELL   PE_SC3   00000002 DELL 00000001)
86:[    0.012202] kernel: ACPI: Reserving ERST table memory at [mem 0x7bafb000-0x7bafb22f]
1075:[    1.842525] kernel: ERST: Error Record Serialization Table (ERST) support is initialized.
~~~

Also, the tool allows us to customise the color scheme used to highlight the matched text in the output. By default, the tool presents the matched text in red color. However, we can also customize the color using the `--color` option of the frpresentscommand-line tool. It provides color customization to line numbers, search matches, and file paths. The customization includes the background color, foreground color, and style.

Adding these colors makes the search more readable and easier to work with when we are working with large complex patterns.

In the example below, we are trying to highlight the file path in red font with white background, match the text in blue font with bold style, and line numbers with yellow:

~~~{.bash caption=">_"}
$ rg 'ALERT' --colors 'path:fg:red' --colors 'path:bg:white' \
--colors 'match:fg:blue' 
--colors 'line:bg:yellow' --colors 'match:style:bold' -z messages-2022-04-2*.gz
~~~

<div class="wide">
![Img]({{site.images}}{{page.slug}}/hJiISas.png)\
</div>

The `ripgrep` command-line tool also allows us to perform search and replace operations. We can use the `--replace` option with the new and old strings as the arguments. This substitutes the new string with the old string found during the search.

The following command replaces all occurrences of `ERST` in the `/var/log/dmesg.1.gz` file with a new string `EARTHLY`. It will perform the replacement only on the displayed output, but not on the original file:

~~~{.bash caption=">_"}
$ rg --replace 'EARTHLY' 'ERST' -z dmesg.2.gz
~~~

~~~{ caption="Output"}
65:[    0.012106] kernel: ACPI: EARTHLY 0x000000007BAFB000 000230 (v01 DELL   PE_SC3   00000002 DELL 00000001)
86:[    0.012134] kernel: ACPI: Reserving EARTHLY table memory at [mem 0x7bafb000-0x7bafb22f]
1075:[    1.846199] kernel: EARTHLY: Error Record Serialization Table (EARTHLY) support is initialized.
~~~

<div class="notice--info">
As mentioned earlier, the replacement is only performed on the displayed output, we can however redirect the output to a new file in case we need it for future reference.

You can check out [this article](https://earthly.dev/blog/linux-text-processing-commands) to learn about redirection and other text-processing commands in Linux
</div>
Further, we can also provide regular expressions to create a group pattern and create some complex search queries. The below query will search for the lines starting with `Apr`, has the pattern `ID=` with two-digit numerals and space with any characters:

~~~{.bash caption=">_"}
$ rg '^Apr.*ID=[0-9+][0-9+] \w+ ' /var/log/syslog
~~~

~~~{ caption="Output"}
482:Apr  2 02:33:26 ubuntu-2204 kernel: [325746.634509] [UFW BLOCK] IN=eno1 OUT= MAC=18:66:da:b4:2c:2a:f4:cc:55:43:4f:c1:08:00 SRC=113.203.240.39 DST=14.141.138.19 LEN=48 TOS=0x00 PREC=0x20 TTL=107 ID=43 DF PROTO=TCP SPT=56379 DPT=3389 WINDOW=8192 RES=0x00 SYN URGP=0
1042:Apr  2 05:35:04 ubuntu-2204 kernel: [336644.124908] [UFW BLOCK] IN=eno1 OUT= MAC=18:66:da:b4:2c:2a:f4:cc:55:43:4f:c1:08:00 SRC=113.203.240.39 DST=14.141.138.19 LEN=52 TOS=0x02 PREC=0x20 TTL=107 ID=91 DF PROTO=TCP SPT=53749 DPT=3389 WINDOW=8192 RES=0x00 CWR ECE SYN URGP=0
~~~

Lastly, we can use `rg --help` to display a comprehensive list of all available options with descriptions. This information can help you understand the `rg` tool and its syntax effectively:

~~~{.bash caption=">_"}
rg -help
~~~

## Conclusion

In summary, The `ripgrep` command-line tool is an excellent tool for searching a large set of data in a more customizable form. As we saw in the previous sections, it also has many inbuilt features like multi-pattern search, compressed file search, highlighting the search pattern with different color codes, search and replace options, etc. With its advanced features and highly optimized performance, The `ripgrep` looks a popular choice amongst IT professionals across the industry. If you haven't tried the `ripgrep` command-line tool yet, we highly recommend giving it a try!

To learn more about the `ripgrep` command line tool, you can check out the following links:

- [Github](https://github.com/BurntSushi/ripgrep)
- [Linuxhandbook](https://linuxhandbook.com/ripgrep/)
- [Mariusschulz](https://mariusschulz.com/blog/fast-searching-with-ripgrep)

{% include_html cta/bottom-cta.html %}
