import argparse
import os

from django.core.management import BaseCommand, CommandParser
from git import Repo
from sphinx.cmd.make_mode import run_make_mode

from django_sphinx_cms.Publisher import Publisher

class Command(BaseCommand):
    help = 'Manage local sphinx repositories'
    repo_base = 'private/sphinxes/'
    pickle_base = '_cache/sphinx_pickles'
    destination_base = 'public/'

    def add_arguments(self, parser: CommandParser):
        parser.description = self.help
        parser.add_argument(
            'command', type=str,
            help='One of: clone, pull, build, publish, update. Note: update = '
                 'pull + build + publish.'
        )
        parser.add_argument(
            'repository', type=str,
            help='Local repo name (a simple directory name).'
        )
        parser.add_argument(
            '--url', type=str,
            help='URL to clone from, e.g. Github. Wrap in quotes?'
        )

    def handle(self, *args, **options):
        command = options['command']
        repo = options['repository']
        if command == 'clone':
            url = options['url']
            if url is None:
                raise argparse.ArgumentTypeError(
                    'Clone requires --url option with the repo to clone from.')
            else:
                self.clone(repo, url)
        elif command == 'pull':
            self.pull(repo)
        elif command == 'build':
            self.build(repo)
        elif command == 'publish':
            self.publish(repo)
        elif command == 'update':
            self.pull(repo)
            self.build(repo)
            self.publish(repo)
        else:
            raise argparse.ArgumentTypeError(
                'invalid command {}'.format(command))

    def publish(self, repo):
        """ Publish static HTML files based on templates. """
        publisher = Publisher(repo)
        publisher.publish()

    def build(self, repo_name):
        source = self.get_repo_path(repo_name)
        destination = self.get_pickle_path(repo_name)
        run_make_mode(['htmlcontent', source, destination])

    def clone(self, repo_name, origin_url):
        path = self.get_repo_path(repo_name)
        if os.path.exists(path):
            msg = 'The path to the repo already exists: {}'
            raise FileExistsError(msg.format(path))
        print('Clone {} into {}'.format(origin_url, path))
        local = Repo.init(path)
        remote = local.create_remote('origin', origin_url)
        assert remote.exists()
        assert remote == local.remotes.origin == local.remotes['origin']
        remote.fetch()  # Assure we actually have data.
        # Create local branch "master" from remote "master".
        local.create_head('master', remote.refs.master)
        # Set local "master" to track remote "master.
        local.heads.master.set_tracking_branch(remote.refs.master)
        # Checkout local "master" to working tree.
        local.heads.master.checkout()

    def pull(self, repo_name):
        print('Pull {}'.format(repo_name))
        path = self.get_repo_path(repo_name)
        repo = Repo(path)
        repo.git.pull()

    def get_repo_path(self, repo_name):
        return os.path.join(self.repo_base, repo_name)

    def get_pickle_path(self, repo_name):
        return os.path.join(self.pickle_base, repo_name)

    def get_destination_path(self, repo_name):
        return os.path.join(self.pickle_base, repo_name)
