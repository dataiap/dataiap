from news_util import walk_news
import sys, os

from mrjob.protocol import JSONValueProtocol


def encode_document(text, cats=None, id=None):
    """Encode a document as a JSON so that MRTextClassifier can read it.

    Args:
    text -- the text of the document (as a unicode)
    cats -- a dictionary mapping a category name (e.g. 'sports') to True if
        the document is in the category, and False if it's not. None indicates
        that we have no information about this documents' categories
    id -- a unique ID for the document (any kind of JSON-able value should
        work). If not specified, we'll auto-generate one.
    """
    text = unicode(text, errors='ignore')
    cats = dict((unicode(cat), bool(is_in_cat))
                for cat, is_in_cat
                in (cats or {}).iteritems())

    return JSONValueProtocol.write(
        None, {'document': text, 'cats': cats, 'docid': id, 'type' : 'document'}) + '\n'



root = os.path.abspath(sys.argv[1])
outroot = os.path.abspath(sys.argv[2])

def encode(category, fname, root):
    global outroot
    try:
        os.mkdir(os.path.join(outroot, category))
    except:
        pass

    with file(os.path.join(root, fname), 'r') as f:
        with file(os.path.join(outroot, category, fname), 'w') as outf:
            outf.write(encode_document(f.read(), {category:1}, fname))


walk_news(root, encode)
