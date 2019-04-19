# Logging and Tracing - Detail Notes

* [Practical Considerations](#practical-considerations)
* [General Information and Guidelines](#general-information-and-guidelines)


# Practical Considerations

## Important tools and commands
* `cf logs <appname> --recent` : Shows recent log output for app
* `cf logs <appname>` in another window: See running log for app in separate window
* [Pivotal CLI Log Documentation](https://docs.pivotal.io/pivotalcf/devguide/deploy-apps/streaming-logs.html)

## Different types of logs for different target groups

You should clearly differentiate between two use cases for logging and adapt the logs accordingly.

### Developers: Debugging

* Teams decide what their services need as log information; this totally depends on service semantics
* There is **no debugging in production**, analysis is done in test space while trying to reproduce the bug
* For debugging case: set log level for debugging / analysis and write whatever is needed for a certain bug; then redeploy in testing to run it

### DevOps and Engineers / Admins: Production
* DevOps just needs to know if things are running OK, so their **focus is to see error cases and performance**
  * Only relevant question: "Request processed or not?" (and in what time, with what status codes)

Example Log (logical): A sends request to B which sends request to C
```
  Log Msg 1: A sending request to B
  Log Msg 2: B response status 'OK'
  Log Msg 3: A writes latency time of B request
  When B calls C, the same goes for the request to C so that you can see latencies between services
``` 

* In local deployments (all apps in one data center) the network delay is not important to log because it is just a few msecs but for remote deployments of a target service, the network latency must be measured as well and separately (i.e. in addition: B receiving request). But latency may be an issue even locally! --> Figure out what is relevant in your environment and log that until it is no longer an issue!
* For DevOps case one usually only needs to have ONE log entry per request like 'A.request.received' with the latency and status for response. The other services do not need to log if things are OK, only for error cases.
* CorrelationID is not important for DevOps, only for developer level analysis
* Production level logs cannot contain sensitive information, therefore logs are minimal there. Security and data privacy is a huge issue. E.g. for medical systems, developers cannot even see the information, therefore access to production logs is very limited. This depends on industry and regulations.

### Sizing, Performance and Practical Tips

**Log volume must be controlled and sized just like any other resource!**

* There must be **limit of log messages per service per second**. The log volume quota **must be independent of request volume** and scaling since the infrastructure cannot handle more than a given volume. --> We need **batching or sampling.**
* For reducing log volume you can: 
  * Log only a fraction, e.g. 1% of requests (can be implemented by random numbers),
  * or log averages using a library like [Metrics](https://github.com/dropwizard/metrics) (logs averages / statistics of values at configuratble intervals, e.g. every 5 seconds).
* **Try to be terse!** Use short categories, e.g. "LaSB" = "Latency of Shopping Basket".
  * Naming rules? Are useful but not necessary. The names are totally free and can be decided by the teams. When you put a dashboard together, e.g. for latencies, each service has their own widget and will access their own log keys.
* Logs should show absolute numbers that do not require computation in Kibana; example: log absolute latency times and not timestamps; Kibana can do averages etc but should not be used to do math operations 'substract' etc.



# General Information and Guidelines
Logging means "creating and storing a permanent record of events that can be reviewed, printed, and analyzed". This record usually contains information about the source of the record, a timestamp of the event, a message, and a severity which specifies the importance of the record. As in the logs all the information of an event is kept which operators need to control the status of the system, the database, and all applications, the logs are most important. Logs get written automatically and with a predefined severity which can be modified during runtime.

XS2 will provide a common Logging API for Java Applications, so all the logs have a common format and can be displayed and analyzed in the same viewer e.g. Kibana or SAP Solution Manager.

Logging and Tracing is very important as it is not possible to attach a debugger to an application running in Cloud Foundry.

## How much *can* be logged?
When deciding how much to log, and how much is too much, it is a good idea to understand the technical limitations of the systems involved.
According to [this image](http://logging.apache.org/log4j/2.x/images/async-throughput-comparison.png) you can expect both Logback and Log4j2 to be able to log at least one million messages per second, possibly even way more than that.
With 160 characters in each log message, this means you can log at least 1 GBit/sec.
Based on this we can conclude "logging isn't the bottleneck", as pointed out in more detail in [this article](http://xorlev.com/blog/2013/08/11/overengineering-log4j2-s-asyncappender/).

Cloud Foundry distributes all log messages to Doppler instances.
Depending on the configuration, the messages are then sent to syslog drains, or the traffic controller aggregates the data and forwards it to the ELK stack ("firehose").
With enough VMs dedicated to Doppler and ELK, several hundred messages per second and application instance should be managable.
According to Sergey Balashevich from Altoros a simple setup with two dedicated machines for Logstash (parsing) is able to process around 1.3 million messages an hour (360 messages per second on average).

![Loggregator Diagram](https://docs.cloudfoundry.org/loggregator/images/architecture/loggregator.png)

[Logging architecture in CF](https://docs.cloudfoundry.org/loggregator/architecture.html)

**Note:** Be aware that if you are using the SCP Cloud Foundry **Application Logging Service** the log limits are far lower than stated above. ([SCP CF Services Pricelist](https://wiki.wdf.sap.corp/wiki/display/CPC15N/SAP+Cloud+Platform+-+Internal+Pricelist+for+Neo+and+Cloud+Foundry+Services#SAPCloudPlatform-InternalPricelistforNeoandCloudFoundryServices-ApplicationLogging), [SCP CF Application Logging Plans](https://jam4.sapjam.com/wiki/show/PjbYzmTg8LVR4awH6kHfPO))

## How much *should* be logged?
On the one hand this question correlates with the answer of "How much *can* be logged" and on the other hand, it is not easily possible to add log statements to a running application. If some information is needed *after* an event already occurred, this obviously is not possible at all.

**In general, you should log as much as you feel might be necessary in the future.**
While the approach of adding trace methods for every single method entry and exit generates too many log messages, it is a good idea to provide detailed tracing messages for key methods.
As an example, REST endpoint invocations should be logged, giving information about the provided arguments, and the time needed to fulfill the request.

**Writing logs is subject to continuous improvement.**
Over time it is a simple task to find out which log messages appear too often, while adding little value.
These then should be removed or thinned out.

We suggest to first implement logging according to the other information provided in this document.
Then, after measuring the number of logged messages for typical use cases, this can be fine-tuned.

## What should be logged?
Several cases have to be considered when deciding what to log.
In addition to the following hints you should think about who might need specific data, and when.
The more you know about possible scenarios, wishes of different stakeholders, and already setup rules and regulations, the better you can prepare.
If possible, invite collaborators and other stakeholders interested in your system to brainstorm on this topic.

**Note:** In this list we do not go into technical implementation details.
For most tasks there are helpful implementation tricks and dedicated tools available.
Some suggestions are presented in a later section of this document.

#### General
Cloud Foundry automatically includes a timestamp and information about the corresponding microservice instance for each log line. 

**Timestamp**:
Every log entry should contain a timestamp, even if Cloud Foundry already adds one.
One reason is that the application might be run outside of the Cloud Foundry infrastructure, for example during development.
Furthermore, the timestamp added by Cloud Foundry is added by another process, which means the timestamp is less precise.

**Correlation ID**:
In addition log entries should include information that make it possible to connect several related log entries.
This is especially important for operations spanning multiple microservices.

As an example, a user might send a request to a frontend service.
This in turn could trigger requests to two other microservices.
If one of these downstream services needs to log important information, this log entry should contain a reference to the initial request sent to the upstream frontend service.

Such correlation IDs (or session IDs) might already exist as part of the first incoming request.
If not they can be generated when a new request is received.
This ID then should be propagated so that the code executed as part of the request can use it in logging messages - including code of downstream services.

The decision of format and procedure is a typical cross topic that must be aligned across service boundaries.

**Category**:
In order to be able to analyze a high number of log entries, it is helpful to include a category for each log entry.
Using such category information it is possible to filter the log messages and concentrate on specific aspects.
Such categories could be "SQL", "Authentication", "Tracing", "Order", ...

**Format**:
The log messages need to be parsed and filtered, so it is important to provide the log entries in a machine readable format.
This format should also be the same across all microservices logging into, for example, the same ELK stack instance. In the past the [List Log format 2.0](http://help.sap.com/saphelp_nw73ehp1/helpdata/en/53/82dae7c2f5439a8afd1b0ee95c2e45/content.htm?frameset=/en/47/e11b700b713c86e10000000a42189c/frameset.htm) was used by the Log Viewer tool and AS Java for audit logs. This format is not suitable for the ELK stack but the fields, written, might be the same. There might be further changes once the central log server/service is available.

One possibility is to log using JSON:
```javascript
{   
    "Version": "1.0",
    "DateTime": "2015 10 31 11:33:50:663",
    "TimeZone": "+6:30",
    "Severity": "WARN",
    "SourceName": "com.sap.foo.bar.Recommendations:123",
    "CSN Component": "BC-JAS-ADM", 
    "ThreadName": "qtp1782580546-19",
    "Correlation ID": "663a1be8-4a43-11e5-885d-feff819cdc9f",
    "MsgText": "timeout connecting to recommendation.some.url:8080",
    "Categories": ["timeout", "recommendation", "network"]
}
```

#### Operational
When your microservice starts, you should log information about the **configuration** which might impact the execution.
This includes the version of the code itself, possibly by referencing a commit ID.
Also log information about the configuration of the instance.
This includes information about environment variables, and version numbers of dependencies like the Java runtime or the system kernel.
Also log when your microservice is shut down.

To help debugging your microservice, you should add **tracing** messages.
For certain key methods, for example those processing a REST request or initiating an outgoing request or database query, log both entry and exit.
These log messages should include context information, which could mean to include the method arguments, return value, or the constructed SQL query in the message.
For each incoming/outgoing request or possibly lenghty computation log the time needed for its execution.

In addition add messages for **error cases**.
When throwing an exception, also log information explaining the cause and the meaning of the exceptional situation.
Likewise, when catching and processing an exception, log what is being done because of it. Avoid repeating yourself when logging stack traces, for example it is not helpful to log exceptions which are re-thrown immediately without being processed.

Depending on the error, decide on an appropriate severity and **log level** (TRACE, DEBUG, INFO, WARN, and ERROR are common levels).
Establish guidelines to use log levels consistently in all microservices.
Make sure that certain log levels (e.g., FATAL and ERROR) denote events that must be acted upon (and corresponding log messages automatically trigger alerts), while the other log levels only provide information.

#### Business
Besides logging purely operational data, it is also a good idea to log aspects related to the business itself.
For example, you could log how often certain features are used, or log whenever a customer completes a purchase.
In case of a service level agreement (SLA) associated information might also be helpful, for example logging response times or the number successfully completed requests.

#### Security
In addition to general operational log messages, you should log events supporting a forensical analysis after an attack or security breach.

Examples:
- user login/logout (including IP address, user agent, ...)
- password changes
- password reset requests
- failed login attempts
- denied access to services

Furthermore, if your application has privileged users who may execute restricted actions, it is helpful to log all interactions of such users with more detail.

#### Product Standards and Regulatory Compliance
If your service needs to fulfill certain compliance rules or regulations, you need to take care to log the corresponding information.
Take care that your regulations might also *disallow* certain information from being logged.

Logging and tracing requirements are covered in [ITSAM-17 Logging and Tracing](https://wiki.wdf.sap.corp/wiki/display/operationssupport/ITSAM-17) standard.

- [SEC-106: SAP software shall protect sensitive data when stored persistently at the server side](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-106)
- [SEC-97: SAP software shall protect sensitive data when stored intermediately in transit](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-97)
- [SEC-236: SAP software shall not disclose information to unauthorized receivers](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-236)

#### Translation of Logs?

* **Standard log messages should be written in English only** since this is the development language (for source code at SAP) and logs need to be readable by developers and ops. 
* There may be **specialized logs* where translation is required because the customer will actually look at the log. Examples are e.g. 'audit log' for customization changes done by the customer admins, ... 


## What should *not* be logged?
In general confidential information should not be logged.
This naturally includes user passwords, access tokens, credit card information, and private keys.
Authentication information for downstream services, for example database credentials, should also not be logged.

Furthermore, you should not log actual content and personal data.
This includes messages typed in by a user, names, birthdates, social security number, ...
Instead of logging actual data, it might be helpful to use a corresponding ID instead.

Also take care to respect the rules set up by any regulations you have to follow.

As information like passwords may appear as part of REST URIs, method arguments, or inside exception stack traces, you need to be careful during implementation.

Read also 
- [P&I Technology / Cloud Engineering: What are we allowed to track?](https://wiki.wdf.sap.corp/wiki/display/technology/Telemetry#Telemetry-LegalQuestions%3AWhatareweallowedtotrack%3F)
- [Security Product Standard Glossary: Sensitive Data](https://wiki.wdf.sap.corp/wiki/display/PSSEC/Glossary#Glossary-SensitiveData).

## Metrics
Metrics are used to visualize the health status of the whole application based on certain key measurements, aggregated over all requests and not only individual ones. 
There are tools that help you to aggregate the usage information in a convenient way so that you don't need to compute that information based on your logs.

As an example, you may already log how long an individual request takes.
This information helps when you need to analyze a specific request.
However, you cannot detect if the response times increase over time, possibly approaching a timeout or conflicting with a service level agreement.
To see if your microservice is healthy, you need to combine and compare the response times of all (recent) requests.
By aggregating and visualizing these pieces of information and computing the average/mean/95th percentile/... you can easily monitor the state of your microservice.

Frequently log usage information like CPU, memory, swap, network bandwidth, ...
You should also include aggregated information about the number of served requests, error counts, response times, executed SQL queries, ...

## How should logging be done?

**Logging Libraries and How To Setup**:
The [SLF4J API](http://www.slf4j.org) provides a simple interface that can be used to access logger objects.
Both [Logback](http://logback.qos.ch/) and [Log4j2](http://logging.apache.org/log4j/) can be used as implementations. The [Log4j2 documentation](https://logging.apache.org/log4j/log4j-2.3/manual/index.html) points out that "Log4j 2 is designed to be usable as an audit logging framework. Both Log4j 1.x and Logback will lose events while reconfiguring".

As you need to configure both your application (responsible to format the messages) and the ELK stack instance (responsible for parsing the messages), you should investigate existing solutions.
Based on the work done by the [PerfX team](https://jam4.sapjam.com/groups/about_page/pleCfjogSvhtRhOssiLyWl) a logging library integrating these features is made available [here](https://github.com/SAP/cf-java-logging-support).
This library outputs a JSON format that is understood by the ELK stack, and also provides information about served requests by offering a servlet filter that can be bound to the application.

In the `bulletinboard-ads` project we included the `LoggerInjector` class which makes it possible to inject a logger instance by just declaring a field `@Inject Logger logger`.
This logger instance automatically has the name set to the class it is injected into.
As Spring does not support injection into static fields, when writing logs in static methods you need to instantiate a logger instance using `Logger logger = LoggerFactory.getLogger(YourClass.class)`.

To avoid copy and paste errors, you should use `getClass()` instead of `YourClass.class` whenever possible.
For already existing code, or logger instantiation in a static context, you can make use of the ["detect logger name mismatch" feature of SLF4J](http://www.slf4j.org/codes.html#loggerNameMismatch).
 
**Performance Hints**:
For performance reasons you should avoid string concatenation, especially for debug/trace messages.
As an example, `logger.trace("logging in " + user")` is slower than `logger.trace("logging in {}", user)`.
If computing the data is expensive, it can help to wrap this computation in a `isXXXEnabled` statement:

```
if (logger.isTraceEnabled()) {
   Object expensive = doSomethingExpensive();
   logger.trace("something: {}", expensive);
}
```
[Source](http://www.slf4j.org/faq.html#logging_performance)

**Categories**:
Categories can be added by using SLF4J markers. Example:

```
Marker sqlMarker = MarkerFactory.getMarker("SQL");
logger.info(sqlMarker, "starting query: {}", query);
```
[Source](http://www.slf4j.org/api/org/slf4j/Marker.html)

Then, as shown in [Exercise 13](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/solution-13-Use-SLF4J-Features/src/main/resources/logback.xml), such markers can be used to filter the log output.

**Custom Fields**:
Using custom fields you can add additional information in a structured way.
As an example, this information then can be used for further processing in Kibana.

To add custom fields to a log message, use the `CustomField.customField()` method provided by the logging library.

As an example, `logger.trace("test", customField("key", "value"))` produces a log message containing `{ [...], "msg":"test","custom_fields":{"key":"value"} }`.

**Correlation ID**:
Information spanning more than a single message, for example the correlation ID, can be added to the **thread context**.
Such information then is part of each following log message, although it is only specified once.

Note: If you create new threads while handling a single request (for example if you use Hystrix), take care to propagate the context information to new threads.

The logging library automatically adds the correlation ID to the log context.
To initialize a new thread using an already existing correlation ID, use `LogContext.initializeContext(correlationId)`.
You can retrieve the current correlation ID using `LogContext.getCorrelationId()`.
When communicating with downstream microservices, make sure to supply this correlation ID, for example as part of the HTTP header (in the field `LogContext.HTTP_HEADER_CORRELATION_ID`).

You can add custom information to the logging context using the [MDC class](http://logback.qos.ch/manual/mdc.html).

Note that in the long run the correlation ID might be taken from the [DSR Passport](http://help.sap.com/saphelp_erp60_sp/helpdata/en/1e/12fe54b23cdf45b01137bc72593fab/frameset.htm). This is not implemented yet.

**Tracing**:
Aspect-oriented programming can be used to insert tracing statements in multiple locations easily.
See [Aspect-Oriented Programming for tracing](AOP.md)

**TODOs**:
- How to make existing framework logs readable? For example JPA/EclipseLink (see [Issue 24](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/issues/24))
- AOP approaches
- how to log metric information

## Common Scenarios
You can go through the following list of potential error situations to evaluate whether your log gives you the information needed to analyze the root cause.
- A customer tells you "I saw some error message two weeks ago"
 - Can you identify the corresponding request?
 - Can you find the problem even if it happened in a downstream service?
 - Do you have the data necessary to understand/reproduce the error?
 - Do you know which code ran at that time, even though you updated your code on a daily basis?
- A database server is down
 - Does the stacktrace contain passwords?
 - Did your system automatically send out an alert?
 - Can you reconstruct which customers experienced errors because of this?
- A recent update made everything slower
 - Can you see a difference in response times?
 - Is the regression detected automatically?
 - Can you identify the microservice causing the delays?
- One DEA (out of many) is slower due to hardware problems
 - Can you identify the microservice instances (on that DEA) which have higher response times?
 - Is this detected automatically?
- Special characters in the input cause errors in the persistence layer
 - Can you see requests leading to such errors?
 - Can you see which data is part of these requests?
- A feature stops working on specific mobile devices
 - Do you see a decline in feature usage?
 - Can you identify which clients stop using the feature?
 - Can you identify the commit/deploy that caused this regression?
 - Is this detected automatically?
- Your design team needs to know which of two alternative UI designs lead to more purchases
 - For each log line, can you identify the UI design in use of the corresponding instance?
 - Is business critical information (here: purchases) logged?
- As part of an ongoing lawsuit your logs are investigated
 - Do your log messages only include information that you are allowed to log (passwords, user data)?
 - Do you remove according to a retention policy?
 - Do you log information that you must log due to regulations?
 - Can you ensure that no critical log message is lost?

## Other Logging Services in SCP
**Application Log** is provided by SCP out of box for all applications to consume. These logs are useful for developers and operations only.
Access to these logs is provided only to those users who have access to the space in which the application is deployed and running in.
But for Enterprise grade business applications, there are various other requirements for legal compliance as well as regular operational purposes.

An application for example needs to troubleshoot authorization issues, to identify failed login attempts, to monitor log running batch process/background activities etc.

Except for the Business logs all of the below mentioned logs are supported by the `Audit Log Service`. Audit Log service offers separate library for Java based application and NodeJs based applications. The library has different methods for these different type of logs. 

As the `Audit Log Service` service is provided as part of `Application Run Time` it does not need to be added as a separate item during the Floor Price Calculation in the process of Commercialization. 

As the logs are only for special users, and not meant for regular business purposes, these logs do not have a dynamic nature, rather a fixed format. As consumers of the service, we just need to provide values required for the log entry.

For details on how to configure and use the **Audit log service** as part of your application look up this comprehensive wiki page: https://github.wdf.sap.corp/xs-audit-log/sap-cp-audit-log-service-docs/wiki. 

### Audit Log
- Audit Log service is the most commonly required service for any business applications. There are various product standard requirements which applications can comply with by consuming the Audit Log Service. 
- For instance, whenever there is a master data change, there needs to be a log written capturing the change and that log should be kept valid for a long period of time.
- There may be other legal requirements as well to capture certain events happenning in the system. Ex. Tenant Onboarding, Tenant Offboarding etc.
- Typically audit logs are seen only by special users 'Auditors' and not meant to be seen by regular business users.
- For details on the product standard associated with Audit see [here](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-257)

### Read Access Log
- Read Access Log is not offered as a separate service, but as part of Audit Log Service itself.
- This is a specialized version of Audit Log capturing only access to sensitive information event.
- For instance to log access to health record which is very sensitive, access to sensitive personal information like religious beliefs, political ideology etc.
- This is part of EU-GDPR Requirements as well.
- Access to these logs, again is to be given only to special users and not to regular business application users.
- This is again a Product Standard requirement from SAP, for details see [here](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-254)

### Change Log
- Change Log is not offered as a separate service, but as part of Audit Log Service itself.
- This is a specialized version of Audit Log capturing only Change of Data.
- For instance to log change of Contract Status, change of Personal Data.
- This is part of EU-GDPR Requirements as well. 
- Access to these logs, again is to be given only to special users and not to regular business application users.
- This is again a Product Standard requirement from SAP, for details see [here](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-215)
  
### Security Log
- Security Log is not offered as a separate service, but as part of Audit Log Service itself.
- This is a specialized version of Audit Log capturing only Security Related events.
- For instance to log failed Login attempts, Password Change events, Authorization Check failure events etc.
- Access to these logs, again is to be given only to special users and not to regular business application users.
- This is again a Product Standard requirement from SAP, for details see [here](https://wiki.wdf.sap.corp/wiki/display/PSSEC/SEC-215)
 
### Business Logs
- Business Log is offered as a separate service in SCP CF for applications to consume.
- These logs are not part of Security Requirements, but may be part of Operation and Support Guidelines. 
- These logs are meant for Business Application Users to monitor their Business Processes, and take Business Actions accordingly.
- For instance to monitor Workflow actions, check progress of a long running background activity etc.
- As these messages are meant for Business Application Users, Business Logs offers Multi-lingual support to ensure that logs are shown in the language which the user requires/desires.
- The logs are meant for regular Business Application Users predominantly, and can be used for special users as well.
- Business Logging Service is a Multitenant-Business Service, it offers both PaaS tenant and SaaS tenant level log separation and can be used to log Personal/Sensitive Personal Information as well.
- The `Business Logging Service` needs to be added as a separate entry and involves cost as well.
- For details on Business Logging Service check the [Business Logging Jam Group](https://jam4.sapjam.com/groups/d5rFGe6JlU5MM9zOJLlhiB/overview_page/ncmsQCfeIyozHxe9nWIrmh) and [SAP Help Documentation](https://help.sap.com/viewer/0f34ef9e650e4e1e9d31a72b6f8eb913/LATEST/en-US)
 

## FAQ

#### Q: How important is logging for a fast error analysis in a distributed system?
In the Global Design Frontrunner Apps project "Smart Campus" (SAP CP Neo IoT service extension, for details see [here](https://jam4.sapjam.com/blogs/show/Pm96AwVH65s1vH3VfIAmjz)) logging proved to be essential:
Components and services do break for various reasons, so identifying the root cause as fast as possible either by analyzing the error logs manually or ideally by having automatic health monitoring in place 
is key to quickly getting the system up and running again. 
A database service may break due to insufficient database configuration (HANA row-oriented vs. column-oriented organization, insufficient memory, 
database licences expiration, etc.), an external service may break due to upgrades (incompatible changes during an upgrade).
The services your app depends on are often evolving and managed by other teams.

If calling such a service suddenly fails, an error should be logged, containing the error code and the exception message that are provided by either the service itself or by the framework/component calling the service.
Including the stack trace of the exception into the error log can be helpful to understand the execution order of the code when the error occured. 
For apps running many threads and therefore logging many threads it is important to be able to understand the order of events during an error. 
Always take into account older error log entries during your analysis: The root cause for an error may have been logged earlier, whereas errors being logged later may report consequential errors.

#### Q: What is the relation between exception handling and error logging?  
Error logging proved helpful in our "Smart campus" system (see previous question) only if it contained detailed information about what went wrong. 
Therefore the Java code must be organized in a way that exception handling covers possible failures of the system, its frameworks and resources. 
The code should differentiate between different possible failures by mentioning the exact root cause in the exception message. 
The exception message should either be logged right where the error happens or must passed up the calling chain and logged later. 
It is essential that this information does not get lost during the exception handling process.

If your Java code exposes a service, the aspect of passing on the information about what went wrong is even more important: 
In addition to logging an error in your service the cause of an error must be passed on to the caller  (for example by using error codes).
This allows the calling application to decide whether it reacts to the error and if it logs the error in its domain. 
The caller may not be aware of the dependencies within your service and must therefore be given the chance to learn about the root cause of a failure.

#### Q: What if devices neither support debugging nor tracing?
In the Global Design Frontrunner Apps project "projectQ" (Samsung and Apple smart watches connected to a  SAP CP Neo backend, see [here](https://experiencesmartwatch.mo.sap.corp/)) 
we found that when an end user reports an issue, a quick access to debugging the wearable application or to traces is not possible.
Especially if the issue is reported remotely and the device cannot be connected to the local development environment.
For the cloud foundry platform there is also no guarantee that all connected IoT or wearable devices support or allow (remote) access to their trace files. 
A mitigation for this situation where backend traces can be accessed whereas client traces cannot may be to report information about an error on the client to the backend and trace it there. 
Keep in mind the security and legal aspects mentioned on this page and (only) send data to the backend that helps to reproduce the user steps in a test system set-up (test device connected to test backend).
For example, the version of the client application code is necessary to identify the release version used by the end user.  
An identifier like device id or user id (if available) helps to map the backend trace entries to a user/device. 
If an exception occurs in the client code, the exception message plus, for example, information in which screen/step/action the error occurred is useful to reproduce the issue.

## Further Reading
- [Debugging on CF possible?](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/issues/54)
- [XS2 Java - Logging and Tracing](https://wiki.wdf.sap.corp/wiki/display/xs2java/Logging+and+Tracing)
- [Logging at SAP Help Portal](http://help.sap.com/saphelp_erp60_sp/helpdata/en/b7/54e63f48e58f15e10000000a155106/content.htm?frameset=/en/b7/54e63f48e58f15e10000000a155106/frameset.htm&current_toc=/en/49/e98876e9865b4e977b54fc090df4ed/plain.htm&node_id=568&show_children=false)
- http://pixlcloud.com/applicationlogging.pdf
- https://journal.paul.querna.org/articles/2011/12/26/log-for-machines-in-json/

