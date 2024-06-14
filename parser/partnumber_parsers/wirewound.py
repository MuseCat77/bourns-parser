def ws_series(partnumber):
    res_start = 4
    # на 1 больше всегда
    res_end = 8

    tolerance = "5%"

    power = str(partnumber[2]) + "W"

    resistance = 0
    if "R" not in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end - 1] + "0" * int(partnumber[res_end - 1]))
    elif "R" in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end].replace("R", "."))

    temperature = "±300 PPM/°C"

    resistance = str(resistance) + " Ohm"

    return resistance, tolerance, temperature, power


def w_series(partnumber):
    res_start = res_end = 0
    power = ''

    if len(partnumber) == 9:
        res_start = 4
        res_end = 8
        power = str(partnumber[1:3]) + "W"

    elif len(partnumber) == 8:
        res_start = 3
        res_end = 7
        power = str(partnumber[1]) + "W"

    tolerance = "5%"

    resistance = 0
    if "R" not in partnumber[res_start:res_end]:
        print(partnumber[res_start:res_end - 1])
        print(partnumber[res_start:res_end])
        resistance = float(partnumber[res_start:res_end - 1] + "0" * int(partnumber[res_end - 1]))
    elif "R" in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end].replace("R", "."))

    temperature = "±300 PPM/°C"

    resistance = str(resistance) + " Ohm"

    return resistance, tolerance, temperature, power


def pwr2615_4525_series(partnumber):
    res_start = 8
    res_end = 12

    power = "Unknown"
    if "PWR2615" in partnumber:
        power = "1 W"
    elif "PWR4525" in partnumber:
        power = "2 W"

    tolerance = "Unknown"
    if "J" in partnumber:
        tolerance = "±5%"
    elif "F" in partnumber:
        tolerance = "±1%"
    elif "D" in partnumber:
        tolerance = "±0.5%"

    resistance = 0
    if "R" not in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end - 1] + "0" * int(partnumber[res_end - 1]))
    elif "R" in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end].replace("R", "."))

    temperature = "Unknown"
    if resistance > 10:
        temperature = "±20 PPM/°C"
    elif 1.0 < resistance < 10:
        temperature = "±50 PPM/°C"
    elif 0.1 < resistance < 1.0:
        temperature = "±90 PPM/°C"
    elif resistance < 0.1:
        temperature = "±150 PPM/°C"

    resistance = str(resistance) + " Ohm"

    return resistance, tolerance, temperature, power


# PWR2010N1000F
def pwr2010_series(partnumber):
    res_start = 8
    res_end = 12

    power = "Unknown"
    if "PWR2010" in partnumber:
        power = "0.5 W"
    elif "PWR3014" in partnumber:
        power = "1.0 W"
    elif "PWR4318" in partnumber:
        power = "2.0 W"
    elif "PWR5322" in partnumber:
        power = "3.0 W"

    tolerance = "Unknown"
    if "J" in partnumber:
        tolerance = "5%"
    elif "F" in partnumber:
        tolerance = "1%"
    elif "D" in partnumber:
        tolerance = "0.5%"

    resistance = 0
    if "R" not in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end-1] + "0" * int(partnumber[res_end-1]))
    elif "R" in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end].replace("R", "."))

    temperature = "Unknown"
    if resistance < 0.1:
        temperature = "±200 PPM/°C"
    elif 0.1 < resistance < 0.99:
        temperature = "±90 PPM/°C"
    elif 1.0 < resistance < 10.0:
        temperature = "±50 PPM/°C"
    elif resistance > 10.0:
        temperature = "±20 PPM/°C"

    resistance = str(resistance) + " Ohm"

    return resistance, tolerance, temperature, power


# FW10A1000JA
def fw_series(partnumber):
    res_start = 5
    res_end = 9

    power = str(partnumber[2]) + "W"

    tolerance = "Unknown"
    if "J" in partnumber:
        tolerance = "±5%"

    resistance = 0
    if "R" not in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end - 1] + "0" * int(partnumber[res_end - 1]))
    elif "R" in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end].replace("R", "."))

    temperature = "±200 PPM/°C"

    resistance = str(resistance) + " Ohm"

    return resistance, tolerance, temperature, power

if __name__ == "__main__":
    print(pwr2010_series("PWR2010N1000F"))
