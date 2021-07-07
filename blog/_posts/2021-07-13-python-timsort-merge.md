---
title: "Beating TimSort at Merging"
categories:
  - Tutorials
author: Adam
internal-links:
 - python
 - performance
 - timsort
 - list merging
---
<div class="narrow-code">

Here is a problem. You are tasked with improving the hot loop of a python program: maybe it is an in-memory sequential index of some sort. The slow part is the updating, where you are adding a new sorted list of items to the already sorted index. You need to combine two sorted lists and keep the result sorted. How do you do that update?

Yes, this sounds like a leetcode problem and maybe in the realworld you would reach for some existing [sortedset]() [datastructure](), but if you were working with python lists you might do something like this:

``` Python
def merge_sorted_lists(l1, l2):
    sorted_list = []

    while (l1 and l2):
        if (l1[0] <= l2[0]): # Compare both heads
            item = l1.pop(0) # Pop from the head
            sorted_list.append(item)
        else:
            item = l2.pop(0)
            sorted_list.append(item)

    # Add the remaining of the lists
    sorted_list.extend(l1 if l1 else l2)

    return sorted_list

```

Python has a builtin method that does with in [heapq.merge](https://github.com/python/cpython/blob/3.7/Lib/heapq.py#L314). It nicely takes advantage of the fact that both our lists are already sorted, so we can get a new sorted list linear time rather than the n log n time it would take for combining and sorting two unsorted lists.

Imagine my surprise then when I saw this performance graph from Stack Overflow:

<div class="wide">
{% picture content-wide {{site.pimages}}{{page.slug}}/performance-sort1.png --picture --alt {{ Python sort is beating merge }} %}
<figcaption>Python's sort is beating merge at merging sorted lists!</figcaption>
</div>

Sorting the list is faster than just merging the list in almost all cases!  That doesn't sound right but I checked it and it's true. As Stack Overflow user [JFS](https://stackoverflow.com/users/4279/jfs) puts it:

> Long story short, unless len(l1 + l2) ~ 1000000 use sort

The reason this sort is so fast is because of a man named Tim Peters.

## TimSort

Python's `list.sort` is the original implementation of a hybrid sorting algorithm called TimSort which is named after its author Tim Peters.

> \[Here is\] stable, natural mergesort, modestly called
timsort (hey, I earned it <wink>). It has supernatural performance on many
kinds of partially ordered arrays (less than lg(N!) comparisons needed, and
as few as N-1), yet as fast as Python's previous highly tuned samplesort
hybrid on random arrays.

<figcaption>Tim Peters explaining [TimSort](https://github.com/python/cpython/commit/92f81f2e63b5eaa6d748d51a10e32108517bf3bf#diff-6d09fc0f0b57214c2e3a838d366425836c296fa931fe9dc430f604b7e3950c29)</figcaption>

Timsort is designed to find runs of sequential numbers and merge them together:

> The main routine marches over the array once, left to right,
alternately identifying the next run, then merging it into the previous
runs "intelligently". Everything else is complication for speed, and some
hard-won measure of memory efficiency.

This is why `list(x + y).sort()` can be surprizingly fast: once it finds the sequiential runs of numbers it is functioning just like our merge algorithm, combining the two sorted lists in linear time.

Timsort have to do extra work though. It needs to do a pass over the data to find these sequential runs. We know where the runs are ahead of time but it overcomes this disadvantage by being written in C rather than Python. Or as ShawdowRanger on Stack Overflow explains it:

> CPython's list.sort is implemented in C (avoiding interpreter overhead), while heapq.merge is mostly implemented in Python, and optimizes for the "many iterables" case in a way that slows the "two iterables" case.

This means that is should be possible for me to write a merge that beats Timsort if I drop down to C and write a c extension. This turned out to be easier than I thougth it would be[^1].

## The C Extension

The bulk of the C Extension, whose performance I'm going to cover in a minute, was just the pop the stack algorithm discussed before:

``` c
  //New List
  PyObject* mergedList = PyList_New( n1 + n2 );

 for( i = 0;; ) {
  elem1 = PyList_GetItem( listObj1, i1 );
  elem2 = PyList_GetItem( listObj2, i2 );
  result = PyObject_RichCompareBool(v, w, Py_LT);
  switch( result ) {
    // List1 has smallest, Pop from list 1
  case 1:
   PyList_SetItem( mergedList, i++, elem1 );
   i1++;
   break;

  case 0:
      // List2 has smallest, Pop from list 2
   PyList_SetItem( mergedList, i++, elem2 );
   i2++;
   break;
  }
  if( i2 >= n2 || i1 >= n1 )) {
   //One list is empty, add remainder of other list to result
   ...
   break;
  }
 }
 return mergedList;

```

<figcaption>C merge ([full and final version on github]())</figcaption>

The nice thing about C extensions is they are just pips. I have it compiler and published and now can use it just like this: `pip install tim-merge`:

``` Python
import merge

# create some sorted lists
a = list(range(-100, 1700))
b = list(range(1400, 1800))

# merge them
merge.merge(a, b)
```

## Testing It

Testing my new merge with a list of ints and floats, we can see that we are beating Timsort, especially for long lists:

``` Python
import merge
import timeit

a = list(range(-100, 1700)) + [0.1]
b = list(range(1400, 1800))

def merge_test():
   m1 = merge.merge(a, b)

def sort_test():
   m2 = list(a + b)
   m2.sort()

sort_time = timeit.timeit("sort_test()", setup="from __main__ import sort_test", number=100000)
merge_time = timeit.timeit("merge_test()", setup="from __main__ import merge_test",number=100000)

print(f'timsort took {sort_time} seconds')
print(f'merge took {merge_time} seconds')
```

``` bash
timsort took 3.9523325259999997 seconds
merge took 3.0547665259999994 seconds
```

Graphing the performance we get this:

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/beating-with-hetro1.png --picture --alt {{ Our Merge beating TimSort }} %}
<figcaption>We are beating timsort with our merge</figcaption>
</div>

But if we switch to a list of only integers `sort` is beating us for small lists and even on big lists our performance improvement is thin at best:

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/losing-with-homo.png --picture --alt {{ Our Merge beating TimSort }} %}
<figcaption>With lists of all `int` or all `float` we lose our advantage.</figcaption>
</div>
What is going on here?

## Timsort's Special Comparisons

It turns out that Timsort has some extra tricks up its sleves in the case of a list of integers. In that initial pass over the list it, checks the types of the elements and if they are all of the uniform it tries to use a cheaper comparison operation.

Specifically, if your list is all [longs](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2085), [floats](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2113), or [latin strings](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2061) Timsort will save a lot of cycles on the comparison operations.

Learning from Timsort we can bring in these comparison operations ourselves. We don't want to do a full pass over the list, or we will lose our advantage, so we can just specialize our merge by offering seperate calls for longs, floats, and latin alphabet strings like so:

``` c
//Default comparison
PyObject* merge( PyObject*, PyObject* );

//Compare assuming ints
PyObject* merge_int( PyObject*, PyObject* );

//Compare assuming floats
PyObject* merge_float( PyObject*, PyObject* );

//Compare assuming latin
PyObject* merge_latin( PyObject*, PyObject* )
```

<figcaption>merge.h</figcaption>

## Beating TimSort

Doing that, we now can finally beat Timsort at merging sorted lists, not just when the list is a heterogeneous mix of elements, but also when its all integers, or floating point numbers or one byte per char strings.

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/summary1-int.png --picture --alt {{ Our Merge beating TimSort }} %}
<figcaption>merge vs TimSort for `int`.</figcaption>
</div>

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/summary2-float.png --picture --alt {{ Our Merge beating TimSort }} %}
<figcaption>merge vs TimSort for `float`.</figcaption>
</div>

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/summary3-latin.png --picture --alt {{ Our Merge beating TimSort }} %}
<figcaption>merge vs TimSort for latin alphabet strings.</figcaption>
</div>

<div class="wide">
{% picture {{site.pimages}}{{page.slug}}/summary4-else.png --picture --alt {{ Our Merge beating TimSort }} %}
<figcaption>merge vs TimSort for everything without a specialized compare.</figcaption>
</div>

The default `merge` beats Timsort for heterogeneous lists, and the specialized versions are there for when you have uniform types in your list, and you need to go fast.

## TimSort Is Good

There, I have beat Timsort for merging sorting lists, although I had to pull in some code from it to get here.

Also, I learned that dropping down to C isn't as scary as it sounds. The build steps are a bit more involved but with the included [earthfile]() the build is a one liner and cross platform. This process is adaptable to any other python c extension. You can find the full code [on github]() and an intro to [earthly]() on this very site.

The surprising thing, though is how good Timsort still is, it wasn't designed for merging sorted lists but for sorting real-world data. It turns out real-world data is often partially sorted.

Timsort on partially sorted data shows us where Big O notation can lead us astray. If your input always keeps you near the median or best-case performance then the worse-case performance doesn't matter much. It's no wonder then that since its first creation TimSort has spread from Python to JavaScript, Swift, and Rust. Thank you, Tim Peters!

[^1]: It was easier because my teammate Alex has experience writing C extensions for Python, so by the time I had found the Python header files, Alex had already put together a prototype solution.

### Writing Article Checklist

- [ ] Fix Grammarly Errors
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

</div>
