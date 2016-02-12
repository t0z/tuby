from pyminifier import minification, analyze
import re
pat_blob = re.compile(r"^.*\('(.*)'\).*$")


class NoMatchError(Exception):
    pass


def bz2_pack(source):
    """
    Returns 'source' as a bzip2-compressed, self-extracting python script.

    .. note::

        This method uses up more space than the zip_pack method but it has the
        advantage in that the resulting .py file can still be imported into a
        python program.
    """
    import bz2
    import base64
    out = ""
    # Preserve shebangs (don't care about encodings for this)
    first_line = source.split('\n')[0]
    if analyze.shebang.match(first_line):
        out = first_line + '\n'
    compressed_source = bz2.compress(source.encode('utf-8'))
    out += base64.b64encode(compressed_source).decode('utf-8')
    return out


def mini(source):
    for action in [
                   'remove_blank_lines',
                   'remove_comments_and_docstrings',
                   'reduce_operators',
                   'remove_blank_lines',
                   'dedent'
                   ]:
        source = getattr(minification, action)(source)
    return bz2_pack(source)
