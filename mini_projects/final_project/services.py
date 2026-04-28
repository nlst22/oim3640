import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from io import BytesIO
from pathlib import Path


MONEY_RE = re.compile(r"(-?(?:\$\s*\d+(?:\s*[,\.]\s*\d{2})?|\d+\s*[,\.]\s*\d{2}))\s*$")
WINDOWS_TESSERACT_PATH = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
IGNORE_WORDS = {
    "subtotal",
    "sub total",
    "tax",
    "tip",
    "total",
    "balance",
    "change",
    "cash",
    "credit",
    "visa",
    "mastercard",
    "amex",
}
EXACT_IGNORE_WORDS = {"ta"}


def money(value):
    """Convert a value to a Decimal rounded like currency."""
    try:
        cleaned = str(value).replace("$", "").replace(" ", "").strip()
        if "," in cleaned and "." not in cleaned:
            cleaned = cleaned.replace(",", ".")
        else:
            cleaned = cleaned.replace(",", "")
        return Decimal(cleaned).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return Decimal("0.00")


def format_money(value):
    return f"{money(value):.2f}"


def parse_receipt_text(text):
    """
    Pull likely item names and prices from receipt text.

    This intentionally uses a simple pattern for the basic version:
    each item should be on a line that ends with a price.
    """
    items = []

    for raw_line in text.splitlines():
        line = " ".join(raw_line.strip().split())
        if not line:
            continue

        match = MONEY_RE.search(line)
        if not match:
            continue

        name = line[: match.start()].strip(" .:-")
        price = money(match.group(1))

        if not name or len(name) <= 2 or price <= 0:
            continue

        normalized_name = name.lower()
        alpha_name = " ".join(re.sub(r"[^a-zA-Z ]", " ", name).lower().split())
        if any(word == normalized_name or word in normalized_name for word in IGNORE_WORDS):
            continue
        if alpha_name in IGNORE_WORDS or alpha_name in EXACT_IGNORE_WORDS:
            continue

        items.append({"name": name.title(), "price": format_money(price)})

    return items


def extract_text_from_upload(file_storage):
    """
    Extract text from a user upload.

    Text files work without extra packages. Images use Pillow + pytesseract when
    those optional dependencies and the Tesseract program are installed.
    """
    if not file_storage or not file_storage.filename:
        return "", None

    filename = file_storage.filename.lower()
    data = file_storage.read()

    if filename.endswith((".txt", ".csv")):
        return data.decode("utf-8", errors="ignore"), None

    try:
        from PIL import Image, ImageOps
        import pytesseract
    except ImportError:
        return "", "Image OCR needs Pillow and pytesseract installed. You can paste receipt text instead."

    try:
        if WINDOWS_TESSERACT_PATH.exists():
            pytesseract.pytesseract.tesseract_cmd = str(WINDOWS_TESSERACT_PATH)

        image = Image.open(BytesIO(data))
        image = ImageOps.exif_transpose(image)
        image = ImageOps.grayscale(image)
        image = ImageOps.autocontrast(image)
        image = image.resize((image.width * 2, image.height * 2))

        text = pytesseract.image_to_string(image, config="--psm 6")
        return text, None
    except pytesseract.TesseractNotFoundError:
        return "", "Tesseract OCR was not found. Check that C:\\Program Files\\Tesseract-OCR\\tesseract.exe exists."
    except Exception as exc:
        return "", f"I could not read that image: {exc}"


def compute_total(subtotal, tax_pct, tip_pct):
    """Calculate tax, tip, and final total, adapted from Project 1."""
    subtotal = money(subtotal)
    tax = (subtotal * money(tax_pct) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    tip = (subtotal * money(tip_pct) / Decimal("100")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return tax, tip, subtotal + tax + tip


def calculate_itemized_split(items, people, tax_pct=0, tip_pct=0):
    """
    Calculate each person's total from assigned receipt items.

    Items assigned to Shared are split evenly across all people. Tax and tip are
    also split evenly, matching the itemized split workflow from Project 1.
    """
    cleaned_people = [person.strip() for person in people if person.strip()]
    if not cleaned_people:
        cleaned_people = ["Person 1", "Person 2"]

    base_totals = {person: Decimal("0.00") for person in cleaned_people}
    shared_total = Decimal("0.00")
    cleaned_items = []

    for item in items:
        name = item.get("name", "").strip() or "Receipt item"
        price = money(item.get("price", "0"))
        assigned_to = item.get("assigned_to", "Shared")
        if isinstance(assigned_to, str):
            assigned_people = [assigned_to] if assigned_to and assigned_to != "Shared" else []
        else:
            assigned_people = [person for person in assigned_to if person in base_totals]

        if price <= 0:
            continue

        if not assigned_people:
            shared_total += price
            assigned_label = "Shared"
        else:
            split_count = Decimal(len(assigned_people))
            split_amount = (price / split_count).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            running_total = split_amount * split_count
            remainder = price - running_total

            for index, person in enumerate(assigned_people):
                person_share = split_amount
                if index == len(assigned_people) - 1:
                    person_share += remainder
                base_totals[person] += person_share

            assigned_label = ", ".join(assigned_people)

        cleaned_items.append(
            {
                "name": name,
                "price": format_money(price),
                "assigned_to": assigned_label,
            }
        )

    shared_each = Decimal("0.00")
    if cleaned_people:
        shared_each = (shared_total / Decimal(len(cleaned_people))).quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    for person in cleaned_people:
        base_totals[person] += shared_each

    subtotal = sum(base_totals.values(), Decimal("0.00"))
    tax, tip, final_total = compute_total(subtotal, tax_pct, tip_pct)
    tax_each = (tax / Decimal(len(cleaned_people))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    tip_each = (tip / Decimal(len(cleaned_people))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    people_totals = []
    for person in cleaned_people:
        base = base_totals[person]
        people_totals.append(
            {
                "name": person,
                "base": format_money(base),
                "tax": format_money(tax_each),
                "tip": format_money(tip_each),
                "total": format_money(base + tax_each + tip_each),
            }
        )

    return {
        "items": cleaned_items,
        "people": people_totals,
        "shared_total": format_money(shared_total),
        "subtotal": format_money(subtotal),
        "tax": format_money(tax),
        "tip": format_money(tip),
        "final_total": format_money(final_total),
    }
