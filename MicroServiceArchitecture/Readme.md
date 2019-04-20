# Microservice Architecture - Detail Notes

This page contains further notes, discussions and links on the topic of Microservices.


## Microservices Design Considerations

### 12 factors

The '12 factor app' describes a set of **rules that microservices must adhere to** so they can be developed, deployed and operated nicely in a cloud context. They are describe in detail at [12factor.net](http://12factor.net).

### Some design aspects of Microservices

* Goal: Microservices do not share database tables, no joins in DB. Read more about data layer APIs in the [whitepaper: Further Guidance on How to Apply Microservices at SAP](https://documents.wdf.sap.corp/share/proxy/alfresco/api/node/content/workspace/SpacesStore/2988a5a0-fe35-4112-9ca4-af337c0350ad/Further%20Guidance%20on%20How%20to%20Apply%20Microservices%20at%20SAP.pdf?a=true)
* Many cloud apps started as monoliths with pieces extracted to microservices over time as needed for scalability, resilience or for other business benefits
* When developing a new app, start with a larger microservice until the logical boundaries have stabilized, then extract.
* Design microservices using the Bounded Context design method and following the Single-Responsibility-Principle in design
* Driver of transition to microservices is scalability, uptime >99% and developer productivity.
* Tight coupling slows down the innovation cycle since a new version of the entire app needs to be developed, tested and deployed as a whole.
* This whitepaper is to provide knowledge and guidance on the micorservice architectural style: [Microservices - Concept, Trade-offs, Guidance](https://documents.wdf.sap.corp/share/proxy/alfresco//api/node/content/workspace/SpacesStore/8d453f64-655d-4a88-8925-24ed16845aa0/Microservices%20CTO%20Circle%20final.pdf).

For more details and guidance see the [Microservice Design](../MicroserviceDesign/readme.md) chapter. 


## An more complex application example 

The picture below shows a more complex microservice application example (high level) in the domain of ecommerce. There are many huge systems that are basically structured this way. 

[<img src="https://github.com/ccjavadev/cc-coursematerial/blob/master/MicroServiceArchitecture/images/MSLargeExample.png" height="350" alt="More complex example"/>]()

#### Comments
- All requests from mobile devices or browsers come through the router to the application.
- There is a `user mgt` component that manages user authentication.
- The `Landing Page` is the first page the user sees. This is often implemented in a specialized service that is very fast.
- `Static content` (static html, css, ... resources) is always served from the webserver level, directly from the file system or cache. 

Then there are many services that could all have REST endpoints that either deliver JSON or HTML (fragments). Things that are usually seperated are e.g.
- **Search**: highly specialized service for product search. Needs to be basically 'all in memory' to be fast enough. The data structures are usually not SQL on the DB.
- **Recommendations** is another typical service related to product discovery. Often, this is implemented on a graph DB.
- **Product Info** is usually just data (JSON) that is assembled in the front-end with pictures (from the `media` service). Persistence can be in SQL but also in a document DB.
- The **media** service service pictures and videos etc. that are large blobs. They are usually written in node.js and not in java since that is much more efficient that way. 
- ... and you can see the other services that each have their special role and behaviors.

Note that all services **scale independently and automatically**, have their **own DB and specialized tools**, and for a global system, the services are also **globally distributed and replicated**. 


## FAQ

In this file we want to collect and try to answer typical questions around microservice architecture -
especially the critical questions. This page is always 'work in progress'.

#### Q: Since you have to partition data anyway for scaling, why is ‘many SAP systems side by side’ (like HEC) not enough?

One naive approach to scalability could be to simply give each customer their own system / instance or maybe put a few customers in one system, a few more in the next and so on. Why is this not enough?
* If you partition on system level, TCO is much too high since you have to scale everything in huge granularity. Instead you want a tenant without data to basically cost nothing. Operations TCO and hardware requirements are the main cost driver that decide if you can make money at all in the cloud.
* You do not want hundreds / thousands of servers each with their own OS and application software version. Instead you want all your servers for that app to appear as one application. This is also a TCO argument.
* How you can scale also depends a lot on what the scope of data is that needs to see each other. Companies as customers, or a site like shopify for webshops are easier to scale 'by customer' since their data is usually totally separate (and needs to be!). This is much different from e.g. Facebook or LinkedIn where each person potentially can know any other person anywhere in the world and there is no natural data partitioning scheme.
* Certain types of scalability and algorithms do not partition on keys (e.g. customer ID) but require a totally different way of programming. Example: A google search request triggers tens or hundreds of requests to other services that hold partial results. This is not request data partitioning but ‘result partitioning’.


#### Q: How can facebook ship twice a day when they are a monolith?
* First of all: Only the rendering part is a monolith and all backing and infrastructure services are separate and they are also separately updated. Backing services are e.g. authentication, pictures ('haystack'), messaging, chat, data storage etc.
* All presentation logic of all logical components is in the presentation server and therefore part of this 'large update' but they are very well separated so that each component UI is pretty much independent from all the others.
* The presentation server is stateless and they have 60000 servers!
* There is very high test automation and a rigorous focus on code reviews.
* They have invested extremely into automating all build+test+deploy related tools and therefore this process is very stable.

#### Q: What are the dominant factors that drive microservice architecture?

* Linear scale out to thousands of servers; elasticity = automated scaling according to load
* Cheap resilience (instead of doubling the whole landscape)
* Zero downtime deployments
* Low TCO (per customer/user)

#### Q: What does the CAP Theorem mean and imply?

The CAP theorem was stated and proven by Eric Brewer. For a good description an updated interpretation see the followup article by Eric Brewer himself [CAP Twelce Years later](https://www.infoq.com/articles/cap-twelve-years-later-how-the-rules-have-changed).

See also the [NoSQL Guidance](https://documents.wdf.sap.corp/share/proxy/alfresco/api/node/content/workspace/SpacesStore/4fae26ec-b6b8-4ff0-8b81-742f597b73a6/CTO%20Circle%20-%20NoSQL%20Guidance%20-%20final.pdf?a=true) paper by SAP's CTO Circle. 


#### Q: Doesn’t microservice architecture drive back into component teams?

* A microservice is almost always owned by just one team. This means they own all layers from persistence to UI. This in effect is a feature team for that topic that the microservice covers.
* Services are designed around business capabilities, not layers or technical boundaries. This means that teams (and their POs) are usually business domain experts, i.e. they cover multiple features inside a business domain. This is different from a 'generic feature team approach' where all teams pull from the same product backlog and each team is suppoed to be able to cover all epic level topics. However, teams structure defined by business domain expertise is considered the best compromise.
Thus, microservices actually promotes the feature team approach.


#### Q: What is the difference between SOA and Microservices?

SOA and Microservices are related but Microservices are a subset of SOA. SOA means many things to many people. The table below would be disputed by some. But generally speaking, microservices have stricter conditions. Some differences:

Topic | SOA | Microservices
----------- |  ---------- | ------------------
State  | often stateful |  stateless
Messaging type  | Smart enterprise service bus  |  dumb and fast
Communication  | synchronous  |  asynchronous
Database  | large relational | small DBs, also NoSQL
System evolution  | evolve services |  immmutable services
System change  | modify the monolith  |  add new services
System scaling  | optimize the monolith |  add more services


## Further References
- [CTO Circle: Internal Whitepaper](https://jam4.sapjam.com/wiki/show/eBIJTH4EwfD15ymE2nv2pG) 
- [Microservice@SAP Jam Group](https://jam4.sapjam.com/groups/w12lqZCV3pTdERnuIUMcBO/overview_page/136843)
- [Martin Fowler on Microservices](https://jam4.sapjam.com/blogs/show/spPIuI94GYS4rtjCPWttrq) at SAP (blog post and video)
- [12factor.net](http://12factor.net)
