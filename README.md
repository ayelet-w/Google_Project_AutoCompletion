# Google Project AutoCompletion (ExcellenTeam Bootcamp)
## Team Members:
### Orpaz Levi
### Ayelet Weinstock


## Introduction:
### In order to improve the user experience of the Google search engine, the development team decided to allow the completion of sentences from articles, documentation and information files on various technological topics.

## The Task:
### A program that supports two main functions: Initialization function - The purpose of the function is to get a list of text sources on which the search engine will run, each source contains a collection of sentences.
   Completion function - the function must get a string - which is the text that the user typed - the function must return the five best completions.

## Our solution:
###  Keep in one dictionary the full sentence and as a key to some number.  And in a second dictionary, keep as a key all the possibilities that the user will type (include mestakes), and as a list of five numbers for the full sentences with the highest score.  So we got a very fast run time and in order to deal with the memory problem we divided the dictionary into several files.

## Libraries/Technologies Used:
### * python 3.7
### * VS code
### * Google colab
