import os
import re
import json
import string
import sys
import time

import click
from termcolor import colored
# Get actual path of the project   
def get_actual_path(template:str):
    if template == "flutter":
        return "lib"
    elif template == "react":
        return "src"
    elif template == "react-native":
        return "src"
    elif template == "angular":
        return "src/app"
    elif template == "plain-html":
        return ""

def get_file_extension_from_template(template:str):
    if template == "flutter":
        return "dart"
    elif template == "react":
        return "jsx", "tsx"
    elif template == "react-native":
        return "jsx", "tsx" 
    elif template == "angular":
        return "ts"
    elif template == "plain-html":
        return "html"
    
# List directories and files in given directory according to the template
def list_all_files_in_directory(dir: str, template: str, folders: list):
    valid_file_extension = get_file_extension_from_template(template)
    all_files = []
    
    for root, dirs, files in os.walk(dir):
        # Şu anki klasör ismini alıyoruz
        current_folder = os.path.basename(root)
        
        # Eğer current_folder folders listesindeyse, dosyaları kontrol et
        if current_folder in folders:
            for file in files:
                # Dosya uzantısını kontrol et
                if file.endswith(f".{valid_file_extension}"):
                    # Tam dosya yolunu ekliyoruz
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
    
    return all_files

# Dart dosyasından stringleri çıkart
def extract_strings_from_dart_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()
    
    # Düzenli ifade deseni: Tek ve çift tırnaklı stringleri yakalar
    string_pattern = r"(?:'([^'\\]*(?:\\.[^'\\]*)*)'|\"([^\"\\]*(?:\\.[^\"\\]*)*)\")"
    
    # Tüm eşleşmeleri bul
    matches = re.findall(string_pattern, code)
    
    # Elde edilen tuple'lardan stringleri al
    strings = [s[0] if s[0] else s[1] for s in matches]
    
    # Önemli Stringleri almak için aşağıdaki stringleri temizle
    strings = [s for s in strings if not s.startswith("package:") and not s.startswith("http:") and not s.startswith("https:") and not s.startswith("dart:") 
               and not s.startswith("mailto:") and not s.startswith("tel:") and not s.startswith("sms:") and not s.startswith("print(") and not s.startswith("debugPrint(") 
               and not s.startswith("log(") and not s.startswith("assert(") and not s.startswith("throw(") and not s.startswith("Uri.parse(") and not s.startswith("RegExp(")
               and not s.startswith("RegExp.escape(") and not s.startswith("RegExp.quote(") and not s.startswith("RegExp.unescape(") and not s.startswith("RegExp.compile(")
               and not s.startswith("RegExp.hasMatch(") and not s.startswith("RegExp.firstMatch(") and not s.startswith("RegExp.allMatches(") and not s.startswith("RegExp.stringMatch(")
               and not s.startswith("RegExp.replaceAll(") and not s.startswith("RegExp.replaceFirst(") and not s.startswith("RegExp.split(") and not s.startswith("RegExp.matchAsPrefix(")
               and not s.startswith("RegExp.matchAsPrefix(") and not s.startswith("RegExp.matchAsPrefix(") and not s.startswith("RegExp.matchAsPrefix(") and not s.startswith("RegExp.matchAsPrefix(")
               and not s.startswith("../") and not s.startswith("RegExp.matchAsPrefix(") and not s.startswith("RegExp.matchAsPrefix(") and not s.startswith("RegExp.matchAsPrefix(")]    
    
    return strings    

def remove_emojis_and_punctuation(text):
    # Emojileri kaldırmak için Unicode aralığını tanımla
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # Yüz emojileri
        "\U0001F300-\U0001F5FF"  # Simgeler ve objeler
        "\U0001F680-\U0001F6FF"  # Taşıtlar ve simgeler
        "\U0001F1E0-\U0001F1FF"  # Bayraklar
        "]+", flags=re.UNICODE)

    # Noktalama işaretlerini kaldırmak için string.punctuation'ı kullan
    no_punctuation = text.translate(str.maketrans("", "", string.punctuation))
    
    # Emojileri kaldır
    no_emoji = emoji_pattern.sub(r'', no_punctuation)
    
    return no_emoji.strip()

def format_as_json(file_path_and_strings : list) -> str:
    
    data = []
    for file_path, strings in file_path_and_strings:
        basename = os.path.basename(file_path)
        # First characters should be upper Ex: Settings Screen
        file_title =  (basename.split(".")[0].replace("_", " ")).title()
        # Generate a key for every string value and create "values" dict
        values = {}
        for string in strings:
            key = ""
            cleaned_text = remove_emojis_and_punctuation(string)
            words = cleaned_text.split(" ")
            # If string has more than 3 words, key will be first two words and last word
            if len(words) >= 3:
                middle_word = words[len(words) // 2]
                key = (words[0] + "_" + middle_word + "_" + words[-1]).lower()
                values[key] = string
            elif len(words) == 2:
                key = (words[0] + "_" + words[1]).lower()
                values[key] = string
            else: 
                key = string.lower()
                values[key] = string
        if values:
            data.append({"file_title" : file_title, "values": values})
    return json.dumps(data)

def colored_custom(text, r, g, b):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def print_ascii_art(): 
    ascii_art = [
    "                    _      _                        ___   __   _____ ",
    " /\   /\ ___  _ __ | |__  | |  __ _  ____ ___      / __\\ / /   \\_   \\",
    " \\ \\ / // _ \\| '__|| '_ \\ | | / _` ||_  // _ \\    / /   / /     / /\\/ ",
    "  \\ V /|  __/| |   | |_) || || (_| | / /|  __/   / /___/ /___/\\/ /_  ",
    "   \\_/  \\___||_|   |_.__/ |_| \\__,_|/___|\\___|   \\____/\\____/\\____/  ",
    "                                                                     "
    ]

    for line in ascii_art:
        print(colored_custom(line, 79, 70, 229))        

def loading_animation():
    timer = 0
    loading = "Output.json Generating: [----------]"
    backtrack = '\b'*len(loading)

    while timer < 11:
        sys.stdout.write(backtrack + loading)
        sys.stdout.flush()
        loading = loading.replace("-","=",1)
        time.sleep(0.5)
        timer += 1
        time.sleep(0.5)
        sys.stdout.write(backtrack)


@click.command()
@click.option("-t", type=str, help="Enter the technology in which you developed your project: flutter, react-native, react, angular, plain-html \n")
@click.option("-d", type=str, help="Directory of project. Example: -d '/Users/username/Projects/MyProject'\n")
@click.option("-f", type=str, help="Folders containing UI codes. Example: -f 'src, app, screens, view, views, components, widgets, widget' \n")
def main(t, d, f):
    loading_animation()
    print_ascii_art()
    """ Verblaze: Auto-Localization Generation Tool """
    selected_template = t
    project_dir = d
    if not project_dir.endswith("/"):
        project_dir += "/"
    folders = f.split(", ")
    actual_path = get_actual_path(selected_template)# Actual path of the project such as /lib for flutter, /src for react, /src/app for angular, /src for react-native, / for plain-html
    file_list = list_all_files_in_directory("{}{}".format(project_dir, actual_path), selected_template, folders)  
    file_path_and_strings = []
    for file_path in file_list:
        strings = extract_strings_from_dart_file(file_path)
        file_path_and_strings.append((file_path, strings))
    # print file_path_and_strings to output.txt
    current_path = os.getcwd()
    with open(current_path + "/output.json", "w") as file:
        formatted_data : dict = format_as_json(file_path_and_strings)
        file.write(formatted_data)
        print(colored("\n\n {}/output.json file is created successfully!".format(current_path), "green"))
        
if __name__ == "__main__":
    main()