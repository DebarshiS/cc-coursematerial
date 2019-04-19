# Aspect-Oriented Programming (AOP) for tracing
Aspect-Oriented Programming is a programming paradigm, which allows to add arbitrary code to multiple existing locations, without actually modifying those locations. As such, AOP allows us to centrally define which methods/fields/exceptions should be traced and which information should be logged, without having to change all of the existing code.

In the following examples, we focus on method execution aspects, since this is the most simple and common usecase for tracing. AOP additionally allows for logging field accesses, exception handling and synchronization wrapping.

Our used library for AOP in Java is [AspectJ](https://eclipse.org/aspectj/), due to widespread tooling support.

## Basic concepts
- **Pointcut** expressions are used to define code and code events that should be modified using AOP. For example, using pointcut expressions one can specify "any code inside a class in the package `com.xyz`" or "execution of any public method". In AspectJ it is possible to name pointcut expressions by using the `@Pointcut` annotation, where the annotation argument is the pointcut expression, and the void method the annotation is attached to serves as the name. As an example, `@Pointcut("within(com.xyz.*)")` could annotate an empty method `public void inPackageComXyz() {}`. Then, in other pointcut expressions, the name `inPackageComXyz()` can be used where appropriate.
- A **join point** is an actual event matching some pointcut expression, for example execution of a method. While pointcut expressions are used to define join points, the actual join points are the "instances" matching these expressions.
- An **advice** is the Java code that should be applied to a set of join points. As an example, advices can add logging statements to methods represented by the join points matching a given pointcut expression. Each advice further specifies whether the code should be added before, after, or around the execution of the join point. For example, the following advice uses the `@Before` annotation so that an additional log message is printed before the actual executions of the referenced join points. Note that we used a combination of named pointcuts in the pointcut expression.
```java
@Before("inPackageComXyz() && !nameStartsWithGet()") 
public void logNonGetterMethods(JoinPoint joinPoint) {
   logger.trace("Reached join point");
}
```

For more detailed concepts of AspectJ, see [The AspectJ Programming Guide](http://www.eclipse.org/aspectj/doc/next/progguide/).

## Compile-time weaving vs. load-time weaving
In order for the tracing statements to be executed, the original code is augmented by the tracing methods. This action of injecting the AOP-code into target code is called weaving. 
The main difference is when weaving takes place. The simplest approach is compile-time weaving via maven-plugin, which we'll be using in our example. See [Load-Time Weaving](https://eclipse.org/aspectj/doc/released/devguide/ltw.html) for further details.

## Examples
For examples, see [cc-bulletinboard-ads with AOP](hhttps://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/demo-aop-for-logging/src/main/java/com/sap/bulletinboard/ads/aspects). 

## Basic setup
- Install AJDT in Eclipse. 
  - Find the correct software site for your Eclipse version on [Eclipse AJDT downloads](http://www.eclipse.org/ajdt/downloads/). 
  - In Eclipse, open `Help`->`Install New Software` and paste the software site (for Eclipse Mars: `http://download.eclipse.org/tools/ajdt/45/dev/update`). Then select AspectJ Development Tools and proceed.
- Checkout branch [demo-aop-for-logging](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/demo-aop-for-logging). 

### Maven `pom.xml`

You need to maintain in the dependency to `aspectjrt`:
```
<!-- AspectJ -->
<dependency>
   <groupId>org.aspectj</groupId>
   <artifactId>aspectjrt</artifactId>
   <version>1.8.6</version>
</dependency>
```
In order to introduce compile-time weaving. The plugin `aspectj-maven-plugin` is configured, such that the original code is supplemented during process-source phase of the build process:
```
<plugins>
	<plugin>
		<groupId>org.codehaus.mojo</groupId>
		<artifactId>aspectj-maven-plugin</artifactId>
		<version>1.7</version>
		<configuration>
			<encoding>UTF-8</encoding>
			<showWeaveInfo>true</showWeaveInfo>
			<verbose>true</verbose>
			<source>1.8</source>
			<target>1.8</target>
			<complianceLevel>1.8</complianceLevel>
		</configuration>
		<executions>
			<execution>
				<id>weave-classes</id>
				<phase>process-sources</phase>
				<goals>
					<goal>compile</goal>
				</goals>
			</execution>
		</executions>
		<dependencies>
			<dependency>
				<groupId>org.aspectj</groupId>
				<artifactId>aspectjtools</artifactId>
				<version>1.8.6</version>
			</dependency>
		</dependencies>
	</plugin>
</plugins>			
````			


### Example 1 - Tracing methods calls with @Before
See class [`com.sap.bulletinboard.ads.aspects.TraceAllRestCallsAspect`](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/demo-aop-for-logging/src/main/java/com/sap/bulletinboard/ads/aspects/TraceAllRestCallsAspect.java).

### Example 2 - Tracing method calls with parameters and annotations
See class [`com.sap.bulletinboard.ads.aspects.TraceModelSetterParametersAspect`](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/demo-aop-for-logging/src/main/java/com/sap/bulletinboard/ads/aspects/TraceModelSetterParametersAspect.java).

### Example 3 - Wrapping calls and accessing return values
See class [`com.sap.bulletinboard.ads.aspects.TraceUserServicePerformanceAspect`](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-webmvc/tree/demo-aop-for-logging/src/main/java/com/sap/bulletinboard/ads/aspects/TraceUserServicePerformanceAspect.java).


## Further Reading
- [AspectJ Project](https://eclipse.org/aspectj/)
- [The AspectJ Programming Guide](http://www.eclipse.org/aspectj/doc/next/progguide/)
- [AspectJ-Cheat-Sheet](http://blog.espenberntsen.net/2010/03/20/aspectj-cheat-sheet/)
- [Eclipse AspectJ Development Tools (AJDT)](http://www.eclipse.org/ajdt/)
