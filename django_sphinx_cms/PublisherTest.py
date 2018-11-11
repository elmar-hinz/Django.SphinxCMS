from pathlib import Path
import pickle


from django.test import TestCase

from django_sphinx_cms.Publisher import Publisher


class PublisherTest(TestCase):

    def test_find_pickles(self):
        publisher = Publisher('PythonBlog')
        pickles = publisher.list_pickles()
        self.assertEqual(
            '_cache/sphinx_pickles/PythonBlog/pickle/genindex.fpickle',
            str(list(pickles)[0]))

    def test_unserialize_pickle(self):
        path = '_cache/sphinx_pickles/PythonBlog/pickle/Django' \
               '/DjangoSetupChecklist.fpickle'
        path = Path(path)
        parts = pickle.loads(path.read_bytes())
        publisher = Publisher('PythonBlog')
        content = publisher.render(parts)
        publisher.write(content, parts)

    def test_publish(self):
        publisher = Publisher('PythonBlog')
        publisher.publish()


