---
title: "Consine Similarity and Text Embeddings In Python with OpenAI"
categories:
  - Tutorials
toc: true
author: Adam
---

Okay, so I wanted to add related items to the sidebar on the Earthly Blog. Since we are approaching 500 blog posts, building this related list for each post manually wasn't going to work.

Thankfully, with the available ML libraries and the OpenAI embedding API, I can use text embeddings and cosine similarity to find related blog posts in a couple of lines of Python.

## What Is A Text Embedding

Imagine a simpler problem. You want to figure out how similar a given word is to another word. In this case, I have a blog page for `dog`, and I want to show the related post `cat`, and `bulldog`, but not ones for the inanimate objects `shoe` and `brick`.

One way to solve this problem is to create a table of words and their membership in various classes. A dog and a cat are both pets. A brick is a building material, and a shoe is footwear. So if we have a list of bits, marking `isPet`,`isConstruction`,`isMaterial`, then we can store words like this:

~~~{.python caption=""}
items = {
  "dog":[1,0,0],
   "cat":[1,0,0],
   "bulldog":[1,0,0],
   "brick":[0,1,0],
   "shoe":[0,0,1],
}
~~~

Pedants might say, well, someone could have a pet brick, couldn't they? And maybe you could use a shoe as construction material? And yes, that is true. Categories are not all or nothing. Let's make them float from 1 to 0. The closer to 1, the more relevant the word is to the category.

~~~{.python caption=""}
items = {
  "dog":[1.0,0.0,0.0],
   "cat":[1.0,0.0,0.0],
   "bulldog":[1.0,0.0,0.0],
   "brick":[0.1,1.0,0.1],
   "shoe":[0.1,0.1,1.0],
}
~~~

Now, if you look at these three numbers as a point in three-dimensional space, you can see that we've found a way to map a word into three-dimensional space such that items near each other are related to the dimensions we care about.

In our footwear, construction materials and pets website, we should find that this view of our has three pretty clear clusters of related data, but there might be some out outlier groups for the pet rock people of the world. This projection of the data is a text embedding.

The problem with all this is coming up with all the dimensions and the giant membership list for every word that's important to you. In the real world, we will have a lot more words than this, and we will need a lot more categories to disambiguate them. For instance, many words would score [0,0,0] like `sadness` or `purple` and `philosophy` even though they have nothing to do with each other. We will get to that soon enough, but assuming we have these values, how do we figure out what's related to what?

## What Is Cosine Similarity

Ok, it's time to get a little mathy. If we take our points in three-dimensional space and treat them as a vector from [0,0,0] to their value, we get a bunch of arrows in three-dimensional space. Here is `dog` and `brick`.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5500.png --alt {{ Large Angle Between Dog and Brick }} %}
<figcaption>Large Angle Between Dog and Brick</figcaption>
</div>

You'll notice that the angle between these points is quite large. But if we compare related terms, that's not the case.

<div class="wide">
{% picture content-wide-nocrop {{site.pimages}}{{page.slug}}/5920.png --alt {{ Small Angle Between Dog and Cat }} %}
<figcaption>Small Angle Between Dog and Cat</figcaption>
</div>

So, the angle is a great measurement to use for similarity, and thankfully, it's fairly easy to calculate. This is high school math, but we are just going to be adding some more dimensions.

~~~{.python caption=""}
import numpy as np

def calculate_angle_degrees(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    cosine_of_angle = dot_product / (magnitude_a * magnitude_b)
    angle_in_degrees = np.degrees(np.arccos(cosine_of_angle))
    return angle_in_degrees

# Example vectors for 'brick' and 'shoe'
vector_brick = np.array([0.1, 1.0, 0.1])
vector_shoe = np.array([0.1, 0.1, 1.0])

calculate_angle_degrees(vector_brick, vector_shoe)
~~~

 ( How we calculate that angle isn't essential if you want to gloss over it. )

 This gives `78.118` degrees for the angle between `brick` and `shoe`. The maximum possible angle with this formula is 90 degrees, completely perpendicular to each other. And the min value is 0 degrees, the two angles are exactly the same.

 To get a similarity score, we just need to invert these values to get them between 0 and 1. 0 degrees should be our exact match value 1, and 90 degrees should be 0. That projection is the cosine of the angle.

~~~{.python caption=""}
 import numpy as np

def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    return dot_p

cosine_similarity(vector_brick, vector_shoe)

~~~

The similarity between `brick` and `shoe` is 0.20. Not very high, corresponding to an angle of ~70 degrees of difference. That is the cosine similarity.

For our silly little example, we now have all the necessary components. We can take all our words, calculate the cosine similarity for every possible combination of them, and return the N values as our related items for each.

Now, let's talk about doing this in the real world.

## Word2Vec

In the real world, things don't cleanly separate into 3 dimensions, and we can't possibly manually calculate the dimensions for every English word. Thankfully, in 2013, Tomáš Mikolov at Google came up with a technique to calculate vectors for words based on a corpus of training data.

How it works isn't important for our purposes. Besides, in the vector values generated with word2vect, similar words are near each other, and dissimilar words are far away. Because of this grouping, we can use the same techniques as above, cosine similarity, to calculate relatedness.

We can test this out by grabbing word2vect dataset :

~~~
python -m spacy download en_core_web_lg
~~~

And then using spacy to test it out:

~~~{.python caption=""}
import spacy

# Load a large English model with word vectors included
nlp = spacy.load('en_core_web_lg')

# Access the vector for a specific word
dog_vector = nlp('dog').vector

print(dog_vector)
~~~

In word2vec, the dimensions are discovered via training and are opaque to us. It's not clear what any specific dimension means when looking at the raw vectors; they just group related items together. To make this all work, the dimensions of `en_core_web_lg` are 300 instead of our previous 3. That makes it much harder to visualize.

~~~{.python caption=""}
print(dog_vector)
[ 1.2330e+00  4.2963e+00 -7.9738e+00 -1.0121e+01  1.8207e+00  1.4098e+00
 -4.5180e+00 -5.2261e+00 -2.9157e-01  9.5234e-01  6.9880e+00  5.0637e+00
 -5.5726e-03  3.3395e+00  6.4596e+00 -6.3742e+00  3.9045e-02 -3.9855e+00
  1.2085e+00 -1.3186e+00 -4.8886e+00  3.7066e+00 -2.8281e+00 -3.5447e+00
  7.6888e-01  1.5016e+00 -4.3632e+00  8.6480e+00 -5.9286e+00 -1.3055e+00
  8.3870e-01  9.0137e-01 -1.7843e+00 -1.0148e+00  2.7300e+00 -6.9039e+00
  8.0413e-01  7.4880e+00  6.1078e+00 -4.2130e+00 -1.5384e-01 -5.4995e+00
  1.0896e+01  3.9278e+00 -1.3601e-01  7.7732e-02  3.2218e+00 -5.8777e+00
  6.1359e-01 -2.4287e+00  6.2820e+00  1.3461e+01  4.3236e+00  2.4266e+00
 -2.6512e+00  1.1577e+00  5.0848e+00 -1.7058e+00  3.3824e+00  3.2850e+00
 ...
~~~

Using this dataset, we can skip the whole creating our own vectors:

~~~{.python caption=""}

import spacy
import numpy as np

# Load a large English model with word vectors included
nlp = spacy.load('en_core_web_lg')

# Access the vector for a specific word
dog_vector = nlp('dog').vector
bulldog_vector = nlp('bulldog').vector
shoe_vector = nlp('shoe').vector
brick_vector = nlp('brick').vector

def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    return dot_product / (magnitude_a * magnitude_b)

similarity_dog_bulldog = cosine_similarity(dog_vector, bulldog_vector)
similarity_shoe_brick = cosine_similarity(shoe_vector, brick_vector)
~~~

~~~
Dog, Bulldog similarity: 0.6215080618858337
shoe, brick similarity: 0.301258385181427
~~~

We see that `dog` is over twice as related to `bulldog` as `shoe` is to `brick`. This seems vaguely right to me. Surprisingly, though, 'dog' is closer to 'cat' than to 'bulldog,' but this will work for our purposes.

## Text Embeddings

So now we can do related words but in the real world it would be great to extend this to whole sentences, or titles or even full documents. The simple way to do this might be find the vector of each word in the document and then combine these vectors.

We can use this, but there are some issues. The primary problem is that writing is complex. The meaning of a sentence is not a combination of the meaning of the various words. "I like dogs" and "I hate dogs" mean the opposite, but combining the weights of individual vectors will end up very close to each other since all but 1 word is precisely the same. Meanwhile, a sentence like "You love dogs" will end up further away because of the difference between "You and "I"

Thankfully, we now have better approaches. A text embedding is a vector, similar to a word2vec vector, but produced based on a whole piece of text ( a word, a sentence, a document ) that produces vectors based on a richer semantic understanding of the text.

~~~{.python caption=""}

import os
from openai import APIError, OpenAI
from sklearn.metrics.pairwise import cosine_similarity

# Set your OpenAI API key here
client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

def get_text_embedding(text):
    embedding = client.embeddings.create(input=text, model="text-embedding-3-large"

).data[0].embedding
    return embedding

def calculate_cosine_similarity(vector1, vector2):
    return cosine_similarity([vector1], [vector2])[0][0]

sentences = {
    'like': "I like dogs.",
    'love': "You love dogs.",
    'dont_like': "I hate dogs."
}

embeddings = {label: get_text_embedding(text) for label, text in sentences.items()}

similarity_like_love = calculate_cosine_similarity(embeddings['like'], embeddings['love'])
similarity_like_dont_like = calculate_cosine_similarity(embeddings['like'], embeddings['dont_like'])

closest_sentence_label = 'love' if similarity_like_love > similarity_like_dont_like else 'dont_like'
closest_sentence_similarity = similarity_like_love if similarity_like_love > similarity_like_dont_like else similarity_like_dont_like

print(f"The closest to '{sentences['like']}' is '{sentences[closest_sentence_label]}'")
print(f"Similarity: {closest_sentence_similarity}")

~~~

~~~
The closest to 'I like dogs.' is 'You love dogs.'
Similarity: 0.7072032971889817
~~~

In a text embedding, the context of the surrounding words enriches the semantic meaning so that "I like dogs" is more closely related to "You love dogs" than "I hate dogs".

How this is all done is outside the scope of this article, but with the OpenAI embedding API, it's done using Generative Pre-trained Transformers.

## Putting It All Together

With all of this information, I can calculate related items for this blog. You can see in the sidebar, if you click around on the blog. Some articles have more related than others, for reasons that hopefully now are clear. The code is [in github](https://github.com/earthly/website/blob/main/util/psupport/psupport/scripts/suggested_posts.py). You should be able to understand it. It gets the text embedding vector for each blog post and then uses cosine similarity to find the posts closest to it.

The great thing about this technique is that as text embedding technology continues to improve, it becomes easier and easier to find related items.
