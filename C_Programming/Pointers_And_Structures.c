#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{

struct human{
    char *name;
    int age;
}*person;

char buffer[20];

//Assign memeory to the person pointer member to the same size of the structure
person = ( struct human *)  malloc( sizeof(struct human) * 1);
if (person== NULL){
    printf("Could not assign memeory");
    exit(1);
}

//Take user input and store in buffer
printf("What is your name? ");
fgets(buffer,20,stdin);

//Assign memory to the name pointer to the same size of the buffer - ready for contents to be copied across
person->name = (char *)malloc( sizeof(buffer) ) ;
//check if memory was assigned correctly
if (person->name == NULL){
    printf("Could not assign memeory");
    exit(1);
}
//copy input from buffer to necessary places using the pointer notation
strcpy(person->name,buffer);

printf("What is your age? ");
scanf("%d",&person->age); //Need to use "&" here to get the address of the age pointer. This means we can store the user input at this address

/* Print statements */
printf("Your name is %s\n",person->name);
printf("Your age is %d", person->age);


}