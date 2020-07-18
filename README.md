# paycom-pubsub-broker
This repository is my implementation of an assigned project from Paycom's Virtual Summer Engagement Program during Summer 2020 in creating a program to replicate pub-sub messaging between various clients. It is based on Python 3.8, with notable libraries containing **asyncio** to build an asynchronous, concurrent broker server, along with the **asyncpg**, **gino**, and **SQLAlchemy** libraries to connect to a PostgreSQL-based database storing client information, messages, topics, and more. 

## Installation
With the assumption of having Python 3.8+ installed, use the package manager **pip** to install the required libraries as mentioned above, which are listed in the **requirements.txt** file in this repository. 

```pip install -r requirements.txt```

Additionally, having a PostgreSQL server running with a user and database to to utilize, import the SQL file **database.sql** which contains the necessary tables to run the broker server and sample data that fulfills the non-functional requirements listed in the project guidelines provided by Paycom. After editing the **.env** file to the correct credentials, you can simply run the file **run.py** with Python and the broker server should be good to go!

## Usage
The broker server is based on the TCP protocol, and processes information by sending and receiving JSON text, ending it with the newline character, and **encoding it in UTF8**. For example, to connect and authenticate to a user account, you would have to create a new connection to the broker server and send a JSON such as the one below to authenticate as one of the provided subscribers stored in the database, provided that you have encoded the request in UTF8.

```{"action":"connect","user_email":"tientavu@tamu.edu"}\n```

The JSON text must always contain the "action" parameter and its required arguments in order to process the request. A list of actions and its required arguments are shown below.

### Client Requests
The following categorized actions below are several actions that a client can send to the broker server to receive and process various information.

#### Authentication
* **create(user_email, user_type)**: Allows the client to create a user account, and will be identified as a pub or a sub with the 'type' parameter. The 'type' parameter must be sent as either 'publisher' or 'subscriber'. 
* **connect(user_email)**: Allows the client to login to a created user account, and will be authenticated and identified as a pub or sub. An example of this action is provided in the introduction to the Usage section above.

#### Publishers
* **create_topic(topic_name)**: Allows a publisher to create a topic, given the name of the topic. 
* **publish_msg(topic_name, msg)**: Allows the publisher to publish a message to a given topic name.

#### Subscribers
* **list_topics()**: The broker server would return all of the topics created and saved from publishers for the potential to subscribe or unsubscribe for messages.
* **subscribe(topic_name)**: Allows a subscriber to subscribe to a particular topic, and begin receiving messages that get published towards this topic.
* **unsubscribe(topic_name)**: Allows a subscriber to unsubscribe to a particular topic, and halt all messages to be received from this particular subscriber in a given topic.

### Server Requests
The following actions below are several actions that a broker server would send to the client in lieu of a request that a client has sent to the broker server.

* **success(code)**: After a client sends a request to the broker server, the broker server would send in a success action JSON message with a code of 0 to indicate that their request has been processed successfully.
* **error(message)**: After a client sends a request to the broker server, the broker server would send in a failed action JSON message that indicates an error. The message parameter in the JSON will indicate what has gone wrong.
* **broadcast(message)**: After a publisher successfully publishes a message to a topic, the broadcast request would be sent to all clients who are subscribed to the topic that the publisher wished to publish to. The 'message' parameter would contain the actual message that the publisher has wished to send.
* **list_topics(topics)**: After a subscriber sends a request to the broker server to probe on a list of topics, the broker server would send in a JSON message with an action 'list_topics' containing an array of topic names in the 'topics' parameter.
* **unread(message)**: After a client successfully logins and authenticates as a subcriber, the broker server would send in any messages that a publisher has published to a particular topic the client has subscribed to when the client was not present and connected in the TCP broker server.
