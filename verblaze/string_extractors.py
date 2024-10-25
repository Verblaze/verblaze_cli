# string_extractors.py

import re
import string

class BaseStringExtractor:
    """
    Base class for string extractors. All extractor classes should inherit from this class
    and implement the extract_strings method.
    """
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_strings(self):
        raise NotImplementedError("This method should be implemented in the subclass.")

    def remove_emojis_and_punctuation(self, text):
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

# Extractor registry
EXTRACTOR_REGISTRY = {}

def register_extractor(template_name):
    """
    Decorator to register extractor classes in the EXTRACTOR_REGISTRY.
    """
    def decorator(cls):
        EXTRACTOR_REGISTRY[template_name.lower()] = cls
        return cls
    return decorator

@register_extractor("flutter")
class DartStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Dart (.dart) files in Flutter projects.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture single and double-quoted strings
        string_pattern = r"(?:'([^'\\]*(?:\\.[^'\\]*)*)'|\"([^\"\\]*(?:\\.[^\"\\]*)*)\")"
        matches = re.findall(string_pattern, code)
        strings = [s[0] if s[0] else s[1] for s in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "package:", "http:", "https:", "dart:", "mailto:", "tel:", "sms:", "print(",
            "debugPrint(", "log(", "assert(", "throw(", "Uri.parse(", "RegExp(",
            "../"
        ]

        strings = [
            s for s in strings
            if not any(s.strip().startswith(prefix) for prefix in prefixes_to_ignore)
        ]

        return strings

@register_extractor("react")
@register_extractor("react-native")
class ReactStringExtractor(BaseStringExtractor):
    """
    Extracts strings from JSX and TSX files in React and React Native projects.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Regex to capture strings in JSX text nodes and specific attributes
        jsx_string_pattern = re.compile(
            r"""
            # Capture strings within JSX tags (e.g., <div>Hello World</div>)
            (?:>([^<>{}]+)<)|
            # Capture strings within specific JSX attributes (e.g., alt="description")
            (?:(?:alt|title|placeholder|aria-label|label)=["']([^"']+)["'])
            """,
            re.VERBOSE
        )

        matches = re.findall(jsx_string_pattern, code)
        strings = []

        for match in matches:
            # match is a tuple with two elements; only one will be non-empty
            if match[0]:
                strings.append(match[0].strip())
            if match[1]:
                strings.append(match[1].strip())

        # Handle template literals with expressions (e.g., `Hello, ${user.name}!`)
        template_literal_pattern = re.compile(
            r"`([^`]*?)`"
        )
        template_matches = re.findall(template_literal_pattern, code)
        for tpl in template_matches:
            # Remove embedded expressions
            clean_tpl = re.sub(r"\${[^}]+}", "", tpl).strip()
            if clean_tpl:
                strings.append(clean_tpl)

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "export ", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)
    
@register_extractor("nextjs")
class NextJsStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Next.js (.js, .jsx, .ts, .tsx) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in JSX text nodes and specific attributes
        jsx_string_pattern = re.compile(
            r"""
            # Capture strings within JSX tags (e.g., <div>Hello World</div>)
            (?:>([^<>{}]+)<)|
            # Capture strings within specific JSX attributes (e.g., alt="description")
            (?:(?:alt|title|placeholder|aria-label|label)=["']([^"']+)["'])
            """,
            re.VERBOSE
        )

        matches = re.findall(jsx_string_pattern, code)
        strings = []

        for match in matches:
            if match[0]:
                strings.append(match[0].strip())
            if match[1]:
                strings.append(match[1].strip())

        # Handle template literals with expressions
        template_literal_pattern = re.compile(
            r"`([^`]*?)`"
        )
        template_matches = re.findall(template_literal_pattern, code)
        for tpl in template_matches:
            # Remove embedded expressions
            clean_tpl = re.sub(r"\${[^}]+}", "", tpl).strip()
            if clean_tpl:
                strings.append(clean_tpl)

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "export ", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("angular")
class AngularStringExtractor(BaseStringExtractor):
    """
    Extracts strings from TypeScript (.ts) and HTML files in Angular projects.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in single, double, or backtick quotes
        string_pattern = re.compile(
            r"""
            # Capture strings within single quotes
            '(?:\\.|[^'\\])*'|
            # Capture strings within double quotes
            "(?:\\.|[^"\\])*"|
            # Capture strings within backticks
            `(?:\\.|[^`\\])*`
            """,
            re.VERBOSE
        )
        matches = re.findall(string_pattern, code)
        strings = [match.strip("'\"`") for match in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "export ", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("plain-html")
class PlainHtmlStringExtractor(BaseStringExtractor):
    """
    Extracts text content from HTML files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture text within HTML tags
        string_pattern = re.compile(r'>([^<>]+)<')
        matches = re.findall(string_pattern, code)
        strings = [s.strip() for s in matches if s.strip()]

        # Additional filtering can be added if necessary
        return strings

@register_extractor("vue")
class VueStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Vue.js (.vue) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in single or double quotes within template and script sections
        vue_string_pattern = re.compile(
            r"""
            # Capture strings within Vue template text nodes (e.g., <div>Hello World</div>)
            (?:>([^<>{}]+)<)|
            # Capture strings within specific Vue attributes (e.g., alt="description")
            (?:(?:alt|title|placeholder|aria-label|label|tooltip)=["']([^"']+)["'])
            """,
            re.VERBOSE
        )

        matches = re.findall(vue_string_pattern, code)
        strings = []

        for match in matches:
            if match[0]:
                strings.append(match[0].strip())
            if match[1]:
                strings.append(match[1].strip())

        # Handle template literals with expressions
        template_literal_pattern = re.compile(
            r"`([^`]*?)`"
        )
        template_matches = re.findall(template_literal_pattern, code)
        for tpl in template_matches:
            # Remove embedded expressions
            clean_tpl = re.sub(r"\${[^}]+}", "", tpl).strip()
            if clean_tpl:
                strings.append(clean_tpl)

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "export ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("svelte")
class SvelteStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Svelte (.svelte) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in single, double, or backtick quotes within markup and script sections
        svelte_string_pattern = re.compile(
            r"""
            # Capture strings within Svelte markup text nodes (e.g., <div>Hello World</div>)
            (?:>([^<>{}]+)<)|
            # Capture strings within specific Svelte attributes (e.g., alt="description")
            (?:(?:alt|title|placeholder|aria-label|label)=["']([^"']+)["'])
            """,
            re.VERBOSE
        )

        matches = re.findall(svelte_string_pattern, code)
        strings = []

        for match in matches:
            if match[0]:
                strings.append(match[0].strip())
            if match[1]:
                strings.append(match[1].strip())

        # Handle template literals with expressions
        template_literal_pattern = re.compile(
            r"`([^`]*?)`"
        )
        template_matches = re.findall(template_literal_pattern, code)
        for tpl in template_matches:
            # Remove embedded expressions
            clean_tpl = re.sub(r"\${[^}]+}", "", tpl).strip()
            if clean_tpl:
                strings.append(clean_tpl)

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "export ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("swift")
class SwiftStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Swift (.swift) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in double quotes
        string_pattern = re.compile(r'(?<!\\)"(.*?)(?<!\\)"')
        matches = re.findall(string_pattern, code)
        strings = [s.strip() for s in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "func ", "let ", "var ", "//", "/*", "print(", "NSLog(", "http:", "https:", "mailto:", "tel:", "sms:"
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("kotlin")
class KotlinStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Kotlin (.kt) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in double quotes
        string_pattern = re.compile(r'(?<!\\)"(.*?)(?<!\\)"')
        matches = re.findall(string_pattern, code)
        strings = [s.strip() for s in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "fun ", "val ", "var ", "//", "/*", "print(", "println(", "http:", "https:", "mailto:", "tel:", "sms:"
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("ember")
class EmberStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Ember.js (.js, .hbs) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in single, double, or backtick quotes
        string_pattern = re.compile(
            r"""
            # Capture strings within single quotes
            '(?:\\.|[^'\\])*'|
            # Capture strings within double quotes
            "(?:\\.|[^"\\])*"|
            # Capture strings within backticks
            `(?:\\.|[^`\\])*`
            """,
            re.VERBOSE
        )
        matches = re.findall(string_pattern, code)
        strings = [match.strip("'\"`") for match in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "export ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("nextjs")
class NextJsStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Next.js (.js, .jsx, .ts, .tsx) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in JSX text nodes and specific attributes
        jsx_string_pattern = re.compile(
            r"""
            # Capture strings within JSX tags (e.g., <div>Hello World</div>)
            (?:>([^<>{}]+)<)|
            # Capture strings within specific JSX attributes (e.g., alt="description")
            (?:(?:alt|title|placeholder|aria-label|label)=["']([^"']+)["'])
            """,
            re.VERBOSE
        )

        matches = re.findall(jsx_string_pattern, code)
        strings = []

        for match in matches:
            if match[0]:
                strings.append(match[0].strip())
            if match[1]:
                strings.append(match[1].strip())

        # Handle template literals with expressions
        template_literal_pattern = re.compile(
            r"`([^`]*?)`"
        )
        template_matches = re.findall(template_literal_pattern, code)
        for tpl in template_matches:
            # Remove embedded expressions
            clean_tpl = re.sub(r"\${[^}]+}", "", tpl).strip()
            if clean_tpl:
                strings.append(clean_tpl)

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "export ", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)
    
@register_extractor("backbone")
class BackboneStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Backbone.js (.js) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in single, double, or backtick quotes
        string_pattern = re.compile(
            r"""
            # Capture strings within single quotes
            '(?:\\.|[^'\\])*'|
            # Capture strings within double quotes
            "(?:\\.|[^"\\])*"|
            # Capture strings within backticks
            `(?:\\.|[^`\\])*`
            """,
            re.VERBOSE
        )
        matches = re.findall(string_pattern, code)
        strings = [match.strip("'\"`") for match in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "export ", "require(", "console.log(", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "function", "const ", "let ", "var ", "{", "}", "return "
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("javafx")
class JavaFXStringExtractor(BaseStringExtractor):
    """
    Extracts strings from JavaFX (.java, .fxml) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in double quotes
        string_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
        matches = re.findall(string_pattern, code)
        strings = [s.strip() for s in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "public ", "private ", "protected ", "class ", "extends ", "implements ",
            "System.out.println(", "logger.", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "return ", "new ", "(", ")", "{", "}", ";", ","
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("wpf")
class WPFStringExtractor(BaseStringExtractor):
    """
    Extracts strings from WPF (.xaml) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings within attribute values in XAML
        string_pattern = re.compile(
            r"""
            # Capture strings within double quotes
            "([^"]+)"
            """,
            re.VERBOSE
        )
        matches = re.findall(string_pattern, code)
        strings = [s.strip() for s in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "xmlns:", "x:", "mc:", "d:", "toolkit:", "http:", "https:", "mailto:", "tel:", "sms:",
            "../", "./", "StaticResource", "DynamicResource", "Binding", "System.", "DisplayMemberPath"
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("qt")
class QtStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Qt (.qml) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in double quotes
        string_pattern = re.compile(r'"([^"\\]*(?:\\.[^"\\]*)*)"')
        matches = re.findall(string_pattern, code)
        strings = [s.strip() for s in matches]

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "import ", "QtQuick.", "QtQuick.Controls.", "Qt.", "width:", "height:", "id:", "anchors.",
            "http:", "https:", "mailto:", "tel:", "sms:", "../", "./", "return ", "new ", "function ", "var ",
            "{", "}", ";", ","
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            if not any(s.startswith(prefix) for prefix in prefixes_to_ignore) and len(s) > 0:
                unique_strings.add(s)

        return list(unique_strings)

@register_extractor("blazor")
class BlazorStringExtractor(BaseStringExtractor):
    """
    Extracts strings from Blazor (.razor) files.
    """
    def extract_strings(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Capture strings in double quotes and within @bind or other directives
        string_pattern = re.compile(
            r"""
            # Capture strings within double quotes
            "([^"\\]*(?:\\.[^"\\]*)*)"|
            # Capture strings within single quotes
            '([^'\\]*(?:\\.[^'\\]*)*)'|
            # Capture strings within @bind or other directives
            @bind="([^"]+)"
            """,
            re.VERBOSE
        )
        matches = re.findall(string_pattern, code)
        strings = [s[0] or s[1] or s[2] for s in matches if (s[0] or s[1] or s[2])]

        # Handle template literals with expressions if any (Blazor uses Razor syntax)
        # Not commonly used, but to be safe
        template_literal_pattern = re.compile(
            r"`([^`]*?)`"
        )
        template_matches = re.findall(template_literal_pattern, code)
        for tpl in template_matches:
            # Remove embedded expressions
            clean_tpl = re.sub(r"\${[^}]+}", "", tpl).strip()
            if clean_tpl:
                strings.append(clean_tpl)

        # Filter out unwanted strings
        prefixes_to_ignore = [
            "using ", "namespace ", "public ", "private ", "protected ", "class ", "void ", "return ",
            "http:", "https:", "mailto:", "tel:", "sms:", "../", "./", "var ", "let ", "const ", "{", "}", "@"  # To exclude directives and code snippets
        ]

        # Remove duplicates and filter
        unique_strings = set()
        for s in strings:
            s_clean = s.strip()
            if not any(s_clean.startswith(prefix) for prefix in prefixes_to_ignore) and len(s_clean) > 0:
                unique_strings.add(s_clean)

        return list(unique_strings)

# Additional extractor classes can be added here following the same pattern.

def get_string_extractor(template, file_path):
    """
    Retrieves the appropriate string extractor class for the given template.
    """
    extractor_class = EXTRACTOR_REGISTRY.get(template.lower())
    if extractor_class:
        return extractor_class(file_path)
    else:
        raise ValueError(f"Unsupported template type: {template}")