# Exercise 1: Cloud Foundry as a PaaS (Platform as a Service)

## Learning Goal
After this exercise you will have a more detailed understanding about basic concepts & tools in Cloud Foundry and you will have successfully deployed an application on Cloud Foundry.

Get familiar with **[SAP Cloud Platform Cockpit for Cloud Foundry](https://help.cf.sap.hana.ondemand.com/frameset.htm?7bc6369a68b14833bdb741a12141d70a.html#loio3527b8af78814cbdbd719cb7f7bca1d6) (CF Cockpit)** as well as with the **Cloud Foundry Command Line Interface (CF CLI)**, which you will use to run basic commands e.g. to deploy a single Java application (aka microservice) to **Cloud Foundry (CF)**


## Demo
- <img src="https://github.com/ccjavadev/cc-coursematerial/blob/master/Z_ReuseImages/images/information.jpg" height="20" alt="Video on video.sap.com"/> [Cloud Foundry Demo (CF Cockpit and CLI)](https://video.sap.com/media/t/1_74uuo41d) (25 minutes)

## Prerequisite Steps
### Request Trial Space on Cloud Foundry
Get a Trial Space on the Cloud Foundry Instance, download and install Cloud Foundry Command Line Interface (CF CLI client) as described here as part of the [Getting Started](https://help.cf.sap.hana.ondemand.com/frameset.htm?b8ee7894fe0b4df5b78f61dd1ac178ee.html) section. Now a space has been created for your SAP user id in Cloud Foundry organization **trial**. 

### Download Java application
Download a sample Java application `bulletinboard-ads ` from [here](https://github.com/ccjavadev/cc-coursematerial/blob/master/QuickStart/bulletinboard-ads.war), which is packaged as **w**eb **ar**chive (war file). Store the .war file locally (remember the path to the file as you need this for a later step). Note that this Java application is a microservice for managing `Adertisements` and is part of a `Bulletinboard` business application. 

### Set environment variables (Windows)
Open the Command Prompt (cmd) via Windows Start Bar and enter the following commands in order to define the proxy settings to use the provided Cloud Foundry Command Line interface.

```
setx HTTP_PROXY http://proxy.wdf.sap.corp:8080
setx HTTPS_PROXY http://proxy.wdf.sap.corp:8080
```
**Note**: You need to close command line and open it again before the changes take effect.

### Set environment variables (Mac)
Open the Terminal and do the following setps in order to define the proxy settings to use the provided Cloud Foundry Command Line interface.

Edit `.bash_profile` to set proxies in terminal with the following commands:
```
touch ~/.bash_profile
open ~/.bash_profile
``` 
And include the two commands in your `.bash_profile`:
```
export HTTP_PROXY=http://proxy.wdf.sap.corp:8080
export HTTPS_PROXY=http://proxy.wdf.sap.corp:8080
```
Save the bash_profile file and quit the text edit. **Note**: You also need to close command line and open it again before the changes take effect.

## General Hints
- You are going to need the [CF Cheatsheet](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/Cheat_Sheets/CS_Merged.pdf).
- In the terminal you can always make use of the CF CLI help. Just type `cf help` from the command line to see all cf commands, and `cf help <command>` to see the description and usage details of a particular command.

## Step 1: Familiarize yourself with the CF Cockpit
- Open the [CF Cockpit](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview), login with your SAP credentials and try to navigate to your `Cloud Foundry trial` **space** e.g. `dev`, which is created as part of your `D012345trial` global account (from now on replace `D012345` by your SAP user id).
- Have a look at the navigation bar, here you find under `Services` the `Service Marketplace`. This gives you a great overview about the services that are available on Cloud Foundry. You dig into the particular `PostgreSQL`, which is a SQL database service, to see which plans are offered. Find the one, which requests the least memory resources.


## Step 2: Login via Command Line Interface (CLI)
Open the Command Prompt (cmd) via Windows Start Bar (Windows) or Terminal (Mac) and enter the following commands in order to setup your environment to use the provided Cloud Foundry instance.

- `cf api https://api.cf.sap.hana.ondemand.com` to target the Cloud Foundry instance ( in the Canary landscape)
- `cf login -u d012345` (from now on, always replace `d012345` by your user id; use your SAP global domain password)
- In case you are assigned to multiple spaces, select your trial organization.


## Step 3: Create `manifest.yml` as deployment descriptor
A common practice when deploying an application to Cloud Foundry is to manifest the concrete parameters in a deployment descriptor file named `manifest.yml`. It automates deployment, makes deployment reproducable and avoids manual errors. 

In the directory of the downloaded war-file as you remember from prerequisite step 'Download Java application', create a new file named `manifest.yml` using Wordpad or Notepad and fill it with the following data:

```
---
applications:
- name: bulletinboard-ads
  memory: 1G
  instances: 1
  path: bulletinboard-ads.war
  buildpack: sap_java_buildpack
  services:
  - postgres-bulletinboard-ads
```

The `manifest.yml` is also called the **Cloud Foundry deployment descriptor**. It provides Cloud Foundry information about the application (in the above it is application: bulletinboard-ads) that should be uploaded and deployed. It also specifies how much `memory` is assigned to the application (in the above exammple this is 1 Gigabyte) and how many instances are created. Information on where to find the `buildpack` that the application requires is also supplied. Please note: buildpacks provide framework and runtime support for your application. The `manifest.yml` also defines which `services` the application requires (in the above it is a postgres service, which is an open source data management service). For more information please read about Application Manifests [here](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).


## Step 4: Create a `PostgreSQL` database service as specified in the manifest

The `manifest.yml` file specifies that the application requires a service with name `postgres-bulletinboard-ads`. 
Enter the following command in the terminal to create a `PostgreSQL` service instance with name `postgres-bulletinboard-ads`, which is only visible within your CF space.
```
cf create-service postgresql v9.4-dev postgres-bulletinboard-ads
```
Note: You can list all available services and its plans in your organization (e.g. `D012345trial_trial`) for your space (`dev`) in the Service Marketplace (command `cf marketplace`). Here we have selected the service plan `v9.4-dev` for the `postgresql` service as this is a *less expensive* offering as you have analyzed in **Step 1**. 

## Step 5: Deploy your application
In the root directory of the downloaded war-file, you can now deploy the `bulletinboard-ads.war` application to Cloud Foundry using the `manifest.yml` as deployment descriptor (see **Step 3**). For this you need to change the directory in the command line to the directory where you stored the manifest.yml (use command `cd <directory name>` to change to the respective directory).

Push the application with a unique **(host) name**. **Hint:** replace `<place-holder>` accordingly.
```
cf push -n bulletinboard-ads-<d012345>
```

### Some Explanations
- The url of your application consists of `host name` + `domain`. The `domain` is fixed, so `host name` needs to be unique within the Cloud Foundry instance. If no host name is specified the application name specified in the **manifest.yml** is taken.

- As specified in the `manifest.yml`, this will bind your application to the `postgresql` service created in the previous step.   
In detail that means that Cloud Foundry provides information to any application instance, so that the application knows how to connect to the `postgresql` database. The information is provided to application as a system `Ennvironment Variable`.

### Make sure the execution is successful
- Open again the [CF Cockpit](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview), make sure that you are still within your trial space. 
- Then select `Applications` in the navigation bar and ensure that `bulletinboard-ads` application is shown with state `started`. 
- Select the application and open the `Application Route`. Open the application route link `bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com` to open the URL: `https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com/` in your browser. You should get response `ok`. In addition you can enhance the URL by `/health` to do a little smoke test. If your application is running, you should get response `{"status":"UP"}`.
- Optionally you can also have a look at the `Environment Variables` to check whether the `VCAP_SERVICES` variable contains connection information for the `postgresql` service.


## Step 6: Scale your application
Currently we only run one instance of the microservice. To validate this go the command line and enter `cf apps`. You should see that for your application `bulletinboard-ads` only one instance is running.
Enter the `cf scale bulletinboard-ads -i 2` command to scale your microservice to two instances, so that the load is spread and a single crash is less harmful as each application instance runs in a fully separated process. Check with command `cf apps` that now two instances are running. 

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="/QuickStart/Readme.md">
  <img align="left" alt="Overview">
</a>
<a href="/QuickStart/Exercise2_TestYourRESTApi.md">
  <img align="right" alt="Next Exercise">
</a>
