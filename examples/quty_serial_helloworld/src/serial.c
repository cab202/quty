#include "serial.h"

#include <avr/io.h>
#include <avr/interrupt.h>

#include <stdint.h>
#include <stdio.h>

// Setup stdio stream
static int uart_putchar(char c, FILE *stream);
static int uart_getchar(FILE *stream);
static FILE uart = FDEV_SETUP_STREAM(uart_putchar, uart_getchar, _FDEV_SETUP_RW);

// Rx buffer
#define BUFFER_SIZE 256
volatile char rx_buf[BUFFER_SIZE] = {0};
volatile uint8_t rx_write = 0;
uint8_t rx_read = 0;

void serial_init(void)
{
    // Output enable UART_TX
    PORTB.DIRSET = PIN2_bm;

    USART0.BAUD = 4167;                           // 9600 baud @ 10 MHz
    USART0.CTRLA = USART_RXCIE_bm;                // Enable recieve interrupt
    USART0.CTRLB = USART_RXEN_bm | USART_TXEN_bm; // Enable Tx/Rx

    // Assign stream to stdio
    stdout = &uart;
    stdin = &uart;
}

uint8_t serial_bytes_available(void)
{
    // Return number of bytes available in buffer
    return (rx_write - rx_read);
}

static int uart_putchar(char c, FILE *stream)
{
    while (!(USART0.STATUS & USART_DREIF_bm))
        ; // Wait if UART Tx busy

    // Write char to Tx buffer
    USART0.TXDATAL = c;
    return c;
}

static int uart_getchar(FILE *stream)
{
    while (!(rx_write - rx_read))
        ; // Wait if buffer is empty

    // Return oldest character in buffer
    return rx_buf[rx_read++];
}

ISR(USART0_RXC_vect)
{
    rx_buf[rx_write++] = USART0.RXDATAL;
}
