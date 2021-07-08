#include <stdio.h>
#include <iostream>
using namespace std;
// length  = sizeof(arr) / sizeof(int)

// interface 
int inter();

// clear screen (8)
void clrscr();


// initiate array
void setA(int * , int);

// add value (1)
void getAdd(int*,int,int*);
// search	(2)
void searchA(int*,int);
int search(int* , int , int );
// remove first (3)
void getRmF(int*,int,int*);
// remove all (4)
void getRmA(int*, int ,int*);
// display array (5)
void getA(int*, int,int*);
// sort Low --> High  --> ascending (6)
void sortAs(int* , int *);
// sort High --> Low  --> descending (7)
void sortDs(int* , int *);
void printvalue(int*, int*);
// print between min and max
void range(int*, int *);


int main(){
	int a[100];
	int n;
	// INTERFACE 
	int c;
	
	printf("\nInitiate Array(MAX=100)");
	printf("\n-----------------------\n\n");
	printf("Amount of array : ");
	scanf("%d", &n);
	
	
	setA(a,n);
	
	system("color 2");
	printf("\n");
	printf("\n     =====================");
	printf("\n     |PROGRAM START !!!!!|");
	printf("\n     =====================");
	
	do{
		c = inter();
		switch(c){
			case 1 : getAdd(a,n,&n);	break;
			case 2 : searchA(a,n);		break;
			case 3 : getRmF(a,n,&n);	break;
			case 4 : getRmA(a,n,&n);	break;
			case 5 : getA(a,n,&n);		break;
			case 6 : sortAs(a,&n);		break;
			case 7 : sortDs(a,&n);		break;
            case 8 : range(a, &n);		break;
			case 9 : clrscr();	break;
		}
	}while(c>0 && c <10);
	printf("Thanks !!!");
	
	
	

	fflush(stdin);
	getchar();
	getchar();
	return 0;
}

// scanf Array
void setA(int *a , int n ){

	printf("---->Enter the array : ");
	int i=0;
	
	// for
	for(int i = 0 ; i < n ; i++){
		scanf("%d", &a[i]);
	}
		fflush(stdin);
	
	// first look : 
	printf("All the number after a[%d]= %d will be clear !!!",n,a[n-1]);
}

// print Array 
void getA(int *a , int n , int *pn ){
	printf("The array  a[] =  "); 
	for(int i = 0 ; i < n ; i++){	// fix
		printf("%5d",(a[i]));	
	}
	printf("\n");
}


//inter face  : menu
int inter(){
//	printf("%15s" , "Menu");
	printf("\n\n");
	printf("   ==========================\n");
	printf("   |          MENU          |\n");
	printf("   ==========================\n");
	
	
	
	printf("\n%-20s%10s"," Option" , "Name");
	printf("\n%-20s%10s","---------" , "----------------------");
	
	printf("\n %-20s%10s","   1   " , "Add an element");
	printf("\n %-20s%10s","   2   " , "Search value");
	printf("\n %-20s%10s","   3   " , "Remove FIRST value");
	printf("\n %-20s%10s","   4   " , "Remove ALL value");
	printf("\n %-20s%10s","   5   " , "Display an array");
	printf("\n %-20s%10s","   6   " , "Sort array ASCENDING");
	printf("\n %-20s%10s","   7   " , "Sort array DESCENDING");
    printf("\n %-20s%10s","   8   " , "Range between min and max");
	printf("\n %-20s%10s","   9   " , "CLEAR screen");
	printf("\n %-20s%10s","Other " , "Quit");
	
	
	int choice ;
	printf("\n\n-----> Choice : ");
	scanf("%d", &choice);
	
	return choice;
}

//clear screen
void clrscr(){
	system("cls");
}

// Get search (main option 2)
void searchA(int* a, int n){
	int x;
	printf("----->Enter the search Value  : ");
	scanf("%d",&x);
	int s;
	s = search(a,n,x);
	
	if(s != 0)	printf(".....Founded : %d",s );
	else 		printf(".....NOT inside the Array !!");
}

// func search element
int search(int* a, int n , int x){
	int res = 0;
	for(int i=0 ; i < n ; i++){
		if(a[i] == x) res ++;
	}	
	return res;
}

// remove all element of input (main option 4)
void getRmA(int * a , int n, int *pn){
	int x;
	printf("----->Select : ");
	scanf("%d",&x);
	
	
	int flag=0;
	int i=0,j = 0;
	int checkI=0;
	// OP so fk OP :)))))))))))))))))))))))
	for(i=*pn - 1;i >= 0 ; i--){
		if(a[i] == x){
		checkI = i;
		flag ++;
			
		
			for(j = checkI; j < *pn  ; j++){
			a[j] = a[j+1];
			
			}
			
			
		}*pn  = n-flag ;
	}
	
	if(flag != 0)	printf(".....Removed !!");
	else printf(".....Not found !!");
}

//  Add 1 element to the last array  (main option 1)
void getAdd(int *a  , int n, int *pn){

   int x;
	printf("----->Enter value to add : ");
	scanf("%d",&x);

	a[*pn] = x;
	*pn = n+1;
	
	printf(".....Add Successfull !");
}


// Rm the first element 
void getRmF(int* a, int n, int *pn){
	int i=0;
	for(i ;i <n-1 ; i++){
		a[i] = a[i+1];
	}
	*pn = n-1; 
	
	printf("Remove successfull !!");
}


// sort ascending
void sortAs(int *a , int *pn){
	printf("Sort successfull !!");
	int i=0,j=0;
	for(i; i < *pn-1 ; i ++){
		for(j=i+1; j < *pn ; j++){
			if(a[i] > a[j]){
				//swap
				int t=0;
				t= a[i];
				a[i] = a[j];
				a[j] =t;
			}
		}
	}
}


// sort descending
void sortDs(int *a , int *pn){
	printf("Sort successfull !!");
	int i=0,j=0;
	for(i; i < *pn-1 ; i ++){
		for(j=i+1; j < *pn ; j++){
			if(a[i] < a[j]){
				//swap
				int t=0;
				t= a[i];
				a[i] = a[j];
				a[j] =t;
			}
		}
	}
}

void range(int*a, int *pn)
{
    int min, max;

    printf("Enter min: ");
    scanf("%d", &min);
    printf("Enter max: ");
    scanf("%d", &max);
    printf("The Elements between min and max are: ");
    for (int i = 0; i < *pn; i++)
    {
        if (a[i] >= min && a[i] <= max)
            printf("%5d ", a[i]);
    }
}