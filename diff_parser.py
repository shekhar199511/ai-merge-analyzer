from unidiff import PatchSet

def get_valid_diff_lines(diff_content: str):
    """
    Parses the diff and returns a set of (filename, line_number) tuples
    representing valid lines for inline comments.
    """
    valid_lines = set()
    patch = PatchSet(diff_content.splitlines(keepends=True))
    for file in patch:
        for hunk in file:
            for line in hunk:
                # Only consider added or modified lines (not removed/context)
                if line.is_added or line.is_modified:
                    valid_lines.add((file.path, line.target_line_no))
    return valid_lines