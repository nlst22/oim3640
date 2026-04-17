## Project Idea

For my final project, I want to build an application that helps users split a bill by taking a picture of a receipt. Instead of manually typing in every item, the app will use image recognition or OCR to identify the items and prices on the receipt. Then, the user will be able to assign items to different people and calculate how much each person owes.

# Why I Chose This Project

Earlier in the semester, I built a terminal-based bill splitter. That project focused on user input and bill-splitting logic. For this final project, I want to expand that idea into a more practical application with a visual interface and image-processing features. This lets me build on something I already understand while also challenging myself with new concepts.

# Main Features

The basic version of the app will include:

Uploading or taking a picture of a receipt
Extracting item names and prices from the receipt
Displaying the detected items in a list
Letting the user choose which person is responsible for each item
Calculating how much each person owes

# Tools / Technologies

OCR tools such as Tesseract to read the receipt
Python functions and data structures to organize items and split totals

# Challenges I Expect

One challenge will be making sure the app reads receipt images accurately, since different receipts may have different formats. Another challenge will be connecting the image-reading part to the bill-splitting logic in a clean way. Because of this, I plan to keep the first version simple and focus on making the core workflow function correctly.

# Minimum Goal

At minimum, I want the app to:

Take in a receipt image
Extract item names and prices
Allow the user to split items between people
Output the final amount each person owes
Possible Stretch Goals

# If I have extra time, I may add:

Tax and tip splitting
A cleaner, more polished interface
The ability to edit incorrectly detected items
Saving or exporting the final split summary