# Receipt Splitter

This is a basic first version of the final project idea. It builds on the Project 1 bill splitter by moving the itemized split into a small Flask web app.

## What it does

- accepts a receipt image or text file upload
- also lets the user paste receipt text manually
- detects item lines that end with prices
- lets the user assign each item to Person 1, Person 2, or Shared
- calculates each person's total
- splits shared items, tax, and tip evenly

## Project structure

- `app.py`: Flask routes
- `services.py`: receipt parsing and bill-splitting functions
- `templates/`: web pages
- `static/styles.css`: page styling
- `requirements.txt`: Python packages

## Run locally

From the repository root:

```powershell
pip install -r mini_projects/final_project/requirements.txt
python mini_projects/final_project/app.py
```

Then open `http://127.0.0.1:5000`.

## OCR note

Text uploads and pasted receipt text work with only Python packages. Image OCR also needs the Tesseract program installed on your computer. If image OCR is not set up yet, paste receipt text into the text box and the rest of the app will still work.

Example receipt text:

```text
Burger 12.50
Fries 4.25
Soda 3.00
Nachos 9.75
Tax 2.10
Total 31.60
```
