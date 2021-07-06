---
title: "Beating TimSort at Merging"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---
### Writing Article Checklist

- [ ] Write Outline
- [ ] Write Draft
- [ ] Fix Grammarly Errors
- [ ] Read out loud
- [ ] Write 5 or more titles and pick the best on
- [ ] Create header image in Canva
- [ ] Optional: Find ways to break up content with quotes or images
- [ ] Verify look of article locally
- [ ] Run mark down linter (`earthly +blog-lint-apply`)
- [ ] Add keywords for internal links to front-matter
- [ ] Run `earthly --build-arg NAME=2020-09-10-better-builds.md +link-opportunity` and find 1-5 places to incorporate links to other articles
- [ ] Raise PR

# Outline
## Imagine the problem
Here is a problem. You are tasked with improving the hot loop of a python program. Maybe it is an in-memory sequential index of some sort. The slow part is the updating where add a new sorted list of items to add to the already sorted index. How do you do that update?

Yes, this sounds like a leetcode problem and maybe in the realworld you would reach for some existing but [sortedset]() [datastructure]() but if you were working with python lists you might do somehting like this :
```
Given:
n1 = [1,4,8,12,24 ...]
n2 = [3,7,9]

Create n3 of size n1+n2
Treat n1 and n2 like a stack
Compare the head of each, and pop the smallest one off, adding it to n3
Repeat until done
```
We should get something like this:
```
n3 = [1,3,4,7,8,9,12.24 ...]
```
Python has a builtin method that does with in [heapq.merge](https://github.com/python/cpython/blob/3.7/Lib/heapq.py#L314). It nicely takes advantage of the fact that both our lists are already sorted so we can get a new sorted list linear time rather then the n log n time it would take for combining unsorted lists.

Imagine my surprise then when I saw this performance graph from Stack Overflow:

Python sort is beating merge
## TimSort

Python's list.sort is the original implementation of a hybrid sorting algorithm called TimSort which is named after its author Tim Peters.

> This describes an adaptive, stable, natural mergesort, modestly called
timsort (hey, I earned it <wink>).  It has supernatural performance on many
kinds of partially ordered arrays (less than lg(N!) comparisons needed, and
as few as N-1), yet as fast as Python's previous highly tuned samplesort
hybrid on random arrays.
>

<figcaption>Tim Peters explaining [TimSort](https://github.com/python/cpython/commit/92f81f2e63b5eaa6d748d51a10e32108517bf3bf#diff-6d09fc0f0b57214c2e3a838d366425836c296fa931fe9dc430f604b7e3950c29)<figcaption>


Timsort is designed to find runs of sequential numbers and merge them together:

> In a nutshell, the main routine marches over the array once, left to right,
alternately identifying the next run, then merging it into the previous
runs "intelligently".  Everything else is complication for speed, and some
hard-won measure of memory efficiency.

This is why `list(x + y).sort()` can be surprizingly fast: once it finds the sequiential runs of numbers it is functioning just like our merge algorithm, combining the two sorted lists in linear time.

Timsort does have less information than our merge algorith though. It needs to do a pass over the data to find these sequential runs where we know them ahead of time. It overcomes this advantage though by being written in C.

>  CPython's list.sort is implemented in C (avoiding interpreter overhead), while heapq.merge is mostly implemented in Python, and optimizes for the "many iterables" case in a way that slows the "two iterables" case. 
<figcaption>ShadowRanger on StackOverflow</figcaption>

This mean that is should be possible to beat Timsort for list merging if we write our own c extension.

## Building A C Extension
My team mate Alex has experience writing C extensions for Python so by the time I had found the Python headerfiles, Alex had already put together a working solution.

The bulk of the algorithm is just the merge process we discussed above:

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

Once we have that extension compiled we can easily use it from python after a `pip install bla`:

``` python
import merge

# create some sorted lists
a = list(range(-100, 1700))
b = list(range(1400, 1800))

# merge them
merge.merge(a, b)
```

## Testing It
Testing this with a lists of ints and floats we can see that we are beating timsort, though not by much in some cases:
``` python
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
....
But if we switch to a list of only integers we are losing again:
....

Timsort has some extra tricks up its sleves in the case of a list of integers. In that intial pass over the list, checks the types of the elements and if they are all of the same type it uses a cheap comparison operation.

Specifically, if you list is all [longs](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2085), [floats](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2113), or [latin strings](https://github.com/python/cpython/blob/main/Objects/listobject.c#L2061) timsort will save a lot of cycles on the comparison operations.

## Special Comparisons

Learning from timsort we can bring in these comparison operations ourselves.  We don't want to actually do a full pass over the lists, or we will lose our theoritical advantage but we can just specialize our merge by offer seperate calls for longs, floats and latin strings.  

## Beatin TimSort

Doing that, we now can beat Timsort, not just when the list is a hetrogenius mix of elements, but also when its all integers, or floating point numbers or one byte per char strings.

....
....

## TimSort Is Good
In this case, where we have more information, we can beat TimSort. The surprising thing though is how good timsort still is, it wasn't really designed for merging sorted lists, but for sorting real-world data. In the real world, data is not as randomly distributed and worst case performance is often less important than median performance. It's no wonder then that since its first creation TimSort has spread from Python to JavaScript, Swift, and Rust. Good job Tim Peters!


