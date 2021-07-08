//Write a program that check Canadian SIN or not.

#include <stdio.h>
#include <stdlib.h>

int checkCanadianSIN (int n)
{
    int N[10];
    //Array that contains digits of n.
    int C[12];
    //Array for checking.
    int T1, T2, T3, totals;
    //Temporary values.
    int i, result = 0;
    //Loop variable and result of the function.
    if (n > 0)
    {
        for (i = 9; i > 0; i--)
        {
            N[i] = n%10;
            n = n/10;
        }
        //Compute N[i].
        C[1]=C[5]=N[2]; C[2]=C[6]=N[4]; C[3]=C[7]=N[6]; C[4]=C[8]=N[8];
        C[9]=2*C[1]; C[10]=2*C[2]; C[11]=2*C[3]; C[12]=2*C[4];
        //Compute C[i].
        T1=C[9]/10 + C[9]%10 + C[10]/10 + C[10]%10 + C[11]/10 + C[11]%10 + C[12]/10 + C[12]%10;
        T2=N[1] + N[3] + N[5] + N[7];
        totals = T1 + T2;
        T3 = (totals/10 + 1)*10;
        //Compute temporary values
        if (T3 - totals == N[9])
        //conclusion;
        result = 1;
    }
    return result;
}
//Check Canadian SIN function
int main()
{
    int n = 193456787;
    if (checkCanadianSIN(n)==1)
    printf("Valid");
    else printf("Invalid");
    getchar();
    return 0;
}
//simple main that calling function