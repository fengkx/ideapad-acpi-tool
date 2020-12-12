# IdeaPad ACPI Tool

> GUI tool to config IdeaPad ACPI setting

The project is build on `PySide2 (PyQt5)` and `acpi_call`. You will need to install the two pacakge and Qt5 runtime first. Root privilege is required for ACPI call. You need to install `polkit` to be the root privilege gui frontend

For example in ArchLinux

```sh
sudo pacman -S qt5-base acpi_call pyside2 polkit
```

## Install

```sh
make run # first Check wether the app can run, otherwise install the missing dependency
sudo make install # It install the app to /usr/share/ideapad-acpi-tool and add the desktop entry


sudo make uninstall # You can uninstall by this command
```

Then You need to enable `acpi_call` see https://wiki.archlinux.org/index.php/Lenovo_IdeaPad_5_15are05#System_Performance_Mode

## Notice

The project is tested on IdeaPad 5 15 2021 ARE(小新 Air15 2021 AMD) model. And the acpi call comes from archwiki. It should be able to use in other IdeaPad machine as long as the acpi call stay the same. such as [Lenovo_IdeaPad_S540_13ARE (小新 pro13)](https://wiki.archlinux.org/index.php/Lenovo_IdeaPad_S540_13ARE#System_Performance_Mode)
