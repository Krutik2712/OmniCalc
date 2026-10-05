import math
from typing import Dict, Any, Tuple

# Supported unit conversion factors relative to a base unit
# Base units:
# - length: meter (m)
# - weight: gram (g)
# - data: byte (B)

UNIT_DEFINITIONS: Dict[str, Dict[str, Any]] = {
    "length": {
        "label": "Length",
        "base": "meters",
        "units": {
            "meters": {"name": "Meters (m)", "to_base": 1.0},
            "kilometers": {"name": "Kilometers (km)", "to_base": 1000.0},
            "centimeters": {"name": "Centimeters (cm)", "to_base": 0.01},
            "millimeters": {"name": "Millimeters (mm)", "to_base": 0.001},
            "miles": {"name": "Miles (mi)", "to_base": 1609.344},
            "yards": {"name": "Yards (yd)", "to_base": 0.9144},
            "feet": {"name": "Feet (ft)", "to_base": 0.3048},
            "inches": {"name": "Inches (in)", "to_base": 0.0254},
        }
    },
    "weight": {
        "label": "Weight / Mass",
        "base": "grams",
        "units": {
            "grams": {"name": "Grams (g)", "to_base": 1.0},
            "kilograms": {"name": "Kilograms (kg)", "to_base": 1000.0},
            "milligrams": {"name": "Milligrams (mg)", "to_base": 0.001},
            "pounds": {"name": "Pounds (lbs)", "to_base": 453.59237},
            "ounces": {"name": "Ounces (oz)", "to_base": 28.349523},
        }
    },
    "temperature": {
        "label": "Temperature",
        "base": "celsius",
        "units": {
            "celsius": {"name": "Celsius (°C)"},
            "fahrenheit": {"name": "Fahrenheit (°F)"},
            "kelvin": {"name": "Kelvin (K)"},
        }
    },
    "data": {
        "label": "Digital Storage",
        "base": "bytes",
        "units": {
            "bytes": {"name": "Bytes (B)", "to_base": 1.0},
            "kilobytes": {"name": "Kilobytes (KB)", "to_base": 1024.0},
            "megabytes": {"name": "Megabytes (MB)", "to_base": 1024.0 ** 2},
            "gigabytes": {"name": "Gigabytes (GB)", "to_base": 1024.0 ** 3},
            "terabytes": {"name": "Terabytes (TB)", "to_base": 1024.0 ** 4},
        }
    }
}


def calculate(operation: str, num1: float, num2: float = 0.0) -> Tuple[float, str]:
    """
    Performs arithmetic operations.
    Returns: (result, expression_string)
    """
    op = operation.lower().strip()

    if op in ("add", "+"):
        res = num1 + num2
        expr = f"{num1:g} + {num2:g} = {res:g}"
        return res, expr

    elif op in ("subtract", "-"):
        res = num1 - num2
        expr = f"{num1:g} - {num2:g} = {res:g}"
        return res, expr

    elif op in ("multiply", "*"):
        res = num1 * num2
        expr = f"{num1:g} × {num2:g} = {res:g}"
        return res, expr

    elif op in ("divide", "/"):
        if num2 == 0:
            raise ValueError("Division by zero is undefined.")
        res = num1 / num2
        expr = f"{num1:g} ÷ {num2:g} = {res:g}"
        return res, expr

    elif op in ("power", "^"):
        # Prevent overly massive powers that would cause OverflowError
        if abs(num2) > 1000:
            raise ValueError("Exponent is too large.")
        res = math.pow(num1, num2)
        expr = f"{num1:g} ^ {num2:g} = {res:g}"
        return res, expr

    elif op in ("modulo", "%"):
        if num2 == 0:
            raise ValueError("Modulo by zero is undefined.")
        res = num1 % num2
        expr = f"{num1:g} mod {num2:g} = {res:g}"
        return res, expr

    elif op in ("sqrt", "√"):
        if num1 < 0:
            raise ValueError("Square root of a negative number is not real.")
        res = math.sqrt(num1)
        expr = f"√({num1:g}) = {res:g}"
        return res, expr

    elif op in ("percentage", "pct"):
        res = (num1 * num2) / 100.0
        expr = f"{num1:g}% of {num2:g} = {res:g}"
        return res, expr

    else:
        raise ValueError(f"Unknown operation: '{operation}'")


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Helper to convert temperatures between Celsius, Fahrenheit, and Kelvin."""
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    if from_unit == to_unit:
        return value

    # Step 1: Convert to Celsius
    if from_unit == "celsius":
        celsius = value
    elif from_unit == "fahrenheit":
        celsius = (value - 32.0) * 5.0 / 9.0
    elif from_unit == "kelvin":
        celsius = value - 273.15
    else:
        raise ValueError(f"Unsupported temperature unit: '{from_unit}'")

    # Step 2: Convert Celsius to target unit
    if to_unit == "celsius":
        return celsius
    elif to_unit == "fahrenheit":
        return (celsius * 9.0 / 5.0) + 32.0
    elif to_unit == "kelvin":
        return celsius + 273.15
    else:
        raise ValueError(f"Unsupported temperature unit: '{to_unit}'")


def convert_unit(category: str, value: float, from_unit: str, to_unit: str) -> Tuple[float, str]:
    """
    Converts a value between two units in a given category.
    Returns: (converted_value, formatted_summary)
    """
    category = category.lower().strip()
    from_unit = from_unit.lower().strip()
    to_unit = to_unit.lower().strip()

    if category not in UNIT_DEFINITIONS:
        raise ValueError(f"Invalid category '{category}'. Available: {list(UNIT_DEFINITIONS.keys())}")

    cat_data = UNIT_DEFINITIONS[category]
    units_dict = cat_data["units"]

    if from_unit not in units_dict:
        raise ValueError(f"Unit '{from_unit}' not found in category '{category}'")
    if to_unit not in units_dict:
        raise ValueError(f"Unit '{to_unit}' not found in category '{category}'")

    if category == "temperature":
        result = convert_temperature(value, from_unit, to_unit)
    else:
        from_factor = units_dict[from_unit]["to_base"]
        to_factor = units_dict[to_unit]["to_base"]
        # Convert to base unit, then to target unit
        base_value = value * from_factor
        result = base_value / to_factor

    from_label = units_dict[from_unit]["name"]
    to_label = units_dict[to_unit]["name"]
    summary = f"{value:g} {from_label} = {result:.6g} {to_label}"

    return round(result, 8), summary
