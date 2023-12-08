---
title: "Python Concatenate Lists"
description: "There are several ways to join lists in Python. In almost all situations using list1 + list2 is the way you want to concatenate lists." 
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - python list
 - python concatenate
 - concatenate
 - concate
excerpt: |
    Learn how to concatenate lists in Python using different methods, such as the `+` operator and the `extend()` function. Discover the best practices for combining lists and optimize performance in various scenarios.
last_modified_at: 2023-07-14
---
**In this article, you'll discover how to merge lists in Python. If you're a Python developer, Earthly provides a containerized solution to simplify your build processes. [Learn More](https://cloud.earthly.dev/login).**

<iframe width="560" height="315" src="https://www.youtube.com/embed/Ko6OESfhxbw" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

<div class="narrow-code">

## Concatenate Two Lists in Python

**Problem:** You have two lists and you'd like to join them into a new list.
Solution:

~~~{.python caption=""}
Python 3.8.2
>>> one = ["one","two", "three"]
>>> two = ["four","five"]
>>> one + two
['one', 'two', 'three', 'four', 'five']
~~~

<div class="notice--warning notice--big">

### 📢 TLDR: Use `+`

In almost all simple situations, **using `list1 + list2` is the way you want to concatenate lists**.
</div>
The edge cases below are better in some situations, but `+` is generally the best choice. All options covered work in Python 2.3, Python 2.7, and all versions of Python 3[^1].

## Combine Lists In Place In Python

**Problem:** You have a huge list, and you want to add a smaller list on the end while minimizing memory usage.

In this case, it may be best to append to the existing list, reusing it instead of recreating a new list.

~~~{.python caption=""}
>>>longlist = ["one","two", "three"] * 1000
['one', 'two', 'three', 'one', 'two', 'three', ... ]
>>>shortlist = ["four","five"]
["four","five"]
>>> x.extend(y)
>>> x
['one', 'two', 'three', 'one',  ..., "four","five"]
~~~

As with any optimization, you should verify that this reduces memory thrash in your specific case and stick to the simple idiomatic `x + y` otherwise.

Let's use the [`timeit`](https://docs.python.org/3/library/timeit.html) module to check some performance numbers.

~~~{.python caption=""}
# Performance Check
>>> setup = """\
x = ["one","two","three"] * 1000 
y = ["four","five","six"]
"""
# x + y with large x
>>> timeit.timeit('x + y', setup=setup, number=1000000)
3.6260274310000113
# x.extend(y) with large x
>>> timeit.timeit('x.extend(y)', setup=setup, number=1000000)
0.06857255800002804
~~~

In this example, where x is 3000 elements, extend is around 50x faster.

<div class="notice--info">

### ❗ Concatenating Lists With Huge Elements is Fine

If the elements in your list are huge (million character strings), but the list size is less than a thousand elements, the previous solution `x + y` will work just fine. This is because Python stores references to the values in the list, not the values themselves. Thus, the element size makes no difference to the runtime complexity.

~~~{.python caption=""}
>>> x = ["one" * 1000, "two" * 1000, "three" * 1000]
>>> y = ["four" * 1000, "five" * 1000]
>>> #This is fine
>>> z = x + y
>>> #Performance Testing (extend is slower for large elements)
>>>  setup = """\
x = ["one" * 1000, "two" * 1000, "three" * 1000]
y = ["four" * 1000, "five" * 1000]
"""
>>> timeit.timeit('x + y', setup=setup, number=1000000)
0.05397573999994165
>>> timeit.timeit('x.extend(y)', setup=setup, number=1000000)
0.06511967799997365
~~~

In this case, `extend` does not have an advantage.

</div>

### Avoid Chain From `itertools` For Two Lists

It is possible to use `chain` from `itertools` to create an iterable of two lists.

~~~{.python caption=""}
>>>longlist = ["one","two", "three"] * 1000
['one', 'two', 'three', 'one', 'two', 'three',, .......... ]
>>>shortlist = ["four","five"]
["four","five"]
>>> from itertools import chain
>>> z = list(chain(longlist, shortlist)
['one', 'two', 'three', 'one', , .........., "four","five"]
~~~

We can check the performance of using chain:

~~~{.python caption=""}
>>> setup = """\
from itertools import chain
x = ["one","two","three"] * 1000 
y = ["four","five","six"]
"""
# x + y with large x
# x.extend(y) with large x
>>> timeit.timeit('x.extend(y)', setup=setup, number=1000000)
0.06857255800002804
>>> timeit.timeit('list(chain(x, y))', setup=setup, number=1000000)
16.810488051999982
~~~

Using `chain` with two lists is slower in all cases tested, and `x + y` is easier to understand.

## Combining N Lists in Python

If you need to add three or even ten lists together and the lists are statically known, then `+` for concatenate works great.

~~~{.python caption=""}
>>> one = ["one","two", "three"]
>>> two = ["four","five"]
>>> three = []
>>> z = one + two + three
~~~

## Flatten a List of Lists in Python

However, if the number of lists is dynamic and unknown until runtime, `chain` from `itertools` becomes a great option. Chain takes a list of lists and flattens it into a single list.

~~~{.python caption=""}
>>> l = [["one","two", "three"],["four","five"],[]] * 99
[['one', 'two', 'three'], ['four', 'five'], [], ...
>>> list(chain.from_iterable(l))
['one', 'two', 'three', 'four', 'five', 'one', 'two', ... ]
~~~

`chain` can take anything iterable, making it an excellent choice for combining lists, dictionaries, and other iterable structures.

~~~{.python caption=""}
>>> from itertools import chain
>>> one = [1,2,3]
>>> two = {1,2,3}
>>> list(chain(one, two, one))
[1, 2, 3, 1, 2, 3, 1, 2, 3]
~~~

### Performance of Flattening a List of Lists

Performance doesn't always matter, but readability always does, and the chain method is a straightforward way to combine lists of lists. That said, let's put readability aside for a moment and try to find the fastest way to flatten lists.

One option is iterating ourselves:

~~~{.python caption=""}
result = []
for nestedlist in l:
    result.extend(nestedlist)
~~~

Let's check its performance vs chain:

~~~{.python caption=""}
>>> setup = """\
from itertools import chain
l = [["one","two", "three"],["four","five"],[]] * 99
"""
>>> # Add Nested Lists using chain.from_iterable
>>> timeit.timeit('list(chain.from_iterable(l))', setup=setup, number=100000)
1.0384087909997106
>>> ### Add using our own iteration
>>> run = """\
result = []
for nestedlist in l:
    result.extend(nestedlist)  
"""
>>> timeit.timeit(run, setup=setup, number=100000)
1.8619721710001613

~~~

This shows that `chain.from_iterable` is faster than extend.

## Flattening and Merging Lists With One Big List

What about adding a list of lists to an existing and large list? We saw that using extend can be faster with two lists when one is significantly longer than the other so let's test the performance of `extend` with N lists.

First, we use our standard `chain.from_iterable`.

~~~{.python caption=""}
>>> # Method 1 - chain.from_iterable 
>>> longlist = ["one","two", "three"] * 1000
>>> nestedlist = [longlist, ["one","two", "three"],["four","five"],[]]
>>> list(chain.from_iterable(nestedlist))
~~~

We then test its performance:

~~~{.python caption=""}
>>> setup = """\
from itertools import chain
longlist = ["one","two", "three"] * 1000;
combinedlist = [longlist, ["one","two", "three"],["four","five"],[]]
"""
>>> timeit.timeit('list(chain.from_iterable(combinedlist))', setup=setup, number=100000)
1.8676087710009597
~~~

Next, let's try concatenating by adding everything onto the long list:

~~~{.python caption=""}
>>> # Method 2 - extend
>>>  longlist = ["one","two", "three"] * 1000
>>>  nestedlist = [["one","two", "three"],["four","five"],[]]
>>>  for item in nestedlist:
>>>     longlist.extent(item)
~~~

Performance Test:

~~~{.python caption=""}
>>> setup = """\
from itertools import chain
longlist = ["one","two", "three"] * 1000;
nestedlist = [["one","two", "three"],["four","five"],[]]
"""
>>> run = """\
for item in nestedlist:
   longlist.extend(item)
   """
>>> timeit.timeit(run, setup=setup, number=100000) 
0.02403609199973289
~~~

There we go, `extend` is much faster when flattening lists or concatenating many lists with one long list. If you encounter this, using `extend` to add the smaller lists to the long list can decrease the work that has to be done and increase performance.

## Summary

These are the main variants of combining lists in python. Use this table to guide you in the future.

Also, if you are looking for a nice way to standardize the processes around your python projects -- running tests, installing dependencies, and linting code -- take a look at Earthly for [Repeatable Builds](https://cloud.earthly.dev/login).

|  Condition  |  Solution  | Performance Optimization[^2]   |
|--- |--- |:-: |
| 2 lists   | `x + y`   |   No  |
| 1 large list, 1 small list   | `x.extend(y)`  |   Yes   |
| Known number of N lists   | `x + y + z`   |   No  |
| Unknown number of N lists | `list(chain.from_iterable(l))`   |   No  |
| List of Lists    |  `list(chain.from_iterable(l))`     |  No  |
| 1 large list, many small lists    |  `for l1 in l: x.extend(...)`  |   Yes  |

[^1]: I did all the performance testing using Python 3.9.5 on MacOS BigSur.
[^2]: If you don't have a performance bottleneck, clarity trumps performance, and you should ignore the performance suggestions.
</div>
