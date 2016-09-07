import codecs
import os

from usfm_utils.html import HtmlVisitor
from usfm_utils.usfm import UsfmLexer, UsfmParser


def convert(usfm_filenames, output_dir, input_encoding="utf-8"):
    """
    :param iterable[str] usfm_filenames: Filenames of USFM files
    :param str input_encoding: Encoding of USFM files
    :param str output_dir: Output directory for generated files
    :return: Filenames of output files
    :rtype: list[str]
    """
    return [output for input_filename in usfm_filenames
            for output in convert_single(input_filename, output_dir,
                                         input_encoding=input_encoding)]

def convert_single(usfm_filename, output_dir, input_encoding="utf-8"):
    """
    :param str|unicode usfm_filename:
    :param str|unicode output_dir:
    :param str|unicode input_encoding:
    :return: Filenames of output files
    :rtype: list[str]
    """
    with codecs.open(usfm_filename, "r", encoding=input_encoding) as usfm_file:
        content = usfm_file.read()
    lexer = UsfmLexer.create()
    parser = UsfmParser.create()
    lexer.input(content)
    document = parser.parse(lexer=lexer)

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(usfm_filename))

    output_basename = os.path.splitext(os.path.basename(usfm_filename))[0] + ".html"
    output_filename = os.path.join(output_dir, output_basename)

    with codecs.open(output_filename, "w") as output_file:
        HtmlVisitor(output_file).write(document)

    return [output_filename]
