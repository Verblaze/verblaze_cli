# string_extractors.py

import re
import string
from .pattern_utils import load_patterns

class BaseStringExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.patterns = load_patterns(self.__class__.__name__.replace('StringExtractor', '').lower())

    def extract_strings(self):
        raise NotImplementedError("This method should be implemented in the subclass.")

    def remove_emojis_and_punctuation(self, text):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "]+", flags=re.UNICODE
        )
        no_punctuation = text.translate(str.maketrans("", "", string.punctuation))
        no_emoji = emoji_pattern.sub(r'', no_punctuation)
        return no_emoji.strip()

    def filter_strings(self, strings):
        prefixes_to_ignore = self.patterns.get('prefixes_to_ignore', [])
        unique_strings = set()
        for s in strings:
            s = s.strip()
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)
        return list(unique_strings)

EXTRACTOR_REGISTRY = {}

def register_extractor(template_name):
    def decorator(cls):
        EXTRACTOR_REGISTRY[template_name.lower()] = cls
        return cls
    return decorator

@register_extractor("flutter")
class FlutterStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        for pattern in self.patterns.get('code_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            if matches:
                if isinstance(matches[0], tuple):
                    strings.extend([m[0] or m[1] for m in matches if m[0] or m[1]])
                else:
                    strings.extend(matches)

        return self.filter_strings(strings)

@register_extractor("react")
@register_extractor("react-native")
@register_extractor("nextjs")
class ReactStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        # JSX patterns
        for pattern in self.patterns.get('jsx_patterns', []):
            matches = re.findall(pattern['pattern'], code, re.VERBOSE)
            if matches:
                if isinstance(matches[0], tuple):
                    strings.extend([m[0] or m[1] for m in matches if m[0] or m[1]])
                else:
                    strings.extend(matches)

        # Template literals
        for pattern in self.patterns.get('template_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            for match in matches:
                clean_match = re.sub(r"\${[^}]+}", "", match).strip()
                if clean_match:
                    strings.append(clean_match)

        return self.filter_strings(strings)

@register_extractor("swift")
class SwiftStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        if self.file_path.endswith(('.storyboard', '.xib')):
            for pattern in self.patterns.get('ui_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                strings.extend(matches)
        else:
            for pattern in self.patterns.get('code_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                strings.extend(matches)

        return self.filter_strings(strings)

@register_extractor("kotlin")
class KotlinStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        if self.file_path.endswith('.xml'):
            for pattern in self.patterns.get('ui_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                strings.extend(matches)
        else:
            for pattern in self.patterns.get('code_patterns', []):
                matches = re.findall(pattern['pattern'], code)
                strings.extend(matches)

        return self.filter_strings(strings)

@register_extractor("blazor")
class BlazorStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        for pattern in self.patterns.get('code_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            if matches:
                if isinstance(matches[0], tuple):
                    strings.extend([m[0] or m[1] or m[2] for m in matches if m[0] or m[1] or m[2]])
                else:
                    strings.extend(matches)

        for pattern in self.patterns.get('template_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            for match in matches:
                clean_match = re.sub(r"\${[^}]+}", "", match).strip()
                if clean_match:
                    strings.append(clean_match)

        return self.filter_strings(strings)

@register_extractor("qt")
class QtStringExtractor(BaseStringExtractor):
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        strings = []
        
        for pattern in self.patterns.get('code_patterns', []):
            matches = re.findall(pattern['pattern'], code)
            strings.extend(matches)

        return self.filter_strings(strings)

def get_string_extractor(template, file_path):
    extractor_class = EXTRACTOR_REGISTRY.get(template.lower())
    if extractor_class:
        return extractor_class(file_path)
    else:
        raise ValueError(f"Unsupported template type: {template}")