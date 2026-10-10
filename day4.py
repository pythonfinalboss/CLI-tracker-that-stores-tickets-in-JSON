import json
import os

FILE_NAME = "tickets.json"

def load_tickets():
    """loads tickets from json file . if file doesn't exist , it return empty list . """
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_tickets(tickets):
    """saves the list of tickets to the json file """
    with open(FILE_NAME, "w") as f:
        json.dump(tickets, f, indent=4)

def get_next_id(tickets):
    """calculates the next id to be used for the ticket"""
    if not tickets:
        return 1
    return max(t['id'] for t in tickets) + 1

def create_ticket():
    tickets = load_tickets()
    ticket_id = get_next_id(tickets)
    
    print(f"\n------ Create Ticket #{ticket_id} ---")
    issue = input("enter the issue : ").strip()
    priority = input("enter the priority (high,medium,low): ").strip().capitalize()

    new_ticket = { 
        "id": ticket_id,
        "issue": issue,
        "priority": priority,
        "status": "open"
    }
    tickets.append(new_ticket)
    save_tickets(tickets)
    print(f"ticket #{ticket_id} created and saved to disk!")

def view_tickets():
    tickets = load_tickets()

    if not tickets:
        print("no tickets found!")
        return 

    print("\n============= ALL TICKETS ==============")
    for t in tickets:
        print(f"Ticket ID : {t['id']}")
        print(f"Issue     : {t['issue']}")
        print(f"Priority  : {t['priority']}")
        print(f"Status    : {t['status']}")
        print("-" * 50)

def resolve_ticket():
    tickets = load_tickets()

    if not tickets: 
        print("\nNo tickets to resolve !")
        return
    try:
        target_id = int(input("\nEnter the Ticket Id to resolve : "))
    except ValueError:
        print("Invalid input. please enter a valid ID number")
        return

    found = False
    for t in tickets:
        if t['id'] == target_id:
            if t['status'] == "resolved":
                print(f"Ticket #{target_id} is already resolved!")
                return
            t['status'] = "resolved"
            found = True
            break
    if found:
        save_tickets(tickets)
        print(f"ticket #{target_id} resolved successfully and closed ")
    else:
        print(f"ticket #{target_id} not found ")

def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("     TICKET MANAGEMENT SYSTEM      ")
        print("=" * 50)
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Resolve Ticket")
        print("4. Exit")
        print("=" * 50)
        
        choice = input("enter your choice 1-4 : ").strip()
        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            resolve_ticket()
        elif choice == "4":
            print("thank you for using the ticket management system")
            break
        else:
            print("invalid choice. please try again")

if __name__ == "__main__":
    main_menu()
