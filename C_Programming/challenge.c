#include <stdio.h>
#include <string.h>

int main(){
    char name[32];
    char new[64];
    char last[]="You passed the challenge! ";
    int x,ch;

    /* For loop to take user input and store it character by character in the array */
    printf("please enter your name: ");

    x=0;

    while( (ch=getchar()) != '\n'){
        name[x] = ch;
        x++;
        if (x == 31){
            break;
        }

    }
    name[x] = '\0';

    /* Copy strings to new buffer */
    strcpy(new,name);
    strcat(new," ");
    strcat(new,last);

    /* For loop to putchar the final string to screen */
    for(x=0;x<sizeof(new);x++){
        putchar(new[x]);
    }

    /* 
    
    OR you could have used a while loop to say while x is not the end of the line put the character to the screen and increment to the next one
    
    x = 0;
	while( putchar(buffer[x++]) )
		;
    
    */

    return 0;

}