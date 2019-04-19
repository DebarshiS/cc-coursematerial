# User Provided Service (Cloud Foundry)

Cloud Foundry offers a set of services that you can bind to in your application. But sometimes you need to also integrate with / use a services that is hosted outside of Cloud Foundry. This could be e.g. a special log analysis services within your company or even an external service like 'Credit Check' that is hosted by a third-party. 

In these cases you want to 
* avoid having to hard-code access information to these services in your code, which means 
* provide the connection information to the service in the same way as the predefined services, i.e. access them via `VCAP_SERVICES`.

To support this, Cloud Foundry lets you define a **User Provided Service**. This is basically a parameter structure (name-value pairs, possibly hierarchical) that simply contains the access information to the remote service. Then the service appears in the same way as all others when you enter the `cf s` command.

Details / HOWTO can be found [here](https://docs.pivotal.io/pivotalcf/devguide/services/user-provided.html).

# Example

## How the service is created
In this example we create the service parameters (fictitious publish-subscribe message service 'pubsub') interactively by specifying the names of the parameters and entering the values at the prompts. 
```
$ cf cups pubsub -p "host, port, url, username, password"

host> pubsub01.example.com
port> 1234
url> pubsub-example.com
username> pubsubuser
password> XXXX

Creating user provided service pubsub in org my-org / space development as a.user@example.com...
OK
```

## How the service appears in CF Services
```
$ cf s

name                        service             plan            bound apps
postgres-bulletinboard-ads  postgresql          v9.4-dev  bulletinboard-ads
pubsub                      user-provided
```

## See User Defined Services in ENV
After binding the service to an application and restarting it, you see it in `VCAP_SERVICES`:

```
$ cf env bulletinboard-ads

System-Provided:
{
 "VCAP_SERVICES": {
  "postgresql": [
   ...
 ],
   "user-provided": [
   {
    "credentials": {
     "host": "pubsub01.example.com",
     "password": "XXXX",
     "port": "1234",
     "url": "pubsub-example.com",
     "username": "pubsubuser"
    },
    "label": "user-provided",
    "name": "pubsub",
    "syslog_drain_url": "",
    "tags": []
   }
  ]
 }
}
```
