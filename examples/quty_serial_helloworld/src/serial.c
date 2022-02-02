#include <avr/io.h>
#include <avr/interrupt.h>
#include <stdio.h>

//PB2 UART0 TXD
//PB3 UART0 RXD

//Function prototypes
static int uart_putchar(char c, FILE *stream);
static int uart_getchar(FILE *stream);

//Stream for stdio
static FILE uart = FDEV_SETUP_STREAM(uart_putchar, uart_getchar, _FDEV_SETUP_RW);

uint8_t rxbuf[256];             //Rx buffer
volatile uint8_t pWrite = 0;    //Write index into Rx buffer
uint8_t pRead = 0;     //Read index into Rx buffer

void serial_init(void) {
    // Set Tx pin as output
    PORTB.DIRSET = PIN2_bm;

    USART0.BAUD = 4167;  // 9600 baud @ 10 MHz
    USART0.CTRLA = USART_RXCIE_bm;  // Enable recieve interrupt
    USART0.CTRLB = USART_RXEN_bm | USART_TXEN_bm; // Enable Tx/Rx
    
    //Assign stream to stdio
    stdout = &uart;
    stdin = &uart;
}

uint8_t serial_bytesAvaialble(void) {
    //Return number of bytes available in buffer
    return (pWrite-pRead);
}

static int uart_putchar(char c, FILE *stream) {
    //Wait while UART Tx busy
    while (!(USART0.STATUS & USART_DREIF_bm));
    //Write char to Tx buffer
    USART0.TXDATAL = c;
    return c;
}

static int uart_getchar(FILE *stream) {
    //Wait while buffer is empty
    while(!(pWrite-pRead));
    //Return oldest character in buffer
    return rxbuf[pRead++];
}

ISR(USART0_RXC_vect) {
    //Add character to Rx buffer
    rxbuf[pWrite++] = USART0.RXDATAL;
}