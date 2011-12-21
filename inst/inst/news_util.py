import os
def walk_news(root, f):
    """
    f(category, fname)
    """
    for root, dirs, files in os.walk(root):
        category = os.path.basename(root)
        for fname in files:
            f(category, fname, root)

