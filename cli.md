## CLI Usage

### Installation

If you do not wish to install PIO globally, please see [Advanced Installation](#advanced-installation)

1. Install PlatformIO.

    ```bash
    # pip (Python users)
    pip install -U platformio

    # apt (Linux users)
    sudo apt install platformio

    # brew (macOS users)
    brew install platformio
    ```

2. Add the QUTy platform by following the steps in [QUTy Platform Installation](#quty-platform-installation).

### Advanced Installation

1. Download the `get-platformio.py` script from the PlatformIO (PIO) repository.

    ```bash
    # curl
    curl -fsSL https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py -o get-platformio.py

    # wget
    wget https://raw.githubusercontent.com/platformio/platformio-core-installer/master/get-platformio.py -O get-platformio.py
    ```

2. Install PIO using Python.

    ```bash
    python get-platformio.py
    ```

    Once PIO is installed to your home directory, fetch the executable location via:

    ```bash
    python get-platformio.py check core
    # (Linux) home/username/.platformio/penv/bin/platformio
    # (Windows) C:\Users\username\.platformio\penv\Scripts\platformio.exe
    ```

    You may wish to add this directory to the system PATH variable or create an alias to this executable.

3. Add the QUTy platform by following the steps in [QUTy Platform Installation](#quty-platform-installation).

### QUTy Platform Installation

Run the following command to register the QUTy platform within PlatformIO.

```bash
pio pkg install --platform https://github.com/cab202/quty --global
```

To confirm that the installation was successful, use

```bash
pio pkg list --global
```

### Getting Started

1. Create the following configuration file (`platformio.ini`) in the root directory of your project.

    ```ini
    # platformio.ini
    [env:QUTy]
    platform = quty
    board = QUTy
    ```

2. Follow the given directory structure as per PlatformIO specifications.

    ```bash
    root
    ├───.pio
    │   └───build
    │       └───QUTy
    ├───include
    │   └───<header files>
    ├───lib
    │   └───<pre-compiled programs>
    └───src
        └───<source files>
    ```

    Here the `.pio` directory is automatically created by PIO when the user tries to build or upload the program.

    Note that if you wish to use the `lib` directory, the following compiler flags need to be added inside `platformio.ini`.

    ```ini
    # platformio.ini
    # ... platform configuration
    build_flags =
        # Add directory
        -L lib
        # Add linker option
        -Wl,lib/<file name>
    ```

3. Build your program with the `run` command.

    ```bash
    pio run
    ```

4. Build and upload your program to the QUTy microcontroller with the `-t` flag.

    ```bash
    pio run -t upload
    ```

    If PIO cannot determine the port automatically determined, use the `--upload-port` option to specify the port. The port can be found using the following command:

    ```bash
    pio device list
    ```

    If no devices are listed, you may be missing some drivers. See [Installation](index.md#installation) for more information.
