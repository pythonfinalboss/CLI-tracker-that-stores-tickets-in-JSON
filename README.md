# CLI Ticket Tracker

A lightweight Command-Line Interface (CLI) Ticket Management System built in Python.

## Structure

- **`day1.py`**: Initial ticket data structure using Python dictionaries.
- **`day2.py`**: Multi-ticket creation loop with list storage and formatted console output.
- **`day3.py`**: Modular menu-driven application with options to create and view tickets.
- **`day4.py`**: Persistent storage using JSON files (`tickets.json`) and ticket resolution feature.
- **`day5.py`**: Advanced management featuring ticket timestamps, card formatting, filtering (by status, priority, keyword), ticket resolution, and deletion.
- **`day6.py`**: Object-Oriented Programming (OOP) refactor introducing `Ticket` and `TicketManager` classes with an interactive menu.
- **`day7.py`**: Command-line interface built with `argparse` supporting subcommands (`add`, `list`, `resolve`, `delete`) and filtering flags.

## Getting Started

Run the CLI ticket tracker using `day7.py`:

```bash
# Add a ticket
python day7.py add "Database connection timeout" --priority High

# List tickets (with optional filters)
python day7.py list
python day7.py list --status Open --priority High

# Resolve a ticket
python day7.py resolve 1

# Delete a ticket
python day7.py delete 1
```
