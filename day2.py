tickets =[]
ticket_counter = 1 
while True:
    print(f"\n--- Creating Ticket #{ticket_counter} ---")
    user = input("Enter your name : ")
    issue = input("Enter your issue : ")
    priority = input("Enter the priority (high, medium, low): ")

    ticket = { 
        "id": ticket_counter, 
        "issue": issue,
        "priority": priority,
        "status": "open" 
    }
    tickets.append(ticket)
    print("ticket created successfully!")
    ticket_counter += 1 

    choice = input("do you want to add another ticket ? (y/n) : ").strip().lower()
    if choice != "y":
        break

print ("\n ============== ALL TICKETS LIST ============ \n")
for t in tickets:
    print(f"TicketID : {t['id']}")
    print(f"Issue    : {t['issue']}")
    print(f"Priority : {t['priority']}")
    print(f"Status   : {t['status']}")
    print("-"*50) 

