# Trainer Info

**Step 1:** We recommend you to test briefly the VM Image that is linked implicitely in the [`CoursePrerequisites.md`](/CoursePrerequisites/README.md), whether it satisfies your need. If not read below...

**Step 2:** Inform the course particpants at least 14 days before the start of the course about the 
[`CoursePrerequisites.md`](/CoursePrerequisites/README.md), which describes the necessary steps in detail.

**Step 3:** Ensure that the dependend services are running - as explained below.


### Ensure User Service is running
The trainer should take care that the following dependent microservice is running in the cloud:
User Service: [cc-bulletinboard-users](https://github.wdf.sap.corp/cc-java-dev/cc-bulletinboard-users).
 
You can check this by accessing [this URL](https://bulletinboard-users-course.cfapps.sap.hana.ondemand.com). Also make sure that [this URL](https://bulletinboard-users-course.cfapps.sap.hana.ondemand.com/api/v1.0/users/42) returns a premium user when visited in a browser: `{"id": "42", ..., "premiumUser": true}`

**Note:** To deploy the dependend service trigger manually a build in [Jenkins](https://cc-admin.mo.sap.corp/view/DeleteSpaces/job/setup_devopscourse_users_microservice_cc-course/).

### Check Virtual Machine (VM)
For a reliable and easy to setup development environment we provide you a virtual machine (VM) image. The VM runs an Ubuntu (Linux) system and offers all tools and configuration that are required for the course.

Normally the provided VM image should be fine for the training and you as trainer don't need to offer a new one.

### Advanced: If adaption required... 
#### Simple Variant - Adapt VM manually
- Download the VM image as described [here](https://github.wdf.sap.corp/agile-se/vagrant-development-box/blob/master/VMImage_GettingStarted.md)
- Start the VM in Virtual Box
- Apply the changes
- Shut down the VM (as described [here](https://github.wdf.sap.corp/agile-se/vagrant-development-box/blob/master/VMImage_GettingStarted.md#shut-down-the-vm))

To create the image within Virtual Box:
- in the list select the VM
- in the menu select `File` - `Export Appliance`
- distribute the exported file and inform the participants to use this VM image instead

#### Advanced Variant - Start from Scratch
- A fresh VM can be created on base of some configuration files as explained [here](https://github.wdf.sap.corp/agile-se/vagrant-development-box).

