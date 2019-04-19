# Redis
If we need to attach temporary data to a session, we need to take into account that incoming requests may, and very likely will, be routed to different application instances. Instead of storing the data in application memory or using standard persistence, we use Redis as an in-memory data structure and store session information using it. In case a new request needs to be handled, the necessary data can be retrieved quickly from the Redis service bound to the application.

## Implementation
In the [redis branch](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/demo-redis) of the
proof of concept project we demonstrate how Redis can be used.

We use the [spring-session-data-redis](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/redis/pom.xml) dependency, which can be configured to automatically store session data in Redis:

```
<!-- Redis -->
<dependency>
  <groupId>org.springframework.session</groupId>
  <artifactId>spring-session-data-redis</artifactId>
  <version>1.2.0.RELEASE</version>
</dependency>
```

The [RedisConfig](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/redis/src/main/java/com/sap/bulletinboard/ads/config/RedisConfig.java)
file takes care of this configuration.
The `RedisConnectionFactory` is used internally to connect to the Redis backing service bound to the application.
Using the `@EnableRedisHttpSession` annotation a filter bean is provided, which uses Redis to manage sessions and persist session data:

```
@Configuration
@EnableRedisHttpSession
// use @EnableRedisHttpSession(maxInactiveIntervalInSeconds = 60) to expire the data after 60 seconds, default 30 minutes
public class RedisConfig extends AbstractCloudConfig {
  @Bean
  public RedisConnectionFactory redisFactory() {
    return connectionFactory().redisConnectionFactory();
  }
}
```

In [AppInitializer](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/redis/src/main/java/com/sap/bulletinboard/ads/AppInitializer.java) we use this filter bean and attach it to the servlet context:

```
// register spring session filter
servletContext.addFilter("springSessionRepositoryFilter", new DelegatingFilterProxy("springSessionRepositoryFilter"))
                .addMappingForUrlPatterns(null, false, "/*");
```

When a new request is served, a new session is created or a previously created session is made available.

In [RedisController](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/blob/redis/src/main/java/com/sap/bulletinboard/ads/controllers/RedisController.java)
we have spring inject the `HttpServletRequest` bean to read the session information using `request.getSession()`.
As the session is configured to use Redis as backing store, we can simply use `session.get()` and `session.put()` to (temporarily) persist session information.

## Demonstration

You can test this functionality by deploying the application and accessing the `RedisController` at `/redis/`.
Every session will store a number, which will be incremented for each incoming request.
By running multiple browsers or using the privacy mode you can start two separate sessions, and observe two different counters.

When deployed in the cloud, you can start multiple instances and see that the counter is synchronized between all instances.

**Note**: For local tests, adapt the `VCAP_SERVICES` accordingly.

## Content
Generally, arbitrary data can be stored using Redis, with a limit of 512 MByte per String and 2 GByte of data stored per key.
However, you should only store interaction-based data in Redis.
Incomplete business data, for example the shopping cart, should be persisted permanently (using a database).

## Serialization
While object (de)serialization is possible, it is advisable to store primitive values. For further information have a look at this [Spring documentation](http://docs.spring.io/spring-data/data-redis/docs/current/reference/html/#redis:serializer).

## Multiple Microservices
In addition to using Redis for several instances of the same microservice, you may also synchronize data between different applications. If the data is stored based on a session (as described above), you need to take care to use disjoint keys for the data. As an example, you can prefix each key with the application name to avoid conflicts. One way to use the same session spanning several microservices is to combine those microservices using a common [Application Router](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Security/Exercise_22_DeployApplicationRouter.md).
