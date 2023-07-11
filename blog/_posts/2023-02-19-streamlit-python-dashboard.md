---
title: "Build a Data Dashboard with Streamlit in Python"
categories:
  - Tutorials
toc: true
author: Barine Sambaris
editor: Bala Priya C

internal-links:
 - Python
 - Data
 - OpenSource
 - Matplotlib
excerpt: |
    Learn how to build a data dashboard with Streamlit in Python. This tutorial will teach you how to create interactive visualizations and deploy web apps for data analysis and machine learning models.
---
<!--sgpt-->**We're [Earthly](https://earthly.dev/). We make building software simpler and therefore faster using containerization. This article is about building a data dashboard with Streamlit in Python. Earthly is a popular choice for developers and system administrators who are looking for an efficient and reliable build tool for continuous integration (CI). [Check us out](/).**

Streamlit is an open-source Python framework that lets you turn data scripts into shareable web apps in minutes. Streamlit makes it easy for data scientists and analysts to create and deploy interactive visualizations and dashboards for machine learning models and other Python applications.

You need almost no experience with building front ends to get started with Streamlit. It is designed to do the heavy lifting of generating an intuitive and responsive interface from a simple Python script.

This tutorial will teach you how to build a dashboard for a Github dataset of movie records. You'll then learn how to deploy the web app and interactively explore the dataset, visualize, and retrieve information from it.

## Why Should You Use Streamlit?

There are several reasons to choose Streamlit for data visualization. Some of them include:

Streamlit is written for Python and is compatible with major Python libraries for data analysis and machine learning.
The Streamlit interface is intuitive and user-friendly.
Streamlit dashboards can be hosted on Streamlit Cloud.
You can configure Streamlit to monitor the GitHub repository where the code and data are hosted, and update the web app when changes are made to the repository.

## Installing Streamlit

Before we get started, you should know that you need a good understanding of data analysis and visualization in Python. This is because Streamlit only lets you embed your visualization within its framework and display them as web apps; you still need to analyze the data and meaningfully visualize it.

From the command prompt, install Streamlit using pip by running the following command:

~~~{.bash caption=">_"}
pip install streamlit 
~~~

To check if the installation worked, create a new Python script in your editor, import streamlit under the alias `st`, and use the `write` function to print out some text. The `st.write()` function is used to display information like text, dataframes, or figures.

~~~{.python caption="data_analysis.py"}
import streamlit as st
st.write("Hello World!")
st.write("Hello Streamlit!")

~~~

Run the app on your browser (in your command prompt, change the directory to the folder where your file is located) by running this command:

~~~{.bash caption=">_"}
streamlit run file_name.py

~~~

This will automatically open a tab in your browser.

<div class="wide">
![Streamlit Hello World Output]({{site.images}}{{page.slug}}/hello.png)\
</div>

If you get this output, your installation works and you are ready to use Streamlit.

## Plotting With Streamlit

You can find the code for this project [on Github](https://github.com/barrisam/Interactive-visualization-with-streamlit) and the real-time application [on Streamlit Cloud](https://barrisam-interactive-visualization-with-st-data-analysis-95hcxj.streamlit.app/).

### Adding a Matplotlib Chart

`st.pyplot()` is the Streamlit function to create figure objects and plots. To create a matplotlib visualization, you have to perform data analysis and then create the visualization. For this section, we will use [this movie industry dataset from
Github](https://github.com/danielgrijalva/movie-stats).

This dataset contains over 7000 movie entries—from the period 1986-2016—scraped from IMDb (Internet Movie Database). It lists movies of different genres and countries. I'll be using this dataset to create different interactive plots for this tutorial.

~~~{.python caption="data_analysis.py"}
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
~~~

We use the pandas `read_csv()` function to read in the data into a dataframe.

~~~{.python caption="data_analysis.py"}
#read in the file
movies_data = pd.read_csv("https://raw.githubusercontent.com/danielgrijalva/movie-stats/7c6a562377ab5c91bb80c405be50a0494ae8e582/movies.csv")
~~~

To generate a summary of the dataset and check for missing values and duplicates, we'll use the following functions:

~~~{.python caption="data_analysis.py"}
movies_data.info()
~~~

~~~{caption="Output"}
#output
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 7668 entries, 0 to 7667
Data columns (total 15 columns):
 #   Column    Non-Null Count  Dtype