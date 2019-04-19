# Exercise: Analyze application logs in `Kibana`

## Learning Goal
The goal of this exercise is to get familiar with the log output of Cloud Foundry and learn how you can analyze logs in Kibana as part of the provided ELK stack. The ELK stack includes **`E`**lasticSearch, **`L`**ogstash and **`K`**ibana. Logstash supplies the logging infrastructure, Elastic search offers search features, Kibana reports, consolidates, slices and dices the information. 

Proper logging is very important as it is not possible to debug a running microservice. Reason for this is that the debug port is closed and as we have multiple instances it is difficult to target a specific instance.

## Demo
- <img src="https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Z_ReuseImages/images/information.jpg" height="20" alt="Video on video.sap.com"/> [Kibana demo](https://video.sap.com/media/t/1_4gvkpx00) (14 minutes)

## Steps
Optionally you can follow these [Exercise steps](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/LoggingTracing/Exercise_14_GettingStarted_With_ELK_Stack.md#step-3-login-to-kibana) to analyze the (application) log messages in the [Kibana dashboard](https://logs.cf.sap.hana.ondemand.com/) by your own.


***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="/QuickStart/Exercise2_TestYourRESTApi.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="/QuickStart/Exercise4_CleanUp.md">
  <img align="right" alt="Next Exercise (Clean up)">
</a>
