Exercise 6: Deploy Ads on Cloud Foundry
=======================================
## Learning Goal
Get familiar with the basic commands of the Cloud Foundry CLI, learn how to deploy your advertisement service into the cloud, and understand how microservices are managed.

## Prerequisite
Continue with your solution of the last exercise. If this does not work, you can checkout the branch [origin/solution-5-ValidationExceptions](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc/tree/solution-5-ValidationExceptions).

Ensure that you've created your own trial space on the Cloud Foundry as described as part of the [Course Prerequisites](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/CoursePrerequisites/README.md):

- Create your own **Trial Account and Space** on the Cloud Foundry system using the [**self-service**](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview) (click the button **Start Cloud Foundry Trial** and select the Europe/Frankfurt region). For login, use your domain user and password. Further information you can get from the [**Getting Started with Cloud Foundry** help page](https://help.sap.com/viewer/65de2977205c403bbc107264b8eccf4b/Cloud/en-US/b8ee7894fe0b4df5b78f61dd1ac178ee.html). 
- You can optionally join the [CF users mailing list](https://listserv.sap.corp/mailman/listinfo/cf.users) for questions, answers and discussions regarding SAP CP Cloud Foundry.

## Step 1: Login
The following commands will setup your environment to use the provided Cloud Foundry instance.

 - `cf api https://api.cf.sap.hana.ondemand.com`
 - `cf login -u d012345` (from now on, always replace `d012345` by your user id; use your domain password)
 - In case you are assigned to multiple orgs, select the `D012345trial_trial` organisation.

## Step 2: Create `manifest.yml`
In the root directory of your project, create a new file named `manifest.yml` and fill it with the following data:

```
---
applications:
- name: bulletinboard-ads
  memory: 1G
  timeout: 360
  path: target/bulletinboard-ads.war
  buildpack: https://github.com/cloudfoundry/java-buildpack.git#v4.6
  env:
      # Use the non-blocking /dev/urandom instead of the default to generate random numbers.
      # This may help with slow startup times, especially when using Spring Boot.
      JAVA_OPTS: -Djava.security.egd=file:///dev/./urandom
```
Note: In case you make use of the Community Java Buildpack it is recommended to specify the **version of the buildpack** e.g. `buildpack: https://github.com/cloudfoundry/java-buildpack.git#v4.6`. You can get the current version using `cf buildpacks` and on Github there must be a so-called `release` for every released buildpack version.

## Step 3: Push your service
- Before you push your service into the cloud, make sure to build the WAR file (`mvn clean verify`). 

- The name `bulletinboard-ads` specified in the manifest file is used as hostname and is already used in this CF instance. With this in mind, push your microservice using another hostname:
  ```
  cf push -n bulletinboard-ads-d012345
  ```
  Make sure the execution is successful.
- Using a browser and the `Postman` REST client test whether your microservice runs in the cloud.
For this use the URL `https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com/api/v1/ads/`.

Note: In order to build the WAR file without running the tests, you can use `mvn clean package -DskipTests`.

## Step 4: Scale your service
Currently we only run one instance of the microservice.
Run `cf scale bulletinboard-ads -i 2` to scale your microservice to two instances, so that the load is spread and a single crash is less harmful.

Manually create and retrieve advertisements and observe the responses. You might recognize that you get different responses depending on the service instance you are talking to. Each service instance runs in a fully separated process. In our current example, the hash maps are not in sync.

> Note:
> When you deploy your application into your Cloud Foundry `trial` subaccount then you're limited to **2GB memory**. In  order to monitor the quota you need to open the [SAP CP Cockpit](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview), navigate into your `trial` subaccount e.g. by using the `Go to Cloud Foundry trial` button.

## [Optional] Step 5: Explore the SAP Cockpit 

Open the [SAP CP Cockpit](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview). Note that this SAP Cockpit shows you only SAP internal Cloud Platform offerings.
- Navigate first into your **Trial Global Account** and find out how much memory (in GByte) is assigned to it and which kind of services you are allowed use.
- Then navigate into your `trial` **Subbaccount** and find out how much of the memory you have already consumed by the applications deployed  in all of your Cloud Foundry spaces.
- Now navigate into your `dev` Cloud Foundry **Space** and make sure that only one single application instance is running. 
- Finally assign a colleague in the role of an `Auditor` to your space and let them check, whether they see the space as well in its Cockpit.

![](/CloudFoundryBasics/images/SAPCockpit.png) 

## [Optional] Step 6: Add heartbeat URL to the Application Manifest
There are various attributes that can be used to configure the deployment of your application, which are documented [here](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).  

For example you can configure the health check in such a way that it considers the application as healthy, when the `health` endpoint returns HTTP `200` status within 1 second. For this you need to specify the following attributes in your `manifest.yml`:

```
---
applications:
- name: bulletinboard-ads
  health-check-type: http
  health-check-http-endpoint: /health
```
Note: By default the health check tries to establish a TCP connection to an application port within 1 second.  

Now deploy your application again and make sure that it starts and does not crash. In case you face a Server error when deploying your application similar to `Server error, status code: 400, error code: 100001, message: The app is invalid: health_check_http_endpoint HTTP health check endpoint is not a valid URI path:`: Check the version of your Cloud Foundry CLI version using `cf --version` and make sure that it is **>=6.27.0**. You can upgrade the version as documented [here](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

Note also that the `health` endpoint remains accessible even after introduction of authentication and authorization checks as part of **[Exercise 24](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Security/Exercise_24_MakeYourApplicationSecure.md)**.

## Used Frameworks and Tools
- [Cloud Foundry CLI](https://github.com/cloudfoundry/cli)
- [Postman REST Client (Chrome Plugin)](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop)
- [Community Java Buildpack](https://github.com/cloudfoundry/java-buildpack)
- [SAP CP Cockpit](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview)

## Further Reading
- [Cloud Foundry CheatSheet](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/Cheat_Sheets/CS_Merged.pdf)
- [SAP CP documentation](https://help.cf.sap.hana.ondemand.com/)
- [Cloud Foundry documentation: Deploying with Application Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html)
- [Cloud Foundry documentation: Troubleshooting Application Deployment](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html)
- [https://wiki.wdf.sap.corp/wiki/display/xs2/Secure+delivery+of+Node.js+applications](XS2 wiki: Secure delivery of Node.js applications)
- [Cloud Foundry documentation: Community Buildpacks](https://docs.cloudfoundry.org/buildpacks/)
- [SAP Java Buildpack](https://wiki.wdf.sap.corp/wiki/display/xs2java/SAP+Java+Buildack+for+Cloud+Foundry).

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="/CreateMicroservice/Exercise_5_ValidationAndExceptions.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="/ConnectDatabase/Exercise_7_ConnectLocalDatabase.md">
  <img align="right" alt="Next Exercise">
</a>
