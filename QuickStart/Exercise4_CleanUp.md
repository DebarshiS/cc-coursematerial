# Exercise 4: Clean Up after you are done with the exercises

## Learning Goal
Avoid generating costs without benefit.

## Step 0: Login

Open the Command Prompt (cmd) via Windows Start Bar (Windows) or Terminal (Mac) and enter the following commands in order to logon to Cloud Foundry instance.

- `cf api https://api.cf.sap.hana.ondemand.com` to target the Cloud Foundry instance ( in the Canary landscape)
- `cf login -u d012345`  (replace  d012345  by your user id; use your SAP global domain password)
- In case you are assigned to multiple spaces, select the  trial organisation.

## Step 1: Delete the application in your trial
- Via `cf apps`you can find the name of the application you deployed.
- `cf delete bulletinboard-ads` to delete the deployed application (bulletinboard-ads should be the name of your application).

## Step 2: Delete postgres service

- Via `cf services` you can find the name of all running services.
- `cf delete-service postgres-bulletinboard-ads`to delete the postgres service.

## Thank you again for saving unnecessary costs.

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="/QuickStart/Exercise4_CleanUp.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="/QuickStart/Readme.md">
  <img align="right" alt="Overview">
</a>
