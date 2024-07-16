#include <avr/io.h>
#include <util/delay.h>

int main(void)
{
    // Set DISP_EN HIGH
    PORTB.OUTSET = PIN1_bm;
    // Output enable DISP_EN and DISP_DP
    PORTB.DIRSET = PIN1_bm | PIN5_bm;

    while (1)
    {
        // 500 ms delay (1 Hz)
        _delay_ms(500);
        // Toggle DISP_DP
        PORTB.OUTTGL = PIN5_bm;
    }
}
