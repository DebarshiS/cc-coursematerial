# Frequently asked Questions in regard to Cloud Foundry 
## (always under construction)

### Sources of information
- [cf.users](mailto:cf.users@listserv.sap.corp) mailing list – from developers for developers, getting fast feedback
-	[Cloud Foundry Jam](https://jam4.sapjam.com/groups/ApFhQ0NCGAzAtXQWsdqB3B/overview_page/xgk0oDPal4vQRit4gAWq8P): more official and structured, containing FAQ, roadmaps, best practices, etc...
-	Central official FAQ (building up): [Q&A Central](https://qac.wdf.sap.corp/): containing FAQs in a structured way (that can be published also to partners)


### Q: High Availability on Cloud Foundry, how is it realized?
Cloud Foundry applications are [health-checked](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html). 
When the health-check for your application fails, they are re-started. Read more about that [here](https://docs.cloudfoundry.org/concepts/high-availability.html#cf-ha).  

Furthermore you can make use of the [SAP CP Availability Service](https://availability.cfapps.sap.hana.ondemand.com/), other Monitoring tools are mentioned [here](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/DevOps/Monitoring/Monitoring.pptx).


### Q: How does CF recognize that there are running processes?
Examples are background jobs, asynchronous processes, making use of WebSockets or long polling techniques (HTTP 2.0 keeps the connection open).

This information is relevant for blue-green deployment.

./.

###	Q: How to implement an User-Provided Service?
Cloud Foundry lets you bind an arbitrary service as [user-provided service](https://docs.cloudfoundry.org/devguide/services/user-provided.html). All you need to do is provide the parameters to the application, so it can contact the service (e.g. URL, port, credentials, etc). Those will be put into the ENV for the application in the [VCAP_SERVICES environment variable](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html), just in the same way as for other services.

./. Best Practices / how to implement an HA user service? Is a User Service scoped for a specific space only?
 
### Q: How to address single Application Instances? 

This is relevant when using [Ribbon](https://github.com/Netflix/ribbon), a client-side load-balancer, and [HystrixDashboard](https://github.com/Netflix/Hystrix/wiki/Dashboard), to monitor the configuration of Hystrix, a fault tolerance library.

The simple answer is: you can't (yet)! The CF router does load balancing for you, and you cannot talk directly to an application without going through the router. That means you cannot directly address a specific application instance by IP Address, until SAP CP CF makes use of the [networking release](https://github.com/cloudfoundry-incubator/cf-networking-release) and enable container networking on our cloudfoundry installations – which will come some time in the future. With this, you can access the internal IP and Port over ENV variables within your application. See the [example from the networking release](https://github.com/cloudfoundry-incubator/cf-networking-release/blob/develop/src/example-apps/cats-and-dogs/backend/main.go#L114) for an idea of what's possible then. 
However, for now, you need to use the route to your application when registering with e.g. [Eureka](https://github.com/Netflix/Eureka).

### Q: How to debug

See [Exercise 15: Debugging a Java CF app](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/LoggingTracing/Exercise_15_Debug_CF_Application.md).

### Q: Architecture concepts for Automatic Scaling
The [app autoscaler](https://github.com/cloudfoundry-incubator/app-autoscaler) is currently developed in cooperation with IBM.
./.

### Q: How to monitor / access a Backing Service? E.g. MessageQueue, Postgresql and HANA

The generic answer is: **SAP will deploy Dynatrace for all internal and cloud systems. Dynatrace offers very extensive monitoring of systems and services.** For details see: [SAP APM](https://github.wdf.sap.corp/pages/apm/)

### Q: How analyze DB content?

- To connect to a DB in order to analyze its content, you can use CF SSH as described in [this exercise](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/ConnectDatabase/Exercise_10_2_ConnectBackingService.md)
- See also the general CF documentation on [Accessing Services with SSH](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-services.html)

### Q: Standard Endpoints for health checks?
We recommend using Spring Boot Actuator for this purpose and selectively enable the endpoints you want. See the exercise in the course [here](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/solution-24-Make-App-Secure/src/main/java/com/sap/bulletinboard/ads/config/WebSecurityConfig.java).

**Attention: Make sure to secure your actuator endpoints as described [here](https://wiki.wdf.sap.corp/wiki/display/PSSEC/Spring+Boot+-+Trace+Issue).**


### Q: How can I send an email with my app?
- See SCP "mail and sms service" offering here: https://wiki.wdf.sap.corp/wiki/display/NGP/SAP+CP+Product+Day+for+2017T03
- JAM community for connectivity: https://jam4.sapjam.com/groups/2fk0AYCCXwEJbk9FLWCIV9/content?folder_id=gjYA1tN39AtKdKHBjBzWaq


### Q: What is the difference between java_buildpack and sap_java_buildpack?
The XS Java Runtime team supports only the SAP Java buildpack. However there could be SAP employees that contribute to the Community Java Buildpack, which is SAP product standard compliant.
Currently the SAP Java Buildpack on the Cloud Foundry landscapes is local so no dependencies are downloaded from the internet. 

The `sap_java_buildpack` contains the SAPJVM (the corporate SAP Java virtual machine) that includes many features such as on-the-fly debugging, profiling, extensive monitoring and tracing etc. Furthermore it contains a Hana DB driver. Further differences between the SAP Java Buildpack and the Community Java Buildpack are described [here](https://wiki.wdf.sap.corp/wiki/display/xs2java/SAP+Java+Buildack+for+Cloud+Foundry).

You need to make use of SAP java buildpack for implementing SAP cloud agnostic Java applications (XSA, Neo or plain CF).

###	Q: Architecture concepts for Backing Services, Service Fabrik
./. whitepaper?

### Q: How to scale databases, or change plans, without having to migrate data manually? 
./. whitepaper?

## Further References
- [Related Issue](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/issues/271)
- [Cloud Foundry - FAQ](https://qac.wdf.sap.corp/Default.aspx?ExpandTree=1&GroupID=4&TopicID=10246)
