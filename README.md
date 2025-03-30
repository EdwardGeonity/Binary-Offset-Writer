🔧 Binary Offset Writer – User Guide

This small program allows you to write binary data into specific locations inside another binary file. It’s useful for firmware tuning, patching or updating internal data blocks in system libraries.
💡 What it does:

    You open a binary file (.bin or .so).

    The program looks for a .txt file with offset instructions.

    You select a block (like GainMap1, Golden2, etc.) from a list.

    You click “Write data to offset” to insert data into the selected location.

🧩 Offset map example:

GainMap1|0x3738,0xD454|0xDD0

    GainMap1: block name shown in the list.

    0x3738,0xD454: memory addresses where the data will be written.

    0xDD0: how many bytes will be written.

✍️ How to use:

    Start the app. Choose your main binary file (.so or .bin).

    The program will try to find an .txt file with the same name to read the offset map.

        If not found, it will ask you to pick one manually.

    Select a section from the dropdown menu.

    Click “Write data to offset”.

        If a file with the right name isn’t found, it will ask you to choose one manually.

        If the file starts with 82000000, that part will be skipped.

    Done! The data is written in the right place.

    You can also:

        Open the binary file in your default editor.

        Close the app with the Exit button.
