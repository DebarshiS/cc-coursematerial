Exercise 2: Deploy Microservice on Cloud Foundry
=======================================
Get familiar with the basic commands of the Cloud Foundry CLI, learn how to deploy your microservice into Cloud Foundry.

## Prerequisite
You should have an account on any Cloud Foundry instance. Take a look at the [CF @SAP CP help page](https://help.cf.sap.hana.ondemand.com/). This is your entry point to request a trial account users, get help etc.

## Step 1: Login
The following commands will setup your environment to use the provided Cloud Foundry instance.

 - `cf api https://api.cf.sap.hana.ondemand.com`
 - `cf login` 
   - Enter your SAP email; use your domain password
   - Select your `D012345trial_trial` organization and your `dev` space (from now on, always replace `d012345` by your user id)

## Step 2: Create `manifest.yml`
In the root directory of your project, create a new file named `manifest.yml` and fill it with the following data:

```
---
applications:
- name: weather
  memory: 1G
  path: target/weather-0.0.1-SNAPSHOT.jar
  buildpack: sap_java_buildpack
  env:
      # Use the non-blocking /dev/urandom instead of the default to generate random numbers.
      # This may help with slow startup times, especially when using Spring Boot.
      JAVA_OPTS: -Djava.security.egd=file:///dev/./urandom
      # see https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Knowledge/JavaMemoryAllocationInCF.md
      MALLOC_ARENA_MAX: 4
      JBP_CONFIG_OPEN_JDK_JRE: '[memory_calculator: {stack_threads: 100, memory_sizes: {native: 220m..}}]'
```

For a more detailed discussion of the memory settings have a look at [Java Memory Allocation in Cloud Foundry
](../Knowledge/JavaMemoryAllocationInCF.md).

## Step 3: Push your service
- Before you push your service into the cloud, make sure to build the JAR file (`mvn clean verify`). 

- The name `weather` specified in the manifest file is used as hostname and is already used in this CF instance. With this in mind, push your microservice using an unique hostname:
  ```
  cf push -n weather-d012345
  ```
  Make sure the execution is successful.
- Open the URL `https://weather-d012345.cfapps.sap.hana.ondemand.com/health` in the Browser or in `Postman` to test whether your microservice runs in the cloud. Notice that the `d012345` needs to be replaced accordingly. `Postman` requires also the `https` protocol.

## Step 4: Scale your service
Currently we only run one instance of the microservice.
Run `cf scale weather -i 2` to scale your microservice to two instances, so that the load is spread and a single crash is less harmful.

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="Exercise_1_SpringBoot_GettingStarted.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="Exercise_3_SpringBoot_CreateWeatherService.md">
  <img align="right" alt="Next Exercise">
</a>
