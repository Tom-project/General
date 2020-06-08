//This C++ code is used to take an input string and
 // put the instructions in an array
 #include <iostream>
 #include <string>
 #include <sstream>
 using namespace std;


 int main() {
   string user_input1 = "";
   string user_input2 = "";
   string user_input3 = "";
   string object1 = "";
   string action;
   string Location;
   int size;
   int movement1;
   int time;

  cout << "Do you want to enter an Object, Location or Movement:\n>";
    cin >> user_input1;
      if (user_input1 == "Object") {
        std::cout << "Action or Size" << '\n';
        std::cin >> user_input2;

          if (user_input2 == "Action") {
            std::cout << "Enter a time" << '\n';
            std::cin >> time;

            std::cout << "You entered: " << user_input1 << user_input2 <<  time  << '\n';
          }

          else {
            std::cout << "Enter an Action" << '\n';
            std::cin >> action;

            std::cout << "You entered: " << user_input1 << user_input2 <<  action  << '\n';
          }

          }

          if (user_input1 == "Location") {
            std::cout << "Enter an Action" << '\n';
            std::cin >> action;
            std::cout << "Enter an Object" << '\n';
            std::cin >> object1;

            std::cout << "You entered: " << user_input1 << action <<  object1  << '\n';
          }

            if (user_input1 == "Movement") {
              std::cout << "Time1 or Time2" << '\n';
              std::cin >> user_input3;

                  if (user_input3=="Time1") {
                    std::cout << "Enter a movement" << '\n';
                    std::cin >> movement1;

                    cout << "You entered: " << user_input1 << user_input3 << movement1;
                  }
                else(user_input3=="Time2") {
                  std::cout << "Nothing" << '\n';
                }
          }

    cout << "You entered: " << user_input1 << user_input3 << endl; //set up input string




    string input="left 2seconds";
    //initalise input stream
    stringstream currentstring(input);
    int count=-1;
    string instruction[10];
    //Repeatedly put instruction in string array
    while (currentstring.good())
        {
          count=count+1;
         currentstring >> instruction[count];
        }
return 0; }
