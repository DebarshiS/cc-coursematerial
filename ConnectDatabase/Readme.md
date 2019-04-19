# Connect to Database - Detail Notes

Business data of applications is typically persisted in databases. Standard transaction requirement (ACID) must be applied to all databases involved in a transaction:
- **Atomicity:** commit all OR rollback all
- **Consistency:** transform database from a valid state to a valid state
- **Isolation:** changes that a transaction made to a database are not visible to other operations until the transaction completes its work
- **Durability:** changes that a transaction makes to a database survive future system or media failures. Most commonly this is implemented using "Two Phase Commit".

## Binding Cloud Foundry Backing Services
Using the marketplace (`cf m`) you can see the backing services which are available in the cloud.
After creating an instance (`cf create-service`) this instance can be bound to your application.
This can be done using `cf bind-service`, or by specifying the service instance's name in the `manifest.yml` file of the application.
In both variants the service details (password etc.) are provided in the `VCAP_SERVICES` environment variable, which is only visible/updated after an application restart. If the manifest file is used to bind a service, the details are visible after issuing `cf push`.

Note that you can only bind service instances to applications in the same Cloud Foundry space.

## How to persist data to database?
### Use SQL directly with JDBC
Problem: SQL is not Object Oriented (like Java Objects) whereas Java objects offer the possibility to encapsulate application state/behavior. As persistence mechanism needs to be hard-coded, developer needs to be aware of all SQL issues when attempting to update the data. That becomes hard to maintain. Assume for example you need to change the database schema, then the application code needs to be changed as well. 

This leads to brittle, inflexible and database-depended application code and **it is definitely not the goal and best practice!**

### Mapping Business Data encapsulated using JPA

Alternatively business data is easily mapped to an underlying data store using the JPA Services for database connectivity and persistence management. JPA gives us a simple persistence model:
- describes rules for managing persistence and doing Object-Relational (O-R) mapping with a lot of defaults and assumptions
- O-R mapping refers to mapping objects to relational databases like PostgreSQL.
- Several open-source implementations (such as [EclipseLink or Hibernate](/_Internals/Tool_Decisions.md#eclipselink-vs-hibernate#eclipselink-vs-hibernate)) are available that give us access to a lot of databases and that perform O-R mapping

JPA specification expects the vendor providers to support persisting and retrieving data (examples include creating a table, adding column and performing CRUD operations).

## Understand JPA in more detail
### Entities 
- represent business objects in a persistent storage (usually a database) that are shared and concurrently accessed by multiple clients
- represent physical things or nouns in a system, for example Customer or Order
- can be created/found/pooled and removed
- are long-lived and survive both a crash or a deliberate shutdown of the server
- cannot be accessed remotely
- are Plain old java objects (POJOs), classes are annotated using the `@Entity` annotation. Class name is used as table name or you map to another (existing) table using the `@Table(name="MYTABLENAME")` annotation. Any field name specifies the name of the column, also here you can map to another (existing) table column using the `@Column(name="MYCOLUMNNAME")` annotation. Each Entity instance represents a unique row in a table, each entity has a primary key using `@Id` annotation. There are different [ID-Generation strategies](https://docs.oracle.com/javaee/6/api/javax/persistence/GenerationType.html) available. Read more about it [here](http://www.developerscrappad.com/408/java/java-ee/ejb3-jpa-3-ways-of-generating-primary-key-through-generatedvalue/).

### Types for `@Id` entity field
The types for the `@Id` field and its corresponding setter need to be picked with care. Internally the repository (part of Spring Data JPA) needs to decide if a given object instance already is persisted, or if it is a new object instance. An ID field with value `null` designates a new (unpersisted) instance, whereas `0` is treated as a valid ID. Thus, the field annotated with `@Id` must have a type corresponding to a Java wrapper class (`Long`, `Integer`, ...).

When constructing a Java object instance based on JSON, Jackson uses setters if available. Here, a missing attribute in the JSON string causes JSON to invoke the setter with a `null` argument. This works as expected. However, if the setter's argument has a primitive type (`long`, `int`, ...), Jackson automatically provides `0` as an argument. As outlined above, this can cause problems, as `null` and `0` are treated differently.

#### Composite Primary Key
Sometimes a key is not simply one type. A composite primary key consists of multiple primary key fields. Each primary key field must be one of the supported types.

For example, the primary key of the following Project entity class consists of two fields:
```
@Entity @IdClass(ProjectId.class)
public class Project {
    @Id int departmentId;
    @Id long projectId;
     :
}
```
Note that when an entity has multiple primary key fields, JPA requires defining a special ID class that is attached to the entity class using the `@IdClass` annotation. The ID class reflects the primary key fields and its objects can represent primary key values:
```
Class ProjectId {
    int departmentId;
    long projectId;
}
```


### JPA Performance
JPA is used as an additional layer between business logic and the actual database.
For most cases the corresponding performance hit can be ignored, as the actual query design and resulting database performance is more important.
In the context of JPA the developer needs to think about pre-fetching strategies (lazy vs. eager), selection of columns, and pagination - just to name the most important aspects. [This article](http://zeroturnaround.com/rebellabs/how-to-use-jpa-correctly-to-avoid-complaints-of-a-slow-application/) gives a good overview over this topic.

### JPA Callback Methods 
JPA callback methods are methods which can be defined within an entity class. The annotation specifies when the callback method is invoked by JPA:

| method annotation | description |
| ----------------- | ----------- |
| `@PrePersist` | before a new entity is persisted (added to the EntityManager) |
| `@PostPersist` | after storing a new entity in the database (during commit or flush) |
| `@PostLoad` | after an entity has been retrieved from the database |
| `@PreUpdate` | when an entity is identified as modified by the EntityManager |
| `@PostUpdate` | after updating an entity in the database (during commit or flush) |
| `@PreRemove` | when an entity is marked for removal in the EntityManager |
| `@PostRemove` | after deleting an entity from the database (during commit or flush) |

Read more about JPA Lifecycle Events [here](http://www.objectdb.com/java/jpa/persistence/event).

### Entity Manager
- Entity manager is a service that manages persistent entities. It offers a CRUD interface. 
- An application works with an entity instance to retrieve and update data. Behind the scene, the entity manager synchronizes the data to the database. The entity manager keeps track of every entity instance that has been used by the application to load, update or insert data.
- The entity manager manages the entity instances until they are detached (for example when a transaction fails and is rolled back).
- The insert, delete, update operations done by the application code are translated to actual SQL calls just before the transaction ends. Until that point the entity manager simply "records" all the activity. For example, if you delete an instance, the system flags it as removed. Just before the transaction is committed, the system actually executes the DELETE statements for the deleted instances.

### Transactions
In our example project we do not explicitly use transactions. To adhere to the ACID principles outline above, the code needs to be extended accordingly. In our setting methods annotated with `@Transactional` automatically use a new (or re-use an existing) transaction. For this to work, the `@EnableTransactionManagement` annotation needs to be added to an active Spring configuration, for example `CloudDatabaseConfig`. As described in the [documentation](http://docs.spring.io/spring-data/jpa/docs/current/reference/html/#transactions) the Spring Data repositories also use transactions internally.

### JPQL and Native Quries
With JPA it is possible to query the underlying database using the Java Persistence Query Language (JPQL). In contrast to SQL, in JPQL one uses the (Java) entities' names and attribute names.
The mapping to actual SQL queries and the corresponding table/column names is done by JPA, exactly as in the case of working directly with the entity manager (or constructs such as the `Criteria` API).
As such, JPQL is platform independent.

Example:
```
entityManager.createQuery("SELECT u.id FROM User u WHERE u.city=’Berlin’");
```

For queries that cannot be expressed using JPQL, one can also issue native SQL queries to the database.
For this, the entity manager provides the `createNativeQuery` method.
Example:
```
entityManager.createNativeQuery("select * from T where CONTAINS( (column1,
column2,column3), ’cats OR dogz’, FUZZY(0.7));");
```
[Further information](https://wiki.eclipse.org/EclipseLink/UserGuide/JPA/Basic_JPA_Development/Querying/Native#Native_SQL_Queries)

## Database Configuration
In order to interact with the database there must be some sort of database configuration, so that the Data Source is instantiated. 
We need to instantiate the JPA implementation (such as EclipseLink) to get connected to the database via a Data Source.

## Connect to a User Provided Service

Services can be predefined as a Cloud Foundry Backing Service in your CF instance, or you can expose existing services hosted elsewhere as 'User Provided Service' and then connect to it the same way as to predefined services. 

See the [User Provided Service](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Knowledge/UserProvidedService.md) page for details.


## Cloud Foundry Demo

Prepare your command line:
- increase font size
- increase screen buffer size (e.g. 250x4000)

Check out an application that depends on a postgres database service e.g. [`origin/solution-10-Deploy-Ads-With-DB-Service-On-CF`](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/solution-10-Deploy-Ads-With-DB-Service-On-CF).

## Create Service and push your Application
Go to the project root folder.

Explain the dependency to the database service with name `postgres-bulletinboard-ads` in the `manifest.yml` file. With that it's not possible to deploy the application to CF without having a backing service provided within the space. 

```
$ cf marketplace       # explain the different services that are available in the space
$ cf create-service postgresql v9.4-dev postgres-bulletinboard-ads
$ cf s                 # show service is created and available, but not bound to any application
$ cf push -n <my-host>
$ cf s                 # show service is now also bound to <my-app>
$ cf env <my-app>      # show the postgres db connection information
```

Note that the same database instance is shared by all application instances.

## FAQ

#### Q: How straight-forward is JPA?
There are situations where the complete set of CRUD operations offered by JPA does not fit your use case:
If, for example, the data your application relies on is generated by a service that is owned by a different team, you may only want to read but not update, create or delete the data. 
Your application that accesses this data ideally consumes a bulk read service offered by the other team. 
However, depending on which project phase the service you rely on is in, such a service may not be available yet. 
Therefore you may have to access the service's data source directly without using an API.
In this case, your code must ensure to only offer READ operations and exclude all operations that are modifying the data. 
In the Global Design Frontrunner Apps project "Smart Campus" (SAP CP Neo IoT service extension, for details see [here](https://jam4.sapjam.com/blogs/show/Pm96AwVH65s1vH3VfIAmjz)) we used plain JDBC with SQL views to adopt to the restrictions described above and to ensure good query performance.
You may have to invest additional effort into your JPA implementation if your requirements differ from the typical CRUD operation scope.

#### Q: What about database backup, migration, higher performance, ...?
The services with the suffix "-lite" should not be used for production. Recently, "-pro" services have been added, which in the long term also offer features like backup. More up-to-date information will be provided on the cf.users mailing list.
 - [initial announcement](https://listserv.sap.corp/pipermail/cf.users/2016-April/001542.html)
 - [cf.users](https://listserv.sap.corp/mailman/listinfo/cf.users)

