def hex_to_rgb(hex_color: str) -> tuple:
    """Convert hex to rgb"""
    if hex_color == '#000':
        return (0, 0, 0)
    elif hex_color == '#fff':
        return (255, 255, 255)
    else:
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def correct_channel(channel: float) -> float:
    """Converts sRGB into linear RGB"""
    return channel / 12.92 if channel <= 0.03928 else ((channel + 0.055) / 1.055) ** 2.4

def get_luminance(rgb) -> float:
    """Calculate the relative luminance of an RGB color."""
    r, g, b = rgb
    r, g, b = correct_channel(r), correct_channel(g), correct_channel(b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def compare_hex_colors(first_color: str, second_color: str) -> tuple:
    """Compare two hex colors and return a tuple wth the darker one first."""
    first_rgb   = hex_to_rgb(first_color)
    second_rgb  = hex_to_rgb(second_color)

    first_luminance = get_luminance(first_rgb)
    second_luminance = get_luminance(second_rgb)

    if first_luminance < second_luminance:
        return second_color, first_color 
    elif first_luminance > second_luminance:
        return first_color, second_color
    else:
        return second_color, first_color 
