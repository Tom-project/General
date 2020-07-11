#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define SIZE 51

int compare(const void *a, const void *b)
{
	return( *(int *)a - *(int *)b);
}

int main(){
    int x,r;
    int list[SIZE];
    int winnings[6];

    //initialise random number generator
    srand((unsigned) time(NULL));

    //print out random numbers
    for(x=0; x<SIZE; x++){
        list[x] = rand() % SIZE + 1;
        //printf("%4d ",list[x]);
    }
    putchar('\n');

    //pick winning lottery numbers
    for(x=0;x<6;x++){
        r = rand() % SIZE + 1;
        winnings[x] = list[r];
        //printf("%4d",winnings[x]);
    }
    putchar('\n');
    

    /* perform the quick sort */
	qsort(winnings, 6, sizeof(int), compare);

    for(x=0;x<6;x++){
		printf("%4d",winnings[x]);
    }
	putchar('\n');

    return 0;
}