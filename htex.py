from html.parser import HTMLParser

# Read contents of file
html_path = 'sample.html'

with open(html_path, 'r') as file:
    html_content = ''
    line = file.readline()

    while line:
        html_content += line
        line = file.readline()

html = html_content

class MyHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.current_heading = None
        self.result = []  # List to store the formatted text
        self.in_p = False

    def handle_starttag(self, tag, attrs):
        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self.current_heading = tag

        if tag == "p":
            self.in_p = True

    def handle_endtag(self, tag):
        if tag == self.current_heading:
            self.current_heading = None

        if tag == "p":
            self.in_p = False

    def handle_data(self, data):
        if self.current_heading == "h1":
            self.result.append(f"\\section{{{data.strip()}}}")  

        if self.current_heading == "h2":
            self.result.append(f"\\subsection{{{data.strip()}}}")  

        if self.in_p:
            self.result.append(f"{data}")

# Example usage
parser = MyHTMLParser()


parser.feed(html)

# Store result as a single text string
output_text = "\n".join(parser.result)

with open("output.tex", "w") as f:
    f.write(output_text)
