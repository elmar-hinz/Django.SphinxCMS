import os
from pathlib import Path

from django.test import TestCase
from django_sphinx_cms.management.commands.sphinx import Command


# Create your tests here.


class CommandLineTest(TestCase):

    def test_path(self):
        path = os.path.join('first/second', 'third\\fourth')
        self.assertEqual('first/second/third\\fourth', path)

    def test_pathlib(self):
        path = Path('/first/second') / 'third' / 'fourth'
        self.assertEqual('/first/second/third/fourth', path.as_posix())
        self.assertEqual('/first/second/third/fourth', str(path))
        self.assertEqual('fourth', path.name)
        self.assertEqual(['/', 'first', 'second', 'third', 'fourth'], path._parts)

    def test_commands_pubilsh(self):
        command = Command()
        command.build('PythonBlog')
        command.publish('PythonBlog')
