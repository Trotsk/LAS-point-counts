#!/usr/bin/env python3

"""Computes point counts for all size datasets.

Resolves issue with LASinfo's -merge command which is restricted
by memory constraints and has no in-built error handling
(it will spit out a result and then terminate).

Requires pip install tqdm
Requires LAStools downloaded into default data structure (C:\LAStools\bin)
"""

import re
from glob import glob
import subprocess
import os
from tqdm import tqdm


dir = input('What is the full path of your LAS files? \n > ')
try:
    os.chdir(dir)
except:
    raise ValueError('Invalid directory')


exp_cl = input('Expected classes? \n > ')
classes = list(map(str, exp_cl.split()))
print("\n")


def log(i):
    """Intakes file name, appends to text file"""
    with open('CLASS_ERRORS.txt', 'a') as log_file:
        log_file.write(i + '\n')


def extract_classes(text):
    """Intakes text string, returns point classifications as key-value pair"""
    raw_text = text.partition("histogram of classification of points:")
    text = raw_text[2]
    clean_lines = [l.lstrip() for l in text.splitlines()]
    parse_lines = [l for l in clean_lines if re.match(r"^\d+.*$", l)]
    return {key: int(val) for val, key in (parse_lines.split(" ", 1)
            for parse_lines in parse_lines)}


def main():
    """ Invokes lasinfo, parses output for each LAS file,
    creates dictionary and updates point counts for each successive loop """
    filename = glob("*.las")  # search for LAS files in directory
    pbar = tqdm(total=len(filename), unit="file")  # instantiate progress bar
    dict = {}  # instantiate master dictionary
    for i in filename:
        # redirects to stdout as tqdm uses stderr
        proc = subprocess.Popen(['lasinfo', i, '-no_vlrs', '-stdout'],
                                stdout=subprocess.PIPE)
        f = extract_classes(proc.communicate()[0].decode('utf-8').strip())
        for key, val in f.items():
            if key in dict.keys():
                dict[key] += val  # if key already in dict, values updated
            else:
                dict[key] = val  # new key has key-value pair added to dict
        for item in f.keys():
            if not any(x in item for x in classes):
                log(i + item)  # write file out if it holds an unexpected class
        pbar.update(1)  # increment progress bar
    pbar.close()  # close progress bar
    print("\n histogram of classification of points: \n")
    for key, val in dict.items():
        print(key.rjust(25), "\t", val)


if __name__ == "__main__":
    main()
