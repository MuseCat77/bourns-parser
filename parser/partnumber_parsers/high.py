def parse_resistance(p):
    res_start = 11
    res_end = 15
    if "L" in p[res_start:res_end]:
        return float(p[res_start:res_end].replace("L", "."))
    return "Unknown"


def parse_packaging(p):
    if "6918" in p:
        # 0, 1, 2
        if p[-2] == "0":
            return "Bulk Pack (50 pcs. per bag)"
        # 0, 1, 2
        elif p[-2] == "T":
            return "Tray Pack (52 pcs. per bag)"
        # x0, x1, x2
        elif p[-2] == "2" or p[-2] == "3":
            return "Tray Pack (30 pcs. per bag)"
        return "Unknown"

    elif "7036" in p:
        # 0, 1, 2
        if p[-2] == "0":
            return "Bulk Pack (50 pcs. per bag)"
        # 0, 2
        elif p[-2] == "T" and (p[-1] == "0" or p[-1] == "2"):
            return "Tray Pack (30 pcs. per bag)"
        # 1
        elif p[-2] == "T" and p[-1] == "1":
            return "Tray Pack (28 pcs. per bag)"
        # x0, x1, x2
        elif p[-2] == "2" or p[-2] == "3":
            return "Tray Pack (20 pcs. per bag)"
        return "Unknown"

    elif "8518" in p:
        # 0, 1, 2
        if p[-2] == "0":
            return "Bulk Pack (50 pcs. per bag)"
        # 0, 2
        elif p[-2] == "T" and (p[-1] == "0" or p[-1] == "2"):
            return "Tray Pack (30 pcs. per bag)"
        # 1
        elif p[-2] == "T" and p[-1] == "1":
            return "Tray Pack (32 pcs. per bag)"
        # x0, x1, x2
        elif p[-2] == "2" or p[-2] == "3":
            return "Tray Pack (24 pcs. per bag)"
        return "Unknown"

    elif "8536" in p:
        # 0, 1, 2
        if p[-2] == "0":
            return "Bulk Pack (50 pcs. per bag)"
        # 0, 1, 2
        elif p[-2] == "T":
            return "Tray Pack (15 pcs. per bag)"
        # x0, x1, x2
        elif p[-2] == "2" or p[-2] == "3":
            return "Tray Pack (16 pcs. per bag)"
        return "Unknown"


def get_specs(p):
    return parse_resistance(p), parse_packaging(p)
