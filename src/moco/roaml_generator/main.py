#!/usr/bin/env python3

# Copyright (c) 2024 - for information on the respective copyright owner
# see the NOTICE file

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
from typing import Optional, Sequence

from moco.moco_common.logging import get_warn_msg
from moco.roaml_generator.scxml_helpers.top_level_interpreter import interpret_top_level_xml


def main_roaml_to_scxml(_args: Optional[Sequence[str]] = None) -> None:
    """
    Main function for the RoaML model (with ASCXML models) to SCXML conversion.

    Module containing the main entry points, pulling all necessary files together.
    BT.xml         \
    plugin.ascxml    \
    node1.ascxml      => main_roaml_to_scxml  =>  output folder
    node2.ascxml     /
    env.ascxml      /

    :param args: The arguments to parse. If None, sys.argv is used.
    :return: None
    """
    parser = argparse.ArgumentParser(
        description="Convert RoaML robot system models to plain SCXML."
    )
    parser.add_argument(
        "--out", "--o",
        type=str,
        default="./output",
        help="Path to the folder containing the generated plain-SCXML files.",
    )

    parser.add_argument("roaml_xml", type=str, help="The path to the main RoaML XML file to interpret.")
    args = parser.parse_args(_args)

    # Check the main xml file provided by the user
    main_xml_file = args.roaml_xml
    assert os.path.isfile(main_xml_file), f"File {main_xml_file} does not exist."
    assert main_xml_file.endswith(".xml"), f"File {main_xml_file} is not a '.xml' file."
    # Process additional, optional parameters
    scxml_out_dir = args.out
    scxml_out_dir = None if len(scxml_out_dir) == 0 else scxml_out_dir

    print("MOCO - RoAML to SCXML.\n")
    print(f"Loading model from {main_xml_file}.")

    interpret_top_level_xml(main_xml_file, scxmls_dir=scxml_out_dir)

    print(f"SCXML model saved to {scxml_out_dir}")


if __name__ == "__main__":
    # for testing purposes only
    import sys

    main_roaml_to_scxml(sys.argv[1:])
