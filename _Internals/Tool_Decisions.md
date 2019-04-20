Tool Decisions
==============

The Cloud Foundry platform, specifically the Java buildpack, allows pretty much everything that is possible in Java, i.e. there are many choices on frameworks, tools etc. This means that in general every project can use whatever they like - and that they have the open source approval for. 

In general we (the developers of this course) do not try to make tool / framework decisions but align with CF @SAP CP as a platform and the major projects about what is used there. Our goal is to show what is mainstream and concensus, not to define it. 

SAP CP supports for the OnPremise shipment Node.js, XSJS, Tomcat and TomEE. CF @SAP CP will support the same buildpacks plus everything that the Cloud Foundry platform and the SAP-team behind it support. Have a look at the supported buildpacks (run `cf buildpacks`) that are available on your Cloud Foundry instance.

On this page we describe the main tool / framework choices and the rationale behind. 

### Spring Boot (Spring Web MVC) vs. Spring JAX-RS

There is a set of evolving technologies which belong to the context of a core programming model like Spring / Spring Boot or frameworks coming from successful cloud service providers like Pivotal and Netflix.   

**Spring Boot** makes it easy to create stand-alone applications based on the Spring framework. Today Spring Boot is much more mature, it offers a valuable amount and a conclusively set of Spring Boot starter packages, that makes absolutely sense in context of Microservice application development. 

Apart from that **Spring Cloud** builds on top of Spring Boot, which empowers developers to rapidly build complex applications by leveraging common patterns in distributed systems. 

**From the historical point of view we decided in the past for Spring and JAX-RS for providing REST APIs. In the current version we make use of the Spring libraries, like `Spring Web MVC` for building RESTful APIs, that are promoted in context of Spring Boot. From a didactical point of view we decided to introduce Spring Boot framework and its specifics at the very end of the course.** Having understood the basics / underlying concepts and libraries you are not only ready to bootstrap your application with Spring Boot but also able to understand the magic behind. Read more about the ["Way towards Spring Boot"](https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBoot/Readme.md).

#### Rationales behind Spring Boot
- Has huge open source community: a lot of tutorials / code examples, simplifies troubleshooting, keeping yourself up-to-date.
- One recommended cloud programming model: more and more SAP development teams decides for Spring Boot.
- It's the basis for Spring Cloud components for implementing distributed design patterns in the cloud. 


### Why Spring at all?

We use the [Spring Framework](https://github.com/spring-projects/spring-framework) with several of its modules.
Using Spring we get Dependency Injection (Inversion of Control), automatic configuration of several services running on Cloud Foundry using [Spring Cloud](http://projects.spring.io/spring-cloud/), simple database access using [Spring Data JPA](http://projects.spring.io/spring-data-jpa/), Messaging functionality using [Spring AMQP](http://projects.spring.io/spring-amqp/), security/authorization utilities using [Spring Security](http://projects.spring.io/spring-security/), etc.

The individual modules can easily be used in combination, and integrate with Spring's injection/test/configuration functionalities. Furthermore, Spring currently is mainstream.

Read more about `Spring Basics`[here](https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBasics/Readme.md).

### Jetty vs. TomEE vs. Tomcat

*Jetty* is a lightweight Java Web Server that allows to start the webserver as part of the application as an integrated/embedded server. This is especially useful for testing the application locally in a production-like environment.

When using *TomEE* several (Apache) projects are provided as part of the server, for example Apache CXF to serve REST requests. As such, one needs to use the versions part of the TomEE package.
The javax.ws.rs (REST) API included in TomEE 1.7.2 does not contain a client, nor convenient `readEntity(Class)` or `StatusInfo` functionality which is part of recent Apache CXF (or Jersey) versions (see https://issues.apache.org/jira/browse/TOMEE-1307). A [TomEE Version 7.0 will be released soon](https://tomee.apache.org/tomee-7.0.0-M1.html), which will contain the missing features.

The suggestion is to start with *Tomcat*, as provided with the current [SAP Java-Buildpack](https://wiki.wdf.sap.corp/wiki/display/xs2java/SAP+Java+Buildack+for+Cloud+Foundry).

### EclipseLink vs. Hibernate
EclipseLink is the SAP-internal preferred framework when using JPA. Hibernate requires a HANA dialect specification which must be implemented and maintained by SAP HANA Core, which is actually not the case. EclipseLink is the reference JPA implementation for SAP HANA.

Depending on how often implementation specifics are used (for example HQL instead of JPQL, or Hibernate API instead of JPA), migrating can be a tough challenge. A quick internet search reveals many tutorials helping with migrations from Hibernate to EclipseLink.

### AspectJ vs. Spring AOP

Both Spring AOP and AspectJ can be used in a Spring project, and both offer similar functionality.
The main advantage of Spring AOP is that it can be used without much effort, as it integrates with Spring and aspects are applied automatically for Spring Beans. However, AspectJ allows more features than Spring AOP, and Spring AOP only works with classes managed by Spring (beans).

Using AspectJ more flexible Pointcut definitions can be used, giving additional flexibility.
When using AspectJ the class files have to be compiled using the AspectJ compiler, or weaving has to be configured.

A more detailled discussion can be found [on Stackoverflow](http://stackoverflow.com/questions/1606559/spring-aop-vs-aspectj).

### Spring MVC Test Framework
It is important to be able to perform some integration tests against the REST API of your web application. 

The `org.springframework.mock.web` package contains a comprehensive set of Servlet API mock objects, which are useful for testing web application contexts, controllers, and filters. These mock objects are targeted at usage with Spring’s Web MVC framework and provides an effective way for testing controllers by performing requests and generating responses through the actual `DispatcherServlet`. The tests run server-side only without the need of an (embedded) web server, which reduces the startup time and gives you the option to inject mocked services into the Spring `TestContext` (loads and caches the `WebApplicationContext`).

Read more about the `Spring MVC Test Framework` [here](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/integration-testing.html#spring-mvc-test-framework).

As a consequence we decided against end-to-end integration tests as part of the Microservice. Note: Spring Boot provides an option to write full, end-to-end integration tests that include a running server...

### Logback vs. Log4j2
Both [Logback](http://logback.qos.ch/) and [Log4j2](http://logging.apache.org/log4j/) can be used as SLF4J implementations. The Log4j2 documentation points out that "Log4j 2 is designed to be usable as an audit logging framework. Both Log4j 1.x and Logback will lose events while reconfiguring". This might be an argument for preferring Log4j 2. 

### Message Queue
Currently we use [RabbitMQ](https://www.rabbitmq.com/), as this is the only queue available in CF@<span></span>SAP CP. In the course we only use basic features to introduce the idea of MQ systems, so we might change the implementation if necessary. Instead of directly using core RabbitMQ funcionality, we try to use [AMQP](https://www.amqp.org/) (Advanced Message Queuing Protocol) as much as possible. AMQP is intended as a general API for MQ systems like RabbitMQ. However, to receive messages (subscribe to a queue), we currently need to use RabbitMQ classes directly. [Details](../Service2ServiceCommunication/MessageQueue.md)

### Session Storage
In order to use sessions even if multiple applications or application instances are used, we intend to persist session data using [Redis](http://redis.io/). Similar to Message Queues (RabbitMQ), this is the only available alternative. Furthermore, this work is still ongoing.

### Hystrix
We use [Netflix Hystrix](https://github.com/Netflix/Hystrix) to mitigate failures (or slow responses) of downstream microservices, making the microservice resilient. Hystrix offers simple approaches that can be extended where necessary, offering many configuration options and fallback mechanisms. Currently we do not know about a similar alternative.

## Related Links
- [Overview Tools used](Tools.md)
- [RAML - Swagger - OData](Discussions/RAMLSwaggerOData.md) 
