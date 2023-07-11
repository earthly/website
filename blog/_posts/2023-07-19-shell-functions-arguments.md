---
title: "Learning Shell Script Functions and Arguments: A Comprehensive Guide"
categories:
  - Tutorials
toc: true
author: Aniket Bhattacharyea
editor: Ubaydah Abdulwasiu

internal-links:
 - learning shell script
 - shell script functions
 - functions and arguments
 - shell script functions and arguments
excerpt: Learn the fundamentals of shell scripting functions and arguments in this comprehensive guide. Discover how to create functions, pass arguments, use variables, and return values in Bash scripts, along with best practices for writing efficient and reusable code.
---

**We're [Earthly](https://earthly.dev/). We make building software simpler and, therefore, faster by using containerization. This article is about autotools and make. If you're interested in a different building and packaging software approach, then [check us out](/).**

When you think of automation, you might initially envision its application in physical implementations, such as Internet of Things (IoT) tools like lights and voice assistants. Or you may think of new AI automation tools or platforms like [Microsoft Flow](https://powerautomate.microsoft.com/en-us/blog/welcome-to-microsoft-flow/). But what if there was a closer, more versatile tool, and right at your very fingertips?

Bash is a known shell that is preinstalled with most Unix and Linux distributions. Bash makes it extremely easy to write powerful scripts that you can use to perform complex jobs, control hardware and software, and perform logical and analytical computations.

In this article, you'll explore the fundamentals of shell scripting functions and arguments. You'll see how they're used and learn how to create your own scripts. You may come across some more terminology than you typically encounter in a blog post, along with some simple scripts you can reproduce and run. So grab your keyboard, open up a terminal, and get started!

## Shell Script Functions

For decades, shell scripting, has been the go-to solution for automation on Unix and Linux systems. One of the key features of shell scripting is its ability to create functions and pass arguments to them. Creating functions in shell scripting has three key elements that are discussed here:

* A **function** is a block of code in a script that performs a specific task. The simplest scripts are composed of one function, but functions are often combined into scripts. Think of a script like a module; functions can break up a large script into smaller, more manageable parts. Or they can be used to perform a specific task multiple times throughout a script.
* An **argument** is a piece of information that you provide at some point during the software's execution. The software's actions or calculations then use the argument. Arguments are, therefore, changeable without any modification to the function or the software itself.
* A **parameter** is a placeholder for the value of an argument or other inputs. These values can be used within the function to perform specific tasks. **Positional parameters**, discussed later, have default designations from `$0` to `$9`.

In the next section, you'll look at how to work with functions and arguments in Bash.

### Creating Shell Script Functions and Arguments

Like any other programming language, functions in Bash must be defined before use. Defining a function in Bash uses the following syntax:

~~~{.bash caption=">_"}
function_name() {
    function_body
}
~~~

Or, equivalently

~~~{.bash caption=">_"}
function function_name() {
    function_body
}
~~~

Both syntaxes give the same result, which means you can use either without worrying about whether different syntaxes do different things.

Take a look at an example where you define a function named `greet`, which prints "Hello, Earthly" when run:

~~~{.bash caption=">_"}
greet() {
    echo "Hello, Earthly"
}
~~~

You can execute the function simply by typing its name:

~~~{.bash caption=">_"}
greet
~~~

This will output

~~~{ caption="Output"}
Hello, Earthly
~~~

You can also define a function that takes parameters:

~~~{.bash caption=">_"}
greet() {
    echo "Hello, $1"
}
~~~

And you can call it with arguments:

~~~{.bash caption=">_"}
greet "John"
~~~

This will output:

~~~{ caption="Output"}
Hello, John
~~~

You may have noticed two striking differences between functions in Bash and functions in other programming languages, such as C, Java, and Python:

1. When defining the function, you don't need to mention function parameters in the function signature.
2. When calling the function, you don't need to add parentheses to the function call.

What does this mean for you when working with function parameters? Well, rest easy, dear reader! That question will be answered soon, but you'll learn about variables inside functions before that.

![Easy]({{site.images}}{{page.slug}}/easy.png)\

### Using Variables in Functions

You might be tempted to define variables inside functions using the typical Bash syntax:

~~~{.bash caption=">_"}
oops() {
    my_var="I'm a variable"
    echo $my_var
}
~~~

This code works as you'd expect it to and outputs "I'm a variable". However, it also throws the `my_var` variable into the global scope, and `$my_var` can be accessed from outside the function:

~~~{.bash caption=">_"}
$ oops
I'm a variable
~~~

~~~{.bash caption=">_"}
$ echo $my_var
I'm a variable
~~~

This might seem innocent, but it can be problematic if you already have a variable in the global scope with the same name. The function may accidentally overwrite the global variable and cause bugs:

~~~{.bash caption=">_"}
my_bank_balance=1000

boom() {
    my_bank_balance=0
    echo "I stole your money"
}

Boom
echo $my_bank_balance
~~~

This will output:

~~~{ caption="Output"}
I stole your money
0
~~~

In this code, the `boom` function modifies the `my_bank_balance` variable from the global scope instead of defining a local variable named `my_bank_balance`.

To define a local variable, you must prefix the `local` keyword:

~~~{.bash caption=">_"}
my_bank_balance=1000

boom() {
    local my_bank_balance=0
    echo "I stole your money"
}

boom
echo $my_bank_balance
~~~

This outputs:

~~~{ caption="Output"}
I stole your money
1000
~~~

As you can see, the `my_bank_balance` variable is now intact. Using `local` creates a new variable local to the function, and the function can't access the global variable.

In the next section, you'll learn how to return a value from a function, a common pattern in other programming languages.

### Using the Return Value of a Function

Return values are tricky in Bash because, unlike other languages, you cannot return whatever you want. You must return a numeric value:

~~~{.bash caption=">_"}
foo() {
    return "Hi"
}

foo
~~~

In this code, the `foo` function returns `Hi`, which is not numeric, and the script fails with the error: `bash: return: Hi: numeric argument required`.

Although you're free to return any numeric value you want, by convention, it denotes the exit status of the function, where zero denotes a successful execution and a nonzero value denotes an error has occurred. This exit status is stored in the `$?` variable after the function executes:

~~~{.bash caption=">_"}
foo() {
    return 0
}
foo
echo $?
~~~

In this code, `foo` returns `0`. After executing `foo`, the return value is stored in `$?`, which will output `0`.

With this technique, you can use the return value of a function as a condition in an `if` statement or on the left-hand side of the short circuit operators (`&&` and `||`). Remember that an exit status of zero means successful execution:

~~~{.bash caption=">_"}
foo() {
    return 0
}

bar() {
    return 1
}

foo && echo "foo executed successfully"
bar && echo "bar executed successfully"
~~~

This code outputs "foo executed successfully". However, since `bar` returns a nonzero value, it's not classified as a successful execution. The same thing can also be written with an `if` statement:

~~~{.bash caption=">_"}
if foo
then
    echo "foo executed successfully"
fi

if bar
then
    echo "bar executed successfully"
fi
~~~

So now the question is: How do you return some nonnumerical value? The trick is to print to `stdout` whatever you want to return and then capture this output to a variable using `$()`:

~~~{.bash caption=">_"}
greet() {
    echo "Hello, Earthly"
}

output=$(greet)
echo "Output is: $output"
~~~

This code prints "Output is: Hello, Earthly", and the `greet` function outputs "Hello, Earthly". But instead of running `greet` normally and letting it print to `stdout`, the output is captured using `$()` and stored in the `output` variable.

Now that you know how to use variables in functions, it's time to learn how to deal with function arguments.

### Passing Arguments to Bash Functions

Like other programming languages, Bash functions can accept arguments. However, they're not mentioned in the definition, and Bash doesn't enforce the number of arguments. This means you can pass any number of arguments to any function without an error:

~~~{.bash caption=">_"}
foo() {
    echo "I don't accept arguments. Please don't pass any"
}

foo "Take an argument" # No error
~~~

To use the arguments inside the function body, you need to know the position of the argument. This is why these arguments are called positional parameters/arguments. You can access the first argument with `$1`, the second argument with `$2`, and so on:

~~~{.bash caption=">_"}
bar() {
    echo "First argument: $1"
    echo "Second argument: $2"
}
~~~

<div class="notice--info">
**Please note:** A space must separate the arguments. Additionally, you need to use double quotes if your argument contains a space:
</div>

~~~{.bash caption=">_"}
bar arg1 "Argument 2"
~~~

Output:

~~~{ caption="Output"}
First argument: arg1
Second argument: Argument 2
~~~

If you have more than nine arguments, something interesting occurs:

~~~{.bash caption=">_"}
foo() {
    echo $10
}

foo This is a lot of arguments what will happen now
~~~

Instead of outputting `now`, the tenth argument, this code prints `This0`. This is because `$10` is expanded as `($1)0` (*ie* the first argument followed by a `0`). To solve this, use `${}`:

~~~{.bash caption=">_"}
foo() {
    echo ${10}
}

foo This is a lot of arguments what will happen now
~~~

This outputs `now` as expected.

There are a few special variables available inside a function body. Take a quick look at them:

* The **`$#`** variable holds the number of arguments passed to the function:

~~~{.bash caption=">_"}
foo() {
    echo $#
}

foo 1 2 3
~~~

Here, three arguments are passed to `foo`, and the code outputs `3`.

* **`$*`** expands to list all positional arguments. When double-quoted, it expands to a string of all positional arguments separated by a space (or the first character of `$IFS`):

~~~{.bash caption=">_"}
count_args() {
    echo "$# arguments passed"
}

foo() {
    count_args "$*"
}

foo 1 2 3
~~~

This code snippet defines a `count-args` function that prints the number of arguments. Inside `foo`, the `count_args` function is called, and `"$*"` is passed as the argument. This code snippet outputs "1 arguments passed" since `"$*"` expands to a single string `"1 2 3"`.

* **`$@`** is similar to `$*`. When not double-quoted, they're the same. However, when you use double quotes, `$@` expands to a list of separate strings. Here's the previous example with `$@` in place of `$*`:

~~~{.bash caption=">_"}
count_args() {
    echo "$# arguments passed"
}

foo() {
    count_args "$@"
}

foo 1 2 3
~~~

Here, it outputs "3 arguments passed", as `$@` expands to `"1" "2" "3"`.

However, if you remove the double quotes, both `$*` and `$@` will expand to three arguments.

## Best Practices for Shell Script Functions and Arguments

![Best]({{site.images}}{{page.slug}}/best.png)\

Now that you're familiar with functions and arguments, this section covers some best practices that can enhance the readability of your scripts and make them more user-friendly for yourself and others. Some of these practices are essential, while others are recommended for convenience.

### Choose Descriptive Names for Functions and Arguments

When it comes to naming functions and arguments, there are certain guidelines you should keep in mind. The only nonnegotiable rule is that they can only contain letters and underscores. Beyond that, you're free to create any name you choose, but it's recommended that you pick something that makes sense and helps you identify the created function or argument. A name that consists of lowercase words linked by underscores is considered good practice.

For example, `MyVariable` works, but it's not particularly useful when troubleshooting or learning a new script. Instead, use a name such as `add_three_numbers`. This function name is descriptive, and the predictable pattern makes it easy to read.

Likewise, the argument `$FN` could be used, but `$first_name` is a simple way to communicate the expected value to the reader.

### Make Functions Single-Purpose

One advantage of breaking down a script into functions is its modularity and reusability. Functions can be designed to be independent, self-contained units, allowing them to be used in various contexts without additional dependencies. Once the function works as expected, the writer can integrate it into the script multiple times to provide the same utility.

To ensure your functions are modular and reusable, make them as single-purpose as possible. Consider the following script where the `setUpStudent` function creates a student, registers a student, and saves the student:

~~~{.bash caption=">_"}
setUpStudent() {
    # Create a student
    …
    # Register the student
    …
    # Save the student
    …
}
~~~

If, in a particular case, you need to save a student without registering it, you can't reuse the `setUpStudent` function. The better solution is to separate the different functions into single-purpose functions:

~~~{.bash caption=">_"}
createStudent() {
    …
}

registerStudent() {
    …
}

saveStudent() {
    …
}
~~~

### Create Function Libraries in Shell Scripts

You can create a [function library](https://bash.cyberciti.biz/guide/Shell_functions_library) to reuse functions between scripts. This library is a single file that stores the functions you want to make available between scripts. For example, if you wish to insert a library called "all_my_math_functions" (remember, descriptive names!), you must save the functions into a single file. Then you would insert the file into the beginning of the script with two dots and the library file name, like this:

~~~{.bash caption=">_"}
#!/bin/bash
. ./all_my_math_functions
~~~

### Insert Error Handling in Each Function

As you may have noticed, Bash is lax regarding what would be considered errors in other languages (*eg* passing the wrong number of arguments). This makes it necessary to handle errors in functions because Bash won't handle them for you. And there are many ways you can do this. For example, you can use a conditional statement to check for the correctness of arguments:

~~~{.bash caption=">_"}
foo() {
    if [ $# -ne 3 ]
    then
    echo "Error: Need 3 arguments"
    return 1
    fi

    echo "All good"
}

foo # Error: Need 3 arguments
foo 1 2 3 # All good
~~~

Here, the `$#` variable is checked before executing the rest of the function. The function exits if exactly three arguments are not passed.

Or you can use `set -e` to stop execution on the first error. The [most recommended option is to use `set -eou pipefail`](https://gist.github.com/vncsna/64825d5609c146e80de8b1fd623011ca).

Finally, always make use of the exit codes. Remember to use `0` for successful execution and a nonzero value to denote an error.

## Conclusion

Scripting can make your work more efficient, but there are practical considerations that you should keep in mind. When you write scripts, concentrate on utility and efficiency. Name scripts and variables descriptively and use conventions that make it easier for others (and yourself) to understand.

In this article, you learned about functions in Bash—how to define and use them, pass arguments, return values, and declare variables inside functions. You also learned about some best practices to implement when working with functions.

If you want to learn more about what you can do with scripting and the methodology behind it, check out these resources:

* [Bash error handling](https://linuxhint.com/bash_error_handling/)
* [Command line arguments in Bash scripts](https://www.baeldung.com/linux/use-command-line-arguments-in-bash-script)
* [Bash scripts and function libraries](https://medium.com/swlh/bash-scripts-part-6-functions-and-library-development-2411adbf962)

{% include_html cta/bottom-cta.html %}
