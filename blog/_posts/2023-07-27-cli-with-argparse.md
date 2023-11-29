---
title: "Building a CLI Application With Argparse"
categories:
  - Tutorials
toc: true
author: Kabaki Antony
editor: Ubaydah Abdulwasiu

internal-links:
 - building a cli application
 - cli application
 - building a with argparse
 - application
 - command line interface
excerpt: |
    This tutorial explores how to build a Command-Line Interface (CLI) application using the `argparse` module in Python. It covers topics such as defining and parsing command-line arguments, error handling, help messages, choices in command-line arguments, and advanced features like sorting and filtering tasks.
last_modified_at: 2023-08-28
---
**This article teaches you to master the `argparse` module for Python command-line interfaces. Earthly simplifies and accelerates build and test cycles for Python CLI projects. Visit Earthly's homepage.**

A Command-Line Interface (CLI) is a method of interacting with a computer program by entering text commands. It provides a way of controlling programs, executing tasks, and manipulating system resources through a terminal or command prompt. To build programs that accept input through the command line, the Python library offers the `argparse` module. The module simplifies the process of building command-line interfaces by providing the functionality to define command-line arguments, parse arguments, validate user input, and generate help messages.

In this tutorial, let's explore using the `argparse` module by building a ToDo application that will be operated through the Command-Line. This project will serve as an example to introduce the various concepts of `argparse` and demonstrate their practical use. Therefore, throughout the tutorial, we will build the application incrementally while exploring the different features of the `argparse` module.
The ToDo application will allow users to manage tasks by providing commands to add tasks, view the task list, mark tasks as done, and delete tasks.

## Setting Up the Environment

![Environment]({{site.images}}{{page.slug}}/environment.png)\

Setting up the environment for the ToDo CLI project will involve getting some things ready. Let's look at what you will need:
The first thing you need is to have Python installed. If you don't have Python installed on your system, [download](https://www.python.org/downloads/) it and select the Python version appropriate for your operating system.
The next thing you need to do is create the project directory; You can create the directory in your integrated development environment (IDE), or you can create it on the terminal using the following command:

~~~{.bash caption=">_"}
mkdir todo_cli
~~~

This will create a new directory named `todo_cli`.
With the project directory created, set up a virtual environment. A virtual environment is an isolated Python environment where you can install packages for a given project without affecting the global Python installation.
To create a virtual environment, you will use the `virtualenv` package. This package, however, does not come with the standard Python library; you have to install it. To do that, you will use the following command:

~~~{.bash caption=">_"}
pip install virtualenv
~~~

Once the package has been installed, create a virtual environment in the `todo_cli` project directory. You can create a virtual environment using the following command:

~~~{.bash caption=">_"}
virtualenv myenv
~~~

The above command will create a virtual environment called `myenv`. To use the virtual environment, you need to activate it. To activate the virtual environment, use the following command on **Linux** or **macOS**:

~~~{.bash caption=">_"}
. myenv/bin/activate
~~~

If you are using a **Windows** operating system, you can activate the environment using the following command:

~~~{.bash caption=">_"}
. myenv\Scripts\activate
~~~

Once the virtual environment has been activated, create the Python module that will hold the CLI application. For simplicity, call it `todo_cli.py`. To create the module, you can use your preferred IDE and create a new file, or you could create it on the terminal on **Linux** or **macOS** using the following command:

~~~{.bash caption=">_"}
touch todo_cli.py
~~~

The above command will create a file named `todo_cli.py`. With the environment ready, you are going to have an application structure similar to the one below:

~~~{ caption=""}
todo_cli/
├── myenv/  # Virtual environment directory
├── todo_cli.py  # Main Python module for the CLI application
~~~

Now that you have set up the basic environment and file structure, you can start building the ToDo CLI application in the `todo_cli.py` module using the `argparse` module.

## Building the ToDo CLI Application

To learn how to use the `argparse` module, you will start by building an application that accepts just one command line option named `task`, whose value will be the description of the task to be added to a task list.
`argparse` is a standard Python module, so you don't need to install it separately. It comes bundled with Python and should be available for use on import.

Let's start by importing the `argparse` module; doing this will provide the various methods you will use for handling and parsing command line arguments.

~~~{.python caption="todo_cli.py"}
import argparse
~~~

Go ahead and define a `main` function that will be the entry point of your application. The function will define an empty list named `tasks`; it will hold tasks as they get added from the command line.

~~~{.python caption="todo_cli.py"}
def main():
    tasks = []
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="+")
    args = parser.parse_args()
    print(args)

if __name__ == "__main__":
    main()
~~~

To use `argparse`, you create a parser object using the `ArgumentParser()` method.

~~~{.python caption="todo_cli.py"}
parser = argparse.ArgumentParser()
~~~

Once you have a parser object, you then go ahead and add arguments to it using the `add_argument` method and configure their behavior. In this example, you will define a positional argument called `task`.

~~~{.python caption="todo_cli.py"}
parser.add_argument("task")
~~~

After adding arguments to the parser object, the program will require the user to provide some information on the command line. To get the value the user supplied, you will use the `parse_args()` method of the `ArgumentParser` object. The parsed arguments are stored in a namespace object, an instance of the `argparse.Namespace` class. The namespace object acts as a container for the values assigned to arguments.

~~~{.python caption="todo_cli.py"}
args = parser.parse_args()
~~~

Let's throw a print statement in the code and look at what we have so far.

~~~{.python caption="todo_cli.py"}
print(args)
~~~

To ensure that the main function is called when this module is run, you add the `if __name__ == "__main__":` check.

~~~{.python caption="todo_cli.py"}
if __name__ == "__main__":
    main()
~~~

Run the application and provide a task, enclosing it with quotation marks `""`

~~~{.bash caption=">_"}
python todo_cli.py "clean the house"
~~~

This will return a namespace object, showing the name of the positional argument you defined, and its value enclosed in a string, to get the value for further processing, use the dot notation, `args.task`.

~~~{ caption="Output"}
Namespace(task="clean the house")
~~~

To add tasks to the list, define the 'add_task' function; the main function will call it each time you want to add a new task.

~~~{.python caption="todo_cli.py"}
def add_task(args, tasks):
    task = args.task
    task_id = len(tasks) + 1

    new_task = {
        'id':task_id,
        'task': task
    }

    tasks.append(new_task)

    print(f"Added task: {task}")
~~~

The function will take two arguments, `args` and `tasks`. Using the dot notation, you will extract the description of the `task` from the `args` namespace object.

~~~{.python caption="todo_cli.py"}
task = args.task
~~~

To create an ID for the new task, you will first check the length of your current task list and increment it by one.

~~~{.python caption="todo_cli.py"}
task_id = len(tasks) + 1
~~~

Once you have the task and generate an id, you will create a dictionary named `new_task`, which will hold key-value pairs of the task.

~~~{.python caption="todo_cli.py"}
 new_task = {
        'id':task_id,
        'task': task
    }
~~~

Then append the new task to the `tasks` list and print a message with the task that has been added to the list.

~~~{.python caption="todo_cli.py"}
tasks.append(new_task)

print(f"Added task: {task}")
~~~

The `if` check confirms whether the user has supplied any tasks on the command line and calls the `add_task()` function.

~~~{.python caption="todo_cli.py"}
if args.task:
     add_task(args, tasks)
~~~

Let's run the application and supply a task:

~~~{.bash caption=">_"}
python todo_cli.py  "Write an article on argparse"
~~~

This will add the task "Write an article on argparse" to the ToDo list and display the following confirmation message on the command line:

~~~{ caption="Output"}
Added task: Write an article on argparse
~~~

Overall, the simple application shows the primary usage of the `argparse` module in creating a command line interface. It takes the following steps; import the `argparse` module; create a parser object using the `ArgumentParser` method; then create a positional argument using the `add_argument` method of the parser object, parse the arguments using the `parse_args` method and store them in a namespace object, and finally to access the value of the positional argument, you use the dot notation that is  `namespace_object.name_of_your_positional_argument`

## Subparsers and Subcommands

![commands]({{site.images}}{{page.slug}}/command.png)\

The way the application is set up, you can only add one task to the list; however, in a ToDo application, there is a need to view tasks, mark tasks as done, or delete tasks. To fulfill those actions, you need to create a way for the user to specify what action they want to carry out in the application.

To solve this, `argparse` enables you to define subcommands, enhancing the application by splitting it into several sub-commands. This will require the user to specify the action they want to carry out on the command line. For instance, for a user to add a task, they will have to explicitly indicate on the command line that they wish to add a task using the `add` subcommand, then provide the task after the subcommand; for example, `add "this is my task"`, similarly, if the user wants to view tasks they will explicitly state that on the command line by running the application and providing the `view` subcommand. Therefore, you must explicitly indicate the command and its arguments if any to use subcommands.

Therefore, instead of just one action, you will create different subcommands denoting the actions one can carry out in your application. The subcommands will present the user with a way of executing other actions based on their chosen subcommand. So in the application, you will eventually have subcommands for `add`, `view`, `remove`, and `done`.  

To create subcommands in `argparse` you use subparsers; you first create a subparser object using the `add_subparsers` method of the main parser object.

Creating the main subparser object can take an optional parameter `dest`. This parameter is used to specify the name of the attribute where a selected subcommand will be stored. In this case, set it to "command", this attribute is very beneficial in an application with different subcommands. Instead of checking all the command-line arguments, you directly access the attribute and determine which subcommand you executed.

~~~{.python caption="todo_2_cli.py"}
import argparse

parser = argparse.ArgumentParser()
sub_parsers = parser.add_subparsers(dest="command")
~~~

Using the main subparser object, you can now create subcommands for the application. To create a subcommand you use the `add_parser` method of the main subparser object providing it with a string argument that denotes the name of the subcommand you are creating. However, if you want to configure the subcommand to give it positional or optional arguments, you must create a parser object and add arguments to its `add_argument` method.

The `add` subcommand takes in an argument describing the task you want to add to the list. You will add the argument to the `add` subcommand using the `add_parser.add_argument("task",metavar="task")`, and doing that defines a positional argument named "task"; hence it has to be supplied on the command-line after the `add` subcommand. Notice that it also has a `metavar` parameter with the value `task`; this specifies the name displayed for the argument in help and error messages.

~~~{.python caption="todo_2_cli.py"}
add_parser = sub_parsers.add_parser("add")
add_parser.add_argument("task", metavar="task") 

view_parser = sub_parsers.add_parser("view")
~~~

Creating the two subcommands extends the functionality of the application; however, to view the tasks, the application has to persist them in some way, and this is not possible with the list since it is recreated for each run of the program, so you have to persist the tasks somewhere you can retrieve them. For simplicity, you will persist them in a JSON file. Therefore, apart from `argparse`, you will also need to import the `json` module; This will provide the functions required to work with a JSON file. You will also create a constant (`TASKS_JSON` ) that will hold the JSON file's path.

~~~{.python caption="todo_2_cli.py"}
import json

TASKS_FILE = 'tasks.json'
~~~

To save tasks to the file, create the `save_task` function (it will take a tasks parameter). The function uses the `open` function to open the specified file ('TASKS_FILE') in write mode ('w'). Then, the `json.dump` function is used to write the tasks to the file in JSON format.

~~~{.python caption="todo_2_cli.py"}
def save_task(tasks):
    with open(TASKS_FILE, 'w') as file:
            json.dump(tasks, file)
~~~

To read the tasks from the file `read_tasks` function will open the `TASKS_FILE`  in read mode ('r') using the `open` function. It reads the file's contents using `json.load` function, which deserializes the JSON data from the file into a Python list. A `FileNotFoundError` will be raised if the file does not exist and an empty list is returned.

~~~{.python caption="todo_2_cli.py"}
def read_tasks():
    try:
        with open(TASKS_FILE, 'r') as file:
                tasks = json.load(file)
    except FileNotFoundError:
            tasks = []
    return tasks
~~~

You can now save and read data from the JSON file using the `read_tasks` and `save_task` functions. The `view` and `add` subcommands need supporting functions that will be called whenever a user specifies an action on the command line. Let's define the functions next.

The `add_task` function will be called when a user passes the `add` subcommand on the command line. It will take one parameter, the `args` namespace object. To read the tasks it will call the `read_tasks` function and the `save_tasks` function to save tasks to the file.

~~~{.python caption="todo_2_cli.py"}
def add_task(args):
    tasks = read_tasks()
    task = args.task
    task_id = len(tasks) + 1

    new_task = {
            'id':task_id,
            'task': task,
    }

    tasks.append(new_task)
    save_task(tasks)
    print(f"Added task: {task}")
~~~

The `view_tasks` function will be called when a user passes the `view` subcommand on the command line. It will read tasks from the file using the `read_tasks` function and save them on a list named `tasks`. Once you have the tasks, you can iterate through the list printing out individual tasks.

~~~{.python caption="todo_2_cli.py"}
def view_tasks():
    tasks = read_tasks()
    print("ToDo List:")
    for task in tasks:
            print(f"Task {task['id']}: {task['task']}")
~~~

Let's now run the script and provide the two subcommands, so you have to explicitly indicate the subcommand you want to use, and supply its arguments if any:

~~~{.bash caption=">_"}
python todo_2_cli.py add "Write an article on argparse"
~~~

Running the application with the `add` subcommand and giving it the `task` argument in the form of the string "Write an article on argparse", appends the task to the file, and if the file is not available, it is created. This will give you the following output, notifying you that everything worked correctly.

~~~{ caption="Output"}
Added task: Write an article on argparse
~~~

To view the tasks on the file, you will now run the application and supply the `view` subcommand this way:

~~~{.bash caption=">_"}
python todo_2_cli.py view
~~~

This will give you the following output:

~~~{ caption="Output"}
ToDo List:
Task 1: Write an article on argparse
~~~

By using subparsers, you can create subcommands for your application, tying each subcommand to a unique action on the application. This enhances the application by allowing users to take different actions depending on their subcommand.

## Error Handling and Help Messages

![Help]({{site.images}}{{page.slug}}/help.png)\

As you add more functionality to the application, you will expect that users will sometimes use invalid arguments or occasionally supply commands with missing arguments. Therefore, your application needs to handle errors and give helpful information showing users how to use the application and the commands available.

`argparse` provides built-in support for error handling and help messages. They are very beneficial since they help users understand how to use the application correctly and provide meaningful feedback when an error occurs.

By default, `argparse` generates help messages describing the available commands and arguments based on the parsers and arguments you define. However, on top of the default help messages provided by `argparse`, you can add your help messages as you create the commands. These help messages become the description of what the command does. Right now, the way you have set up the commands, they don't have any help messages. Let's look at how to add help messages to a command shortly.

To access help in `argparse`, you don't need to set up any commands; they are provided out of the box using the following options `-h` or `--help`. Therefore, to access the help message, you will need to run the application with either of the two flags.

~~~{.bash caption=">_"}
python todo_2_cli.py -h 
~~~

This will give an output similar to the one below:

~~~{ caption="Output"}
usage: todo_2_cli.py [-h] {add,view} ...
positional arguments:
  {add,view}
options:
  -h, --help  show this help message and exit
~~~

The help message shows that the application takes in one optional command, `-h`  for help, and two positional arguments, `add` and `view`. However, it could be more descriptive of what the commands do.
To add a help message to a subcommand, add a `help` parameter with a string of the help message as its value to the `add_parser` method of a sub_parser.
Let's see how by updating the application the following sections:

~~~{.python caption="todo_2_cli.py"}
# add task command
add_parser = sub_parsers.add_parser("add", \
help="Add a new task to the todo list")
add_parser.add_argument("task", metavar="task")

# view tasks command
sub_parsers.add_parser("view", help="Lists all the tasks in your todo list")
~~~

Now, if you try accessing help from the command line again, you will have a more informative help message.

~~~{.bash caption=">_"}
python todo_2_cli.py -h 
~~~

Output:

~~~{ caption="Output"}
usage: todo_2_cli.py [-h] {add,view} ...

positional arguments:
  {add,view}
    add       This adds a new task to the todo list
    view      This lists all the tasks in your todo list

options:
  -h, --help  show this help message and exit
~~~

The help messages now say what each command does in the application, and this is now more informative.

### Running the Application Incorrectly

So far, you have run the application and provided all the arguments needed correctly. If you run the application with the `add` subcommand and fail to provide the task, this will result in a missing arguments error, or if you run it with the `view` subcommand and provide some arguments, the application is going to throw some errors, just like the help messages. `argparse` provides error handling out of the box. So the two different scenarios will give an output showing what happened.

~~~{.bash caption=">_"}
python todo_2_cli.py add
~~~

In the above example, you have not provided the expected argument for the task that is to be added to your list, so the application is not going to work, and you will get an error message similar to the one below:

~~~{ caption="Output"}
usage: todo_2_cli.py add [-h] task
todo_2_cli.py add: error: the following arguments are required: task
~~~

Let's now run the application and supply the `view` command with an argument:

~~~{.bash caption=">_"}
python todo_2_cli.py view "test"
~~~

This will also fail since the `view` subcommand does not take any arguments, and it will give an output similar to the one below:

~~~{ caption="Output"}
usage: todo_2_cli.py [-h] {add,view} ...
todo_2_cli.py: error: unrecognized arguments: test
~~~

The two scenarios gave back error messages that are quite descriptive and informative, showing exactly what caused the error. Therefore, a user will be able to rectify what caused the error. This shows the ability of `argparse`  to handle errors and give help messages out of the box, making it a very powerful module for use in developing command-line applications.

## Choices in Command Line Arguments

More often than not, when a user writes down the tasks they want to do over a certain duration, they will want to classify the tasks in terms of their priority. There could be some that need to be carried out as soon as possible and some that don't have to be fulfilled immediately, and therefore, they will want this information captured as they save the tasks.
This introduces us to the concept of choices in command line arguments. `argparse` provides a way of adding `choices` to the optional or positional arguments.
In this application, you want to choose the priority of a task at the point when you are adding it to the list. This means that you will have to extend the functionality of the `add` subcommand. Sometimes you may not want to choose the priority of a task. You will use an optional argument to the `add` subcommand. So if a user wants to assign a certain priority to a task, they will use the `add` subcommand with the optional flag `--priority`, and then they can choose between the given choices, which in this case will be `["low", "medium", "high"]`.

Let's enhance the application to add choices to the `add` subcommand:
You will also need to change the task structure for these changes to work, so update the `add_task` function by adding a priority key-value pair to the `new_task` dictionary.

~~~{.python caption="todo_2_cli.py"}
def add_task(args):
    priority = args.priority
    task_id = len(tasks) + 1

    new_task = {
        'id': task_id,
        'task': task,
        'priority': priority,
    }
   
    print(f"Added task: {task} (Priority: {priority})")
~~~

To add an optional argument to the `add` subcommand, use the `add_argument` method. The difference between a positional argument and an optional argument is that positional arguments are required, and to show that an argument is optional, you mark it with a single dash (-) for a short option name, for example, `-p`, and a double dash (--) for the long option name `--priority`.
The optional arguments will also take a choice value indicating the priority level.

~~~{.python caption="todo_2_cli.py"}
def main():
    # add task command
    add_parser = sub_parsers.add_parser("add", 
    help="Add a new task to the todo list")
    add_parser.add_argument("task", metavar="task")
    add_parser.add_argument("-p","--priority", 
    choices=["low", "medium", "high"])
~~~

By utilizing choices in command-line arguments, you can enforce specific valid values for certain arguments and ensure that the user provides valid input based on the available choices. So if a user runs the script and provides the `add` command with the `--priority` argument, `argparse` will enforce that the value of `--priority` must be one of the specified choices. If the user provides an invalid value, `argparse` will raise an error and display the appropriate error message.
Here is an example of how you could use the `add` command with the `--priority` argument and supply one of the choices:

~~~{.bash caption=">_"}
python todo_2_cli.py add "Edit this article" –priority high
~~~

This will give the following output:

~~~{ caption="Output"}
Added task: edit this article (Priority: high)
~~~

Overall, using choices in our commands allows you to extend the functionality of your application, giving the user many ways to use it.

## Adding Advanced Command Line Arguments

Up to this point, the CLI only has the `add` and `view` commands and only takes commands and arguments as strings. Say you wanted to supply the ID of a task; you would need to provide arguments in integer form.
Using `argparse`, it is possible to specify the data `type` an argument of a command can take, enabling you to define more advanced commands that can accept different data types.
Update your application in the following code sections to add `mark` and `remove` subcommands that will take the ID of the task the user wishes to mark as done or remove from the list.
For the `mark` subcommand to work, start by updating the `new_task` dictionary; this will add a `done` entry that will hold the status of the task.

~~~{.python caption="todo_2_cli.py"}
def add_task(args):

    new_task = {
        'id':task_id,
        'task': task,
        'priority':priority,
        'done':False,
    }
~~~

Then create the `mark_task_done` function, it will be called when a user invokes the `mark` subcommand. This function will take an `args` object parameter. You will get the `task_id` from the parameter using the dot notation `task_id = args.task_id`. You will also get tasks and store them in a list, `tasks=read_tasks()`.
Once you have the `tasks` in a list, you can iterate through them and check if a task with an id equal to the one the user passed exists. If such a task exists, then you update the `done` status by marking it `True`, and if a task with a matching id is not found, you return a "Task not found" message to the user.

~~~{.python caption="todo_2_cli.py"}
def mark_task_done(args):
    tasks = read_tasks()
    task_id = args.task_id

    for task in tasks:
            if task['id'] == task_id:
            task['done'] = True
            save_task(tasks)
            print(f"Marked task {task_id} as done.")
            return
    print(f"Task {task_id} not found.")
~~~

To remove a task, create the `remove_task` function. Regarding functionality, it is similar to the `mark_task_done`; the only difference is that once you find the task with an id as supplied by the user. You will use the `remove` function of the list object by passing it the `task`. This will consequently remove the task, and after that, you will call the `save_tasks` function to save the new list.

~~~{.python caption="todo_2_cli.py"}
def remove_task(args):
    tasks = read_tasks()

    task_id = args.task_id

    for task in tasks:
        if task['id'] == task_id:
            tasks.remove(task)
            save_task(tasks)
            print(f"Removed task {task_id}.")
            return

    print(f"Task {task_id} not found.")
~~~

Adding the `mark` subcommand also calls for an update of the `view_tasks` function by slightly changing the print function format string to accommodate `Priority` and `Done` statuses.

~~~{.python caption="todo_2_cli.py"}
def view_tasks():
    tasks = read_tasks()
    print("ToDo List:")
    for task in tasks:
            print(f"Task {task['id']}: {task['task']}, \
            Priority:{task['priority']}, Done:{task['done']}")
~~~

Update the `main` function by ensuring that each new subcommand has its own sub-parser object (`mark_parser`, `remove_parser`) created using `sub_parsers.add_parser()`. The respective arguments (`task_id` in this case) are added to the sub-parser objects to capture the necessary input with the  `type` specified as `int`, clearly indicating that the value expected for the `task_id` is an integer. This update also includes the `help` string for each subcommand.

~~~{.python caption="todo_2_cli.py"}
def main():
    # Mark task as done command
    mark_parser = sub_parsers.add_parser("done", \
    help="Mark task as done")
    mark_parser.add_argument("task_id", type=int)

    # Remove task command
    remove_parser = sub_parsers.add_parser("remove", \
    help="Remove task from list")
    remove_parser.add_argument("task_id", type=int)    

    args = parser.parse_args()

    if args.command == "add":
            add_task(args)
    elif args.command == "view":
            view_tasks()
    elif args.command == "remove":
            remove_task(args)
    elif args.command == "done":
            mark_task_done(args)
~~~

Let's see an example of running the script with the remove command:

~~~{.bash caption=">_"}
python todo_2_cli.py remove 1
~~~

Output:

~~~{ caption="Output"}
Removed task 1.
~~~

That option removes the task with an ID of 1.
Overall, you can add various advanced commands to your CLI application, giving your users different ways of operating the application. Also, specifying the data type an argument expects helps ensure that the provided values are of the expected type, enabling better validation and reducing the risk of type-related errors in your command-line application.

## Enhancing the CLI Application

The Todo application is almost complete now, but you could add more functionality to make it more flexible for users. To do this, you could add options like due dates, sort tasks by their due dates, and filter them according to their priority. At the same time, you have already encountered the optional arguments in the choices in the command line arguments section.
This section will also extensively use the optional commands to give the application these advanced features like sorting and filtering.
Update your code in the following places to add sorting, filtering, and setting due dates on tasks:
Let's start by importing `datetime` to enable you to work with dates that you will use to indicate a todo `due_date`.

~~~{.python caption="todo_2_cli.py"}
from datetime import datetime
~~~

Update the `add_task` function to include a variable to get a due date; also update the `new_task` dictionary to add a `due_date` key-value pair.

~~~{.python caption="todo_2_cli.py"}
def add_task(args):
    
    due_date = args.due_date

    task_id = len(tasks) + 1

    new_task = {
        'id':task_id,
        'task': task,
        'priority':priority,
        'done':False,
        'due_date':due_date,
    }
~~~

To sort and filter tasks, update the `view_tasks` function since they are optional commands, the `if args.sort:` checks if the user provided the `--sort` option. If the option is present, the code block inside the `if` statement is executed.

~~~{.python caption="todo_2_cli.py"}
def view_tasks(args):
    tasks = read_tasks()

    if args.sort:
             tasks.sort(key=lambda task: task['due_date'])

    print("ToDo List:")
    for task in tasks:
             if args.filter:
                      if task['priority'] == args.filter:
                  print_task(task)
        else:
                  print_task(task)

~~~

Inside the `if` code block, `tasks.sort(key=lambda task: task['due_date'])` sorts the `tasks` list based on the value of the 'due_date' key in each task dictionary. The `sort` method is called on the `tasks` list, and the `key` parameter is set to a lambda function that extracts the 'due_date' value from each task dictionary. This lambda function serves as the sorting key, determining the basis for the sorting operation.

By providing the lambda function as the key parameter, the sort method can sort the tasks based on their 'due_date' values. This will result in ‌tasks being rearranged in ascending order based on their due dates.

~~~{.python caption="todo_2_cli.py"}
if args.sort:
            tasks.sort(key=lambda task: task['due_date'])
~~~

The `view_tasks` function will also filter tasks. If `args.filter` is not specified (i.e., it is `None` or empty), indicating no filtering is requested, the code block inside the `else` statement is executed. In this case, the `print_task` function is called for every task in the task list without filtering.

Overall, this code snippet allows filtering the tasks based on the `args.filter` value. Only ‌tasks with a matching 'priority' value will be displayed if a filter value is provided. If no filter value is provided, all tasks will be displayed.

~~~{.python caption="todo_2_cli.py"}
print("ToDo List:")
for task in tasks:
    if args.filter:
       if task['priority'] == args.filter:
            print_task(task)
    else:
            print_task(task)
~~~

Update the `print_task` function to print the tasks in a good format.

~~~{.python caption="todo_2_cli.py"}
def print_task(task):
        status= "Done" if task['done'] else "Not Done"
        due_date=task['due_date'] if task['due_date'] else "N/A"

        print(f"""
        Task {task['id']}: {task['task']},
        Priority:{task['priority']},
        Done:{status},
        Due Date: {due_date},
        """)
~~~

In the `main()` function, you will add the following options:
**Due Date**: An optional `--due-date` argument, enabling setting a due date for the task. You should provide the due date in the format "YYYY-MM-DD".
**Sorting**: Add a `--sort` option to the `view` subcommand. When this option is specified, the tasks will be sorted by their due dates in ascending order. The `--sort` option has no value.
**Filtering**: Add a `--filter` option to the `view` subcommand, which takes values from any of the following choices: "low", "medium", and "high". Only tasks with specified choices will be displayed when this option is specified.

~~~{.python caption="todo_2_cli.py"}
def main():
    #...
    
    # add task command
    add_parser = sub_parsers.add_parser("add", \
    help="Add a new task to the todo list")
    add_parser.add_argument("task", metavar="task", \
    help="Description of the task.")
    add_parser.add_argument("-p","--priority", \
    choices=["low","medium","high"], help="Choose the priority of a task")
    add_parser.add_argument("--due-date", help="Task due date (YYYY-MM-DD)")


    # view tasks command
    view_parser = sub_parsers.add_parser("view", \
    help="Lists all the tasks in your todo list")
    view_parser.add_argument("--sort", action="store_true", \
    help="Sort tasks by due date")
    view_parser.add_argument("--filter", \
    choices=["low", "medium", "high"], help="Filter tasks by priority")

    # Mark task as done command
    mark_parser = sub_parsers.add_parser("done", \
    help="Mark task as done")
    mark_parser.add_argument("task_id", type=int, \
    help="The ID of the task")

    # Remove task command
    remove_parser = sub_parsers.add_parser("remove", \
    help="Remove task from list")
    remove_parser.add_argument("task_id", type=int, \
    help="The ID of the task")   

    args = parser.parse_args()

    if args.command == "add":
            add_task(args)
    elif args.command == "view":
            view_tasks(args)
    elif args.command == "remove":
            remove_task(args)
    elif args.command == "done":
            mark_task_done(args)
~~~

The additional optional commands also have help messages; however, the help messages for optional arguments are not shown at the top level of the help command. To view them, specify the command and then the help option.

~~~{.bash caption=">_"}
python todo_2_cli.py add --help 
~~~

Output:

~~~{ caption="Output"}

usage: todo_2_cli.py add [-h] [-p {low,medium,high}] 
[--due-date DUE_DATE] task
positional arguments:
  task                  Description of the task.

options:
  -h, --help            show this help message and exit
  -p {low,medium,high}, --priority {low,medium,high}
                        Choose the priority of a task
  --due-date DUE_DATE   Task due date (YYYY-MM-DD)
~~~

The output shows the positional and optional arguments the `add` command takes and what each does.
These changes enhance your application, giving the user more commands, options, and different ways to work with them.

~~~{.bash caption=">_"}
python todo_2_cli.py add "submit this article" \
--priority high --due-date 2023-05-20
~~~

This will give the following confirmation message:

~~~{ caption="Output"}
Added task: submit this article (Priority: high)
~~~

Using the `view` command with the `--filter` option:

~~~{.bash caption=">_"}
python todo_2_cli.py view --filter medium
~~~

This option will not return anything since no tasks are marked as priority medium.
Those new features give the user more choice and versatility in the ToDo application. By combining positional arguments, subcommands, and optional arguments, you can create a rich application that users can interact with in many ways.

## Conclusion

In this article, we covered the essential aspects of using `argparse` in Python CLI applications. We began by introducing `argparse` and its basic usage, including defining and parsing command-line arguments. Then, we built a ToDo CLI application, gradually adding features such as task storage, advanced arguments, error handling, and help messages.

We explored advanced argument concepts like choices, enabling us to enforce valid values for arguments. By leveraging `argparse`, we enhanced our ToDo CLI with features like sorting, such as marking tasks as done and removing tasks.

You can find the code examples used in this tutorial [in this GitHub repository](https://github.com/KabakiAntony/cli_with_argparse_tutorial).

{% include_html cta/bottom-cta.html %}