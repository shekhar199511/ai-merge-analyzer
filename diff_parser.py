from unidiff import PatchSet

def get_valid_diff_lines(diff_content: str):
    valid_lines = set()
    patch = PatchSet(diff_content.splitlines(keepends=True))
    for file in patch:
        for hunk in file:
            for line in hunk:
                if line.is_added:
                    valid_lines.add((file.path, line.target_line_no))
    return valid_lines