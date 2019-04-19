# Reusable Images
The powerpoint presentation `reuse.pptx` contains some images which are used in the slides.
Instead of exporting the individual slides to PNG files (or, worse, taking screenshots), we export the whole slide set
as a PDF file and import single pages from this PDF file.
 
One advantage is that only one step (exporting from PPTX to PDF) is necessary for each change. Another advantage is that
the resulting PDF file provides vector graphics, giving better quality in the presentation (and, if printed, also
printouts of the slides).

To get rid of the whitespace around the images, the `pdfcrop` command is automatically started when building the slides.
For that the file `reuse-crop.pdf` is (re)generated. The already existing file is just used if the
`pdfcrop` step is not run (maybe because it is not available on the developer's machine). As such, the `-crop.pdf` file
should be updated when necessary, so that local builds show the correct information. The current version of that file, generated in the build job, is available [here](http://mo-9d199bd4b.mo.sap.corp:8080/job/cc-coursematerial/lastSuccessfulBuild/artifact/Z_Presentations/cc-appdev-java.pdf).

To make usage of these slides/images easy, we introduced commands like `\includeGraphicsExerciseFour`
(example usage: `\includeGraphicsExerciseFour{width=\textwidth}`).
The definition of these commands is part of the file [graphics_support.tex](../Z_Presentations/graphics_support.tex).
Here, the page is given as the second argument of the command.
Note that LaTeX commands must not include numbers (i.e., use `Four` instead of `4` in the definition).

To add a new image to the set, add it as the last page and create a new command for it in `graphics_support.tex`.
