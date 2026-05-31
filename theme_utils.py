def get_colors(theme: str) -> dict:
    """Return a dictionary of color values based on the theme ("light" or "dark").
    The keys correspond to the main UI elements used throughout the app.
    """
    if theme == "dark":
        return {
            "background": "#0F172A",
            "secondary_background": "#1E293B",
            "text": "#F8FAFC",
            "primary": "#0071CE",
            "secondary": "#FFC220",
        }
    # light theme defaults
    return {
        "background": "#FFFFFF",
        "secondary_background": "#F3F4F6",
        "text": "#0F172A",
        "primary": "#0071CE",
        "secondary": "#FFC220",
    }

# Convenience constants for direct imports
LIGHT_COLORS = get_colors("light")
DARK_COLORS = get_colors("dark")
