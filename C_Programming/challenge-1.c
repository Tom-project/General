#include <stdio.h>
struct date {
        int day;
        int month;
        int year;
	};
	struct person {
        char name[32];
        struct date tookoffice;
	};

void show(struct person president[]){
int x;

	for(x=0;x<4;x++)
	{
        
		printf("Presidents %s came into office on %d/%d/%d\n",
                president[x].name,
				president[x].tookoffice.day,
				president[x].tookoffice.month,
				president[x].tookoffice.year
			  );
	}
}


int main()
{
    struct person president[4] = {
        {"George Washington", { 30, 4, 1789, } },
        {"Thomas Jefferson", { 4,  3, 1801 } },
        {"Abraham Lincoln", { 4,  3, 1861 } },
        {"Theodore Roosevelt", { 14, 9, 1901 } }
    };
    
    struct person temp;
    show(president);
    /* Swap names about */
    puts("Swapping...");
    temp = president[1];
    president[1] = president[3];
    president[3] = temp;

    show(president);

	return(0);
}