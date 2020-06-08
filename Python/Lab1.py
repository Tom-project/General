Times = ["1", "2", "5", "unlimited"]
Locations = ["door", "kitchen", "table"]
Sizes = ["small", "big", "little", "massive"]
Objects = ["apple", "orange", "bus", "car", "diamond"]
Movements = ["left", "right", "forward", "back", "stop"]
Actions = ["recognise", "eat", "see", "lift", "drop", "fetch"]


def robot():
    prompt = input("Object, Location, or Movement? \n Enter here: ")        
    if prompt in Objects:

        promt2 = input("Action or Size? \n Enter here: ")
        if promt2 == Actions:
            promt3 = int(input("Enter a time: "))
            if promt3 == Times:
                print(promt, promt2, promt3)

            elif promt2 != Times:
                print("you did not choose a time, please try again")
                robot()

        elif promt2 == Sizes:
            promt3 = input("Enter an action: ")
            if promt3 == Actions:
                print(promt, promt2, promt3)

        elif promt2 != Actions or Sizes:
            print("you did not choose a size, please try again")
            robot()

    elif prompt == Locations:
        promt2 = input("Enter an action: ")
        promt3 = input("Enter an Object: ")

    elif prompt == Movements:
        promt2 = input("Enter a time: ")
        promt3 = input("Are you done?: ")
        if promt3 == "yes":
            print("okay")

        elif promt3 == "no":
            promt4 = input("Enter a movment: ")
            promt5 = input("Enter a time: ")

    else:
        print("you did not choose one of the options stated, please try again")
        robot()


robot()
