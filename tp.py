from __future__ import unicode_literals

import unittest

from elements.document import Document
from usfm.lex import UsfmLexer
from usfm.parse import UsfmParser


class UsfmParserTests(unittest.TestCase):
    longMessage = True

    lexer = UsfmLexer.create()
    parser = UsfmParser.create()

    @staticmethod
    def parse(*lines):
        """
        :rtype: Document
        """
        UsfmParserTests.parser.reset()
        text = "\n".join(lines)
        UsfmParserTests.lexer.input(text)
        return UsfmParserTests.parser.parse(UsfmParserTests.lexer)
