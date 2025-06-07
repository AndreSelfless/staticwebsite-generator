import os
import shutil
from pathlib import Path
from markdown_blocks import markdown_to_html_node, extract_title

def clear_directory(path):
    log = []
    if os.path.exists(path) and len(os.listdir(path)) != 0:
        directory_files = os.listdir(path)
        for element in directory_files:
            full_path = os.path.join(path, element) 
            if os.path.isfile(full_path):
                os.remove(full_path)
                log.append(f"Removed file: {full_path}")
            elif os.path.isdir(full_path):
                sub_log = clear_directory(full_path)
                log.extend(sub_log)
                os.rmdir(full_path)
                log.append(f"Removed directory: {full_path}")
    return log
     
def copy_files(from_path, to_path):
    log = []

    if os.path.exists(from_path) and os.path.exists(to_path):

        for element in os.listdir(from_path):
            full_from_path = os.path.join(from_path, element)
            full_to_path = os.path.join(to_path, element)

            if os.path.isfile(full_from_path):
                shutil.copy(full_from_path, full_to_path)
                log.append(f"> Now copying {element}, from {full_from_path} to {full_to_path}")

            elif os.path.isdir(full_from_path):
                os.makedirs(full_to_path, exist_ok=True)
                log.append(f"> Created directory: {full_to_path}")
                log.extend(copy_files(full_from_path, full_to_path))

        return log

    else:
        raise Exception("The file paths provided are incorrect.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as contents:
        markdown_file = contents.read()
        html_string = markdown_to_html_node(markdown_file).to_html()
        title = extract_title(markdown_file)

    with open(template_path) as contents:
        template_file = contents.read()
        final_file = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(final_file)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    content_root = Path(dir_path_content)
    dest_root = Path(dest_dir_path)

    for entry in content_root.iterdir():
        
        if entry.is_file() and entry.suffix == ".md":
        
            relative_path = entry.relative_to(content_root)
            dest_file = dest_root / relative_path.with_suffix(".html")
            generate_page(entry, template_path, dest_file)
        
        elif entry.is_dir():

            generate_pages_recursive(entry, template_path, dest_root / entry.name)