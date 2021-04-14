
#include <stdio.h>

int main(int argc, char const *argv[]) {
    printf("STARTING instrumentation here\n");

    volatile unsigned long long returned_value = 0;
    __asm__ volatile ("csrrw    %0, 0x803, %1"  /* read and write atomically */
                    : "=r" (returned_value) /* output: register %0 */
                    : "r" ( 0x01 )  /* input: register %1 */
                    : /* clobbers: none */);
    printf("Returned value 0x%08lX\n", returned_value);

    printf("I'm inside the app\n");

    __asm__ volatile ("csrrw    %0, 0x803, %1"  /* read and write atomically */
                    : "=r" (returned_value) /* output: register %0 */
                    : "r" ( 0x00 )  /* input: register %1 */
                    : /* clobbers: none */);

    printf("Returned value 0x%08lX\n", returned_value);
    printf("STOPPED instrumentation here\n");

    return 0;
}
