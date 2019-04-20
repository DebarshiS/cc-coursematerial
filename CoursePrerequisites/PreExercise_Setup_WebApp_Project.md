Exercise: Setup a Web Application Project 
===========================================
## Learning Goal
Get familiar with the provided web application project setup and understand how to build, deploy and test your web application in your local environment. 

## The task of this exercise...
... is to find out whether the `DefaultController` instance is instantiated per HTTP request or only once.

## Prerequisite - Import project into Eclipse
- Run `VirtualBox` or `VMware` and start your Virtual Machine (VM).
- Start Eclipse IDE **Important: If you are asked for a workspace, make sure to use the default workspace at `/home/vagrant/workspace`**.
- Import `initial` branch of [Git Project](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc):
    - Select `File - Import - Git - Projects from Git`. 
    - In the next dialog, select `Clone URI`. In the next dialog, enter the URI `git@github.wdf.sap.corp:cc-java/cc-bulletinboard-ads-spring-webmvc.git`. Note: do not change any user/password or http/ssh settings.
    - **Important**: Choose **`initial`** as `Initial branch`
    - Use the `Next` and `Finish` buttons to go through the following dialogs (the default settings should be OK).
- Update the Maven Settings of the project: Press `ALT+F5`, then `OK`

Now the code of this project is located under `~/git/cc-bulletinboard-ads-spring-webmvc`.

## Step 1: Get to know the Code
The main entry point for our web application is not a `main` method but the `onStartup` method within the `AppInitializer` class. 
This class gets automatically instantiated, as it implements the `WebApplicationInitializer` interface.  
It initializes the *Servlet Context* of the Spring web application with
- the `DispatcherServlet` and the URL it is responsible for
- the *Spring Application Context*, in which the `WebAppContextConfig` class is registered as main configuration class.

Have also a look at the `WebAppContextConfig` class. It has some important annotations, such as:
- `@Configuration` means it is a **source of Beans (classes, managed by Spring)**. And as `@Configuration` is meta-annotated with `@Component`, it is also a candidate for component scanning. 
- `@ComponentScan(basePackages = "com.sap.bulletinboard.ads")` activates the **search for Bean definitions**, that are defined in `@Component` (or `@Configuration`) annotated classes. The scan is configured for the "com.sap.bulletinboard.ads" root package, which includes the scan of all subpackages.
- `@EnableWebMvc` imports the Spring MVC configuration, that is required to **add other Spring Web MVC related Beans** like the `HandlerMapping` to the *Spring Application Context*.

We use Spring Web MVC to provide REST interfaces in our application.
In addition we are going to use several Spring components for Dependency Injection (Inversion of Control), cloud configuration, simple database access, etc.

## Step 2: Trigger a Maven Build in Eclipse
Before we deploy our web application to Tomcat Web Server we need to package our application as a deployable artifact, which in our case is a web archive (WAR zip file). The packaging strategy is also defined in the `pom.xml`: `<packaging>war</packaging>`.

#### Compile and package application using Maven
- Right-click on the project's root and select `Run as - Maven build ...` 
- In the popup enter `package` as goal and run it.
- This will open the `Console` view and display the run results.

**Note:** You can also compile and package your application on the Command Line using `mvn package` (in the project root dir).

#### Examine the created build artifact
In the `Project Explorer` view refresh the `target` folder and you will see a `bulletinboard-ads.war` file.You can  take a look into the war file by double-click on windows or `unzip <war-file>` on linux. All class files from the `target/bulletinboard-ads/WEB-INF/classes` directory are included.

## Step 3: Run the Web Application on the Command Line 

#### Specify Maven Plugin
As prerequisite you need to setup and configure the Tomcat Maven Plugin. For this open the `pom.xml` using the XML view of Eclipse.
Then add `tomcat7-maven-plugin` within the `<build><plugins>` section:
```xml
<plugin>
  <groupId>org.apache.tomcat.maven</groupId>
  <artifactId>tomcat7-maven-plugin</artifactId>
  <version>2.2</version>
  <configuration>
      <port>8080</port>
      <path>/</path>
      <systemProperties>
          <http.proxyHost>proxy</http.proxyHost>
          <http.proxyPort>8080</http.proxyPort>
      </systemProperties>
  </configuration>
</plugin>
```

In this configuration Tomcat provides the application at `http://localhost:8080/` and pre-configures the environment so that the SAP proxy is used.

Note: After you've changed the Maven settings, don't forget to update your Eclipse project! To do so right click on your Eclipse project and select `Maven` - `Update Project ...` (or hit alt-F5 within the active project).

#### Run on Command Line
Ensure that you are in the **project root** e.g. ~/git/cc-bulletinboard-ads-spring-webmvc.

```
$ mvn tomcat7:run
```

With the tomcat maven plugin the maven build is triggered and if successful the application is deployed and run on an embedded tomcat.
- Start the `Web Browser` and ensure that the following url `http://localhost:8080/` returns `OK`
- You can terminate the web server in the command window with `CTRL+C`.



## Step 4: Wrap-Up: Understand how the Application is Deployed and Initialized
Now you should be able to understand the following picture:
![](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Z_ReuseImages/images/Tomcat_DeployAndInitApp.png)
Find further information [here](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Knowledge/AssemblyAndInitialization.md).

## Step 5: Debug the Web Application in Eclipse
You can also build and deploy your application within your Eclipse IDE, which might be more convenient and which allows you to start the web application in debug mode. 

**Your Task:** Find out whether the `DefaultController` instance is created per request or only once.

In Eclipse open the `Servers` view and ensure that there is a Tomcat v8.0 web server defined. 
- Right-click the Tomcat server entry in the `Servers` view and select `Add and Remove ...` and click `Add` to move your project to the configured ones.
- Set a breakpoint in the  `get` method of the `DefaultController` class
- Then `Debug` or `Restart in Debug` the Tomcat server
(also have a look at the [Eclipse documentation](http://help.eclipse.org/luna/index.jsp?topic=%2Forg.eclipse.stardust.docs.wst%2Fhtml%2Fwst-integration%2Fconfiguration.html) for your reference).
- Ensure that in the console information similar to the one below is logged:

~~~
INFO: 1 Spring WebApplicationInitializers detected on classpath
Nov 18, 2016 12:07:24 PM org.apache.catalina.core.ApplicationContext log
...
INFO: Initializing Spring root WebApplicationContext
Nov 18, 2016 12:07:24 PM org.springframework.web.context.support.AnnotationConfigWebApplicationContext loadBeanDefinitions
INFO: Registering annotated classes: [class com.sap.bulletinboard.ads.config.WebAppContextConfig]
Nov 18, 2016 12:07:25 PM org.springframework.beans.factory.annotation.AutowiredAnnotationBeanPostProcessor <init>
INFO: JSR-330 'javax.inject.Inject' annotation found and supported for autowiring
Nov 18, 2016 12:07:26 PM org.springframework.web.servlet.mvc.method.annotation.RequestMappingHandlerMapping register
INFO: Mapped "{[/],methods=[GET]}" onto public java.lang.String com.sap.bulletinboard.ads.controllers.DefaultController.get()
Nov 18, 2016 12:07:27 PM org.springframework.web.context.ContextLoader initWebApplicationContext
INFO: Root WebApplicationContext: initialization completed
...
INFO: Initializing Spring FrameworkServlet 'DispatcherServlet'
Nov 18, 2016 12:07:27 PM org.springframework.web.servlet.DispatcherServlet initServletBean
...
Nov 18, 2016 12:07:27 PM org.apache.coyote.AbstractProtocol start
INFO: Starting ProtocolHandler ["http-nio-8080"]
Nov 18, 2016 12:07:27 PM org.apache.coyote.AbstractProtocol start
INFO: Starting ProtocolHandler ["ajp-nio-8009"]
Nov 18, 2016 12:07:27 PM org.apache.catalina.startup.Catalina start
INFO: Server startup in 3653 ms
~~~

- When (re-)entering the following url `http://localhost:8080/`. Eclipse will switch to the `Debug Perspective` and will hold at the breakpoint. 
  - Now you can e.g. look at the `this` pointer to see if you see multiple instances or always the same
- You can terminate the web server in the Eclipse `Console` view (red square button), or stop the Tomcat server explicitly in the `Servers` view.

## Step 6: Excursion: Understand Configuration of Tomcat and Application Path (URL Mapping)
Assume the incoming request is: `http://localhost:8080/`.

1. The Tomcat web server is configured to run locally on port `8080` and the registered context path is `/`
Note: the context path is explicitly defined in pom.xml (tomcat7-maven-plugin) or within Eclipse in the Tomcat server properties - as default the application name from the pom.xml is taken.
1. Inside Tomcat we register a `DispatcherServlet` servlet directly at the root context path. And the `DefaultController` defines in that context a REST endpoint.
1. When a request matches the given path, an instance of `DefaultController` is provided. Methods in the controller are annotated with HTTP Verbs (`@GetMapping`, etc.) and optionally with a `@RequestMapping(path = "/")`. The path is called **end-point**.
1. The end-point that matches the request is then called, in this case `GET`.

## Used Frameworks and Tools
- [Tomcat Web Server](http://tomcat.apache.org/)
- [Spring - DI Framework](https://github.com/spring-projects/spring-framework)

## Further Reading
- [Assembly and Initialization](../Knowledge/AssemblyAndInitialization.md)
- [Eclipse Git Plugin (Egit) tutorial](http://eclipsesource.com/blogs/tutorials/egit-tutorial/)
