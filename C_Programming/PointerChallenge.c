#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main()
{
	char *pbuffer[10], buff[32];
    int i;


for(i=0;i<10;i++){
	
    pbuffer[i] = (char *)malloc( strlen(buff) + 1 );
	if( pbuffer[i] == NULL )
	{
		puts("Unable to allocate memory");
		exit(1);
	}
    
    printf("Enter 10 fruits #%d ",i+1);
    fgets(*(pbuffer+i),32,stdin);

}

    for(i=0;i<32;i++){
        printf("%s",*(pbuffer+i));
    }

    return(0);
}