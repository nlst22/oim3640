# Receipt Splitter

Receipt Splitter is a Flask web app that builds on Project 1's itemized bill-splitting logic. It takes receipt text or a receipt image, extracts likely items and prices, lets you assign each item to one person or a subset of the group, and calculates what everyone owes.

## Live app

Try the deployed version here:

https://receipt-splitter-l9w7.onrender.com

## Demo video

Project demo video: Local usage of OCR

[final_project_demo_video.mp4](./final_project_demo_video.mp4)

## Current features

- upload a receipt image, text file, or CSV file
- paste receipt text manually
- run OCR on receipt images with Tesseract
- detect likely item lines and prices from extracted text
- enter any number of people by name
- assign an item to:
  - one person
  - several specific people
  - everyone by leaving it unchecked
- split tax and tip evenly across the full group
- show a final per-person summary and assigned item list

## How item sharing works

- If you check one person for an item, that person pays for the whole item.
- If you check multiple people, the item is split evenly across only those people.
- If you check nobody, the item is treated as shared across the whole table.

## Project structure

- `app.py` - Flask routes and form handling
- `services.py` - OCR helpers, receipt parsing, and bill-splitting logic
- `templates/` - Jinja templates for the main page and results page
- `static/styles.css` - app styling
- `requirements.txt` - Python dependencies
- `final_proposal.md` - proposal for the final project

## Requirements

- Python 3.10+
- Tesseract OCR installed on Windows if you want image OCR
- Python packages from `requirements.txt`

## Install dependencies

From the repository root:

```powershell
pip install -r mini_projects/final_project/requirements.txt
```

## OCR setup note

Image OCR needs:

- `Pillow`
- `pytesseract`
- the Tesseract OCR program installed on your computer

On this project, the code is set up to look for Tesseract here on Windows:

```text
C:\Program Files\Tesseract-OCR\tesseract.exe
```

If OCR is not available, the app still works with pasted receipt text.

## Example receipt text

```text
Taco 10.89
Burrito 13.50
Starter 20.00
Drink 3.00
Tax 4.21
Total 51.60
```

## Example workflow

1. Upload a receipt image or paste receipt text.
2. Click `Detect Items`.
3. Enter names separated by commas.
4. Check which people share each item.
5. Add tax and tip percentages if needed.
6. Click `Calculate Split`.

## Known limitations

- OCR accuracy depends on receipt quality, lighting, and formatting.
- The parser is intentionally simple and works best when each item appears on its own line with a price.
- Tax and tip are split evenly across the group rather than proportionally by subtotal.
