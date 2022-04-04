import json
import sys
import traceback
import re
import inspect
from ast import literal_eval
from collections.abc import Iterable
from itertools import zip_longest


# By ideasman42, https://stackoverflow.com/a/41658338.
def execfile(filepath, globals=None, locals=None):
    if globals is None:
        globals = {}
    globals.update({
        '__file__': filepath,
        '__name__': '__main__',
    })
    with open(filepath, 'rb') as file:
        exec(compile(file.read(), filepath, 'exec'), globals, locals)


dirname, name, *_ = sys.argv[1:]
py = f'./{dirname}/{name}.py'
tests = f'./{dirname}/{name}.testcases'

with open(tests) as f:
    lines = [l for l in f.readlines() if l.startswith('Input: ') or l.startswith('Output: ')]
    tests = [
        {
            'inputs': {k: literal_eval(v) for k, v in kwargs},
            'output': literal_eval(v.title() if (v := lines[i+1][len('Output: '):].strip()) in ('true', 'false') else v),
        }
            for i in range(0, len(lines), 2)
            if (kwargs := re.findall(r'(\w+) = ([^=]+)(?:,|$)', lines[i]))
    ]
    if False:
        tests = [
            {
                'inputs': literal_eval(lines[i]),
                'output': literal_eval(lines[i+1]),
            }
            for i in range(0, len(lines), 2)
        ]


try:
    execfile(py, globals(), locals())
except SyntaxError as e:
    traceback.print_exc()
    exit(2)

method = next(n for n, _
              in inspect.getmembers(Solution, predicate=inspect.isfunction)
              if not n.startswith('_'))

s = Solution()
wrong_answer = False

def wa(t, output):
    print(f'{method}({t["inputs"]})\n\t== {output}\n\t!= {t["output"]}')
    global wrong_answer
    wrong_answer = True

for t in tests:
    m = getattr(s, method)
    try:
        output = m(**t['inputs'])
    except Exception as e:
        traceback.print_exc()
        exit(3)

    if isinstance(output, Iterable):
        if not isinstance(t["output"], Iterable) or any(a != b for a, b in zip_longest(output, t["output"])):
            wa(t, output)
    elif output != t['output']:
        wa(t, output)

if wrong_answer:
    exit(1)

if 'check_tle' in locals():
    check_tle()
