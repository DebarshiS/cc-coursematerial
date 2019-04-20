Exercise 1: Getting Started - Setup Tomcat Web Server 
====================================================

## Learning Goal
Get familiar with the provided code base and understand how to test your microservice in your local environment. In this exercise you will start the microservice on your locally installed Tomcat web server while making use of Spring Dependency Injection.

**[Changes](#changes-since-video-recording) since video recording**.

## Prerequisite - Import project into Eclipse (`master` branch)

- Run `VirtualBox` and start your Virtual Machine (VM).
- Run Eclipse inside the VM **Important: If you are asked for a workspace, make sure to use the default workspace at `/home/vagrant/workspace`**
- Import the `master` branch of this [Git Project](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc/tree/master) as described below:

#### Case 1: Initial Import
If you did not import the `cc-bulletinboard-ads` project previously, follow these steps:
- Select `File - Import - Git - Projects from Git`. 
- In the next dialog, select `Clone URI`. In the next dialog, enter the URI `git@github.wdf.sap.corp:cc-java/cc-bulletinboard-ads-spring-webmvc.git`.
- **Important**: Choose **`master`** as `Initial branch`
    - Use the `Next` and `Finish` buttons to go through the following dialogs (the default settings should be OK).
- **Then update the Maven Settings: `ALT+F5`, `OK`**

#### Case 2: Switch back to `master` branch of previously imported project
If you already imported the above project earlier and tried out things before this course, you need to switch back to the `master` branch.
- Right-Click on your project and click on `Team - Fetch from Upstream`, then `OK`
- Right-Click on your project and click on `Team - Switch To - Other...`.
 - In `Remote Tracking` find and select the entry starting with `origin/master`.
 - Click `Checkout`, then `Checkout as New Local Branch`
 - Click `Finish`
 - Click `Stash...` and close the dialog with `OK`
- **Don't forget to Update the Maven Settings: `ALT+F5`, `OK`**

## Step 1: Get to know the Code
Take some time to familiarize yourself with the given `bulletinboard-ads` microservice. Concentrate on the `src/main/java` source folder and there in particular the following classes are now of interest: `AppInitializer`, the `WebAppContextConfig` and `DefaultController`.

## Step 2: Run the Microservice in Eclipse

In order to run/debug the microservice within your Eclipse IDE you need to deploy the application on your Tomcat server instance. 

- Right-click the Tomcat server entry in the Servers View and select `Add and Remove ...` and click `Add` to move your project to the configured ones. 
- Then `(re)start` the Tomcat server
(see [Eclipse documentation](http://help.eclipse.org/luna/index.jsp?topic=%2Forg.eclipse.stardust.docs.wst%2Fhtml%2Fwst-integration%2Fconfiguration.html) for your reference).
- Ensure that in the console information similar to the one below is logged:
~~~
Okt 18, 2016 6:42:32 PM org.springframework.web.context.ContextLoader initWebApplicationContext
INFO: Root WebApplicationContext: initialization started
...
Okt 18, 2016 6:42:32 PM org.springframework.web.context.support.AnnotationConfigWebApplicationContext loadBeanDefinitions
INFO: Registering annotated classes: [class com.sap.bulletinboard.ads.config.WebAppContextConfig]
...
Okt 18, 2016 6:42:34 PM org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping register
INFO: Mapped "{[/],methods=[GET]}" onto public java.lang.String com.sap.bulletinboard.ads.controllers.DefaultController.get()
...
Okt 18, 2016 6:42:36 PM org.apache.catalina.core.ApplicationContext log
INFO: Initializing Spring FrameworkServlet 'DispatcherServlet'
...
Okt 18, 2016 6:42:36 PM org.apache.coyote.AbstractProtocol start
INFO: Starting ProtocolHandler ["http-nio-8080"]
Okt 18, 2016 6:42:36 PM org.apache.coyote.AbstractProtocol start
INFO: Starting ProtocolHandler ["ajp-nio-8009"]
Okt 18, 2016 6:42:36 PM org.apache.catalina.startup.Catalina start
INFO: Server startup in 6912 ms
~~~
- Start the `Web Browser` and ensure that the following url `http://localhost:8080/` returns `OK`
- You can terminate the web server in the Eclipse `Console` view (red square button), or stop the Tomcat server explicitly in the `Servers` view.

## [Optional] Step 3: Run the Microservice on the Command Line 
Ensure that you are in the project root e.g. ~/git/cc-bulletinboard-ads-spring-webmvc.

Linux:
```
# prerequisite: navigate to the root directory of the project
$ source localEnvironmentSetup.sh
$ mvn tomcat7:run
```

Windows:
```
# prerequisite: navigate to the root directory of the project
$ localEnvironmentSetup.bat
$ mvn tomcat7:run
```

With the tomcat maven plugin the maven build (including the tests) is triggered and if successful the application is run on an embedded tomcat.
- Ensure that the following url `http://localhost:8080/` shows `OK`  
  - Note: If you got an exception ` Failed to initialize end point associated with ProtocolHandler ...` then you most likely forgot to stop your server in Eclipse. There can always just be one tomcat running on a host:port (e.g. localhost:8080) address.
  - Note: If you need to use another port, you can change the default tomcat port in the `pom.xml` at the setting `maven.tomcat.port`.
- You can terminate the web server in the command window with `CTRL+C`.

## Step 4: Gain application insight with the Actuator
The main thing that the Spring Boot Actuator does is to add several helpful management endpoints to a Spring Web MVC-based application. Some of the endpoints are:

Method      |  Endpoint   | Description
----------- | ----------- | -------------------------
 GET        | health      | Shows application health information (when the application is secure, a simple ‘status’ when accessed over an unauthenticated connection or full message details when authenticated).
 GET        | beans       | Displays a complete list of all the Spring beans in your application. 
 GET        | mappings    | Displays a collated list of all @RequestMapping paths.
 GET        | env         | Lists all environment and system property variables available to the application context
 GET        | env/{name}  | Displays the value for a specific environment or property variable
 GET        | metrics     | Lists metrics concerning the application 

Note that the actuator plugin is designed for Spring Boot applications, and therefore not all endpoints are accessible. Find a more detailed description [here](https://docs.spring.io/spring-boot/docs/current/reference/html/production-ready-endpoints.html).

The next steps explains how to enable the actuator.

#### Add Maven dependency
Add the `spring-boot-actuator` dependency to your `pom.xml` using the XML view of Eclipse:
```
<!-- Actuator for adding management endpoints -->
<dependency>
	<groupId> org.springframework.boot</groupId>
	<artifactId>spring-boot-actuator</artifactId>
	<version>1.2.5.RELEASE</version>
	<exclusions>
		<exclusion>
			<groupId>org.springframework</groupId>
			<artifactId>spring-core</artifactId>
		</exclusion>
		<exclusion>
			<groupId>org.springframework</groupId>
			<artifactId>spring-context</artifactId>
		</exclusion>
	</exclusions>
</dependency>
```
> Note: In this exercise we intentionally **do NOT make use of the latest version of actuator** for simplicity reasons. Please be aware of the possible security implications of using this productively as documented [here](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/CreateMicroservice/Exercise_1_GettingStarted.md#remarks-on-using-the-actuator-productive-code).  

> Note: After you've changed the Maven settings, don't forget to update your Eclipse project (`ALT-F5`)! 

#### Enable Auto-configuration 
To enable the Spring-boot actuator plugin you need to pretend to be a SpringBoot application by enabling [Auto-configuration](http://docs.spring.io/spring-boot/docs/current/reference/html/using-boot-auto-configuration.html).

Create a `SpringBootActuatorConfig` class in the `com.sap.bulletinboard.ads.config` package and provide the following annotations:
```Java
@Configuration
@EnableConfigurationProperties
@EnableAutoConfiguration(exclude = { DataSourceAutoConfiguration.class, RabbitAutoConfiguration.class })
public class SpringBootActuatorConfig {
}
```
With that Spring beans gets automatically configured depending on the `@ConfigurationProperties` annotated beans and what is found on the classpath.

#### Test
Start the `Web Browser` and ensure that the following url `http://localhost:8080/health` shows the status `"UP"`. Note: The response type (media type) of this HTTP GET request is `JSON`. 
In order to analyze JSON responses best you can install a Chrome extension like [`JSON  Viewer`](https://chrome.google.com/webstore/detail/json-viewer/gbmdgpbipfallnflgajpaliibnhdgobh?utm_source=chrome-app-launcher-info-dialog).

#### Remarks on using the Actuator in productive code
In the older versions of the Actuator (as used here), the endpoints are by default enabled for unauthenticated and unauthorized access.
As described [here](https://wiki.wdf.sap.corp/wiki/x/3qnRc) this is not, what you want **(later) in your productive code**. Instead:
- Use a version of `spring-boot-actuator` >= 1.5.4.RELEASE (and not 1.2.5.RELEASE as in this exercise).
- Test your productive application that all the Spring Boot Actuator endpoints behave as expected (enabled / disabled or secured in the way you expect them to be).

## Used Frameworks and Tools
- [Tomcat Web Server](http://tomcat.apache.org/)
- [Spring - DI Framework](https://github.com/spring-projects/spring-framework)

## Further Reading
- [Assembly and Initialization](../Knowledge/AssemblyAndInitialization.md)
- [Eclipse Git Plugin (Egit) tutorial](http://eclipsesource.com/blogs/tutorials/egit-tutorial/)

## Changes since video recording
 - In the video the application was made available at `http://localhost:8080/bulletinboard-ads/`. We removed the `bulletinboard-ads` path.
 - JAX-RS (Java API for RESTful services) is replaced by [Spring Web MVC framework](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/mvc.html).
 - Spring Boot actuator plugin is introduced to get some management endpoints like `/mapping`.
 - Spring Component Scan is activated in the `WebAppContextConfig` class to auto-detect classes, that are annotated with `@Component`, `@Configuration`,...  Therefore, the bean classes need no longer be registered explicitly.

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
<a href="Exercise_2_HelloWorldResource.md">
  <img align="right" alt="Next Exercise">
</a>
