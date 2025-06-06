# Add text properties to satisfy the following colors for json strings
# COLOR_BLACK = (0, 0, 0, 1)
# COLOR_RED = (.93, 0, 0, 1)
# COLOR_GREEN = (0, 1, .5, 1)
# COLOR_YELLOW = (.98, .98, .82, 1)
# COLOR_BLUE = (.4, .58, .93, 1)
# COLOR_MAGENTA = (.93, 0, .93, 1)
# COLOR_CYAN = (0, .93, .93, 1)
# COLOR_WHITE = (1, 1, 1, 1)
#
# COLOR_PLUM = (.69, .6, .93, 1)
# COLOR_SLATEBLUE = (.43, .54, .9, 1)
# COLOR_SALMON = (.97, .5, .45, 1)
#
# COLOR_MAP = {
#     'black': COLOR_BLACK,
#     'red': COLOR_RED,
#     'green': COLOR_GREEN,
#     'yellow': COLOR_YELLOW,
#     'blue': COLOR_BLUE,
#     'magenta': COLOR_MAGENTA,
#     'cyan': COLOR_CYAN,
#     'white': COLOR_WHITE,
#     'plum': COLOR_PLUM,
#     'slateblue': COLOR_SLATEBLUE,
#     'salmon': COLOR_SALMON
# }
from typing import List, NamedTuple

from panda3d.core import TextProperties, TextPropertiesManager

from toontown.archipelago.util.net_utils import JSONPartFormatter, JSONMessagePart

__TEXT_PROPERTIES_MANAGER = TextPropertiesManager.getGlobalPtr()

__JSON_COLOR_CODE_TO_TEXT_PROPERTY = {}


# Called locally to register a new constant TextProperties
def __register_property(json_color_code: str, text_property_code: str, properties: TextProperties):
    __JSON_COLOR_CODE_TO_TEXT_PROPERTY[json_color_code] = text_property_code
    __TEXT_PROPERTIES_MANAGER.setProperties(text_property_code, properties)


# Now define all our TextProperty instances, first define what the code is for Panda3D, this isn't important
# Instantiate a TextProperties instance and tweak the settings desired
# Register it using __register_property() and provide the Panda3D code, the JSON code, then the TextProperties instance


# Black text
TEXT_PROPERTIES_CODE_BLACK = "json_black"
__TEXT_PROPERTIES_BLACK = TextProperties()
__TEXT_PROPERTIES_BLACK.setTextColor(*JSONPartFormatter.COLOR_BLACK)
__register_property('black', TEXT_PROPERTIES_CODE_BLACK, __TEXT_PROPERTIES_BLACK)


# Gunmetal Gray text
TEXT_PROPERTIES_CODE_GUNMETAL = "json_gunmetal"
__TEXT_PROPERTIES_GUNMETAL = TextProperties()
__TEXT_PROPERTIES_GUNMETAL.setTextColor(*JSONPartFormatter.COLOR_GUNMETAL)
__register_property('gunmetal', TEXT_PROPERTIES_CODE_GUNMETAL, __TEXT_PROPERTIES_GUNMETAL)

# Gray text
TEXT_PROPERTIES_CODE_GRAY = "json_gray"
__TEXT_PROPERTIES_GRAY = TextProperties()
__TEXT_PROPERTIES_GRAY.setTextColor(*JSONPartFormatter.COLOR_GRAY)
__register_property('gray', TEXT_PROPERTIES_CODE_GRAY, __TEXT_PROPERTIES_GRAY)

# Silver text
TEXT_PROPERTIES_CODE_SILVER = "json_silver"
__TEXT_PROPERTIES_SILVER = TextProperties()
__TEXT_PROPERTIES_SILVER.setTextColor(*JSONPartFormatter.COLOR_SILVER)
__register_property('silver', TEXT_PROPERTIES_CODE_SILVER, __TEXT_PROPERTIES_SILVER)


# Brown text
TEXT_PROPERTIES_CODE_BROWN = "json_brown"
__TEXT_PROPERTIES_BROWN = TextProperties()
__TEXT_PROPERTIES_BROWN.setTextColor(*JSONPartFormatter.COLOR_BROWN)
__register_property('brown', TEXT_PROPERTIES_CODE_BROWN, __TEXT_PROPERTIES_BROWN)


# Gold text
TEXT_PROPERTIES_CODE_GOLD = "json_gold"
__TEXT_PROPERTIES_GOLD = TextProperties()
__TEXT_PROPERTIES_GOLD.setTextColor(*JSONPartFormatter.COLOR_GOLD)
__register_property('gold', TEXT_PROPERTIES_CODE_GOLD, __TEXT_PROPERTIES_GOLD)


# Red text
TEXT_PROPERTIES_CODE_RED = "json_red"
__TEXT_PROPERTIES_RED = TextProperties()
__TEXT_PROPERTIES_RED.setTextColor(*JSONPartFormatter.COLOR_RED)
__register_property('red', TEXT_PROPERTIES_CODE_RED, __TEXT_PROPERTIES_RED)


# Deep Red text
TEXT_PROPERTIES_CODE_DEEP_RED = "json_deep_red"
__TEXT_PROPERTIES_DEEP_RED = TextProperties()
__TEXT_PROPERTIES_DEEP_RED.setTextColor(*JSONPartFormatter.COLOR_DEEP_RED)
__register_property('deep_red', TEXT_PROPERTIES_CODE_DEEP_RED, __TEXT_PROPERTIES_DEEP_RED)


# Green text
TEXT_PROPERTIES_CODE_GREEN = "json_green"
__TEXT_PROPERTIES_GREEN = TextProperties()
__TEXT_PROPERTIES_GREEN.setTextColor(*JSONPartFormatter.COLOR_GREEN)
__register_property('green', TEXT_PROPERTIES_CODE_GREEN, __TEXT_PROPERTIES_GREEN)


# Yellow text
TEXT_PROPERTIES_CODE_YELLOW = "json_yellow"
__TEXT_PROPERTIES_YELLOW = TextProperties()
__TEXT_PROPERTIES_YELLOW.setTextColor(*JSONPartFormatter.COLOR_YELLOW)
__register_property('yellow', TEXT_PROPERTIES_CODE_YELLOW, __TEXT_PROPERTIES_YELLOW)


# Blue text
TEXT_PROPERTIES_CODE_BLUE = "json_blue"
__TEXT_PROPERTIES_BLUE = TextProperties()
__TEXT_PROPERTIES_BLUE.setTextColor(*JSONPartFormatter.COLOR_BLUE)
__register_property('blue', TEXT_PROPERTIES_CODE_BLUE, __TEXT_PROPERTIES_BLUE)


# Magenta text
TEXT_PROPERTIES_CODE_MAGENTA = "json_magenta"
__TEXT_PROPERTIES_MAGENTA = TextProperties()
__TEXT_PROPERTIES_MAGENTA.setTextColor(*JSONPartFormatter.COLOR_MAGENTA)
__register_property('magenta', TEXT_PROPERTIES_CODE_MAGENTA, __TEXT_PROPERTIES_MAGENTA)


# Purple text
TEXT_PROPERTIES_CODE_PURPLE = "json_purple"
__TEXT_PROPERTIES_PURPLE = TextProperties()
__TEXT_PROPERTIES_PURPLE.setTextColor(*JSONPartFormatter.COLOR_PURPLE)
__register_property('purple', TEXT_PROPERTIES_CODE_PURPLE, __TEXT_PROPERTIES_PURPLE)


# Cyan text
TEXT_PROPERTIES_CODE_CYAN = "json_cyan"
__TEXT_PROPERTIES_CYAN = TextProperties()
__TEXT_PROPERTIES_CYAN.setTextColor(*JSONPartFormatter.COLOR_CYAN)
__register_property('cyan', TEXT_PROPERTIES_CODE_CYAN, __TEXT_PROPERTIES_CYAN)


# Light Blue text
TEXT_PROPERTIES_CODE_LIGHT_BLUE = "json_light_blue"
__TEXT_PROPERTIES_LIGHT_BLUE = TextProperties()
__TEXT_PROPERTIES_LIGHT_BLUE.setTextColor(*JSONPartFormatter.COLOR_LIGHT_BLUE)
__register_property('light_blue', TEXT_PROPERTIES_CODE_LIGHT_BLUE, __TEXT_PROPERTIES_LIGHT_BLUE)


# White text
TEXT_PROPERTIES_CODE_WHITE = "json_white"
__TEXT_PROPERTIES_WHITE = TextProperties()
__TEXT_PROPERTIES_WHITE.setTextColor(*JSONPartFormatter.COLOR_WHITE)
__register_property('white', TEXT_PROPERTIES_CODE_WHITE, __TEXT_PROPERTIES_WHITE)


# Plum text
TEXT_PROPERTIES_CODE_PLUM = "json_plum"
__TEXT_PROPERTIES_PLUM = TextProperties()
__TEXT_PROPERTIES_PLUM.setTextColor(*JSONPartFormatter.COLOR_PLUM)
__register_property('plum', TEXT_PROPERTIES_CODE_PLUM, __TEXT_PROPERTIES_PLUM)


# slateblue text
TEXT_PROPERTIES_CODE_SLATEBLUE = "json_slateblue"
__TEXT_PROPERTIES_SLATEBLUE = TextProperties()
__TEXT_PROPERTIES_SLATEBLUE.setTextColor(*JSONPartFormatter.COLOR_SLATEBLUE)
__register_property('slateblue', TEXT_PROPERTIES_CODE_SLATEBLUE, __TEXT_PROPERTIES_SLATEBLUE)


# salmon text
TEXT_PROPERTIES_CODE_SALMON = "json_salmon"
__TEXT_PROPERTIES_SALMON = TextProperties()
__TEXT_PROPERTIES_SALMON.setTextColor(*JSONPartFormatter.COLOR_SALMON)
__register_property('salmon', TEXT_PROPERTIES_CODE_SALMON, __TEXT_PROPERTIES_SALMON)


# Plastic White text
TEXT_PROPERTIES_CODE_PLASTIC_WHITE = "json_plastic_white"
__TEXT_PROPERTIES_PLASTIC_WHITE = TextProperties()
__TEXT_PROPERTIES_PLASTIC_WHITE.setTextColor(*JSONPartFormatter.COLOR_PLASTIC_WHITE)
__register_property('plastic_white', TEXT_PROPERTIES_CODE_PLASTIC_WHITE, __TEXT_PROPERTIES_PLASTIC_WHITE)


# Pink text
TEXT_PROPERTIES_CODE_PINK = "json_pink"
__TEXT_PROPERTIES_PINK = TextProperties()
__TEXT_PROPERTIES_PINK.setTextColor(*JSONPartFormatter.COLOR_PINK)
__register_property('pink', TEXT_PROPERTIES_CODE_PINK, __TEXT_PROPERTIES_PINK)


# Orange Gradient text
TEXT_PROPERTIES_CODE_ORANGE_GRADIENT = "json_orange_gradient"
__TEXT_PROPERTIES_ORANGE_GRADIENT = TextProperties()
__TEXT_PROPERTIES_ORANGE_GRADIENT.setTextColor(*JSONPartFormatter.COLOR_ORANGE_GRADIENT)
__register_property('orange_gradient', TEXT_PROPERTIES_CODE_ORANGE_GRADIENT, __TEXT_PROPERTIES_ORANGE_GRADIENT)


# Royal Blue Gradient text
TEXT_PROPERTIES_CODE_ROYAL_BLUE_GRADIENT = "json_royal_blue_gradient"
__TEXT_PROPERTIES_ROYAL_BLUE_GRADIENT = TextProperties()
__TEXT_PROPERTIES_ROYAL_BLUE_GRADIENT.setTextColor(*JSONPartFormatter.COLOR_ROYAL_BLUE_GRADIENT)
__register_property('royal_blue_gradient', TEXT_PROPERTIES_CODE_ROYAL_BLUE_GRADIENT, __TEXT_PROPERTIES_ROYAL_BLUE_GRADIENT)


# Deep Red Gradient text
TEXT_PROPERTIES_CODE_DEEP_RED_GRADIENT = "json_deep_red_gradient"
__TEXT_PROPERTIES_DEEP_RED_GRADIENT = TextProperties()
__TEXT_PROPERTIES_DEEP_RED_GRADIENT.setTextColor(*JSONPartFormatter.COLOR_DEEP_RED_GRADIENT)
__register_property('deep_red_gradient', TEXT_PROPERTIES_CODE_DEEP_RED_GRADIENT, __TEXT_PROPERTIES_DEEP_RED_GRADIENT)


# Purple Gradient text  
TEXT_PROPERTIES_CODE_PURPLE_GRADIENT = "json_purple_gradient"
__TEXT_PROPERTIES_PURPLE_GRADIENT = TextProperties()
__TEXT_PROPERTIES_PURPLE_GRADIENT.setTextColor(*JSONPartFormatter.COLOR_PURPLE_GRADIENT)
__register_property('purple_gradient', TEXT_PROPERTIES_CODE_PURPLE_GRADIENT, __TEXT_PROPERTIES_PURPLE_GRADIENT)


# Black Gradient text
TEXT_PROPERTIES_CODE_BLACK_GRADIENT = "json_black_gradient"
__TEXT_PROPERTIES_BLACK_GRADIENT = TextProperties()
__TEXT_PROPERTIES_BLACK_GRADIENT.setTextColor(*JSONPartFormatter.COLOR_BLACK_GRADIENT)
__register_property('black_gradient', TEXT_PROPERTIES_CODE_BLACK_GRADIENT, __TEXT_PROPERTIES_BLACK_GRADIENT)


# Bold text (ideally use a diff font but too much work rn so i am making bold actually italics)
TEXT_PROPERTIES_CODE_BOLD = "json_bold"
__TEXT_PROPERTIES_BOLD = TextProperties()
__TEXT_PROPERTIES_BOLD.setSlant(.30)
__register_property('bold', TEXT_PROPERTIES_CODE_BOLD, __TEXT_PROPERTIES_BOLD)


# Underline text
TEXT_PROPERTIES_CODE_UNDERLINE = "json_underline"
__TEXT_PROPERTIES_UNDERLINE = TextProperties()
__TEXT_PROPERTIES_UNDERLINE.setUnderscore(True)
__register_property('underline', TEXT_PROPERTIES_CODE_UNDERLINE, __TEXT_PROPERTIES_UNDERLINE)


# salmon text
TEXT_PROPERTIES_CODE_FISH_SUBTEXT = "json_fish_subtext"
__TEXT_PROPERTIES_FISH = TextProperties()
__TEXT_PROPERTIES_FISH.setSlant(0.25)
__TEXT_PROPERTIES_FISH.setTextScale(0.73)
__register_property('fishSubtext', TEXT_PROPERTIES_CODE_FISH_SUBTEXT, __TEXT_PROPERTIES_FISH)


# Called publically to get the TextProperties property code from a json color code
def get_property_code_from_json_code(json_color_code: str) -> str:
    return __JSON_COLOR_CODE_TO_TEXT_PROPERTY.get(json_color_code, TEXT_PROPERTIES_CODE_WHITE)


class MinimalJsonMessagePart(NamedTuple):
    message: str
    color: str = 'white'  # Use a json color code, 'red' 'blue' 'salmon' etc.


def interpolate_color(start_color: tuple, end_color: tuple, t: float) -> tuple:
    """Interpolate between two RGBA colors. t should be between 0.0 and 1.0"""
    return tuple(start_color[i] + (end_color[i] - start_color[i]) * t for i in range(4))


def create_gradient_text_parts(text: str, start_color: tuple, end_color: tuple) -> List[MinimalJsonMessagePart]:
    """
    Create a list of colored text parts that simulate a left-to-right gradient effect.
    This breaks the text into individual characters, each with a slightly different color.
    """
    if not text:
        return []
    
    parts = []
    char_count = len(text)
    
    for i, char in enumerate(text):
        # Calculate the gradient position (0.0 to 1.0)
        t = i / max(1, char_count - 1) if char_count > 1 else 0.0
        
        # Interpolate the color
        interpolated_color = interpolate_color(start_color, end_color, t)
        
        # Find the closest existing color or create a temporary color name
        color_name = f"gradient_{i}_{hash(interpolated_color) % 10000}"
        
        # Register this color if it doesn't exist
        if color_name not in __JSON_COLOR_CODE_TO_TEXT_PROPERTY:
            temp_props = TextProperties()
            temp_props.setTextColor(*interpolated_color)
            __register_property(color_name, f"temp_{color_name}", temp_props)
        
        parts.append(MinimalJsonMessagePart(message=char, color=color_name))
    
    return parts


def get_gradient_formatted_string(text: str, gradient_type: str) -> str:
    """
    Get a gradient-formatted string for the specified gradient type.
    """
    # Define gradient color mappings based on your specifications
    gradient_colors = {
        'orange_gradient': (
            (0.7, 0.2, 0.0, 1.0),    # Start: darker orange
            (1.0, 0.576, 0.0, 1.0)   # End: brighter orange
        ),
        'royal_blue_gradient': (
            (0.11, 0.203, 0.282, 1.0),  # Start: dark steel blue
            (0.274, 0.509, 0.705, 1.0)  # End: lighter steel blue
        ),
        'deep_red_gradient': (
            (0.405, 0.0, 0.0, 1.0),   # Start: darker red
            (0.945, 0.0, 0.0, 1.0)    # End: brighter red
        ),
        'purple_gradient': (
            (0.259, 0.174, 0.342, 1.0),  # Start: darker purple
            (0.603, 0.406, 0.798, 1.0)   # End: brighter purple
        ),
        'black_gradient': (
            (0.0, 0.0, 0.0, 1.0),      # Start: black
            (0.45, 0.45, 0.45, 1.0)    # End: medium gray
        ),
        'green_gradient': (
            (0.0, 0.5, 0.25, 1.0),     # Start: dark emerald green
            (0.2, 0.9, 0.4, 1.0)       # End: bright emerald green
        )
    }
    
    if gradient_type in gradient_colors:
        start_color, end_color = gradient_colors[gradient_type]
        gradient_parts = create_gradient_text_parts(text, start_color, end_color)
        return get_raw_formatted_string(gradient_parts)
    else:
        # Fallback to regular single color
        return get_raw_formatted_string([MinimalJsonMessagePart(message=text, color=gradient_type)])


# Use this is you want to use the JSONMessagePart system to create strings to display in game. This method will skip
# all the special formatting that AP messages need however, and will only utilize the 'text' and 'color' fields
# There is no error checking for this method so be wary of the color ur passing in

# Example usage:
# msg = get_raw_formatted_string([
#   MinimalJsonMessagePart(message='this is a '),
#   MinimalJsonMessagePart(message='colorful', color='red'),
#   MinimalJsonMessagePart(message='message ', color='blue'),
#   MinimalJsonMessagePart(message=' :)', color='green'),
# ])
def get_raw_formatted_string(parts: List[MinimalJsonMessagePart]) -> str:
    msg = ''
    for part in parts:
        msg += f"\1{get_property_code_from_json_code(part.color)}\1{part.message}\2"
    return msg
