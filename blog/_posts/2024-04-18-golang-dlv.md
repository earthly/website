---
title: "go delve - The Golang Debugger "
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
excerpt: |
    Delve is a CLI-based debugger for Go that allows you to set breakpoints, inspect goroutines, and manipulate variables in real-time. It supports remote debugging and seamlessly integrates with major IDEs like Visual Studio Code.
---
**This article explores the use of Delve for effective Go debugging. Earthly streamlines and enhances Go build processes. [Check it out](https://cloud.earthly.dev/login).**

Delve (`dlv`) is a CLI-based debugger for Go, tailored to the language's concurrency model and runtime. It allows you to set breakpoints, inspect goroutines, and evaluate and manipulate variables in real-time. Delve supports remote debugging and seamlessly integrates with major IDEs, including Visual Studio Code. Let me walk you through using it, but first, some background.

## Background

In my recent foray into Python, one thing that has become endlessly useful is the ability to add a `breakpoint()` to a line of code without an IDE or any setup at all, ending up in a console-based debugger at that point.

In the past, I had always associated debuggers with IDEs like Visual Studio or IntelliJ. Those are great. However, I find myself in VS Code most of the time now, and I've never fully understood its debugging support. Instead, I resort to using prints, which usually suffices. But there are times when I need to step through some code and require an easy-to-use debugger. This is where Delve shines, making it a breeze to debug a go executable, a go test, and even, in theory, a go docker container running on a remote host.

## Installing Delve

To install just run `go install` with the package path:

~~~
$ go install github.com/go-delve/delve/cmd/dlv@latest

go: downloading github.com/go-delve/delve v1.22.1
go: downloading github.com/hashicorp/golang-lru v1.0.2
go: downloading github.com/cosiner/argv v0.1.0
go: downloading github.com/derekparker/trie v0.0.0-20230829180723-39f4de51ef7d
go: downloading github.com/go-delve/liner v1.2.3-0.20231231155935-4726ab1d7f62
go: downloading golang.org/x/arch v0.6.0
go: downloading github.com/google/go-dap v0.11.0
go: downloading go.starlark.net v0.0.0-20231101134539-556fd59b42f6
go: downloading github.com/mattn/go-runewidth v0.0.13
go: downloading github.com/rivo/uniseg v0.2.0

~~~

That will install it into your GOPATH:

~~~
$ go env GOPATH
/Users/adam/go
~~~

Make sure you have GOPATH in your path ( I didn't):

~~~
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc && source ~/.zshrc
~~~

Then you can run it:

~~~
$ dlv version                                                                 
Delve Debugger
Version: 1.22.1
Build: $Id: 0c3470054da6feac5f6dcf3e3e5144a64f7a9a48 $
~~~

### Debugging `dlv debug`

Now before `dlv`, I was using `go run` with a lot of parameters to run Earthly:

~~~
go run cmd/earthly/main.go -P -i --buildkit-image earthly/buildkitd:prerelease ./tests/raw-output+gha
~~~

To debug with delve I just change `go run` to `dlv debug` and introduce a `--` to delimit where my apps params start.

~~~
dlv debug cmd/earthly/main.go -- -P -i --buildkit-image earthly/buildkitd:prerelease ./tests/raw-output+gha
~~~

Now, I want to debug this header printing code in Earthly:

~~~{.go caption="conslogging/conslogging.go"}
func (cl ConsoleLogger) PrintPhaseHeader(phase string, disabled bool, special string) {
    w := new(bytes.Buffer)
    cl.mu.Lock()
    defer func() {
        _, _ = w.WriteTo(cl.errW)
        cl.mu.Unlock()
    }()
    msg := phase
    c := cl.color(phaseColor)
    if disabled {
        c = cl.color(disabledPhaseColor)
        msg = fmt.Sprintf("%s (disabled)", msg)
    } else if special != "" {
        c = cl.color(specialPhaseColor)
        msg = fmt.Sprintf("%s (%s)", msg, special)
    }
    underlineLength := utf8.RuneCountInString(msg) + 2
    if underlineLength < barWidth {
        underlineLength = barWidth
    }
    c.Fprintf(w, " %s", msg)
    fmt.Fprintf(w, "\n")
    c.Fprintf(w, "%s", strings.Repeat("—", underlineLength))
    fmt.Fprintf(w, "\n\n")
}
~~~

I want to understand more about the underlineLength calculation at run time. To do so, I set a breakpoint and continue execution until that point is hit:

~~~
(dlv) break conslogging/conslogging.go:230
Breakpoint 1 set at 0x1050c4e44 for github.com/earthly/earthly/conslogging.ConsoleLogger.PrintPhaseHeader() ./conslogging/conslogging.go:230
(dlv) continue

~~~

`dlv` returns this, when I hit a break point:

~~~
   225:         }
   226:         underlineLength := utf8.RuneCountInString(msg) + 2
   227:         if underlineLength < barWidth {
   228:                 underlineLength = barWidth
   229:         }
=> 230:         c.Fprintf(w, " %s", msg)
   231:         fmt.Fprintf(w, "\n")
   232:         c.Fprintf(w, "%s", strings.Repeat("—", underlineLength))
   233:         fmt.Fprintf(w, "\n\n")
   234: }
   235:
~~~

To check the value of underline length I can use print (p) or list all locals with `locals`

~~~
(dlv) p underlineLength
80
~~~

~~~
(dlv) locals
w = (*bytes.Buffer)(0x1400041c420)
msg = "Init 🚀"
c = ("*github.com/fatih/color.Color")(0x140001e49e0)
underlineLength = 80
(dlv) p underlineLength
~~~

I can also use `args` to get the arguments passed into my function:

~~~
(dlv) args
cl = github.com/earthly/earthly/conslogging.ConsoleLogger {prefix: "", metadataMode: false, isLocal: false,...+14 more}
phase = "Init 🚀"
disabled = false
special = ""
~~~

From this point, I can do many things, including saving a checkpoint that lets me return to this point of execution later, but for now, I just want to modify `underlineLength` and see how that changes the execution. I can do this using `set` and print `p`.

~~~
(dlv) set underlineLength = 5
(dlv) p underlineLength
5
~~~

I can then use next (`n`) to step through the code and continue (`c`) to continue execution and see my new shortened underline. `c` works just like you'd expect continue to work, it continues the execution until another break point is hit.

~~~
(dlv) c
Init 🚀
-----
~~~

That `----` is my much shortened underscore line, but the problem is this function gets called in a loop and so I quickly end up back at my breakpoint again:

~~~
   225:         }
   226:         underlineLength := utf8.RuneCountInString(msg) + 2
   227:         if underlineLength < barWidth {
   228:                 underlineLength = barWidth
   229:         }
=> 230:         c.Fprintf(w, " %s", msg)
   231:         fmt.Fprintf(w, "\n")
   232:         c.Fprintf(w, "%s", strings.Repeat("—", underlineLength))
   233:         fmt.Fprintf(w, "\n\n")
   234: }
   235:
~~~

I can keep mashing `c` until I get past this, or clear my breakpoint with `clear`:

~~~
breakpoints
Breakpoint runtime-fatal-throw (enabled) at 0x1048551ac,0x10483e3c0,0x10483e480 for (multiple functions)() <multiple locations>:0 (0)
Breakpoint unrecoverable-panic (enabled) at 0x10483e750 for runtime.fatalpanic() /opt/homebrew/Cellar/go/1.21.1/libexec/src/runtime/panic.go:1188 (0)
        print runtime.curg._panic.arg
Breakpoint 1 (enabled) at 0x1050c4e44 for github.com/earthly/earthly/conslogging.ConsoleLogger.PrintPhaseHeader() ./conslogging/conslogging.go:230 (1)
~~~

My breakpoint is breakpoint 1, so I can clear it and continue:

~~~
(dlv) clear 1
(dlv) continue

~~~

**Side Note:** Breakpoints `runtime-fatal-throw` and `unrecoverable-panic` do exactly what they sound like. Delve includes breakpoints on these critical failure points to debug a fatal runtime throw or an unrecoverable panic easily.

With the breakpoint cleared, Earthly now runs to completion.

~~~
Process 91365 has exited with status 0
Process 91365 has exited with status 0
(dlv) 
~~~

From that point, I can restart to rerun the same process with the same arguments or quit. And that is quick tutorial on `dlv`.

## Quick Tips

For all the in and outs of `dlv` checkout [the docs](https://github.com/go-delve/delve), but here is some quick tips.

| **Task**                 | **Go Command**          | **Delve Command**          |
|--------------------------|-------------------------|----------------------------|
| **Run Program**          | `go run main.go`        | `dlv debug`                |
| **Run Tests**            | `go test`               | `dlv test`                 |
| **Compile and Run Executable** | `go build -o myapp && ./myapp` | `dlv exec ./myapp`       |
| **Run Specific Test**    | `go test -run TestName` | `dlv test -- -test.run TestName` |

### Keyboard Shortcuts

| **Command Name** | **Shortcut** | **Description**                                |
|------------------|--------------|------------------------------------------------|
| `break`          | `b`          | Sets a breakpoint at a specific source location. |
| `continue`       | `c`          | Resumes program execution until a breakpoint.    |
| `step`           | `s`          | Executes the current line, entering functions.    |
| `next`           | `n`          | Executes the current line, skipping functions.    |
| `print`          | `p`          | Prints the value of a variable or expression.     |
| `list`           | `l`          | Displays source around the current execution point. |
| `clear`          |              | Removes a breakpoint.                            |
| `set`            |              | Modifies the value of a variable during debugging. |

## Headless for remote or Containerize Debugging

Delve can be run headless, `--headless` , and then connected to remotely. This can be useful in a docker container where the trick is to install `dlv` and then run it and open the correct port:

~~~{.dockerfile caption="Dockerfile"}
FROM golang:1.18

RUN go install github.com/go-delve/delve/cmd/dlv@latest

COPY myapp  .
EXPOSE 40000

# Command to run Delve server
CMD ["dlv", "--listen=:40000", "--headless=true", "--api-version=2", "--accept-multiclient", "exec", "./myapp"]
~~~

Your app needs to be built with debug capabilities, and of course, you can use Earthy to do this building and containerizing. Here is an Earthfile for building the app with debug symbols and building the debug container:

~~~{.dockerfile caption="Earthfile"}
VERSION 0.8
FROM golang:1.22

build-debug:
    WORKDIR /myapp
    COPY ./src .
    RUN go build -gcflags="all=-N -l" -o /myapp/myapp .
    SAVE ARTIFACT /myapp/myapp myapp

containerize-debug:
    FROM golang:1.18
    # Install Delve 
    RUN go install github.com/go-delve/delve/cmd/dlv@latest
    # Copy the built app from the previous stage
    COPY +build-debug/myapp /myapp/myapp
    WORKDIR /myapp
    EXPOSE 40000
    CMD ["dlv", "--listen=:40000", "--headless=true", "--api-version=2", "--accept-multiclient", "exec", "/myapp/myapp"]
    SAVE IMAGE myapp-debug
~~~

Then you can debug like this:

~~~
earthly +containerize-debug
docker run -d -p 40000:40000 myapp-debug
dlv connect localhost:40000
~~~

You could even run delve from right within Earthly:

~~~{.dockerfile caption="Earthfile"}
interactive-debug:
    FROM golang:1.18
    RUN go install github.com/go-delve/delve/cmd/dlv@latest
    COPY +build-debug/myapp /myapp/myapp

    # Did you know earthly also allows you to run commands that require a tty?
    RUN --interactive dlv exec /myapp/myapp
~~~

## VS Code and GoLand

Delve is what powers the debugger you see in various go IDEs. If you want to debug go code in VS Code, then the official go extension will probably just work once you configure a launch.js.

For me, I had to add this under `Run`-> `Add Configuration`:

~~~{.yaml caption="launch.js"}
{
    "version": "0.2.0",
    "configurations": [
 {
            "name": "Debug Earthly",
            "type": "go",
            "request": "launch",
            "mode": "debug",
            "program": "./cmd/earthly/main.go",
            "args": [
                "./examples/c+deps"
            ],
            "env": {
                "FORCE_COLOR": "1"
            },
            "cwd": "${workspaceFolder}"
        }

    ]
}
~~~

This is the equivalent of `dlv debug`. To Debug an executable in VS Code, build with debug symbols `-gcflags="all=-N -l"` and then use `mode=exec`, which corresponds to `dlv exec`:

~~~{.yaml caption="launch.js"}
        {
            "name": "Debug Earthly Binary",
            "type": "go",
            "request": "launch",
            "mode": "exec",
            "env": {
                "FORCE_COLOR": "1"
            },
            "program": "./build/darwin/amd64/earthly",
            "args": [
                "./examples/c+deps"
            ],
            "cwd": "${workspaceFolder}"
        },
~~~

You can make similar changes to `mode` to run tests with `dlv test` and presumably to connect to remote or headless debug sessions.

### GoLand and IntelliJ

Delve works out of the box with GoLand, and with the IntelliJ Go Plugin. It works just like IntelliJ users would expect a debugger to work.

To setup remote debugging a bit more configuration is required but the folks at JetBrains kindly provide a GUI with instructions embedded in it.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/7180.png --alt {{ GoLand Remote Go Debugging }} %}
<figcaption>GoLand Remote Go Debugging ( find this under Run&Debug Configurations -> Add Configuration -> Go Remote)</figcaption>
</div>

## That's a Wrap

Ok, that's a wrap. `dlv` can integrate with neovim, vim, neovim, Sublime and probably a number of other editors as well, but setting those up is left as an exercise for the reader. Check out [github](https://github.com/go-delve/delve) for more information on `dlv`, including trace points and checkpoints which are valuable tools that deserve their own write up.

{% include_html cta/bottom-cta.html %}
