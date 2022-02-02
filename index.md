## QUTy Development Board

QUTy is a development board based on the Microchip ATtiny1626 AVR microcontroller. It is designed specifically to teach microcontroller programming in the course _CAB202 Microprocessors and Digital Systems_.

### Features

- Microchip ATtiny1626 microcontroller (16 KB flash, 2 KB SRAM)
- USB-C interface for power, programming (UPDI) and serial communications (UART)
- 4x pushbuttons
- Piezo buzzer
- Potentiometer
- 2-digit, 7-segment LED display
- Expansion header for socketting into breadboard

### Development environment

Development for the QUTy is supported via [PlatformIO](https://platformio.org/). We recommend using the [PlatformIO IDE for VSCode](https://platformio.org/install/ide?install=vscode) which is avilable for Windows, MacOS, and Linux.

#### Usage

1. Install [PlatformIO](https://docs.platformio.org/en/latest/integration/ide/vscode.html#ide-vscode)
2. Create a PlatformIO project and configure the QUTy platform in the platformio.ini file:

```
[env:QUTy]
platform = quty
board = QUTy
```

#### Examples

A number of example projects are available as part of the platform. These can be accessed via: 
```
PlatformIO Home > Platforms > QUTy > Examples
```
- quty_blinky_c 
  - 1 Hz LED flash, in C.
- quty_blinky_asm
  - 1 Hz LED flash, in Assembly.
- quty_blinky_asm_bare
  - 1 Hz LED flash, in Assembly (without startup code).
- quty_serial_helloworld
  - Serial monitor/stdio example (prints "Hello world!" on key press).

### Contact

QUTy designed and maintained by the Queenland University of Technology (QUT), based in Brisbane Austrialia. Please direct enquiries to mark.broadmeadow@qut.edu.au.
