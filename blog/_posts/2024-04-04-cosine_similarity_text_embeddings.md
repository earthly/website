---
title: "Put Your Best Title Here"
categories:
  - Tutorials
toc: true
author: Adam

internal-links:
 - just an example
---

Ok, so I wanted to add related items to the side bar on the Earthly Blog. We are approaching 500 blog posts, so building this related list for each blog post manually wasn't going to work.

Thanksfully, with the available ML libraries and with the availabilty of the OpenAI embbeddigns API, I can using text embeddings and cosine similarity to find related blog posts in a couple lines of python. 


## What is a text embedding

Imagine a simpler problem. You want to figure out how similar a given word is to another word. In this case, I have a blog page for dog, and I want to show the related post cat, and bulldog, but not ones for the inanimate objects 'shoe' and 'brick'.

One way to solve this problem is to create a table of words, their membership in various classes. A dog and cat are both pets. A brick is a building material and a shoe is footwear. So if we have a list of bits, marking `isPet`,`isConstruction`,`isMaterial` then we can store are words like this:

```
items = {
  "dog":[1,0,0],
   "cat":[1,0,0],
   "bulldog":[1,0,0],
   "brick":[0,1,0],
   "shoe":[0,0,1],
}
```

Pedants might say, well, someone could have a pet brick couldn't they? And maybe you could use a shoe as construction material? And yes, that is true, categoies are not all or nothing, lets make them floats from 1 to 0. The closer to 1 the more relevant the word is to the category.

```
items = {
  "dog":[1.0,0.0,0.0],
   "cat":[1.0,0.0,0.0],
   "bulldog":[1.0,0.0,0.0],
   "brick":[0.1,1.0,0.1],
   "shoe":[0.1,0.1,1.0],
}
```

Now, if you look at these three numbers as a point in 3-dimensional space, you can see what we've done is found a way to map a word into a 3-dimensional space such that items near each other are related on the dimensions we care about.

In our footwear, construction materials and pets website, we should find that this view of our has three pretty clear clusters of related data, but thre might be some out outlier groups for the pet rock people of the world. This projection of the data is a text embedding.

Obviously the problem will all this is coming up with what all the dimensions are and with the giant membership list for everything word that's important to you. In the real world we will have a lot more words than this, and we will need a lot more categories, to disambiguate them. For instance, lots of words would score [0,0,0] like `sadness` or `purple` `philosophy` even though they have nothing to do with each other. We will get to that soon enough, but assuming we have these values, how do we figure out what's related to what?

## What is cosine simularity

Ok, time to get a little mathy. If we take our points in three dimensional space, and treat them as a vector from [0,0,0] to their value, we get a bunch of arrows in three dimensional space. Here is dog and brick.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5500.png --alt {{ Large Angle Between Dog and Brick }} %}
<figcaption>Large Angle Between Dog and Brick</figcaption>
</div>

You'll notice that the angle between these points is quite large. But if we compare related terms that's not the case.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5920.png --alt {{ Small Angle Between Dog and Cat }} %}
<figcaption>Small Angle Between Dog and Cat</figcaption>
</div>

So the angle is a great measurement to use for simularity and thankfully it's fairly easy to calcualate. 

Cosine similarity is a metric used to measure how similar two entities (in your case, blog posts represented by their text embeddings) are irrespective of their size. Mathematically, it measures the cosine of the angle between two vectors projected in a multi-dimensional space. The closer the cosine value is to 1, the smaller the angle and the greater the similarity between the two vectors.

In the context of your 3-dimensional example with `items`, you can think of each item as a point in a 3D space. The dimensions of this space are defined by your categories: `isPet`, `isConstruction`, and `isMaterial`. Each item (e.g., "dog", "cat", "brick") is represented by a vector in this space, pointing from the origin (0, 0, 0) to its coordinates (for example, "dog" would point to (1.0, 0.0, 0.0)).

### Why Cosine Similarity?

Imagine shining a flashlight from the origin towards each item's vector. The shadows of vectors that fall closer together will look more alike than those that are far apart if you look down from above. Cosine similarity essentially measures how similar these shadows are, ignoring how far from the origin (how "long") the vectors are. This makes it perfect for comparing the "direction" of the vectors (which represents the similarity in terms of categories) rather than their magnitude (which could be influenced by other factors like the length of a blog post).

### Explaining with the 3D Example

To bring this to life with your 3D example, let's calculate the cosine similarity between two items, say "dog" and "cat":

- "dog" is represented by the vector [1.0, 0.0, 0.0].
- "cat" is represented by the vector [1.0, 0.0, 0.0].

The cosine similarity formula is:

\[ \text{Cosine Similarity} = \frac{A \cdot B}{\|A\| \|B\|} \]

where:
- \(A \cdot B\) is the dot product of vectors A and B,
- \(\|A\|\) and \(\|B\|\) are the magnitudes (lengths) of the vectors.

For "dog" and "cat", both the dot product and the magnitudes would result in:

\[ \text{Cosine Similarity} = \frac{(1.0 \times 1.0) + (0.0 \times 0.0) + (0.0 \times 0.0)}{\sqrt{(1.0^2 + 0.0^2 + 0.0^2)} \times \sqrt{(1.0^2 + 0.0^2 + 0.0^2)}} = \frac{1}{1} = 1 \]

A cosine similarity of 1 means the vectors are identical in terms of direction, indicating maximum similarity—in this case, both "dog" and "cat" are fully within the "isPet" category, and not at all in the others, making them very similar within the context of your categories.

### Python Example

Let's see how you could implement a simple cosine similarity function in Python to compare any two items from your `items` dictionary:

```python
import numpy as np

def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    return dot_product / (magnitude_a * magnitude_b)

# Example vectors from your items dictionary
vector_dog = np.array([1.0, 0.0, 0.0])
vector_cat = np.array([1.0, 0.0, 0.0])

# Calculating the cosine similarity between 'dog' and 'cat'
similarity = cosine_similarity(vector_dog, vector_cat)
print(f"The cosine similarity between 'dog' and 'cat' is: {similarity}")
```

This approach, scaled up from your simplified 3D model to the high-dimensional space used by text embeddings, lets you automatically determine related blog posts based on the similarity of their content, operationalized through the cosine similarity of their embedding vectors.

## How similar is similar enough?
