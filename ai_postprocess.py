import re
from typing import List, Dict

def parse_ai_issues(report_text: str) -> List[Dict]:
    """
    Parses the AI output to extract structured issue data for inline comments.

    Args:
        report_text: The AI's markdown-formatted analysis report.

    Returns:
        A list of dictionaries, each containing:
            - file: filename (str)
            - line: line number (int)
            - problem: description (str)
            - why: reason (str)
            - solution: suggested fix (str)
    """
    issues = []
    # Split issues by '---'
    for issue_block in report_text.split('---'):
        file_match = re.search(r'File:\s*(.+)', issue_block)
        line_match = re.search(r'Line:\s*(\d+)', issue_block)
        problem_match = re.search(r'Problem:\s*(.+)', issue_block)
        why_match = re.search(r'Why:\s*(.+)', issue_block)
        solution_match = re.search(r'Solution:\s*(.+)', issue_block)
        if file_match and line_match and problem_match:
            issues.append({
                'file': file_match.group(1).strip(),
                'line': int(line_match.group(1)),
                'problem': problem_match.group(1).strip(),
                'why': why_match.group(1).strip() if why_match else '',
                'solution': solution_match.group(1).strip() if solution_match else ''
            })
    return issues