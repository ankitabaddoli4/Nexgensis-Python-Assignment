# Nexgensis-Python-Assignment
Python-based Mystery Delivery System for the Nexgensis Technologies assignment.

# 🚚 Mystery Delivery System

### Nexgensis Technologies — Python Developer Assignment

A Python-based simulation of a logistics delivery system for **FastBox**, a fictional logistics company. The system processes warehouse, delivery agent, and package data from JSON files, assigns packages to the nearest delivery agent, simulates package deliveries, calculates travel distances, and generates a final performance report.

---

## 📌 Assignment Overview

FastBox operates multiple warehouses and delivery agents across a city.

The objective of this assignment is to simulate one working day of deliveries and determine:

* Which packages were delivered by each agent
* The total distance travelled by each agent
* The average distance travelled per delivered package
* The most efficient delivery agent

The application accepts JSON input files so that different delivery scenarios can be tested without changing the source code.

---

## 🎯 Objectives

The project implements the following core requirements:

1. Read and parse delivery data from a JSON file.
2. Store warehouses, agents, and packages using structured Python data models.
3. Calculate Euclidean distances between coordinates.
4. Assign each package to the nearest agent based on the agent's distance from the package's warehouse.
5. Simulate package pickup and delivery.
6. Calculate total delivery distance for every agent.
7. Calculate delivery efficiency.
8. Identify the most efficient agent.
9. Generate a JSON report.
10. Validate that every package has been delivered exactly once.
11. Provide automated unit tests.
12. Support multiple JSON test cases without changing the application code.

---

## 🛠️ Technologies Used

* **Python 3**
* Python Standard Library
* `json` — JSON parsing and report generation
* `math` — Euclidean distance calculations
* `dataclasses` — structured data models
* `argparse` — command-line interface
* `unittest` — automated testing
* `csv` — optional top-performer CSV report
* Git & GitHub

No external Python packages are required.

---

## 📂 Project Structure

```text
Nexgensis-Python-Assignment/
│
├── data/
│   ├── base_case.json
│   ├── test_case_1.json
│   ├── test_case_2.json
│   ├── test_case_3.json
│   └── ...
│
├── src/
│   ├── __init__.py
│   ├── models.py
│   ├── loader.py
│   ├── distance.py
│   ├── assignment.py
│   ├── simulator.py
│   ├── report.py
│   └── main.py
│
├── tests/
│   └── test_delivery_systems.py
│
├── output/
│   └── report.json
│
├── screenshots/
│   ├── 01_base_case_output.png
│   ├── 02_unit_tests_passed.png
│   ├── 03_test_case_1_output.png
│   └── 04_report_json.png
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🧩 Module Description

### `src/models.py`

Defines the main data structures using Python dataclasses:

* `Warehouse`
* `Agent`
* `Package`
* `DeliveryRecord`

This keeps the application data organized and type-safe.

---

### `src/loader.py`

Responsible for loading and validating JSON input.

It supports:

* Warehouse data
* Agent data
* Package data
* Coordinate validation
* Missing-field validation
* Duplicate ID validation
* Unknown warehouse validation
* Invalid JSON detection
* File existence validation

The loader also supports both dictionary-style and list-style warehouse/agent representations.

---

### `src/distance.py`

Contains the Euclidean distance calculation.

The distance between two points `(x1, y1)` and `(x2, y2)` is calculated as:

```text
distance = √((x2 - x1)² + (y2 - y1)²)
```

For example:

```text
(0, 0) → (3, 4)

distance = √(3² + 4²)
         = 5
```

---

### `src/assignment.py`

Assigns every package to the nearest delivery agent.

For each package:

1. Identify its warehouse.
2. Calculate the distance from every agent to that warehouse.
3. Select the nearest agent.
4. Store the package under that agent.
5. Use agent ID as a deterministic tie-breaker when distances are equal.

The basic assignment process has a time complexity of approximately:

```text
O(P × A)
```

where:

* `P` = number of packages
* `A` = number of agents

---

### `src/simulator.py`

Simulates the actual delivery process.

For every assigned package, the system calculates:

```text
Agent → Warehouse
+
Warehouse → Destination
```

The resulting package distance is added to the agent's total distance.

The agent's simulated location is then updated to the delivered package's destination before processing its next assigned package.

---

### `src/report.py`

Generates the final delivery report.

For every agent, the report contains:

* Number of packages delivered
* Total distance travelled
* Average distance per package

Efficiency is calculated as:

```text
efficiency = total_distance / packages_delivered
```

The agent with the lowest efficiency value among agents who delivered at least one package is selected as `best_agent`.

The report is saved as:

```text
output/report.json
```

The module also supports an optional CSV output for the top performer.

---

### `src/main.py`

Provides the command-line interface and connects all modules together.

The complete workflow is:

```text
Load JSON
   ↓
Validate Input
   ↓
Assign Packages
   ↓
Simulate Deliveries
   ↓
Validate Delivery Count
   ↓
Generate Report
   ↓
Save report.json
```

---

# 📥 Input Format

The application accepts JSON files containing:

* Warehouses
* Agents
* Packages

Example:

```json
{
    "warehouses": {
        "W1": [0, 0],
        "W2": [50, 75],
        "W3": [100, 25]
    },
    "agents": {
        "A1": [5, 5],
        "A2": [60, 60],
        "A3": [95, 30]
    },
    "packages": [
        {
            "id": "P1",
            "warehouse": "W1",
            "destination": [30, 40]
        },
        {
            "id": "P2",
            "warehouse": "W2",
            "destination": [70, 90]
        }
    ]
}
```

The loader also accepts the package field:

```json
"warehouse_id": "W1"
```

in addition to:

```json
"warehouse": "W1"
```

---

# 📤 Output Format

The application generates `output/report.json`.

Example structure:

```json
{
    "A1": {
        "packages_delivered": 2,
        "total_distance": 121.21,
        "efficiency": 60.61
    },
    "A2": {
        "packages_delivered": 2,
        "total_distance": 79.21,
        "efficiency": 39.6
    },
    "A3": {
        "packages_delivered": 1,
        "total_distance": 14.14,
        "efficiency": 14.14
    },
    "best_agent": "A3"
}
```

---

# ▶️ How to Run

## 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Nexgensis-Python-Assignment.git
```

Move into the project directory:

```bash
cd Nexgensis-Python-Assignment
```

---

## 2. Run the base case

```bash
python -m src.main --input data/base_case.json
```

The program prints a delivery summary and generates:

```text
output/report.json
```

---

## 3. Run another test case

For example:

```bash
python -m src.main --input data/test_case_1.json
```

The same command structure can be used with the other JSON test cases.

---

## 4. Specify a custom output file

```bash
python -m src.main --input data/base_case.json --output output/custom_report.json
```

---

## 5. Generate optional CSV output

The project includes an optional top-performer CSV report.

```bash
python -m src.main --input data/base_case.json --csv output/top_performer.csv
```

This produces a CSV containing:

```text
agent_id
packages_delivered
total_distance
efficiency
```

---

# 🧪 Testing

The project includes automated unit tests using Python's built-in `unittest` framework.

Run all tests with:

```bash
python -m unittest discover -s tests -v
```

Current test coverage includes:

* Euclidean distance calculation
* JSON data loading
* Nearest-agent assignment
* Package delivery validation
* Report generation
* Best-agent identification

Expected result:

```text
Ran 5 tests

OK
```

---

# 🔍 Delivery Validation

The application performs additional validation after simulation.

It verifies that:

```text
Number of delivered packages
=
Number of input packages
```

It also checks that package IDs are unique in the delivery records.

This prevents silent loss or duplicate delivery of packages.

---

# ⚙️ Design Assumptions

The assignment leaves some details of the delivery route open to interpretation. The following assumptions are therefore used:

### 1. Agent Assignment

A package is assigned to the agent with the shortest Euclidean distance from the agent's current position to the package's warehouse.

### 2. Delivery Route

For each assigned package, the simulated route is:

```text
Agent's current location
        ↓
Warehouse
        ↓
Package destination
```

### 3. Agent Position

After delivering a package, the agent's location becomes that package's destination.

Therefore, the next package handled by the same agent starts from the previous delivery destination.

### 4. Multiple Packages

Packages assigned to the same agent are processed in deterministic package-ID order.

### 5. Tie Handling

If two agents are equally close to a warehouse, the agent with the lexicographically smaller agent ID is selected.

### 6. Efficiency

Efficiency is represented as average distance travelled per delivered package:

```text
Total Distance / Packages Delivered
```

A lower value represents fewer distance units travelled per package.

### 7. Agents Without Packages

Agents who do not receive any packages are included in the report with:

```text
packages_delivered = 0
total_distance = 0
efficiency = 0
```

They are not considered when selecting `best_agent`.

---

# 📊 Example Console Output

```text
============================================================
FASTBOX DELIVERY REPORT
============================================================
A1: 2 packages | 121.21 distance | 60.61 per package
A2: 2 packages | 79.21 distance | 39.60 per package
A3: 1 packages | 14.14 distance | 14.14 per package
------------------------------------------------------------
Best agent: A3
============================================================

Report saved to:
output/report.json
```

---

# 🏗️ Architecture

The project follows a modular architecture:

```text
                 ┌──────────────────┐
                 │   JSON Input     │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Loader       │
                 │ Validation/Parse │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   Assignment     │
                 │ Nearest Agent    │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │    Simulator     │
                 │ Pickup/Delivery  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │     Report       │
                 │ Metrics/Ranking  │
                 └────────┬─────────┘
                          │
                          ▼
                 ┌──────────────────┐
                 │   report.json    │
                 └──────────────────┘
```

---

# 💡 Key Python Concepts Demonstrated

This assignment demonstrates practical Python development concepts including:

* JSON parsing
* File handling
* Dataclasses
* Type hints
* Lists and dictionaries
* Functions and modular design
* Euclidean distance calculations
* Sorting and minimum selection
* Command-line arguments
* Input validation
* Exception handling
* Unit testing
* CSV generation
* Deterministic algorithms
* Separation of concerns

---

# 🚀 Optional Extension

The architecture can be extended to support additional logistics features such as:

* Random delivery delays
* Delivery timestamps
* ASCII route visualization
* New agents joining during the day
* Top-performer CSV reports
* Delivery status tracking
* Additional distance metrics
* Larger delivery datasets

The current implementation keeps the core assignment logic simple and deterministic while leaving room for future extensions.

---

# 📸 Screenshots

The `screenshots/` directory contains evidence of the application running:

### `01_base_case_output.png`

Shows the application running with the base input.

### `02_unit_tests_passed.png`

Shows the automated unit tests completing successfully.

### `03_test_case_1_output.png`

Shows the application running with an additional test dataset.

### `04_report_json.png`

Shows the generated `output/report.json`.

---

# 📦 Dependencies

The project uses only Python's standard library.

No third-party packages are required.

Therefore:

```bash
pip install -r requirements.txt
```

is optional and will not install external dependencies.

---

# 👩‍💻 Assignment

**Company:** Nexgensis Technologies
**Role:** Python Developer
**Assignment:** Mystery Delivery System
**Language:** Python
**Submission:** GitHub Repository

---

# 📝 Conclusion

The Mystery Delivery System provides a modular simulation of a logistics company's daily delivery operations.

It reads structured delivery data, validates the input, assigns packages to nearby agents, simulates deliveries, calculates distance and efficiency metrics, verifies that all packages were delivered, and produces a machine-readable JSON report.

The project is designed to be reusable with different JSON datasets while maintaining clear separation between data loading, distance calculation, package assignment, delivery simulation, reporting, and testing.
