import argparse
import json
import os
from datetime import datetime

FILE_NAME = "tickets.json"


class Ticket:
    """Represents a single support ticket."""
    def __init__(self, ticket_id, issue, priority, status="Open", created_at=None):
        self.id = ticket_id
        self.issue = issue
        self.priority = priority
        self.status = status
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M")

    def resolve(self):
        self.status = "Closed"

    def to_dict(self):
        return {
            "id": self.id,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            ticket_id=data["id"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "Open"),
            created_at=data.get("created_at")
        )

    def display(self):
        print(f"Ticket #{self.id} | [{self.status}] | Priority: {self.priority} | Created: {self.created_at}")
        print(f"Issue: {self.issue}")
        print("-" * 65)


class TicketManager:
    """Manages file storage and ticket operations."""
    def __init__(self, filepath=FILE_NAME):
        self.filepath = filepath
        self.tickets = self.load_tickets()

    def load_tickets(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                raw_data = json.load(f)
                return [Ticket.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, KeyError):
            return []

    def save_tickets(self):
        with open(self.filepath, "w") as f:
            data = [t.to_dict() for t in self.tickets]
            json.dump(data, f, indent=4)

    def get_next_id(self):
        if not self.tickets:
            return 1
        return max(t.id for t in self.tickets) + 1

    def add_ticket(self, issue, priority):
        new_id = self.get_next_id()
        ticket = Ticket(new_id, issue, priority)
        self.tickets.append(ticket)
        self.save_tickets()
        return ticket

    def find_ticket_by_id(self, ticket_id):
        for t in self.tickets:
            if t.id == ticket_id:
                return t
        return None

    def resolve_ticket(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)
        if not ticket:
            return False, f"Error: Ticket #{ticket_id} not found."
        if ticket.status == "Closed":
            return False, f"Ticket #{ticket_id} is already Closed."

        ticket.resolve()
        self.save_tickets()
        return True, f"Success: Ticket #{ticket_id} has been marked as Closed."

    def delete_ticket(self, ticket_id):
        ticket = self.find_ticket_by_id(ticket_id)
        if not ticket:
            return False, f"Error: Ticket #{ticket_id} not found."

        self.tickets.remove(ticket)
        self.save_tickets()
        return True, f"Success: Ticket #{ticket_id} permanently removed."

    def list_tickets(self, status=None, priority=None):
        results = self.tickets
        if status:
            results = [t for t in results if t.status.lower() == status.lower()]
        if priority:
            results = [t for t in results if t.priority.lower() == priority.lower()]
        return results


# ================= CLI PARSER SETUP =================

def main():
    parser = argparse.ArgumentParser(
        description="CLI Support Ticket Tracker — manage tasks and IT bugs directly from your terminal."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available sub-commands")

    # Command: add
    parser_add = subparsers.add_parser("add", help="Create a new ticket")
    parser_add.add_argument("issue", type=str, help="Description of the issue")
    parser_add.add_argument(
        "-p", "--priority",
        choices=["High", "Medium", "Low"],
        default="Medium",
        help="Priority level (default: Medium)"
    )

    # Command: list
    parser_list = subparsers.add_parser("list", help="List tickets")
    parser_list.add_argument("-s", "--status", choices=["Open", "Closed"], help="Filter by status")
    parser_list.add_argument("-p", "--priority", choices=["High", "Medium", "Low"], help="Filter by priority")

    # Command: resolve
    parser_resolve = subparsers.add_parser("resolve", help="Mark a ticket as closed")
    parser_resolve.add_argument("id", type=int, help="Numeric Ticket ID")

    # Command: delete
    parser_delete = subparsers.add_parser("delete", help="Permanently delete a ticket")
    parser_delete.add_argument("id", type=int, help="Numeric Ticket ID")

    args = parser.parse_args()
    manager = TicketManager()

    if args.command == "add":
        ticket = manager.add_ticket(args.issue, args.priority)
        print(f"Created Ticket #{ticket.id} [{ticket.priority}] successfully.")

    elif args.command == "list":
        tickets = manager.list_tickets(status=args.status, priority=args.priority)
        if not tickets:
            print("No matching tickets found.")
        else:
            print(f"\n--- TICKETS ({len(tickets)}) ---")
            for t in tickets:
                t.display()

    elif args.command == "resolve":
        _, message = manager.resolve_ticket(args.id)
        print(message)

    elif args.command == "delete":
        _, message = manager.delete_ticket(args.id)
        print(message)

    else:
        # If user runs 'python day7.py' without arguments, show help
        parser.print_help()


if __name__ == "__main__":
    main()