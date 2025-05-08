# expense_chart
# Expense Tracker

A simple desktop application built with Python and Tkinter to help users track and manage their expenses.

## Features

- Add expenses with details including name, date, amount, and category
- Categorize expenses into different types (Food, Transport, Utilities, etc.)
- View monthly expense summaries
- Export expenses to CSV file
- Visualize expense distribution using bar charts
- User-friendly graphical interface

## Requirements

- Python 3.x
- Required Python packages:
  - tkinter
  - tkcalendar
  - matplotlib
  - sqlite3 (included in Python standard library)

## Installation

1. Clone this repository or download the source code
2. Install the required packages:
```bash
pip install tkcalendar matplotlib
```

## Usage

1. Run the program:
```bash
python expense.py
```

2. The application window will open with the following features:
   - Add new expenses using the form at the top
   - Select a month and year to view monthly summaries
   - Export your expenses to CSV using the "Export to CSV" button
   - View expense distribution charts using the "Show Graph" button

## Data Storage

- All expenses are stored in a SQLite database (`expense.db`)
- Data can be exported to CSV format for backup or analysis

## Categories

The application supports the following expense categories:
- Food
- Transport
- Utilities
- Entertainment
- Shopping
- Healthcare
- Rent
- Education
- Other

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.

## License

This project is open source and available under the MIT License.
