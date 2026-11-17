import os
import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get(
    "SECRET_KEY", "local-development-only"
)

DATABASE = Path(__file__).with_name("inventory.db")


@app.route("/")
def home():
    return redirect(url_for("inventory"))


@app.route("/inventory", methods=["GET", "POST"])
def inventory():
    demo_mode = os.environ.get("DEMO_MODE") == "1"

    if request.method == "POST":
        if demo_mode:
            return "Demo changes are handled in the browser.", 403    
        component = request.form.get("component", "")
        action = request.form.get("action", "")
        raw_units = request.form.get("units", "")

        try:
            units = int(raw_units)

            if units <= 0:
                raise ValueError

        except ValueError:
            flash("Please enter a positive whole number.")
            return redirect(url_for("inventory"))

        connection = sqlite3.connect(DATABASE)

        try:
            if action == "receive":
                cursor = connection.execute(
                    """UPDATE inventory
                       SET quantity = quantity + ?
                       WHERE component = ?""",
                    (units, component)
                )

            elif action == "issue":
                cursor = connection.execute(
                    """UPDATE inventory
                       SET quantity = quantity - ?
                       WHERE component = ?
                       AND quantity >= ?""",
                    (units, component, units)
                )

            else:
                flash("Invalid inventory operation.")
                return redirect(url_for("inventory"))

            if cursor.rowcount == 1:
                connection.commit()
                flash("Inventory updated successfully!")
            else:
                flash("Component not found or insufficient stock.")

        finally:
            connection.close()

        return redirect(url_for("inventory"))

    connection = sqlite3.connect(DATABASE)

    try:
        rows = connection.execute(
            "SELECT component, quantity, location FROM inventory ORDER BY id"
        ).fetchall()
    finally:
        connection.close()

    total_components = len(rows)
    total_units = sum(row[1] for row in rows)
    low_stock = sum(1 for row in rows if row[1] < 10)

    return render_template(
        "inventory.html",
        rows=rows,
        total_components=total_components,
        total_units=total_units,
        low_stock=low_stock,
        demo_mode=demo_mode
    )


if __name__ == "__main__":
    app.run(debug=True)
