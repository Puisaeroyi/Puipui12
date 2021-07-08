//Write a program that will accept a number >=1 000 000 000.
//Check if the number is an ISBN (International Standard Book Number).

#include <stdio.h>
#include <stdlib.h>

int checkISBN(long long int);
void clear();

int main()
{
    long long int n;
    int count = 0;
    //ISBN too big.
    do
    {
    printf("\nEnter your ISBN (Enter 0 to quit): ");
    scanf("%lld", &n);
    clear();
    if (n > 0)
    {
    if (checkISBN(n) == 1) printf("Your ISBN is valid!");
    else printf("Your ISBN is not valid!");
    }
    //check if ISBN is valid or not.
    }
    while (n != 0);
    //Out loop if 0 is input
    printf("\nGood Bye!");
    getchar();
    return 0;
}
int checkISBN(long long int n)
{
    int i, j, N[10];
    int count = 10;
    int sum = 0;

    for (i = 9; i >= 0; i--)
	{
		N[i] = n % 10;
		n = n / 10;
	}
    //Extract digits from ISBN and then sign them to array
    for (j = 0; j < 9; j++)
    {
        sum += N[j]*count;
        count --;
    }
    //Algorithm to check ISBN
    sum += N[9];
    //The last digit of ISBN is to check so plus only
    if (sum % 11 == 0)
        return 1;
    else
        return 0;
}

void clear()
{
    while(getchar()!='\n');
}