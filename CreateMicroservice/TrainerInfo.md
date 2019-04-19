## Exercise 3:
You can import the [Postman Collection](Exercise_3_CreateAdsEndpoints.json.postman_collection)

When issuing a POST request, you must provide a valid JSON body and must ensure that the application type header is set to `application/json`. 

## Exercise 4:
You should look at the steps on how to deploy microservice on Tomcat manually in the command line as described here: [Exercise 1: Getting Started](Exercise_1_GettingStarted.md)
as these steps are automated in the Component JUnit Tests.

In the exercise demo:
- look at the pom.xml to see dependencies to embedded Tomcat
- look at the test code and understand how the embedded Tomcat server is started/stopped
- look at how to run JUnit tests

Important Notes
- The embedded Tomcat server is not the same like locally installed!
- With the usage of an embedded Tomcat it's possible to start the tests in any environment e.g. on Jenkins without installing a tomcat webserver
