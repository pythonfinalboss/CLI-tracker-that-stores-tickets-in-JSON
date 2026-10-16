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
        """Marks this ticket as closed."""
        self.status = "Closed"

    def to_dict(self):
        """Converts the Ticket object into a dictionary for JSON saving."""
        return {
            "id": self.id,
            "issue": self.issue,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data):
        """Creates a Ticket object from a dictionary loaded from JSON."""
        return cls(
            ticket_id=data["id"],
            issue=data["issue"],
            priority=data["priority"],
            status=data.get("status", "Open"),
            created_at=data.get("created_at")
        )

    def display(self):
        """Prints the ticket in a clean card layout."""
        print(f"Ticket ID : #{self.id} | Status: {self.status} | Priority: {self.priority}")
        print(f"Created   : {self.created_at}")
        print(f"Issue     : {self.issue}")
        print("-" * 55)


class TicketManager:
    """Manages file storage, ticket collection, and operations."""
    def __init__(self, filepath=FILE_NAME):
        self.filepath = filepath
        self.tickets = self.load_tickets()

    def load_tickets(self):
        """Reads tickets from JSON and converts them into Ticket objects."""
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r") as f:
                raw_data = json.load(f)
                return [Ticket.from_dict(item) for item in raw_data]
        except (json.JSONDecodeError, KeyError):
            return []

    def save_tickets(self):
        """Saves all Ticket objects back into tickets.json."""
        with open(self.filepath, "w") as f:
            data = [t.to_dict() for t in self.tickets]
            json.dump(data, f, indent=4)

    def get_next_id(self):
        """Calculates the next available ID."""
        if not self.tickets:
            return 1
        return max(t.id for t in self.tickets) + 1

    def add_ticket(self, issue, priority):
        """Creates and saves a new ticket."""
        new_id = self.get_next_id()
        ticket = Ticket(new_id, issue, priority)
        self.tickets.append(ticket)
        self.save_tickets()
        return ticket

    def find_ticket_by_id(self, ticket_id):
        """Finds and returns a Ticket object by its ID."""
        for t in self.tickets:
            if t.id == ticket_id:
                return t
        return None

    def resolve_ticket(self, ticket_id):
        """Resolves a ticket if found."""
        ticket = self.find_ticket_by_id(ticket_id)
        if not ticket:
            return False, "Ticket not found."
        if ticket.status == "Closed":
            return False, f"Ticket #{ticket_id} is already closed."

        ticket.resolve()
        self.save_tickets()
        return True, f"Ticket #{ticket_id} marked as Closed!"

    def delete_ticket(self, ticket_id):
        """Removes a ticket permanently."""
        ticket = self.find_ticket_by_id(ticket_id)
        if not ticket:
            return False, "Ticket not found."

        self.tickets.remove(ticket)
        self.save_tickets()
        return True, f"Ticket #{ticket_id} deleted permanently."

    def filter_by_status(self, status):
        return [t for t in self.tickets if t.status.lower() == status.lower()]

    def filter_by_priority(self, priority):
        return [t for t in self.tickets if t.priority.lower() == priority.lower()]

    def search_by_keyword(self, keyword):
        return [t for t in self.tickets if keyword.lower() in t.issue.lower()]


# ================= USER INTERFACE (CLI) =================

def run_app():
    manager = TicketManager()

    while True:
        print("\n=== OOP ISSUE TRACKER (CLI) ===")
        print("1. Create New Ticket")
        print("2. View All Tickets")
        print("3. Filter / Search Tickets")
        print("4. Resolve a Ticket")
        print("5. Delete a Ticket")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            issue = input("Enter issue description: ").strip()
            if not issue:
                print("Issue cannot be empty!")
                continue

            while True:
                priority = input("Enter priority (High/Medium/Low): ").strip().capitalize()
                if priority in ["High", "Medium", "Low"]:
                    break
                print("Invalid priority! Choose High, Medium, or Low.")

            ticket = manager.add_ticket(issue, priority)
            print(f"Ticket #{ticket.id} created successfully!")

        elif choice == "2":
            if not manager.tickets:
                print("\nNo tickets found!")
            else:
                print(f"\n================ ALL TICKETS ({len(manager.tickets)}) ================")
                for t in manager.tickets:
                    t.display()

        elif choice == "3":
            if not manager.tickets:
                print("\nNo tickets to search!")
                continue

            print("\n1. Filter by Status (Open/Closed)")
            print("2. Filter by Priority (High/Medium/Low)")
            print("3. Search by Keyword")
            filter_choice = input("Select option (1-3): ").strip()

            results = []
            if filter_choice == "1":
                status = input("Enter status: ").strip()
                results = manager.filter_by_status(status)
            elif filter_choice == "2":
                priority = input("Enter priority: ").strip()
                results = manager.filter_by_priority(priority)
            elif filter_choice == "3":
                kw = input("Enter keyword: ").strip()
                results = manager.search_by_keyword(kw)
            else:
                print("Invalid choice.")
                continue

            if not results:
                print("\nNo matching tickets found.")
            else:
                print(f"\n--- MATCHING TICKETS ({len(results)}) ---")
                for t in results:
                    t.display()

        elif choice == "4":
            try:
                target_id = int(input("\nEnter Ticket ID to resolve: "))
            except ValueError:
                print("Please enter a valid numeric ID.")
                continue

            success, msg = manager.resolve_ticket(target_id)
            print(msg)

        elif choice == "5":
            try:
                target_id = int(input("\nEnter Ticket ID to delete: "))
            except ValueError:
                print("Please enter a valid numeric ID.")
                continue

            confirm = input(f"Confirm delete Ticket #{target_id}? (yes/no): ").strip().lower()
            if confirm == "yes":
                success, msg = manager.delete_ticket(target_id)
                print(msg)
            else:
                print("Deletion canceled.")

        elif choice == "6":
            print("Application closed. All data safely saved in tickets.json.")
            break
        else:
            print("Invalid selection! Please enter a number from 1 to 6.")


if __name__ == "__main__":
    run_app()