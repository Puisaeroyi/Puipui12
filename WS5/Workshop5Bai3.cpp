//
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void getEquation();
int deposit(int, int, int);
void getDeposit();

int interface();
void clear();
void cls();

int main()
{
    int c;
    do
    {
        c = interface();
        switch (c)
        {
            case 1: getEquation(); break;
            case 2: getDeposit(); break;
            case 3: cls(); break;
        }
    }
    while (c > 0 && c < 4);

    getchar();
    return 0;
}
//this is a main, using switch case and do while to switch and loop between operation
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
void getEquation()
{
    double a, b, c, d, root1, root2;
    printf("\nEnter the ax^2 + bx + c: ");
    scanf("%lf %lf %lf", &a, &b, &c);
    clear();
    d = (b*b) - (4*a*c);
    //discriminant of equation
    if (d < 0)
    {
        printf("No Solution!");
    }
    //it has solution but it not real
    else if (d == 0)
    {
        printf("Root1 = root2 = %.2lf", -b/(2*a));
    }
    else
    {
        root1 = (-b + sqrt(d))/(2*a);
        root2 = (-b - sqrt(d))/(2*a);
        printf("Root1 = %.2lf", root1);
        printf("\nRoot2 = %.2lf", root2);
    }
}
//print root 1 and 2 of quaratic equation
double deposit(int d, double r, int n)
{
    return d*pow(1+r, n);
}
//formula deposit
void getDeposit()
{
    int d, n;
    double r, P;
    printf("\nPLease enter your deposit: ");
    scanf("%d", &d);
    clear();
    printf("Please enter yearly rate: ");
    scanf("%lf", &r);
    clear();
    printf("Please enter number of years: ");
    scanf("%d", &n);
    clear();
    P = deposit(d, r, n);
    printf("Your deposit is: %.2lf", P);
}
//nothing to say here
int interface()
{
    int choice;
    printf("\n===================  Menu  ===================");
    printf("\n1\t-\t Quadratic Equation calculator");
    printf("\n2\t-\t\t  Check yearly deposit");
    printf("\n3\t-\t\t\t\t Clear");
    printf("\nOther\t-\t\t\t\t  Quit");
    printf("\n==============================================");
    printf("\nEnter Your Choice: ");
    scanf("%d", &choice);
    clear();

    return choice;
}
//simple interface