import os
from flask import Flask, render_template, request, jsonify
from converters import UNIT_DEFINITIONS, calculate, convert_unit

app = Flask(__name__)


@app.route("/")
def index():
    """Serves the main calculator and unit converter webpage."""
    return render_template(
        "index.html",
        unit_definitions=UNIT_DEFINITIONS
    )


@app.route("/api/units", methods=["GET"])
def get_units():
    """API endpoint to get available unit categories and supported units."""
    return jsonify({
        "success": True,
        "categories": UNIT_DEFINITIONS
    })


@app.route("/api/calculate", methods=["POST"])
def api_calculate():
    """API endpoint to execute arithmetic operations."""
    data = request.get_json(silent=True) or request.form

    operation = data.get("operation", "").strip()
    num1_raw = data.get("num1")
    num2_raw = data.get("num2", 0)

    if not operation or num1_raw is None:
        return jsonify({
            "success": False,
            "error": "Missing required fields: 'operation' and 'num1' are required."
        }), 400

    try:
        num1 = float(num1_raw)
        num2 = float(num2_raw) if num2_raw not in (None, "") else 0.0
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Operands must be valid numbers."
        }), 400

    try:
        result, expression = calculate(operation, num1, num2)
        return jsonify({
            "success": True,
            "result": result,
            "expression": expression,
            "operation": operation,
            "num1": num1,
            "num2": num2
        })
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except OverflowError:
        return jsonify({
            "success": False,
            "error": "Calculation result caused an overflow error."
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500


@app.route("/api/convert", methods=["POST"])
def api_convert():
    """API endpoint to convert units across multiple measurement categories."""
    data = request.get_json(silent=True) or request.form

    category = data.get("category", "").strip()
    value_raw = data.get("value")
    from_unit = data.get("from_unit", "").strip()
    to_unit = data.get("to_unit", "").strip()

    if not all([category, from_unit, to_unit]) or value_raw is None:
        return jsonify({
            "success": False,
            "error": "Missing required fields: 'category', 'value', 'from_unit', and 'to_unit' are all required."
        }), 400

    try:
        value = float(value_raw)
    except (ValueError, TypeError):
        return jsonify({
            "success": False,
            "error": "Value to convert must be a valid number."
        }), 400

    try:
        result, summary = convert_unit(category, value, from_unit, to_unit)
        return jsonify({
            "success": True,
            "category": category,
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "result": result,
            "summary": summary
        })
    except ValueError as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"An unexpected error occurred: {str(e)}"
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
