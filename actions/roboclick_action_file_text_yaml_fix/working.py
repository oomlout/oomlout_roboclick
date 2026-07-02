"""
roboclick_action_file_text_yaml_fix

Reads a YAML file that may have block scalars (>-, |-) with unindented
content — a common AI output artefact — and rewrites it as valid YAML.

Strategy: treat every line that starts at column 0 matching `key:` as a key
anchor. Content between two anchors belongs to the preceding key. Block scalar
markers (>-, |-, >, |) are stripped; the raw content lines are collected and
written back with 2-space indentation under a `|-` literal block scalar.
Simple single-line values are written inline (quoted if necessary).

Action config keys:
  file_name  — filename to fix in place (relative to directory)

Returns None on success, "exit_no_tab" if the file is missing.
"""

import os
import re


def describe():
    d = {}
    d["name"]              = "roboclick_action_file_text_yaml_fix"
    d["name_short"]        = ["file_text_yaml_fix"]
    d["name_short_options"] = ["file_text_yaml_fix"]
    d["description"]       = "Fix malformed YAML with unindented block scalar content."
    d["returns"]           = "None on success, exit_no_tab if file missing."
    d["category"]          = "File"
    d["variables"]         = [
        {"name": "file_name", "description": "Filename to fix in place.", "type": "string", "default": ""},
    ]
    return d


def define():
    return describe()


def _needs_quoting(s):
    """Return True if the string must be quoted for safe inline YAML."""
    if not s:
        return True
    special = set(':#{}[]|>&*!,?\'"\\\n\r\t')
    return any(c in special for c in s) or s[0] in ('-', ' ', '@', '`')


def _quote(s):
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


def _parse(text):
    """
    Parse text where block scalar content may be at column 0.
    Returns list of (key, value_str) in document order.
    value_str is the raw collected text (may be multiline).
    """
    lines = text.splitlines()
    key_re = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)')

    # Find indices of key lines (column-0 key: … lines)
    anchors = []  # list of (line_index, key, inline_value)
    for i, line in enumerate(lines):
        m = key_re.match(line)
        if m:
            anchors.append((i, m.group(1), m.group(2).strip()))

    if not anchors:
        return []

    pairs = []
    for idx, (line_i, key, inline_val) in enumerate(anchors):
        next_line_i = anchors[idx + 1][0] if idx + 1 < len(anchors) else len(lines)

        # Lines between this key and the next (exclusive of the key line itself)
        body = lines[line_i + 1 : next_line_i]

        # Strip block scalar markers from inline_val
        is_block = inline_val in ('>-', '|-', '>', '|', '>+', '|+')

        if is_block or inline_val == '':
            # Content is in body lines
            # Strip leading/trailing blank lines
            while body and not body[0].strip():
                body.pop(0)
            while body and not body[-1].strip():
                body.pop()
            # Remove any common leading indentation
            non_empty = [l for l in body if l.strip()]
            if non_empty:
                min_indent = min(len(l) - len(l.lstrip()) for l in non_empty)
                body = [l[min_indent:] for l in body]
            value = re.sub(r'\n{2,}', '\n', '\n'.join(body))
        else:
            # Inline value — strip surrounding quotes if present
            val = inline_val
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            value = val

        pairs.append((key, value))

    return pairs


def _write(pairs):
    """Serialise key-value pairs as valid YAML."""
    out = []
    for key, value in pairs:
        if '\n' in value:
            out.append(f'{key}: |-')
            for line in value.splitlines():
                out.append(f'  {line}')
        else:
            out.append(f'{key}: {_quote(value) if _needs_quoting(value) else value}')
        out.append('')  # blank line between top-level keys
    return '\n'.join(out).rstrip('\n') + '\n'


def action(**kwargs):
    action_cfg = kwargs.get("action", {})
    file_name  = action_cfg.get("file_name", "")
    directory  = kwargs.get("directory", "")

    if not file_name:
        print("[yaml_fix] no file_name specified")
        return

    file_path = os.path.join(directory, file_name) if directory else file_name

    if not os.path.isfile(file_path):
        print(f"[yaml_fix] file not found: {file_path} — skipping")
        return "exit_no_tab"

    raw = open(file_path, encoding="utf-8-sig").read()

    pairs = _parse(raw)
    if not pairs:
        print(f"[yaml_fix] {file_name} — could not extract any key-value pairs")
        return

    fixed = _write(pairs)

    # Verify the fix actually parses
    try:
        import yaml as _yaml
        _yaml.safe_load(fixed)
    except Exception as e:
        print(f"[yaml_fix] fixed YAML still invalid ({e}) — leaving file unchanged")
        return

    with open(file_path, 'w', encoding='utf-8') as fh:
        fh.write(fixed)

    print(f"[yaml_fix] rewrote {file_name} as valid YAML ({len(pairs)} keys)")


def test(**kwargs):
    return callable(action)
