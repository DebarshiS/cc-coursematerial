Exercise: Use HANA Database via JDBC
====================================

## Learning Goal
Connect an application with a HANA database via JDBC. In this exercise the application creates tables **without using HDI**. 

Note: If you use HANA-specific features (not just standard SQL) then you should go for the HDI deployment approach as shown in the [next exercise](Demo_HANA_HDI.md).

## Prerequisite
- An account on **hanatrial** [https://account.hanatrial.ondemand.com](https://account.hanatrial.ondemand.com) (since the hdi-shared hana plan is not supported on the internal canary trial landscape ~~https://accounttrial.int.sap.hana.ondemand.com~~)
- As the `bulletinboard-ads` project already uses a PostgreSQL database, we will extend the `bulletinboard-statistics` project to use HANA. For this, import the `master` branch from [Statistics Git Project](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-statistics).

## Step 1: Create and bind CF HANA backing service
Use the HANA service plan `schema`, to get a pre-configured schema on a shared HANA database.

#### Get service plan description
As there are several plans for the `HANA` service, you can get further information by using `cf m -s hana`. 

#### Creating the service
In the terminal, run the following command: `cf create-service hana schema hana-statistics`

If you have already created this service before, delete first the application as well as the service:
```
cf delete bulletinboard-statistics
cf delete-service hana-statistics
```

#### Bind service
In the `manifest.yml` file, add `hana-statistics` as a service to be bound to your application:

```
services:
 - hana-statistics
```

## Step 2: Add Maven dependencies
Add the following dependencies to your `pom.xml` using the XML view of Eclipse:

- Add `ngdbc` dependency which is the JDBC driver for HANA:
```xml
<!-- SAP HANA -->
<dependency>
    <groupId>com.sap.db.jdbc</groupId>
    <artifactId>ngdbc</artifactId>
    <version>1.111.1</version>
    <scope>runtime</scope>
    <exclusions>
        <exclusion> <!-- Exclude old mockito version -->
            <artifactId>mockito-all</artifactId>
            <groupId>org.mockito</groupId>
        </exclusion>
    </exclusions>
</dependency>
```

- Add spring cloud connector dependencies:

```xml

<!-- Spring Cloud Connector -->
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-spring-service-connector</artifactId>
    <version>1.2.2.RELEASE</version>
</dependency>
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-cloudfoundry-connector</artifactId>
    <version>1.2.2.RELEASE</version>
    <scope>runtime</scope>
</dependency>
<dependency>
    <groupId>com.sap.hana.cloud</groupId>
    <artifactId>spring-cloud-cloudfoundry-hana-service-connector</artifactId>
    <version>1.0.4.RELEASE</version>
</dependency>
```
Note: You can get the most recent version of `spring-cloud-cloudfoundry-hana-service-connector` from [nexus](http://nexusrel.wdf.sap.corp:8081/nexus/#nexus-search;quick~spring-cloud-cloudfoundry-hana-service-connector)(group: com.sap.hana.cloud). A HANA connector for spring-cloud is available at [Github](https://github.com/SAP/spring-cloud-sap).
Similar to the PostgreSQL case, using this connector for bound HANA services will automatically give you a preconfigured `DataSource` instance you can use.

- Note: After you've changed the Maven settings, don't forget to update your Eclipse project! To do so right click on your Eclipse project and select `Maven` - `Update Project ...`  (`Alt+F5`)

## Step 3: Provide a database configuration
In order to get the preconfigured `DataSource` instance from the spring-cloud connector you need to:

- Create a configuration class named `CloudDatabaseConfig`:
```java
@Configuration
public class CloudDatabaseConfig extends AbstractCloudConfig {

	@Bean
	public DataSource dataSource() {
		return connectionFactory().dataSource();
	}
}
```
- Ensure, that you've enabled `@ComponentScan`, that is able to find the `CloudDatabaseConfig`, so that the `DataSource` gets injected. The `DataSource` provides the `getConnection` method to execute SQL statements as shown in the next step. (see [Cloud Database Connections](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Knowledge/CloudDatabaseConnection.md) for more information).

## Step 4: Use database connection
Replace the code of the `StatisticsCounter` class with this: [StatisticsCounter.java](https://github.wdf.sap.corp/raw/cc-java/cc-bulletinboard-statistics/solution-hana-no-hdi/src/main/java/com/sap/bulletinboard/statistics/util/StatisticsCounter.java) and have a closer look at it...

#### Executing queries
Queries based on SQL strings are executed using the `connection` provided by the `DataSource` bean. For this the code in the `execute` method is used.

#### Setup a Non-HDI database
Since we decided on using a non-HDI version of HANA, the tables are setup similar to other SQL databases.
**When not using JPA**, the tables need to be created via `CREATE TABLE`. 
Note: Ignore the error while creating the database table because HANA does not support `CREATE TABLE ... IF NOT EXISTS`.

## Step 5: Deploy and test application
With the created HANA backing service and binding (using `manifest.yml`), you can now make use of the service.

To deploy your application run in the terminal:
```
mvn clean package
cf push -n bulletinboard-statistics-d012345
```

Test your statistics application using `Postman`:
- Send multiple times a `PUT` request to `https://bulletinboard-statistics-d012345.[LANDSCAPE]/api/v1.0/statistics/1`. Each request increases the usage of item with id `1`.
- Send a `GET` request to the same URL. The response should reflect the number of your `PUT` requests.
- Furthermore the `PUT` request logs a `DEBUG` message `Execute update query, updated 1 rows`, which you can see in [Kibana](https://logs.cf.sap.hana.ondemand.com). 


## References
- [XSA Wiki: HANA](https://github.wdf.sap.corp/xs2/xsa-docs/wiki/HANA)


***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="Demo_HANA_HDI.md">
  <img align="right" alt="Next Exercise">
</a>
