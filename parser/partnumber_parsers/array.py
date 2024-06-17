def parse_packaging(p):
    if "16" in p[:4]:
        return "5000 pcs. per reel"
    else:
        return "10000 pcs. per reel"


def parse_tolerance(p):
    if p[-4] == "J":
        return "±5%"

    if p[-4] == "F":
        return "±1%"


def parse_resistance(p, tolerance):
    res_start = -7
    res_end = -4
    # 1% - 4 символа
    # 5% - 3 символа
    if tolerance == "1%":
        res_start = -8
        res_end = -4
    if tolerance == "5%":
        res_start = -7
        res_end = -4

    if "R" not in p[res_start:res_end]:
        return float(p[res_start:res_end - 1] + "0" * int(p[res_end - 1]))
    elif "R" in p[res_start:res_end]:
        return float(p[res_start:res_end].replace("R", "."))


def parse_ppm(p, resistance):
    if p.startswith("CAY16A"):
        if 10 <= resistance <= 1000000:
            return "±200 PPM/°C"
        elif 3 <= resistance < 10:
            return "±400 PPM/°C"

    elif p.startswith("CAY16"):
        return "±200 PPM/°C"

    elif p.startswith("CAY10"):
        if 10 <= resistance <= 1000000:
            return "±200 PPM/°C"
        elif 3 <= resistance < 10:
            return "±500 PPM/°C"

    elif p.startswith("CAT16"):
        return "±200 PPM/°C"

    elif p.startswith("CAT10A"):
        return "±300 PPM/°C"

    elif p.startswith("CAT10"):
        return "±200 PPM/°C"


def get_specs(p):
    tolerance = parse_tolerance(p)
    resistance = parse_resistance(p, tolerance)
    temperature = parse_ppm(p, resistance)
    resistance = str(resistance) + " Ohms"
    packaging = parse_packaging(p)

    return resistance, tolerance, temperature, packaging
