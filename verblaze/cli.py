# cli.py

import os
import sys
import click
from termcolor import colored
from .file_utils import get_actual_path, list_all_files_in_directory
from .string_extractors import get_string_extractor
from .string_utils import format_as_json
from .display_utils import print_ascii_art, loading_animation

SUPPORTED_TEMPLATES = [
    "flutter", "react", "react-native", "angular", "plain-html",
    "vue", "svelte", "ember", "backbone", "swift", "kotlin",
    "javafx", "wpf", "qt", "blazor"
]

@click.command()
@click.option(
    "-t",
    type=click.Choice(SUPPORTED_TEMPLATES, case_sensitive=False),
    required=True,
    help="Enter the technology/framework used in the project."
)
@click.option(
    "-d",
    type=str,
    required=True,
    help="Directory of the project. Example: -d '/path/to/project'"
)
@click.option(
    "-f",
    type=str,
    required=True,
    help="Folders containing UI code. Example: -f 'src, app, screens, components'"
)
def main(t, d, f):
    """
    Verblaze: Auto-Localization Generation Tool
    """
    loading_animation()
    print_ascii_art()

    selected_template = t.lower()
    project_dir = d.rstrip('/') + '/'
    folders = [folder.strip() for folder in f.split(",")]
    actual_path = get_actual_path(selected_template)
    search_path = os.path.join(project_dir, actual_path)
    file_list = list_all_files_in_directory(search_path, selected_template, folders)
    file_path_and_strings = []

    for file_path in file_list:
        extractor = get_string_extractor(selected_template, file_path)
        strings = extractor.extract_strings()
        if strings:
            file_path_and_strings.append((file_path, strings))

    if not file_path_and_strings:
        print(colored("No strings found to extract.", "yellow"))
        sys.exit()

    current_path = os.getcwd()
    output_file = os.path.join(current_path, "output.json")
    with open(output_file, "w", encoding='utf-8') as file:
        formatted_data = format_as_json(file_path_and_strings)
        file.write(formatted_data)
        print(colored(f"\n\n{output_file} file is created successfully!", "green"))

if __name__ == "__main__":
    main()