# Configuring OpenBCI GUI

Since the OpenBCI GUI determines whether or not a devices is a Cyton by inspecting the vendor information on the USB controller, any device that was made with a different controller will by default not be found. To rectify this we made a patch to the OpenBCI GUI that removed the check for vendor specific indentification on the USB controller. In order to use this changes first set up an envirnment to compile the OpenBCI GUI. Details on how to do this can be found in their [wiki](https://github.com/OpenBCI/OpenBCI_GUI/wiki/Developer-Setup). After set up simply follow the commands below.

```bash
cd <This directory>
cp UART.patch <OpenBCI_GUI root directory>
cd <OpenBCI_GUI root directory>
git apply UART.patch
```

After making these changes if you follow the steps on the OpenBCI_GUI documentation to compile the project. Then the filtering that would prevent the custom design to be selectable.