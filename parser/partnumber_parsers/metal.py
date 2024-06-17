import parser.series_parser.metal_csi_css as metal_csi_css


def parse_tcr(p):
    if "X" in p:
        return "±100 PPM/°C"
    elif "Z" in p:
        return "±50 PPM/°C"
    elif "/" in p:
        return "±3800 PPM/°C"
    elif "C" in p[3:]:
        return "±200 PPM/°C"
    return "Unknown"


def parse_tolerance(p):
    if "J" in p:
        return "±5 %"
    # отсекаем последний знак ибо на конце бывает F
    # например CR0402-F/-6R19GLF CR0402-F/-6R19GPF
    elif "F" in p[:-1]:
        return "±1 %"
    # elif "D" in p:
    #     return "±0.5 %"
    return "Unknown"


def parse_resistance(p, tolerance):
    res_start = 11
    res_end = 15
    if p.startswith("CST"):
        return float(p.split("-")[2].replace("E", "").replace("R", "."))
    elif "R" not in p[res_start:res_end] and "L" not in p[res_start:res_end]:
        return float(p[res_start:res_end - 1] + "0" * int(p[res_end - 1]))
    elif "R" in p[res_start:res_end]:
        return float(p[res_start:res_end].replace("R", "."))
    elif "L" in p[res_start:res_end]:
        return float(p[res_start:res_end].replace("L", ".")) / (10**int(p[res_start]))

    return "Unknown"


def parse_power(p):
    power_map = {}
    if p[:3] == "CFG" or p[:3] == "CRK" or p[:3] == "CST":
        power_map = {
            "0612": 1.0,
            "0815": 1.0
        }

    elif p[:3] == "CFN":
        power_map = {
            "0402": 0.2,
            "0603": 0.5,
            "0805": 0.75,
            "1206": 1.0
        }

    elif p[:3] == "CRA":
        power_map = {
            "2512": 3.0
        }

    elif p[:3] == "CRE" or p[:3] == "CRG":
        if p[-1] == "2":
            power_map = {"2512": 2.0}
        elif p[-1] == "3":
            power_map = {"2512": 3.0}

    elif p[:3] == "CRF" or p[:3] == "CRS":
        power_map = {
            "0805": 0.5,
            "1206": 1.0,
            "2010": 1.5,
            "2512": 2.0
        }
        if "CRF2512" in p and "J" not in p:
            resistance = parse_resistance(p, parse_tolerance(p))
            if 0.001 < resistance < 0.01:
                power_map = {"2512": 2.0}
            if 0.011 < resistance < 0.5:
                power_map = {"2512": 1.0}

    for key in power_map:
        if key in p:
            return str(power_map[key]) + " W"
    return "Unknown"  # Возвращаем None, если ни одна подстрока не найдена


def parse_packaging(partnumber):
    base_text = " pieces on 180 mm (7 inch) reel"
    quantities = {
        "CST": "4,000",
        "CRG": "4,000",
        "CRF0805": "4,000",
        "CRF1206": "5,000",
        "CRF2010": "4,000",
        "CRF2512": "4,000",
        "CRE": "4,000",
        "CRA": "4,000",
        "CFN0805": "4,000",
        "CFN1206": "4,000",
        "CFN0603": "5,000",
        "CFN0402": "10,000",
        "CFG": "4,000",
        "CRK0612": "5,000",
        "CRK0815": "4,000"
    }
    for key in quantities:
        if key in partnumber[:7]:
            return quantities[key] + base_text

    return "Unknown"


def get_specs(p):
    resistance = tolerance = temperature = power = packaging = "- Unknown"
    if p[:3] == "CSS" or p[:3] == "CSI":
        temperature = metal_csi_css.parse_tcr(p)
        tolerance = metal_csi_css.parse_tolerance(p)
        power = metal_csi_css.parse_power(p)
        packaging = metal_csi_css.parse_packaging(p)
        resistance = metal_csi_css.parse_resistance(p)
    else:
        temperature = parse_tcr(p)
        tolerance = parse_tolerance(p)
        power = parse_power(p)
        packaging = parse_packaging(p)
        resistance = parse_resistance(p, tolerance)
        resistance = str(resistance) + " Ohms"


    return resistance, tolerance, temperature, power, packaging


if __name__ == "__main__":
    print(parse_packaging("CRS1206QFX-1002ELF"))
