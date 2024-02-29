import re
import sys

def convert_markdown(text):
    # First pass: Handle blocks with language and captions
    complex_pattern = re.compile(
        r'~~~\{\.(\w+)(?:\s+caption="([^"]*)")?\}\n(.*?)~~~', re.DOTALL)
    
    def complex_replacer(match):
        language = match.group(1)
        caption = match.group(2) or "Unnamed"
        code = match.group(3).strip()
        return f"## {caption}\n```{language}\n{code}\n```"

    text = re.sub(complex_pattern, complex_replacer, text)

    # Intermediary pass: Handle blocks with just a language specification
    intermediary_pattern = re.compile(
        r'~~~\{(.*?)\}\n(.*?)~~~', re.DOTALL)
    
    def intermediary_replacer(match):
        language = match.group(1)
        code = match.group(2).strip()
        return f"## Unnamed\n```{language}\n{code}\n```"

    text = re.sub(intermediary_pattern, intermediary_replacer, text)

    # Second pass: Handle simpler blocks without language or captions
    simple_pattern = re.compile(
        r'~~~\n(.*?)~~~', re.DOTALL)
    
    def simple_replacer(match):
        code = match.group(1).strip()
        return "## Unnamed\n```\n" + code + "\n```"

    text = re.sub(simple_pattern, simple_replacer, text)

    return text

def add_page_break_before_headings(text):
    # Regex to match headings that start with # or ##
    heading_pattern = re.compile(r'^(#{1,2}\s+.+)$', re.MULTILINE)
    
    # Function to add a markdown page break before the matched heading
    def page_break_replacer(match):
        return f"---\n{match.group(0)}"

    # Replace all occurrences of headings with themselves preceded by a page break
    text_with_breaks = re.sub(heading_pattern, page_break_replacer, text)
    
    return text_with_breaks

# Read input from stdin and process
input_text = sys.stdin.read()
converted_text = add_page_break_before_headings(convert_markdown(input_text))

# Output the converted text to stdout
sys.stdout.write(converted_text)
