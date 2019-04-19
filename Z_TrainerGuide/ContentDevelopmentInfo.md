# Content Developer Information

This section gives an overview about the material that is hosted in this repository and serves as initial entry point to the content and how to change / customize it and build it.


## Course Customization for Trainers

As a trainer you may want to just **adapt the schedule**. The simplest way to do this is to simply edit the agenda image and use it instead of the one included in the slides. The original of the Agenda Image is [here](/Abstract/images/Java_CoursePlan.pptx). 

Anything more, such as changing slides, changing or adding content will require that you
1. Fork the `cc-coursematerial` repo
2. You set up your own development environment (latex) and build (jenkins) environment and learn latex. The section below describes how to do that.



# Overview of the Course Material Content and Build

## Agenda Image

The agenda image is editable [here](/Abstract/images/Java_CoursePlan.pptx). Afterwards you need to export it to [Abstract/images/Java_CoursePlan.png](/Abstract/images/Java_CoursePlan.png).

## Slides
The slides are written in LaTeX and are automatically built on Jenkins. You can find the most current version [here](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf).  

## Exercises
The exercises are written in [Markdown](http://daringfireball.net/projects/markdown/syntax) [(Cheat Sheet)](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet). The files are prefixed with "Exercise_".

## Accessing and Updating the LaTeX Slides
The slides are built using LaTeX and under version control of Github. This allows us to version
all changes, do DIFFs on versions and allow several developers of materials to work together.

## Continuous Integration for Sample Solution and Slides Build
[Jenkins Job (not working in Internet Explorer)](http://mo-9d199bd4b.mo.sap.corp:8080/job/bulletinboard-ads%20(Solutions)/) is registered as Github Hook and is notified whenever a new change was pushed to the sample solution GitHub repository  [`cc-java/cc-bulletinboard-ads`](https://github.wdf.sap.corp/cc-java/cc-bulletinboard-ads). Then the Jenkins job builds the app and runs the tests.


# Updating the Course Materials

The course material is written in LaTeX, a document markup language which bears some similarities to HTML. This markup language allows to separate contents and layout, so either can be adapted without interfering with the other. Also, the underlying format is ASCII, which allows to easily merge and compare the work of multiple people in a source code management system like github. These advantages led us to selecting it for the documentation.

The following sections will explain how you can work with the documentation.

## Introduction to LaTeX

To get started using LaTeX, there are tutorials and documentation available at http://tug.org/. 

A two-page reference card for LaTeX is available at http://www.stdout.org/~winston/latex/.

### LaTeX on Windows

- Download and install MiKTeX from http://miktex.org/ (e.g. Version 2.9, Basic install works)
- Then, in the miktex Package Manager install all packages (This will since there is apparently no automated load of missing packages and we use a lot of them. This may take a while!)
- Double-click a .tex-file (e.g. trainerguide_JAVA.tex, two windows will open as shown in the screenshot)
- To render any changes in .tex-files just press the play-button on the top left of the left window. The right window will refresh and show the newly created pdf-file. 
- If any error occurs it will be displayed in the console which will pop up in the left window during the rendering process.
- During the rendering process MiKTeX will download any required packages.
- If there is a problem with the font "Metrics (TPM)" the package "symbol" has to be installed manually using the package manager delivered with MiKTeX.

### LaTeX on Mac

On the Mac, it is recommended to use the MacTeX distribution http://www.tug.org/mactex/.

### LaTeX on Linux

On Linux, it is recommended to use the TeX Live distribution (http://www.tug.org/texlive/). Ubuntu users should make sure that the packages `texlive-latex-extra` and `texlive-fonts-extra` are being included in the installation.


### Building the Documentation

To build the documentation manually, you need to run the `latex` and possibly also the `bibtex` command several times. This is inconvenient and also error-prone, therefore we recommend to use `latexmk` which is a build-mechanism that figures out the required steps automatically. You can invoke it like this:

`latexmk -pdf <latexfile>`

## Content Structure

The `cc-m2-java-course` repository contains the top-level directory `blocks` which contains the course material, namely the presentation slides. In the following, we give an overview of the various parts and their contents.

### General Remarks
The directory contains two kinds of directories: those that are prefixed with `Z_` and those that are not.

Naming conventions:
- The suffix `_JAVA` refers to the ASE-Java Web course.

### Directories not prefixed with Z

These directories contain material for one topic of the course. This material may include the corresponding slides and the code that is provided for exercises, possibly for several course flavors side-by-side.

### Directories prefixed with Z

These directories contain meta-elements. The following directories exist:

- Z_BookCovers: This directory contains small images of book covers. 
- Z_Forms: Single sheets that are handed out during a course, for example the skill sheet or the feedback form.
- Z_Presentations: This directory contains the master documents for the presentation slides (e.g. presentations_JAVA<>.tex) along with a common setup file containing some macros as well as setup for syntax highlighting for Java.

### The Master Document

For each course flavor there is a master document. For example the JAVA presentation /Z_Presentations/presentations_JAVA.tex. 

This master document combines all chapters into one document. This way, different courses can use a different ordering of the topics, and they can flexibly decide which chapters to include and which to leave out. As some of the chapters are specific to the underlying technology stack, this allows for reuse of common chapters in the different courses.

In the body of a master document, all desired chapters are included. 
Only the master documents can be converted to PDF. Attempts to convert any other `.tex` document will fail because they only represent a document fragment. The conversion can be done using the `latexmk` command as described in Section `Building the documentation`. The appropriate build mechanisms of graphical LaTeX environments will also be suitable.

### Presentations

The presentation slides are rendered into a single PDF file for each course flavor. This allows to switch from one presentation to the next without having to search around in the file system. Additionally, each presentation is preceded with an introductory page containing a picture and followed by a page asking for questions about the presentation.
In order to make this as easily usable as possible, several macro commands are provided.

To include any presentation, the macro `includepresentation` can be used. It has one mandatory parameter which is the path from the master document to the presentation to be included, and one optional parameter which is the path from the master document to the picture that is to be used for the first page. If this optional parameter is not given, a default picture is used. This example includes the refactoring presentation:

`\includepresentation[backgrounds/LoggingTracing.jpg]{../LoggingTracing/LoggingTracing_presentation}`

In order to avoid giving a lengthy specification of the name of the picture, the path name and the presentation name, we introduced shortcuts to include presentations. These will accept a parameter and assume that the presentation is stored in a folder of the same name, that the presentation file bears this name, and that the background picture is stored in the backgrounds folder and also bears the same name, suffixed with `.jpg`. There are commands available for all flavors of the course as well as for presentations common to several flavors. These commands are:

~~~
\includeCommonPresentation{<name>}
\includeJavaPresentation{<name>}
...
~~~

These commands include a presentation that resides in a folder called `<name>`, stored in a file called `<name>_presentation.tex` (for the common version) or `<name>_presentation_JAVA.tex` (for the JAVA version) and so on, and an image called `<name>.jpg` stored in the backgrounds folder is being used for the start page.

The full list of shortcut commands together with the commands they abbreviate can be found in the file `presentations_setup.tex`.

To use syntax highlighting for a programming language, include one of the files `java_support.tex` in the master document.

### Book Covers

The book covers can be downloaded from Amazon at http://www.majordojo.com/projects/javascript/amazon-image-hacks.php.

There you need to enter the ASIN which is the lengthy number that is part of the Amazon URL. The resolution ``Huuge'' works well. 

Open the displayed link in a separate browser window and save the image. Convert it to PNG afterwards.

Note: Often there is a white frame around the pictures which needs to be removed manually.




