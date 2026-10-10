tickets = []
ticket_counter = 1

def create_ticket():
    global ticket_counter
    print(f"\n-- Create Ticket #{ticket_counter} --")
    issue = input("Enter your issue : ")
    priority = input("Enter the priority (high, medium, low): ")
    
    ticket = {
        "id": ticket_counter,
        "issue": issue,
        "priority": priority,
        "status": "open" 
    }
    tickets.append(ticket)
    ticket_counter += 1 
    print("Ticket created successfully!")

def view_tickets():
    if not tickets: 
        print("No tickets found!")
        return 
    
    print("\n--- ALL TICKETS ---")
    for t in tickets:
        print(f"ID : {t['id']}")
        print(f"Issue : {t['issue']}")
        print(f"Priority : {t['priority']}")
        print(f"Status : {t['status']}")
        print("-" * 50) 

def main_menu():
    while True:
        print("\n" + "=" * 50)
        print("      TICKET MANAGEMENT SYSTEM       ")
        print("=" * 50)
        print("1. Create Ticket")
        print("2. View Tickets")
        print("3. Exit")
        print("=" * 50)

        choice = input("Enter your choice: ")

        if choice == "1":
            create_ticket()
        elif choice == "2":
            view_tickets()
        elif choice == "3":
            print("Thank you for using the Ticket Management System!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()