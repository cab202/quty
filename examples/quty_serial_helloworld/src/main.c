#include <avr/io.h>
#include <avr/interrupt.h>

#include <stdio.h>

#include "serial.h"

int main(void)
{
    // Initialisation
    cli();                                                   // Disable interrupts
    CCP = CCP_IOREG_gc;                                      // Configuration change enable
    CLKCTRL.MCLKCTRLB = CLKCTRL_PDIV_2X_gc | CLKCTRL_PEN_bm; // Set clock to 10 MHz (x2 prescaler enabled)
    serial_init();                                           // Initialise serial & stdio
    sei();                                                   // Enable interrupts

    // Print on key press
    getchar();
    printf("Hello world!\n");

    while (1)
        ; // Infinite loop
}
