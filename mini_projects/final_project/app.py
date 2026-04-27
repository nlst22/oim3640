import json
import os

from flask import Flask, render_template, request

try:
    from .services import calculate_itemized_split, extract_text_from_upload, parse_receipt_text
except ImportError:
    from services import calculate_itemized_split, extract_text_from_upload, parse_receipt_text


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "receipt-splitter-dev"
    app.config["APP_VERSION"] = "OCR debug version 3"

    @app.context_processor
    def inject_app_version():
        return {"app_version": app.config["APP_VERSION"]}

    @app.route("/", methods=["GET", "POST"])
    def index():
        detected_items = []
        receipt_text = ""
        message = None
        error = None

        if request.method == "POST":
            uploaded_text, upload_error = extract_text_from_upload(request.files.get("receipt_file"))
            typed_text = request.form.get("receipt_text", "").strip()
            receipt_text = uploaded_text.strip() or typed_text

            if upload_error:
                message = upload_error
            elif uploaded_text.strip():
                message = f"OCR extracted {len(uploaded_text.strip())} characters. You can edit the text below before detecting again."

            detected_items = parse_receipt_text(receipt_text)
            if not receipt_text:
                error = "Upload a receipt file or paste receipt text to start."
            elif not detected_items:
                error = "OCR ran, but no item lines were detected. Check the extracted text below or add items manually."

        return render_template(
            "index.html",
            detected_items=detected_items,
            receipt_text=receipt_text,
            message=message,
            error=error,
        )

    @app.route("/split", methods=["POST"])
    def split():
        people_raw = request.form.get("people", "")
        people = [name.strip() for name in people_raw.split(",") if name.strip()]

        names = request.form.getlist("item_name")
        prices = request.form.getlist("item_price")
        assigned = request.form.getlist("assigned_to")

        items = []
        for name, price, assigned_to in zip(names, prices, assigned):
            if name.strip() or price.strip():
                items.append(
                    {
                        "name": name,
                        "price": price,
                        "assigned_to": assigned_to,
                    }
                )

        result = calculate_itemized_split(
            items=items,
            people=people,
            tax_pct=request.form.get("tax_pct", "0"),
            tip_pct=request.form.get("tip_pct", "0"),
        )

        return render_template(
            "results.html",
            result=result,
            people=people,
            original_items=json.dumps(items),
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", "5000")), use_reloader=False)
