"""Provides tools for automatically rewriting large sets of CSS."""

from __future__ import print_function
import re
import util


def contains(pattern, text):
  """Check that some text contains a pattern or the pattern is none."""
  if pattern is None:
    return True
  return re.search(pattern, text, re.MULTILINE)


class Mod(object):
  """Represents a rewrite to a CSS rule."""

  def __init__(self, match, remove, replace=None, anti=None, enabled=True):
    """Constructs a 'Mod' object.

    Args:
      match(string): A regex that the head of a CSS rule must match to be
        rewritten.
      remove(string): A regex for the portion of the CSS rule's body to be
        rewriten.
      replace(string): A regex that replace matches to 'remove' with.
      anti(List[string]): A set of regexes that the head of the CSS rule must
        not match.
      enabled(bool): A flag to easily enabled/disable a Mod.
    """
    self.match = match
    self.remove = remove
    self.replace = replace or r''
    self.anti = anti or []
    self.enabled = enabled

  def apply(self, head, body):
    """Rewrites a CSS rule if it matches a set of patterns.

    Replaces self.remove with self.replace (or nothing) in a chunk if the
    following conditions are met:
    - 'self.enabled' is True.
    - The rule's selectors contain text matching the pattern self.match.
    - The rule's selectors do not contain any of the patterns in self.anti.

    Args:
      head(string): Text containing all the selectors of a CSS rule.
      body(string): Text containing all the properties of a CSS rule.
    Returns:
      A tuple containing the updated selectors and properties of the CSS rule.
    """

    if self.enabled:
      if contains(self.match, head):
        for anti in self.anti:
          if contains(anti, head):
            return head, body
        # Apply the body change
        body, _ = re.subn(self.remove, self.replace, body)
    return head, body


def process_rule(chunk, mods):
  """Apply a set of modifications to a chunk of CSS.

  Args:
    chunk (string): a 'chunk' of CSS (generally a rule or a comment).
    mods (List[Mod]): a list of modifications/rewrites.
  Returns:
    the rewritten chunk.
  """
  sp_chunk = chunk.split('{')
  if len(sp_chunk) != 2:
    return chunk  # Not recognised as a 'rule'

  head, body = sp_chunk[0], sp_chunk[1]
  for mod in mods:
    head, body = mod.apply(head, body)

  # Clean up any deleted lines.
  body = util.remove_empty_lines(body)

  return head + '{' + body


def process(content, mods):
  """Apply a set of modifications to CSS."""
  output = []
  while content:
    # Skip over whitespace.
    whitespace, content = util.whitespace(content)
    output.append(whitespace)

    # Consume a rule or a comment at a time.
    chunk, split, content = util.until(content, ['}', '*/'])
    if split == '}':
      output.append(process_rule(chunk, mods))
    else:
      output.append(chunk)  # Leave unknown blocks unmodified.
    output.append(split)
  return ''.join(output)


def color_property_ending_in(suffix):
  """Generates regexes for color properties that have the suffix."""
  # Selects whitespace and property name before the suffix.
  before_suffix = r'([^;]*  *'
  # Selects the colon and most color values after the suffix and before the
  # semicolon.
  after_suffix = r':[^@#;0-9]*)([@#0-9][a-z_0-9]*)([^;]*;)'
  return before_suffix + suffix + after_suffix


def background_color():
  return color_property_ending_in(r'background-color')


def color():
  return color_property_ending_in(r'color')


def border_color():
  return color_property_ending_in(r'border-color')


def rewrite(path, mods):
  """Rewrites a file with a set of modifications.

  Reads a file, rewrites it in memory and then updates the source on disk.

  Args:
    path (string): a path to the file to rewrite.
    mods (List[Mod]): a list of modifications/rewrites.
  """
  contents = None
  with open(path, 'r') as cssfile:
    contents = cssfile.read()

  refactored = process(contents, mods)

  with open(path, 'w') as cssfile:
    cssfile.write(refactored)


def rewrite_files(paths, mods):
  """Rewrites a set of files with a set of modifications.

  Args:
    paths (List[string]): a list of paths to files to rewrite.
    mods (List[Mod]): a list of modifications/rewrites.
  """
  for path in paths:
    print('Rewriting {}'.format(path))
    rewrite(path, mods)
