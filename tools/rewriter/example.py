"""An example script applying rewrite rules files passed in as arguments.

Usage: example.py "gtk-3.*/*.css"
"""

from __future__ import print_function
import sys
from rewriter import background_color
from rewriter import border_color
from rewriter import color
from rewriter import Mod
from rewriter import rewrite_files

mods = [
    Mod(r'button',
        remove=r' *box-shadow:[^;]*;',
        enabled=True),
    Mod(r'button\.suggested-action',
        anti=[r'\.destructive-action'],
        remove=color(),
        replace=r'\1@theme_base_color\3',
        enabled=False),
    Mod(r'button\.suggested-action',
        anti=[r'\.destructive-action'],
        remove=background_color(),
        replace=r'\1@suggestion_color\3',
        enabled=False),
    Mod(r'button',
        anti=[r'\..*\-action'],
        remove=color(),
        replace=r'\1@suggestion_color\3',
        enabled=False),
    Mod(r'button',
        anti=[r'\..*\-action'],
        remove=background_color(),
        replace=r'\1@theme_base_color\3',
        enabled=False),
    Mod(r'menuitem.*button',
        anti=[r'\..*\-action'],
        remove=color(),
        replace=r'\1@theme_text_color\3',
        enabled=True),
    Mod(r'text-button',
        anti=[r'\..*\-action'],
        remove=color(),
        replace=r'\1@theme_text_color\3',
        enabled=True),
    Mod(r'menuitem.*button',
        anti=[r'\..*\-action'],
        remove=background_color(),
        replace=r'\1@theme_base_color\3',
        enabled=True),
    Mod(r'text-button',
        anti=[r'\..*\-action'],
        remove=background_color(),
        replace=r'\1@theme_base_color\3',
        enabled=True),
    Mod(r'button.*:disabled',
        anti=[r'-action'],
        remove=border_color(),
        replace=r'\1@insensitive_bg_color\3',
        enabled=True),
    Mod(r'button.*:disabled',
        anti=[r'-action'],
        remove=border_color(),
        replace=r'\1@insensitive_bg_color\3',
        enabled=True),
    Mod(r'button.*:disabled',
        anti=[r'-action'],
        remove=background_color(),
        replace=r'\1@theme_base_color\3',
        enabled=True),
    Mod(r'button.*:disabled',
        anti=[r'-action'],
        remove=color(),
        replace=r'\1@insensitive_fg_color\3',
        enabled=True),

    Mod(r'button.suggested-action.*:disabled',
        anti=[r'\.destructive-action'],
        remove=color(),
        replace=r'\1@insensitive_fg_color\3',
        enabled=True),
    Mod(r'button.suggested-action.*:disabled',
        anti=[r'\.destructive-action'],
        remove=background_color(),
        replace=r'\1@suggestion_color\3',
        enabled=True),
    Mod(r'.*',  # Fixes rgba(@color, .*)
        remove=r'rgba(\(@[a-z_]*), .*(, [01]\.[0-9]*\))',
        replace=r'alpha\1\2'),
    Mod(r'.*',  # Fixes alpha(currentColor, @var.*
        remove=r'alpha\(currentColor, (@[a-z][^\.]*)([\.0-9]*)\)',
        replace=r'alpha(\1, 0\2)')
]

if len(sys.argv) > 1:
  rewrite_files(sys.argv[1:], mods)
else:
  print('No files were passed in.')
  exit()
