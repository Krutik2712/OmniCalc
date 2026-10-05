# OmniCalc & Unit Hub (Flask Application)

A modern, responsive Python web application built with **Flask** that performs mathematical arithmetic calculations and multi-category unit conversions. It features an interactive web interface as well as clean JSON REST API endpoints.

---

## 🚀 Features

1. **Calculator Hub**:
   - Arithmetic operations: Addition (`+`), Subtraction (`−`), Multiplication (`×`), Division (`÷`).
   - Advanced functions: Power (`xʸ`), Square Root (`√`), Modulo (`%`).
   - Interactive onscreen keypad + physical keyboard support.
   - Calculation history panel with clickable past expressions to reload results.
   - Safe division-by-zero and domain error handling.

2. **Unit Converter**:
   - **Length**: Meters, Kilometers, Centimeters, Millimeters, Miles, Yards, Feet, Inches.
   - **Weight / Mass**: Grams, Kilograms, Milligrams, Pounds, Ounces.
   - **Temperature**: Celsius, Fahrenheit, Kelvin.
   - **Digital Storage**: Bytes, Kilobytes, Megabytes, Gigabytes, Terabytes.
   - Live dynamic result update and instant unit swap button (`⇄`).

3. **REST API Endpoints**:
   - `GET /api/units`: Returns all available categories and conversion factors.
   - `POST /api/calculate`: JSON API for math calculations.
   - `POST /api/convert`: JSON API for unit conversions.

---

## 📁 Project Structure

```text
flask-calculator-app/
├── app.py              # Flask server routes and entry point
├── converters.py       # Core mathematical and unit conversion logic
├── requirements.txt    # Project dependencies
├── test_app.py         # Automated unit test suite
├── templates/
│   └── index.html      # Frontend HTML template (Jinja2)
└── static/
    ├── style.css       # Responsive styling with glassmorphism theme
    └── script.js       # Client-side reactivity and API integrations
```

---

## 🛠️ How to Run the Application

### 1. (Optional) Create & Activate Virtual Environment
```bash
# In the project directory:
python -m venv venv

# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Windows Command Prompt:
.\venv\Scripts\activate.bat
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start the Flask Server
```bash
python app.py
```
Open your web browser and navigate to:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 🧪 Running Automated Tests

Run the test suite with:
```bash
python -m unittest test_app.py
```

---

## 🔌 API Quick Reference

### Calculate
```bash
curl -X POST http://localhost:5000/api/calculate \
  -H "Content-Type: application/json" \
  -d '{"operation": "multiply", "num1": 12, "num2": 8}'
```
**Response:**
```json
{
  "expression": "12 \u00d7 8 = 96",
  "num1": 12.0,
  "num2": 8.0,
  "operation": "multiply",
  "result": 96.0,
  "success": true
}
```

### Convert Units
```bash
curl -X POST http://localhost:5000/api/convert \
  -H "Content-Type: application/json" \
  -d '{"category": "length", "value": 10, "from_unit": "kilometers", "to_unit": "miles"}'
```
**Response:**
```json
{
  "category": "length",
  "from_unit": "kilometers",
  "result": 6.213712,
  "summary": "10 Kilometers (km) = 6.21371 Miles (mi)",
  "success": true,
  "to_unit": "miles",
  "value": 10.0
}
```
