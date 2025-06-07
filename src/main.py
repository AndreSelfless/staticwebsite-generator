import os
from textnode import *
from htmlnode import *
from codes import *
from markdown_blocks import *
from fileManager import *


def main():

    src_path = "static"
    dst_path = "public"
    content = "content"
    template = "template.html"
    

    log1 = clear_directory(dst_path)
    print("\n".join(log1))


    log2 = copy_files(src_path, dst_path)
    print("\n".join(log2))

    generate_pages_recursive(
        dir_path_content=content,
        template_path=template,
        dest_dir_path=dst_path
    )
    print("Page generated!")


if __name__ == "__main__":
    main()