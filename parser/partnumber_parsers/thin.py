def parse_resistance(res_start, res_end, partnumber):
    resistance = 0
    if "R" not in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end - 1] + "0" * int(partnumber[res_end - 1]))
    elif "R" in partnumber[res_start:res_end]:
        resistance = float(partnumber[res_start:res_end].replace("R", "."))
    return resistance


# CRT0603-CV-1003ELF
def crt_series(p):
    res_start = 11
    res_end = 15

    tolerance = "Unknown"
    if p[8] == "F":
        tolerance = "±1 %"
    elif p[8] == "D":
        tolerance = "±0.5 %"
    elif p[8] == "C":
        tolerance = "±0.25 %"
    elif p[8] == "B":
        tolerance = "±0.1 %"
    elif p[8] == "A":
        tolerance = "±0.05 %"
    elif p[8] == "P":
        tolerance = "±0.01 %"

    temperature = "Unknown"
    if p[9] == "Z":
        temperature = "±50"
    elif p[9] == "Y":
        temperature = "±25"
    elif p[9] == "X":
        temperature = "±15"
    elif p[9] == "W":
        temperature = "±10"
    elif p[9] == "V":
        temperature = "±5"
    elif p[9] == "U":
        temperature = "±3"
    elif p[9] == "T":
        temperature = "±2"

    temperature += "PPM/°C"

    resistance = str(parse_resistance(res_start, res_end, p)) + " Ohms"

    power = "Unknown"
    if p[3:7] == "0402":
        power = "0,0625 W"
    elif p[3:7] == "0603":
        power = "0,1 W"
    elif p[3:7] == "0805":
        power = "0,125 W"
    elif p[3:7] == "1206":
        power = "0,25 W"

    packaging = "Unknown"
    if p[15] == "G":
        packaging = "Paper tape (10K pcs.) on 7 ˝ plastic reel"
    elif p[15] == "E":
        packaging = "Paper tape (5K pcs.) on 7 ˝ plastic reel"
    return resistance, tolerance, temperature, power, packaging