#include <avr/io.h>

// Place in init section 
.section .init0

entry:
    // Change to 32k clock
    ldi r16, 0xD8   // IOREG change enable
    ldi r17, 0x01   // 32kHz clock select
    ldi r18, 0x07   // 16x prescaler
    out CPU_CCP, r16
    sts CLKCTRL_MCLKCTRLA, r17
    out CPU_CCP, r16
    sts CLKCTRL_MCLKCTRLB, r18
    // DISP_EN and DISP_DP as outputs
    ldi r16, 0x22
    sts PORTB_OUT, r16
    sts PORTB_DIR, r16
    // LED is on B5
    ldi r16, 0x20
loop:
    // ~4 cycles per loop
    // ~2 Hz at clk = 2048 Hz
    nop
    inc r17
    brne loop
    // Toggle LED
    sts PORTB_OUTTGL, r16
    rjmp loop