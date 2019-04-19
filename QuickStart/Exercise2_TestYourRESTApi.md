# Exercise 2: Test your Rest API using `Postman`

## Learning Goal
After this exercise you will have a more detailed understanding on how to test a Rest API (application programming interface) of an Cloud Foundry application using `Postman` REST client.

`Postman` is a Google Chrome app for interacting with HTTP APIs. It has a friendly GUI for constructing requests and reading responses. With that exercise you will learn also some REST basics (header, body, status code). 

## Demo
- <img src="https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/Z_ReuseImages/images/information.jpg" height="20" alt="Video on video.sap.com"/> [Testing REST APIs using `Postman`](https://video.sap.com/media/1_k9t9op6j) (8 minutes)

## Prerequisite
In order to analyze JSON responses best you need to install [Postman Chrome Plugin](https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop) that helps to create and test custom HTTP requests.

## Step 0: Get familiar with the Advertisement service
As part of the last exercise you've deployed an `Advertisement` Service that provides a REST API for all CRUD operations for creating, reading, updating and deleting an Advertisement resource.

Have a look at the table below to get an overview about the REST API:

| HTTP Verb |  CRUD      | collection/unspecific (e.g. `/api/v1.0/ads/`)   | specific item (e.g. `/api/v1.0/ads/0`)|   
| ----------- | ---------- | ------------------------------------ | ------------------------------------- |
| POST        | Create     | 201 (Created), single ad, `Location` header with link to `/api/v1.0/ads/{id}` | 405 (Method not allowed) |
| GET         | Read       | 200 (OK), list of advertisements | 200 (OK), single ad; 404 (Not Found), if no advertisement with this ID exists |
| PUT         | Update     | 405 (Method not allowed)                      | 200 (OK), updated ad; 404 (Not Found), if no advertisement with this ID exists |
| DELETE      | Delete     | 204 (No Content)                              | 204 (No Content); 404 (Not Found), if no advertisement with this ID exists |

Find [here](http://www.restapitutorial.com/httpstatuscodes.html) an overview of HTTP status codes.

## Step 1: Do some REST requests 
Test the REST Service manually in the browser using the `Postman` chrome plugin. 

#### Create an advertisement resource

Select request method `POST`, enter URL: `https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com/api/v1.0/ads` to call the API, substitute d012345 with your userID. Select `Body` and `raw`. When issuing a POST request, you must provide a valid JSON body `{"title": "Advertisement 1"}`and must ensure that the application type header is set to `JSON(application/json)`. Press the `Send`button on the top right to execute the method.

```
POST-request
URL: https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com
Endpoint /api/v1.0/ads/
Body: JSON(application/json)
{"title": "Advertisement 1"}
```

For details see the screen shot: 
![Post Request using Postman](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/blob/master/CreateMicroservice/images/RestClient_PostRequest.png)
The response of your post request can be seen in the `Body` section at the bottom.

### Get all advertisements
```
GET-request
URL: https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com/api/v1.0/ads
```
Identify one advertisement id from the response for the next request.

Note: From everywhere, everybody is able to access the URL. You can easyily test that by switching to `SAP Internet` (network settings of your PC).

### Get a single advertisement
```
GET-request
URL: https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com
Endpoint /api/v1.0/ads/<id>
```
Note: Enter a valid identifier for the placeholder `id`, which you have identified in the Get all advertisements and copy the response `body`. 

### Update a single advertisement
```
PUT-request
URL: https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com
Endpoint /api/v1.0/ads/{id}

Body (json/application)
{
    ...
    "title": "some 3",
    ...
}
```
Note: Use the same `id` as before. Paste the response from the earlier get-request into the body of this request and modify the `title`. 
### Get a single advertisement
```
GET-request
URL: https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com
Endpoint /api/v1.0/ads/<id>
```
Note: Use the same `id` as before. 
Have you succeeded to change the title of the advertisement? Congratulations :-) 

## [Advanced] Step 2: Make use of environments
Create a new **Environment** with name "cloud". In that context you can specify some key-value pairs e.g. you can introduce a variable `host` with value `https://bulletinboard-ads-d012345.cfapps.sap.hana.ondemand.com`. In order to make use of the environment variable, you need to use `{{host}}` in the request URL field. 

[Reference](https://www.getpostman.com/docs/environments)
  
## Step 3: Save collection
If you use the same request regulary it is cumbersome to enter all request details manually. For this purpose you can save requests for later use as part of a so called **Collection** which you can also export and import for sharing them within your team. As part of this exercise you can create a collection, assign at least one request and export it.


[Reference](https://www.getpostman.com/docs/collections)


## References
- [Overview HTTP Status Codes](http://www.restapitutorial.com/httpstatuscodes.html)

***
<dl>
  <dd>
  <div class="footer">&copy; 2018 SAP SE</div>
  </dd>
</dl>
<hr>
<a href="/QuickStart/Exercise1_CloudFoundry.md">
  <img align="left" alt="Previous Exercise">
</a>
<a href="/QuickStart/Exercise3_KibanaLoggingDashboard.md">
  <img align="right" alt="Next Exercise">
</a>
