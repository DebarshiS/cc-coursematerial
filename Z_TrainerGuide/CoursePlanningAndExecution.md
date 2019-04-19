# Course Planning and Execution 

This page describes the course planning and organizational steps. The course is called "Microservice Development in Java" in the learning system. 

## Course Organization Types and Steps

There are two ways to offer and run this course:
- **A: Local and closed team trainings** where the trainer trains 'people from their own unit / area' and therefore booking is not open but planned locally. Most trainings will probably be of this type.
**Variants:**
  - In case of a training for a specific team you may know which sections / exercises you do not need since the team already has a working knowledge of that topic. In that case think about just highlighting the key concepts, presenting the solution code of the skipped exercises (i.e. last commit of the solution branch). You can build your own [Agenda](/Abstract/images/Java_CoursePlan.pptx).
  - You can also choose a freestyle module-based learning approach where some developers come together on a weekly basis and concentrate on one module per learning session, like "Service2Service Communication". The modules can then be prepared by different people and you can do a deep dive into the topic before you pick the next module.

- **B: Open courses where anyone can participate.** 

### A: Locally organized team trainings 

- **Plan trainers:** The trainer is training only people in their area / unit. We recommend two trainers per course and no more than 30 participants.
- **Plan participants:** Registration and planning of the course is done within the area. Typically, a team is trained as a whole. The trainer (or an assistant within the area) collects the names / applications and decides on participation.
- **Plan the date and get a room:** If you do not have a local room that you can book and use yourself you should book a room in the training organization / centers. In either case, you want an official 'training course instance' in the learning system where the training time, the trainers and all participants are recorded. 
  - Go to the page [Classroom Event Services (CES)](https://jam4.sapjam.com/groups/X8D0kf6Fgcf4KLjrrzB3Cq/overview_page/0S4rPChR68arzzH6Hcm1bj), click on `Room reservation` to download an XLS template, fill in the details and send it to [CES](mailto:saplearningces@exchange.sap.corp). The course ID is `COURSE DEV_CloudAppJava_PA_CLOUD_1508`.
  - In addition to the room data, also send **all planned participants** along so that they can be booked into the course from the beginning. 
  - **Usually, rooms are hard to get, especially for the 5-day courses. You should book rooms 2-3 months in advance to make sure you can get the date you want.**
  - Since developers are to bring their own laptops, the room needs only seats and tables, power outlets and a beamer. 
- **Communicate date and preparation to participants:** Once the course instance is created, participants automatically get an invitation mail with all the details from the learning system. In addition you should send a mail / meeting request ([see e.g. template](MeetingRequestTemplate.md)) to the participants to inform them about the date, the [**prerequisites / preparation tasks**](https://github.wdf.sap.corp/cc-java-dev/cc-coursematerial/tree/master/CoursePrerequisites) and that they bring their own laptops. Don't hesitate to send a gentle reminder some days before the course starts.

If you need help with course setup and dealing with CES you can also try to contact:  
  - Americas: Wode Courchesne
  - EMEA/MEE: Bilyana Ka]yonska
  - India: Anitha Rani SR
  - Greater China (APJ): Carrie Kang
  - Global Services: Nadia Ryan


### B: Centrally organized open trainings

**Open courses** that are not specific to a team / product / unit are organized by CES on demand. These courses are then just visible in the course catalog and any individual can book themselves into a course. 


## Preparation

As trainer you should follow up the [Course Prerequisites](/CoursePrerequisites/TrainerInfo.md) to ensure the infrastructure and services are running.

#### Print Out
* **Print participant list:** You will get a mail from CES (training system) with the participants list. Print this list and take it to the course since participants have to sign it.
- [Course Agenda](/Abstract/images/Java_CoursePlan_Simple.png) ([Powerpoint](/Abstract/images/Java_CoursePlan.pptx)) in a large print (e.g. A2 or A1) to hang it up in the classroom.
- Cheat Sheets (10-15 copies)
  - Hamcrest: http://www.marcphilipp.de/blog/2013/01/02/hamcrest-quick-reference/ 
  - Cloud Foundry - [internal variant of Anynines](https://github.wdf.sap.corp/cc-devops-course/coursematerial/blob/master/Cheat_Sheets/CS_Merged.pdf)
  - Eclipse Shortcuts: [Eclipse 3.0 predefined shortcuts](http://eclipse-tools.sourceforge.net/Keyboard_shortcuts_(3.0).pdf) (official),  [Eclipse Shortcuts Sheet](http://www.shortcutworld.com/en/win/Eclipse.pdf) (from ShortcutWorld)
- **Course Feedback** is now done electronically, i.e. the participants get a mail after the course. Send in the signed participant list on day 3 or 4 of the training so that participants get the feedback mail during the course time. We recommend: Let participants do the feedback at the end of the course within the course time. This gives much better return rates.

#### Install Eclipse plugin to change the font size
The `tarlog-plugins` is an Eclipse plugin that allows you to **change the font size** using shortcuts: `Ctrl++` and `Ctrl+-`.
Other available features are documented [here](https://github.com/tarlog/tarlog-plugins/wiki/Available-Features).

##### Installation Instructions for `tarlog-plugins`
- Download the latest version of [`tarlog-plugins`](https://github.com/tarlog/tarlog-plugins/releases/).
- Place the jar into `~/apps/eclipse/plugins` folder. Eclipse needs to be restarted.


## During the course
- **Send signed participant list**: Take a picture or scan the participant list with participant signatures and send to [CES](mailto:saplearningces@exchange.sap.corp). Additional participants have to have their userID clearly legible and sign as well. 
**This is very important for the participants (confirmed participation, time recording) as well as for us to justify our budget!**
- Friday afternoon: 
  - It may make sense to again discuss the expectations of the participants in the large round and discuss what was good, what was missing etc. Please note feedback that is relevant to improve the course material and send relevant feedback to [Nena Raab](mailto:nena.raab@sap.com).

## Course Post-Processing
- If this course was a **TTT (train-the-trainer) course**, you should send the names of the new trainers to [Bilyana Kalyonska](mailto:bilyana.kalyonska@sap.com) together with the name of the course.

## Trainers 
Trainers are maintained by the central ASE / Cloud Curriculum group in the [course trainer list](https://jam4.sapjam.com/groups/9R17gNnhm59Nn0eCoX7hnG/content?folder_id=EQa4TsWSUQbKaW6CZEdxIU). 
