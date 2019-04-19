# Performance

For general resources and courses on performance of applications see the [Performance and Scalability JAM](https://jam4.sapjam.com/groups/tRkQO9JI6Bhq4XdU7cu9TZ/overview_page/QnIu7Bwo4dokPqvRPozTgf).

## Startup Performance

Startup performance is a critical aspect of your application when you need to be able to scale out horizontally to handle increased workload. Indeed, it sits straight in the middle of the critical path. With `cf scale` you can trigger the deployment of more nodes to serve incoming requests, but the additional capacity will actually be there later when those nodes have begun operating.

There are many things that may affect negatively startup time. Input-output (e.g., read configuration files, consume external services) should also be avoided as much as possible during startup. (Besides, [12-factor-apps should have their configuration passed in the environment](http://12factor.net/config).) Additionally, many libraries also slow down start-up time due to bytecode manipulation and extensive intialization.

**Random number** generation can also bring the start-up of an application to a standstill. 
When a Java web application is deployed to Cloud Foundry, the Java build pack configures an instance of Apache Tomcat where the Java web application will be deployed. Recent versions of Tomcat (7 and 8) rely on Java's SecureRandom class to provide random values for things like session ids. Depending on the JVM and environment, the startup of Tomcat can be delayed if SecureRandom does not have access to sufficient entropy. This will in turn cause your application to start slow and, if it's slow enough, fail with the error instance failed to start accepting connections. Depending on the environment, the blocking `/dev/random` is used by default. Configuring the application to use the non-blocking `/dev/urandom` instead can reduce the startup time dramatically.

```
env:
  JAVA_OPTS: -Djava.security.egd=file:///dev/./urandom
```

- http://www.2uo.de/myths-about-urandom/
- https://docs.oracle.com/cd/E13209_01/wlcp/wlss30/configwlss/jvmrand.html
- http://stackoverflow.com/questions/20315022/java-slow-entropy-related-issue

## Memory

Providing more/enough memory to the application might give better performance.
We noticed dramatic differences when comparing 512 MByte to 768 MByte even for simple applications.

## Scaling horizontally or vertically? 

In general it is said for the cloud that one should scale horizontally. This means that if you have more requests to handle, just start more instances. But of course things are not so easy. 

### Possible performance issues with microservices

There are a lot of things to get right when you want to write high performance Java services. The main areas are:
- **Memory**: Providing more/enough memory to an application usually gives better performance. We noticed dramatic differences when comparing 512 MByte to 768 MByte even for simple applications. It is worth observice garbage collection rates and memory consumption.
- **Synchronous usage of other apps / services**: When service A calls B synchronously, the response time of B is obviously added to the response time of A - plus the overhead of the call itself. 
- **Persistence**: Loading /saving data - including the communication and round-trips to the database - is usually a big part of the response time. Consequently, inefficient DB access is a killer for performance and scalability. For in-depth material on how to do persistence right with JPA, see the e-learning [Efficient Persistence with JPA](https://github.wdf.sap.corp/cloud-native-dev/java-persistence/wiki).
- **Concurrency Issues**: Concurrency issues of all kinds, synchronization problems and not optimally adjusted thread pools / connection pools etc. will also have a dramatic performance impact. See [Java Concurrency](https://github.wdf.sap.corp/cloud-native-dev/java-concurrency/wiki) for an in-depthe treatment. 
- **Design problems of all kinds**: Putting different types of requests (short / long, small/large queries, queries vs. worker) into the same service will also lead to sub-optimal performance and availability SLAs. See the video [Split that monolith](https://www.youtube.com/watch?v=SDPonggiu28), ) for more details.


### When does vertical scaling make sense?

Vertical scaling means usually 'more memory' or 'more / faster CPUs' instead of scaling small apps horizontally. Consider this input from Ulf Fildebrandt (resilience expert) about aspects that matter in this question:

-	**Costs:** The cost calculation is also an important aspect that is too often considered too late. In every IaaS there are different prices for the compute units. If you take a look at the [SAP Cloud Platform - Internal Pricelist for Neo and Cloud Foundry Services](https://wiki.wdf.sap.corp/wiki/x/hPbyc), you see that x-small VM (1 CPU, 2 GB) costs 23,63 €, but medium (4 CPU, 8 GB) costs 37,44  only 13,81 € more for 4x the compute power (status May 2018). This is just an example that costs are also an important factor for this calculation. Usually, the bigger the compute unit is, the smaller the relative price is. 
  - **Consequence:** It could make sense to scale vertically, if the service wants to utilize the resources very cost efficient (but a counter argument would also be that the scaling granularity is much higher with bigger compute units, if you have to scale out reaching the very end of a big compute unit).
- **Basic load of a runtime** that is required to execute a task: Usually the requests are executed on runtimes that are already running, e.g. a Tomcat server for requests to a servlet. If the requests go to a runtime that is taking a lot of memory, then smaller compute units are not optimal, e.g. if the basic runtime is taking 700 MB (like in CPI: container OS (Ubuntu) + JVM + Apache Camel runtime), then it could be difficult, if you decide that the runtimes should not be bigger than 1 GB, because this only leaves 300 MB for the messages.
  - **Consequence:** It could make sense to scale vertically, if the fixed memory consumption for the basic runtime is very high, because if a bigger compute unit is used, then the basic runtime only consumes the memory once.
- **Crash-prevention/isolation:** Running multiple tasks together on one runtime can create a problem, because the crash of one task execution can crash all others in the same process (side-effect of shared resources). This is usually the argument to scale-out, because doing more distribution would mean that the tasks are really executed independently.  
