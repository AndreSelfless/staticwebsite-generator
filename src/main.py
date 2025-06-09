import os
import sys
from textnode import *
from htmlnode import *
from codes import *
from markdown_blocks import *
from fileManager import *


def main():

    args = sys.argv    
    if len(args) >= 2:
        basepath = args[1]
        print(f"Setting {args[1]} as the base path")
        if len(args) > 2:
            print("As more than one path was set, please make sure the correct one is beaing loaded!")
    elif len(args) == 1:
        basepath = "/"


    src_path = "static"
    dst_path = "docs"
    content = "content"
    template = "template.html"
    

    log1 = clear_directory(dst_path)
    print("\n".join(log1))


    log2 = copy_files(src_path, dst_path)
    print("\n".join(log2))

    generate_pages_recursive(
        dir_path_content=content,
        template_path=template,
        dest_dir_path=dst_path, 
        basepath=basepath
        )
    print("Page generated!")


if __name__ == "__main__":
    main()