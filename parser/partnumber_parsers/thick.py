def parse_tcr(p):
    if "W" in p:
        return "±200 PPM/°C"
    elif "X" in p:
        return "±200 PPM/°C"
    elif "X" in p:
        return "±200 PPM/°C"
    elif "FV" in p or "JV" in p or "DV" in p:
        return "±300 PPM/°C"
    elif "/" in p:
        return "0 PPM/°C"
    elif "Z" in p:
        if "CRM0805" in p or "CRM1206" in p or "CRM2010" in p:
            return "150 PPM/°C"
        elif p[2].isdigit() and p[:2] == "CR":
            return "400 PPM/°C"
    # elif "CRM0603A" in p:
    #     return "150 PPM/°C"
    return "Unknown"


def parse_tolerance(p):
    if "J" in p:
        return "±5 %"
    # отсекаем последний знак ибо на конце бывает F
    # например CR0402-F/-6R19GLF CR0402-F/-6R19GPF
    elif "F" in p[:-1]:
        return "±1 %"
    elif "D" in p:
        return "±0.5 %"
    return "Unknown"


def parse_resistance(p, tolerance):
    res_start = 0
    res_end = 0
    # -----------------------------
    # CR серия
    # -----------------------------
    if p[2].isdigit() and p[:2] == "CR":
        # resistance
        # если вот эта вот дурацкая серия с длинным типоразмером, то у нее свой оффсет
        if p.startswith("CR01005"):
            if tolerance == "±1 %":
                res_start = 11
                res_end = 15

            # если точность 5%, то на сопротивление уходит три знака
            elif tolerance == "±5 %":
                res_start = 11
                res_end = 14
        else:
            # если точность 1%, то на сопротивление уходит 4 знака
            if tolerance == "±1 %":
                res_start = 10
                res_end = 14

            # если точность 5%, то на сопротивление уходит три знака
            elif tolerance == "±5 %":
                res_start = 10
                res_end = 13
    # -----------------------------
    # Остальные серии
    # -----------------------------
    else:
        # если точность 1%, то на сопротивление уходит 4 знака
        if tolerance == "±1 %" or tolerance == "±0.5 %":
            res_start = 11
            res_end = 15

        # если точность 5%, то на сопротивление уходит три знака
        elif tolerance == "±5 %":
            res_start = 11
            res_end = 14
    # -----------------------------
    # Парсим само число
    # -----------------------------
    if "R" not in p[res_start:res_end]:
        return float(p[res_start:res_end - 1] + "0" * int(p[res_end - 1]))
    elif "R" in p[res_start:res_end]:
        return float(p[res_start:res_end].replace("R", "."))
    return "Unknown"


def parse_power(p):
    power_map = {}
    if p[:2] == "CR" or p[:3] == "CHV":
        power_map = {
            "0603": 0.1,
            "0805": 0.125,
            "1206": 0.25,
            "2512": 1.0,
            "2010": 0.5,
            "01005": 0.03125,
            "0201": 0.05,
            "0402": 0.0625,
        }
    elif p[:3] == "CHP":
        power_map = {
            "0603": 0.33,
            "0805": 0.5,
            "1206": 0.75,
            "2512": 3.0
        }
    elif p[:3] == "CMP":
        power_map = {
            "0603": 0.25,
            "0805": 0.5,
            "1206": 0.75,
            "2512": 1.5,
            "2010": 1.0
        }
    elif p[:3] == "CRL":
        power_map = {
            "0603": 0.125,
            "0805": 0.25,
            "1206": 0.5,
            "2512": 1.0,
            "2010": 0.75
        }
    elif p[:3] == "CRM" or p[:3] == "CRS":
        power_map = {
            "0603": 0.125,
            "0805": 0.25,
            "1206": 0.5,
            "2512": 2.0,
            "2010": 1.0,
            "1210": 0.5,
        }
    for key in power_map:
        if key in p:
            return str(power_map[key]) + " W"
    return "Unknown"  # Возвращаем None, если ни одна подстрока не найдена


def parse_packaging(partnumber):
    base_text = " pieces on 180 mm (7 inch) reel"
    quantities = {
        "CHP2512": "3,000",
        "2010": "4,000",
        "2512": "4,000",
        "0603": "5,000",
        "0805": "5,000",
        "1206": "5,000",
        "1210": "5,000",
        "01005": "10,000",
        "0201": "10,000",
        "0402": "10,000"
    }
    for key in quantities:
        if key in partnumber[:7]:
            return quantities[key] + base_text

    return "Unknown"


def get_specs(p):
    temperature = parse_tcr(p)
    tolerance = parse_tolerance(p)
    power = parse_power(p)
    packaging = parse_packaging(p)
    resistance = parse_resistance(p, tolerance)

    if "CRM0805AD" in p or "CRM0805AF" in p or "CRM0603A" in p:
        if 1 <= resistance < 10:
            if temperature == "±200 PPM/°C":
                temperature = "±150 PPM/°C"

    resistance = str(resistance) + " Ohms"

    return resistance, tolerance, temperature, power, packaging



if __name__ == "__main__":
    print(parse_packaging("CRS1206QFX-1002ELF"))
