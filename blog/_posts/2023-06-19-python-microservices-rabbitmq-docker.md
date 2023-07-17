---
title: "Building Python Microservices with Docker and RabbitMQ"
categories:
  - Tutorials
toc: true
author: Muhammed Ali
editor: Mustapha Ahmad Ayodeji

internal-links:
 - Python
 - Microservices
 - RabbitMQ
 - Docker
 - Software
excerpt: |
    Learn how to convert a monolith recipe API into microservices using Django and Flask. This article covers the usage of RabbitMQ for communication between microservices and provides a step-by-step guide on Dockerizing the microservices.
---
**We're [Earthly](https://earthly.dev/). We simplify and speed up software building using containerization. Earthly ideal for developers building microservices. [Check it out](/).**

Microservices are a software architectural style where an application is composed of small, independently deployable services. Each microservice has a single, narrowly defined responsibility and communicates with other microservices through APIs.

In this article, we will learn how to convert a [monolith](https://www.atlassian.com/microservices/microservices-architecture/microservices-vs-monolith#:~:text=A%20monolithic%20architecture%20is%20a%20singular%2C%20large%20computing%20network%20with,of%20the%20service%2Dside%20interface.) recipe API into microservices. We will use an [already-built Django and Flask application](https://github.com/khabdrick/recipe-app) and make them communicate with each other as one.

In the Recipe app we can create, delete, update, and comment on recipes. These features are divided into 2 microservices, one built with the [Django web framework](https://www.djangoproject.com/) and the other built with the [Flask web framework](https://flask.palletsprojects.com/en/2.2.x/). The Django application handles the creating, deleting and updating of recipes. While the Flask side handles the logic to comment on a recipe. Both Flask and Django use Postgres as their database.

We will also be introduced to [RabbitMQ](https://www.rabbitmq.com/) and its usage with Python frameworks for facilitating communication between microservices. After all that is done, we will create a docker container for each microservice and run everything using Docker Compose.

To follow up with this article, we need to have a working knowledge of Django, Flask and Docker.

## A Brief Introduction To RabbitMQ

[RabbitMQ](https://www.rabbitmq.com/) is an open-source message broker software that implements the [Advanced Message Queuing Protocol (AMQP)](https://www.amqp.org/). It allows applications to communicate and exchange messages (data) asynchronously, enabling loose coupling and promoting system resilience. RabbitMQ provides features such as routing, reliability, and scalability, making it a popular choice for many distributed systems. It can be used in a variety of scenarios, including serving as the backbone for microservices, handling background jobs, and implementing communication between different systems.

In RabbitMQ [the  **Producers** send messages to the **exchanges**](https://www.rabbitmq.com/tutorials/tutorial-three-java.html#:~:text=A%20producer%20is%20a%20user,user%20application%20that%20receives%20messages.), which then route the messages to one or many queues based on a specified rules. The Exchange checks if the *[routing key](https://www.cloudamqp.com/blog/part4-rabbitmq-for-beginners-exchanges-routing-keys-bindings.html?gclid=CjwKCAiA0cyfBhBREiwAAtStHNofBeG35nsG_iI6lQhtE62oPQNL9hsomiT8EPYm8hbI46eBUfSPdBoC-hIQAvD_BwE#:~:text=The%20routing%20key%20is%20a%20message%20attribute%20the%20exchange%20looks%20at%20when%20deciding%20how%20to%20route%20the%20message%20to%20queues%20(depending%20on%20exchange%20type).) matches a*queue name* before allowing the message to pass to its destination (the **consumer**). The messages could be from or to either of the Django or Flask application.

To work with RabbitMQ on Python we will use the [Pika](https://pika.readthedocs.io/en/stable/) library. Pika is a Python library that provides a framework for working with RabbitMQ. Pika allows developers to easily connect to a RabbitMQ server, declare and manage exchanges and queues, and publish and consume messages using the AMQP.

<div class="wide">
![Framework of RabbitMQ]({{site.images}}{{page.slug}}/mc7y8Yn.png)
</div>

We will use [CloudAMQP](https://www.cloudamqp.com/), a cloud-based message queue service, to manage our RabbitMQ server.

## Get CloudAMQP URL

[CloudAMQP](https://www.cloudamqp.com/) is a cloud-based message queue service that allows developers to easily and securely integrate messaging functionality into their applications. It is based on RabbitMQ, and offers a variety of features and benefits. It is also has a dashboard where we can manage and our RabbitMQ instances as well as see the metrics and logs to give us insight about the communication between our microservices.

To get started, go to the CloudAMPQ [homepage](https://www.cloudamqp.com/) and click on the **Get a managed message broker today** button:

<div class="wide">
![Cloud AMQP home page]({{site.images}}{{page.slug}}/tM9X9sB.png)
</div>

We will be prompted to create a new account. After we are done signing up, fill out the *Team name* form:

<div class="wide">
![create team page]({{site.images}}{{page.slug}}/mywjrQ4.png)
</div>

Click the *All instances* dropdown, then click the *Create new instance* button:

<div class="wide">
![CloudAMQP instance]({{site.images}}{{page.slug}}/DwhVciY.png)
</div>

From there, we can create a free instance and get its URL.

To get the instance URL, click on the instance created and copy the URL from there:

<div class="wide">
![CloudAMQP overview]({{site.images}}{{page.slug}}/Xn5Zji3.png)
</div>

Later in this article, We will use this URL provided by CloudAMQP to connect the microservice to the message queue to send or receive messages.

## Add RabbitMQ to the Django Microservice

For this part of the article, we will be working with the [*django_microservice*](https://github.com/khabdrick/recipe-app/tree/master/django-microservice) folder in the project.
We will create the producers that will send the message/data for the created, updated, and deleted recipes. We will also create the consumers to consume the data that will be sent from the Flask microservice regarding the comment and the recipe the comment belongs to.

Finally, we will create Docker and Docker compose configurations for running the Django microservice.

### Developing the Producer and Consumer

We will first start with the Producer. The following is the code that sends messages from the Django microservice. We can get this going by copying the following code from the *django-microservice/app/producer.py*:

~~~{.python caption="producer.py"}
import pika, json

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='django', \
    body=json.dumps(body), properties=properties) 
    # routing key here must match the queue name in the consumer\
    # of the flask app
~~~

> Please be sure to replace the value of `params` with the URL we got from CloudAMQP.

The code imports the necessary modules and then sets up a connection to RabbitMQ message broker using the provided `URLParameters`.

It then creates a `BlockingConnection` and a `channel` object. The `BlockingConnection` object establish and manage connection to the RabbitMQ message broker. The `channel` object (which is created from the `connection`) creates a channel on which messages can be published.

The `publish` function accepts a `message` and a `body` argument. It handles the publishing of messages with the provided `method` and `body`. The `body` argument represents the message or data to be published and the `method` argument is used to set the properties of the message.

The `body` is serialized to JSON format before being sent to channel with the `'main'` routing key.

Now we will call this producer in the `create`, `update` and `destroy` methods of our `RecipeView` class in the [*view.py*](https://github.com/khabdrick/recipe-app/blob/master/django-microservice/app/views.py) file. This is so that RabbitMQ can receive the messages when it is sent from the [viewset actions](https://www.django-rest-framework.org/api-guide/viewsets/#viewset-actions).

Now, when an action takes place in `RecipeView`, RabbitMQ will be notified through this producer.
To do this, update our *django-microservice/app/views.py* file to look like the following:

~~~{.python caption="views.py"}
...
from .producer import publish

class RecipeView(viewsets.ViewSet):
    ...

    def create(self, request):
        ...
        publish('recipe_created', serializer.data) #new
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        ...
        publish('recipe_updated', serializer.data) #new
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        ...
        publish('recipe_deleted', pk) #new
        return Response(status=status.HTTP_204_NO_CONTENT)
~~~

In the code above, we added the `publish()` function (which we created earlier) to each of the viewset action so that when an action is performed on those views, JSON data is sent to the message queue. This data will be consumed by the Flask microservice and it will update the database as necessary.

For the Django microservice consumer, paste the following code in *django_microservice/consumer.py* to add a comment to the specified recipe. The data for the comment text and recipe ID is sent from the Flask microservice:

~~~{.python caption="consumer.py"}
import pika, json, os, django
from django.http import JsonResponse
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "recipe.settings")
django.setup()

from app.models import Recipe, RecipeComment

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='flask') # this will match the 
# routing key in the producer of the flask app


def callback(ch, method, properties, body):
    print('Received in Django microservice')
    print(body)
    data = json.loads(body)
    # print(data)
    recipe_id = data[0]
    comment_text = data[1]
    recipe = Recipe.objects.get(pk=recipe_id)
    comment = RecipeComment(recipe=recipe, comment_text=comment_text)
    comment.save()
    print('Added a comment')


channel.basic_consume(queue='flask', on_message_callback=callback, \
auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()

~~~

The code import the necessary modules and then sets up the Django environment. This is important for ensuring that the Django web application is configured correctly, and that the Python interpreter knows which settings module to use for the Django application.

We then imports the `Recipe` model from the app. The `channel.queue_declare()` method declares a queue named `flask` that will be used to consume messages sent from the Flask application with a matching routing key.

The `callback` function handles incoming messages, which are deserialized from JSON to obtain the `id` from the `body` passed in. This function takes four arguments: `ch` (the channel object), `method` (the delivery method that will be sent my RabbitMQ), `properties` (associated metadata attached to the message), and `body` (the message body).

Finally, we set up a basic consumer using `channel.basic_consume()`, which listens for messages on the `flask` queue and calls the `callback` function to handle each message. The `channel.start_consuming()` method starts the message consumption loop.

The Recipe ID and comment text is obtained from the JSON serialized body and the corresponding Recipe object is retrieved using the `Recipe.objects.get()` method, and the comment is saved to the database.

At this moment, our Django microservice can send a message to the Flask microservice whenever a recipe is created, updated, or deleted. The Django microservice can also receive a message from the Flask microservice whenever a comment is made on a recipe.

Now that we have the Django part ready, we can now package it with Docker to isolate it from the Flask microservice.

### Dockerize the Django Microservice

Docker allows developers to package the application, including its dependencies and configuration, into a container that can run consistently across different environments. We will need it to Dockerize our project so that we can easily run and test the application with one command and isolate it from other microservices.

To Dockerize our application, add the following configuration in *django_microservice/Dockerfile*. The following code initializes a Python Docker image that the Django microservice will run on and installs the necessary dependencies. This Dockerfile will be the base for the Django server and the RabbitMQ server:

~~~{.dockerfile caption="Dockerfile"}
FROM python:3.7

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
~~~

Now, we can create the Docker Compose configuration by adding the following code in *django_microservice/docker-compose.yaml.* The following code uses the Dockerfile we created earlier to run the Django service. The `python -u consumer.py` command runs the *consumer.py* script that listen for messages that are sent from the Flask service. We also set the configuration to set up and run the PostgreSQL database.

~~~{.yaml caption="docker-compose.yaml"}
version: '3.8'
services:
  django:
    build:
      context: .
      dockerfile: Dockerfile
    command: 'python manage.py runserver 0.0.0.0:8000'
    ports:
      - 8000:8000
    volumes:
      - .:/app
    depends_on:
      - db

  mq:
    build:
      context: .
      dockerfile: Dockerfile
    command: 'python -u consumer.py'
    depends_on:
      - db

  db:
    image: postgres:10.3
    volumes:
      - db:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=khabdrick
      - POSTGRES_PASSWORD=secure-password
      - POSTGRES_DB=comments
    ports:
      - "5435:5435"

volumes:
  db:
~~~

## Add RabbitMQ to Flask Microservice

For this part of the article, we will be working with the *flask_microservice* folder in the project. Here, we will create the producers that will send the message/data to the Django service when a user comment on recipe. We will also create the consumers to consume the data for the created, updated, and deleted recipes sent from the Django microservice.

Finally, we will develop the Docker and Docker compose configurations for running the Flask microservice.

### Developing the Producer and Consumer

We will start with the Producer. The following is the initial code that receives a message from the Django microservice. We can get this going by adding the following code in *flask_microservice/producer.py*:

~~~{.python caption="producer.py"}
import pika, json

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd') 

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='flask', \
    body=json.dumps(body), properties=properties)
~~~

> Please be sure to replace the value of `params` with the URL we got from CloudAMQP.

The code is similar to the `producer` code in the Django microservice, however, we published the message to the `flask` queue which is specified by the `routing_key = "flask"`. The Django service listen to messages sent to this `queue`.

The data we need to publish to the Django microservice is the recipe comment data, so we will add the `publish()`  function to the `comment()` function in the *flask_microservice/main.py* file:

~~~{.python caption="main.py"}
...

from producer import publish

...
@app.route('/api/comment', methods=['POST'])
def comment():
    
    data = request.get_json()
    print(data['recipe_id'])
    recipe_id = data['recipe_id']
    comment_text = data['comment_text']
    messages = [recipe_id, comment_text]

    # publish messages
    
    publish('commented', messages)    

    return jsonify({
        'message': 'success'
    })

…

~~~

We will create a consumer that gets the published data from the Django microservice because we need the Flask microservice to be aware of the changes made to the recipes. Then the consumer updates the Flask database based on the data it receives.

Add the following code in the *consumer.py* of the Flask microservice:

~~~{.python caption="consumer.py"}
import pika, json

from main import Recipe, db

params = pika.URLParameters('amqps://tyfodnmd:t0Ps2Jnw97Epl3YNe67zm2mjdDdir5Y8@rat.rmq2.cloudamqp.com/tyfodnmd')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='django') # this must match the 
# routing key of the Django microservice 


def callback(ch, method, properties, body):
    print('Received in Flask microservice')
    data = json.loads(body)
    print(data)

    if properties.content_type == 'recipe_created':
        recipe = Recipe(id=data['id'], title=data['title'], \
        time_minutes=data['time_minutes'], price=data['price'], \
        description=data['description'], ingredients=data['ingredients'])
        db.session.add(recipe)
        db.session.commit()
        print('recipe Created')

    elif properties.content_type == 'recipe_updated':
        recipe = Recipe.query.get(data['id'])
        recipe.title = data['title']
        recipe.time_minutes = data['time_minutes']
        recipe.price = data['price']
        recipe.description = data['description']
        recipe.ingredients = data['ingredients']
        db.session.commit()
        print('recipe Updated')

    elif properties.content_type == 'recipe_deleted':
        recipe = Recipe.query.get(data)
        db.session.delete(recipe)
        db.session.commit()
        print('recipe Deleted')


channel.basic_consume(queue='django', on_message_callback=callback, \
auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()
~~~

This code sets up a RabbitMQ consumer that listens to a queue named 'django' for messages.. When a message is received, it is parsed from a JSON format and the content type of the message is checked to determine the appropriate action to take.

If the content type is `recipe_created`, a new recipe object is created and added to a database. If the content type is `recipe_updated`, an existing recipe object is updated with the new data provided in the message. If the content type is `recipe_deleted`, the corresponding recipe object is deleted from the database. The consumer uses a `callback` function to handle the received messages.

### Dockerize the Flask Service

The Dockerfile for the Flask side is the same as the Django. So, just add the following code in *flask_microservice/Dockerfile*:

~~~{.dockerfile caption="Dockerfile"}
FROM python:3.7

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
~~~

The Docker compose configuration here will run the Flask, PostgreSQL, and RabbitMQ servers at once. We can get this done by adding the following code in *flask_microservice/docker-compose.yaml*:

~~~{.yaml caption="docker-compose.yaml"}
version: '3.8'
services:
  flask:
    build:
      context: .
      dockerfile: Dockerfile
    command: 'python main.py'
    ports:
      - 5000:5000
    volumes:
      - .:/app
    depends_on:
      - flask_db

  mq:
    build:
      context: .
      dockerfile: Dockerfile
    command: 'python -u consumer.py'
    depends_on:
      - flask_db

  flask_db:
    image: postgres:10.3
    volumes:
      - db:/var/lib/postgresql/data/
    environment:
      - POSTGRES_USER=khabdrick1
      - POSTGRES_PASSWORD=secure-password
      - POSTGRES_DB=comments
    ports:
      - "5433:5433"

volumes:
  db:
~~~

## Run All Components With Docker Compose

Let us first build the Docker images for the project.

Build the Django microservice by running the following in the *django_microservice* directory:

~~~{.bash caption=">_"}
docker compose build
~~~

We can build the Flask microservice by running the following in the *flask_microservice* directory:

~~~{.bash caption=">_"}
docker compose build
~~~

Before we run the application, we need to run migrations and create a superuser that we can use to access data from the Django admin.

Navigate to the *django_microservice/* directory and run the migration commands for the database:

~~~{.bash caption=">_"}
docker compose run django sh -c "python manage.py makemigrations" 
docker compose run django sh -c "python manage.py migrate"
~~~

Then run the following to create a superuser:

~~~{.bash caption=">_"}
docker compose run django sh -c "python manage.py createsuperuser"
~~~

Now run the migration commands for the Flask microservice in *flask_microservice/* directory:

~~~{.bash caption=">_"}
docker compose run flask sh -c "python manager.py db init"
docker compose run flask sh -c "python manager.py db migrate"
~~~

Now run the Django microservice with the following command and access the application on the browser with *<http://0.0.0.0:8000/admin/>*:

~~~{.bash caption=">_"}
docker compose up
~~~

 Fill out the login form with the superuser credentials we just created, and we will be able to access our application.

Run the Flask microservice with the following command while in the *flask_microservice* directory:

~~~{.bash caption=">_"}
docker compose up
~~~

On another terminal window, run the following [cURL command](https://curl.se/docs/manpage.html) to create a new recipe:

~~~{.bash caption=">_"}
curl -H 'Content-Type: application/json'  -d \ 
'{"title":"French toast","time_minutes":35, "price":45, \
"description":"This is the description", \
"ingredients":"this is ingredient"}'  \
-X POST http://0.0.0.0:8000/recipe
~~~

Output:

~~~{ caption="Output"}
{"id":23,"title":"French toast","time_minutes":35,\
"price":"45.00","description":"This is the description",\
"ingredients":"this is ingredient"}
~~~

We can now comment by running the following command:

~~~{.bash caption=">_"}
curl -X POST http://127.0.0.1:5005/api/comment -H \
'Accept: application/json' -H 'Content-Type: application/json' \
-d '{"recipe_id": 23, "comment_text":"This recipe is time efficient :)"}'
~~~

Output:

~~~{ caption="Output"}
{
    "message": "success"
}
~~~

We can go to our instance on CloudAMQP and click the "**RabbitMQ Manager**" button, and we should see a dashboard as shown in the image below. This shows that there are some activities between the microservices:

<div class="wide">
![RabbitMQ manager]({{site.images}}{{page.slug}}/ywOa2xY.png)
</div>

Now we can go to the Django admin, and we will see that a recipe was created. And we can also see a comment attached to it.

<div class="wide">
![Django admin]({{site.images}}{{page.slug}}/7p1oo8H.png)
</div>

## Conclusion
<!--sgpt-->
So, today we went over how to connect Django and Flask microservices using RabbitMQ and Python's Pika library. We covered the basic setup for a message broker, producer, and consumer service, along with Dockerizing these microservices. 

If you're working on a bigger application, try splitting it into smaller bits based on features and experiment with RabbitMQ to connect them. And if you're building microservices, you might want to make your build process a breeze with [Earthly](https://www.earthly.dev/). It's a tool worth checking out to streamline your development workflow.

Happy coding!

{% include_html cta/bottom-cta.html %}