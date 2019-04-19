# Actuator

The actuator offers several useful REST endpoints that help you to monitor and manage your application. Note that those are only available with a Spring Web MVC-based application.

Some of the endpoints are:

Method      |  Endpoint   | Description
----------- | ----------- | -------------------------
 GET        | **actuator**  | Provides a **“discovery page” for the other endpoints**. Requires Spring HATEOAS to be on the classpath.
 GET        | health      | Shows application health information (when the application is secure, a simple ‘status’ when accessed over an unauthenticated connection or full message details when authenticated).
 GET        | beans       | Displays a complete list of all the Spring beans in your application. 
 GET        | mappings    | Displays a collated list of all @RequestMapping paths.
 GET        | env         | Lists all environment and system property variables available to the application context
 GET        | env/{name}  | Displays the value for a specific environment or property variable
 GET        | metrics     | Lists metrics concerning the application 

Find a more detailed description [here](https://github.com/spring-projects/spring-boot/blob/master/spring-boot-docs/src/main/asciidoc/production-ready-features.adoc).

## Getting started

#### Add Maven dependency
Add the following dependencies to your `pom.xml` using the XML view of Eclipse:
```
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-hateoas</artifactId>
</dependency>
```

#### Example
Github project: https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-boot 

## Details
#### `/env` endpoint
For developers, the `/env` endpoint is very helpful, as this endpoint gives information about the environment variables and configuration details.
As an example, the `VCAP_SERVICES` variable is shown (when running in the cloud), and also details of the bound backing services are provided in a more readable format.

#### `/mappings` endpoint
Using `/mappings` one can easily find out which components registered which Spring MVC endpoints, and also see which details (e.g. headers, arguments) are part of the corresponding mapping.
As an example, the following information is given for the endpoint providing information about a single advertisement:

```json
{"{[/api/v1/ads/{id}],methods=[GET]}":
  {
    "bean":"requestMappingHandlerMapping",
    "method":"public com.sap.bulletinboard.ads.models.Advertisement com.sap.bulletinboard.ads.controllers.AdvertisementController.advertisementById(long)"
  }
}
```

#### `/health` endpoint
At `/health` you can see information about the health status of the application. As most Spring components automatically add information to this page, you can get a very helpful overview about the system status without having to tweak the code at all.
Additionally it is possible to add more information to be shown by this endpoint. There are a bunch of load balancing solutions that monitors the `/health` endpoint periodically.

## Further Reading
- [spring.io: Spring Boot Actuator](http://docs.spring.io/spring-boot/docs/current/reference/html/production-ready.html)
