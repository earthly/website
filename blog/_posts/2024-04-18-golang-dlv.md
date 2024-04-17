---
title: "go delve - The Golang Debugger "
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
Delve (`dlv`) is a CLI based debugger for Go, tailored to the language's concurrency model and runtime. You can set breakpoints, inspect goroutines, and evaluate and manipulate variables in real time. Delve supports remote debugging and seamlessly integrates with major IDEs, including Visual Studio Code. Let me walk your through using it, but first some background.

## Background

In my recent foray into python that one thing that has become endless useful is the ablity to add `breakpoint()` to a line of code, and without an IDE or any setup at all, ending up in a console based debugger at that point.

In the past, I had always associated debuggers with IDEs like Visual Studio or Intellij and they were very useful for me, but now I find myself in VS Code most of the time and I've never figured out it's debugging support works. Often I'm just using prints and that is usually enough. But sometimes I want to walk through some code, and need a easy to use debugger. Thankfully, delve makes its easy to debug a go executuble, a go test, even in theory, a go docker container running on a remote host.

## Installing Delve

To install just run `go install` with the package path:

```
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

```
That will install it into your GOPATH:

```
$ go env GOPATH
/Users/adam/go
```

Make sure you have GOPATH in your path ( I didn't):
```
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.zshrc && source ~/.zshrc
```

Then you can run it:
```
$ dlv version                                                                 
Delve Debugger
Version: 1.22.1
Build: $Id: 0c3470054da6feac5f6dcf3e3e5144a64f7a9a48 $
```
### Debugging `dlv debug`

Now before `dlv`, I was using `go run` with a lot of parameters to run Earthly:

````
go run cmd/earthly/main.go -P -i --buildkit-image earthly/buildkitd:prerelease ./tests/raw-output+gha
```

To debug with delve I just change `go run` to `dlv debug` and introduce a `--` to delimit where my apps params start.

```
dlv debug cmd/earthly/main.go -- -P -i --buildkit-image earthly/buildkitd:prerelease ./tests/raw-output+gha
```

Now, I want to debug this header printing code in Earthly:

```
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
```

Let's say that I want to understand more about how the underlineLength calculation works at run time. To do so I set a breakpoint and continue execution until that point is hit:

```
(dlv) break conslogging/conslogging.go:230
Breakpoint 1 set at 0x1050c4e44 for github.com/earthly/earthly/conslogging.ConsoleLogger.PrintPhaseHeader() ./conslogging/conslogging.go:230
(dlv) continue

```

`dlv` returns this, when I hit a break point:

```
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
```

To check the value of underline length I can use print (p) or list all locals with `locals`

```
(dlv) p underlineLength
80
```

```
(dlv) locals
w = (*bytes.Buffer)(0x1400041c420)
msg = "Init 🚀"
c = ("*github.com/fatih/color.Color")(0x140001e49e0)
underlineLength = 80
(dlv) p underlineLength
```
I can also use `args` to get the arguments passed into my function:
```
(dlv) args
cl = github.com/earthly/earthly/conslogging.ConsoleLogger {prefix: "", metadataMode: false, isLocal: false,...+14 more}
phase = "Init 🚀"
disabled = false
special = ""
```

I can do many things from this point, including saving a checkpoint, that lets me return to this point of execution later, but for now I just want to modify `underlineLength` and see how that changes the execution. I can do this using `set` and print `p`.

```
(dlv) set underlineLength = 5
(dlv) p underlineLength
5
```
I can then use use next (`n`) to step through the code and continue (`c`) to continue execution and see my new shortened underline. `c` works just like you'd expect continue to work, it continues the execution until another break point is hit.

```
(dlv) c
Init 🚀
-----
```
That `----` is my much shortened underscore line, but the problem is this function gets called in a loop and so I quickly end up back at my breakpoint again.

```
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
```

I can keep mashing `c` until I get past this, or clear my breakpoint with `clear`:

```
breakpoints
Breakpoint runtime-fatal-throw (enabled) at 0x1048551ac,0x10483e3c0,0x10483e480 for (multiple functions)() <multiple locations>:0 (0)
Breakpoint unrecovered-panic (enabled) at 0x10483e750 for runtime.fatalpanic() /opt/homebrew/Cellar/go/1.21.1/libexec/src/runtime/panic.go:1188 (0)
        print runtime.curg._panic.arg
Breakpoint 1 (enabled) at 0x1050c4e44 for github.com/earthly/earthly/conslogging.ConsoleLogger.PrintPhaseHeader() ./conslogging/conslogging.go:230 (1)
```
My breakpoint is breakpoint 1, so i can clear it and continue:
```
(dlv) clear 1
(dlv) continue

```

Side Note: Breakpoint `runtime-fatal-throw` and `unrecovered-panic` do exactly what they sound like. Delve includes breakpoints on these critical failure points for ease of debugging a fatal runtime throw or an unrecovered panic.


With the breakpoint cleared, Earthly now runs to completetion.

```
Process 91365 has exited with status 0
Process 91365 has exited with status 0
(dlv) 
```

From that point, I can restart to rerun the same process with the same arguments or quit. And that is quick tutorial on `dlv`.

## Quick Tips

For all the in and outs of dlv checkout [the docs](https://github.com/go-delve/delve), but here is some quick tips. 


| **Task**                 | **Go Command**          | **Delve Command**          |
|--------------------------|-------------------------|----------------------------|
| **Run Program**          | `go run main.go`        | `dlv debug`                |
| **Run Tests**            | `go test`               | `dlv test`                 |
| **Compile and Run Executable** | `go build -o myapp && ./myapp` | `dlv exec ./myapp`       |
| **Run Specific Test**    | `go test -run TestName` | `dlv test -- -test.run TestName` |
| **Benchmark Tests**      | `go test -bench=.`      | `dlv test -- -test.bench=.` |
| **Install Package**      | `go install ./...`      | Not directly applicable with Delve, as Delve does not perform installations. |

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

Delve can be run headless, `--headless` , and then connected to remotely. This can be useful in a docker container where the trick is to install dlv and then run it and opne the correct port:

```
FROM golang:1.18

RUN go install github.com/go-delve/delve/cmd/dlv@latest

COPY myapp  .
EXPOSE 40000

# Command to run Delve server
CMD ["dlv", "--listen=:40000", "--headless=true", "--api-version=2", "--accept-multiclient", "exec", "./myapp"]
```

Your app needs to be built with debug capabilities and overcourse you might want to use Earthy to do this building and containerizing. Here is an Earthfile for building the app with debug symbols and building the debug container:

```
VERSION 0.6
FROM golang:1.18

build-debug:
    WORKDIR /myapp
    COPY ./src .
    RUN go build -gcflags="all=-N -l" -o /myapp/myapp .
    SAVE ARTIFACT /myapp/myapp build/myapp

containerize:
    FROM golang:1.18
    # Install Delve in the containerization stage as well, in case it's needed
    RUN go install github.com/go-delve/delve/cmd/dlv@latest
    # Copy the built app from the previous stage
    COPY +build-debug/myapp /myapp/myapp
    WORKDIR /myapp
    EXPOSE 40000
    CMD ["dlv", "--listen=:40000", "--headless=true", "--api-version=2", "--accept-multiclient", "exec", "/myapp/myapp"]
    SAVE IMAGE myapp-debug
```

Then you can debug like this:

```
docker build -t myapp-debug .
docker run -d -p 40000:40000 myapp-debug
dlv connect localhost:40000

```

Check out [github](https://github.com/go-delve/delve) for more information on `dlv`, including tracepoints and checkpoints which are valuable tools that deserver their own write up. 

{% include_html cta/bottom-cta.html %}
