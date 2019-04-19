Exercise 26: Performance-Testing with JMeter
============================================

## Learning Goal
Performance tests are used to ensure that the application satisfies certain non-functional requirements like scalability, reliability and resource usage.

The task of this exercise it to setup and expand a simple performance test using JMeter.

## Prerequisite
Start [JMeter](http://jmeter.apache.org/). In the VM it suffices to run `jmeter` in the terminal.

Make sure your application `bulletinboard-ads` and all dependencies are running on the local machine.

## Step 1: Create a simple test plan for REST GET
When starting up JMeter, an empty test plan is automatically created. 
- Thread Group are a basic component of a test. Start by adding a Thread Group to the test plan: Right-click on `Test Plan` and select `Add`->`Threads (Users)`->`Thread Group`
- Add a HTTP Request to the Thread Group by right-clicking on the Thread Group and selecting `Add`->`Sampler`->`HTTP Request`
- In the HTTP Request, set Server Name or IP to `localhost`, port to `8080` and path to `api/v1/ads` 
- In order to view the results, add `Listener`->`View Results in Table` to the test plan.
- Click the play-icon and look at the results (save the plan if you are asked to do so to avoid further messages). 
- Notice that the status indicates a failure. Fix this by adding an authorization header:
 - add `Config Element` - `HTTP Header Manager` to the HTTP Request
 - configure a header named `Authorization` with the value of [this file](https://github.wdf.sap.corp/raw/cc-java-dev/cc-coursematerial/master/Security/jwtUpdate.txt) (which grants the Display and Update scopes)
 - run the test again and make sure that the status indicates success

## Step 2: Multiple threads
- Open the thread group and increase the number of threads to 10.
- Experiment with the number of threads in order to find a maximum of parallel requests. Be careful not to increase the number of threads too high.

## Step 3: Assertions
- Set the number of threads to 100.
- Add a `Response Assertion` to the HTTP Request, which checks that the response code is 200.

## Step 4: Timers
- Add a `Gaussian Random Timer` to the thread group.
- Increase the loop count of the thread group to 20.

## Step 5: Testing POST-Requests
- Change the test such that it tests ad-creation by POST-Request. The minimum JSON to send in such a request is:
```javascript
{
"title" : "xyz"
}
```
- Furthermore you need to specify the Content type as part of the HTTP header: In the `HTTP Header Manager` add the key-value pair `Content-Type`=`application/json`.
- Change the value of the `Authorization` header to the contents of [this file](https://github.wdf.sap.corp/raw/cc-java-dev/cc-coursematerial/master/Security/jwtUpdate.txt) (which grants the Display and Update scopes)

<a id='jmeter-known-issues'></a>
## Known Issues with JMeter

### Problems running JMeter on Windows
Running JMeter on Windows may cause problems if sending many requests in a short time.
You may get an error *""java.net.BindException: Address already in use: connect” issue on Windows"*.
A solution to this problem is described [here](https://www.baselogic.com/2011/11/23/solved-java-net-bindexception-address-use-connect-issue-windows/):
- open the Windows Registry (press 'Windows+R' and enter `regedit`)
- go to entry `HK_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters`
- add `DWORD MaxUserPort` with decimal value `65,534` ([docs](https://technet.microsoft.com/en-us/library/cc938196.aspx))
- add `DWORD TcpTimedWaitDelay` with decimal value `30` ([docs](https://technet.microsoft.com/en-us/library/cc938217.aspx))

### Out of Memory Exceptions in JMeter
A good summary of sources for OutOfMemory exceptions and possible solutions is provided [here](https://www.blazemeter.com/blog/9-easy-solutions-jmeter-load-test-%E2%80%9Cout-memory%E2%80%9D-failure).

## Used Frameworks and Tools
- [JMeter](http://jmeter.apache.org/)

## Further Material
- Watch [Recording at SAP Media Share](https://video.sap.com/media/t/1_4nj2lh3u/39197781)
- [JMeter Example that test the secured bulletinboard-ads application](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/TestStrategy/JMeterPerformanceTestPlan_security.jmx)  
(please that you need to adapt url, xsuaa client / secret)
