from html.parser import HTMLParser
import argparse

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_heading = None
        self.result = []  # List to store the formatted text
        self.in_p = False
        self.in_title = False
        self.is_strong = False
        self.is_membername = False
        self.is_date = False

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.current_heading = tag
        if tag == "title":
            self.in_title = True

        if tag == "p":
            self.in_p = True

        if tag == "strong":
            self.is_strong = True

        if tag == "membername":
            self.is_membername = True

        if tag == "date":
            self.is_date = True

    def handle_endtag(self, tag):
        if tag == self.current_heading:
            self.current_heading = None

        if tag == "p":
            self.in_p = False

        if tag == "title":
            self.in_title = False

        if tag == "strong":
            self.is_strong = False

        if tag == "membername":
            self.is_membername = False 

        if tag == "date":
            self.is_date = False

    def handle_data(self, data):
        if self.current_heading == "h1":
            self.result.append(f"\\section{{{data.strip()}}}")  

        if self.current_heading in {"h2", "h3", "h4", "h5", "h6"}:
            self.result.append(f"\\subsection{{{data.strip()}}}")  

        if self.in_p:
            self.result.append(f"{data}")

        if self.in_title:
            self.result.append(f"\\title{{{data}}}")
            self.result.append("\\maketitle")

        if self.is_strong:
            self.result.pop()
            self.result.append(f"\\textbf{{{data}}}")

        if self.is_membername:
            self.author = data.strip()

        if self.is_date:
            self.date = data.strip()
        


parsed = MyHTMLParser()

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input [filename]')
args = parser.parse_args()

input = args.input
with open(input, 'r') as file:
    content = ''
    line = file.readline()

    while line:
        content += line
        line = file.readline()

html_to_transform = content 

parsed.feed(html_to_transform)

output = "\n".join(parsed.result)
with open("output.tex", "w") as f:
    f.write(output)

def insert_template(file_path, lines_to_insert, lines_to_append):
    try:
        with open(file_path, 'r') as file:
            content = ''
            line = file.readline()

            while line:
                content += line
                line = file.readline()

        with open(file_path, 'w') as file:
           file.write('\n'.join(lines_to_insert) + '\n')
           file.write(content)
           file.write('\n'.join(lines_to_append) + '\n')

        print(f"article {file_path} created successfully.")

    except Exception as e:
        print(f"Error: {e}")


author = parsed.author
date = parsed.date
file = 'output.tex'
template_start= [
    r"\documentclass{article}",
    rf'\author{{{author}}}',
    rf'\date{{{date}}}'
    '\n', r"\begin{document}",
]

template_end = [
    '\n', r'\end{document}'
]

insert_template(file, template_start, template_end)

