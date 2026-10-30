from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import date

app = Flask(__name__)
DB = "fridge.db"


def get_items():
    """Read all items from the database, soonest-expiring first."""
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT * FROM items ORDER BY expiry_date").fetchall()
    conn.close()

    today = date.today()
    items = []
    for row in rows:
        item = dict(row)
        expiry = date.fromisoformat(item["expiry_date"])
        item["days_left"] = (expiry - today).days

        if item["days_left"] < 0:
            item["status"] = "expired"
        elif item["days_left"] <= 2:
            item["status"] = "soon"
        else:
            item["status"] = "fresh"

        items.append(item)
    return items


@app.route("/")
def home():
    return render_template("index.html", items=get_items())


@app.route("/add", methods=["POST"])
def add_item():
    """Save a new item from the form."""
    name = request.form["name"]
    quantity = request.form["quantity"]
    expiry_date = request.form["expiry_date"]

    conn = sqlite3.connect(DB)
    conn.execute(
        "INSERT INTO items (name, quantity, location, date_added, expiry_date) VALUES (?, ?, ?, ?, ?)",
        (name, quantity, "fridge", date.today().isoformat(), expiry_date),
    )
    conn.commit()
    conn.close()

    # Go back to the home page so the new item shows up
    return redirect(url_for("home"))


@app.route("/delete/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    """Remove an item (used it up or threw it out)."""
    conn = sqlite3.connect(DB)
    conn.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)