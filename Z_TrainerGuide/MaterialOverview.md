# Overview Material Structure

Even if the course participant meets the course prerequisites there might be differences in the knowledge level. 

Thats's why the course material is very modular, contains some optional or advanced exercises and demos. If you download the [latest slides](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf) you can see, that the slides are grouped and are selectable by topic.

### Skip non-optional parts for experienced java developers
Let's assume you conduct a training to SAP CP Neo developers. Then you might want to skip the one or the other exercise or even module of the first day. 
Then explain concepts as needed, look at the solution code (show what is what).
It's no problem to skip even non-optional exercises. You can checkout and start with the next branch. 

### Optional steps and exercises
Typically you have a mixed audience, that's why most exercises itself contains optional steps. When introducing the exercises don't forget to mention / introduce the optional exercises as well.
The more experienced java developers can select them, either when they have finished the core part or when they are more interested in those.

### Sample solution branches
For each exercise exists a sample solution. After you have chosen the right branch e.g. `Solution Exercise 5-1: Validation and Exceptions` in the sample Github projects 
select `Commits` ([example](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc/commits/solution-5-ValidationExceptions)). 
The last commit (or last two commits) shows the code, that was added as part of the exercise.

Github projects with sample solution
- [cc-bulletinboard-ads-spring-webmvc](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc)
- [cc-bulletinboard-systemtest](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-systemtest)

### Detailed information
You can find in context of most modules another `Readme.md` that offers you further details that might come in handy you when preparing the topic. Furthermore you can deep dive in some topics, that are collected in the [/Knowledge](/Knowledge) folder. You can refer to those documents if you like. 

**Note**: If you wish to read the Github Flavored `.md` files offline you can install [MarkView Chrome plugin](https://chrome.google.com/webstore/detail/markview/iaddkimmopgchbbnmfmdcophmlnghkim).

### Advanced demos
Find on the [Exercises and Demos wiki](https://github.com/ccjavadev/cc-coursematerial/wiki/Exercises-and-Demos) some additional demos you can show like `Redis` or `Connect to HANA Database`, if you have time and the people are interested.

## Tool decisions and other internals
Find some internal discussions in the [_Internals](/_Internals) folder like a list of [OSS approved tools](/_Internals/Tools.md) used in the course and the [tool decisions](/_Internals/Tool_Decisions.md), we made.

## Further links and Resources
- Find [here](https://github.com/ccjavadev/cc-coursematerial/blob/master/Resources.md) some important lins in respect to SAP CP classic, CF @SAP CP, related communities etc. plus some links to external resources.
