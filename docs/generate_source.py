# Copyright (C) Unitary Fund
#
# This source code is licensed under the GPL license (v3) found in the
# LICENSE file in the root directory of this source tree.

"""
Copied modified files from the 'source' directory to the '_source' directory
and generates .ipynb files for myst notebooks
"""
import os
import shutil


class ConversionError(Exception):
    """Exception raised if jupytext has error when converting file"""

    pass


def files_have_different_contents(first_file, second_file):
    """Compare the contents of two files.

    Args:
        first_file (str): Path to the first file.
        second_file (str): Path to the second file.

    Returns:
        bool: True if the contents are different, False otherwise.
    """
    with open(first_file, "rb") as source:
        with open(second_file, "rb") as target:
            return source.read() != target.read()


source_directory = "source"
target_directory = "_source"

# Get the current working directory
current_directory = os.getcwd()

# Construct the source and target directory paths
source_path = os.path.join(current_directory, source_directory)
target_path = os.path.join(current_directory, target_directory)


def main():
    """Copied modified files from the 'source' directory to the '_source' directory
    and generates .ipynb files for myst notebooks
    """

    # Create the target directory if it doesn't exist
    if not os.path.exists(target_path):
        os.makedirs(target_path)

    # Recursively iterate over all files and directories in the source directory
    for root, dirs, files in os.walk(source_path):
        # Get the corresponding subdirectory in the target directory
        relative_path = os.path.relpath(root, source_path)
        target_subdirectory = os.path.join(target_path, relative_path)

        # Create the subdirectory in the target directory if it doesn't exist
        if not os.path.exists(target_subdirectory):
            os.makedirs(target_subdirectory)

        # Copy each file from source to target if the contents has changed
        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_subdirectory, file)

            if not os.path.exists(target_file) or files_have_different_contents(
                    source_file, target_file
            ):
                shutil.copy2(source_file, target_file)
                print(f"Copied: {source_file} -> {target_file}")

                # Convert notebooks to ipynb
                if file.endswith(".md"):
                    with open(target_file, "r") as f:
                        file_contents = f.read()
                        if "---\njupytext:" in file_contents:
                            exit_code = os.system(
                                f"jupytext --from myst --to ipynb {target_file}"
                            )
                            if exit_code != 0:
                                raise ConversionError(
                                    f"Error converting notebook: {target_file}"
                                )


if __name__ == "__main__":
    main()
