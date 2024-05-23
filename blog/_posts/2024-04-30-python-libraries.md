---
title: "Top 10 Python Libraries for Data Science"
toc: true
author: Alen Kalac

internal-links:
 - 10 python libraries
 - python libraries for data science
 - best python libraries for data science
 - top python libraries for data science
 - top 10 python libraries for data science
-excerpt: |
   This article provides an overview of the top Python Libraries for data science. These include Beautiful Soup, Keras, TensorFlow, Matplotlib and some other interesting libraries.
categories:
  - Data
---

One of the main reasons why Python is the go-to programming language for data science is its [vast ecosystem](https://learnpython.com/blog/python-modules-packages-libraries-frameworks/) of libraries, packages, and frameworks, many of which are geared toward data science.

Python's data science ecosystem allows you to easily acquire data, manipulate, clean, analyze, and visualize it, and then use it to train machine learning models. To perform any of these processes without data science libraries, you'd have to write the code for the functionalities from scratch, which would be time-consuming and far less efficient.

There are thousands of libraries available, but in this article, you'll review ten of the most essential libraries for data scientists. These ten were chosen based on their popularity, functionality, community support, relevance, and ease of use.

Please keep in mind that data science is a vast field with numerous separate use cases. The libraries reviewed here have been grouped by what they're commonly used for. You'll find libraries for data acquisition, data analysis and processing, machine learning, and data visualization.

## Data Acquisition

Before data can be manipulated or analyzed, it needs to be acquired. If you're lucky, you may already have the data. But, more often than not, data will not be readily available. In that case, if the data is on the web, you can acquire it through web scraping.

Python has a few popular and powerful web scraping libraries, including [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) and [Scrapy](https://scrapy.org/).

### Beautiful Soup

[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) is one of the most popular web scraping libraries. It's lightweight, versatile, user-friendly, easy to learn, and powerful.

One of its biggest advantages is its ease of use. You can set it up and scrape a web page with just a few lines of code. Once the HTML or XML is scraped, Beautiful Soup can easily parse the document, navigate it, and extract information.

Despite its simplicity, Beautiful Soup has some powerful and useful methods, including [`find()` and `find_all()`](https://www.geeksforgeeks.org/difference-between-find-and-find_all-in-beautifulsoup-python/).

Here's how easy it is to acquire data with Beautiful Soup with just a few lines of code:

~~~{.python caption=""}
from bs4 import BeautifulSoup
import requests

x = requests.get("https://quotes.toscrape.com/")
soup = BeautifulSoup(x.text, 'html.parser')

quotes = soup.find_all("div", class_="quote")

scraped_quotes = []
for quote in quotes:
    scraped_quotes.append(quote.find("span", class_="text").text)
~~~

In this example, you scrape [quotes.toscrape.com](https://quotes.toscrape.com/), which is designed for web scraping practice. Here, you import `BeautifulSoup` (note that you'll first have to install it if you don't have it already) and `requests`, fetch the url with `requests`, parse the returned HTML with `BeautifulSoup`, identify all the `div` elements that contain quotes, and finally scrape the quotes themselves and store them into the list `scraped_quotes`.

With just a few seconds and less than ten lines of code, you can scrape the entire contents of a web page. While simplistic, you can scrape most web pages with these few Beautiful Soup methods alone.

### Scrapy

[Scrapy](https://scrapy.org/) is another popular Python web scraping tool. It's faster and more powerful than Beautiful Soup, which is beneficial when you want to acquire large volumes of data or when you want to crawl an entire website instead of just one web page. It can deal with broken and nonstandard declarations and scrape a lot of data without consuming too much memory. It's also asynchronous, meaning it can crawl multiple pages in parallel.

However, keep in mind that Scrapy is more complex than Beautiful Soup and more difficult to set up. Its learning curve is fairly steep, especially when compared to the simplicity of Beautiful Soup.

If you're completely new to web scraping, it's probably a good idea to start with Beautiful Soup, and once you're comfortable with it, consider learning Scrapy.

**Honorable mention:** [Selenium](https://www.selenium.dev/) (best for scraping dynamic web pages)

## Data Analysis and Processing

Python has become essential for data analysis, with data libraries like [NumPy](https://numpy.org/) and [pandas](https://pandas.pydata.org/) playing a crucial role in the process. In the field of data science, there's hardly a Jupyter Notebook or Google Colab whose first cell doesn't include the famous `import pandas as pd` and `import numpy as np` lines. It's generally considered that [data preparation takes up the majority of a data scientist's time](https://www.forbes.com/sites/gilpress/2016/03/23/data-preparation-most-time-consuming-least-enjoyable-data-science-task-survey-says/?sh=4c5ed4ee6f63), and these libraries are indispensable for that task.

### NumPy

[NumPy](https://numpy.org/) is a popular Python library that works with mathematical and scientific computations. It contains built-in mathematical functions that allow you to work with large matrices and multidimensional arrays.

With NumPy, you can perform complex algebraic computations, Fourier transformations, operations with matrices, and much more. This may sound scary, but NumPy makes it relatively simple.

At the core of NumPy is the [NumPy array](https://www.geeksforgeeks.org/basics-of-numpy-arrays/), a highly efficient data structure that outperforms lists and makes NumPy blazing fast. NumPy is also the foundation for other data science libraries, such as pandas and [scikit-learn](https://scikit-learn.org/), and provides a robust framework for advanced data analysis and manipulation.

Let's quickly look at what NumPy can do:

~~~{.python caption=""}
import numpy as np

a = np.array([3, 8, 12, 0, 1])
b = np.zeros(5)
c = np.arange(5)
~~~

There are many ways to create an array in NumPy. In this code, you create arrays in three different ways: array `a` is created by specifying its values, array `b` is created to consist of only zeros, and array `c` contains the digits from 0 to 4. You can perform countless manipulations on these arrays, such as slicing, indexing, concatenating, sorting, filtering, and splitting. You can also perform mathematical operations on these arrays, such as matrix multiplication:

~~~{.python caption=""}
np.matmul(a,c)
~~~

### `pandas`

Along with NumPy, [pandas](https://pandas.pydata.org/) is the most popular data science library; the two libraries are even among the [most popular libraries overall](https://survey.stackoverflow.co/2023/#most-popular-technologies-misc-tech). It's great for data analysis, data preprocessing, and data manipulation.

At the heart of pandas are the [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) (a data structure akin to tables that allows you to work with structured data) and [Series](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.html) (essentially a specific type of DataFrame, which consists of only one column).

pandas simplifies the process of importing and exporting data from (and to) various files (such as CSV, Excel, or JSON). Once your data is imported, pandas lets you group, aggregate, slice, sort, impute, merge, and visualize it. It's indispensable for exploratory data analysis, as it allows you to quickly gain insight into the data, understand it, and identify potential data issues.

pandas can be likened to working in a spreadsheet but with significantly enhanced capabilities.

Let's take a quick look at pandas in action. Here, you'll use the famous [Titanic data set](https://github.com/datasciencedojo/datasets/blob/master/titanic.csv), which contains various data about the passengers on the Titanic, such as their name, age, gender, passenger class, and fare. Here's how easy it is to start with pandas:

~~~{.python caption=""}
import pandas as pd

df = pd.read_csv("titanic.csv")
~~~

The first line imports pandas as `pd`, which is by far the most common way to import pandas. Then, the second line imports data from `titanic.csv` and stores it in the `df` DataFrame. If you want to see a sample of the data, you can use the line `df.head()`, which will show you the first five rows of the data, like this:

<div class="wide">
![pandas head() method]({{site.images}}{{page.slug}}/87aFSsv.png)
</div>

You can also use `df.info()`, which shows all the columns in the data set, their type, and whether they contain missing values. From the following output, you can see that the data set contains 12 columns and 891 rows. You can also see that columns such as "Age," "Cabin," and "Embarked" contain missing values:

<div class="wide">
![pandas info() method]({{site.images}}{{page.slug}}/I7H1Peq.png)
</div>

With `df.describe()`, you can quickly get summary statistics, such as the count, mean, and standard deviation of the columns. With just this one line, you can see that the average person on the Titanic (from the 891 people included in the data set) was 29.7 years old, while the oldest was 80 years old:

<div class="wide">
![pandas describe() method]({{site.images}}{{page.slug}}/xjI2urK.png)
</div>

Methods such as `df.head()`, `df.info()`, and `df.describe()` are great ways to quickly see what data you're working with, but you can also use pandas to clean and manipulate data.

You already saw that there was missing data in the "Age," "Cabin," and "Embarked" columns. Most machine learning models can't work with missing data. That means you'll have to find a way to either deal with the missing data or drop those rows. You can use `df.fillna()` to fill in the missing data in a way you think is appropriate, or drop any rows with missing data with `df.dropna()`.

You can also remove columns that you don't need, create new columns based on the existing ones, or group the data. For example, by running `df.groupby("Pclass").mean()`, you can group the passengers based on their passenger class and calculate the means for each class. As you can see, the average age of the passengers in the first class was significantly higher compared to the other classes, as was their fare:

<div class="wide">
![pandas groupby() method]({{site.images}}{{page.slug}}/vt0crHe.png)
</div>

### SciPy

Another library that's widely used for scientific computation is [SciPy](https://scipy.org/). It's built on top of NumPy and extends its capabilities for scientific computations. Both of these aspects are reflected in SciPy's name. This library can be used for linear algebra, Fourier transformations, differential equations, and statistics, as well as optimization algorithms.

Like NumPy, SciPy also has multidimensional matrices as its main object. Overall, SciPy is a great choice if you're building sophisticated, specialized scientific applications.

**Honorable mention:** [statsmodels](https://www.statsmodels.org/stable/index.html) (specifically for statistics)

## Machine Learning

In essence, machine learning allows computers to learn from experience instead of being explicitly programmed. Machine learning used to require writing code from scratch, which made it extremely complex and time-consuming. However, with the help of some great Python libraries, you can perform machine learning with just a few lines of code.

Let's take a look at three of the most popular libraries for machine learning.

### `scikit-learn`

[scikit-learn](https://scikit-learn.org/) is Python's go-to machine learning library. It contains a plethora of machine learning algorithms that are extremely straightforward to use; it doesn't matter whether you're interested in supervised or unsupervised learning or whether you're performing classification or regression tasks.

When it comes to supervised learning, you can use scikit-learn for simpler algorithms such as linear and logistic regression, but also for support vector machines, nearest neighbors, Naive Bayes, decision trees, and random forests. It's also useful for unsupervised tasks such as dimensionality reduction and clustering. scikit-learn even offers some neural network algorithms, though it's very limited in the realm of deep learning, so you'd be better off with another library such as TensorFlow or Keras.

However, scikit-learn can be used for more than merely supervised or unsupervised learning. You can also utilize it for data preprocessing tasks (such as normalization, standardization, categorical encoding, imputing missing values, and similar), hyperparameter tuning, cross-validation, feature selection, classification and regression metrics, and much more.

### TensorFlow

Deep learning is a subset of machine learning that has become extremely prevalent in the last decade. It utilizes deep neural networks and is commonly used for tasks that involve unstructured data, such as images, text, or audio. One of the most popular libraries to make training neural networks as straightforward as possible is [TensorFlow](https://www.tensorflow.org/), developed by Google.

In essence, TensorFlow allows you to perform numerical computations with high performance and makes it relatively easy to develop, evaluate, and visualize deep learning models. TensorFlow is memory-efficient and can be easily deployed using both CPUs and GPUs. However, TensorFlow is not as beginner-friendly as other deep-learning libraries, like Keras.

### Keras

[Keras](https://keras.io/) is one of the easiest ways for a complete beginner to start with deep learning. It can run on top of TensorFlow, which allows it to train deep neural networks with just a little code and a user-friendly syntax. Its website's tagline is "Deep learning for humans," and Keras lives up to that.

Through its [Layers API](https://keras.io/api/layers/), Keras provides you with numerous layers, such as convolution, pooling, recurrent, preprocessing, normalization, and regularization layers. It also allows you to use many different optimizers, metrics, and losses.

Though it's not as powerful as TensorFlow, Keras's flexibility and simplicity make it a popular choice among machine learning engineers.

**Honorable mentions:** [PyTorch](https://pytorch.org/) (alternative to TensorFlow and Keras), [NLTK](https://www.nltk.org/) (for natural language processing), [XGBoost](https://xgboost.readthedocs.io/en/stable/) (for gradient boosting)

## Data Visualization

Analyzing data by looking at the raw numbers, while useful, is far from ideal. You may not be able to identify patterns in the data by merely looking at it. However, visualizing the data does allow you to quickly examine it and notice patterns and trends.

Fortunately, Python has a plethora of great data visualization libraries. These libraries provide you with numerous chart types with just a few lines of code.

### Matplotlib

Among the many data visualization Python libraries, [Matplotlib](https://matplotlib.org/) is a very popular one. In fact, a lot of the other data visualization libraries are [built on top of Matplotlib](https://mode.com/blog/python-data-visualization-libraries).

Matplotlib lets you easily create different charts and customize every detail on them. Its customizability is one of its strongest points.

However, Matplotlib is considered relatively complex, especially when you compare it to other data visualization libraries, such as [seaborn](https://seaborn.pydata.org/). It's also [generally considered to have old-fashioned default charts](https://www.oreilly.com/library/view/python-data-science/9781491912126/ch04.html).

Let's take a quick look at how to create a simple chart with Matplotlib and what the output looks like using the Titanic data set. Below is the code to create a histogram showing the age distribution of the passengers. Here, you import the library, identify the column you want to create a histogram of, and add axis labels:

~~~{.python caption=""}
import matplotlib.pyplot as plt

plt.hist(df["Age"])
plt.xlabel('Age')
plt.ylabel('Count')
plt.show()
~~~

![Matplotlib chart]({{site.images}}{{page.slug}}/rDpyFSR.png)

### `seaborn`

Another popular Python data visualization library is [seaborn](https://seaborn.pydata.org/). It's built on top of Matplotlib, so it shares many similarities. However, seaborn is designed to be easier to use and requires less code for the same functionality.

In addition, seaborn's default charts are generally considered to be more modern than Matplotlib's. However, seaborn doesn't offer all the functionalities that Matplotlib does, so if you want to get into the specific details, you're stuck with Matplotlib.

For comparison, let's use seaborn to recreate the same chart you created with Matplotlib. As you'll notice, it takes less code, and the output looks better:

~~~{.python caption=""}
import seaborn as sns

sns.histplot(df["Age"])
plt.show()
~~~

![seaborn chart]({{site.images}}{{page.slug}}/Tq4EaIF.png)

**Honorable mentions:** [Bokeh](http://bokeh.org/), [Plotly](https://plotly.com/python/)

## Conclusion

In this article, you learned about the most popular Python libraries for data acquisition, data analysis and processing, machine learning, and data visualization.

If you're a beginner, try not to be overwhelmed by your choices. Some of the listed libraries have a similar use case (*eg* Matplotlib and seaborn, Beautiful Soup and Scrapy), so you only need to know one of them. Additionally, most of the discussed libraries are useful for a specific task, which may or may not be of interest to you. For example, if you're not going to use deep learning, you don't need to master TensorFlow or Keras. So, identify which of the libraries are relevant to you and dive into those. A great starting point is the combination of pandas, NumPy, and Matplotlib. Most data scientists use those three regularly.

And if you're searching for a simple build framework that you'll write only once and run anywhere, take a look at [Earthly](https://earthly.dev/). It offers straightforward syntax and is compatible with all languages and frameworks. You can [start for free](https://cloud.earthly.dev/login) and try its consistent and repeatable builds, advanced caching, and easy integration with any CI.

{% include_html cta/bottom-cta.html %}
