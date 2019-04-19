# Questions from the classroom-trainings:

## Logging

### Question
Is it possible to consolidate the logging levels of an application into the same tenant to which the corresponding logging messages belong to?

### Answer
The tenant-id, respectively subaccount, is part of the url to which the request was sent. The approuter is able to identify the tenant-id according to the tenant-host pattern configured in the manifest of the business application. Approuter sends the tenant-id to XSUAA. XSUAA includes the tenant-id when it issues the access token (JWT). XSUAA delivers the JWT to the approuter upon its request (towards XSUAA). The approuter always enriches client requests with the JWT before they are forwarded to the requested endpoints of the business application.

The microservices of the business application can query the JWT for the id of the tenant which sent the request. For logging purposes, it is always possible to utilize a custom field to store the tenant-id and group the logging-messages in the monitoring tool by this custom field.

### Question
Do logging retention periods collide with data-privacy requirements?

### Answer
Logging-Services plan to offer different service-plans with different retention periods. Consumers can then select a plan which adhere to their specific data-privacy requirements.

> Currently the retention period is a landscape specific setting which is set by operators of a landscape and is commonly 7 days.

## Security

### Question
Is it possible to configure trust for the JWT in service to service communication across CF landscapes (e.g. AWS Canary to Siemens Industry Cloud)?

### Answer
Yes, provided that both landscapes run XSUAA versions which are compatible to one another and that the called app/service uses an XSA Container Security API wich is compatible to that one the calling app/service is using. Given that, App2App calls should also work accross Cloud Foundry landscapes, as described in [Integration Scenarios](https://jam4.sapjam.com/groups/DRuoC97ApSanbbXx20g4kb/overview_page/tZSANTJpf4SKvN5UHrMPvV).

## REST

### Question
What does "stateless communication" really mean with respect to the client and the server of a web application?

### Answer
Stateless communication does not imply that an application is not allowed to produce and hold state. But, REST does not allow the server to hold client specific state with a lifetime exceeding the lifetime of the client request.

REST does allow the server to hold state if the state can be represented as a resource. If the server holds a shopping cart of a client as a resource, the particular shopping cart does not need to be connected to a specific session id and can be accessed later via the hyper-link pointing to the resource. The hyper-link - representing the shopping cart resource - can also be bookmarked or sent via e-mail.

The client of RESTful web applications is allowed to hold state. The client state does not necessarily need to be represented as a ressource on the client side.

Conclusion: Either hold all state on the client side or represent server state as a resource.

## Buildpacks

### Question
Can parameters be set for the buildpack when pushing an application?

### Answer
The buildpack is configured by the ```.yml``` files located in the ```/config``` directory of the buildpack. You can override the buildpack configuration by environment variables with names matching those names of the configuration files you wish to override minus the ```.yml``` extension plus the prefix ```JBP_CONFIG```. The value of the environment variable must be a valid inline yaml.

The environment variables can be set with the following command:
```
$ cf set-env <my-app> JBP_CONFIG_<name_of_config_file_without_.yml_extension> ...
```
The app needs to be at least restaged (to trigger the buildpack run) or pushed again. You can also set the environment variables in section ```env:``` of the corresponding ```manifest.yml```.

It is not possible to add completely new configuration properties. Properties with nil or empty values will be ignored by the buildpack. See also section [Configuration and Extension, in the documentation of the Cloud Foundry Java Buildpack](https://github.com/cloudfoundry/java-buildpack#additional-documentation)

## Multitenancy

### Question
Can you give me an example for an endpoint my microservices would need to provide in the event that a new tenant subscribes to my application?

### Answer
An example can be found on in section **_How to Provide Multitenant Applications_** of [concept paper Multitenancy for SAP CP CF](https://wiki.wdf.sap.corp/wiki/display/IoTArch/Multitenancy?preview=/1850370042/1850370323/Multitenancy%20for%20HCP%20CF%20-%20Concept%20Paper.pdf): Your microservices will most probably depend on other microservices and subscriptions to your application will also need to trigger subscriptions to all dependencies as well. Your own microservices will therefore need to provide a well-known endpoint, so that **_Commercial Infrastructure Services_** can collect your dependencies and report them to XSUAA, in order to have all necessary OAuth2 clients created.

