# Assembly and Initialization

When a program has a `main` method it is usually straightforward to understand the flow of control and how the application is initialized. When we however use a lot of frameworks, a lot of things become indirect. You register classes, callbacks, endpoints etc. and they get called in some order at later times. In addition we usually want different configuration and/or classes (mocks) to be used for productive and testing cases. 

This page describes briefly how the Advertisement app is assembled and how the url, the path gets finally mapped to the implementation of an REST endpoint. It points to some places in the code that are important to understand. We describe the app in its final state, i.e. after the last excercise. Therefore, some parts may not exist at the beginning of the course. 


# Productive Case
Our app is a Java Web App which produces a WAR file (see ./target/*.war). The WAR file is a ZIP file with a specific structure. It will be deployed on a servlet container (Tomcat) and then 'started'. For our purposes the most important aspect is that there is a an implementation of the interface `WebApplicationInitializer`, which gets detected on the classpath and which `onStartup` method is initially executed to configure and start the web app after deploy.


## Web Application Initialization
A "Web application" is a collection of servlets running in a Servlet Container such as `Tomcat` Web Server. Without the `AppInitializer` implementation there would be no servlet at all...

The main purpose of the `AppInitializer.onStartup` is the configuration of the **ServletContext** with one **`DispatcherServlet`** and some **Servlet Filters**. This implies a proper setup of the **Spring ApplicationContext**. Some details on the implementation:
* **Spring ApplicationContext Setup**: it registers explicitly one initial configuration class `WebAppContextConfig` into the Spring ApplicationContext, which then
  * enables the `ComponentScan` for all packages to find and register automatically all the other classes, that should be managed by Spring (`Beans`) and that should be injectable by `@Inject`. Read more about Spring [here](/SpringBasics/Readme.md).
  * enables the registration of Spring Web MVC specific components. Read more about Spring Web MVC [here](/CreateMicroservice/Readme.md).
* In Spring Web MVC the `DispatcherServlet` is the single entry point of a Web application, it registers itself for the URL pattern "/*" that means that the servlet container forwards all requests for any URL pattern to this single `DispatcherServlet`.
* `ServletFilters` such as "RequestLoggingFilter" or "springSecurityFilterChain" are Spring Web MVC independent and need to be registered explicitly.

![](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Z_ReuseImages/images/Tomcat_DeployAndInitApp.png)

# Flow of an incoming REST Request in general
Assume the incoming request is: `http://localhost:8080/api/v1/ads/3`.

![Spring Web MVC Components](/CreateMicroservice/images/SpringWebMVCComponents.png)

1. The web server runs locally on port 8080. The registered context path is `/` as in the cloud the content usually is made available directly at the root path (in our example, the path then would be `https://some-hostname/api/v1/ads/3`).
1. Inside Tomcat we register a `DispatcherServlet` directly at the root context path.
1. The HandlerMapping component of Spring Web MVC knows that the method `advertisementById` as part of the `AdvertisementController` class defines a REST endpoint that is registered at the path `/api/v1/ads/{id}`. The path is called **end-point**.  
  - Methods in the controller are annotated with HTTP Verbs (`@GetMapping`, `@PostMapping` etc.) where you can enhance the `@RequestMapping` path, which is defined on class-level. The path expression can also specify path variables that can be handed over to the Java method as parameters.
1. When a request matches the given path, a new instance of `AdvertisementController` gets created by Spring, assumed the Bean is request-scoped (`@RequestScope`). 
  - Note: per default the scope of a controller class is 'singleton'. This means that the threads of all active requests would run through the same instance. Be aware of thread issues when you want to use instance variables or state that is kept between requests. You can add the annotation `@Scope(ConfigurableBeanFactory.SCOPE_PROTOTYPE)` or `@RequestScope` in order to get a fresh instance of the *Controller* class for each and every request.
1. The method that handles the end-point is then called, in this case `advertisementById` and the value of the path variable is passed as parameter `id`.
1. On the HTTP level, the method has to return a result body and status code (e.g. 200). We can simply return a Java object which will be automatically converted by Jackson `HttpMessageConverter` into JSON format. For other situations you can use the `ResponseEntity` object to have all flexibility.

Additionally there might be filters that are wrapped around each request. In our case, a logging filter is called for each incoming request. This filter measures how long the request takes and logs this information at the end of each request.
 

## Further References
- [Spring Basics](/SpringBasics/Readme.md)
- [Spring Web MVC explained](/CreateMicroservice/Readme.md)
