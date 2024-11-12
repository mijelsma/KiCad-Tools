import os
import argparse
import shutil
from pathlib import Path

# Define the root directory based on the current script location
ROOT_DIR = Path(__file__).parent

def create_folder(path: Path) -> None:
    """Creates a folder if it does not exist."""
    if not path.exists():
        path.mkdir(parents=True)
        print(f'Created folder "{path.name}"')
    else:
        print(f'Folder "{path.name}" already exists')

def write_file(path: Path, contents: str) -> None:
    """Writes contents to a file, creating it if it does not exist."""
    with path.open('w') as file:
        file.write(contents)
    print(f'Created file "{path.name}"')

def copy_template(template_path: Path, destination_path: Path) -> None:
    """Copies the template project to the destination path."""
    print('Copying the template project...')
    try:
        shutil.copytree(template_path, destination_path)
        print(f'Template project copied to "{destination_path}"')
    except OSError as err:
        print(f'Error copying template project: {err}')

def rename_template_files(destination_folder: Path, project_name: str) -> None:
    """Renames template files in the destination folder to the project name."""
    print('Renaming project files...')
    for file in destination_folder.iterdir():
        if file.stem == 'TEMPLATE_PROJECT':
            new_file = file.with_stem(project_name)
            print(f'Renaming file {file} --> {new_file}')
            file.rename(new_file)

def main() -> None:
    """Main function to handle project setup."""
    parser = argparse.ArgumentParser(description='Set up a new project from a template.')
    parser.add_argument('--name', required=True, help='Project name')
    args = parser.parse_args()
    project_name = args.name

    # Define paths
    template_folder = ROOT_DIR / 'TEMPLATE_PROJECT' / 'PROJECT'
    project_folder = ROOT_DIR / project_name
    destination_folder = project_folder / project_name
    git_ignore_file = ROOT_DIR / 'TEMPLATE_PROJECT' / '.gitignore'

    # Create the project folder
    create_folder(project_folder)

    # Copy the template project and gitignore file
    copy_template(template_folder, destination_folder)

    # Copy .gitignore to the project folder
    if git_ignore_file.exists():
        shutil.copy(git_ignore_file, project_folder / '.gitignore')
        print('Copied .gitignore file')
    else:
        print(f'.gitignore file not found at {git_ignore_file}')

    # Rename template files in the destination folder
    rename_template_files(destination_folder, project_name)

    # Create the README file
    readme_path = project_folder / 'README.md'
    write_file(readme_path, f'# {project_name}')

    print('Project setup complete!')

if __name__ == '__main__':
    main()
