# SauceDemo Test Automation

The project automates functional testing of the [SauceDemo](https://www.saucedemo.com/) website using **Selenium WebDriver**, **pytest** and **Page Object Model (POM)**.

---

## Contents

- [Technologies](#technologies)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Reports](#reports)
- [Project Structure](#project-structure)
- [Conventions](#conventions)
- [Sample Tests](#sample-tests)

---

## Technologies

- Python 3.11+
- Selenium 4.x
- pytest 8.x
- webdriver-manager 4.x
- Firefox / Chrome
- pytest-html (raporty w HTML)

---

## Installation

1. Clone repository:

```bash
git clone <repo-url>
cd <project-folder>
```
2. Create virtual environment:
```bash
python -m venv .venv
```
3.Activate virtual environment:
Windows
```bash
.venv\Scripts\activate
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running Tests
```bash
pytest -v
```
- Tests use Firefox by default.
- All tests automatically open the browser, perform actions, and close it after the test.

## Reports
You can generate reports in HTML using pytest-html:
```bash
pytest --html=reports/report.html --self-contained-html
```
The report will be saved in the reports/ folder (you'll need to create it if it doesn't exist). It contains test details, results, etc.

## Project Structure
```
project/
│
├── core/                 # Configuration and global settings
│   └── config.py         # URLs, test data, constants
│
├── pages/                # Page Object Models
│   ├── base_page.py
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
│
├── tests/                # Automated tests
│   ├── test_login.py
│   ├── test_inventory.py
│   ├── test_cart.py
│   └── test_checkout.py
│
├── conftest.py           # Pytest fixtures
├── requirements.txt      # Dependency list
├── reports/              # HTML test reports
└── README.md             # Documentation
```
## Conventions
- Page Object Model – each page has its own class in pages/.
- Private locators begin with __, helper methods begin with _.
- Public methods describe user actions (e.g., login, add_to_cart, checkout_overview).
- checkout_overview).
- Configuration data (URLs, logins, passwords) is located in core/config.py.

## Sample Tests
- Login success and failure (test_login.py)
- Sorting products by name and price (test_inventory.py)
- Adding/removing products from the cart (test_cart.py)
- Checkout and price total verification (test_checkout.py)