import argparse
import os
import re

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
                    print(file_path)
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
    
    # 'package:' ile başlayan stringleri listeden kaldır
    strings = [s for s in strings if not s.startswith("package:") and not s.startswith("http:") and not s.startswith("https:") and not s.startswith("dart:") and not s.startswith("mailto:") and not s.startswith("tel:") and not s.startswith("sms:") and not s.startswith("print(") and not s.startswith("debugPrint(")]    
    
    return strings    


def main():
    parser = argparse.ArgumentParser("Auto-Localization Generation Tool")
    parser.add_argument("-t", type=str, help="Enter the technology in which you developed your project: flutter, react-native, react, angular, plain-html")
    parser.add_argument("-d", type=str, help="Directory of project. Example: -d '/Users/username/Projects/MyProject'")
    parser.add_argument("-f", type=str, help="Folders containing UI codes. Example: -f 'screens, components, widgets'")
    args = parser.parse_args()
    selected_template = args.t
    project_dir = args.d
    folders = args.f.split(", ")
    actual_path = get_actual_path(selected_template)# Actual path of the project such as /lib for flutter, /src for react, /src/app for angular, /src for react-native, / for plain-html
    file_list = list_all_files_in_directory("{}{}".format(project_dir, actual_path), selected_template, folders)    
    file_path_and_strings = []
    for file_path in file_list:
        strings = extract_strings_from_dart_file(file_path)
        file_path_and_strings.append((file_path, strings))
    # print file_path_and_strings to output.txt
    
    with open("output.txt", "w") as file:
        for file_path, strings in file_path_and_strings:
            file.write(f"{file_path}\n")
            for string in strings:
                file.write(f"{string}\n")
            file.write("\n")        

if __name__ == "__main__":
    main()