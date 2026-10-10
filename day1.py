name = input("enter your name : ")
print("welcome to python", name)
ticket_id = int(input("enter your ticket id : "))
print("your ticket ID is : ", ticket_id)
title = input("enter your title : ")
print("your issue title is :", title)
status = "open"
print("current status:", status)
action = input(" type resolved if your problem resolved : ")
if action.strip().lower() == "resolved":
    status = "ticket closed"
print("updated status", status)

priority = input("Enter your priority(high,medium,low ): ").strip().lower()

if priority == "high":
    print("your priority is high , we will look into it ASAP")
elif priority == "medium":
    print("your priority is medium , we will look into it")
elif priority == "low":
    print("your priority is low , we will look into it whenever possible")
else:
    print("invalid priority")