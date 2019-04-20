Exercise: Development Efficiency
===========================================
## Learning Goal
In this exercise you will implement a little bit of Java Code to let `http://localhost:8080/` respond with the content of the `/META-INF/MANIFEST.MF` file that is part of the WAR file. 

Along the way you will learn
- how to add dependencies to other libraries to your Maven build and
- some Eclipse Shortcuts to become more efficient in your IDE. While developing try to use your keyboard as much as possible!

## Prerequisite
- You should have done the [Exercise: Setup and Deploy Web Application](PreExercise_Setup_WebApp_Project.md).
- Ensure that you've stopped the running Tomcat server in the `Servers` view.

## Step 1: Enhance your Code

- Open the `DefaultController` class by using the shortcut `CTRL+Shift+T`.
- Copy the below code into the `get` method:
```java
// Move the context definition up using ALT+Up
@Inject  ServletContext context;

InputStream in = context.getResourceAsStream("/META-INF/MANIFEST.MF");
if (in != null) {
Manifest manifest = new Manifest(in);
return manifest.getMainAttributes().getValue("Created-By");
}
return context.getRealPath("/");
```
This code reads the `MANIFEST.MF` file and parses the `Created-By` information out of it.
- The `context` variable must be defined outside of the method. Move the cursor into the respective line and use shortcut `ALT+Up` (moves current line)
- Use the shortcut `CTRL+Shift+F` to format your code (similar to ABAP Pretty Printer :-))
- Use the shortcut `CTRL+Shift+O` to organize missing imports
- The Manifest creation brings you an unhandled IOException. Move the cursor into the respective line and use the shortcut `CTRL+1` (Quick fix) and select `Add throws declaration`
- Delete the comment: move the cursor into the respective line and use shortcut `CTRL+D` (deletes current line)
- Use the shortcut `CTRL+S` to save the current file and to trigger the automatic build


## Step 2: Run the Web Application in Eclipse
- In the `Servers` view -> (Re-)start the server (`CTRL+ALT+R`)
- In a browser open the URL: `http://localhost:8080/` which should show:
``` 
Maven Integration for Eclipse
```
Why is this the case? Maybe you've thought it must be like the content of the manifest file that is part of `target/bulletinboard-ads.war`? BUT: If you run your application within Eclipse, the Maven Integration Plugin creates no WAR file at all. But it generates a `MANIFEST.MF` file under `target/m2e-wtp/web-resources`.

## Step 3: Return all Manifest Attributes
In the `DefaultController` class we want to enhance the code in a way that all attributes are returned.

Some implementation notes and tips:
- Evaluate the return type of the `java.util.jar.Manifest.getMainAttributes()` method. Set the cursor on the method name and 
  - use the shortcut `F2` to get the documentation, or 
  - use the shortcut `F3` to navigate into the method. Navigate back and forth via shortcut `ALT+LEFT` (or `ALT+RIGHT`)
- Make use of [`google.com`](google.com) and [`http://stackoverflow.com/`](http://stackoverflow.com/) to get help from other developers. 
- Use the shortcut `CTRL+Space` for code completion whenever possible, e.g. when calling a method, when writing a `for` loop, or when auto-complete "syso" to get `System.out.println()`.
- Use `StringBuilder` to build the final `String`. The shortcut `CTRL+ALT+Down` might come handy for duplicating the line.
- In order to make the line breaks ("\n") visible in the browser you need to change the media type of your HTTP Rest API from `text/html` to `text/plain`. Additional hint: You do that by replacing the `@RequestMapping` annotation in the `DefaultController` class with `@RequestMapping(path = "/", produces = MediaType.TEXT_PLAIN_VALUE)`. Use the shortcut `CTRL+1` to fix the import issue.

## Step 4: Use Apache Commons `StrBuilder`
We want to avoid the hardcoded / selfdefined line breaks (e.g. "\n"). Here we want to make use of [`StrBuilder`](https://commons.apache.org/proper/commons-text/javadocs/api-release/index.html) from a third-party Apache Commons library.

#### Add Maven Dependencies 
- We want to search the SAP internal Maven Repository to find the right library dependency to be entered in our `pom.xml`. Open the url [`http://nexusrel.wdf.sap.corp:8081/nexus/`](http://nexusrel.wdf.sap.corp:8081/nexus/) and enter `apache commons-text`  (like the package name of the StrBuilder) as search string. The right one is provided under groupId `org.apache.commons`. Select the latest version and copy the given Maven (pom) dependency description (ensure that the jar file is selected).
  - Alternatively you can also search the [global Maven Repository](http://mvnrepository.com/) to find the right library dependency to be entered in our `pom.xml`.
  - In addition you can check on the risk rating of the open source library [here](https://open-source.mo.sap.corp). 
  - Note: `StrBuilder` is deprecated in commons-lang3 as of 3.6 and moved into commons-text.  
- Open the `pom.xml` using the XML view of Eclipse and add the copied dependency description **at the end of the <dependencies> section**. Use the shortcut `CTRL+Shift+F` to format your XML code. 
- Note: After you've changed the Maven settings, don't forget to update your Eclipse project! To do so right click on your Eclipse project and select `Maven` - `Update Project ...` (or hit `Alt-F5`).

#### Make Use of `StrBuilder`
- Open `DefaultController` class again and replace the usage of `StringBuilder` by the usage of `StrBuilder`.  Use the shortcut `CTRL+Shift+O` to organize missing imports.
- Make use of the `appendln` feature of `StrBuilder`
- Run the Web Application in Eclipse as described previously.

## Overview Eclipse Shortcuts that might come handy...
Create a new method in your code base and paste the comments from below. Now you can follow the 10 steps... Have fun! 


```java

// 1. Delete this line
// CTRL+D

// 2. Toggle this comment
// CTRL+7 or CTRL+/

// 3. Move this line down
// ALT+Down

// 4. Duplicate this line
// CTRL+ALT+Down

// 5. Find / Replace "+" (use Return to move to next finding)
// CTRL+F

// 6. Format Code (pretty printer)
// CTRL+Shift+F

// 7. Fix code (e.g. create methods, import)
// CTRL+1

// 8. Complete code e.g. call method, "for" or "syso"
// CTRL+Space 

// 9. Save and Save all
// CTRL+S and CTRL+Shift+S

// 10. Organize imports
// CTRL+Shift+O
```

## Used Frameworks and Tools
- [Tomcat Web Server](http://tomcat.apache.org/)

## Further References
- Have a look at the [sample solution](https://github.com/ccjavadev/cc-bulletinboard-ads-spring-webmvc/tree/solution-pre-exercises)
