import itertools
import unittest

from elements.document import Document
from elements.element_impls import FormattedText, Text, Paragraph
from render_html.html_visitor import HtmlVisitor, non_span_formatting

from tests import test_utils


class HtmlRenderingTest(unittest.TestCase):

    @staticmethod
    def render_elements(*elements):
        return HtmlRenderingTest.render(Document(elements))

    @staticmethod
    def render(document):
        test_file = HtmlRenderingTest.TestFile()
        visitor = HtmlVisitor(test_file)
        visitor.write(document)
        return test_file.content()

    def test_formatted_text(self):
        for kind in list(FormattedText.Kind):
            formatted_text = FormattedText(kind, [Text("hello world")])
            rendered = self.render_elements(formatted_text)
            if kind in non_span_formatting:
                open_tag, close_tag = non_span_formatting[kind]
                self.assertIn(open_tag, rendered)
                self.assertIn(close_tag, rendered)
            else:
                self.assertIn(kind.name, rendered)  # kind.name should appear as a class

    def test_heading(self):
        word = test_utils.word()
        heading = test_utils.word()
        elements = [Paragraph([Text(word)])]
        document = Document(elements, heading=heading)
        rendered = self.render(document)
        self.assertIn(word, rendered)
        self.assertIn(heading, rendered)

    def test_paragraph(self):
        bools = (False, True)
        for embedded, poetic, introductory in itertools.product(bools, bools, bools):
            word = test_utils.word()
            text = Text(word)
            paragraph = Paragraph([text],
                                  embedded=embedded,
                                  poetic=poetic,
                                  introductory=introductory)
            rendered = self.render_elements(paragraph)
            self.assertIn(word, rendered)
            if embedded:
                self.assertIn("embedded", rendered)  # should appear as a class
            else:
                self.assertNotIn("embedded", rendered)
            if poetic:
                self.assertIn("poetic", rendered)
            else:
                self.assertNotIn("poetic", rendered)
            if introductory:
                self.assertIn("introductory", rendered)
            else:
                self.assertNotIn("introductory", rendered)

    class TestFile(object):
        """
        A file-like string object used for mocking text files
        """
        def __init__(self):
            self._content = ""

        def content(self):
            return self._content

        def write(self, p_str):
            self._content += p_str


if __name__ == "__main__":
    unittest.main()
