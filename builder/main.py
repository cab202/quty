# Copyright 2019-present PlatformIO <contact@platformio.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Modifications Copyright (C) 2022 Queensland University of Technology (QUT)
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
from os.path import join

from SCons.Script import (ARGUMENTS, COMMAND_LINE_TARGETS, AlwaysBuild,
                          Builder, Default, DefaultEnvironment)

from platformio.util import get_serial_ports


def BeforeUpload(target, source, env):  # pylint: disable=W0613,W0621
    upload_options = {}
    if "BOARD" in env:
        upload_options = env.BoardConfig().get("upload", {})

    if env.subst("$UPLOAD_SPEED"):
        env.Append(UPLOADERFLAGS=["-c", "$UPLOAD_SPEED"])
        env.Append(ERASEFLAGS=["-c", "$UPLOAD_SPEED"])

    # extra upload flags
    if "extra_flags" in upload_options:
        env.Append(UPLOADERFLAGS=upload_options.get("extra_flags"))
        env.Append(ERASEFLAGS=upload_options.get("extra_flags"))

    env.AutodetectUploadPort()
    env.Append(UPLOADERFLAGS=["-u", '"$UPLOAD_PORT"'])
    env.Append(ERASEFLAGS=["-u", '"$UPLOAD_PORT"'])
    env.TouchSerialPort("$UPLOAD_PORT", 1200)


env = DefaultEnvironment()

try:
    import pymcuprog
except ImportError:
    env.Execute("$PYTHONEXE -m pip install pymcuprog")

env.Replace(
    AR="avr-gcc-ar",
    AS="avr-as",
    CC="avr-gcc",
    GDB="avr-gdb",
    CXX="avr-g++",
    OBJCOPY="avr-objcopy",
    RANLIB="avr-gcc-ranlib",
    SIZETOOL="avr-size",

    ARFLAGS=["rc"],

    SIZEPROGREGEXP=r"^(?:\.text|\.data|\.rodata|\.bootloader)\s+([0-9]+).*",
    SIZEDATAREGEXP=r"^(?:\.data|\.bss|\.noinit)\s+([0-9]+).* ",
    SIZEEEPROMREGEXP=r"^(?:\.eeprom)\s+([0-9]+).*",
    SIZECHECKCMD="$SIZETOOL -A -d $SOURCES",
    SIZEPRINTCMD='$SIZETOOL --mcu=$BOARD_MCU -C -d $SOURCES',

    UPLOADER="pymcuprog",
    UPLOADERFLAGS=[
		"--erase",
        "-d", "$BOARD_MCU",
        "-t", "uart",
        "-f", "$SOURCES"
    ],
    UPLOADCMD="$UPLOADER $UPLOADERFLAGS write",
    
    ERASEFLAGS=[
        "-d", "$BOARD_MCU",
        "-t", "uart"
    ],
    ERASECMD="$UPLOADER $ERASEFLAGS erase",

    PROGSUFFIX=".elf"
)

env.Append(
    BUILDERS=dict(
        ElfToBin=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "binary",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".bin"
        ),

        ElfToEep=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-j",
                ".eeprom",
                '--set-section-flags=.eeprom="alloc,load"',
                "--no-change-warnings",
                "--change-section-lma",
                ".eeprom=0",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".eep"
        ),

        ElfToHex=Builder(
            action=env.VerboseAction(" ".join([
                "$OBJCOPY",
                "-O",
                "ihex",
                "-R",
                ".eeprom",
                "$SOURCES",
                "$TARGET"
            ]), "Building $TARGET"),
            suffix=".hex"
        )
    )
)

# Allow user to override via pre:script
if env.get("PROGNAME", "program") == "program":
    env.Replace(PROGNAME="firmware")

env.SConscript("frameworks/_bare.py", exports="env")

#
# Target: Build executable and linkable firmware
#

target_elf = env.BuildProgram()
target_firm = env.ElfToHex(join("$BUILD_DIR", "${PROGNAME}"), target_elf)
env.Depends(target_firm, "checkprogsize")

AlwaysBuild(env.Alias("nobuild", target_firm))
target_buildprog = env.Alias("buildprog", target_firm, target_firm)

#
# Target: Print binary size
#

target_size = env.AddPlatformTarget(
    "size",
    target_elf,
    env.VerboseAction("$SIZEPRINTCMD", "Calculating size $SOURCE"),
    "Program Size",
    "Calculate program size",
)

#
# Target: Upload by default .hex file
#

upload_protocol = env.subst("$UPLOAD_PROTOCOL")

if upload_protocol == "custom":
    upload_actions = [env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")]
else:
    upload_actions = [
        env.VerboseAction(BeforeUpload, "Looking for upload port..."),
        #env.VerboseAction("$ERASECMD", "Erasing flash..."),
        env.VerboseAction("$UPLOADCMD", "Uploading $SOURCE")
    ]

    upload_options = env.BoardConfig().get("upload", {})

if int(ARGUMENTS.get("PIOVERBOSE", 0)):
    env.Prepend(UPLOADERFLAGS=["-vinfo"])
    env.Prepend(ERASEFLAGS=["-vinfo"])

env.AddPlatformTarget("upload", target_firm, upload_actions, "Upload")

#
# Setup default targets
#

Default([target_buildprog, target_size])
