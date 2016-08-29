import sys

from render_html.html_visitor import HtmlVisitor
from usfm import lex, parse


def main(input_filename, output_filename):
    with open(input_filename, "r") as input_file:
        contents = input_file.read()
        lexer = lex.UsfmLexer.create()
        lexer.input(contents)
        parser = parse.UsfmParser.create()
        document = parser.parse(lexer=lexer)
        with open(output_filename, "w") as output_file:
            visitor = HtmlVisitor(output_file)
            visitor.write(document)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
