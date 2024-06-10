#include "types.h"
#include "stat.h"
#include "user.h"

int
main(int argc, char *argv[])
{
    int writesOutput = writecount();
    printf(1, "%d\n",writesOutput);
    //printint(1, writesOutput, 10, 1);
    exit();
}