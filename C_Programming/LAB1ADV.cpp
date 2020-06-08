#include <iostream>
using namespace std;

int lengthOfName; //defining variables
lengthOfName = name.length();
int value;
value=0;
int counter = 0;

int main() {
    string name;
    cout << "Please enter your first name: ";
    getline(cin, name); // take user input through cin doesnt like spaces so we wouldnt be abke to replace them with colons later on

    string ID;
    cout << "Please enter your full student ID: ";
    getline(cin, ID);
}



int check() {
for (int i=0; i<ID.length(); i++ ){ //Iterates over 
    char emptyArray[i];
    emptyArray[0]=ID[i];
    int emptyList = atoi(emptyArray)

    if (emptyList[i] >2; and emptyList[i] < 7) { //checks to see if value is between 2 and 7
        value = emptylist[i]; //aassigns the inetger to our variable
        break;
    }
if (value == 0){ // if there is no integer in student ID with this condition it assumes it is 4
    value = 4;
}
}

for (int  i=0; i<lengthOfName; i++){
    if (name[i]==" "){ //if a character in the name is a space then
        name[i]=';'; //repalce it with a colon
    }
    else{
        if (name[i].isupper()){ // checks to see if the character is uppercase
            name[i]=name[i].lower(); // if it is then make it lower case
            cout << name[i]; << endl; // output
        }

        else{
            name[i]=name[i].upper();//if its not upper then it must be lowercase
            cout << name[i] << endl; // so make it upper case and output
        }
    }
}
}

if (count == value){
    cout << endl;
    count=0;//reset counter
}
if (count < value){ //if counter is less than value then padd it with "="
    int n = value - (count % value);
    for (int i=0; i<n; i++){
        cout << '=';
    }
    cout << endl;
}

count = 0; // reset counter
