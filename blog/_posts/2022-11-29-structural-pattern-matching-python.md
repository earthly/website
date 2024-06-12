---
title: "Structural Pattern Matching in Python"
toc: true
author: Mustapha Ahmad Ayodeji
editor: Bala Priya C

internal-links:
 - python
 - Pattern
 - Structural
excerpt: |
    In this tutorial, you'll learn how structural pattern matching works in Python 3.10 and how to use different types of patterns to match and extract values from objects. You'll also explore real-world examples and see how this feature can be applied in various scenarios.
last_modified_at: 2023-07-19
categories:
  - python
---
**This article explores Python's structural pattern matching. Earthly streamlines the build process for Python developers. [Check it out](https://cloud.earthly.dev/login).**

*Structural Pattern Matching* is a new feature introduced in Python 3.10 in the [PEP 634](https://peps.python.org/pep-0634/) specification. The feature verifies if the value of an expression, called the *subject*, matches a given structure called the `pattern`.

Structural Pattern Matching provides an elegant method to destructure, extract, and match the values or attributes of an object using an easy-to-read syntax.

In this tutorial, you'll learn how structural pattern matching works in Python by coding several examples in the context of working with web services. We'll explore this new feature to match the structure and attributes of the response from the [JSONPlaceholder](https://jsonplaceholder.typicode.com
) Fake API. [JSONPlaceholder](https://jsonplaceholder.typicode.com) is a free online REST API that you can use whenever you need some fake data.

In this tutorial, we'll use the following endpoints from the API:

~~~
GET /posts  #returns 100 posts
GET /posts/<id>   #returns a single post
~~~

By the end of this tutorial, you'll have a better understanding of structural pattern matching and you'll be able to use it in your next Python project or a codebase that you're working on.

The code examples in this tutorial are in the `pattern-matching.py` file; you can download it from [this GitHub repository](https://github.com/DrAnonymousNet/Structural-Pattern-Matching) and follow along.

## Prerequisites

- Proficiency in Python
- [Python 3.10](https://www.python.org/downloads/release/python-3106/)  or the most recent stable release of Python 3.11

This tutorial uses the Python [Requests](https://requests.readthedocs.io/en/latest/) library to retrieve fake [blog](/blog/top-5-scala-blogs) post data from the *JSONPlaceholder* API. Therefore, a working knowledge of the library will be helpful but not required.

You may install the Requests library using the `pip` package manager:

~~~{.bash caption=">_"}
pip install requests
~~~

## Basics of Pattern Matching

### Understanding the `match-case` Syntax

~~~{.python }
match <expression>:
    case <pattern 1> [<if guard>]:
        <block to execute if pattern 1 matches>
    case <pattern n> [<if guard>]:
        <code block to execute if pattern n matches>
~~~

The `match` keyword is a [soft keyword](https://docs.python.org/3/reference/lexical_analysis.html#soft-keywords) whose expression evaluates to produce a value called the *subject*. The *subject* is then matched against the pattern of each `case` clause. The `case` block corresponding to the first match is executed; all subsequent case statements are ignored.

The `guard` is an optional `if condition` in a `case clause`. It's evaluated after a `pattern` matches the subject. The block of code associated with the case clause will execute only if the `guard` evaluates to `True`. Otherwise, the next pattern will be compared until there is another match with a `guard` that evaluates to True (if we specified a `guard`).

If you've coded in Javascript or C, the `match-case` statement might look similar to the `switch-case` statement. However, there are certain differences.
The `match-case`  statement differs from the `switch-case` statement in that it does not require an explicit `break` statement after a pattern has been matched. It also has a lot of powerful features that cannot be found in the `switch-case` statement in other languages. We will explore these features later on.

The patterns are shapes or structures that the *subjects* are compared against. The values of the *subject* can also be captured and `bound` to a variable that we specified in the pattern.

Binding variables to values is a little different than assigning variables to values. The value captured in the pattern can not be set as a value to an attribute of an object in the `case clause` using the dot notation:

~~~{.python caption=""}
object.attribute = value 
~~~

However, variable bindings outlive the scope of the respective case or match statements just like a normal variable.

~~~{.python caption=""}
book_data = ["Structural Pattern Matching", "DrA", 232113]

match book_data:
    case title, author:
        isbn = None
    case title, author, isbn if type(isbn) == 'int':
        pass
~~~

In the example above:

- The `book_data` variable that precedes the `match` statement is the `subject`
- The variables in front of the `case` statements are a form of pattern we will discuss later.
- The second `case` clause will be matched and the elements in the `book_data` list will be bound to these variables (`title`, `author`, and `isbn`).
- The condition in the `if statement` is the `guard` and the Python interpreter only evaluates it if the pattern has *matched* the `subject`.

There are several classes of structural patterns that can be matched and they include the following:

- Literal Patterns
- As Patterns
- Wildcard Patterns
- OR Patterns
- Value Patterns
- Sequence Patterns
- Mapping Patterns
- Class Patterns

## Matching Literal Patterns in Python

![Literal patterns]({{site.images}}{{page.slug}}/T0rEuUn.png)\

Literal patterns are constants (alphabetic, numeric, or boolean) that only match the exact values. They include a *subject* with one of the basic data types (integer, float, string, and Boolean) matched against a pattern of the same data type.

The behavior of the `match-case` statement, in this case, is similar to the `switch-case` statement in Javascript.

The `match-case` statement compares the value of the *subject* with the literal values specified as patterns in the case clauses.

This comparison is done using the equality == operator for all the literal patterns except for `True`, `False`, and `None` which are compared using Python's `is` keyword.

All forms of strings ([byte](https://docs.python.org/3/library/stdtypes.html#bytes), [raw](https://www.digitalocean.com/community/tutorials/python-raw-string), [triple quoted](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str) string) can be specified as a pattern except the [F string](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals) which are not really literals.

However, based on the consistent rule of equality `==`  in Python, literal patterns like 1 and 1.0 will match (so do all expressions that evaluate to `True`) when compared with the equality sign:

~~~{.python caption=""}
In [1]: 1 == 1.0
Out[1]: True

In [2]: 0 == False
Out[2]: True
~~~

### Matching Integer Values

Let's take a look at an example of matching a literal integer value:

~~~{.python caption="pattern-matching.py"}
import requests

def main(response):
   status_code = response.status_code #200
   match status_code:
       case 200:
           print("The response is OK")
       case 400:
           print("The response is Bad")

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
~~~

If we execute the code above, we will get the following output:

~~~{.bash caption="Output"}
The response is OK
~~~

In the case above, Python compares the *subject* which is the `status_code` to the literal integer pattern we specified in the case clauses (200 and 400). After the status code matches the *subject*, the interpreter executes the code under the case clause.

### Matching String Values

We can match a string like the encoding of the response as shown below:

~~~{.python caption="pattern-matching.py"}
import requests

def main(response):
   encoding = response.encoding
   match encoding:
       case "utf-8":
           print("The encoding is utf-8")
       case "utf-16":
           print("The encoding is utf-16")

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
~~~

We have this output:

~~~{.bash caption="Output"}
The encoding is utf-8
~~~

### Matching Boolean Values

Similarly, we can match a `bool` value:

~~~{.python caption="pattern-matching.py"}
import requests

def main(response):
    check = response.ok
   match check:
       case True:
           print("The response is ok")
       case False:
           print("The response is not ok")

response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
~~~

We will get the output as shown below:

~~~{.bash caption="Output"}
The response is ok
~~~

To match a floating value or a `None` keyword, you can specify an expression that evaluates to either of them in the `match` statement to compare against them as a literal value in the case clauses.

## Matching Capture Patterns

We can capture and bind some or all the values of the *subject* to a variable.

`Capture patterns` are names that capture values that match the structure of the subject in a variable. These variables outlive the scope of their respective case clauses; they can be accessed outside the `match-case` block.

The binding of values to variables is similar to how arguments are the values of parameters in a function.

~~~{.python caption="pattern-matching.py"}

def main(response):
   values = [response.status_code, response.encoding, response.json()]
   match values:
       case [status_code, encoding]:
           print("The first pattern matches the subject")
           print(status_code, encoding)
       case [status_code, encoding, response_data] if status_code <= 399:
           print("The second pattern matches the subject")
           print(status_code, encoding, response_data)

~~~

In the snippet above, the *subject* is a sequence with three elements, therefore only a pattern with this same structure can match the *subject* successfully.

- The `pattern` in the first `case` matches only two of the three elements in the *subject*,  as a result, the match will not be successful.

- The pattern in the second `case` matches the structure of the *subject* and the `guard` evaluates to `True`. In addition, the interpreter binds the names we specified in the pattern to the values of the elements in the sequence.

When we run the code above, we will get the following output:

~~~{.bash caption="Output"}
The second pattern matches the subject
200 utf-8 {'userId': 1, 'id': 1, 'title': \
'sunt aut facere repellat provident occaecati \
excepturi optio reprehenderit', 'body': \
'quia et suscipit\nsuscipit recusandae consequuntur \
expedita et cum\nreprehenderit molestiae ut ut quas \
totam\nnostrum rerum est autem sunt rem eveniet architecto'}

~~~

Only the second pattern matches the subject and the bound values are printed out in the `case` block.

The capture pattern matches and binds values to the names we specified in the pattern. However, individual data type matching of the elements in the sequence above is not possible. This can be achieved with the `As pattern`, which we will discuss in the next section.

## As Pattern

The *As pattern* allows us to specify a pattern to match the *subject* or individual elements in a *subject*  against and also a name to bind the value of the subject.

The `As pattern` uses the `as` keyword to bind a variable to the value after the structure of the subject matches the pattern.

Let us modify the snippet above to match the number of elements in the sequence and the data-types of the individual elements.

~~~{.python caption="pattern-matching.py"}

def main(response):
   values = [response.status_code, response.encoding, response.json()]
   match values:
       case [int() as status_code, str() as encoding]:
           print("The first pattern matches the subject")
                   
       case [int() as status_code, str() as encoding, str() as \
       response_data]:
           print("The second pattern matches the subject")
       case [int() as status_code, str() as encoding, dict() as \
       response_data]:
           print("The Third pattern matches the subject")
   print(f"status_code:{status_code}, encoding:{encoding}, \
   response_data:{response_data}")

~~~

In this example:

- The first pattern fails because it does not match the number of elements in the sequence, but matches the data type of the `status_code` and the `encoding` which are integer and string respectively.
- The second pattern matches the number of the elements but fails to match the data type of the `response_data` which is a `dict` data type.
- The third pattern matches both the number of elements and the data type of each element.

When we run the code above, we will get the following output:

~~~{.bash caption=">_"}
The Third pattern matches the subject
status_code:200, encoding:utf-8, response_data: \
{'userId': 1, 'id': 1, 'title': 'sunt aut facere \
repellat provident occaecati excepturi optio reprehenderit', \
'body': 'quia et suscipit\nsuscipit recusandae consequuntur \
expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum \
rerum est autem sunt rem eveniet architecto'}

~~~

The above pattern can be made more concise by passing in the variable names as arguments into the data type classes, as shown below:

~~~{.python caption="pattern-matching.py"}
case [int(status_code), str(encoding)]:
~~~

## Matching Wildcard Patterns

![Wildcard Patterns]({{site.images}}{{page.slug}}/HFFv2Tb.png)\

The wildcard pattern, denoted by an underscore ( `_` ) matches any structure but doesn't bind the value. It is often used as a fallback pattern if no pattern matches the structure of the subject.
Here's an example:

~~~{.python caption="pattern-matching.py"}

def main(response):
   status_code = response.status_code
   match status_code:
       case 300:
           print("The response is 300")
       case 400:
           print("The response is 400")
       case _:
           print("No pattern matches the response status !")

~~~

When you run the code above, you will get an output as shown below:

~~~{.bash caption=">_"}
No pattern matches the response status !
~~~

The status code of the response is expected to be 200; so none of the *literal patterns* matched the status code. Since the *wildcard pattern* ( `_` ) matches any structure, the interpreter will execute the statement in the last case clause.

We can match the example in the *captured pattern* above with the *wildcard pattern* if we only want to bind the value of the `encoding` as shown below:

~~~{.python caption="pattern-matching.py"}
def main(response):
   values = [response.status_code, response.encoding, response.json()]
   match values:
       case [ _, encoding]:
           print("The first pattern matches the subject")
           print(encoding)
       case [ _, encoding, _ ]:
           print("The second pattern matches the subject")
           print(encoding)
~~~

The *wildcard pattern* will match the status code and response data:

~~~{.bash caption=">_"}
The second pattern matches the subject
utf-8
~~~

An attempt to access the value of the wildcard pattern ( `_` ) will give a `NameError` as shown below:

~~~{.python caption="pattern-matching.py"}
NameError: name '_' is not defined
~~~

## Matching OR Patterns

The OR pattern allows you to combine *structurally equivalent* alternatives into a new pattern, allowing several patterns to share a common handler.

> "If any of an OR pattern's subpatterns matches the subject, the entire OR pattern succeeds." - [PEP635](https://peps.python.org/pep-0635/#or-patterns)

The OR pattern is specified with a `pipe` ( | ) character in between the structurally equivalent alternatives.

Once one of the patterns that are separated by the *or character* matches the structure of the *subject*, the pattern matching is successful and the interpreter executes the code under the respective case clause.

If more than one of the alternatives matches, only the first value will be picked and optionally bound to a variable if we specify a variable to bind to. This behavior conforms with Python's `or` operator [short-circuit evaluation](https://docs.python.org/3/library/stdtypes.html#boolean-operations-and-or-not)  which stops evaluation as soon as it finds the first condition that evaluates to `True`.

The example below checks the encoding scheme of the response by matching the *subject* against patterns with alternatives.

As with other pattern, we can bind the value of the pattern that matches the structure of the *subject* to a variable as shown below:

~~~{.python caption="pattern-matching.py"}

def main(response):
   encoding = response.encoding
   match encoding:
       case "utf-8" | "utf-16" as encoding:
           print(f"The response was encoded with {encoding} \
           encoding scheme")
       case "base64" | "ascii" as encoding:
           print(f"The response was encoded with {encoding} \
           encoding scheme")
       case _:
           print("No pattern matches the response encoding !")
       
~~~

The first pattern will match if the encoding scheme is either `utf-8` or `utf-16`.The second pattern will match if the encoding scheme is either `base64` or `ascii` and the value of the encoding will be bound to the `encoding` variable we specified.

If we run the code above, we will get the output below:

~~~{.bash caption="Output"}
The response was encoded with utf-8 encoding scheme
~~~

## Matching Value Patterns

Value patterns involve accessing the attributes of an object. Python matches the subject against the value of the attribute that we accessed in the pattern.

This is similar in syntax to the *capture pattern*. However, the [structural pattern matching specification](https://peps.python.org/pep-0634) adopted a rule that any attribute access is to be interpreted as a *value pattern*, and the value of the subject is matched against the value of the attribute.

~~~{.python caption="pattern-matching.py"}

from http import HTTPStatus
import requests

def main(response):
   match (response.status_code, response.json()):
       case (HTTPStatus.OK.value, body):
           print(f"The response is OK")
       case (HTTPStatus.BAD_REQUEST.value | HTTPStatus.NOT_FOUND.value, _):
           print(f"Bad request or Not found")
       case _:
           print("No pattern matches the response status code !")


response = requests.get("https://jsonplaceholder.typicode.com/posts/0") #new
main(response)
~~~

In the example above:

- We request an article with an `id` of `0` which returns a status code of `404 Not Found`.
- We specify the *subject* as a sequence of the response status code and the response [json](/blog/convert-to-from-json) data.
- The pattern in each case clause is a *sequence* whose first element is the attribute access.

The *subject* is matched against the value the attribute access evaluates to—rather than binding the *subject* as a value to the attribute.

The first case pattern evaluates to:

~~~{.python caption=">_"}
case (200, body)
~~~

The second case pattern evaluates to:

~~~{.python caption=">_"}
case (400 | 404, _)
~~~

The evaluation of the second pattern contains a *literal pattern*, an *or pattern*, and the *wildcard pattern*.

The response status code is 404; so the second pattern matches and the interpreter executes the code block associated with it:

~~~{.bash caption="Outpu"}
Bad request or Not found
~~~

## Matching Sequence Patterns

Sequence patterns are patterns with comma-separated values enclosed within  `( … )`  or  `[ … ]`.

Depending on whether or not the sequence pattern contains a wildcard, it could be a fixed-length or a variable-length sequence pattern.

The fixed-length sequence pattern has to match the subject length-wise and element-wise. The pattern fails if the length of the subject sequence is not equal to the length of the sequence in the pattern.

The variable-length sequence pattern uses the Python iterable packing and unpacking syntax ( the star character `*` ) to pack a slice of the sequence into a variable. A variable-length sequence can contain at most one starred subpattern.

As in iterable unpacking, the specification does not distinguish between 'tuple' and 'list' notation. `[1, 2, 3]` is equivalent to `(1, 2, 3)` as well as `1, 2, 3`. If we need to match the sequence against its type, we need to wrap the sequence with the data type class: list([1,2,3]) or tuple(1,2,3).

In the context of pattern matching, only the following are recognized as sequences:

1. `array.array`
2. `collections.deque`
3. `list`
4. `memoryview`
5. `range`
6. `tuple`

~~~{.python caption="pattern-matching.py"}
import requests

def main(response):
   match response.json():
       case [last_post]:
           print(last_post)
       case first_post, *_, last_post:
           print("first_post: ", first_post)
           print("last_post:", last_post)
       case _:
           print("No pattern matches the response status code !")


response = requests.get("https://jsonplaceholder.typicode.com/posts")
main(response)
~~~

The code above gives the output shown below:

~~~{.bash caption=">_"}
first_post:  {'userId': 1, 'id': 1, 'title': \
'sunt aut facere repellat provident occaecati excepturi \
optio reprehenderit', 'body': 'quia et suscipit\nsuscipit \
recusandae consequuntur expedita et cum\nreprehenderit molestiae \
ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto'}
last_post: {'userId': 10, 'id': 100, 'title': 'at nam consequatur ea \
labore ea harum', 'body': 'cupiditate quo est a modi nesciunt soluta\nipsa \
voluptas error itaque dicta in\nautem qui minus magnam et distinctio \
eum\naccusamus ratione error aut'}

~~~

The code snippet above requests a list of posts from the `/posts` endpoint which returns 100 lists of posts.

The first pattern match is unsuccessful because the length of the sequence pattern does not match the length of the sequence in the subject.

The second pattern binds the value of the first element in the sequence of the *subject* to the `first_post` pattern and binds the last element in the `last_post` variable. The elements in between are packed and bound into the wildcard pattern. Hence the second pattern matches the structure of the *subject*.

## Matching Mapping Patterns

![Mapping Patterns]({{site.images}}{{page.slug}}/R4sOIib.png)\

The mapping pattern allows us to match and extract both values and keys from mapping data structures like Python dict data type. The values and keys are matched against a given subpattern.
The keys of the mapping pattern must be literals or value patterns while the value could be any of the patterns we've discussed earlier.

As an example, let's match the data of the [json](/blog/convert-to-from-json) response of the `posts/1` endpoint. The response data has the following structure:

~~~{.json caption=">_"}
{
"userId": 1,
"id": 1,
"title": "sunt aut facere…",
"body": "quia et suscipit\nsuscipit recusandae…"
}
~~~

### Matching Keys

The patterns in the key could be literal or value patterns.

All or some of the keys in the mapping data structure could be specified. If only some of the keys are specified, other keys are ignored and the pattern will match if a key that matches such a pattern is in the mapping data structure that we specify as the *subject*.

~~~{.python caption="pattern-matching.py"}
import requests

def main(response):
   post_data = response.json()
   match post_data:
        case {"user_id":1}:
            print("Pattern 1 matched")
        case {"userId":1, "postId":1}:
            print("pattern 2 matched")
        case {"userId":1, "id":1}:
            print("pattern 3 matched")
        case _:
            print("No pattern matched")
    
response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
~~~

In the example above:

- The first pattern failed because `user_id` is not a key in the response data ( the *subject* ).
- The second pattern failed because the *subject* does not have a `post_id` key.
- The third pattern matches because both of the keys we specified are present in the *subject*.

Output :

~~~{.bash caption=">_"}
pattern 3 matched
~~~

### Matching Values

The patterns in the value could be any form of pattern we have discussed so far.

~~~{.python caption="pattern-matching.py"}
def main(response):
    post_data = response.json()
    match post_data:
        case {"userId":2}:
            print("Pattern 1 matched")
        case {"userId":user_id, "id":post_id} if user_id < post_id:
            print("pattern 2 matched")
        case {"userId":user_id, "id":1|2|3} if user_id >= 1:
            print("pattern 3 matched")
        case _:
            print("No pattern matched")
~~~

In the code above:

- The first pattern will fail because the literal pattern `2` does not match the value of the `userId` key in the subject.
- The second pattern will fail because the guard clause will fail since the `user_id` is not less than the `post_id`.
- The third pattern will match because all the keys we specified are present, the `guard` will evaluate to `True` and the `or pattern` will pass.

Output :

~~~{.bash caption="Output"}
pattern 3 matched
~~~

### Key-Value Packing

When we match some part of the key-value pairs in a mapping data structure, as shown above, the interpreter ignores the other key-value pairs. If we need them, we can leverage Python's [sequence packing](https://peps.python.org/pep-3132/) feature to match and bind several keys and values in the *subject* to a variable as shown below:

~~~{.python caption="pattern-matching.py"}
def main(response):
   post_data = response.json()
   match post_data:
        case {"user_id":1, **others}:
            print("Pattern 1 matched ", others)
        case {"userId":user_id, "id":post_id, **others} \
        if user_id < post_id:
            print("pattern 2 matched", others)
        case {"userId":user_id, "id":1|2|3, **others} \
        if "title" in others.keys():
            print("pattern 3 matched")
            print(others)
        case _:
            print("No pattern matched")
           
~~~

When we execute the code above, we get the following output:

~~~{.bash caption="Output"}
pattern 3 matched
{'title': 'sunt aut facere repellat provident occaecati\
 excepturi optio reprehenderit', 'body': 'quia et \
 suscipit\nsuscipit recusandae consequuntur expedita et \
 cum\nreprehenderit molestiae ut ut quas totam\nnostrum \
 rerum est autem sunt rem eveniet architecto'}
~~~

The third pattern matches.

The value that the interpreter binds to the `others` variable is a mapping data structure that has all the attributes of a normal mapping data structure. Hence we can construct a `guard` checking if a key is present in it.

## Matching Class Pattern

Class patterns check whether the subject is an instance of a specific class. If there are no arguments, the pattern matches if the subject is an instance of the class specified in the pattern.

~~~{.python caption="pattern-matching.py"}
class Post:
    def __init__(self, userId, id, title, body):
        self.userId = userId
        self.title = title
        self.body = body
        self.post_id = id

class Post2:
    pass
~~~

We have two classes:

- The `Post` class with attributes that match with the keys in the single post [json](/blog/convert-to-from-json) response.

- The `Post2` class with no attribute.

### Matching an Instance of a Class

In the code below, the `match-case` statement behaves like the Python `isinstance` function.

We create an instance of the `Post` class with the [json](/blog/convert-to-from-json) response and match the instance against the two classes we created earlier. If the subject is an instance of the class we specify as the pattern in the case clause, the pattern matching will be successful. In this case, the second pattern matches.

~~~{.python caption="pattern-matching.py"}
import requests

def main(response):
    post = Post(**response.json())
    match post:
        case Post2():
            print("Pattern 1")
        case Post():
            print("Pattern 2")
        case _:
            print("No pattern matches the post class !")


response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
main(response)
~~~

#### Matching Keyword Arguments

The patterns above only match if the *subject* is an instance of the `pattern`.

In addition to matching class instances, we can specify keyword arguments in the pattern to match against the keyword arguments in the *subject*.

If keywords arguments are present in the class pattern:

- They are looked up as an attribute on the subject.
- If the attribute lookup raises an `AttributeError`, the pattern fails.
- If not, the subpattern associated with the keyword pattern is matched against the attribute value of the subject, if it succeeds, the whole pattern matching succeeds, otherwise it fails.

~~~{.python caption="pattern-matching.py"}
def main(response):
    post = Post(**response.json())
    match post:
        case Post(post_id = 4 | 5):
            print("Pattern 1")
        case Post(post_id = 1 | 2, userId= id) if id >= 2:
            print("Pattern 2")
        case Post(post_id = 1 | 2, userId= id) if id == 1:
            print("Pattern 3")
        case _:
            print("No pattern matches the post class !")

~~~

In the case above:

- The first pattern above matches the class of the subject but the value of the `post_id` keyword argument does not match because the `post_id` is neither 4 nor 5 hence the overall pattern fails.
- The second pattern matches the class and the `post_id` but the `guard` clause fails because the `userId` is less than 2
- The third pattern matches the class, the `post_id`, and the `guard`, hence the whole pattern matching succeeds.

#### Matching Positional Arguments

Let's specify the arguments as positional arguments instead:

~~~{.python caption="pattern-matching.py"}
def main(response):
    post = Post(**response.json())
    match post:
        case Post(4 | 5):
            print("Pattern 1")
        case Post(1 | 2, id) if id >= 2:
            print("Pattern 2")
        case Post(1 | 2, id) if id == 1:
            print("Pattern 3")
        case _:
            print("No pattern matches the response status code !")
~~~

We will get the following error:

~~~{.bash caption="Output"}
Traceback (most recent call last):
  File "/home/dracode/Adventure/pattern_matching.py", \
  line 302, in <module>
    main(response)
  File "/home/dracode/Adventure/pattern_matching.py", \
  line 292, in main
    case Post(4 | 5):
TypeError: Post() accepts 0 positional sub-patterns (1 given)
~~~

Python classes do not have a natural ordering of their attributes, we need to specify the order of the attributes using the `__match_args__` attribute before we can use the positional arguments in the patterns.

~~~{.python caption="pattern-matching.py"}
class Post:
    __match_args__ = ("post_id", "userId", "title", "body")
    def __init__(self, userId, id, title, body):
        self.userId = userId
        self.title = title
        self.body = body
        self.post_id = id
~~~

The `__match_args__` allows us to order the attributes based on our preference.

- In the case above, the first argument in the pattern will match against the equivalent first value in the `__match__args`.
- The`post_id` will be the first positional argument, the `userId` will be the second while the `title` and `body` will be the third and fourth positional arguments respectively.

If positional patterns are present in a class, they are converted to keyword patterns based on the arrangement in the `__match_args__` attribute.

## Conclusion

In this tutorial, we delved into Python 3.10's *structural pattern matching* feature. You learned about various patterns, like literal, capture, wildcard, AS, OR, sequence, mapping, and class. And the practicality of this feature isn't confined to API response matching in web development, it's useful in any scenario where value structure matching is required.

As you continue to explore Python's capabilities, you might also be interested in optimizing your builds. If so, give [Earthly](https://cloud.earthly.dev/login) a try! Earthly can be a great asset in your Python development toolkit.

{% include_html cta/bottom-cta.html %}
