---
title: "Building a Real-time Stock Price Dashboard Using Python, QuestDB, and Plotlye"
categories:
  - Tutorials
toc: true
author: Verah Ombui

internal-links:
 - Dashboard
 - Python
 - QuestDB
 - Plotlye
---

Are you dealing with huge amounts of data? If so, you're likely facing a problem storing and analyzing such data to gain meaningful insights.

One of the most efficient ways of analyzing and presenting data is through charts and graphs. In this tutorial, you will build a real-time stock price streaming web application having a dashboard with charts for data visualization.

The application will use [QuestDB](https://questdb.io/), [Celery](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/redis.html), [Redis](https://redis.io/), and [Plotly Dash](https://dash.plotly.com/introduction).

## Prerequisites

To follow along with this tutorial, ensure you have the following:

- A computer running Ubuntu version 22.04. Note: You  can also work with other Linux distros or an operating system of your choice.
- [Python version 3.8](https://www.python.org/downloads/release/python-380)
- [Docker](https://docs.docker.com/desktop/install/windows-install/) and [Docker Compose](https://docker-docs.netlify.app/compose/install/)
- A [Finnhub](https://finnhub.io/register) account with a sandbox API key
- Working knowledge of  Linux, SQL, and Python
- Familiarity with Plotly Dash and Celery will be helpful

## Project Overview

The project you'll be building has the following two main components:

- A backend that continuously fetches user-defined stock data from Finnhub.
- A frontend that uses Plotly and Dash to visualize the gathered data on the charts.

Note: You'll also use Celery, which is backed by Redis as the message broker, and QuestDB will act as the database that will store the periodically fetched data. You can use Celery in Python applications to quickly implement task queues for workers. You will need it later in this tutorial to execute the periodic tasks.

You can find the code in [this GitHub repo](https://github.com/verah-tech/stock-market).

## Project Setup

In this section, you will set up your project environment as explained below.

### Creating a Project Directory

Let's start by creating a project directory. This tutorial uses `stock-prices` and `app` as the names of the root directory and Python module, respectively.

~~~{.bash caption=">_"}
$ mkdir -p stock-prices/app
~~~

### Installing QuestDB and Redis

Next you need to install the project's required services. In this project, you need Docker and [Docker Compose](/blog/youre-using-docker-compose-wrong) to avoid overloading the local system. Inside the project's root directory, create a new `.yml` file named `docker-compose.yml` file for Docker Compose as shown below. The `.yml` file lets you define the configuration or [container](/blog/docker-slim) environment for multiple Docker containers.. In this project it will allow you to run QuestDB and Redis services simultaneously. Later on, you will install other services as needed.

~~~{.yaml caption="docker-compose.yml"}
# docker-compose.yml
 
version: "3"
 
volumes:
  questdb_data: {}
 
services:
  redis:
    image: "redis:latest"
    ports:
    - "6379:6379"
 
  questdb:
    image: "questdb/questdb:latest"
    volumes:
    - questdb_data:/root/.questdb/db
    ports:
    - "9000:9000"
    - "8812:8812"
~~~

Upon running the `docker-compose up` command the QuestDB and Redis services will fire up. The purpose of Redis is to store real-time data and act as a message broker, as the QuestDB stores the fetched data. The reason for using QuestDB over other databases is that it is lightweight hence less complex, designed to offer real-time analytics on the time series data. For this reason it was the best database to use for this kind of application that deals with real time data fetched from the API.

After services have started on [Docker](/blog/rails-with-docker) containers, you will access QuestDB's interactive console at <http://127.0.0.1:9000>.

The below output will be displayed:

<div class="wide">
![Running Docker Compose command]({{site.images}}{{page.slug}}/GJHoYI3.png)
</div>
<div class="wide">
![Accessing QuestDB's web console]({{site.images}}{{page.slug}}/IyA9iv1.png)
</div>

### Creating the Database Table

Now that you have QuestDB running, you can create the database table by connecting to QuestDB's interactive console and running the below SQL statement.

~~~{.bash caption=">_"}
CREATE TABLE
    quotes(stock_symbol SYMBOL CAPACITY 5 CACHE INDEX,
            current_price DOUBLE,
            high_price DOUBLE,
            low_price DOUBLE,
            open_price DOUBLE,
            percent_change DOUBLE,
            tradets TIMESTAMP, -- timestamp of the trade
            ts TIMESTAMP)   -- time of insert into the table
    timestamp(ts)
PARTITION BY DAY;
~~~

Upon running the above statement the database table named `quotes` will be created and ready for use as shown below:

<div class="wide">
![Creating QuestDB Table]({{site.images}}{{page.slug}}/CkwHRFz.png)
</div>

The `quotes` table created by the above SQL command will have the following fields:
`stock_symbol`: stores unique codes that uniquely identify the company and stock that it issues.
`current_price`: stores the current price of the particular stock.
`high_price`: stores the value when a given stock price rises.
`low_price`: stores the value when a given stock price drops.
`open_price`: stores the opening price at which stock first trades when an exchange opens for the day.
`percent_change`: assists to track a given stock's prices increase or decrease.
`tradets`: stores date and time of the day identifying when a trade happened.

## Creating Workers Using Celery

In this section, you will define Python dependencies that the project requires, define the worker settings, and create the periodic tasks that will fetch data from Finnhub.

![Creating Workers Using Celery]({{site.images}}{{page.slug}}/lqv7XJ9.png)
 
### Defining Dependencies

The next step is to define the Python dependencies. You will create a `requirements.txt` file in the project root directory with the below contents. The `.txt` file will contain the dependencies that will fetch data and visualize this gathered data.

~~~{ caption="requirements.txt"}
finnhub-python==2.4.14  # The official Finnhub Python client
pydantic[dotenv]==1.9.2 # You will use Pydantic to create data models
celery[redis]==5.2.7    # Celery will be the periodic task executor
psycopg2==2.9.1         # You are using QuestDB's PostgreSQL connector
dash==2.6.1             # Dash is used for building data apps
pandas==1.4.3           # Pandas will handle the data frames from QuestDB
plotly==5.10.0          # Plotly will help with charts
~~~

The above dependencies stored in a `.txt` file can be divided into two logical categories:

- The dependencies that fetch the raw data from Finnhub. These include `finnhub-python`, `pydantic`, `celery`, and `pyscopg2`.
- The dependencies that are needed to visualize and present fetched data. You will require these librraies to visualize and present data: `dash`, `pandas`, and `plotly`.

Next, let's create a Python virtual environment named `virtualenv` to install the defined dependencies as follows:

~~~{.bash caption=">_"}
$ virtualenv -p python3.8 virtualenv
$ source virtualenv/bin/activate
$ pip install -r requirements.txt
~~~

### Setting Up the Database Connection

Note that the periodic tasks would require you to store fetched data into the database. This means that you will need to connect to QuestDB. This is achieved by creating a `db.py` file below that contains the PostgreSQL connection pool engine that will serve as the base for your database connections.

~~~{.python caption="db.py"}
# app/db.py
 
from sqlalchemy import create_engine
 
from app.settings import settings
 
engine = create_engine(
    settings.database_url, pool_size=settings.database_pool_size, \
    pool_pre_ping=True
)
~~~

### Defining the Worker Settings

Before you start implementation of the application, first you have to configure Celery. You will create a configuration that will be used by the workers and the dashboard. To achieve this, you will create a `settings.py` file in the `app` package, then use `BaseSettings` to define the configuration. This will help to read settings from a `.env` file, an environmental variable and prefix them when needed.

You will set the prefix as `SMD` to ensure that you do not overwrite any other environment variables in the `settings.py` file as below:

~~~{.python caption="settings.py"}
# app/settings.py
 
from typing import List
 
from pydantic import BaseSettings

# [...]
~~~

In the above code snippet, you have imported `List` from `typing` which takes in a sequence of elements and returns types such as strings. You have also imported `BaseSettings` from `pydantic` which helps settings management of the application. It also assists in determining the values of any fields that are not passed as keyword arguments by reading from `.env` files.

~~~{.python caption="settings.py"}
# [...]

class Settings(BaseSettings):
    """
    Settings of the application, used by workers and dashboard.
    """
# [...]
~~~

Next, you will define the link which celery will communicate to the backend. Note that celery requires a solution to send and receive messages which usually come as a form of separate service known as a message broker. In this tutorial, you are using Redis as the message broker as defined in the below code snippet.

~~~{.python caption="settings.py"}
# [...]
 
    # Celery settings
    celery_broker: str = "redis://127.0.0.1:6379/0"

# [...]
~~~

Next, you have to define the database settings of the application. In the below code snippet, you will specify the database connection string that the application will connect to store data.

~~~{.python caption="settings.py"}
# [...]
 
    # Database settings
    database_url: str = "postgresql://admin:quest@127.0.0.1:8812/qdb"
    database_pool_size: int = 3

# [...]
~~~

![Image]({{site.images}}{{page.slug}}/p5JXM6g.png)

Next, you will define the API settings. You have to specify the API key, the stock data fetch frequency and the stock symbols to be fetched. The API key and stock symbols contain sensitive data and will be stored in a separate file called a `.env` file.

~~~{.python caption="settings.py"}
# [...]
 
    # Finnhub settings
    api_key: str = ""
    frequency: int = 5  # default stock data fetch frequency in seconds
    symbols: List[str] = list()

# [...]
~~~

Next, you will set the graph interval to the rate at which the charts will refresh in real time without having to reload the browser page. This is provided by Plotly and Dash.

~~~{.python caption="settings.py"}
# [...]
 
    # Dash/Plotly
    debug: bool = True
    graph_interval: int = 10

# [...]
~~~

Finally, you will create a `Config` class that will parse the settings you have previously defined. It contains a `.env` file that contains the sensitive data. It is better to note that the file name has a prefix `SMD` to avoid mixing up with any other environmental variables.

~~~{.python caption="settings.py"}
# [...]
 
    class Config:
        """
        Meta configuration of the settings parser.
        """
 
        env_file = ".env"
        # Prefix the environment variable not to mix up with other variables
        # used by the OS or other software.
        env_prefix = "SMD_"  # SMD stands for Stock Market Dashboard
 
 
settings = Settings()
~~~

In the above `settings.py` file, `celery_broker` and `database_url` settings have been defined with default values. You will have to change their values with the correct settings and run the worker in a Docker container to get started with the settings. To keep the environment separated, you will create a `.env` file in the project root directory with the below content. The reason for using a `.env` file is to store sensitive credentials such as API keys, the stock symbols, and the frequency at which stock prices are fetched from the API.

~~~{.env caption=""}
SMD_API_KEY = "<YOUR SANDBOX API KEY>"
SMD_FREQUENCY = 10
SMD_SYMBOLS = ["AAPL","DOCN","EBAY"]
~~~

Next, you will need to get your API key for the sandbox environment. You can retrieve the key by signing up to Finnhub. The API key will be displayed on the dashboard upon login as shown below:

<div class="wide">
![Accessing Finnhub API key]({{site.images}}{{page.slug}}/few5xJg.png)
</div>

### Creating the Periodic Task to Fetch Data from API to the Database

Next, we create periodic tasks by creating a new `worker.py` file in the `app` module of the project as below and understand different functions used.

~~~{.python caption="worker.py"}
import finnhub
from celery import Celery
from app.db import pool
from app.settings import settings
 
# [...]
~~~

As you can see in the first few lines of code snippet above, you have imported the requirements needed to fetch and store data. The imports include `finnhub` which assists in fetching stock data from Finnhub API, `celery` which communicates via messages using a Redis broker to mediate between clients and workers, and the database for inserting fetched data into the database table.

After importing the requirements, you will configure the Finnhub client and Celery to use the Redis broker you defined earlier in the application's settings as below:

~~~{.python caption="worker.py"}
# [...]
 
client = finnhub.Client(api_key=settings.api_key)
celery_app = Celery(broker=settings.celery_broker)
 
# [...]
~~~

To fetch data periodically per stock symbol, you will programmatically create a periodic task for every stock symbol you initially defined in the `settings.py` file as below:

~~~{.python caption="settings.py"}
# [...]
 
@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Set up a periodic task for every symbol defined in the settings.
    """
    for symbol in settings.symbols:
        sender.add_periodic_task(settings.frequency, fetch.s(symbol))
 
# [...]
~~~

The code snippet above will register a new periodic per stock symbol after Celery is connected to the Redis broker.

Finally, you will define the fetch task that does most of the work. The fetch `function` fetches stock data for a given stock symbol from API and inserts the data into the database table `quotes` you earlier created.

~~~{.python caption="settings.py"}
# [...]
 
@celery_app.task
def fetch(symbol: str):
    """
    Fetch the stock info for a given symbol from Finnhub and 
    load it into QuestDB.
    """
 
    quote: dict = client.quote(symbol)
    # https://finnhub.io/docs/api/quote
    # quote = {'c': 148.96, 'd': -0.84, 'dp': -0.5607, 'h': 149.7, 'l': \
    #147.8, 'o': 148.985, 'pc': 149.8, 't': 1635796803}
    # c: Current price
    # d: Change
    # dp: Percent change
    # h: High price of the day
    # l: Low price of the day
    # o: Open price of the day
    # pc: Previous close price
    # t: when it was traded
 
    query = f"""
    INSERT INTO quotes(stock_symbol, current_price, high_price, low_price,\
    open_price, percent_change, tradets, ts)
    VALUES(
        '{symbol}',
        {quote["c"]},
        {quote["h"]},
        {quote["l"]},
        {quote["o"]},
        {quote["pc"]},
        {quote["t"]} * 1000000,
        systimestamp()
    );
    """
 
    with pool.connection() as conn:
        conn.execute(query)
~~~

As you have seen in the above code snippet, Finnhub client will assist you to fetch a stock price for a given stock symbol from the API. Upon successful retrieval of the quote, a SQL query to insert data into the database is defined. The function also connects to QuestDB and a new quote is inserted.

So far, you have configured the worker successfully and are ready to test it. To test the worker run the below command in the terminal window within the Python virtual environment and wait for sometime to let Celery start.

~~~{.bash caption=">_"}

$ python3 -m celery --app app.worker.celery_app worker --beat -l info -c 1
~~~

In the above command, using `-m` runs celery as the main module. The `celery --app app.worker.celery_app worker` executes celery on the same level as the `app` Python package and lets the worker load normally. The  `--beat` flag ensures that the periodic tasks run on a regular schedule since it queues the tasks for execution. The `-l info` flag ensures that the command logs the details on the console and the `-c`flag ensures the command executes as the Python statement.

Upon successful execution of the above command, you will see that the tasks are scheduled, and the database is slowly filling as shown below:

<div class="wide">
![Celery starting and updating]({{site.images}}{{page.slug}}/npycsnl.png)
</div>

<div class="wide">
![QuestDB table updating records]({{site.images}}{{page.slug}}/vTKNPnr.png)
</div>

So far in the project, you have created the following:

- A project root directory.
- A `docker-compose.yml` file to manage related services.
- The `settings.py` file that handles the application configuration.
- The `db.py` file for configuring the database pool.
- The `worker.py` file fetches data and stores it in the database.

## Visualizing the Data Using Plotly and Dash

In this section, you will set up the front end of the application using Plotly and Dash. Plotly comes with a framework known as Dash, enabling you to create a web application quickly and efficiently. Dash abstracts away the boilerplate useful in setting up a web server and creating several handles for the application.

### Getting Static Assets

This tutorial focuses less on the front-end of the application—meaning you won't be required to write stylesheets for the application—but just copy and paste existing code. You will create an `assets` directory in the root project directory and download the `styles.css` file using the `curl` command below. This is possible as Dash provides you with boilerplate code.

~~~{.bash caption=">_"}
$ curl -o assets/style.css https://github.com/verah-tech/stock-market/blob/main/assets/style.css
~~~

### Setting Up the Application

![Setting Up the Application]({{site.images}}{{page.slug}}/3OFABqK.png)

This is the last part of the application as you will be able to visualize the data you earlier fetched. You will create the `main.py` file in the `app` [packages](/blog/setup-typescript-monorepo) and performing several imports required by the project as below:

~~~{.python caption="main.py"}
# app/main.py
 
from datetime import datetime, timedelta
 
import dash
import pandas
from dash import dcc, html
from dash.dependencies import Input, Output
from plotly import graph_objects
 
from app.db import pool
from app.settings import settings
 
# [...]
~~~

The above code snippet starts with importing required dependencies such as  `dcc` and `html` which are responsible for getting the Dash core components that gives the code access to many interactive components such as dropdown fields. Then you import the `graph_objects` module from plotly which contains the objects such as figure, layout, data, and the definition of the plots like scatter plot and line chart that are responsible for creating the plots. Finally you import the `db` module used to create a connection to the database.

Next, you will define some helper functions and constants as below:

~~~{.python caption="main.py"}
# [...]
 
GRAPH_INTERVAL = settings.graph_interval * 1000
 
TIME_DELTA = 5  # last T hours of data are looked into as per insert time
 
COLORS = [
    "#1e88e5",
    "#7cb342",
    "#fbc02d",
    "#ab47bc",
    "#26a69a",
    "#5d8aa8",
]
 
 
def now() -> datetime:
    return datetime.utcnow()
 
 
def get_stock_data(start: datetime, end: datetime, stock_symbol: str):
    def format_date(dt: datetime) -> str:
        return dt.isoformat(timespec="microseconds") + "Z"
 
    query = f"SELECT * FROM quotes WHERE ts BETWEEN \
    '{format_date(start)}' AND '{format_date(end)}'"
 
    if stock_symbol:
        query += f" AND stock_symbol = '{stock_symbol}' "
 
    with pool.connection() as conn:
        return pandas.read_sql_query(query, conn)
 
# [...]
~~~

In the above code snippet, you have defined constants a graph update frequency `GRAPH_INTERVAL` and colors that will be used in coloring the graph `COLORS`. Next, you have defined two helper functions `now` and `get_stock_data`. The function `now` is responsible for fetching the current time in UTC while `get_stock_data` fetches the stock data from QuestDB that workers earlier inserted.

Next, you will define the initial data frame and the application used during rendering as below:

~~~{.python caption="main.py"}
# [...]
 
df = get_stock_data(now() - timedelta(hours=TIME_DELTA), now(), "")
 
app = dash.Dash(
    __name__,
    title="Real-time stock market changes",
    assets_folder="../assets",
    meta_tags=[{"name": "viewport", "content": \
    "width=device-width, initial-scale=1"}],
)
 
# [...]
~~~

In the above code snippet the initial data frame (`df`) will contain the latest 5 hours of the data fetched. This is useful in pre-populating the application with some data you fetched earlier.

Then you will create the application layout that will be rendered as HTML. Remember you won't be required to write any HTML since Dash will help you with that as shown:

~~~{.python caption="main.py"}
# [...]
 
app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H4("Stock market changes", \
                        className="app__header__title"),
                        html.P(
                            "Continually query QuestDB and \
                            display live changes of the specified stocks.",
                            className="app__header__subtitle",
                        ),
                    ],
                    className="app__header__desc",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                html.P("Select a stock symbol"),
                dcc.Dropdown(
                    id="stock-symbol",
                    searchable=True,
                    options=[
                        {"label": symbol, "value": symbol}
                        for symbol in df["stock_symbol"].unique()
                    ],
                ),
            ],
            className="app__selector",
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            [html.H6("Current price changes", \
                            className="graph__title")]
                        ),
                        dcc.Graph(id="stock-graph"),
                    ],
                    className="one-half column",
                ),
                html.Div(
                    [
                        html.Div(
                            [html.H6("Percent changes", \
                            className="graph__title")]
                        ),
                        dcc.Graph(id="stock-graph-percent-change"),
                    ],
                    className="one-half column",
                ),
            ],
            className="app__content",
        ),
        dcc.Interval(
            id="stock-graph-update",
            interval=int(GRAPH_INTERVAL),
            n_intervals=0,
        ),
    ],
    className="app__container",
)
 
# [...]
~~~

The above code snippet is all about setting up the application user interface where the charts will be displayed using HTML. It has one interesting part, the function `dcc.Interval` which is used to set up periodic graph refresh. It includes a constant `GRAPH_INTERVAL`, which (as earlier defined) is responsible for setting the graph update frequency.

Next, we define two callbacks that will listen to the input changes and the interval. The first callback will assist in generating the graph data and rendering the line per stock symbol.

~~~{.python caption="main.py"}
# [...]
 
@app.callback(
    Output("stock-graph", "figure"),
    [Input("stock-symbol", "value"), \
    Input("stock-graph-update", "n_intervals")],
)
# [...]

~~~

The function `generate_stock_graph` is responsible for filtering the data frames by the selected stock symbol, then getting the stock prices variations between different timestamps. Then it defines the color of the line chart that will be generated by the changes in stock prices.

~~~{.python caption="main.py"}
# [...]

def generate_stock_graph(selected_symbol, _):
    data = []
    filtered_df = get_stock_data(now() - timedelta(hours=TIME_DELTA), \
    now(), selected_symbol)
    groups = filtered_df.groupby(by="stock_symbol")
 
    for group, data_frame in groups:
        data_frame = data_frame.sort_values(by=["ts"])
        trace = graph_objects.Scatter(
            x=data_frame.ts.tolist(),
            y=data_frame.current_price.tolist(),
            marker=dict(color=COLORS[len(data)]),
            name=group,
        )
        data.append(trace)
# [...]

~~~

The function `graphs_objects.Layout` is responsible for drawing the graph objects. It draws the X-axis and Y-axis of the graph and assigns them names accordingly. Then it sets the background color, margins, and font color of the graph. It also sets the change of color of the graph objects when the mouse pointer hovers over them.

~~~{.python caption="main.py"}
# [...]
    layout = graph_objects.Layout(
        xaxis={"title": "Time"},
        yaxis={"title": "Price"},
        margin={"l": 70, "b": 70, "t": 70, "r": 70},
        hovermode="closest",
        plot_bgcolor="#282a36",
        paper_bgcolor="#282a36",
        font={"color": "#aaa"},
    )
 
    figure = graph_objects.Figure(data=data, layout=layout)
    return figure
 
# [...]

~~~

The other callback will be responsible for updating the percentage change representation of the stocks or a given stock.

~~~{.python caption="main.py"}
# [...]
 
@app.callback(
    Output("stock-graph-percent-change", "figure"),
    [
        Input("stock-symbol", "value"),
        Input("stock-graph-update", "n_intervals"),
    ],
)
# [...]

~~~

The function `generate_stock_graph()` is responsible for filtering the data frames by selected stock symbol, then gets the stock prices variations between different timestamps expressed as a percentage. Then it defines the color of the line chart that will be generated by the changes in stock prices.

~~~{.python caption="main.py"}
# [...]
def generate_stock_graph_percentage(selected_symbol, _):
    data = []
    filtered_df = get_stock_data(now() - timedelta(hours=TIME_DELTA),\
     now(), selected_symbol)
    groups = filtered_df.groupby(by="stock_symbol")
 
    for group, data_frame in groups:
        data_frame = data_frame.sort_values(by=["ts"])
        trace = graph_objects.Scatter(
            x=data_frame.ts.tolist(),
            y=data_frame.percent_change.tolist(),
            marker=dict(color=COLORS[len(data)]),
            name=group,
        )
        data.append(trace)
 
    layout = graph_objects.Layout(
        xaxis={"title": "Time"},
        yaxis={"title": "Percent change"},
        margin={"l": 70, "b": 70, "t": 70, "r": 70},
        hovermode="closest",
        plot_bgcolor="#282a36",
        paper_bgcolor="#282a36",
        font={"color": "#aaa"},
    )
 
    figure = graph_objects.Figure(data=data, layout=layout)
    return figure
 
# [...]
~~~

The last part is to call `run_server` on the `app` package when the script is called from the CLI as below:

~~~{.python caption="main.py"}
# [...]
 
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=settings.debug)
~~~

### Running the Application

First, ensure that all the Docker containers you created earlier are started and running. Then run the below command at the terminal to test the application with the actual data.

~~~{.bash caption=">_"}
$ PYTHONPATH=. python3 app/main.py
~~~

Then, navigate to <http://127.0.0.1:8050> to access the web application user interface as below:

<div class="wide">
![Accessing the web app dashboard]({{site.images}}{{page.slug}}/3djKrqn.png)
</div>

To get a better graphical representation of the stock price variations, select any stock symbol in the dropdown field and choose the desired stock symbol and let the application refresh as shown below. A chart with a better line graph will appear with varying stock prices as they load in real time from the API.

<div class="wide">
![Selecting specific stock symbol]({{site.images}}{{page.slug}}/ZyVMWQw.png)
</div>

## Conclusion

In this tutorial, you have seen how you can use Celery and Redis to fetch stock data from the Finnhub API in Python and store the data in QuestDB. You have also learned how to create useful dashboards using Plotly and Dash to visualize and present the fetched data to the user. Although the tutorial is for demonstration purposes and not actual trading, you have learned how to combine these powerful tools and software to create a bigger and more useful application. As a next step, try building a similar project for a dataset of your choice.

{% include cta/cta1.html %}
