from flask import Flask, render_template_string, request, redirect
import csv
from datetime import datetime

app = Flask(__name__)

# In-memory storage (resets on restart)
transactions = []

# HTML template (inline for simplicity)
template = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple Expense Tracker</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container py-4">
    <h2 class="mb-4 text-center">💰 Simple Expense Tracker</h2>

    <!-- Form -->
    <form method="POST" action="/add" class="row g-3 mb-4">
        <div class="col-md-3">
            <input type="date" name="date" class="form-control" required>
        </div>
        <div class="col-md-3">
            <select name="type" class="form-control" required>
                <option value="Income">Income</option>
                <option value="Expense">Expense</option>
            </select>
        </div>
        <div class="col-md-3">
            <input type="number" name="amount" placeholder="Amount" class="form-control" required>
        </div>
        <div class="col-md-3">
            <input type="text" name="note" placeholder="Note" class="form-control">
        </div>
        <div class="col-12 text-center">
            <button class="btn btn-primary">Add Transaction</button>
        </div>
    </form>

    <!-- Summary -->
    <div class="row text-center mb-4">
        <div class="col">
            <h5>Total Income</h5>
            <p class="text-success fw-bold">₹ {{ income }}</p>
        </div>
        <div class="col">
            <h5>Total Expenses</h5>
            <p class="text-danger fw-bold">₹ {{ expense }}</p>
        </div>
        <div class="col">
            <h5>Balance</h5>
            <p class="fw-bold">₹ {{ balance }}</p>
        </div>
    </div>

    <!-- Transaction Table -->
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Date</th><th>Type</th><th>Amount</th><th>Note</th>
            </tr>
        </thead>
        <tbody>
            {% for t in transactions %}
            <tr>
                <td>{{ t['date'] }}</td>
                <td>{{ t['type'] }}</td>
                <td>{{ t['amount'] }}</td>
                <td>{{ t['note'] }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <!-- Export -->
    <form method="GET" action="/export">
        <button class="btn btn-success">Download CSV</button>
    </form>
</body>
</html>
"""

@app.route("/")
def index():
    income = sum(float(t['amount']) for t in transactions if t['type'] == "Income")
    expense = sum(float(t['amount']) for t in transactions if t['type'] == "Expense")
    balance = income - expense
    return render_template_string(template, transactions=transactions, income=income, expense=expense, balance=balance)

@app.route("/add", methods=["POST"])
def add():
    transactions.append({
        "date": request.form["date"],
        "type": request.form["type"],
        "amount": request.form["amount"],
        "note": request.form["note"]
    })
    return redirect("/")

@app.route("/export")
def export():
    filename = "transactions.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "type", "amount", "note"])
        writer.writeheader()
        writer.writerows(transactions)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
