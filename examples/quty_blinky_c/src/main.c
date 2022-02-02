#include <avr/io.h>
#include <util/delay.h>

int main(void) {
    
    // Display on
    PORTB.OUTSET = PIN1_bm;
    // DISP_EN, DISP_DP as outputs
    PORTB.DIRSET = (PIN5_bm | PIN1_bm);
    
    for (;;) {
        // 500ms delay (1 Hz flash)
        _delay_us(500000);
        // Toggle DP
        PORTB.OUTTGL = PIN5_bm;
    }
    
}