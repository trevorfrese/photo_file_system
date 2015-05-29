#include <stdio.h>
#include <stdlib.h>


int main(int argc, char**argv){
  FILE * fp;
  fp = fopen(argv[1], "w");

  int i = 0;


  for (i = 0; i < atoi(argv[2]); i++) {
  	fprintf(fp, "a");
  }

  fclose(fp);
  return 0;
}