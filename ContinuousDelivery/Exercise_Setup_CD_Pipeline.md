# Exercise 27 [Optional] - Setup CD Pipeline

## Learning Goal
The goal of this exercise is to setup a minimal CD pipeline consisting of 2 stages with Jenkins 2.0.


## Prerequisites
- Open a terminal and start Jenkins with `docker start course-jenkins`. Note: Stop all Tomcat instances (started using `mvn tomcat7:run` or inside Eclipse) first, as Jenkins uses the port `8080`.
- Navigate to your Jenkins server: `http://localhost:8080/`.

## Exercise Hello World Pipeline 
In the following exercise we will learn some essential pipeline syntax and create a script that echo `Hello Pipeline!` and give out the version of cloud foundry cli.

- [Pipeline-Exercise: Hello Pipeline](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/ContinuousDelivery/Continuous_Delivery_Basics/Pipeline-Exercise-Hello_Pipeline.md)

**Note:** The Industry Cloud (ICD) runs a workstream `Continuous Delivery` where they provide best practices and [ready-to-use Jenkins pipeline templates](https://github.wdf.sap.corp/ContinuousDelivery/jenkins-pipelines) that help teams to get started as quickly as possible with minimum effort. The workstream also serves as a discussion / communication platform.

## Exercise Commit Stage
In the following exercise you will learn about the commit stage in which the basic automation is done that happens right after the developer committed and pushed his changes to the central repository, such as compilation and unit test execution.

- [Pipeline Plugin Exercise: Commit Stage](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/ContinuousDelivery/Commit_Stage/Pipeline-Exercise-Commit_Stage.md)

## Exercise Integration Stage
In the following exercise you will learn about the integration stage in which you are testing your microservice in integration. From the commit stage we know that internally our component works well in a "sandbox" environment - now we want to find out whether it works in a cloud environment, with application server and database very similar to production. We also want to find out whether our microservice integrates well with the other microservices that belong to our product.

- [Exercise: Integration Stage Part 1 - Deploy](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/ContinuousDelivery/Integration_Stage/Pipeline-Exercise-Integration_Stage_Part1.md)
- [Exercise: Integration Stage Part 2 - System Test](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/ContinuousDelivery/Integration_Stage/Pipeline-Exercise-Integration_Stage_Part2.md)

## Jenkins-as-a-Service
[Jenkins-as-a-Service](https://jenx.int.sap.hana.ondemand.com/api/) aims to provide an easy to use offering where one can create a Jenkins server using a self-service based on a template, e.g. with some default plug-ins being pre-installed, as well as SAP root certificates, build tools etc.
It is intended that this also becomes flexible/extendible, i.e. in case people needn some Python related tools instead of the Node.js ones from the template, they should be able to do that, but this is currently not possible.
