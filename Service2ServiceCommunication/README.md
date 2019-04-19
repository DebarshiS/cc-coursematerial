# Service-to-Service Communication - Detail Notes

## General Communication Guidelines

* Use Hystrix for all communication (and anything else critical that can fail)

* Use **asynchronous messaging (Message Queues)** when you do not need the result and can live with `eventual consistency`. This choreography approach supports a loosly coupled service composition and allows other interested services to subscribe dynamically during runtime.

* All **synchronous communication** should be wrapped in Hystrix since you cannot control latency and/or behavior of the client service.

## Hystrix in-depth learning module
The [Hystrix](https://github.wdf.sap.corp/cloud-native-dev/resilience/blob/master/Hystrix/README.md) module provides an in-depth understanding about Hystrix as Resilience Library (using hystrix-javanica). It assembles good practices on how to implement and configure it in context of your cloud web application in order to isolate points of access to remote systems, services and 3rd party libraries, stop cascading failure and latency.

## Reliable Messaging in-depth learning module
Please read more about Message Queues (RabbitMQ) and reliable messaging [here](MessageQueue.md).


## Suggestions for communication failure cases in more detail:
* When a Hystrix command fails, the client / caller should implement a fallback. 
* For communication: Fail fast, i.e. after 1 sec. (Tuning: Find out what the 99%-ile of response time is and tune the timeout to that value.)
* What does the user see? When a client service is not available, you could hide the UI part, hide or disable the button. It is best to make it so that the users don't even notice that there is a problem (no layout changes!) until they finally want to do an action that would not work.
* When it is information and not action, show cached content when possible (to make the page look normal)

#### Case: "READ MANDATORY":  When you really need the information for full functionality 

Example: ADS service, user is not authorized because USER Service is not there.
* If possible show cached information
* Can you hide the error / effects?
* Try to keep the UI the same, i.e. keep the 'Create Ad' Button visible and even appearing activated (since not everyone will want to use it) as if they were authenticated.
* When user tries, give error message and give idea when to try again
* What type of object to return on Java level? 
* If Hystrix Circuit is open to User service, this will make the communication fail immediately and the information gets returned to the UI immediately.

#### Case "WRITE ERROR": User filled form and wants to create add but the 'Create Add' does not work

You need a business decision. Normally you want to create and read it immediately from the DB so the user can see what it looks like. You cannot make the user lose time. 
* When user presses 'submit' UI will show 'message being processed'. UI will poll every 5 secs. 
* One can use two message Qs for communication to CreateAd service and another one for response. But this is only done when absolutely necessary from a business perspective. Example: Long-running job like upload & processing videos. 
* When you want to be extreme: Store input in backend under GUID, send GUID to front with message "sorry ... save link and click later to complete your work"

#### Case "READ CACHED":  
* When you read stuff e.g. a catalog, or a count that is OK when approximate, we can show cached value.
* If possible hide the potential error when the user doesn't necessarily click on the button.
* If there is no good cached value you have to show 'sorry'
* Implementation: Only use small memory footprint in the Java process

#### Case "REPEAT PROTECTION"
* For requests that have consequences and are not idempotent (e.g. 'buy now', 'add to cart', ...) ...
* Users press F5 when impatient, click on a button twice, ...
* ==> Write code that protects against this, can be done by different means
* This is stateful semantics and shared memory cache is not acceptable
 
#### Multi-Step Transactions

Often a process consists of many steps, eg.: Reserve --> Address Verification --> Pay --> Ship
* Logically there is a 'Buying Process'. How to implement?
* Central orchestration 'Buy Process' that uses command objects and reverse commands for all steps in the process 
  * Not good because all teams / services are tightly connected this way?
  * BUT: We need this level since otherwise the knowledge of the process steps is spread all over the processes --> no SRP!
  * And: SAP software is always highly configurable (even for the cloud) and therefore we need one class (the process level) which deals with that configuration  * 

## Hystrix Code Samples
- [Course Sample Code](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc), UserServiceClient and GetUserCommand [package](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/solution-24-Make-App-Secure/src/main/java/com/sap/bulletinboard/ads/services)
- [Hystrix Examples](https://github.wdf.sap.corp/refapps/SimpleHystrixConceptsPOC), synchronous and asynchronous execution)
