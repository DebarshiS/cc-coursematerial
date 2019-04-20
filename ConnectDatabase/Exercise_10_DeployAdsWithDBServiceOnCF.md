Exercise 10: Deploy Ads on Cloud Foundry
=======================================
## Learning Goal
Get familiar with the service related commands of the Cloud Foundry CLI, learn how to bind your application to a Cloud Foundry service.

The task is to get the Advertisement service including the persistency running on Cloud Foundry. Therefore the deployed application must be bound to a PostgreSQL service, offered by Cloud Foundry.

## Prerequisite
Continue with your solution of the last exercise. If this does not work, you can checkout the branch [`origin/solution-9-Implement-JPA-Entity`](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc/tree/solution-9-Implement-JPA-Entity).

## Step 1: Create CF PostgreSQL Service
Create on Cloud Foundry a service instance with name `postgres-bulletinboard-ads`. 

```
cf create-service postgresql v9.4-dev postgres-bulletinboard-ads
```

Note: You can get the exact names of the available services and its plans in the Service Marketplace (`cf marketplace`). Here we have selected the service plan `v9.4-dev` for the `postgresql` service as this is a *less expensive* offering as you can also analyze in the [**CP Cockpit**](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview).

Furthermore note that the created backing service is only *available* within the current targeted space and can be bound only to the applications within the same space.

## Step 2: Update manifest.yml
Add the name of your postgres service (as defined in the previous step) to your `manifest.yml`. This will bind your application to the service.

Make sure you specify the service entry in context of your application configuration, i.e. place it with the correct indentation.

```
---
applications:
- name: bulletinboard-ads
  ...
  services:
  - postgres-bulletinboard-ads
```

## Step 3: Push your Service
Now you can push your application again as described in [Exercise 6](../CloudFoundryBasics/Exercise_6_DeployAdsOnCloudFoundry.md).

This causes Cloud Foundry to provide a new entry in the environment variable `VCAP_SERVICES` that contains connection and credentials information needed to connect to the database. You can view these values with `cf env bulletinboard-ads`.

After a successful deployment check using `cf services`, whether your `postgres-bulletinboard-ads` service instance is bound to your CF application. If this is the case you can test your application using `Postman`. 

Optionally you can check what happens with your persisted data if you stop or even delete your CF application.

## Used Frameworks and Tools
- [Cloud Foundry CLI](https://github.com/cloudfoundry/cli)
- [Postman REST Client (Chrome Plugin)](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop)

## Further Reading
- [Cloud Foundry CheatSheet](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/Cheat_Sheets/CS_Merged.pdf)

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="/ConnectDatabase/Exercise_9_ImplementJPAEntity.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="/ConnectDatabase/Exercise_10_2_ConnectBackingService.md">
  <img align="right" alt="Next Exercise">
</a>
