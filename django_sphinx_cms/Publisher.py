from pathlib import Path
from pickle import loads

from django.template.loader import render_to_string


class Publisher:

    def __init__(self, repository_name):
        self._repository_name = Path(repository_name)
        self._pickles_base = Path('_cache/sphinx_pickles')
        self._builder_type = 'htmlcontent'
        self._suffix = '.html'
        self._public_base = Path('public/docs')
        self._template = 'django_sphinx_cms/sphinx.html'

    def publish(self):
        for pickle in self.list_pickles():
            parts = loads(Path(pickle).read_bytes())
            if 'body' in parts:
                self.write(self._render(parts), parts)

    def write(self, content, parts):
        target = self._get_target_path(parts['current_page_name'])
        if not target.parent.exists():
            target.parent.mkdir(parents=True)
        target.write_text(content)

    def list_pickles(self):
        return self._get_pickles_directory().glob('**/*.fpickle')

    def _get_pickles_directory(self):
        return self._pickles_base / self._repository_name / self._builder_type

    def _get_target_path(self, current_page_name):
        return (self._public_base / self._repository_name /
                current_page_name).with_suffix(self._suffix)

    def _render(self, parts):
        return render_to_string(self._template, parts)
