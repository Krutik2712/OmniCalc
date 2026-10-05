document.addEventListener("DOMContentLoaded", () => {
    // -------------------------------------------------------------
    // Tab Switching
    // -------------------------------------------------------------
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanels = document.querySelectorAll(".tab-panel");

    tabButtons.forEach(btn => {
        btn.addEventListener("click", () => {
            const targetId = btn.getAttribute("data-tab");
            tabButtons.forEach(b => b.classList.remove("active"));
            tabPanels.forEach(p => p.classList.remove("active"));

            btn.classList.add("active");
            document.getElementById(targetId).classList.add("active");
        });
    });

    // -------------------------------------------------------------
    // Calculator State & Logic
    // -------------------------------------------------------------
    const calcExpressionEl = document.getElementById("calcExpression");
    const calcResultEl = document.getElementById("calcResult");
    const calcErrorEl = document.getElementById("calcError");
    const historyListEl = document.getElementById("historyList");
    const clearHistoryBtn = document.getElementById("clearHistoryBtn");

    let currentInput = "0";
    let storedOperand = null;
    let pendingOperation = null;
    let shouldResetInput = false;

    function showCalcError(msg) {
        calcErrorEl.textContent = msg;
        calcErrorEl.classList.remove("hidden");
    }

    function clearCalcError() {
        calcErrorEl.textContent = "";
        calcErrorEl.classList.add("hidden");
    }

    function updateCalcDisplay() {
        calcResultEl.textContent = currentInput;
        if (storedOperand !== null && pendingOperation) {
            const opSymbols = {
                add: "+",
                subtract: "−",
                multiply: "×",
                divide: "÷",
                power: "^"
            };
            calcExpressionEl.textContent = `${storedOperand} ${opSymbols[pendingOperation] || pendingOperation}`;
        } else {
            calcExpressionEl.textContent = "";
        }
    }

    async function sendCalculation(operation, num1, num2 = 0) {
        clearCalcError();
        try {
            const response = await fetch("/api/calculate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ operation, num1, num2 })
            });
            const data = await response.json();

            if (!data.success) {
                showCalcError(data.error || "Calculation failed.");
                return null;
            }

            // Add to history
            addHistoryItem(data.expression);
            return data.result;
        } catch (err) {
            showCalcError("Network or server error occurred.");
            return null;
        }
    }

    function addHistoryItem(exprText) {
        const emptyState = historyListEl.querySelector(".history-empty");
        if (emptyState) emptyState.remove();

        const li = document.createElement("li");
        li.className = "history-item";
        li.textContent = exprText;
        li.title = "Click to load result";
        li.addEventListener("click", () => {
            const parts = exprText.split("=");
            if (parts.length > 1) {
                currentInput = parts[1].trim();
                updateCalcDisplay();
            }
        });
        historyListEl.prepend(li);
    }

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener("click", () => {
            historyListEl.innerHTML = '<li class="history-empty">No calculations yet</li>';
        });
    }

    async function handleKeypadAction(action, value) {
        clearCalcError();

        if (action === "num") {
            if (currentInput === "0" || shouldResetInput) {
                currentInput = value;
                shouldResetInput = false;
            } else {
                currentInput += value;
            }
            updateCalcDisplay();
        } else if (action === "dot") {
            if (shouldResetInput) {
                currentInput = "0.";
                shouldResetInput = false;
            } else if (!currentInput.includes(".")) {
                currentInput += ".";
            }
            updateCalcDisplay();
        } else if (action === "clear") {
            currentInput = "0";
            storedOperand = null;
            pendingOperation = null;
            shouldResetInput = false;
            updateCalcDisplay();
        } else if (action === "backspace") {
            if (currentInput.length > 1) {
                currentInput = currentInput.slice(0, -1);
            } else {
                currentInput = "0";
            }
            updateCalcDisplay();
        } else if (action === "op") {
            const num = parseFloat(currentInput);

            // Single-operand operator (sqrt)
            if (value === "sqrt") {
                const res = await sendCalculation("sqrt", num);
                if (res !== null) {
                    currentInput = String(res);
                    calcExpressionEl.textContent = `√(${num}) = ${res}`;
                    shouldResetInput = true;
                    updateCalcDisplay();
                }
                return;
            }

            // If we already have a pending operation, evaluate it first
            if (storedOperand !== null && pendingOperation && !shouldResetInput) {
                const res = await sendCalculation(pendingOperation, storedOperand, num);
                if (res !== null) {
                    storedOperand = res;
                    currentInput = String(res);
                } else {
                    return;
                }
            } else {
                storedOperand = num;
            }

            pendingOperation = value;
            shouldResetInput = true;
            updateCalcDisplay();
        } else if (action === "calculate") {
            if (storedOperand !== null && pendingOperation) {
                const num2 = parseFloat(currentInput);
                const res = await sendCalculation(pendingOperation, storedOperand, num2);
                if (res !== null) {
                    calcExpressionEl.textContent = `${storedOperand} ${pendingOperation} ${num2} =`;
                    currentInput = String(res);
                    storedOperand = null;
                    pendingOperation = null;
                    shouldResetInput = true;
                    updateCalcDisplay();
                }
            }
        }
    }

    document.querySelectorAll(".keypad .btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const action = btn.getAttribute("data-action");
            const val = btn.getAttribute("data-value");
            handleKeypadAction(action, val);
        });
    });

    // Keyboard support for calculator
    window.addEventListener("keydown", (e) => {
        if (!document.getElementById("calculator-tab").classList.contains("active")) return;

        if (e.key >= "0" && e.key <= "9") {
            handleKeypadAction("num", e.key);
        } else if (e.key === ".") {
            handleKeypadAction("dot");
        } else if (e.key === "+" || e.key === "-") {
            handleKeypadAction("op", e.key === "+" ? "add" : "subtract");
        } else if (e.key === "*") {
            handleKeypadAction("op", "multiply");
        } else if (e.key === "/") {
            e.preventDefault();
            handleKeypadAction("op", "divide");
        } else if (e.key === "Enter" || e.key === "=") {
            e.preventDefault();
            handleKeypadAction("calculate");
        } else if (e.key === "Backspace") {
            handleKeypadAction("backspace");
        } else if (e.key === "Escape") {
            handleKeypadAction("clear");
        }
    });

    // -------------------------------------------------------------
    // Unit Converter State & Logic
    // -------------------------------------------------------------
    const categoryPills = document.querySelectorAll(".category-pills .pill-btn");
    const convValueInput = document.getElementById("convValue");
    const convFromSelect = document.getElementById("convFromUnit");
    const convToSelect = document.getElementById("convToUnit");
    const swapUnitsBtn = document.getElementById("swapUnitsBtn");
    const runConvertBtn = document.getElementById("runConvertBtn");
    const convResultCard = document.getElementById("convResultCard");
    const convResultValue = document.getElementById("convResultValue");
    const convResultFormula = document.getElementById("convResultFormula");
    const convErrorEl = document.getElementById("convError");

    let currentCategory = "length";
    const unitsData = window.SERVER_UNITS || {};

    function populateUnitDropdowns(category) {
        if (!unitsData[category]) return;
        const units = unitsData[category].units;

        convFromSelect.innerHTML = "";
        convToSelect.innerHTML = "";

        const keys = Object.keys(units);
        keys.forEach((unitKey, index) => {
            const optionFrom = document.createElement("option");
            optionFrom.value = unitKey;
            optionFrom.textContent = units[unitKey].name;
            convFromSelect.appendChild(optionFrom);

            const optionTo = document.createElement("option");
            optionTo.value = unitKey;
            optionTo.textContent = units[unitKey].name;
            convToSelect.appendChild(optionTo);
        });

        // Set default to-unit to second item if available
        if (keys.length > 1) {
            convToSelect.selectedIndex = 1;
        }
    }

    async function executeConversion() {
        convErrorEl.classList.add("hidden");
        const val = parseFloat(convValueInput.value);

        if (isNaN(val)) {
            convErrorEl.textContent = "Please enter a valid numeric value.";
            convErrorEl.classList.remove("hidden");
            convResultCard.classList.add("hidden");
            return;
        }

        const fromUnit = convFromSelect.value;
        const toUnit = convToSelect.value;

        try {
            const response = await fetch("/api/convert", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    category: currentCategory,
                    value: val,
                    from_unit: fromUnit,
                    to_unit: toUnit
                })
            });

            const data = await response.json();
            if (data.success) {
                convResultValue.textContent = data.result;
                convResultFormula.textContent = data.summary;
                convResultCard.classList.remove("hidden");
            } else {
                convErrorEl.textContent = data.error || "Conversion failed.";
                convErrorEl.classList.remove("hidden");
                convResultCard.classList.add("hidden");
            }
        } catch (err) {
            convErrorEl.textContent = "Failed to communicate with converter service.";
            convErrorEl.classList.remove("hidden");
            convResultCard.classList.add("hidden");
        }
    }

    // Category button clicks
    categoryPills.forEach(pill => {
        pill.addEventListener("click", () => {
            categoryPills.forEach(p => p.classList.remove("active"));
            pill.classList.add("active");
            currentCategory = pill.getAttribute("data-category");
            populateUnitDropdowns(currentCategory);
            executeConversion();
        });
    });

    // Swap units
    swapUnitsBtn.addEventListener("click", () => {
        const temp = convFromSelect.value;
        convFromSelect.value = convToSelect.value;
        convToSelect.value = temp;
        executeConversion();
    });

    runConvertBtn.addEventListener("click", executeConversion);
    convValueInput.addEventListener("input", executeConversion);
    convFromSelect.addEventListener("change", executeConversion);
    convToSelect.addEventListener("change", executeConversion);

    // Initial setup
    populateUnitDropdowns(currentCategory);
    executeConversion();
});
