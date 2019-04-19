# Temporary Notes

## General
- entertaining and insightful presentation (does not really regard Log4j2): https://speakerdeck.com/xorlev/java-logging-ninth-circle-of-hell-a-gentle-introduction-to-java-logging
- Log4j (version 1) and java.util.logging should not be used

## SLF4J
- de-facto standard API
- discards logs if no implementation is provided!
- no need to reference implementation inside logging code
- spot incorrectly named loggers: http://www.slf4j.org/codes.html#loggerNameMismatch

## Logback
http://logback.qos.ch/
### Interesting Features
- MDC (Mapped Diagnostic Context): define context per thread, context is shown in each following log message
- NDC (Nested Diagnostics Context): push into stack structure, useful when debugging recursion
- add packaging information in log output: http://logback.qos.ch/manual/layouts.html#xThrowable
- markers (see Log4J 2) also seem to be supported: http://logback.qos.ch/manual/filters.html

### General
- native support of SLF4J

## Apache Log4J 2
http://logging.apache.org/log4j/2.x/

### Interesting Features
- Thread Context (see MDC and NDC above, https://logging.apache.org/log4j/2.x/manual/thread-context.html)
- markers (may be organized in hierarchy), allows for easy filtering based on markers
  - example: add dedicated marker to everything SQL related, show/hide those messages
- flows (building on markers): convenience methods for tracing (entry/exit/throwing/catching/...)
- message objects: https://logging.apache.org/log4j/2.0/manual/messages.html

### General
- Apache project
- can be used with SLF4J (with less features?)
- supports plugins (easy to configure/extend)
- very fast (only of theoretic interest?) with AsyncAppender
- intended for auditing, loses less log messages
- most Layout+Appender combinations possible
- Maybe helpful article when it comes to Log4j2 and dependencies: http://www.infoq.com/news/2014/07/apache-log4j2

## AOP
- AOP can be used to simply log entry/exit of methods
- implementation, BSD license: http://aspects.jcabi.com/annotation-loggable.html
- automatically log if method is too slow
- ignore logging of certain (expected?) exceptions
- not very flexible, needs weaving/recompilation
- Verwandt: http://docs.oracle.com/javaee/6/tutorial/doc/gkhjx.html

## General Performance Hints
- use format strings like `logger.log("something: {}", foo)` instead of concatenation `logger.log("something: " + foo)`
- use `logger.isLoggable(level) { ... }` if construction of log arguments is expensive
- do not log in tight loops
 
## Best Practises
- log a lot, test for performance impact (most likely logging is not too expensive)
- http://pixlcloud.com/applicationlogging.pdf
- agree on when to use which log level
- agree on log format
- always provide context (logging only constant strings is not really helpful)
- ensure logs are machine readable (TODO check with ELK stack)

### Random Notes (C. Otto)
- the more you log, the more code clutter you have
- we do not have live access to the system, so more log output helps debugging
- log entry/exit of certain important methods, but not all
- TODO: monitoring
- think about who needs data, and when? the more you know, the better you can prepare

### What to Log
- TODO: find out what Cloud Foundry adds for each log entry
- timestamp/application/severity
- user ID
- correlation/session ID (same ID across different microservices!)
- reason
- categorization/markers

### Use Cases
- business
 - which features are used
 - SLA fulfillment
 - changes in user behaviour
- operational
 - (user/critical) errors
 - app start/stop
 - code version
 - configuration
- security
 - login
 - logout
 - password changes
 - activity of admin user
- compliance
 - regulatory rules

## Open Questions
- authorization
- dynamic re-configuration (demanded by IoT team)
 - per microservice?
 - all apps in a space?
 - log all, filter later?
- guidelines what to log
 - IDs, passwords, ...?
 - tracing?
 - JPA/SQL queries?
- how to trace single request with service to service communication (showing same user/request/context id in log outputs?)
- how to instantiate logger?
 - static vs. instance?
 - via dependency injection?
- are logs mission critical?
 - CF may drop messages: https://groups.google.com/a/cloudfoundry.org/d/msg/vcap-dev/xRi_TNo58aE/1fUkRRvkHQgJ
 - https://www.pivotaltracker.com/n/projects/993188/stories/89022638
 - https://www.pivotaltracker.com/n/projects/993188/stories/99494586
 - https://github.com/cloudfoundry/loggregator/blob/9864b19/bosh/jobs/doppler/spec#L26-L28
