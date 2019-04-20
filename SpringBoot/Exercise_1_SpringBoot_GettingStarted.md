# Exercise 1: Spring Boot Jump Start
Learn how simple it is to create a plain Spring Boot application with some management endpoints. Furthermore you will learn how to run and test your microservice locally.

## Step 1: Bootstrapping a Spring Application with Spring Initializr
The [Spring Initializr](http://start.spring.io/) generates a new Spring project based on a selection of features you want to have in the app.
The same functionality is also available as a wizard within the Spring Tool Suite or IntelliJ IDEA (Ultimate Edition).

<img src="https://github.com/ccjavadev/cc-coursematerial/blob/master/SpringBoot/images/SpringInitializer.jpg" height="400" />

- Make use of the [Spring Initializr](http://start.spring.io/) to define your Spring Boot application. Add the following dependencies: `Web`, `Cache`, `Actuator` and `HATEOAS`.
- Click `Generate Project` to download the Spring Boot Project and extract it to Home `/workspace` (default settings are ok).
- Now open `Eclipse` and import the Spring Boot Project as an existing Maven project.

## Step 2: Get to know the Code
Have a look at the project structure in the `Project Explorer` view. It looks as follows:
```
src/main/java
      | com.sap.earlytalent
          |WeatherApplication.java
src/main/resources
      | application.properties
src/test/java
      | com.sap.earlytalent
          | WeatherApplicationTests.java
pom.xml
```

TODO: further explanation....

## Step 3: Run Microservice in Eclipse
In order to run/debug the microservice within your Eclipse IDE you need to deploy the application on your Tomcat server instance. 

- In the `Project Explorer` right-click the `WeatherApplication.java` and select `Run As` -> `Java Application`. 
- Ensure that in the console shows information similar as shown below:
~~~
 .   ____          _            __ _ _
 /\\ / ___'_ __ _ _(_)_ __  __ _ \ \ \ \
( ( )\___ | '_ | '_| | '_ \/ _` | \ \ \ \
 \\/  ___)| |_)| | | | | || (_| |  ) ) ) )
  '  |____| .__|_| |_|_| |_\__, | / / / /
 =========|_|==============|___/=/_/_/_/
 :: Spring Boot ::        (v1.4.2.RELEASE)
...
2016-11-22 13:20:13.104  INFO 7028 --- [           main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat initialized with port(s): 8080 (http)
2016-11-22 13:20:13.360  INFO 7028 --- [ost-startStop-1] o.a.c.c.C.[Tomcat].[localhost].[/]       : Initializing Spring embedded WebApplicationContext
2016-11-22 13:20:13.361  INFO 7028 --- [ost-startStop-1] o.s.web.context.ContextLoader            : Root WebApplicationContext: initialization completed in 2989 ms
...
2016-11-22 13:20:15.101  INFO 7028 --- [           main] o.s.b.a.e.mvc.EndpointHandlerMapping     : Mapped "{[/health || /health.json],produces=[application/json]}" onto public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.HealthMvcEndpoint.invoke(java.security.Principal)
2016-11-22 13:20:15.102  INFO 7028 --- [           main] o.s.b.a.e.mvc.EndpointHandlerMapping     : Mapped "{[/info || /info.json],methods=[GET],produces=[application/json]}" onto public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()
2016-11-22 13:20:15.103  INFO 7028 --- [           main] o.s.b.a.e.mvc.EndpointHandlerMapping     : Mapped "{[/beans || /beans.json],methods=[GET],produces=[application/json]}" onto public java.lang.Object org.springframework.boot.actuate.endpoint.mvc.EndpointMvcAdapter.invoke()
20
2016-11-22 13:20:15.723  INFO 7028 --- [           main] s.b.c.e.t.TomcatEmbeddedServletContainer : Tomcat started on port(s): 8080 (http)
2016-11-22 13:20:15.734  INFO 7028 --- [           main] com.sap.earlytalent.WeatherApplication   : Started WeatherApplication in 6.475 seconds (JVM running for 6.956)
~~~
- Start the `Web Browser` and ensure that the following url `http://localhost:8080/health` shows the status `"UP"`. Note: The response type (media type) of this HTTP GET request is `JSON`.
- You can terminate the Tomcat web server in the Eclipse `Console` view (red square button).

## [Optional] Step 4: Test using `Postman` REST client
In order to analyze JSON responses best you either need to install a Chrome extension like [`JSON  Viewer`](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh?utm_source=chrome-app-launcher-info-dialog) or you can test the REST Service `http://localhost:8080/health` in the browser using the `Postman` Chrome extension.

Note: [Postman](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop) is a Rest client that is also required to create and test custom HTTP requests.

## [Optional] Step 5: Run Microservice on the Command Line 
Ensure that you are in the project root e.g. ~/workspace/weather.

Linux:
```
mvn clean verify
java -jar target/weatherapp-0.0.1-SNAPSHOT.jar
```

or alternatively:
```
mvn spring-boot:run
```
- Ensure again that the following url `http://localhost:8080/health` shows the status `"UP"`. 
- You can terminate the web server in the command window with `CTRL+C`.
- Note: If you get an ERROR message `Failed to start end point associated with ProtocolHandler [http-nio-8080]...` then you most likely forgot to stop your server in Eclipse. There can always just be one tomcat running on a host:port (e.g. localhost:8080) address.

## Step 6: Gain application insight with the Actuator
Beside of the `health` endpoint Spring Boot Actuator adds several helpful management endpoints to a Spring Web MVC-based application, like:

Method      |  Endpoint   | Description
----------- | ----------- | -------------------------
GET         | **actuator**  | Provides a **“discovery page” for the other endpoints**. Requires Spring HATEOAS to be on the classpath.
 GET        | health      | Shows application health information (when the application is secure, a simple ‘status’ when accessed over an unauthenticated connection or full message details when authenticated).
 GET        | beans       | Displays a complete list of all the Spring beans in your application. 
 GET        | mappings    | Displays a collated list of all @RequestMapping paths.
 GET        | env         | Lists all environment and system property variables available to the application context
 GET        | metrics     | Lists metrics concerning the application 

Find a more detailed description [here](docs/Actuator.md).

## Step 7: Run JUnit Tests in Eclipse
To run/debug the JUnit tests within your Eclipse IDE:

- Right-click on the project's root and select `Run As` - `JUnit Test` or `Debug As` - `JUnit Test`.
This will open the JUnit view and display the test results.
- Have a look at the `Console` view. You can see similar output like when you run the Java Application with the exception that there is no deployment to a Web Server like Tomcat.  
 
***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="">
  <img align="left" alt="Previous Exercise">
</a>
<a href="Exercise_2_SpringBoot_DeployAdsOnCloudFoundry.md">
  <img align="right" alt="Next Exercise">
</a>







