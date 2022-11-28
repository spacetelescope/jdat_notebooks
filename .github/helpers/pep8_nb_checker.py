import argparse
import copy
import json
import numpy as np
import pathlib
import pytz
import re
import subprocess
import sys

from collections import defaultdict
from datetime import datetime as dt

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', type=str,
                    help='The notebook file to be checked')
args = parser.parse_args()

nb_ext = '.ipynb'

try:
    nb_file = pathlib.Path(args.file)
    if not nb_file.suffix == nb_ext:
        raise ValueError(f"file extension must be {nb_ext}")

except Exception as err:
    parser.print_help()
    raise err

# create a separating line for the script file with unique text, like:
# #################################flake-8-check################################
# (plus a closing newline to avoid W391 at end of file)
identifier = 'flake-8-check'
line_length = 80
fill_0 = (line_length // 2 - 1) - np.floor(len(identifier) / 2).astype(int)
fill_1 = (line_length // 2 - 1) - np.ceil(len(identifier) / 2).astype(int)

separator = '# ' + '#' * fill_0 + identifier + '#' * fill_1 + '\n'
buffer_lines = 3  # sections must end with >2 blank lines to avoid E302

# save relevant file paths
code_file = pathlib.Path(f"{nb_file.stem}_scripted.py")
warn_file = pathlib.Path(f"{nb_file.stem}_pep8.txt")
nb_magic_file = pathlib.Path(".github/helpers/nb_flake8_magic.json")

def check_cell_content(source):
    """Verify that a cell contains any content besides whitespace or newlines"""
    for line in source:
        if re.search('^(?!(?:\\n)$)', line):
            # a "negative lookahead" for any characters in "non-capturing group"
            return True

# save code cell contents to a script divided into blocks with the separator
code_cells = []
with open(nb_file) as nf:
    og_nb = json.load(nf)

    with open(code_file, 'w') as cf:
        for i, cl in enumerate(og_nb['cells']):
            if (cl['cell_type'] == 'code'
                and cl['source']
                and check_cell_content(cl['source'])
            ):
                # only check code cells containing actual code; skip blanks
                code_cells.append(i)

                # check zeroth line for comment on errors to be ignored in this
                # cell. if any, generate appropriate "noqa" comment
                top_line = cl['source'][0]
                noqa_check = re.search('^# flake8-ignore', top_line)
                noqa_comment = ('' if noqa_check is None
                                else '  # noqa' + top_line[noqa_check.end():])

                for ln in cl['source']:
                    # comment out lines with IPython magic commands
                    line = ln if ln[0] != '%' else '# ' + ln

                    # insert noqa comment if needed (with care for newline char)
                    if (noqa_comment and not line.startswith('#')
                            and line != '\n' and line.endswith('\n')):
                        line = line[:-1] + noqa_comment
                    elif (noqa_comment and not line.startswith('#')
                            and line != '\n'):
                        line += noqa_comment[:-1]

                    cf.write(line)
                cf.write('\n' * buffer_lines)
                cf.write(separator)

# without spawning a shell, run flake8 and save any PEP8 warnings to a new file
with open(warn_file, 'w') as wf:
  # flake8's command line options are specified in base repo folder's .flake8
  subprocess.run(['flake8', code_file], stdout=wf)

# read in the PEP8 warnings
with open(warn_file) as wf:
    warns = wf.readlines()

# if there are none, QUIT while we're ahead
if not warns:
    print(f"{nb_file} is clean!")
    sys.exit()

# else, read in the script and find the lines that function as cell borders
with open(code_file) as cf:
    script = cf.readlines()

borderlines = [j for j, ll in enumerate(script, start=1)  # 1-indexed, like file
               if re.search(fr"#+{identifier}#+", ll)]

# customize the beginning of each PEP8 warning
pre = dt.now(pytz.timezone("America/New_York")).strftime('%Y-%m-%d %H:%M:%S - INFO - ')
# pre = 'INFO:pycodestyle:'
# pre = ''

# create dict ready to take stderr dicts and append warning messages. the nested
# defaultdict guarantees a first-level key for each cell number needed, and a
# second-level list for appending 'text' strings, and nothing extra (w/o errors!)
stderr_shared = {'name': 'stderr', 'output_type': 'stream'}
nu_output_dict = defaultdict(lambda: defaultdict(list))

# match the warnings' line numbers to the notebook's cells with regex and math
for script_line in warns:
    # get this warning's line number in the script
    wrn = script_line[re.match(code_file.name, script_line).end():]
    script_line_num = int(re.search(r'(?<=:)\d+(?=:)', wrn).group())

    # translate it into cell numbers and then to intra-cell line number
    code_cell_num = np.searchsorted(borderlines, script_line_num)
    all_cell_num = code_cells[code_cell_num]
    borderline_num = borderlines[code_cell_num - 1] if code_cell_num > 0 else 0
    next_borderline_num = borderlines[code_cell_num]

    if script_line_num != next_borderline_num:
        line_in_cell = str(script_line_num - borderline_num)
    else:
        # correct line number for E303 by accounting for buffer added earlier
        line_in_cell = str(script_line_num - borderline_num - buffer_lines)

    # print(f"--borderline:L{borderlines[code_cell_num - 1]},"
    #       f"next borderline:L{borderlines[code_cell_num]},"
    #       f"errorline:L{script_line_num}--")
    # print(f"code_cell_num {code_cell_num}, line_in_cell {line_in_cell}, "
    #       f"all_cell_num {all_cell_num}")

    # only keep line/column info and warning from original flake8 text.
    # prepend it with the customized string chosen earlier
    nu_msg = pre + re.sub(r':\d+(?=:)', line_in_cell, wrn, count=1)

    # update the defaultdict
    nu_output_dict[all_cell_num].update({'name': 'stderr',
                                         'output_type': 'stream'})
    nu_output_dict[all_cell_num]['text'].append(nu_msg)

# use the defaultdict's keys to learn which cells require warnings
cells_to_edit = list(nu_output_dict.keys())
injected_nb = copy.deepcopy(og_nb)

for num, cell in enumerate(injected_nb['cells']):
    # clear any cell output, regardless of PEP8 status
    if cell.get('execution_count'):
        cell['execution_count'] = None
    if cell.get('outputs'):
        cell['outputs'] = []

    # inject PEP8 warnings into cells marked earlier
    if num in cells_to_edit:
        cell['outputs'] = [nu_output_dict[num]]

# insert cells for enabling interactive PEP8 feedback just above first code cell
# if they aren't already present
with open(nb_magic_file) as nmf:
  flake8_magic_cells = json.load(nmf)['cells']

if all([og_nb['cells'][i].get('source') != flake8_magic_cells[0]['source']
        for i in code_cells]):
  injected_nb['cells'][code_cells[0]:code_cells[0]] = flake8_magic_cells

# save the edited notebook
with open(nb_file, 'w') as file:
    json.dump(injected_nb, file, indent=1, ensure_ascii=False)
    file.write("\n") # end with new line since json.dump doesn't
