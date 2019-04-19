Exercise: Create table using Hana HDI
=====================================

## Learning Goal
Connect an application with a HANA database using deployment via [HDI](https://wiki.wdf.sap.corp/wiki/display/ngdb/HANA+DI) (HANA Deployment Infrastructure), which was introduced in HANA SPS11. 
HDI provides a HDI container (corresponds to a database schema) and you would use HDI for creating and deploying database artifacts consistently to it. The application itself has no `CREATE ANY` permission.

The gist of HDI is
-	define database objects in a declarative way
-	have HDI create (und update!) the objects consistently (transactional all-or-nothing, implicit dependency management)
-	support HANA-specific artifacts (calculation views, etc.)


## Prerequisites
- An account on **hanatrial** [https://account.hanatrial.ondemand.com](https://account.hanatrial.ondemand.com) (since the hdi-shared hana plan is not supported on the internal canary trial landscape ~~https://accounttrial.int.sap.hana.ondemand.com~~)
- Be familiar with using HANA on Cloud Foundry as shown [in this Exercise](Demo_HANA.md).
- Import the `solution-hana-no-hdi` branch from [Git Project statistics](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-statistics.git) as a starting point. If you already imported the project, you need to switch to the `solution-hana-no-hdi` branch as described in [Exercise 1](/CreateMicroservice/Exercise_1_GettingStarted.md).

## Step 1: Create and bind CF HANA backing service
We use the HANA service plan `hdi-shared`.

#### Creating the service
In the terminal, run the following command: `cf create-service hana hdi-shared hana-statistics`. Note that this creates a HDI container and behind the scenes several database schemas and a technical user/owner was also created in the HANA database.

If you already created this service before, delete first the application and then the service:
```
cf delete bulletinboard-statistics
cf delete-service hana-statistics
```

#### Bind service
In the `manifest.yml` file, make sure the `hana-statistics` service is bound to your application:

```
services:
 - hana-statistics
```

## Step 2: Deploy and test application

To deploy your application run in the terminal:
```
mvn clean package
cf push -n bulletinboard-statistics-d012345
```
After a successful deployment have a look at the `VCAP_SERVICES`-`hana` environment variables and find out the name of the hana schema.

Now, using a browser, send a `GET` request to   
`https://bulletinboard-statistics-d012345.[LANDSCAPE]/api/v1.0/statistics/1`.  
Notice that the error message indicates a missing table.

## Step 4: Define a table database artifact
When deploying with HDI you specify the schema objects by specifying HDI database artifacts. Each database object type has its own file and the file extension `.hdb*` controls what type of object you want to have.
For example a `*.hdbcds` file ("Core Data Services") contains entity (table) definitions. Similarly, there are `*.hdbprocedure` files for database functions, `*.hdbrole` for user roles, and `*.hdbview` for views (virtual tables).

Note: HDI supports also some new DDL-based artifacts like HDB SQL views. This means HDI allows you to manage the lifecycle and consistently deploy catalog objects, which are created via pure SQL/DDL.  

In our setting we define a table using a minimal definition file `Statistics.hdbcds`:
- For that we create a new directory named `hdi-deploy` and then create `src` folder under `hdi-deploy`. 
- Create a file `Statistics.hdbcds` under `src` folder.
```
namespace com.sap.bulletinboard;

Entity Statistics {
        key id : Integer64;
        viewCount : Integer64;
};
```
The table name derived from the deployment descriptor is `<namespace>::<entity_name>`, which is in our case `com.sap.bulletinboard::Statistics` and it needs to be put in quotes in JDBC SQL.
As this name is already configured in the Java code we do not need to update it.

A more detailed discussion is out of scope here, but on the internal GitHub you can find several examples:
- [CDS](https://github.wdf.sap.corp/search?utf8=%E2%9C%93&q=context+extension%3Ahdbcds&type=Code&ref=searchresults)
- [Procedure](https://github.wdf.sap.corp/search?utf8=%E2%9C%93&q=procedure+extension%3Ahdbprocedure&type=Code&ref=searchresults)
- [View](https://github.wdf.sap.corp/search?utf8=%E2%9C%93&q=view+extension%3Ahdbview&type=Code&ref=searchresults)

## Step 5: Create Database Deploy Service to deploy our artifacts
To actually deploy our database artifacts we need a **database deploy service** in our project, which is just an SAP supplied node.js module (`@sap/hdi-deploy`) that runs briefly after deployment and is then shut down. 

- Inside the `hdi-deploy` directory create a file named `.npmrc` with the following content specifying the registry:
```
@sap:registry=https://npm.sap.com
```

- Furthermore create a file named `package.json` (as this is a node.js service) with the following content (similar to `pom.xml`):
```
{
    "name": "deploy",
    "dependencies": {
        "@sap/hdi-deploy": "3.2.0"
    },
    "scripts": {
        "start": "node node_modules/@sap/hdi-deploy/deploy.js"
    },
    "engines": {
        "node": "6.11.2"
    }
}
```
> Note: you can get the current NPM package version of the `@sap/hdi-deploy` module available on `npm.sap.com` from [here](https://npm.dmzwdf.sap.corp/nexus/#browse/search=group%3Dsap%20AND%20name.raw%3Dhdi-deploy) (group name maps to `@sap`).

- Then create a `manifest.yml` for this database deploy service:
```
applications:
- name: bulletinboard-statistics-hanasetup
  memory: 64M
  no-route: true
  health-check-type: none
  services:
  - hana-statistics
```
> Note: Using the `no-route` argument we configure Cloud Foundry to just run the microservice without creating a HTTP(s) route for it.

- The configuration for this module, as well as the `.hdb*` files, must be contained in a `src/` subdirectory of the deploy service. So:
  - Move the `Statistics.hdbcds` file to `src/` 
  - Create a file named `.hdinamespace` with this content:
 ```
 {
     "name":      "com.sap.bulletinboard",
     "subfolder": "append"
 }
 ```
This configuration defines the starting namespace for all database objects. `Subfolder:append` option means that the folders in your project structure are part of the namespace as well.

  - Create a file named `.hdiconfig` with this content:
 ```
 {
     "file_suffixes": {
         "hdbcds": {
             "plugin_name": "com.sap.hana.di.cds",
             "plugin_version": "11.1.0"
         }
     }
 }
 ```
This configuration defines per file extension the HDI plug-in and version to be used. In our case we only need to parse the `.hdbcds` file and specify the version corresponding to [SPS 11](http://help.sap.com/hana/SAP_HANA_Developer_Guide_for_SAP_HANA_Studio_en.pdf).

## Step 6: Deploy database artifacts using HDI
To actually run the application on Cloud Foundry, you need to download/install the dependencies first.

- For that, run in the terminal (within `hdi-deploy` directory):
 ```
 npm install
 ```
With this the node modules are downloaded by the NPM package manager from the `https://npm.sap.com` SAP external NPM repository (aka registry) and are copied into the `hdi-deploy` directory. 

- Now, `cf push -n bulletinboard-hanasetup-d012345` should deploy and start the application, which creates the table if it does not exist. 
- The application may be stopped afterwards (`cf stop bulletinboard-statistics-hanasetup`).
Note that the application does not just exit, as Cloud Foundry would treat this as a crash, resulting in an automated restart.
- After the HDI setup is completed, the `bulletinboard-statistics` microservice should run as expected (even without a restart).

## Further References / Reading
- [Sample Solution: `solution-hana-hdi` branch from Statistics repository](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-statistics/tree/solution-hana-hdi)
- [SAP HANA Developer Guide for SAP HANA XS Advanced Model](http://help.sap.com/hana/SAP_HANA_Developer_Guide_for_SAP_HANA_XS_Advanced_Model_en.pdf) here you can find the list if HDI Plug-ins and Artifact Types and further details.
- [XSA Wiki: HANA Transport & Deployment](https://wiki.wdf.sap.corp/wiki/x/PoHzZ) 
- [YouTube Videos: SAP HANA XS Advanced Model in SPS 11](https://www.youtube.com/playlist?list=PLkzo92owKnVwL3AWaWVbFVrfErKkMY02a)

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="Demo_HANA.md">
  <img align="left" alt="Previous Exercise">
</a>
