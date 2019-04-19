.PHONY: all clean

all: cc-appdev-java.pdf

reuse-crop.pdf: ../Z_ReuseImages/reuse.pdf
	pdfcrop ../Z_ReuseImages/reuse.pdf

cc-appdev-java.pdf: presentations_JAVA.tex reuse-crop.pdf
	latexmk -pdf -pdflatex="pdflatex -interactive=nonstopmode" -use-make presentations_JAVA.tex
	mv presentations_JAVA.pdf cc-appdev-java.pdf

clean:
	latexmk -CA
