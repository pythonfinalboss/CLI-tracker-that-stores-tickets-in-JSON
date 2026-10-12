import json 
import os
from datetime import datetime

FILE_NAME = "tickets.json"


def load_tickets():
    """Loads tickets from the json file. Returns an empty list if file doesn't exist."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tickets(tickets):
    """Saves tickets to the json file."""
    with open(FILE_NAME, "w") as f:
        json.dump(tickets, f, indent=4)


def get_next_id(tickets):
    """Calculates the next available ticket ID."""
    if not tickets:
        return 1
    return max(t['id'] for t in tickets) + 1


def display_ticket_card(t):
    """Displays a single ticket formatted as a card."""
    print(f"Ticket ID   : {t.get('id')}")
    print(f"Issue       : {t.get('issue')}")
    print(f"Priority    : {t.get('priority')}")
    print(f"Status      : {t.get('status')}")
    print(f"Created At  : {t.get('created_at', 'N/A')}")
    print("=" * 60)


displat_ticket_card = display_ticket_card  # alias for backwards compatibility


def create_ticket():
    """Prompts the user to create a new ticket."""
    tickets = load_tickets()
    ticket_id = get_next_id(tickets)

    print(f"\n--- Create Ticket #{ticket_id} ---")
    issue = input("Enter the issue: ").strip()
    if not issue:
        print("Issue description cannot be empty!")
        return

    while True:
        priority = input("Enter priority (low, medium, high): ").strip().lower()
        if priority in ["low", "medium", "high"]:
            break
        print("Invalid priority! Please choose low, medium, or high.")

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_ticket = {
        "id": ticket_id,
        "issue": issue,
        "priority": priority,
        "status": "open",
        "created_at": created_at
    }

    tickets.append(new_ticket)
    save_tickets(tickets)
    print(f"Ticket #{ticket_id} created successfully!")


def view_tickets(tickets_to_show=None):
    """Views all tickets or a filtered list of tickets."""
    if tickets_to_show is None:
        tickets_to_show = load_tickets()

    if not tickets_to_show:
        print("No tickets to show.\n")
        return

    print(f"\n=================== TICKETS ({len(tickets_to_show)}) ==========================")
    for t in tickets_to_show:
        display_ticket_card(t)


def filter_ticket():
    """Filters or searches tickets by status, priority, or keyword."""
    tickets = load_tickets()
    if not tickets:
        print("No tickets found to filter or search.\n")
        return

    print("\nFilter / Search Options:")
    print("1. Filter by Status (open/closed)")
    print("2. Filter by Priority (low/medium/high)")
    print("3. Search by Keyword in Issue")
    sub_choice = input("Enter choice (1-3): ").strip()

    if sub_choice == "1":
        status_input = input("Enter status (open/closed): ").strip().lower()
        filtered = [t for t in tickets if str(t.get('status', '')).lower() == status_input]
        view_tickets(filtered)
    elif sub_choice == "2":
        priority_input = input("Enter priority (low/medium/high): ").strip().lower()
        filtered = [t for t in tickets if str(t.get('priority', '')).lower() == priority_input]
        view_tickets(filtered)
    elif sub_choice == "3":
        keyword = input("Enter keyword to search: ").strip().lower()
        filtered = [t for t in tickets if keyword in str(t.get('issue', '')).lower()]
        view_tickets(filtered)
    else:
        print("Invalid filter option.")


def resolve_ticket():
    """Marks a ticket as closed / resolved."""
    tickets = load_tickets()
    if not tickets:
        print("No tickets to resolve.")
        return

    try:
        ticket_id = int(input("Enter the ticket ID to resolve: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    for t in tickets:
        if t.get('id') == ticket_id:
            if t.get('status') == 'closed':
                print(f"Ticket #{ticket_id} is already closed.")
                return
            t["status"] = "closed"
            save_tickets(tickets)
            print(f"Ticket #{ticket_id} marked as closed!")
            return

    print(f"Ticket #{ticket_id} not found.")


def delete_ticket():
    """Deletes a specific ticket by ID or deletes all tickets with confirmation."""
    tickets = load_tickets()
    if not tickets:
        print("No tickets to delete.")
        return

    print("\nDelete Options:")
    print("1. Delete a specific ticket by ID")
    print("2. Delete ALL tickets")
    del_choice = input("Enter choice (1-2): ").strip()

    if del_choice == "1":
        try:
            ticket_id = int(input("Enter ticket ID to delete: ").strip())
        except ValueError:
            print("Invalid ID.")
            return

        ticket_to_remove = next((t for t in tickets if t.get('id') == ticket_id), None)
        if ticket_to_remove:
            tickets.remove(ticket_to_remove)
            save_tickets(tickets)
            print(f"Ticket #{ticket_id} deleted successfully.")
        else:
            print(f"Ticket #{ticket_id} not found.")

    elif del_choice == "2":
        confirm = input("Are you sure you want to delete all tickets? (y/n): ").strip().lower()
        if confirm == "y":
            save_tickets([])
            print("All tickets deleted.")
        else:
            print("Deletion cancelled!")
    else:
        print("Invalid choice.")


def main_menu():
    """Main CLI navigation loop."""
    while True:
        print("\n" + "=" * 50)
        print("       CLI TICKET MANAGEMENT SYSTEM - DAY 5")
        print("=" * 50)
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Filter / Search Tickets")
        print("4. Resolve Ticket")
        print("5. Delete Ticket")
        print("6. Exit")
        print("=" * 50)

        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            filter_ticket()
        elif choice == "4":
            resolve_ticket()
        elif choice == "5":
            delete_ticket()
        elif choice == "6":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main_menu()