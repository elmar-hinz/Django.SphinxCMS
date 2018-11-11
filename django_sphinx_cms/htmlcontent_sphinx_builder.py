from sphinx.application import Sphinx
from sphinx.builders.html import PickleHTMLBuilder


class HtmlContentBuilder(PickleHTMLBuilder):
    """
    Builds HTML partials to be included in templates.

    Contrary to the PickleHTMLBuilder it builds links with the .html suffix.
    """
    name = 'htmlcontent'
    format = 'html'
    link_suffix = '.html'

    def get_target_uri(self, docname, typ=None):
        return docname + self.link_suffix

def setup(app: Sphinx):
    app.add_builder(HtmlContentBuilder)
    return {'version': '0.1'}
