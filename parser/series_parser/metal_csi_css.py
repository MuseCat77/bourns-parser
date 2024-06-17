def parse_tolerance(p):
    if p[-1] == "F":
        return "±1 %"
    elif p[-1] == "G":
        return "±2 %"
    elif p[-1] == "J":
        return "±5 %"
    elif p[-1].isdigit():
        return "0"
    return "Unknown"


def parse_tcr(p):
    patterns = {
        "CSI2H-2512R-L300": "±150 PPM/°C",
        "CSI2H-2512R-L500": "±100 PPM/°C",
        "CSI2H-2512R-1L00": "±75 PPM/°C",
        "CSI2H-2512K-1L80": "±75 PPM/°C",
        "CSI2H-2512K-2L00": "±75 PPM/°C",
        "CSI2H-2512K-2L30": "±75 PPM/°C",
        "CSI2H-2512K-3L00": "±75 PPM/°C",
        "CSI2H-2512K-3L50": "±75 PPM/°C",
        "CSI2H-3920R-L200": "±100 PPM/°C",
        "CSI2H-3920R-L300": "±100 PPM/°C",
        "CSI2H-3920R-L400": "±100 PPM/°C",
        "CSI2H-3920R-L500": "±100 PPM/°C",
        "CSI2H-3920R-L700": "±100 PPM/°C",
        "CSI2H-3920K-1L00": "±100 PPM/°C",
        "CSI2H-3920K-2L00": "±75 PPM/°C",
        "CSI2H-3920K-2L50": "±75 PPM/°C",
        "CSI2H-3920K-3L00": "±75 PPM/°C",
        "CSI2H-5930R-L200": "±150 PPM/°C",
        "CSI2H-5930R-L300": "±150 PPM/°C",
        "CSI2H-5930R-L500": "±100 PPM/°C",
        "CSI2H-5930K-1L00": "±75 PPM/°C",
        "CSI2H-5930K-2L00": "±75 PPM/°C",
        "CSS2H-5930R-L200": "±150 PPM/°C",
        "CSS2H-5930R-L300": "±150 PPM/°C",
        "CSS2H-5930R-L500": "±100 PPM/°C",
        "CSS2H-5930K-1L00": "±75 PPM/°C",
        "CSS2H-5930K-2L00": "±75 PPM/°C",
        "CSS2H-5930K-3L00": "±75 PPM/°C",
        "CSS4J-4026R-L200": "±150 PPM/°C",
        "CSS4J-4026R-L300": "±100 PPM/°C",
        "CSS4J-4026R-L500": "±100 PPM/°C",
        "CSS4J-4026R-1L00": "±75 PPM/°C",
        "CSS4J-4026K-2L00": "±75 PPM/°C",
        "CSS4J-4026K-3L00": "±75 PPM/°C",
        "CSS4J-4026K-5L00": "±75 PPM/°C",
        "CSS2H-2512R-L300": "±150 PPM/°C",
        "CSS2H-2512R-L500": "±100 PPM/°C",
        "CSS2H-2512R-1L00": "±75 PPM/°C",
        "CSS2H-2512K-1L80": "±75 PPM/°C",
        "CSS2H-2512K-2L00": "±75 PPM/°C",
        "CSS2H-2512K-2L30": "±75 PPM/°C",
        "CSS2H-2512K-3L00": "±75 PPM/°C",
        "CSS2H-2512K-3L50": "±75 PPM/°C",
        "CSS2H-2512K-4L00": "±75 PPM/°C",
        "CSS2H-2512K-5L00": "±75 PPM/°C",
        "CSS2H-3920R-L200": "±100 PPM/°C",
        "CSS2H-3920R-L300": "±100 PPM/°C",
        "CSS2H-3920R-L500": "±100 PPM/°C",
        "CSS2H-3920R-L700": "±100 PPM/°C",
        "CSS2H-3920R-1L00": "±100 PPM/°C",
        "CSS2H-3920K-2L00": "±75 PPM/°C",
        "CSS2H-3920K-2L50": "±75 PPM/°C",
        "CSS2H-3920K-3L00": "±75 PPM/°C",
        "CSS2H-3920K-4L00": "±75 PPM/°C",
        "CSS2H-3920K-5L00": "±75 PPM/°C"
    }

    for pattern in patterns:
        if p.startswith(pattern):
            return patterns[pattern]

    return "Unknown"


def parse_power(p):
    patterns = {
        "CSI2H-2512C-000": "100 A",
        "CSI2H-2512R-L300": "6 W",
        "CSI2H-2512R-L500": "6 W",
        "CSI2H-2512R-1L00": "5 W",
        "CSI2H-2512K-1L80": "5 W",
        "CSI2H-2512K-2L00": "5 W",
        "CSI2H-2512K-2L30": "5 W",
        "CSI2H-2512K-3L00": "4 W",
        "CSI2H-2512K-3L50": "4 W",
        "CSI2H-3920C-000": "160 A",
        "CSI2H-3920R-L200": "12 W",
        "CSI2H-3920R-L300": "10 W",
        "CSI2H-3920R-L500": "9 W",
        "CSI2H-3920R-L700": "8 W",
        "CSI2H-3920R-1L00": "8 W",
        "CSI2H-3920K-2L00": "6 W",
        "CSI2H-3920K-2L50": "5 W",
        "CSI2H-3920K-3L00": "5 W",
        "CSI2H-5930C-000": "160 A",
        "CSI2H-5930R-L200": "15 W",
        "CSI2H-5930R-L300": "15 W",
        "CSI2H-5930R-L500": "8 W",
        "CSI2H-5930K-1L00": "9 W",
        "CSI2H-5930K-2L00": "7 W",
        "CSI4J-4026R-L200": "11 W",
        "CSI4J-4026R-L300": "10 W",
        "CSI4J-4026R-L500": "10 W",
        "CSI4J-4026R-1L00": "8 W",
        "CSI4J-4026K-2L00": "6 W",
        "CSS2H-2512C-000": "100 A",
        "CSS2H-2512R-L300": "6 W",
        "CSS2H-2512R-L500": "6 W",
        "CSS2H-2512R-1L00": "5 W",
        "CSS2H-2512K-1L80": "5 W",
        "CSS2H-2512K-2L00": "5 W",
        "CSS2H-2512K-2L30": "5 W",
        "CSS2H-2512K-3L00": "4 W",
        "CSS2H-2512K-3L50": "4 W",
        "CSS2H-2512K-4L00": "3 W",
        "CSS2H-2512K-5L00": "2.5 W",
        "CSS2H-3920C-000": "160 A",
        "CSS2H-3920R-L200": "12 W",
        "CSS2H-3920R-L300": "10 W",
        "CSS2H-3920R-L500": "9 W",
        "CSS2H-3920R-L700": "8 W",
        "CSS2H-3920R-1L00": "8 W",
        "CSS2H-3920K-2L00": "6 W",
        "CSS2H-3920K-2L50": "5 W",
        "CSS2H-3920K-3L00": "5 W",
        "CSS2H-3920K-4L00": "4 W",
        "CSS2H-3920K-5L00": "3 W",
        "CSS2H-5930C-000": "160 A",
        "CSS2H-5930R-L200": "15 W",
        "CSS2H-5930R-L300": "15 W",
        "CSS2H-5930R-L500": "8 W",
        "CSS2H-5930K-1L00": "9 W",
        "CSS2H-5930K-2L00": "7 W",
        "CSS2H-5930K-3L00": "6 W",
        "CSS4J-4026R-L200": "11 W",
        "CSS4J-4026R-L300": "10 W",
        "CSS4J-4026R-L500": "10 W",
        "CSS4J-4026R-1L00": "8 W",
        "CSS4J-4026K-2L00": "6 W",
        "CSS4J-4026K-3L00": "5 W",
        "CSS4J-4026K-5L00": "4 W"
    }
    for pattern in patterns:
        if p.startswith(pattern):
            return patterns[pattern]

    return "Unknown"


def parse_resistance(p):
    patterns = {
        "CSI2H-2512C-000": "< 0.1 mOhm",
        "CSI2H-2512R-L300": "0.3 mOhm",
        "CSI2H-2512R-L500": "0.5 mOhm",
        "CSI2H-2512R-1L00": "1.0 mOhm",
        "CSI2H-2512K-1L80": "1.8 mOhm",
        "CSI2H-2512K-2L00": "2.0 mOhm",
        "CSI2H-2512K-2L30": "2.3 mOhm",
        "CSI2H-2512K-3L00": "3.0 mOhm",
        "CSI2H-2512K-3L50": "3.5 mOhm",
        "CSI2H-3920C-000": "< 0.2 mOhm",
        "CSI2H-3920R-L200": "0.2 mOhm",
        "CSI2H-3920R-L300": "0.3 mOhm",
        "CSI2H-3920R-L500": "0.5 mOhm",
        "CSI2H-3920R-L700": "0.7 mOhm",
        "CSI2H-3920R-1L00": "1.0 mOhm",
        "CSI2H-3920K-2L00": "2.0 mOhm",
        "CSI2H-3920K-2L50": "2.5 mOhm",
        "CSI2H-3920K-3L00": "3.0 mOhm",
        "CSI2H-5930C-000": "< 0.2 mOhm",
        "CSI2H-5930R-L200": "0.2 mOhm",
        "CSI2H-5930R-L300": "0.3 mOhm",
        "CSI2H-5930R-L500": "0.5 mOhm",
        "CSI2H-5930K-1L00": "1.0 mOhm",
        "CSI2H-5930K-2L00": "2.0 mOhm",
        "CSI4J-4026R-L200": "0.2 mOhm",
        "CSI4J-4026R-L300": "0.3 mOhm",
        "CSI4J-4026R-L500": "0.5 mOhm",
        "CSI4J-4026R-1L00": "1.0 mOhm",
        "CSI4J-4026K-2L00": "2.0 mOhm",
        "CSS2H-2512C-000": "< 0.1 mOhm",
        "CSS2H-2512R-L300": "0.3 mOhm",
        "CSS2H-2512R-L500": "0.5 mOhm",
        "CSS2H-2512R-1L00": "1.0 mOhm",
        "CSS2H-2512K-1L80": "1.8 mOhm",
        "CSS2H-2512K-2L00": "2.0 mOhm",
        "CSS2H-2512K-2L30": "2.3 mOhm",
        "CSS2H-2512K-3L00": "3.0 mOhm",
        "CSS2H-2512K-3L50": "3.5 mOhm",
        "CSS2H-2512K-4L00": "4.0 mOhm",
        "CSS2H-2512K-5L00": "5.0 mOhm",
        "CSS2H-3920C-000": "< 0.2 mOhm",
        "CSS2H-3920R-L200": "0.2 mOhm",
        "CSS2H-3920R-L300": "0.3 mOhm",
        "CSS2H-3920R-L500": "0.5 mOhm",
        "CSS2H-3920R-L700": "0.7 mOhm",
        "CSS2H-3920R-1L00": "1.0 mOhm",
        "CSS2H-3920K-2L00": "2.0 mOhm",
        "CSS2H-3920K-2L50": "2.5 mOhm",
        "CSS2H-3920K-3L00": "3.0 mOhm",
        "CSS2H-3920K-4L00": "4.0 mOhm",
        "CSS2H-3920K-5L00": "5.0 mOhm",
        "CSS2H-5930C-000": "< 0.2 mOhm",
        "CSS2H-5930R-L200": "0.2 mOhm",
        "CSS2H-5930R-L300": "0.3 mOhm",
        "CSS2H-5930R-L500": "0.5 mOhm",
        "CSS2H-5930K-1L00": "1.0 mOhm",
        "CSS2H-5930K-2L00": "2.0 mOhm",
        "CSS2H-5930K-3L00": "3.0 mOhm",
        "CSS4J-4026R-L200": "0.2 mOhm",
        "CSS4J-4026R-L300": "0.3 mOhm",
        "CSS4J-4026R-L500": "0.5 mOhm",
        "CSS4J-4026R-1L00": "1.0 mOhm",
        "CSS4J-4026K-2L00": "2.0 mOhm",
        "CSS4J-4026K-3L00": "3.0 mOhm",
        "CSS4J-4026K-5L00": "5.0 mOhm"
    }

    for pattern in patterns:
        if p.startswith(pattern):
            return patterns[pattern]

    try:
        return str(float(p.split("-")[2].replace("F", "").replace("J", "").replace("L", "."))) + " Ohms"

    except Exception:
        return "Unknown"


def parse_packaging(p):
    patterns = {
        'SCI2H-2512': "3,000 per reel",
        'SCI2H-3920': "3,000 per reel",
        'SCI2H-5930': "1,500 per reel",
        'SCI4J-4026': "1,500 per reel",
        'CSS2H-2512': "3,000 per reel and 1,000 per mini reel",
        'CSS2H-3920': "3,000 per reel and 1,000 per mini reel",
        'CSS2H-5930': "1,500 per reel and 500 per mini reel",
        'CSS4J-4026': "1,500 per reel and 400 per mini reel",
    }

    for pattern in patterns:
        if p.startswith(pattern):
            return patterns[pattern]
    return "Unknown"