//Write a program that roll two dice
//the number depending on user chosen
//Calculate sum between two dice

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

int intRandom(int min, int max)
{
    return rand() % max + min;
    //roll random from [min, max]
}
int main()
{
    int min = 1, max;
    int sum, x, y;
    int count = 0;

    printf("Enter a dice of your choice: ");
    scanf("%d", &max);
    printf("Enter the sum of your two dice: ");
    scanf("%d", &sum);
    srand(time(NULL));
    //srand function guarantee random everytime program runs
    do
    {
        x = intRandom(min, max);
        y = intRandom(min, max);
        sum == x + y;
        count++;
        printf("\n%d-th roll: %d and %d!",count, x, y);
    } 
    while (sum != x + y);
    printf("\nAt the %d-th, the dice roll is %d and %d!",count, x, y);
    getchar();
    return 0;
}