---
title: "Building A Terminal User Interface With Golang"
toc: true
author: Josh

internal-links:
 - terminal user interface
 - tui
topic: go
excerpt: |
    Learn how to build a terminal user interface (TUI) using Golang with the help of the Tview library. This tutorial covers the basics of creating a TUI, including widgets, forms, lists, and layouts, and provides a step-by-step guide to building a simple rolodex app.
last_modified_at: 2023-07-11
categories:
  - golang
---
**This article explains how to create Text-based User Interfaces (TUIs) using Go. Earthly guarantees fast and dependable builds for your Go TUIs. [Learn more about Earthly](https://cloud.earthly.dev/login).**

<script zoom="2" id="asciicast-2UWD3NMXowmPCfTlwYjyFDJSF" src="https://asciinema.org/a/2UWD3NMXowmPCfTlwYjyFDJSF.js" async data-loop="true"  data-fit="none" data-autoplay="true" data-speed="2" data-size="small" data-start-at=04 ></script>

Did you know it's actually possible to build a rich UI that runs completely in the terminal? Programs like [htop](https://htop.dev/) and [tmux](https://github.com/tmux/tmux) use a terminal user interface (TUI) because they are often run on servers that don't have access to a GUI. Many developer tools also a TUI since developers spend so much time in the terminal anyway. There are even a number of [games](https://www.tecmint.com/best-linux-terminal-console-games/) that run entirely in the terminal. In this article we'll use the Go programing language to create our own TUI.

I first became interested in terminal user interfaces when I started using [K9s](https://github.com/derailed/k9s) to help manage multiple Kubernetes clusters. K9s runs entirely in the terminal and has a robust set of features and commands. It allows you to manage multiple clusters by displaying pods and nodes in an interactive real time table view. It also gives you the ability to run `kubectl` commands with the click of a button.

There are a handful of [different packages](https://appliedgo.net/tui/) to help you create a TUI in Go, and they all offer different advantages. But since K9s is what led me here, I decided to do a deeper dive into the library they use which is called [Tview](https://github.com/rivo/tview).

In addition to having a strong project behind it, the documentation for `Tview` is pretty good, and there are a decent number of other example projects linked in their github repo, so it was relatively easy to get something up and running quickly.

In this post I want to highlight some of `Tview`'s core functionality. In order to keep the focus on `Tview` and its features, we'll build a very simple app for storing and displaying contacts. Basically a terminal based rolodex. [All the code is up on Github](https://github.com/jalletto/tui-go-example).

## Widgets

`Tview` is built on top of another Go package called [`tcell`](https://github.com/gdamore/tcell). `Tcell` provides an api for interacting with the terminal in Go. `Tview` builds on top of it by offering some pre-built components it calls [widgets](https://pkg.go.dev/github.com/rivo/tview#hdr-Widgets). These widgets help you create common UI elements like lists, forms, dropdown menus, and tables. It also includes tools to help you build layouts with grids, flexboxes, and multiple pages.

## Installing Tview

To install `tview` run `go get github.com/rivo/tview` and then you can import both `tview` and `tcell` in your `main.go` file.

~~~{.go caption="main.go"}
import (
    "github.com/gdamore/tcell/v2"
    "github.com/rivo/tview"
)

~~~

Next, we'll create a `struct` to hold our contact info and a `slice` to hold multiple contacts.

~~~{.go caption="main.go"}
type Contact struct {
    firstName   string
    lastName    string
    email       string
    phoneNumber string
    state       string
    business    bool
}

var contacts []Contact
~~~

## Creating an App

The first `tview` widget we'll talk about is the `Application`. This is the top level node of our app.

~~~{.go caption="main.go"}
var app = tview.NewApplication()

func main() {
    if err := app.SetRoot(tview.NewBox(), true).EnableMouse(true).Run(); err != nil {
        panic(err)
    }
}
~~~

After creating a new app, we call a series of set up methods including enabling mouse detection and issuing a `Run` command. The `SetRoot` function tells the `tview` app which widget to display when the application starts. In this case we've chosen to use a [`Box`](https://pkg.go.dev/github.com/rivo/tview#Box) widget. Boxes are the parent type of all other widgets. They can do nothing but exist, which is fine for now.

Run this code and marvel at the blank black nothing that fills your terminal screen. You can end the program by pressing `ctrl+c`. Not super exciting, but it's a start. We've created an app, but we haven't told it to display anything or to respond to any key presses.

## Adding Text

Let's get rid of that blank box and replace it with a new widget called a [`TextView`](https://pkg.go.dev/github.com/rivo/tview#TextView).

~~~{.go caption="main.go"}
var app = tview.NewApplication()
var text = tview.NewTextView().
    SetTextColor(tcell.ColorGreen).
    SetText("(q) to quit")

func main() {

    if err := app.SetRoot(text, true).EnableMouse(true).Run(); err != nil {
        panic(err)
    }
}
~~~

Notice that after we created our new `TextView` we use it to replace the blank box as the application root. Now run the code and behold: TEXT! The only problem is that our app is now lying to us because you can press `q` all day and nothing is going to happen. Press `ctrl-c` to quit for now and lets see if we can make an honest app out of this thing.

![Our first step: text]({{site.images}}{{page.slug}}/text.png)

## Responding To Input

`Tview` allows us to respond to all sorts of events that are happening in the terminal, including mouse clicks, on focus actions, and yes, key presses. Let's set up our app to quit when a user presses `q`.

~~~{.go caption="main.go"}
app.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
    if event.Rune() == 113 {
        app.Stop()
    }
    return event
})
~~~

`SetInputCapture` takes a function as an argument. That function gets passed an `EventKey` type. This type holds information about the key press event. In this case, we can access the `ascii` code for the key by calling `Rune()`. If the key pressed is `q` then we call `Stop()` which will quit the application. Run the code again, press `q` and the application should quit.

## Capturing Data With Forms

Now that we can respond to input, let's give the user the ability to create a new contact by providing them with a form to fill out. `Tview` makes creating a [form](https://pkg.go.dev/github.com/rivo/tview#Form) super simple.

~~~{.go caption="main.go"}
var form = tview.NewForm()
~~~

And then, for reasons that will become clearer in a moment, we will create a function that populates the form with input fields.

~~~{.go caption="main.go"}
func addContactForm() {
    contact := Contact{}

    form.AddInputField("First Name", "", 20, nil, func(firstName string) {
        contact.firstName = firstName
    })

    form.AddInputField("Last Name", "", 20, nil, func(lastName string) {
        contact.lastName = lastName
    })

    form.AddInputField("Email", "", 20, nil, func(email string) {
        contact.email = email
    })

    form.AddInputField("Phone", "", 20, nil, func(phone string) {
        contact.phoneNumber = phone
    })

    // states is a slice of state abbreviations. Code is in the repo. 
    form.AddDropDown("State", states, 0, func(state string, index int) {
        contact.state = state
    })

    form.AddCheckbox("Business", false, func(business bool) {
        contact.business = business
    })

    form.AddButton("Save", func() {
        contacts = append(contacts, contact)
    })
}
~~~

The code here is pretty straight forward. We can call a series of functions to add input items to the form. I tried to show off a few of the options available, but [these are not all of them](https://pkg.go.dev/github.com/rivo/tview#Form.AddPasswordField). (The `states` variable that we are passing the drop down is just a [slice of state abbreviations](https://github.com/jalletto/tui-go-example/blob/main/main.go#L8). I didn't add the code here to save some space but it's available in the repo.)

Each of these functions takes a few inputs depending on the type of input field you're adding. All of them take a label as the first argument and then a `changed` function as the last argument. The `changed` function gets called whenever the input item changes. In this case we will use them to set the data for our contact.

The last thing we add is a button which we label `Save` and then pass it a function that will execute when the button is pressed.

Now we can update our app to listen for a new button press and then call our `addContactForm` function.

~~~{.go caption="main.go"}
app.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
    if event.Rune() == 113 {
        app.Stop()
    } else if event.Rune() == 97 {
        addContactForm()
    }
    return event
})
~~~

We can also update our text view with the info about the new command.

~~~{.go caption="main.go"}
var text = tview.NewTextView().
    SetTextColor(tcell.ColorGreen).
   SetText("(a) to add a new contact \n(q) to quit")
~~~

Now if you run the application and press `a`...nothing happens. This is because we need to tell our `app` about our new form and give it a way to switch from the `TextView` to the `Form`.

### Pages

When we originally started the app up we fed it a widget to use as its root, in this case a `TextView` which we set the variable `text`: `app.SetRoot(text, true)`. Because the app is using the `TextView` widget as its main primitive, anything we want to show on the screen needs to be attached to it. Or, we need to reset the app root, which is possible, but `Tview` offers a special widget called [`Pages`](https://pkg.go.dev/github.com/rivo/tview#Pages) to allow us to switch more easily between different views like pages on a website. Let's refactor our code to uses a `Pages` widget.

~~~{.go caption="main.go"}
var pages = tview.NewPages()
~~~

And then down in our main function we can use it as the root.

~~~{.go caption="main.go"}
 if err := app.SetRoot(pages, true).EnableMouse(true).Run(); err != nil {
  panic(err)
 }
~~~

Now we can create a page for our `Form` and a page for our `TextView` and switch between them easily. In the main function add the following code.

~~~{.go caption="main.go"}
pages.AddPage("Menu", text, true, true)
pages.AddPage("Add Contact", form, true, false)
~~~

Then we can update our if statement to switch to the form page when the user presses 'a'.

~~~{.go caption="main.go"}
 app.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
    if event.Rune() == 113 {
        app.Stop()
    } else if event.Rune() == 97 {
        addContactForm()
        pages.SwitchToPage("Add Contact")
    }
    return event
 })
~~~

And lastly, in our `addContactForm` function, we can update our save button to bring us back to the menu after the form is filled out.

~~~{.go caption="main.go"}
form.AddButton("Save", func() {
    contacts = append(contacts, contact)
    pages.SwitchToPage("Menu")
})
~~~

Now if you run the code and press `a` you should see the form show up.

![A simple form]({{site.images}}{{page.slug}}/form.png)

Take a second to fill it out and then click save. You should be taken back to the main menu and our contact will have been saved to `contacts` slice we set up earlier. Only problem now is we can't see any of our contacts.

<div class="notice--info">

### What About Q and A?

You may notice that pressing q still quits. Not great if your contact's name is Quincy Quigley. Don't worry, we'll fix this a little bit later.

</div>

## Lists

Let's create a [`List`](https://pkg.go.dev/github.com/rivo/tview#List) widget to display our contacts.

~~~{.go caption="main.go"}
var contactsList = tview.NewList().ShowSecondaryText(false)
~~~

And then, similar to what we did with our form, we can create a function that adds items to the list.

~~~{.go caption="main.go"}
func addContactList() {
    for index, contact := range contacts {
        contactsList.AddItem(contact.firstName + " " + contact.lastName, nil, rune(49+index), nil)
    }
}
~~~

When we add an item to a list we first pass a string. This is the main text that will be displayed. There is also an option for a secondary text that will appear below the main text, but we've turned this option off so we can get away with just passing an empty string.

Next, we can pass a [`rune`](https://www.geeksforgeeks.org/rune-in-golang/) which is what will show up next to each item. In this case we want numbers `1..n`, so we can take advantage of the index to do that. (49 is the [ascii code](https://www.ascii-code.com/) for the number 1)

This is a good start, but as we learned earlier, we won't be able to see our list until we give our app a way to display it. We could add a new page for our list, but we want to be able to display the `List` and the `TextView` that's displaying our menu options on the same page.

### Flexbox Layout

![Our finished app will display multiple widgets on a single page.]({{site.images}}{{page.slug}}/finished_app.png)

`Tview` gives us a couple options for layouts. The first is a [grid](https://pkg.go.dev/github.com/rivo/tview#Grid) system that allows you to set fixed sizes for rows and columns. The second, and the one we'll use here, is [Flexbox](https://pkg.go.dev/github.com/rivo/tview#Flex). `Flex` lets you create layouts by organizing widgets into rows or columns. We can also nest `flexboxes` to create more complex layouts.

Start by creating a new flex widget.

~~~{.go caption="main.go"}
var flex = tview.NewFlex()
~~~

By default, `flexbox` puts widgets next to each other in columns starting from left to right. For example, let's add three empty boxes to our flex.

~~~{.go caption=""}
flex.AddItem(tview.NewBox().SetBorder(true), 0, 1, false).
    AddItem(tview.NewBox().SetBorder(true), 0, 1, false).
    AddItem(tview.NewBox().SetBorder(true), 0, 1, false)
~~~

![In this case all the boxes are equal size]({{site.images}}{{page.slug}}/flex_box_one.png)

We can set the proportion of each box by setting the third argument in `AddItem`.

~~~{.go caption=""}
flex.AddItem(tview.NewBox().SetBorder(true), 0, 1, false).
    AddItem(tview.NewBox().SetBorder(true), 0, 4, false).
    AddItem(tview.NewBox().SetBorder(true), 0, 1, false)
~~~

![Setting the middle box to 4 makes it 4 times as big as the others. ]({{site.images}}{{page.slug}}/flex_box_two.png)

If we don't want columns, we can tell flex to use rows instead.

~~~{.go caption=">_"}
 flex.SetDirection(tview.FlexRow).
        AddItem(tview.NewBox().SetBorder(true), 0, 1, false).
        AddItem(tview.NewBox().SetBorder(true), 0, 4, false).
        AddItem(tview.NewBox().SetBorder(true), 0, 1, false)
~~~

![Stack widgets with the rows option.]({{site.images}}{{page.slug}}/flex_box_rows.png)

For now we just want to put our `List` on top of our `TextView`, which means we could use a single `Flex` with rows. But later we'll want to add another widget next to our `List`, which will require nesting a `Flex` with columns into a `Flex` with rows.

~~~{.go caption="main.go}
flex.SetDirection(tview.FlexRow).
    AddItem(tview.NewFlex().
        AddItem(contactsList, 0, 1, true).
    AddItem(text, 0, 1, false)
~~~

Let's also update our `SetInputCapture` function. We can actually call this function on any `tview` widget. The function only gets called if the widget we attach it to has focus. Since the `app` is the parent of all widgets, it always has focus. By moving the `SetInputCapture` off of the `app` and onto the `flexbox` we are ensuring that when our form page has focus, users can use the `q` and `a` buttons without triggering a quit or new form action.

~~~{.go caption="main.go"}
flex.SetInputCapture(func(event *tcell.EventKey) *tcell.EventKey {
    if event.Rune() == 113 {
        app.Stop()
    } else if event.Rune() == 97 {
        addContactForm()
        pages.SwitchToPage("Add Contact")
    }
    return event
})
~~~

Now, if you run the code and use the form to add a contact, you should be brought back to the menu and see a list displaying the first and last name of the contact you just added.

Add a few more contacts and you'll notice we have two bugs. Each time we go back to the form page, an additional form gets added.

![Not very formidable for the user]({{site.images}}{{page.slug}}/too_many_forms.png)

Also, when we get brought back to our contacts list, we see that names are being repeated.

## Refreshing

Both of these issues have the same cause. Each time we switch to a page we are adding on to the existing page rather than recreating the page with the new updates. We can fix this pretty easily by clearing the widgets each time we change pages.

~~~{.go caption="main.go"}
} else if event.Rune() == 97 {
    form.Clear(true)
    addContactForm()
    pages.SwitchToPage("Add Contact")
}
~~~

~~~{.go caption="main.go"}
func addContactList() {
    contactsList.Clear()
    for index, contact := range contacts {
        contactsList.AddItem(contact.firstName+" "+contact.lastName, " ", rune(49+index), nil)
    }
}
~~~

Now you should be able to add multiple contacts without seeing duplicates and without doubling up on forms.

### Showing Contact Info

When we select a contact from the list we want to be able to view their information. We'll display it in a text box to the right of our list. First, let's add the new text box.

~~~{.go caption="main.go"}
var contactText = tview.NewTextView()
~~~

We can tell our list to run a function each time an item on it is selected.

~~~{.go caption="main.go"}
contactsList.SetSelectedFunc(func(index int, name string, second_name string, shortcut rune) {
    setConcatText(&contacts[index])
})
~~~

We'll use it to pass the selected contact to a new function that sets the text of our `contactText` `TextView`.

~~~{.go caption="main.go"}
func setConcatText(contact *Contact) {
    contactText.Clear()
    text := contact.firstName + " " + contact.lastName + "\n" + contact.email + "\n" + contact.phoneNumber
    contactText.SetText(text)
}
~~~

We use the same process here of first clearing the widget and then rewriting the content.

The last step is adding our new textbox to the layout.

~~~{.go caption="main.go"}
flex.SetDirection(tview.FlexRow).
    AddItem(tview.NewFlex().
        AddItem(contactsList, 0, 1, true).
        AddItem(contactText, 0, 4, false), 0, 6, false).
    AddItem(text, 0, 1, false)
~~~

Now if we run our code, we can add contacts. Then when we select them from the list we can see the details appear to the right.

<script id="asciicast-2UWD3NMXowmPCfTlwYjyFDJSF" src="https://asciinema.org/a/2UWD3NMXowmPCfTlwYjyFDJSF.js" async data-loop="true"  data-fit="none" data-autoplay="true" data-speed="2" data-size="big" data-start-at=04 ></script>

## Conclusion

We've barely scratched the surface of what's possible with `Tview`. There's a lot more we could do with [styles](https://pkg.go.dev/github.com/rivo/tview#hdr-Styles) and [layouts](https://pkg.go.dev/github.com/rivo/tview#Table). One big problem with our app is that it's not persisting any data. For something simple like this we could get away with [writing to a csv file](https://golangdocs.com/reading-and-writing-csv-files-in-golang), but for larger apps, you might want to checkout this [`tview` example with postgres](https://github.com/rivo/tview/wiki/Postgres).

TUIs will never be able to compare to a full Graphical User Interface, but for certain applications they can provide more options than you might think. They're particularly great for applications developers use frequently since not having to leave the terminal can be a plus, and sometimes you might be on a server that doesn't have access to a GUI at all.

I'm definitely sold on them and will be looking for more opportunities to build them in the future. If you know of any cool TUI apps or libraries, please let me know.

Also, if you're the type of person who's liked building a TUI in Go then you might like [Earthly](https://cloud.earthly.dev/login/):

{% include_html cta/bottom-cta.html %}
