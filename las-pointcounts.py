import re
from glob import glob
import subprocess
import time
from pprint import pprint

# I know global variables are unpythonic, I'll fix it later
g_partition = "histogram of classification of points:"

def extract_classes(text):
  """ Intakes text string, returns point classifications as key-value pair """
  raw_text = text.partition(g_partition)
  text = raw_text[2]
  clean_lines = [l.lstrip() for l in text.splitlines()]
  parse_lines = [l for l in clean_lines if re.match(r"^\d+.*$",l)]
  return {key: int(val) for val, key in (parse_lines.split(" ",1) for parse_lines in parse_lines)}


def main():
  """ Invokes lasinfo, parses output for each LAS file, creates dictionary and updates 
  point counts for each successive loop """
  start_time = time.time()
  filename = glob("*.las") # searches all LAS files in directory
  dict = {} # instantiate master dictionary
  for i in filename:
    # By default all output of lasinfo goes to stderr. A command argument redirects to stdout
    proc = subprocess.Popen(['lasinfo', i, '-no_vlrs', '-stdout'], stdout = subprocess.PIPE)
    out = proc.communicate()[0].decode('utf-8').strip()
    f = extract_classes(out)
    for key, val in f.items():
      if key in dict.keys():
        dict[key] += val # if key already in dict, values updated
      else:
        dict[key] = val # key-value pair added to dict if key does not yet exist
  elapsed_time = time.time() - start_time
  print("\n")
  print(g_partition)
  print("\n")
  pprint(dict)
  print("\n")
  print(time.strftime("Time elapsed: %H:%M:%S", time.gmtime(elapsed_time)))
  
if __name__ == "__main__":
  main()