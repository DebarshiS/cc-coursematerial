Environment Setup and Prerequisites for "Microservices Development in Java"
=====================================================
This file explains the general prerequisites for the "Microservices Development in Java" course.
To be able to install software on your computer, please make sure you have administrative rights.
For a reliable and easy way to get a development environment we provide a virtual machine (VM). 

The VM runs an **Ubuntu Linux** system and provides nearly all tools and configuration which are required within the course. If you are not familiar with Unix/Linux, you can check out [Learn Unix in 10 Minutes](https://csg.sph.umich.edu/docs/hints/learnUNIXin10minutes.html) or [Introduction to Linux](http://tldp.org/LDP/intro-linux/html/index.html) or with a little more detail [Learn Linux in 5 Days](https://linuxtrainingacademy.com/wp-content/uploads/2016/08/learn-linux-in-5-days.pdf) (it actually takes a lot less time). There is also a very good [Linux Commandline Cheat Sheet](https://www.linuxtrainingacademy.com/wp-content/uploads/2016/12/LinuxCommandLineCheatSheet.pdf).

**In case you run into trouble, contact us via our [JAM support community](https://jam4.sapjam.com/groups/qXGUpaYj8Jn3pPCB9xdXiE).**

# Technical Prerequisites
## 1. SAP Github Account
Create a Github account on the SAP internal Github if you don't already have one. Use your d-user as ID and a *separate password* (not your SAP domain password). For help see: [Getting started with git and GitHub at SAP](https://github.wdf.sap.corp/pages/github/learn.html).
 
## 2. Prepare your Development Environment
* **VM Setup**: Please follow the [installations steps](https://github.wdf.sap.corp/agile-se/vagrant-development-box/blob/master/VMImage_GettingStarted.md) to prepare your copy of the VM image which provides the whole development environment.
* **Chrome**: If you want to use Chrome from your host OS as default browser you can follow [these instructions](https://github.wdf.sap.corp/bridge/bridge/wiki/Browser-Support) to get rid of the annoying certificate selection popups.
* **Local Setup**: In case you prefer to use your local Windows/Mac/... system instead of the VM, you can follow [these instructions](/CoursePrerequisites/localEnvSetup/README.md). **However, for the course please make use of the VM, as it provides a tested and well-documented environment.**

## 3. Prepare Trial Account and Space on Cloud Foundry @SAP CP
- Create your own **Trial Account and Space** on the **Cloud Foundry Canary landscape** using the [**self-service on SAP Internal Cockpit**](https://account.int.sap.hana.ondemand.com/cockpit#/home/overview). Click the button **Start Cloud Foundry Trial** and select the Europe/Frankfurt region. Use your domain user and password to log in. You can get further information from the [**Getting Started with Cloud Foundry** help page](https://help.sap.com/viewer/65de2977205c403bbc107264b8eccf4b/Cloud/en-US/b8ee7894fe0b4df5b78f61dd1ac178ee.html). 
- Make sure you have created a trial account on our SAP internal Canary landscape: your Trial account should appear [here](https://account.int.sap.hana.ondemand.com/cockpit#/region/cf-eu10-canary/overview).
- Optionally, you can also join the [CF users mailing list](https://listserv.sap.corp/mailman/listinfo/cf.users) for questions, answers and discussions regarding SAP CP Cloud Foundry.
- Find other SAP internal links such as support and release notes [here](https://github.infra.hana.ondemand.com/cloudfoundry/cf-docs/wiki/CF-EU10-CANARY). 

> #### Important information on Trial Account Expiration  
> -	New CF trial accounts will be suspended automatically after 30 days. The Cloud cockpit now displays the remaining time of a free trial. After suspension, you can still log on to your trial account, but you're not longer able to use the applications or services.
> -	It's possible to renew the account for up to 90 days using the “Extend Free Trial” button in the Cloud cockpit.
> -	90 days after account creation, CF trial accounts are deleted.
> - You will be able to sign-up for a new trial account.


# Test your Java Knowledge - Are you Ready for the Training?
You should have a **working knowledge of Java and be familiar with Eclipse and Maven basics before taking this course!**
The better you are prepared, the easier it will be to follow the course and the more you will get out of it. So please take this seriously and do the following **Exercises** to get to know the basics.

## Exercise: Setup Web Application Project
In the course we develop a web application, as a microservice, which runs on an Apache Tomcat webserver. In order to understand the basics on how to setup and run a web application we've provided you the [Exercise: Setup Web Application Project](../CoursePrerequisites/PreExercise_Setup_WebApp_Project.md) that should be done before the course starts.

## Exercise: Development Efficiency
Having understood a basic Maven Web Application Project setup we want to develop a small functionality using a third-party library while making use of shortcuts. Have fun with [Exercise: Development Efficiency](../CoursePrerequisites/PreExercise_DevelopmentEfficiency.md)!


## Further Learning Opportunities
* **Java**: If you are new to Java you can 
  - Take video courses at Lynda.com. To take this video course, go to successfactors learning (via sap portal) and then in the search enter 'java essentials training' or 'lynda_3643'.
  - You can also login directly to [Lynda.com](http://lynda.com), then click on `Log in`, choose `Organization login` and in the org url field enter "www.sap.com". You will then be logged in with your SAP SSO credentials and you can browse the Lynda catalog and start video courses directly from there . Note: When you do it this way, there will be no record of you taking the course in the SuccessMap Learning system.
  - Alternatively, you can walk through the [Java Tutorials Learning Paths (Oracle)](http://docs.oracle.com/javase/tutorial/tutorialLearningPaths.html#newtojava)
  - An even better option would be to attend the **class room training** ["Introduction to Programming in Java"](https://performancemanager5.successfactors.eu/sf/learning?destUrl=https%3a%2f%2fsap%2eplateau%2ecom%2flearning%2fuser%2fdeeplink%5fredirect%2ejsp%3flinkId%3dSCHEDULED%5fOFFERING%5fDETAILS%26scheduleID%3d97982%26fromSF%3dY&company=SAP&_s.crb=g9sHU%252fcSY3LxZvwYSKQYLsGr73M%253d)
* **Maven**: If you are new to Maven you should have a look at the [Maven basis learning module](https://github.wdf.sap.corp/cloud-native-dev/java-fundamentals/blob/master/4_Build%20Automation%20with%20Maven/README.md)
* **Spring**: 
  * In our course we are using `Spring` as Dependency Injection Framework to achieve loose coupling. Besides that Spring is the most popular application development framework for enterprise Java. Millions of developers around the world use [Spring Framework](http://docs.spring.io/spring/docs/current/spring-framework-reference/html/overview.html) to create highly performant, easily testable, and reusable code. Spring framework is an open source Java platform.
  * Unfortunately, we have no really good video courses on Spring available internally as of now. As far as we know the best free tutorial for what we need is this '[Spring Framework](https://www.youtube.com/watch?v=GB8k2-Egfv0&list=PLC97BDEFDCDD169D7)' playlist. See also the [PDF for this topic](https://jam4.sapjam.com/profile/4zhiFeuhhdWUxETpEjh9Ed/documents/ht2QvRfQKbvaYPlmY80Ews/download) or get a newer version [here](https://gumroad.com/l/IXVR). Note however, that this tutorial covers more than we need for our course.
