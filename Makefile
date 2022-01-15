run:
	@nohup pkexec env DISPLAY=$$DISPLAY XAUTHORITY=$$XAUTHORITY $$PWD/main.py 1>/dev/null 2>/dev/null &
debug:
	pkexec env DISPLAY=$$DISPLAY XAUTHORITY=$$XAUTHORITY $$PWD/main.py
install:
	mkdir -p /usr/share/ideapad-acpi-tool
	install -dm 755 $$PWD /usr/share/ideapad-acpi-tool
	install -dm 755 $$PWD/acpi_call /usr/share/ideapad-acpi-tool/acpi_call
	install -m 755 $$PWD/acpi_call/__init__.py /usr/share/ideapad-acpi-tool/acpi_call/__init__.py
	install -m 644 $$PWD/*.py /usr/share/ideapad-acpi-tool
	install -m 644 $$PWD/*.pyproject* /usr/share/ideapad-acpi-tool
	install -m 644 $$PWD/*.qml /usr/share/ideapad-acpi-tool
	install -dm 755 $$PWD/icons /usr/share/ideapad-acpi-tool/icons
	install -m 755 $$PWD/icons/* /usr/share/ideapad-acpi-tool/icons
	install -m 644 $$PWD/Makefile /usr/share/ideapad-acpi-tool/Makefile	
	install -m 644 $$PWD/LICENSE /usr/share/ideapad-acpi-tool/LICENSE
	chmod +x /usr/share/ideapad-acpi-tool/main.py
	install -m 644 $$PWD/ideapad-acpi-tool.desktop /usr/share/applications/ideapad-acpi-tool.desktop
uninstall:
	rm -rf /usr/share/ideapad-acpi-tool
	rm -f /usr/share/applications/ideapad-acpi-tool.desktop