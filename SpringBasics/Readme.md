# Spring Basics

## Spring Dependency Injection Framework
In our course we are using Spring as Dependency Injection Framework to achieve loose coupling which is especially worth when writing "Unit" tests.

### Overview Picture and Explanation
![](/Z_ReuseImages/images/SpringDependencyInjection.png)
- With `@Inject` or `@Autowired` the code can depend on abstractions instead of concrete implementations (Dependency Inversion Principle). Most prominent use case: you want to replace a class in context of the tests.
- The implementation(s) to be injected need to be registered to the so called Spring `ApplicationContext`. Those classes are then managed by Spring and are called `Beans`.
- There are various options on how to register the concrete implementation (Bean). In case of Java-based configuration you register a `Bean`
    - in a `@Bean` annotated method within a `@Configuration` annotated class
    - in a `@Component` annotated class
- Let's assume you have registered several implementations of the same API then you need to qualify the name of the Bean (this should be used extremely rarely). Examples using the `@Qualifier("namedBean")` annotation can be found [here](http://docs.spring.io/autorepo/docs/spring-framework/3.0.0.M3/reference/html/ch04s11.html).
- During runtime the Spring framework creates the instances, either as singletons (default) or as multiple instances (depending on the Spring Bean Scopes). Note: You can only inject dependencies to a class, that is itself managed by Spring and part of the `ApplicationContext`.

### Spring Bean Scopes
Bean definitions serves as recipes for the IoC container, but the Spring IoC container needs to know if and when a fresh instance should be created. The scopes that were used in the course are:

| Scope               | Description          |
|---------------------|----------------------|
| Singleton | (Default) One single (shared) bean instance per Spring IoC container. Use for stateless beans only. |
| Prototype | Fresh Bean instance is created every time it is referenced in a 'construction context' (e.g. class used as injected parameter) by collaborating beans. Use for all stateful beans. |
| Request  | Fresh Bean instance is created for every HTTP request. It is one of the scopes that are *only* available in a web-aware Spring `ApplicationContext`. |


Note: You cannot dependency-inject a prototype-scoped bean into your singleton bean, because that injection occurs only once, when the Spring container is instantiating the singleton bean and resolving and injecting its dependencies. If you need a new instance of a prototype bean at runtime more than once, consider [“Method injection”](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/beans.html#beans-factory-method-injection).

Example:
```java
@RequestScope
@Component
public class LoginAction {
    // ...
}
```
Read more about `Spring Bean Scopes` [here](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/beans.html#beans-factory-scopes).

### Field vs. Constructor Injection

Field Injection:
```
@Component
public class SomeClass {
    @Inject
    private Foo foo;
}
```

Constructor Injection:
```
@Component
public class SomeClass {
    private final Foo foo;
    
    @Inject
    public SomeClass(Foo foo) {
        this.foo = foo;
    }
}
```
Note that, starting with Spring Boot 1.4, the `@Inject`/`@Autowired` annotation on a constructor may be omitted, if it is the only constructor.

Despite the slightly more verbose setup, [constructor injection should be preferred over field injection](https://programmers.stackexchange.com/questions/300706/dependency-injection-field-injection-vs-constructor-injection):
- The main reason is that, for example in unit tests without a Spring context, it is impossible to create instances with missing dependencies, as all dependencies must be provided explicitly as constructor arguments.
With field injection, it could be possible to invoke the (default) constructor and forget/ignore to set the required fields.
- Furthermore, circular dependencies are detected when the application context is constructed.

Side remark: Let's assume you need to call explicitly a `main` method of a Bean (class managed by Spring) then you could use `context.getBean(SomeClass.class)` if the application context is available. If you need to instantiate the context see also [here](https://stackoverflow.com/questions/4914012/how-to-inject-applicationcontext-itself).

### Difference between the annotation @Inject and @Autowired?
`@Autowired` and `@Inject` can be used interchangeable to inject Spring beans. `@Autowired` is Spring's own annotation , `@Inject` is part of Java's standard for dependency injection  (javax.inject) and needs must be imported (see `pom.xml`). Both annotations behave identically. 

### XML vs. Java Configuration
In our example projects we prefer configuration using Java classes. That's why there is no `*.xml` file defining the classes, that should be managed by Spring. Settings which could be given as part of `*.xml` files are provided using Java annotations. 

As the `maven-war-plugin` fails when there is no `WEB-INF/web.xml` we've set `failOnMissingWebXml` to `false` in our `pom.xml` to overrule the default. 

Basically this is a matter of preference. In the setting of the course, annotations help by making the effects a bit more explicit. Instead of having to read both the Java source and the corresponding XML configuration, one only needs to understand the annotations which are part of the code.

An advantage of Java Configuration and Spring Annotations is that you get some compile time checking of your configuration and some refactoring support that you don't get with Spring XML configuration.

Annotations and tricks like component scan can help reduce the configuration effort because they are picked up automatically, Spring Boot makes use of it.

### Component Scan
Like in a Spring Boot Application we also activate the scan of Spring Bean definitions in all packages by making use of the `@ComponentScan` annotation. As base package we specifiy the root package, so that all sub-packages are covered as well.
With that Spring automatically scans the classpath to find classes annotated with (for example) `@Component` or `@Configuration`.

Classes annotated with `@Component` are automatically registered as beans.
For classes annotated with `@Configuration` the methods inside annotated with `@Bean` are also regarded as bean registrations.
Note that there are other relevant annotations, e.g. `@Service` or `@Controller`, which internally have the `@Component` annotation and, thus, are also regarded in this process.

### Profiles
The annotation `@Profile("xyz")` can be used to express that a `@Component`/`@Configuration` anonotated class should only be regarded by Spring if the profile "xyz" is "active".

In our setting, the profile "cloud" is always set (by the Cloud Foundry java buildpack) when running on Cloud Foundry, and we also ensure that "cloud" is active for local development and execution.

In tests, the "cloud" profile is not set, as consequence those classes are not managed by Spring and, in the case of a database, Spring automatically configures an in-memory database if provided on the classpath.

### Spring Context Example
You can check the [example](https://github.wdf.sap.corp/d052062/spring.example) out and play around with it, e.g. debug the JUnit tests to get a deeper understanding about how to setup a Spring `ApplicationContext`, how to handle ambiguity with `Profiles` and `Qualifiers`.


## Further Reading
- [SpringTutorial: Spring Application Context](https://github.wdf.sap.corp/d022051/SpringTutorial/wiki/SpringContext)
- [Introduction to the Spring Framework](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/overview.html)
- [Spring.io](https://spring.io/)
- [ASE Wiki: Dependency Injection](https://wiki.wdf.sap.corp/wiki/display/ASE/Test+Isolation+-+Dependency+Injection)
