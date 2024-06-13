---
title: "How to Use Django Template Filters"
toc: true
author: Joseph Adediji
editor: Bala Priya C

internal-links:
 - Django
 - Template Filters
 - Template Tags
 - Filters
 - Templates
excerpt: |
    Learn how to use Django template filters to transform and modify variable data in your HTML templates. Discover the built-in filters provided by Django and how to create your own custom filters.
last_modified_at: 2023-07-19
categories:
  - python
---
**The article explains the effectiveness of Django template filters. Earthly accelerates Django template builds with its caching mechanisms. [Learn more about Earthly](https://cloud.earthly.dev/login).**

Django is a powerful Python web framework loaded with many useful built-in features that [make](/blog/using-cmake) building complex web-focused products a lot easier; one such feature is its **templating engine**.

The Django templating engine allows you to build reusable and dynamic HTML pages that change based on data passed to the template language. It provides filters that are used to transform data in the HTML templates. Template filters can be used to transform the values of variables and tag arguments.

In this article, you'll learn about the various built-in Django template filters you can use in your project. You'll also learn how to create a custom filter.

## Template Tags vs Template Filters

![Versus]({{site.images}}{{page.slug}}/vs.jpg)\

The Django template filters and tags are closely related, but they are quite distinct in what they do in the Django template language.

Template tags are keywords and functions for the Django template engine, similar to how Python functions work. Template tags provide control flows and Python tools in the template, but they cannot modify the values of a variable. Template tags are denoted by braces and percent signs `{% raw %}{{ tag_name }}{% endraw %}`.

On the other hand, Django template filters are used to modify the values of a variable or tag arguments and transform and increment the values of a variable as needed. Template filters can be used to format numbers, dates, and other data types in a specific way or to perform common operations such as string concatenation or truncation. Template filters are applied using the pipe operator inside double braces `{% raw %}{{ variable | filter_name }}{% endraw %}`.

Filters can also be chained to perform a series of successive data transformations; this means that the first filter is applied to the next filter and the next until the end of the chain. For example:
`{% raw %}{{ variable | filter_1 | filter_2 }}{% endraw %}`.

## Popular Built-in Django Template Filters

Django comes with a lot of in-built template filters that you can readily apply to your project, but in this section, we will be taking a look at the most popular template filters you will find useful in your day-to-day development journey. Please note that this list is in no particular order.

You can find all the code examples in this tutorial in [this GitHub gist](https://gist.github.com/josylad/3ed636e20453519992a768bd79a0115c).

### Join Filter

The join filter is used to join the elements of a list with a string and outputs a string. It works like Python's `str.join(list)` which returns a string created by joining the items of a list by the given string separator.

Here's the syntax to use the join filter.

~~~{.html caption=""}
-    ``` {% raw %} {{ value | join:" - " }} {% endraw %} ``` : \
If the value is the list **['a', 'b', 'c']**, the output will be \
the string **"a - b - c"**.  

~~~

~~~{.html caption=""}
<!--  the value -->
['python', 'is', 'fun'] | join:" - "

~~~

~~~{.html caption=""}
"python - is - fun"
~~~

~~~{.html caption=""}
<!--  the value -->
['Monday', 'Tuesday', 'Wednesday'] | join:" // "
~~~

~~~{.html caption=""}
"Monday // Tuesday // Wednesday"
~~~

### Date Filter

The date filter is used to format a date according to a given format. There are numerous [format strings available for the date filter](Django documentation](<https://docs.djangoproject.com/en/4.1/ref/templates/builtins/#date>).

Here's the syntax to use the date filter: `{% raw %}{{ value | date:"D d M Y" }}{% endraw %}`.

If value is a **datetime** object (for example, the result of **datetime.datetime.now())** OR 2022-12-12T10:30:00.000123, the output will be the string **"Mon 12 Dec 2022"**.

You can also use one of the predefined date formats such as DATE_FORMAT, DATETIME_FORMAT, SHORT_DATE_FORMAT, or SHORT_DATETIME_FORMAT, or a custom format that uses the format specifiers as shown in the example above.

`{% raw %}{{ value|date:"SHORT_DATE_FORMAT" }}{% endraw %}`

The output would be the string **"12/12/2022"**.  

~~~{.html caption=""}
<!--  the value -->
2023-01-12T10:30:00.000123 | date:"SHORT_DATE_FORMAT"
~~~

~~~{.html caption=""}
'01/12/2023'
~~~

When used without a format string, the DATE_FORMAT format specifier is used. Assuming the same date as the previous example:

`{% raw %}{{ value | date }}{% endraw %}`

~~~{.html caption=""}
<!-- the value -->
2022-12-12T10:30:00.000123 | date

~~~

~~~{.html caption=""}

'Dec. 12, 2022'

~~~

~~~{.html caption=""}
<!--  the value -->
2023-01-12T10:30:00.000123 | date:"D d M Y"

~~~

~~~{.html caption=""}

"Sun 12 Jan 2023"

~~~

### Default Filter

The default filter is used to set a default value to a variable. If the variable evaluates to False, it will use the default argument given.

Here's the syntax to use the default filter: `{% raw %}{{ value | default: "nothing here" }}{% endraw %}`.

If the value is **" "** (the empty string), the output will be **"nothing here"**.

~~~{.html caption=""}
<!-- the value -->
" " | default: "an empty string"

~~~

~~~{.html caption=""}

'an empty string'

~~~

~~~{.html caption=""}
<!-- the value -->
" " | default: "This is a default value"

~~~

~~~{.html caption=""}

'This is a default value'

~~~

### Add Filter

The add filter is used to add the argument to the value. This is useful for numeric data.

Here's the syntax to use the add filter: `{% raw %}{{ value | add:"5" }}{% endraw %}`.

If the value is **10**, then the output will be **15**. This filter is used to increment a variable in Django templates by adding a constant value to the variable.

~~~{.html caption=""}
<!--  the value  -->
20 | add:"5"

~~~

~~~{.html caption=""}

25

~~~

~~~{.html caption=""}
<!--  the value  -->
[1, 2, 3] | add:"[4, 5, 6]"

~~~

~~~{.html caption=""}

[1, 2, 3, 4, 5, 6]

~~~

### Capfirst Filter  

The capfirst filter is used to capitalize the first character of the value. If the first character is not a letter, this filter has no effect.

Here's the syntax to use the capfirst filter: `{% raw %}{{ value | capfirst }}{% endraw %}`.

If the value is **"earthly"**, the output will be **"Earthly"**.

~~~{.html caption=""}
<!--  the value -->
'christmas' | capfirst

~~~

~~~{.html caption=""}

'Christmas'

~~~

~~~{.html caption=""}
<!--  the value -->
'django' | capfirst

~~~

~~~{.html caption=""}

'Django'

~~~

### Cut Filter

The cut filter is used to remove *all* occurrences of the argument from the given string. The argument you pass to the filter will be removed from the value.

Here's the syntax to use the cut filter:
`{% raw %}{{ value | cut:" " }}{% endraw %}`.

If the value is **"String with spaces"**, the output will be **"Stringwithspaces"**, the filter has cut out spaces from the value.

~~~{.html caption=""}
<!--  the value  -->
"Python is Fun" | cut:" "

~~~

~~~{.html caption=""}

'PythonisFun'

~~~

~~~{.html caption=""}
<!--  the value  -->
"January - February - March" | cut:"-"

~~~

~~~{.html caption=""}

'January February March'

~~~

### Dictsort Filter

The dictsort filter is used to sort a list of dictionaries and returns that list *sorted by the key* specified as the argument.

Here's the syntax to use the dictsort filter: `{% raw %}{{ value | dictsort:"name" }}{% endraw %}`

If the value is:

~~~{.html caption=""}
[
    {'name': 'Josh', 'age': 19},
    {'name': 'Dave', 'age': 22},
    {'name': 'Joe', 'age': 31},
]
~~~

Then the output would be:

~~~{.html caption=""}

[
{'name': 'Dave', 'age': 22},
{'name': 'Joe', 'age': 31},
{'name': 'Josh', 'age': 19},

]
~~~

You will notice that the dictionary was sorted by 'name' and 'Dave' being the lowest in the [character order](http://support.ecisolutions.com/doc-ddms/help/reportsmenu/ascii_sort_order_chart.htm) was moved to the top of the list.

~~~{.html caption=""}
<!--  the value  -->
[
   {'name': 'Abhi', 'age': 29},
   {'name': 'Sonia', 'age': 25},
   {'name': 'Rahul', 'age': 36},
]

~~~

~~~{.html caption=""}

[
   {'name': 'Abhi', 'age': 29},
   {'name': 'Rahul', 'age': 36},
   {'name': 'Sonia', 'age': 25},
]

~~~

### Escape Filter

The escape filter is used to escape a string's HTML. Specifically, it makes these replacements:

~~~{.html caption=""}

< is converted to &lt;
> is converted to &gt;
' (single quote) is converted to &#x27;
" (double quote) is converted to &quot;
& is converted to &amp;

~~~

Here's the syntax to use the escape filter: `{% raw %}{{ value | escape }}{% endraw %}`.

If the value is **`<p>You are <em>pretty</em> smart!</p>`**, the output will be **`<p>You are <em>pretty</em> smart!</p>`**. Without escaping it, the output will be, "You are pretty smart!".

~~~{.html caption=""}
<!--  the value -->
<p>This <em>should be</em> fun!</p> | escape
~~~

~~~{.html caption=""}
<p>This <em>should be</em> fun!</p>
~~~

### First Filter

The first filter is used to get the first item in a list.

Here's the syntax to use the first filter: `{% raw %}{{ value | first }}{% endraw %}`

If the value is **['Jane', 'Janet', 'Joe']**, the output will be **'Jane'**.

~~~{.html caption=""}
<!--  the value -->
 ['Apple', 'Mango', 'Orange'] | first
~~~

~~~{.html caption=""}
'Apple'
~~~

~~~{.html caption=""}
<!--  the value -->
 ['China', 'India', 'Thailand'] | first
~~~

~~~{.html caption=""}
'China'
~~~

### Last Filter

The last filter is used to get the last item in a list.  

Here's the syntax to use the last filter: `{% raw %}{{ value | last }}{% endraw %}`

If the value is **['Jane', 'Janet', 'Joe']**, the output will be **Joe**.

~~~{.html caption=""}
<!--  the value -->
 ['Apple', 'Mango', 'Orange'] | last
~~~

~~~{.html caption=""}
'Orange'
~~~

~~~{.html caption=""}
<!--  the value -->
 ['China', 'India', 'Thailand'] | last
~~~

~~~{.html caption=""}
'Thailand'
~~~

### Length Filter

The length filter is used to return the length of the value. This works for both strings and lists.

Here's the syntax to use the length filter: `{% raw %}{{ value | length }}{% endraw %}`

If the value is **['a', 'b', 'c', 'd']** or "**abcd"**, the output will be **4**.

~~~{.html caption=""}
<!--  the value -->
 ['Banana', 'Mango', 'Orange'] | length
~~~

~~~{.html caption=""}
3
~~~

~~~{.html caption=""}
<!--  the value -->
 "Welcome" | length
~~~

~~~{.html caption=""}
7
~~~

### Linenumbers Filter

The linenumbers filter is used to display text with line numbers.

Here's the syntax to use the linenumbers filter: `{% raw %}{{ value | linenumbers }}{% endraw %}`.

If the value is:

~~~{.html caption=""}
cat
dog
horse
~~~

The output will be:

~~~{.html caption=""}
1. cat
2. dog
3. horse
~~~

If the value is:

~~~{.html caption=""}
Arnold
Brandy
Caleb
Dexter
~~~

The output will be:

~~~{.html caption=""}
1. Arnold
2. Brandy
3. Caleb
4. Dexter
~~~

### Lower Filter

The lower filter is used to convert a string to lowercase. This will return a new string in lowercase.

Here's the syntax to use the lower filter: `{% raw %}{{ value | lower }}{% endraw %}`.

If the value is **"I Am Groot"**, the output will be "**i am groot"**.

~~~{.html caption=""}
<!--  the value -->
'I Am Master Yoda' | lower
~~~

~~~{.html caption=""}
 'i am master yoda '
~~~

~~~
<!--  the value -->
'Humpty Dumpty sat on the Wall' | lower
~~~

~~~{.html caption=""}
 'humpty dumpty sat on the wall'
~~~

### Upper Filter

The upper filter is used to convert a string to uppercase. This will return a new string in upper case.

Here's the syntax to use the upper filter: `{% raw %}{{ value | upper }}{% endraw %}`.

If the value is **"Moe is a slug"**, the output will be **"MOE IS A SLUG"**.

~~~{.html caption=""}
<!--  the value -->
'Happy coding!' | upper
~~~

~~~{.html caption=""}
'HAPPY CODING!'
~~~

~~~{.html caption=""}
<!--  the value -->
'Nasa' | upper
~~~

~~~{.html caption=""}
'NASA'
~~~

### Title Filter

The title filter is used to format a string in the title case. The first letter of each word is capitalized.

Here's the syntax to use the title filter: `{% raw %}{{ value | title }}{% endraw %}`.

If the value is **"I LOVE dogs"**, the output will be **"I Love Dogs"**.

~~~{.html caption=""}
<!--  the value -->
'It's a new day' | title
~~~

~~~{.html caption=""}
'It's A New Day'
~~~

~~~{.html caption=""}
<!--  the value -->
'Django rest framework' | title
~~~

~~~{.html caption=""}
'Django Rest Framework'
~~~

### Random Filter

The random filter is used to return a random item from the given list.

Here's the syntax to use the random filter: `{% raw %}{{ value | random }}{% endraw %}`.

If the value is the list **['a', 'b', 'c', 'd']**, the output could be **"b"** or  **"d"** or  **"a"**.

~~~{.html caption=""}
<!--  the value -->
['Banana', 'Mango', 'Orange'] | random
~~~

~~~{.html caption=""}
'Banana or Mango or Orange'
~~~

~~~{.html caption=""}
<!--  the value -->
['Father', 'Mother', 'Child'] | random
~~~

~~~{.html caption=""}
'Father or Mother or Child'
~~~

### Slice Filter

The slice filter is used to return a slice of the given list. This filter will cut off a part of the list from the given index and returns a new list.

Here's the syntax to use the slice filter: `{% raw %}{{ some_list | slice:":2" }}{% endraw %}`.

If `some_list` is **['a', 'b', 'c'],** the output will be **['a', 'b']**.

~~~{.html caption=""}
<!--  the value -->
['Banana', 'Mango', 'Orange'] | slice:":2"
~~~

~~~{.html caption=""}
['Banana', 'Mango']
~~~

~~~{.html caption=""}
<!--  the value -->
['Father', 'Mother', 'Child'] | slice:":2"
~~~

~~~{.html caption=""}
['Father', 'Mother'] 
~~~

### Time Filter

The time filter is used to format time according to the given format. The given format can be the predefined TIME_FORMAT or a custom format.

Here's the syntax to use the time filter: `{% raw %}{{ value | time:"H:i" }}{% endraw %}`.

If the value is equivalent to **datetime.datetime.now()**, the output will be the string **"01:23"**.

~~~{.html caption=""}
<!--  the value -->
10:30:00.000123+02:00 | time:"H:i"
~~~

~~~{.html caption=""}
"10:30"
~~~

~~~{.html caption=""}
<!--  the value -->
12:30:00.000123+02:00 | time:"H\h i\m"
~~~

~~~{.html caption=""}
"12h 30m"
~~~

### Timesince Filter

The timesince filter is used to format a date as the time since that date (for example, "5 days, 4 hours").

This filter also takes an *optional* argument that is a variable containing the date to use as the comparison point (without the argument, the comparison point is **now**).

Here's an example that uses the timesince filter:

~~~{.html caption=""}
{% raw %} {{ publication_date | timesince:comment_date }} {% endraw %}
{% raw %} {{ publication_date | timesince }} {% endraw %}
~~~

If `publication_date` is a date instance representing midnight on 1 December 2022, and `comment_date` is a date instance for 09:00 on 1 December 2022, then the output would be **"9 hours"**.

~~~{.html caption=""}
<!--  the value -->
2022-01-02T10:30:00.000123 | timesince
~~~

~~~{.html caption=""}
'2 hours'
~~~

~~~{.html caption=""}
<!--  the value -->
2023-01-02T9:30:00.000123 | timesince
~~~

~~~{.html caption=""}
'3 hours'
~~~

### Truncatechars Filter  

The truncatechars filter is used to truncate a string if it is longer than the specified number of characters. Truncated strings will end with an ellipsis character (...).

Here's how you can use the truncatechars filter: `{% raw %}{{ value | truncatechars:7 }}{% endraw %}`.

If the value is **"Moe is a slug"**, the output will be **"Moe is…"**.

~~~{.html caption=""}
<!--  the value -->
'Happy coding' | truncatechars:6
~~~

~~~{.html caption=""}
'Happy…'
~~~

~~~{.html caption=""}
<!--  the value -->
'Cloud computing' | truncatechars:5
~~~

~~~{.html caption=""}
'Cloud…'
~~~

### Reviewing What We've Learned So Far

Let's quickly review some of the most helpful filters before we proceed to learn about more filters. If we were building a news web app, we could use a combination of various Django template filters to transform our data in the HTML templates.

For example, we could use the timesince filter to display the time since the publication of a news story. You will find this feature in top news websites where you see timestamps as "1 hour ago", "2 hours ago", "3 hours ago", etc.

If a piece of news was published at 10 AM on 1 January 2023, and you are reading it at 12 PM on 1 January 2023, then the date and time of the article will be "2 hours" ago.

~~~{.html caption=""}
<!--  the value -->
2023-01-01T10:00:00.000123 | timesince
~~~

~~~{.html caption=""}
'2 hours'
~~~

~~~{.html caption=""}
<!--  the value -->
"Microsoft unveils new Bing with ChatGPT powers" | upper
~~~

~~~{.html caption=""}
"MICROSOFT UNVEILS NEW BING WITH CHATGPT POWERS"
~~~

As you can see, these are some of the ways you could use template filters to transform data in your HTML and build reusable templates in your project.

## Other Template Filters

In this previous section, we have looked at some of the most popular Django template filters. But there are still some more filters that might come in handy in your next project, and we will be looking at some of those in this section.

### Wordcount Filter  

The wordcount filter returns the number of words in a string.

Here's the syntax to use the wordcount filter: `{% raw %}{{ value | wordcount }}{% endraw %}`.

If the value is **"Moe is a cat"**, the output will be **4**.

~~~{.html caption=""}
<!-- the value  -->
'Happy coding' | wordcount
~~~

~~~{.html caption=""}
2
~~~

~~~{.html caption=""}
<!-- the value  -->
'You can do a lot of modifications with template filters' | wordcount
~~~

~~~{.html caption=""}
10
~~~

### Truncatewords Filter

The truncatewords filter is used to truncate a string after a certain number of words. This is similar to the truncatechars filter and it will be useful if you prefer to truncate by words instead of characters.

You can use the truncatewords filter: `{% raw %}{{ value | truncatewords:3 }}{% endraw %}`.

If the value is "**Joseph is a software engineer"**, the output will be **"Joseph is a …"**

~~~{.html caption=""}
<!--  the value -->
"Better days ahead!" | truncatewords:2
~~~

~~~{.html caption=""}
"Better days"
~~~

~~~{.html caption=""}
<!--  the value -->
"You can build web apps with python and Django" | truncatewords:7
~~~

~~~
"You can build web apps with python"
~~~

### Striptags Filter

The striptags is used to remove all [X]HTML tags from the value it is piped against. This will be useful if you want to convert HTML data into a string.

Here's the syntax to use the striptags filter: `{% raw %}{{ value | striptags }}{% endraw %}`.

If the value is **"<b>Joseph</b> <button>is</button> a <span>developer</span>"**, the output will be **"Joseph is a developer"**.

~~~{.html caption=""}
<!--  the value -->
<b>I</b> <button>love</button> <span>dogs</span> | striptags
~~~

~~~{.html caption=""}
'I love dogs'
~~~

~~~{.html caption=""}
<!--  the value -->
<b>This</b> is <em>a</em> <button>Button</button> | striptags
~~~

~~~{.html caption=""}
'This is a Button'
~~~

### Pluralize Filter

The pluralize filter is used to return a plural suffix if the value is not 1, '1', or an object of length 1. By default, this suffix is 's'.

You can use the pluralize filter as shown:

~~~{.html caption=""}
You have {% raw %}{{ num_messages }}{% endraw %} message {% raw %}{{ num_messages | pluralize }}{% endraw %}.
~~~

If `num_messages` is 1, the output will be **You have 1 message**. If `num_messages` is 2 the output will be **You have 2 messages**.

For words that require a suffix other than 's', you can provide an alternate suffix as a parameter to the filter.

Here's how you can use other suffixes with the pluralize filter:

~~~{.html caption=""}
You have {% raw %}{{ num_tomato }}{% endraw %} tomato {% raw %}{{ num_tomato | pluralize:"es" }}{% endraw %}.
~~~

For words that cannot be pluralized by a simple suffix, you can specify both a singular and plural suffix, separated by a comma.

~~~{.html caption=""}
You have {% raw %}{{ num_cherries }}{% endraw %} cherr {% raw %}{{ num_cherries | pluralize:"y,ies" }}{% endraw %}.
~~~

~~~{.html caption=""}
<!--  the value -->
You have {% raw %}{{ num_messages }}{% endraw %} message {% raw %}{{ num_messages | pluralize }}{% endraw %}.
~~~

~~~{.html caption=""}
"You have 4 messages"
~~~

### Make_list Filter  

The make_list filter is used to turn a value into a list. For a string, it's a list of characters. For an integer, the argument is cast to a string before creating a list.

Here's the syntax to use the make_list filter: `{% raw %} {{ value | make_list }} {% endraw %}`.

If the value is the string **"Ronaldo"**, the output would be the list **['R', 'o', 'n', 'a', 'l', 'd','o']**. If the value is **1234**, the output will be the list **['1', '2', '3', '4']**.

~~~{.html caption=""}
<!--  the value -->
'Earthly' | make_list
~~~

~~~{.html caption=""}
['E', 'a', 'r', 't', 'h', 'l', 'y']
~~~

~~~{.html caption=""}
<!--  the value -->
'ABCDEF' | make_list
~~~

~~~{.html caption=""}
['A', 'B', 'C', 'D', 'E', 'F']
~~~

### Summing Up With a Quick Example

Let's code an example to put together what we've learned in this section. If you are building a [blog](/blog/top-5-scala-blogs) homepage or an archive page, you can use the "truncatewords" filter to display excerpts on your home or archive page instead of showing the entire article.

For example, we can create an excerpt from the long texts below using the **truncatewords** filter.

~~~{.html caption=""}
<!--  the value -->
"I remember as a child, and as a young budding naturalist, spending \
all my time observing and testing the world around me—moving pieces, \
altering the flow of things, and documenting ways the world responded \
to me. Now, as an adult and a professional naturalist, I've approached 
language in the same way, not from an academic point of view but as a \
curious child still building little mud dams in creeks and chasing after \
frogs. So this book is an odd thing: it is a naturalist's walk through the \
language-making landscape of the English language, and following in \
the naturalist's tradition it combines observation, experimentation, \
speculation, and documentation—activities we don't normally \
associate with language." | truncatewords:36 
~~~

~~~{.html caption=""}
"I remember as a child, and as a young budding naturalist, \
spending all my time observing and testing the world around \
me—moving pieces, altering the flow of things, and documenting ways \
the world responded to me."
~~~

## How to Create a Custom Template Filter

![Create]({{site.images}}{{page.slug}}/create.png)\

Sometimes, the built-in template filters may not meet your exact needs, so Django also allows you to create custom template filters. You can easily create your own custom template filters that can be used anywhere in your templates.

In this section, I'll assume you have a working knowledge of Django and that you can create a Django project and a Django app.

I will be using a "blog" app with an articles model as an example in this tutorial, created by running the following command:

~~~{.bash caption=">_"}
python3 manage.py startapp blog 
~~~

Make sure you have added the **app name** in settings.py inside **INSTALLED_APPS**.
Now follow the steps below to create your Django custom template filter.

### Step 1: Create a "templatetags" Directory

The first thing to do is to create a templatetags directory in our [blog](/blog/top-5-scala-blogs) app, this directory can reside in any of your Django apps top-level directories. i.e. the same place where you have "models.py" or "views.py"

### Step 2: Create the `__init__.py` file

The templatetags directory created above needs to be treated as a Python package and to do that, we need to create an `__init__.py` in this directory. Do not add any code or content to this file.

<div class="wide">
![Folder structure]({{site.images}}{{page.slug}}/sCmO76o.png)
</div>

### Step 3: Create the Custom Filter Python File - `titlecolor_filter.py`

We are creating a custom filter that will change the color of our post titles to red, so we will name it titlecolor_filter.py.
Inside this file, paste the code below in it.

~~~{.pyhton caption="titlecolor_filter.py"}
from django import template

register = template.Library()

@register.filter()
def title_color(value):
    if value:
        return "#FF0000"
~~~

In the code above, we imported the Django template module. Before our custom filter can be a valid filter, we need to have a module-level variable named "register" which is a template library instance in which all tags and filters are registered.

Then we register our filter by using the `register.filter()` decorator on the `title_color()` function.
A decorator is a function that takes another function as an argument and adds functionality to the function without modifying the function itself.

### Step 4: Create HTML Template

Create an HTML template called "blog.html" in your app templates folder with the code below.

~~~{.html caption="blog.html"}
{% raw %} {% extends 'base.html' %}  {% endraw %}
{% raw %} {% load titlecolor_filter %} {% endraw %}

        <div class="col-lg-7">
            <div class="container">
              <!-- the actual blog post: title/author/date/content -->
              <div style="color: {% raw %}{{article.title | title_color}} {% endraw %};"> \
               <h1> {% raw %}{{article.title}}{% endraw %} </h1> </div>
              <hr>
              <p> <i class="fa fa-calendar"></i> \
              Published on {% raw %}{{article.date_posted|date}}{% endraw %}</p>
              <hr>
            <p>{% raw %}{{article.content}}{% endraw %}</p>
          </div>
        </div>
~~~

<div class="wide">
![Blog post title in Red color]({{site.images}}{{page.slug}}/sqSMt6Y.png)
</div>

To be able to use our custom filter in a template, the first thing to do is to load our custom filter module at the top of the template HTML file as shown above with the `{% raw %} {% load titlecolor_filter %} {% endraw %}` tag.

Once the module is loaded, we can now apply our custom filter using the pipe operator inside double braces `{% raw %} {{ variable | filter_name }} {% endraw %}` as shown above.
The filter name is the name of the function in our **"titlecolor_filter.py"** module.

## Conclusion

Django template filters spice up your HTML templates. We've dived into Django's built-in filters and how to create a custom one if you need something special. You're now equipped to use these filters and even make your own.

Want to streamline your Django build process further? Give [Earthly](https://cloud.earthly.dev/login) a go! It's a tool that can help optimize your build process, making it more efficient and less error-prone.

{% include_html cta/bottom-cta.html %}
