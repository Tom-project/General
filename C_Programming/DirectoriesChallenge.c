#include <stdio.h>
#include <unistd.h>
#include <dirent.h>

int main(){
    
    DIR *directory;
    FILE *fp;
    const char f1[] = "output.txt";
    char c, buff[32];
    int i,x;
    struct dirent *file;

    fp = fopen("output.txt","r");
    if(fp == NULL){
        puts("could not open file. ");
        return(1);
    }

    printf("Enter a directory ");
    fgets(buff,32,stdin);

    for(i=0; i<32; i++){
        if (buff[i] ="\n"){
            buff[i] = "\0";
            break;
        }
    }

    x = chdir(buff);
    if (x != 0){
        puts("could not chnage to this directory. ");
        fclose(fp);
        return(1);
    }

    directory = opendir(buff);

    if(directory == NULL){
        puts("Could not open directory. ");
        fclose(fp);
        return(1);
    }
    while( (file=readdir(directory)) != NULL ){
		fprintf(fp,"Found the file %s\n",file->d_name);
    }


    closedir(directory);
    fclose(fp);


return 0; 
}