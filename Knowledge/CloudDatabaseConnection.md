# Cloud Database Connection

In [Exercise 8 Part 1](../ConnectDatabase/Exercise_8_Part1_ConfigurePersistence.md) we introduce the plugins which we use to
connect to database instances running in the cloud. In order to closely mimic the production environment in the cloud, we use
the same code to connect to a local database during development.

## `VCAP_SERVICES`
The environment variable `VCAP_SERVICES` is used by Cloud Foundry to provide access information to all backing services, including database connection information to microservices.
With this information, and the following plugins making use of it, a database connection can be created and used.
Locally we configure this same environment variable so that a dedicated database can be used for local tests.

## `CloudDatabaseConfig`
We use the `CloudDatabaseConfig` file to configure access to a database. Starting with the information provided in the
environment variable `VCAP_SERVICES`, we end up with an instance of a CRUD repository.
For this the three plugins are used, which are explained in detail below.

<img src="https://github.com/ccjavadev/cc-coursematerial/blob/master/Z_ReuseImages/images/DBConnectionSetup.png" height="300" />

### Spring Cloud
In the first step, the Spring Cloud plugin is used. This code parses the information provided in the `VCAP_SERVICES`
environment variable, and provides a preconfigured [Data Source](http://docs.oracle.com/javase/8/docs/api/javax/sql/DataSource.html) instance. Each `DataSource` instance offers
a [Connection](http://docs.oracle.com/javase/8/docs/api/java/sql/Connection.html) to a database.

Just the following parts of `CloudDatabaseConfig` are used in this context.
The super-class `AbstractCloudConfig` is part of the Spring Cloud plugin and, using its `connectionFactory()` method, we can obtain a `DataSource` object instance.
This `DataSource` object instance is automatically registered as a bean, because we added the `@Bean` annotation to the defining method.

```java
public class CloudDatabaseConfig extends AbstractCloudConfig {
    /**
     * Parses VCAP_SERVICES from Cloud configuration and provides a DataSource.
     */
    @Bean
    public DataSource dataSource() {
        return connectionFactory().dataSource();
    }
}
```

### EclipseLink
EclipseLink is used as a JPA implementation.
JPA/EclipseLink is used to map from Java classes to database tables (and from Java data types to SQL data types).
SQL queries, result set handling, and object conversion are managed and optimized by JPA/EclipseLink.
Applications using EclipseLink are portable to supported SQL databases with little performance overhead.
An alternative to EclipseLink is Hibernate (also see [this discussion](/_Internals/Tool_Decisions.md#eclipselink-vs-hibernate)).

EclipseLink needs access to a database, which we provide using the `DataSource` instance of the previous step.
Using this database connection, the JPA object instances (`EntityManager` and `TransactionManager`) are provided.

This is done with the following code, where most functionality is part of `EntityManagerFactoryProvider`.
Again, the two defining methods are annotated with `@Bean` so that the corresponding beans are registered automatically.

```java
public class CloudDatabaseConfig {
    /**
     * Based on a DataSource, provides EntityManager (JPA)
     */
    @Bean(name = "entityManagerFactory")
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(DataSource dataSource) {
        return EntityManagerFactoryProvider.get(dataSource, Advertisement.class.getPackage().getName());
    }

    /**
     * Based on a EntityManager, provides TransactionManager (JPA)
     */
    @Bean(name = "transactionManager")
    public JpaTransactionManager transactionManager(EntityManagerFactory entityManagerFactory) {
        return new JpaTransactionManager(entityManagerFactory);
    }
}
```

#### `EntityManagerFactoryProvider`

In the [EntityManagerFactoryProvider](https://github.wdf.sap.corp/raw/cc-java/cc-bulletinboard-ads-spring-webmvc/solution-8-1-Configure-Persistence/src/main/java/com/sap/bulletinboard/ads/util/EntityManagerFactoryProvider.java) class, we initialize the JPA `EntityManagerFactoryBean` using the provided datasource.
In this process we make sure that our entity classes are known (by providing the packages to scan).
Furthermore, we set some JPA properties:
 * DDL_GENERATION: [create-or-extend-tables (EclipseLink will attempt to create tables. If the table exists, EclipseLink will add any missing columns)](http://www.eclipse.org/eclipselink/documentation/2.5/jpa/extensions/p_ddl_generation.htm)
 * DDL_GENERATION_MODE: [database (DDL will be generated and written to the database only)](http://www.eclipse.org/eclipselink/documentation/2.5/jpa/extensions/p_ddl_generation_output_mode.htm#BABCDHBB)
 * CLASSLOADER: Use the same classloader that Spring uses
 * LOGGING_LEVEL: INFO (Log informational EclipseLink/JPA messages)

Configuration using this class is similar to using a `persistence.xml` file.

### Spring Data JPA
Creating repositories that use the Java Persistence API is a cumbersome process that takes a lot of time and requires a
lot of boilerplate code.
We can eliminate some boilerplate code by using Spring Data JPA to get a convenient interface for generic CRUD operations
on our Advertisement repository.

For this, only the `@EnableJpaRepositories` annotation is added. By specifying where the interfaces are stored, beans with implementations of these interfaces are automatically provided by Spring Data JPA.
Internally Spring uses reflection to generate a [proxy class](https://docs.oracle.com/javase/7/docs/api/java/lang/reflect/Proxy.html), which contains the desired implementation details of the specified interface.
```java
/**
 * Provides a convenient repository, based on JPA (EntityManager, TransactionManager).
 */
@EnableJpaRepositories(basePackageClasses = AdvertisementRepository.class)
public class CloudDatabaseConfig {
}
```

### Excursion `Java Reflection`
Reflection is a language's ability to inspect and dynamically call classes, methods, attributes, etc. at runtime. 

Reflection is important since it lets you write programs that do not have to "know" everything at compile time, making them more dynamic, since they can be tied together at runtime. The code can be written against known interfaces, but the actual classes to be used can be instantiated using reflection from configuration files. Using a class loader we can load classes at runtime by passing the qualified class name as parameter.

When debugging the `AdvertisementController.advertisements()` method you can see that `adRepository` of type `SimpleJPARepository` is instantiated and called via reflection (@see `RepositoryFactorySupport` class).

The drawback of dynamic programming is that vulnerabilities of libaries can't be detected by security scans, as dynamically invoked methods / attributes are not analyzed. On the other hand by using reflection private fields of a class can be accessed and its value can be changed. This can be a serious security threat and cause your application to behave abnormally.


## Used frameworks and tools
- [Java Persistence API (JPA) tutorial](http://docs.oracle.com/javaee/6/tutorial/doc/bnbpz.html) 
- [Spring Data JPA](http://projects.spring.io/spring-data-jpa/)
- [EclipseLink Object/Relational Mapping](http://www.eclipse.org/eclipselink/)

## Further reading
- [JDoc PersistenceUnitProperties](https://eclipse.org/eclipselink/api/2.0/org/eclipse/persistence/config/PersistenceUnitProperties.html)
- [Spring Data JPA - Reference Documentation](http://docs.spring.io/spring-data/jpa/docs/1.8.0.M1/reference/html/#repositories.query-methods.query-creation)
