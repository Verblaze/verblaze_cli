# string_utils.py

import re
import json
import os
import string
from unidecode import unidecode

def remove_emojis_and_punctuation(text):
    """
    Removes emojis and punctuation from the given text.
    """
    # Define the Unicode range for emojis
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
        "\U0001F680-\U0001F6FF"  # Transport & Map Symbols
        "\U0001F1E0-\U0001F1FF"  # Flags
        "]+", flags=re.UNICODE
    )

    # Remove punctuation
    no_punctuation = text.translate(str.maketrans("", "", string.punctuation))

    # Remove emojis
    no_emoji = emoji_pattern.sub(r'', no_punctuation)

    return no_emoji.strip()

def format_as_json(file_path_and_strings: list) -> str:
    """
    Formats the extracted strings into a JSON structure.
    """
    data = []
    for file_path, strings in file_path_and_strings:
        basename = os.path.basename(file_path)
        # First characters should be uppercase, e.g., "Settings Screen"
        file_title = (basename.split(".")[0].replace("_", " ")).title()
        file_key = unidecode(file_title).replace(" ", "_").lower()
        # file_key has contains english characters only
        
        # Generate a key for every string value and create "values" dict
        values = {}
        for string in strings:
            key = ""
            cleaned_text = remove_emojis_and_punctuation(string)
            words = cleaned_text.split()
            # If string has more than 3 words, key will be first, middle, and last word
            if len(words) >= 3:
                middle_word = words[len(words) // 2]
                key = (words[0] + "_" + middle_word + "_" + words[-1]).lower()
            elif len(words) == 2:
                key = (words[0] + "_" + words[1]).lower()
            else:
                key = cleaned_text.lower()
            key = key.replace(" ", "_")
            values[key] = string
        if values:
            data.append({"file_title": file_title, "file_key" : file_key, "values": values})
    return json.dumps(data, ensure_ascii=False, indent=2)