import asyncio
import json
import os
import sys
import click
from termcolor import colored

from .api import API
from .display_utils import loading_animation, print_ascii_art
from .file_utils import get_actual_path, list_all_files_in_directory
from .string_extractor_utils import get_string_extractor
from .string_utils import format_as_json


SUPPORTED_TEMPLATES = [
    "flutter", "react", "react-native", "angular", "plain-html",
    "vue", "svelte", "ember", "backbone", "swift", "kotlin",
    "javafx", "wpf", "qt", "blazor", "nextjs"
]

async def handle_config(secret_key):
    if not secret_key:
        print(colored("Secret key is required to set the configuration.", "yellow"))
        sys.exit()

    secretKeyIsValid = await API.checkCLISecret(secret_key)
    if not secretKeyIsValid:
        print(colored("Secret key is invalid. Please enter a valid secret key.", "red"))
        sys.exit()

    config_path = os.path.join(os.getcwd(), ".env")
    
    with open(config_path, "w") as config_file:
        config_file.write(f"SECRET_KEY={secret_key}\n")
        print(colored(f"Configuration completed successfully!", "green"))
        
async def send_translations(secret_key, translations):
    if not secret_key:
        print(colored("CLI Secret Token is required to set the configuration. \n\n You can use 'verblaze config --secret-key'", "yellow"))
        sys.exit()

    secretKeyIsValid = await API.checkCLISecret(secret_key)
    if not secretKeyIsValid:
        print(colored("CLI Secret Token is invalid. Please enter a valid secret key.", "red"))
        sys.exit()

    response = await API.initLanguage(secret_key, translations)
    if response == False:
        print(colored("Strings could not be synchronized in the verblaze panel.", "red"))
        sys.exit()

@click.group()
def main():
    """Verblaze: Auto-Localization Generation Tool"""
    pass

# generate komutu
@main.command()
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
def generate(t, d, f):
    """
    Generate localization files for the given project.
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
        
    formatted_data = format_as_json(file_path_and_strings)
    secret_key = open(".env", "r").read().split("\n")[0].split("=")[1]
    asyncio.run(send_translations(secret_key, json.loads(formatted_data)))
    print(colored(f"\n\nStrings are syncronized in Verblaze dashboard", "green"))


# config komutu (tek seferde tanımlandı)
@main.command()
@click.option(
    "--secret-key",
    type=str,
    required=True,
    help="Set the secret key for Verblaze configuration."
)
def config(secret_key):
    """
    Set configuration values for Verblaze.
    """
    # asyncio ile async fonksiyonunu çalıştırıyoruz
    asyncio.run(handle_config(secret_key))


if __name__ == "__main__":
    main()