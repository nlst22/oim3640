# AI Usage Statement

## Overview

AI was used as a support tool during the development of this final project, `Receipt Splitter`. I used AI to help brainstorm implementation ideas, debug issues, improve the user interface, and write or revise parts of the supporting documentation. The core project idea, project goals, and major feature decisions came from my own proposal and from building on my earlier Project 1 bill splitter.

## How AI was used

AI helped with the following parts of the project:

- planning how to turn my terminal-based bill splitter into a Flask web application
- suggesting ways to organize the app into routes, templates, styles, and service/helper functions
- helping integrate OCR support using Tesseract, Pillow, and `pytesseract`
- debugging issues related to receipt image uploads, OCR extraction, Flask templates, and item assignment
- improving the interface design and restyling the app theme
- helping extend the app so items can be assigned to any number of named people
- helping extend the app so one item can be split across a selected subset of people
- helping write and update project documentation such as the `README.md`

## What I contributed directly

I was responsible for the project direction and for deciding what the app needed to do. I defined the original idea in my proposal, chose to base the project on my Project 1 bill-splitting logic, tested the app with my own receipt examples, and decided which design and feature changes to keep.

I also reviewed the generated code and outputs, tested the app behavior, and used the results to guide further revisions. When features or bugs did not behave the way I wanted, I used that feedback to refine the implementation.

## Examples of AI-assisted work in this project

Some specific examples of AI-assisted work include:

- converting the Project 1 itemized split logic into a web-based workflow
- adding OCR preprocessing for receipt images
- improving receipt parsing for messy OCR output
- fixing a Flask/Jinja template bug on the split results page
- updating the item assignment system from a simple dropdown to checkbox-based partial sharing
- revising the app theme and layout to create a more polished interface

## Final note

AI was used as a development assistant, not as a substitute for the project itself. I still made the main decisions about the app's purpose, feature set, testing, and final presentation.
