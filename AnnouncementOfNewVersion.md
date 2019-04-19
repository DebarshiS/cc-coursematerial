## New Version and the way towards Spring Boot
There is a set of evolving technologies which belong to the context of a core programming model like Spring / Spring Boot or frameworks coming from successful cloud service providers like Pivotal and Netflix.   

**Spring Boot** makes it easy to create stand-alone applications based on the Spring framework. Today Spring Boot is much more mature, it offers a valuable set of Spring Boot starter packages, that makes development a lot easier in context of Microservice application development. 

Apart from that, **Spring Cloud** builds on top of Spring Boot, which empowers developers to rapidly build complex applications by leveraging common patterns in distributed systems. 

**In the initial version we decided for Spring and JAX-RS for providing REST APIs. In the new version we make use of the Spring libraries, that are promoted in context of Spring Boot. From a didactical point of view, we decided to introduce Spring Boot framework and its specifics at the very end of the course. This gives you an understanding of what happens 'under the hood' before you use annotations that work like magic (until you have to debug :-).**

### Rationale behind Spring Boot
- Is the mainstream framework in the Java cloud world.
- Has huge open source community, a lot of tutorials / code examples, simplifies troubleshooting, introduces the latest new concepts.
- More and more SAP development teams decides for Spring Boot.
- It's the basis for Spring Cloud components for implementing distributed design patterns in the cloud. 

### Why not a Spring Boot version?
While using the same libraries like in context of our Spring Boot version, we introduce Spring Boot at the very end of the course. From a didactical point of view its worth to understand the basic / underlying concepts first:
- Learn which libaries are required to solve which problem => easy to find the right documentation.
- Learn how to manage dependencies in `pom.xml`.
- Learn how to define required Beans instead of let them be created and configured automatically.

Having understood the basics you are not only ready to bootstrap your application with Spring Boot but also able to understand the magic behind. Read more about the ["Way towards Spring Boot"](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/SpringBoot/Readme.md).

### What has changed?
We tried to change "as much as necessary - as little as possible"!
The table provides an high level overview about the main changes, that were introduced within the new course version.

| Tool, that helps ...              | Version 1                      | Version 2            | Read more |
| --------------------------------- | ------------------------------ | -------------------- | ---------- |
| setting up the Spring application context | ./. explicit registration         | Spring component scan, make use of active profiles | New "Spring Basics" chapter in [slides](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf)
| building RESTful web services             | Apache CXF (JAX-RS implementation)   | Spring Web MVC | Updates in "Create Microservice" [slides](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf)
| writing integration tests                 | Embedded Tomcat               | Spring Test MVC | "
| calling a RESTful service (REST Client)   | CXF Rest Client               | Apache Rest Template | Minor update in "Service2Service Communication" [slides](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf)

You can find the tools (link to OSS approvals) that are used in the new version [here](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/_Internals/Tools.md).

### When do we switch offically?
We will activate the new version on friday, **18th of November, 2016**.
With that the e-learning, the [wiki](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/wiki) will refer to the new version.

### How can I learn about the delta?
You can find a recording of the update info session on this share: \\\dwdf212\bst_ecf\X_Public\QE\CloudCurriculum\MicroserviceDevelopment\Infosession_NewVersion_11Nov2016


### What happens with the recordings / e-learning?
Right now, we can't afford to provide new recordings for the new version. Therefore, whatever has changed since the recording is described in the `Changes since video recording` at the beginning of the exercise descriptions. 


### Where can I find the new version?
The new material is available on the `master` branch. 

- [Course Material (`master branch`)](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/tree/master)
- [Exercises and Demos](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Readme.md)
- [Sample Solution](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc) 
- [Slides](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf)

### When the new version is active, what happens with the "old" JAX-RS version?
Note that the material will be still available at the following links but is not longer updated / maintained!

- [Course Material (`spring-jaxrs branch`)](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/tree/spring-jaxrs)
- [Exercises and Demos](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/spring-jaxrs/Readme.md)
- [Sample Solution](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-jaxrs) 
- [Slides](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial-spring-jaxrs/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf) 
