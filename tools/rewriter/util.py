"""A set of helper functions for parsing text."""

import re

NEWLINE = '\n'
WHITESPACE_RE = re.compile(r'\w+')


def remove_empty_lines(text):
  """Removes empty lines from text (preserving trailing whitespace)."""
  non_empty_lines = []
  for line in text.split(NEWLINE):
    if not WHITESPACE_RE.match(line):
      non_empty_lines.append(line)
  return NEWLINE.join(non_empty_lines)


def whitespace(text):
  """Removes leading whitespace from a string.

  Args:
    text(string): Text to remove whitespace from.
  Returns:
    A tuple containing the leading whitespace and the remaining text.
  """
  match = WHITESPACE_RE.match(text)
  if match:
    return (match.group(), text[match.end():])
  return ('', text)


def until(text, suffixes):
  """Splits text at the first suffix or 'end token'.

  Args:
    text(string): a string to remove prefixed whitespace from.
    suffixes(List[string]): a list of strings that mark the end of a block.
  Returns:
    A tuple containing the text before the end token, the end token and any
    remaining, unprocessed, text.
  """
  # Convert the search for each suffix into a single regex
  pattern = '({})'.format(r'|'.join(map(re.escape, suffixes)))
  match = re.search(pattern, text)

  if match:
    # If we find a suffix, split the text around it.
    chunk = text[:match.start()]
    suffix = match.group()
    text = text[match.end():]
    return chunk, suffix, text
  # If no suffix is found, consume the whole string.
  return text, '', ''
