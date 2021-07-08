//Write a menu
//Operation 1 is to check the date
//Operation 2 is to print the ASCII at decesding order
#include <stdio.h>
#include <stdlib.h>

int interface();
int checkDate(int, int, int);
void getDate();
void getASCII();

void clear()
{
    while (getchar()!='\n');
}
//clear buffer
void cls()
{
    system("cls");
}
//clear screen
int main()
{
    int c;
    do
    {
    c = interface();
    switch (c)
    {
        case 1: getDate(); break;
        case 2: getASCII(); break;
        case 3: cls(); break;
        default: printf("Bai bai"); break;
    }
    }
    while (c > 0 && c < 4);
    getchar();
    return 0;
}
//this is a main, using switch case and do while to switch and loop between operation
int checkDate(int dd, int mm, int yyyy)
{
	int maxdd = 31;
	if ((dd<1) || (dd>31) || (mm < 1) || (mm> 12))
	return 0;
	if ((mm==4) || (mm=6) || (mm=9) || (mm=11))
	maxdd=30;
	else if (mm==2)
	{
		if ((yyyy%400==0) || (yyyy%4==0) && (yyyy%100!=0))
		
		maxdd=29;
		
		else maxdd=28;
	}
	return (dd<=maxdd);
}
//check date function
//return 0 if invalid
//return 1 if valid
void getDate()
{
    int dd, mm, yyyy;
    printf("\nEnter day/month/year using dd/mm/yyyy format: ");
    scanf("%d/%d/%d",&dd,&mm,&yyyy);
    if (checkDate(dd, mm, yyyy))
    printf("Valid date");
    else
    printf("Invalid date");
}
//print date function
//calling checkDate function
void getASCII()
{
    char c1, c2, c;
    int d;
    printf("\nEnter character 1: ");
    c1= getchar();
    clear();
    printf("Enter character 2: ");
    c2= getchar();
    clear();
    if (c1 < c2)
    //check if c1 < c2 then swap c1 and c2
    //EX:1 and 5 => swap => 5 and 1
    {
        int t = c1; 
            c1 = c2; 
            c2 = t;
    }
    d = c1 - c2;
    //calculate distance
    printf("The distance between %c and %c: %d\n", c1, c2, d);
    printf("Char   Dec   Oct    Hex\n");
    for (c = c1; c >= c2; c--)
    //take the exemple from above
    // c = 5; c >= 1; c--
    // => c run from 5 to 1 at decesding order
    printf("%3c%6d%6o%6x\n", c, c, c, c);
}
//print ASCII function at decesding order
int interface()
{
    int choice;
    printf("===================  Menu  ===================");
    printf("\n");
    printf("\n1\t-\t\t\t   Check Date");
    printf("\n2\t-   Print ASCII Between two character");
    printf("\n3\t-\t\t\t\tClear");
    printf("\nOther\t-\t\t\t\t Quit");
    printf("\n==============================================");
    printf("\nEnter Your Choice: ");
    scanf("%d", &choice);
    clear();
    return choice;
}
//simple interface