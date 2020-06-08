Times = ["1", "2", "5", "unlimited"]
Locations = ["door", "kitchen", "table"]
Sizes = ["small", "big", "little", "massive"]
Objects = ["apple", "orange", "bus", "car", "diamond"]
Movements = ["left", "right", "forward", "back", "stop"]
Actions = ["recognise", "eat", "see", "lift", "drop", "fetch"]


user_input = input("Enter instructions: ")

x = user_input.split()

for x in user_input:
    if word in Objects:
        order = order + 'o'
    if word not in Objects:
        print("enter a correct Object")
    if word in Actions:
        order = order + 'a'
    if word not in Actions:
        print("enter a correct Action")
