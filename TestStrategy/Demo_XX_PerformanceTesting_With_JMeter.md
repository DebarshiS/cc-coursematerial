Exercise / Demo XX: Performance-Testing with JMeter
===================================================

## Learning Goal
Performance tests are used to ensure that the application satisfies certain non-functional requirements like scalability, reliability and resource usage.

The task of this exercise it to setup and expand a simple performance test using JMeter.

## Prerequisite
Install and start [JMeter](http://jmeter.apache.org/). Make sure your application `bulletinboard-ads` and all dependencies are running. 

## Step 1: Create a simple test plan for REST GET
When starting up JMeter, an empty test plan is automatically created. 
 - Thread Groups are a basic component of a JMeter test. JMeter uses thread groups to execute tests in parallel
 - Thread Group are a basic component of a test. Start by adding a Thread Group to the test plan: Right-click on `Test Plan` and select `Add`->`Threads (Users)`->`Thread Group`
 - In order to test a REST API, HTTP Request are made. Add a HTTP Request to the Thread Group by right-clicking on the Thread Group and selecting `Add`->`Sampler`->`HTTP Request`
 - In the HTTP Request Sampler, you need to fill out
   - Servername: The address of the application you want to test, i.e. `bulletinboard-ads-<your_id>.cfapps.sap.hana.ondemand.com`
   - Path: `/api/v1/ads`
   - Protocol: `https`
   - Port: `443`
   - Proxy: `proxy.wdf.sap.corp`
   - Proxy-Port: `8080`
   - Method: `GET`
 - In order to view the results, add `Listener`->`View Results in Table` to the test plan.
 - Click the play-icon in the icon bar and look at the results.
 - Note: You can click the broom button (Clear all) to clear the result. 

## Step 2: Multiple threads
- Click the thread group and increase the loop count to 10.
- Run the test and review the results  
- Click the thread group and increase the number of threads to 10.
- Run the test and review the results

## Step 3: Assertions
Currently, errors only occurs, if a request in not answered at all. In case of a test, we might also want to check the response code, i.e. that a request was correctly answered. 
- Add a `Response Assertion` to the HTTP Request, which checks that the response code is equals to 200.
Additionally, we want to fail in case a request takes longer than an acceptable duration.
- Add a `Duration Assertion` to the HTTP Request, which checks that the duration of a request is less than `1000` ms.

## Step 4: Errors
- Add another listener `Listener -> View Results in Tree` to the test plan. This listener allows to inspect the actual request and response.
- Experiment with the number of threads in order to find a maximum of parallel requests. Be careful not to increase the number of threads too high.
- Inspect the response of a failing request with the `View Results in Tree`-listener
- Reduce the number of threads back to a sensible amount (10 threads, 10 loops).

## Step 5: Defaults
Assume you need to have multiple different HTTP requests in your test, there needs to be a way to store common configuration data. Config Elements.
 - Add a `Config Element`->`HTTP Request Defaults` to the test plan
 - Move the entries Servername, Path, Protocol, Port, Proxy, Proxy-Port from the HTTP Request to the HTTP Request Defaults. Clear the entries in the HTTP Request.
 - Check that the tests still run 

## Step 6: Testing POST-Requests
- Change the test such that it tests ad-creation via POST-Request. Therefore, change the Method from `GET` to `POST` 
  - The minimum JSON body to send in such a request is:
```javascript
{
"title" : "xyz"
}
```
- Run the test and inspect the result
- The error Unsupported Media Type means that the server does not know how to interpret the body you sent: 
  - Add a `Config Element`->`HTTP Header Manager` below the HTTP Request. 
  - Add an entry in the HTTP Header Manager with name `Content-Type` and value `application/json`
  - Add another entry HTTP Header Manager with name `User-Id` and value `42`. Since we do not have working authentication yet, this is used to tell the server which user created the ad.
- Run the tests


## Step 7: Setting up your test
Test should be reproducable, and the result of a performance test should be comparable to the result of the same test with the last build. That means, we need to setup our test data in the same way:
 - Add a `setup Thread Group` to the test plan. Those are run before any normal `Thread Groups` are executed
 - Add a `HTTP Request`-sampler to the setup Thread Group. Set the method to `DELETE`. This ensures, that all existing ads are deleted.
 
## Used Frameworks and Tools
- [JMeter](http://jmeter.apache.org/)
