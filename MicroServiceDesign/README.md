# Microservice Design - Additional Information

## Microservice Design

Designing a system based on microservices is not at all trivial and requires many more considerations than traditional system design. Currently, the most suitable design method for a microservice based system is **Domain Driven Design** which was invented by Eric Evans, possibly augmented by **Event Storming**, invented by Alberto Brandolini. 

Learning these analysis and design methods is beyond the scope of this course (there will hopefully be a separate workshop offer soon). However we want to give some pointers on where to start if you have to start NOW. 

## Domain Driven Design
### How to get started for new products (not legacy refactoring)
- Read the book **"Implementing Domain Driven Design"** by Vaughn Vernon.
- Identify the **core domain** of your application and focus your design efforts there. 
- Focus on modeling the behaviors, do not simply create a data model (ERD). 
- Identify the entities, value types, aggregates, aggregate roots, repositories etc. and the bounded contexts (see the books).
- Typically, one microservice implements what is included in one bounded context. This is much larger than only a few entities!
- Make sure your dev teams know how to do Continuous Delivery and DevOps and have the infrastructure set up for it!

**The biggest danger in starting with microservices is to create too many small microservices!!!**

Therefore, the standard advice when you start is: Start with a monolith!

### How to get started to 'carve out microservices from existing monoliths'
- All parts that are caraved out must satisfy the 'microservice criteria'
- Make sure you have a clear reason to carve out a piece. This is usually 
  - Scalability: One part of the system needs much more scalability (usually for 'read')
  - Innovation speed: One part of the system needs a lot higher speed in updates than the monolith can support
  - You need different technologies (language, runtime, persistence services) than the monolith for the part
- Suggested steps
  - Separate the data on database level first (identify what exactly the carved out microservice needs)
  - Then separate the code into a separate service
  - It may be cheaper to rewrite a part than to port old code
- When you have extreme scalability, consider CQRS

### Finally: If you can, get a coach to do a DDD modeling workshop for you. (contact: Juergen Heymann)


### Core Resources (to start)
- [Martin Fowler's overview article on Microservice Architecture ](http://martinfowler.com/articles/microservices.html)
- Get the book: **"Implementing Domain Driven Design"** by Vaughn Vernon. 
- **The article [DDD Example](https://www.mirkosertic.de/blog/2013/04/domain-driven-design-example/) is a good introduction to the thinking process of DDD.**

### Additional Material
- [Microservice architecture pattern description](http://microservices.io/patterns/microservices.html) is an interesting entry point also considering the broader question of scaling approaches and the [scaling cube](http://microservices.io/articles/scalecube.html)
- [Examples of SAP CP (Neo) / YaaS Business Services ](http://diginomica.com/2015/09/02/new-business-services-come-to-sap-hcp-weakening-the-iaaspaas-distinctions/) gives you some examples for business oriented services and their granularity
- [Adopting microservices at Netflix](https://www.nginx.com/blog/microservices-at-netflix-architectural-best-practices/) is a very interesting article with references to videos and other resources. It also gives good guidelines for MS design.
- [7 Microservice Antipatterns](http://www.infoq.com/articles/seven-uservices-antipatterns) which describes some prerequistes and some pitfalls to avoid
- http://infoq.com/domain-driven-design
- http://domainlanguage.com
-	http://www.martinfowler.com/bliki/AnemicDomainModel.html 



## Code Reuse: Library versus separate microservice?

One consideration that is also often discussed is code reuse. When do you accept code duplication, e.g. a copy of the same lib in each microservice, and when do you want to have only one copy in a single microservice?  The main points to consider are:
* In general DRY (don't-repeat-yourself) is a good rule to keep to avoid code duplication.
* But it is clearly OK and necessary to have infrastructure type libraries such as logging, hystrix, ... in each microservice since they are the same in each microservice (and have to be).
* You should have business logic that works on business data only in one place. This should mean that the business data is part of one microservice and of course it has its own private data and the business logic together in the same microservice. They should also change infrequently.
* Bottom line: **Adhere to DRY within microservices and be relaxed about it between microservices. **

You can find more on this topic in the book "Building Microservices" by Sam Newman (page 59) and several 
