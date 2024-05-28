---
title: "Getting Started With PyTest Fixtures"
toc: true
author: Ashutosh Krishna
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Python
 - Pytest
 - Testing
 - Fixtures
excerpt: |
    Learn how to use PyTest fixtures to simplify your test setup and improve your testing. Fixtures provide a way to manage test data and resources, making it easier to set up, tear down, and share data between test functions. Discover the advantages of using PyTest fixtures and explore advanced topics such as cleaning up test data, parameterizing fixtures, and using `autouse` fixtures.
last_modified_at: 2023-07-19
categories:
  - Python
---
**Explore the benefits of PyTest fixtures in this article. Earthly significantly accelerates PyTest-based test builds with its caching mechanisms. [Check it out](https://cloud.earthly.dev/login).**

In software development, testing is an essential part of the development process. Tests help to ensure that the code works as expected and help catch bugs early on. To write effective tests, it's often necessary to set up some test data before running the tests and tear down (clean up) that test data after the tests have run. This can be time-consuming and error-prone if done manually.

[PyTest](https://docs.pytest.org/) is a popular testing framework for Python programming language. [Fixtures](https://docs.pytest.org/en/7.1.x/explanation/fixtures.html#about-fixtures) in PyTest provide a way to manage the resources and data required for running tests. They simplify the process of setting up, tearing down, and sharing test data between test functions. PyTest fixtures provide a convenient way to define these resources and data once and reuse them across multiple tests, saving time and reducing the chance of errors.

In this tutorial, you will learn what PyTest fixtures are, why they are used, and how to define and use them in your tests. To explore the usage of Pytest fixtures, you'll be creating a simple note-taking application that lets users add, edit, and get notes.

## Prerequisites

To follow this tutorial, it is recommended that you have the following prerequisites:

1. Basic knowledge of the Python programming language.
2. Familiarity with writing and running tests.
3. A computer with Python 3.8+ installed and a code editor to write code.

You can find all the code samples used in the tutorial in this [repository](https://github.com/ashutoshkrris/pytest-fixtures-tutorial).

## Why Use Pytest Fixtures?

Fixtures are important in testing because they provide a reliable and consistent context for tests. This context may include a variety of components, such as content like a specific dataset or a pre-configured environment. Typically, a test follows the [**Arrange**, **Act**, and **Assert** (AAA) pattern](https://docs.pytest.org/en/7.1.x/explanation/anatomy.html#test-anatomy). Fixtures define the necessary steps and data for the "Arrange" phase of the test. In addition to that, you can also use fixtures to define the "Act" phase, which involves the actual execution of the test logic. However, this will be useful when you're writing complex tests which is beyond the scope of this tutorial.

Fixtures allow you to set up test data that a test function might have in a consistent and repeatable way. This can help [make](/blog/using-cmake) tests more reliable and easier to maintain. Fixtures also help to reduce code duplication by allowing you to reuse common setup and teardown logic across multiple tests.

### Advantages of PyTest Fixtures

There are several advantages to using PyTest fixtures. They include:

1. **Reusability**: Fixtures can be reused across multiple test functions, making it easy to share common setup and teardown logic.

2. **Configuration**: Fixtures can be configured to provide specific data or other resources to test functions, making it easy to test a wide range of scenarios.

3. **Consistency**: Fixtures help ensure that tests are run in a consistent and repeatable way, making it easier to identify issues and debug tests.

4. **Improved test reliability**: By using fixtures to manage test data, you can help ensure that tests are less prone to failing due to changes in the environment or other factors.

5. **Easier maintenance**: Fixtures help [make](/blog/using-cmake) tests easier to maintain by reducing code duplication and simplifying the process of modifying how tests are set up and run.

## Setting Up a Pytest Project

![Setup]({{site.images}}{{page.slug}}/setup.png)\

Before following along with the tutorial, you need to set up a virtual environment for the project and install the Pytest library.

You can create a virtual environment with [venv](https://docs.python.org/3/tutorial/venv.html) as shown below:

~~~{.bash caption=">_"}
mkdir pytest-project && cd pytest-project
python3 -m venv venv
~~~

> Note: The `python` may still refer to Python 2 instead of Python 3 on some systems. Hence, the tutorial recommends using `python3` to avoid confusion.

Run the following command to activate the virtual environment:

~~~{.bash caption=">_"}
source venv/bin/activate
~~~

You can install PyTest by running the following command in your terminal:

~~~{.bash caption=">_"}
pip3 install pytest
~~~

You can run test(s) by executing the `pytest` command:

~~~{.bash caption=">_"}
pytest
~~~

### Creating a Note-Taking Application

As discussed, you'll create a note-taking application to learn the usage of Pytest fixtures. The application will contain three instance methods; `add_note`, `get_note`, and `edit_note`.

You'll start by writing the application logic. Create a `notes_app.py` file in the `pytest-project` directory and add the following code:

~~~{.python caption="notes_app.py"}
class Note:
    def __init__(self, content):
        self.content = content


class NotesApp:
    def __init__(self):
        self.notes_list = []

    def add_note(self, content):
        new_note = Note(content)
        self.notes_list.append(new_note)
        return "Note added successfully"

    def get_note(self, index):
        try:
            return self.notes_list[index].content
        except IndexError:
            return "Index out of range"

    def edit_note(self, index, content):
        try:
            self.notes_list[index].content = content
            return "Note edited successfully"
        except IndexError:
            return "Index out of range"

~~~

The above code defines two classes: `Note` and `NotesApp`.

The `Note` class represents a single note in the application and has a single attribute, `content`, which holds the content of the note. The class takes a string argument and sets it as the value of the `content` attribute in the constructor.

The `NotesApp` class serves as the primary notes application and initializes an empty list attribute `notes_list` to store notes.

The `NotesApp` class has the following three methods:

1. A `add_note` method that takes a string argument, `content`, and creates a new `Note` object with that content. It then appends the new `Note` object to the `notes_list` attribute. The method returns the string `"Note added successfully"`.

2. A `get_note` method that takes an integer argument `index` and returns the content of the note at that index (0-index) in the `notes_list` attribute. To handle the possibility of the index being out of range, the method utilizes a try-except block to handle the `IndexError` exception. In that case, the method returns the string "Index out of range".

3. A `edit_note` method that takes two arguments: an integer `index` and a string `content`. It uses a try-except block to handle the `IndexError` exception similar to the `get_note` method. If the index is valid, it sets the content of the note at that index in the `notes_list` attribute to the new content. The method returns the string `"Note edited successfully"`. If an invalid index is passed, the method returns the string `"Index out of range"`.

Next, you'll write the unit tests for the application. The following tests does not utilize any Pytest features such as fixtures.

Create a `test_notes_app.py` file in the `pytest-project` directory, and add the following code:

~~~{.python caption="test_notes_app.py"}
from notes_app import NotesApp


def test_add_note():
    notes = NotesApp()
    result = notes.add_note("Test note 1")
    assert result == "Note added successfully"
    assert len(notes.notes_list) == 1
    assert notes.notes_list[0].content == "Test note 1"


def test_get_note():
    notes = NotesApp()
    notes.add_note("Test note 1")
    result = notes.get_note(0)
    assert result == "Test note 1"


def test_get_note_index_error():
    notes = NotesApp()
    result = notes.get_note(0)
    assert result == "Index out of range"


def test_edit_note():
    notes = NotesApp()
    notes.add_note("Test note 1")
    notes.edit_note(0, "Test note 1 edited")
    result = notes.get_note(0)
    assert result == "Test note 1 edited"


def test_edit_note_index_error():
    notes = NotesApp()
    result = notes.edit_note(0, "Test note 1 edited")
    assert result == "Index out of range"

~~~

The above code is a set of unit tests that checks the various functionality of the `NotesApp` class such as adding a new note, getting a note by its index, editing an existing note, and handling exceptions when an invalid index is passed.

The code contains the following five test functions:

1. The `test_add_note` function tests the `add_note` method of the `NotesApp` class. It creates an instance of the class, calls the `add_note` method with a string argument, and asserts that the returned result is `"Note added successfully"` which the method is expected to return. It also checks that the `notes_list` attribute of the instance contains exactly one note and that the content of the note is equal to the string passed to the `add_note` method.

2. The `test_get_note` function tests the `get_note` method. It creates an instance of the class, adds a note, and calls the `get_note` method with an index of 0. It asserts that the result is equal to the string `"Test note 1"` which is the content of the note that you added.

3. The `test_get_note_index_error` function tests the handling of exceptions when an invalid index is passed to the `get_note` method. It creates an instance of the class and calls the `get_note` method with an index of 0. It asserts that the result is equal to `"Index out of range"`.

4. The `test_edit_note` function tests the `edit_note` method. It creates an instance of the class, adds a note, calls the `edit_note` method with an index of 0 and a string argument, and asserts that the result of calling `get_note` with an index of 0 is equal to "Test note 1 edited".

5. The `test_edit_note_index_error` function tests the handling of exceptions when an invalid index is passed to the `edit_note` method. It creates an instance of the class and calls the `edit_note` method with an index of 0 and a string argument. It asserts that the result is equal to "Index out of range".

Once you have the `notes_app.py` and `test_notes_app.py` files in place, execute the following command to run the tests:

~~~{.bash caption=">_"}
pytest -v
~~~

Output:

~~~{ caption="Output"}
collected 5 items

test_notes_app.py::test_add_note PASSED                    [ 20%]
test_notes_app.py::test_get_note PASSED                    [ 40%]
test_notes_app.py::test_get_note_index_error PASSED        [ 60%]
test_notes_app.py::test_edit_note PASSED                   [ 80%]
test_notes_app.py::test_edit_note_index_error PASSED       [100%]

===================== 5 passed in 0.07s =========================
~~~

The `-v` option in the `pytest` command increases the verbosity of the output. The verbosity level controls how much information is printed to the console during the test execution. Since you're running the tests for the first time, it makes more sense to increase the verbosity to print more detailed information about the tests being executed

You now have a simple note-taking application with the core logic and unit tests. However, you may notice that there is some code duplication in the unit tests functions. Specifically, you're creating the `NotesApp` object in each of the test methods, and you also need to have existing notes in some of the tests.

To avoid this duplication, you can use fixtures. In the next section, you'll learn how to use fixtures to simplify your test setup and improve your testing.

## Understanding Fixtures

![Understand]({{site.images}}{{page.slug}}/understand.png)\

PyTest fixtures are functions that provide data, objects, or resources to test functions. Fixtures are defined in test files and can be shared across test functions. Fixtures can help simplify test code and make tests more modular and reusable.

### Defining Fixtures

To define a fixture, you simply create a function and decorate it with the [`@pytest.fixture`](https://docs.pytest.org/en/7.1.x/reference/reference.html#pytest.fixture) decorator. This function can then return any data or object that you want to make available to your test functions. For example, earlier you were creating a `NotesApp` object in each of the test methods. But now you can define a fixture to initialize the `NotesApp` class:

~~~{.python caption="test_notes_app.py"}
import pytest

from notes_app import NotesApp


@pytest.fixture
def app_without_notes():
    app = NotesApp()
    return app


@pytest.fixture
def app_with_notes():
    app = NotesApp()
    app.add_note("Test note 1")
    app.add_note("Test note 2")
    return app

~~~

The above code defines two PyTest fixtures for the `NotesApp` class. These fixtures can be used in any test function by including them as arguments to the test function.

The `app_without_notes` fixture creates a new `NotesApp` object and returns it to the test function. This object doesn't contain any notes in it.

The `app_with_notes` fixture creates a new `NotesApp` object and adds two default notes to it by calling the `add_note` method two times. It then returns the object to the test function.

### Using Fixtures in Test Functions

To use a fixture in a test function, include it as an argument to the test function. For example, you can rewrite the `test_add_note` method to use the `app_without_notes` fixture:

~~~{.python caption="test_notes_app.py"}
def test_add_note(app_without_notes):
    result = app_without_notes.add_note("Test note 1")
    assert result == "Note added successfully"
    assert len(app_without_notes.notes_list) == 1
    assert app_without_notes.notes_list[0].content == "Test note 1"
~~~

Instead of creating a new `NotesApp` object, the `test_add_note` method now uses the `app_without_notes` fixture. The test method adds a new note to the NotesApp object using the `add_note` method and then makes several assertions to verify that the method works correctly.

Similarly, you can rewrite the other test methods to use the fixtures accordingly:

~~~{.python caption="test_notes_app.py"}
def test_get_note(app_with_notes):
    result = app_with_notes.get_note(0)
    assert result == "Test note 1"


def test_get_note_index_error(app_without_notes):
    result = app_without_notes.get_note(0)
    assert result == "Index out of range"


def test_edit_note(app_with_notes):
    app_with_notes.edit_note(0, "Test note 1 edited")
    result = app_with_notes.get_note(0)
    assert result == "Test note 1 edited"


def test_edit_note_index_error(app_without_notes):
    result = app_without_notes.edit_note(0, "Test note 1 edited")
    assert result == "Index out of range"

~~~

You can run the test with the `pytest` command:

~~~{.bash caption=">_"}
pytest  -v
~~~

Output:

~~~{ caption="Output"}
collected 5 items

test_notes_app.py::test_add_note PASSED                    [ 20%]
test_notes_app.py::test_get_note PASSED                    [ 40%]
test_notes_app.py::test_get_note_index_error PASSED        [ 60%]
test_notes_app.py::test_edit_note PASSED                   [ 80%]
test_notes_app.py::test_edit_note_index_error PASSED       [100%]

========================= 5 passed in 0.09s ======================
~~~

>Note: The output of running these test case that utilize the Pytest fixture is not different from the one that doesn't.

### The `conftest.py` File

To reuse fixtures in multiple test files, create a `conftest.py` file and define the fixtures in it. Pytest will automatically discover and use them in your test files. However, note that the file must be named `conftest.py` for Pytest to automatically discover it.

You can define fixtures in a `conftest.py` file in the root directory of your project, and they will be available to all of your tests. But you can also define additional fixtures or configuration options in `conftest.py` files in subdirectories or [packages](/blog/setup-typescript-monorepo), which will be available to tests in those directories and any subdirectories or packages contained within them.

For example, let's say you have a directory structure like this:

~~~{ caption=""}
tests/
├── conftest.py
├── test_example1.py
└── subdirectory/
    ├── conftest.py
    └── test_example2.py
~~~

In this example, the fixtures defined in the `conftest.py` file in the root `tests/` directory could be used by all of your tests. However, the fixtures defined in the `conftest.py` file in the `subdirectory/` directory are specific to the tests in that `subdirectory`, and cannot be used by tests in other parts of the project.

Create a `conftest.py` file in the same directory as the source and test file and move the import statements and fixtures from the `test_notes_app.py` file to this file:

~~~{.python caption="test_notes_app.py"}
import pytest

from notes_app import NotesApp


@pytest.fixture
def app_without_notes():
    """Returns an instance of the NotesApp class with zero notes."""
    app = NotesApp()
    return app


@pytest.fixture
def app_with_notes():
    """Returns an instance of the NotesApp class with two notes."""
    app = NotesApp()
    app.add_note("Test note 1")
    app.add_note("Test note 2")
    return app

~~~

Since you have already run the tests earlier, you might not want to see detailed information about the tests. Thus, you can decrease the verbosity of the output by adding the `-q` option to the `pytest` command:

~~~{ caption="Output"}
.....                                        [100%]
5 passed in 0.02s
~~~

### Modularization in Fixtures

Fixtures are highly modular and allow the use of other fixtures within a fixture function, which can be helpful when one fixture depends on another. If you modify the initial fixture, any dependent fixtures will also be updated automatically.

If you take a look at the fixtures in your `conftest.py` file, you might notice that you're creating the `NotesApp` object twice. However, you can create the `NotesApp` instance only once in a fresh fixture and request it from the other fixtures. It's that simple!

~~~{.python caption="test_notes_app.py"}
import pytest

from notes_app import NotesApp


@pytest.fixture
def app():
    """Returns an instance of the NotesApp class."""
    app = NotesApp()
    return app


@pytest.fixture
def app_without_notes(app):
    """Returns an instance of the NotesApp class with zero notes."""
    return app


@pytest.fixture
def app_with_notes(app):
    """Returns an instance of the NotesApp class with two notes."""
    app.add_note("Test note 1")
    app.add_note("Test note 2")
    return app
    
~~~

Notice how you passed the `app` fixture as an argument to the `app_without_notes`  and `app_with_notes` fixtures and used it inside them.

### Fixture Scope

So far, you've explored how Pytest fixtures can be defined for specific test functions. However, fixtures can also be defined with different scopes to suit different needs. Depending on the specific use case, a fixture can be defined for a single test function, a test class, or an entire module.

Pytest fixtures can have different scopes that determine when they are created and destroyed during the test execution process. The available fixture scopes are as follows:

1. **Function scope**: The fixture is created and destroyed for each test function. This is the default scope and is suitable for fixtures that are lightweight and do not depend on any other fixtures.

2. **Class scope**: The fixture is created and destroyed once for each test class. It means that the class-scoped fixtures are useful for fixtures that need to be shared across multiple test functions within the same test class.

3. **Module/Package scope**: The fixture is created and destroyed once for each module or package. It means that the module-scoped or package-scoped fixtures are useful for fixtures that need to be shared across multiple test functions within the same module or package.

4. **Session scope**: The fixture is created and destroyed once for the entire test session. It means that session-scoped fixtures are useful for fixtures that need to be shared across multiple test functions for the entire test run.

The appropriate scope for a fixture depends on its intended use and how expensive it is to create in terms of time and resources. If a fixture is cheap to create and does not depend on other fixtures, the `function` scope is usually sufficient. However, if a fixture is expensive to create or depends on other fixtures, a higher scope may be more appropriate to reduce the overall execution time of the test suite.

Here's how you can set the scope of a fixture, say "session" in this case:

~~~{.python caption="test_notes_app.py"}
@pytest.fixture(scope="session")
def your_function():
    ...
~~~

Similarly, you can set the other scopes by passing a lowercase value of their name to the`scope` argument.

> Note that the scope names are case-sensitive. It means `@pytest.fixture(scope="Class")` will throw an error.

For the `NotesApp` application, it's important to create and destroy fixtures used to create instances of the `NotesApp` class for each test function. Otherwise, the same instance of the `NotesApp` class will be reused across all test functions. This can cause unintended test results and [make](/blog/using-cmake) it difficult to isolate individual tests.

For example, if the fixture that creates an instance of the `NotesApp` class is reused across multiple test functions, it could contain notes from a previous test that could interfere with the intended behavior of the current test. To avoid this, you should define the fixtures with the `function` scope, which ensures that a new instance of the `NotesApp` class is created and destroyed for each test function.

## Advanced Usage of Fixtures

![Advanced]({{site.images}}{{page.slug}}/adv.png)\

Until now, you've just learned how to set up fixtures. In this section, you'll dive into some advanced use cases of fixtures. These include cleaning up test data, parameterizing fixtures, and auto-using fixtures.

### Teardown Test Data Using `yield` Fixtures

To avoid interfering with other tests and cluttering the system with unnecessary test data, it's important to ensure that your tests clean up after themselves. Thankfully, Pytest fixtures come with a convenient [teardown system](https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#teardown-cleanup-aka-fixture-finalization) that enables you to define the exact steps required for each fixture to perform the cleanup. By utilizing this system, you can ensure that your fixtures tidy up after themselves and leave the system in a clean state, making it easier to manage and maintain your test suite.

[`yield` fixtures](https://docs.pytest.org/en/7.1.x/how-to/fixtures.html#yield-fixtures-recommended) can be used to perform setup and teardown operations concisely and elegantly. While regular fixtures use the `return` statement to provide a fixture object that can be used in the test function, `yield` fixtures use the `yield` keyword to define the setup and teardown operations. Any teardown code for that fixture is placed  **after**  the  `yield` statement.

Here's a simple example that shows how you can use `yield` fixtures:

~~~{.python caption="test_notes_app.py"}
@pytest.fixture
def app_with_notes(app):
    """Returns an instance of the NotesApp class with two notes."""
    print("Setting up the data for the test...")
    app.add_note("Test note 1")
    app.add_note("Test note 2")
    print("Data is ready for the test...")
    yield app
    print("Cleaning up the data after the test...\n")
    app.notes_list = []

~~~

The above fixture first sets up the test data (two notes) as earlier. It then yields the `app` instance, allowing the test function that uses this fixture to access the `app` instance. After the test function finishes using the `app` instance, the fixture's code after the `yield` statement is executed. In this case, the code cleans up the test data by resetting the `notes_list` attribute of the `app` instance to an empty list.

The function also contains a few print statements to show the flow of execution. Run the tests by executing the `pytest -q` command:

~~~{ caption="Output"}
.Setting up the data for the test...
Data is ready for the test...
.Cleaning up the data after the test...

.Setting up the data for the test...
Data is ready for the test...
.Cleaning up the data after the test...

.
5 passed in 0.01s
~~~

### Parameterizing Fixtures

By using parameterization in fixtures, a fixture function can be called multiple times, running the dependent tests each time. It can be especially useful when testing components that can be configured in multiple ways, enabling the creation of more comprehensive and exhaustive functional tests.

Similar to scopes, you can pass a `params` list in the `@pytest.fixture` decorator. For example, the below code shows how you can add parameters in a `note_data` fixture:

~~~{.python caption="test_notes_app.py"}

@pytest.fixture(params=[("Test note 1", "Note added successfully"),
                        ("Test note 2", "Note added successfully")])
def note_data(request):
    """Returns a tuple containing an input value and an expected \
    output value for the add_note method."""
    return request.param

~~~

In this fixture, the `params` argument is a list of tuples, each containing an input value and the expected output value for the `add_note` method. The `note_data` fixture returns one tuple from this list each time it is called.

You can then use the `note_data` fixture in a test function that tests the `add_note` method with different input values. Here's an example:

~~~{.python caption="test_notes_app.py"}

def test_add_note_with_param(note_data, app_without_notes):
    input_value, expected_output = note_data
    result = app_without_notes.add_note(input_value)
    assert result == expected_output
    assert len(app_without_notes.notes_list) == 1
    assert app_without_notes.notes_list[0].content == input_value

~~~

In this test function, the `note_data` fixture is used to parametrize the test with different input values and expected output values for the `add_note` method. Each tuple returned by the fixture is unpacked into `input_value` and `expected_output`, and the test is run once for each tuple.

When you run the test using the `pytest -v` command, you'll see the below output:

~~~{ caption="Output"}
collected 7 items 
test_notes_app.py::test_add_note PASSED                          [ 14%] 
test_notes_app.py::test_get_note PASSED                          [ 28%] 
test_notes_app.py::test_get_note_index_error PASSED              [ 42%] 
test_notes_app.py::test_edit_note PASSED                         [ 57%]
test_notes_app.py::test_edit_note_index_error PASSED             [ 71%] 
test_notes_app.py::test_add_note_with_param[note_data0] PASSED   [ 85%] 
test_notes_app.py::test_add_note_with_param[note_data1] PASSED   [100%] 

============================ 7 passed in 0.04s ====================== 

~~~

Notice that the `test_add_note_with_param` test runs twice because you have passed two values in the parameters.

### `autouse` Fixtures

At times, you might have a fixture or multiple fixtures that all your tests will need to depend on. In such cases, the `autouse` option in pytest fixtures can be used to automatically apply the fixture to all tests within a certain scope. This feature removes the need for explicitly requesting the fixture in each test function.

To use `autouse` with fixtures, you can simply add the `autouse` parameter to the fixture definition and set it to `True`.

~~~{.python caption="test_notes_app.py"}
@pytest.fixture(autouse=True)
def your_fixture():
    ...
~~~

> Note that using `autouse` fixtures can be risky, as they can potentially interfere with other fixtures or tests. So, use them with caution and only when necessary.

## Conclusion

PyTest fixtures are indeed a game-changer! They save time and make automated testing a breeze by handling test data creation, setup, and teardown operations. This tutorial covered the basics, like defining and using fixtures, their scopes, and some advanced stuff like yield fixtures, parameterizing fixtures, and `autouse` fixtures.

Having this knowledge in your toolkit is going to level up your testing game, ensuring your code is robust, efficient, and bug-free. And while you're nailing Python testing, consider exploring [Earthly](https://cloud.earthly.dev/login) to boost your build game too. It's an excellent tool for those who want to further optimize their development process.

Keep exploring and happy coding!

{% include_html cta/bottom-cta.html %}
