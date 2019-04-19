# Database Schema Evolution

In the course of microservice developement, you won't design your complete database model upfront, rather you will evolve it i.e. create new tables, alter tables with additional foreign keys, columns etc.

Within the course we've configured EclipseLink in that way, that missing tables/columns are created/added automatically. 
Let's assume you are adding a field such as `version` to your `Advertisement` table. The next time, after you've deployed your application again to the tomcat server, a new column was added.  

What's "wrong" with that? When testing with new model objects (e.g. advertisements) everything seems to be fine. But, as already discussed in [Exercise 9](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/ConnectDatabase/Exercise_9_ImplementJPAEntity.md#problems-with-implicit-database-schema-updates-using-jpa) you might not recognize, that an update of an existing object, that was persisted before the table schema was updated, might cause unexpected side-effects, as your application expects now a not-null value for the new `version` field. And for sure, you typically don't want to work around those situations as part of your application code, rather you would like to fill up existing entries with default values e.g. "1".

The disadvantages migrations done by specific JPA providers:
- the migration is JPA provider specific, is done in an implicit and incomprehensible way
- adding and even renaming a field in a JPA Entity results for example in: `ALTER TABLE table_name ADD column_name datatype ...`
- the migration is not appropriate for production, high chance that data gets inconsistent, lost ...

In that respect you need to prevent (!) the JPA provider such as EclipseLink or Hibernate to update the database schema automatically and instead you should (!) make use of a database schema migration tool.

## Tools: Flyway vs. Liquibase
There are mainly two tools that are commonly used for database migrations we like to mention here: Flyway and Liquibase. 

**Flyway** is the "flyweight" among the two tools, easier to start with, especially if you like to define your database changes in SQL format. 

**Liquibase** on the other hand supports next to SQL a declaritive approach (e.g. xml, yaml, json) for defining the db changes and might be the more flexible approach, when you like to switch to another kind of database.  
Liquibase seems to be more *enterprise* ready, it allows for example to structure your change sets and to define preconditions like "if this table does not exist"... 

### Transactional Consistency
Provided that the database supports database transactions, both tools ensure that a set of database changes is processed in an separate transaction and in an consistent way, i.e. changes are rolled back, in case an error occurs as part of applying the changes.

### Further Hints
- **All changes need to be backward compatible** as all application instances and even in case of Blue-Green deployment both application versions rely on the same database instance.
- **All updates should be applied** by the database migration tool only. Otherwise there are unmanaged and untracked database changes. Consequently you need to configure your JPA Provider that it never applies DDL-statements to your database. 

## Liquibase

### Getting started
In your (Spring Boot) application you integrate Liquibase as dependency to your `pom.xml`:
```
<!-- Liquibase dependencies for db-migration -->
<dependency>
	<groupId>org.liquibase</groupId>
	<artifactId>liquibase-core</artifactId>
	<!-- version 3.5.1 managed by spring boot 1.4 or 3.4.2 managed with SpringBoot 
		1.3.3 -->
</dependency>
```

Then you can configure it. As part of a Spring Boot application this is done as part of your [`application.properties`](https://github.wdf.sap.corp/D047717/LiquibaseDemo/blob/master/LiquibaseDemo/src/main/resources/application.properties).

With that the changes that are declared as part of your `liquibase.change-log` folder e.g. [`src/main/resources/db/changelog`](https://github.wdf.sap.corp/D047717/LiquibaseDemo/tree/master/LiquibaseDemo/src/main/resources/db/changelog) are applied even before the application is started as it runs before Spring Container is fully started and prior JPA validation.

The first time, liquibase runs, two additional database tables get created:
- `databasechangeloglock` - provides "lock" information to avoid conflicts; especially valuable when an application with multiple instances are updated all at once to a higher version and try to apply the same Liquibase schema update.
- `databasechangelog` - contains the information, which `Changeset` was applied at which timestamp. `Changeset` is uniquely identified by author, id and filename). Additionally it stores the Hash of the Liquibase commands to check whether the `Changeset`, which was already applied has changed in between (should never happen). 

#### Changelogs and Changesets
The starting point are so called `Changelog`s, which allow to group and structure the so called `Changeset`s which are executed in exact that order (top down) if the "preconditions" are met and if it was not yet applied (tracked in the `databasechangelog` table). A `Changeset` in turn contains the actual Liquibase commands that should be executed as part of one transaction. 

### Tips from the Experts
#### Example
You can find a simple liquibase example on [github](https://github.wdf.sap.corp/D047717/LiquibaseDemo); you might want to fork or clone it in order to "play" with it locally. 
It is a Spring Boot application with only one Person JPA Entity, where you would like to rename the column from "name" to "surname". The example consolidates the best-practices and learnings of Mario Graf and Team.

#### Liquibase Maven Plugin
You can include Maven Liquibase plugin `liquibase-maven-plugin` into your `pom.xml`:
```
<plugin>
	<groupId>org.liquibase</groupId>
	<artifactId>liquibase-maven-plugin</artifactId>
	<version>3.5.1</version>
	<configuration>
		<propertyFile>src/main/resources/db/liquibase.properties</propertyFile>
	</configuration>
```				
- Run maven command `mvn liquibase:diff` in order to compare two schemas and to generate a change-set for the diff (in xml format). You can configure its behaviour as part of the `liquibase.properties`, e.g. you can specify that the delta of the data should be considered as well as described in this [`liquibase.properties`](https://github.wdf.sap.corp/D047717/LiquibaseDemo/blob/master/LiquibaseDemo/src/main/resources/db/liquibase.properties).
- Run maven command `mvn liquibase:generateChangeLog` in order to generate an initial changelog-file that matches to an already existing database schema.

#### Testing 
Furthermore it describes how to test the Schema migration and data integrity by making use of a special context such as `liquibase-migration-test` to run a conditional [changeset to populate some test-data](https://github.wdf.sap.corp/D047717/LiquibaseDemo/blob/master/LiquibaseDemo/src/main/resources/db/changelog/liquibaseMigrationTestData.xml). This should happen for example right after a new table is created.

To ensure that liquibase applies all changesets, we need to
- drop all tables (extract from `application.properties`):
```
liquibase.enabled=true
liquibase.drop-first=true
liquibase.contexts=liquibase-migration-test
spring.jpa.hibernate.ddl-auto=validate
```
- deploy the application once again on a Web Server as part of your JUnit Test:
```
@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment=WebEnvironment.RANDOM_PORT)
public class LiquibaseMigrationTest {

	@Autowired
	private AdvertisementRepository adsRepository;
	
	@Test
	@Transactional
	public void repository_find_findsTestDataAfterMigration() {
		Advertisement ads = adsRepository.getOne(1l);
		
		assertThat(adsRepository.getId(), Matchers.is(1l));
		assertThat(testPerson.getTitle(), Matchers.is("My first Ad"));
	}
}
```


## Further References
- [Liquibase](http://www.liquibase.org/)
- [Flyway](https://flywaydb.org/)
- [HANA Deployment Infrastructure - HDI](https://wiki.wdf.sap.corp/wiki/x/PoHzZ)
- [Database Migration as part of Zero Downtime Deployment](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/DevOps/Zero_Downtime_Deployment/Zero-Downtime_Migration.md)
- [Database Migration as part of Zero Downtime Deployment - slides](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/DevOps/Zero_Downtime_Deployment/Zero-Downtime_Migration.pptx)

## Recording of Info Session
- Mario's TODO

