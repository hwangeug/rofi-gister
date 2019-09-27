#!/usr/bin/env python3

import os
import sys
import json
import csv
import io
import re
from typing import Dict, Tuple, List
from subprocess import run, PIPE


GISTER_PATH = os.path.join(os.environ['HOME'], 'GitHub', 'gister', 'gister.sh')
GISTS_ROOT = os.path.join(os.environ['HOME'], '.gists')
GISTS_DESC_FILE = os.path.join(GISTS_ROOT, 'gists.list')
GISTS_TREE = os.path.join(GISTS_ROOT, 'tree')


# Read gists.list file
def process_gists(gists_def: Dict) -> Tuple:
    descs = [list(g['files'].keys())[0] + ': ' + g['description'] for g in gists_def]
    locs = [os.path.join(GISTS_TREE, g['id'], list(g['files'].keys())[0]) for g in gists_def]
    
    return(descs, locs)


# Create output for rofi dmenu
def serialize_gist_descs(gist_descs: List) -> str:
    with io.StringIO() as o:
        for desc in gist_descs:
            o.write(desc + '\n')
        options = o.getvalue()

    return(options)


# Spawn selector menu
def rofi_gist_selector(gist_descs: List, gist_locs: List, 
                       master_gist_descs: List, master_gist_locs: List) -> Tuple:
    options_serialized = serialize_gist_descs(gist_descs)

    # Open rofi window and get selection
    rofi_proc = run(['rofi', '-dmenu', '-p', 'Gist', '-mesg', '<b>Alt+r</b>: sync | <b>Alt+s</b>: code search',
                     '-i', #'-no-custom',
                     '-format', 'i:s',
                     '-kb-custom-1', 'alt+r',
                     '-kb-custom-2', 'alt+s'],
                    stdout=PIPE, input=options_serialized, text=True)
    rofi_output = rofi_proc.stdout

    # Get index and selected text from selection
    match = re.match(r"^(\-?[0-9]+):(.*)", rofi_output)
    if match:
        selected_index = int(match.group(1))
        search_text = match.group(2)
    else:
        sys.exit(1)

    # User selected an item, copy item to clipboard
    if rofi_proc.returncode == 0 and selected_index >= 0:
        selected_location = gist_locs[selected_index]
        run(['xclip', '-selection', 'clipboard', selected_location])
    # User requested sync, run gister.sh sync
    elif rofi_proc.returncode == 10:
        run([GISTER_PATH, 'sync'])
    # User requested search, run gister.sh search and filter files list
    elif rofi_proc.returncode == 11:
        gister_proc = run([GISTER_PATH, 'search', search_text], stdout=PIPE, stderr=None, text=True)
        results_lines = gister_proc.stdout.split('\n')

        files = set()
        for line in results_lines:
            m = re.match(r"^([^:]*):", line)
            if m:
                file = m.group(1)
                files.add(file)

        # Spawn a new rofi menu with only the matching files
        descs_filtered = [desc for (desc, loc) in zip(master_gist_descs, master_gist_locs) if loc in files]
        locs_filtered = [loc for loc in master_gist_locs if loc in files]
        
        return(descs_filtered, locs_filtered)
    
    return(None, None)


def main() -> None:
    # Read gister file and extract gist descriptions / locations
    with open(GISTS_DESC_FILE, 'r') as f:
        gists_def = json.load(f)
    
    gist_descs, gist_locs = process_gists(gists_def)
    master_gist_descs = gist_descs
    master_gist_locs = gist_locs

    gist_descs_filtered, gist_locs_filtered = rofi_gist_selector(gist_descs, gist_locs, master_gist_descs, master_gist_locs)
    while gist_descs_filtered is not None:
        gist_descs_filtered, gist_locs_filtered = rofi_gist_selector(gist_descs_filtered, gist_locs_filtered,
                                                                     master_gist_descs, master_gist_locs)
    
        

if __name__=="__main__":
    main()
