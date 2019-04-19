# Hystrix Dashboard

Hystrix provides a dashboard that can be used to get an overview of the status of the individual circuits and thread
pools. This dashboard can be configured to monitor several applications or microservice instances.

In this demonstration we show how the dashboard can be used in conjunction with a microservice.
Furthermore, we explain the basic use cases and information that can be obtained by observing the dashboard.

## Prerequisites
To be able to see details of Hystrix as used in your own microservice, you need to expose the data.
For this add the following Maven dependency:

```
<dependency>
    <groupId>com.netflix.hystrix</groupId>
    <artifactId>hystrix-metrics-event-stream</artifactId>
    <version>1.4.23</version>
</dependency>
```

This library offers a servlet named `HystrixMetricsStreamServlet`.
A microservice extended by this servlet now exposes the necessary data at `https://URL/hystrix.stream`.

## Dashboard installation
To enable it, you need a separate dashboard service. If implemented in Spring boot, you need to provide the following dependencies in the `pom.xml`:
```
<dependency>
    <groupId>org.springframework.cloud</groupId>
    <artifactId>spring-cloud-starter-hystrix-dashboard</artifactId>
</dependency>
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>
```

Then you need to annotate a `@Configuration` annotated class with `@EnableHystrixDashboard` in order to enable the required metrics within your application.

You can also use [this pre-deployed dashboard](https://cc-hystrix-demo.cfapps.sap.hana.ondemand.com/hystrix) instance.

On the landing page you just need to enter the URL to the data exposed by the servlet introduced above (`https://URL/hystrix.stream`, for example `https://bulletinboard-ads-production.cfapps.sap.hana.ondemand.com/hystrix.stream`).
The resulting URL can be bookmarked so that you do not need to re-enter the stream URL.

## Dashboard overview
A dashboard shows the state of all commands used in a system. Below you see a typical dashboard: 

<img src = "https://github.com/Netflix/Hystrix/wiki/images/hystrix-dashboard-netflix-api-example-iPad.png">

The main component of the dashboard is the display of the details for a specific command.
In the following picture the details for the command "SubscriberGetAccount" are explained.

<img src = "https://github.com/Netflix/Hystrix/wiki/images/dashboard-annoted-circuit-640.png">

In error cases the color of the circle changes to indicate the problem visually.
In the following example the high error percentage caused the circuit to open.
Because of that most requests are rejected immediately (shown in blue).

<img src = "https://github.com/Netflix/Hystrix/wiki/images/dashboard-example-open-circuit-640.png">

## Demonstration

To see live information in the dashboard, use the [pre-deployed](https://cc-hystrix-demo.cfapps.sap.hana.ondemand.com/hystrix) dashboard.
The branch [hystrix-dashboard-demo](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-boot/tree/hystrix-dashboard-demo) contains the code necessary for this demonstration.
Deploy the microservice, and connect the dashboard to `https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com/hystrix.stream`.

We use JMeter to access the microservice with a constant stream of requests.
Download [DashboardTest.jmx](https://github.wdf.sap.corp/raw/cc-java-dev/cc-coursematerial/master/Service2ServiceCommunication/DashboardTest.jmx) and load the file in [JMeter](https://jmeter.apache.org/).
This file uses five concurrent request to create new advertisements, and loops forever.

You need to adjust the URL (and possibly other settings) in the "HTTP Request" item.
Start the suite and observe the results in the Hystrix Dashboard.

As the threadpool used for Hystrix only starts five threads (in the "Thread Group" item), you may increase the number of concurrent users to more than five to see the effects as errors in the dashboard.
For example, with 20 concurrent users about half of the requests are rejected (purple) because the thread pool is full.

To trigger the circuit breaker, you can change the timeout of the `GetUserCommand` by issuing a PUT request to the default resource with the timeout in milliseconds as a path argument (i.e., send a PUT request to `https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com/hystrix/80` to update the hystrix timeout to 80 milliseconds).

With a value low enough, you can see that the error percentage quickly rises.
With the current configuration, the circuit breaks at 50% errors.
Afterwards, most incoming requests are rejected (purple).
One request is passed after the sleep window (default 5 seconds), to check if the circuit needs to stay open.

To solve the issue, update the timeout to a higher value (e.g. 1000). 
As you can see in the dashboard, the circuit will close after a short while, and the error percentage drops.

## Multiple Instances
The setup described so far only works with a single microservice instance.
If you want to observe the status of several instances, this is possible by aggregating the data using Netflix Turbine.
The details of this are outlined [here](https://github.com/Netflix/Hystrix/wiki/Dashboard#installation-of-turbine-optional).

## Notes:
 - By default, the servlet exposing the data is limited to five concurrent sessions. Depending on the circumstances connections in Cloud Foundry only time out after fifteen minutes, which may trigger this limit. In this case it can help to simply restart the microservice.
 - Any microservice, including the dashboard, deployed on Cloud Foundry can only be accessed via HTTPs.
   Dashboard versions prior to 1.5.1 depended on a library embedded via a HTTP URL. As such, modern browsers refused
   to download this library. This was fixed with Hystrix 1.5.1.
 - The dashboard only shows "Loading..." before the first Hystrix Command is used in the application. Instead of reloading the page again and again (exhausting the five concurrent sessions, see above), it suffices to just run a single Hystrix Command. In our Proof of Concept implementation we included a [dummy command](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads-spring-boot/blob/master/src/main/java/com/sap/bulletinboard/ads/BulletinboardAdsApplication.java) which is executed once on startup.

## Further Reading
- https://github.com/Netflix/Hystrix/wiki/Dashboard
- https://github.com/Netflix/Hystrix/tree/master/hystrix-dashboard
- https://github.com/Netflix/Hystrix/wiki/Operations
