Message Queues (RabbitMQ)
==================================
Queues can be used to send and receive messages in an asynchronous way. In principle it is possible to send messages, and retrieve and process these messages minutes/hours/days later. The underlying message queue system is responsible for persisting messages in case they are not processed immediately.

The common use case is to send messages into a queue system, which are processed (almost) directly. Instead of directly sending requests/messages to a specific microservice (e.g. using REST), with message queues the configuration of where messages are sent and which microservices process the messages is decoupled from the sending microservice (orchestration vs. choreography). As an example, a microservice might send out a message "a new customer just registered", and the message queue forwards the message to all consumers like a microservice creating a new database entry, and a microservice sending out a welcome mail, and another microservice which adjusts internal statistics - all while the microservice of the originating message does not know about any of this.

A simple use case, which currently is implemented in our project, just sends messages from one microservice to another microservice through a single queue. In more complex cases messages can be put into several queues, may be duplicated so that they can be received by multiple microservices, can automatically trigger a response message in certain cases (e.g. when it is not processed in time), etc. As such, properly configuring a message queue system is a complex task and (currently) out of scope for this course.

## Key concepts
 - messages are the entities published into and received from a message queue system
 - messages are binary (`byte[]`), but it is a common practice to use JSON strings
 - messages cannot be sent into a queue directly, instead messages are sent to an exchange
 - using the default exchange means that the sender needs to specify exactly to which queue the message should go. The queue name is specified in the `routing_key` parameter.
 - messages may contain a correlation id, which can be used for logging and to identify response messages
 - it is not guaranteed that each message is only delivered once, which is why the receivers need to act gracefully when receiving duplicates
 - when receiving, it is possible to subscribe to specific queues and be informed of new messages (this is implemented in our project)
 
The RabbitMQ offers some good tutorials giving more detail: https://www.rabbitmq.com/tutorials/tutorial-one-java.html

## Code Example
In our code examples we use the [AMQP](https://www.amqp.org/) API as it promises to be less coupled to the actual implementation.

The [CloudRabbitConfig](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/solution-20-Use-Message-Queues/src/main/java/com/sap/bulletinboard/ads/config/CloudRabbitConfig.java) bean uses the `Spring Cloud` plugin to parse the `VCAP_SERVICES` environment variables and provide the `AmqpAdmin` and `AmqpTemplate` beans which can be used to communicate with the bound RabbitMQ backing service.

### Publishing
Before publishing individual messages, we setup the system once. In our simple example we just declare a queue (which will automatically be bound to the default exchange), see [constructor code in StatisticsServiceClient](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/solution-20-Use-Message-Queues/src/main/java/com/sap/bulletinboard/ads/services/StatisticsServiceClient.java).

Publishing of individual messages is wrapped by a Hystrix Command `IncrementCounterCommand`, as publishing may fail or run into timeouts. As described above, we use the default exchange, which is why we use the routing key to specify the queue into which the message should be published.

### Receiving
The code used to receive messages is more coupled to the RabbitMQ implementation as we were unable to find a more general approach using AMQP classes.

As in the publishing case, the `CloudRabbitConfig` bean helps us defining the `AmqpAdmin` and `AmqpTemplate` beans. 

Using the [StatisticsListener](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/solution-21-Receive-MQ-Messages/src/main/java/com/sap/bulletinboard/ads/services/StatisticsListener.java) bean we can register listener implementations for specific queues. Note that the queue must be declared first in case it does not already exist in the queue system.

## Reliable Messaging in-depth learning module
The [Reliable Messaging](https://github.wdf.sap.corp/cloud-native-dev/resilience/tree/master/ServiceToService) module provides a basic understanding about RabbitMQ Message Broker using the Advanced Message Queue Protocol (AMQP) and demonstrates how to implement that using Spring AMQP. For implementing reliable messaging we use and explain concepts like “publisher confirms” and “consumer acknowledgements” to avoid message loss. This includes also an appropriate handling of messages when failures happen in any part of the system.


