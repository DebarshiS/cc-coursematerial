# Fast-Track Version for Experienced Java Developers

In its original form, this course targets beginner to intermediate level Java developers. You can also use the material to do a fast-track version for teams where you know that all developers are experienced Java developers. This page describes a proposed content and excercise schedule for this case. 

Basic premise of the fast-track version:
* Participants are experienced Java developers that do not need info on: POM, Spring DI, mocking, servlets, logging basics
* No explanations and hands-on excercises for basic Java topics 
* More explaining code samples and less doing; focus doing parts on key elements that are most likely new to everyone
* Use the same slide deck as the full course but skip over unnecessary slides
* Extensive use of the branches as starting points for exercises in order to skip basic parts. This concerns mostly Day 1-3. Afterwards there is no more skipping parts.
* People are OK with it that they will be rushed 

# Proposed Schedule 
Below we give one proposed schedule that should work in most cases. Time estimates are given in [].

## Day 1
#### Morning
* Intro and Expectations [1h]
* Make sure the IDE works for everyone [30 mins, optional]
  * Exercise 2 done by participants; this is optional but an easy way to get started, make sure the IDE works and have a first look at a REST endpoint
* Microservice Architecture [ Slides / Video: 15 mins, discussion: 15-30 mins]
* Explain REST service in code and add one endpoint with test [1.5 hrs]
  * Checkout branch 4 and explain the relevant code (annotations, key code elements) of: AdvertisementController, AdvertisementControllerTest, Advertisement, Bean registration
  * Exercise 4.2 done by participants (on base of branch 4)
  * Exercise 5: Explain validation annotations [15 mins]

#### Afternoon
* Cloud Foundry Basics 
  * Slides (Video) [20 mins]
  * Demo (video) [20 mins]
  * Exercise 6: Deploy ads on Cloud Foundry [30 mins]
* Connect Database [2-3 hrs]
  * Slides (video) [20 mins]
  * Exercise 7: Demo and explain code / localEnvironment: Connect to local PostgreSQL DB  (DBeaver, VCAP_SERVICES)
  * Checkout branch 8.1 and explain POM, defining an entity, repo interface, config --> datasource
  * Exercise 8.2: Participants change the storage from Map to JPA, **OR** explain code of this branch
  * Exercise 9: Implement JPA Entity: Participants do this; focus is on some new JPA annotations and unit tests 
  * Exercise 10 Deploy on CF

## Day 2
#### Morning
* Logging [2-3 hrs]
  * Reduced logging slides (skip what is basic) [30 min]
  * Checkout branch 12 and explain: POM, logger call, RequestLoggingFilter, example logging calls in code, log level config
  * Exercise 13: Explain MDC, let participants add one custom field
  * Deploy to CF 
  * Show Kibana Demo (video: 15 mins)
* Service-to-service Communication - basics [1 hr]
  * Show slides [30 mins]

#### Afternoon
* Continue Service-to-service Communication [3-4 hrs]
  * Exercise 16,17,18: Explain exercises and let participants do them as described in the exercises
  * Exercise 20,21: Demo how to use messages / RabbitMQ and explain the code

## Day 3 
* Do the topics Security and Testing Strategy with content and exercises 22-25  [5-6 hrs]
* CD overview slides / video [30mins]: this assumes that the topic will be covered in-depth by some developers in the CD & DevOps course 
* Microservice Design [20 mins content + discussion]

## Hints
* If you have any additional time you can also pick from the optional /advanced exercises and other demos. 
* You should also explicitly mention the 'Detail Notes' pages for all the topics.


