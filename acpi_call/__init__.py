from enum import Enum
p = "/proc/acpi/call"


def acpi_call(payload, payload2=None):
    wf = open(p, "w")
    rf = open(p, "r")
    wf.write(payload)
    wf.flush()
    if payload2:
        wf.write(payload2)
    wf.flush()
    wf.close()
    rf.flush()
    result = rf.read()
    rf.close()
    return result


def isBatteryConservation() -> bool:
    result = acpi_call('\_SB.PCI0.LPC0.EC0.BTSM',)
    print(result[:3], len(result[:3]))
    if result[:3] == '0x1':
        return True
    return False


def isRapidCharge() -> bool:
    result = acpi_call('\_SB.PCI0.LPC0.EC0.QCHO')
    print(result[:3], len(result[:3]))
    if result[:3] == '0x1':
        return True
    return False


class Mode(Enum):
    AUTO = 0
    PERF = 1
    SAVE = 2


def getPerfMode() -> Mode:
    result = acpi_call('\_SB.PCI0.LPC0.EC0.FCMO')[:3]
    if result == "0x0":
        return Mode.AUTO
    if result == "0x1":
        return Mode.PERF
    if result == "0x2":
        return Mode.SAVE
    return Mode.AUTO


def setPerfMode(mode: Mode):
    payload1 = ""
    if mode == Mode.AUTO:
        payload1 = '\_SB.PCI0.LPC0.EC0.VPC0.DYTC 0x000FB001'
    if mode == Mode.PERF:
        payload1 = '\_SB.PCI0.LPC0.EC0.VPC0.DYTC 0x0012B001'
    if mode == Mode.SAVE:
        payload1 = '\_SB.PCI0.LPC0.EC0.VPC0.DYTC 0x0013B001'
    payload2 = '\_SB.PCI0.LPC0.EC0.FCMO'
    # print(payload1, payload2)
    result = acpi_call(payload1, payload2)
    # print(result, len(result))
    # print(Mode(int(result[2])))


def setRapidCharge(val: bool) -> bool:
    payload = ""
    if val:
        payload = '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x07'
    else:
        payload = '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x08'
    return (acpi_call(payload, '\_SB.PCI0.LPC0.EC0.QCHO')[:3] == '0x1')


def setBatteryConservation(val: bool) -> bool:
    payload = ""
    if val:
        payload = '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x03'
    else:
        payload = '\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x05'
    return (acpi_call(payload, '\_SB.PCI0.LPC0.EC0.BTSM')[:3] == '0x1')


if __name__ == "__main__":
    print(isRapidCharge())
