#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import time
import json

THIS = os.path.abspath(__file__)
ROOT = os.path.dirname(THIS)
join = lambda dirname, x: '%s/%s' % (dirname, x)
_ = lambda x: join(ROOT, x)
# _ = lambda x: os.path.join(ROOT, x)
# join = os.path.join
DESCRIPTION = u'粘贴板，临时记录一些代码片段或者其他咚咚'.encode('utf-8')
PATTERN = re.compile('^[a-zA-Z0-9\-_]+(\.[a-z]+)?$')
FILE_EXTS = ['', '.markdown', '.md', '.rst', '.txt', '.py', '.c', '.php', '.java', '.js', '.css']
INDEX_FILE = _('README.md')
IGNORE_FILES = ['README.md']
IGNORE_PATHS = [INDEX_FILE, THIS, _('LICENSE'), _('update')]
BASE_URL = 'http://git.oschina.net/catroll/clipboard/blob/master'
MAX_DEPTH = 2


def ctime(path):
    return os.path.getctime(path)


def mtime(path):
    return os.path.getmtime(path)


def time_str(stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp))


class Item(object):
    def __init__(self, path, depth=None):
        self.path = path
        self.depth = depth or 0

    def url(self):
        pass

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, repr(self.__dict__))

    def render(self):
        raise NotImplemented


class Items(Item):
    def __init__(self, path, depth=None):
        super(Items, self).__init__(path, depth)
        self.children = []

    def __iter__(self):
        for i in self.children:
            yield i

    def append(self, item):
        self.children.append(item)

    def sort(self):
        self.children.sort(key=lambda i: i.order, reverse=True)

    def render(self):
        return '\n'.join([i.render() for i in self.children])


class PathItem(Item):
    def __init__(self, path, depth=None, base_url=None):
        super(PathItem, self).__init__(path, depth)
        # self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)
        self.base_url = base_url
        self.ctime = ctime(path)
        self.order = self.basename

    def title(self):
        return self.basename

    def url(self):
        if self.base_url is None:
            return self.basename
        return '/'.join([self.base_url, self.basename])

    def raw_render(self):
        return '%s- %s' % (' ' * 4 * (self.depth - 1), self.title())

    def render(self):
        return '%s- [%s](%s)' % (' ' * 4 * (self.depth - 1), self.title(), self.url())


class FileItem(PathItem):
    def __init__(self, *args, **kwargs):
        super(FileItem, self).__init__(*args, **kwargs)
        self.time = time_str(self.ctime)


class DirItem(PathItem, Items):
    def __init__(self, *args, **kwargs):
        super(DirItem, self).__init__(*args, **kwargs)
        self.order = -1
        if self.depth < MAX_DEPTH:
            self.children = self.walk(self.path)
        self.sort()

    def walk(self, base_path):
        items = []
        for i in os.listdir(base_path):
            path = join(base_path, i)
            if path in IGNORE_PATHS or i in IGNORE_FILES or not PATTERN.match(i):
                continue
            if os.path.isfile(path):
                name, ext = os.path.splitext(i)
                if ext not in FILE_EXTS:
                    continue
                items.append(FileItem(path, depth=self.depth + 1, base_url=self.url()))
            elif os.path.isdir(path):
                items.append(DirItem(path, depth=self.depth + 1, base_url=self.url()))
            else:
                continue
        return items

    def title(self):
        return '**%s/**' % self.basename

    def render(self):
        if not self.children:
            return PathItem.render(self)
        return '\n'.join([PathItem.render(self), Items.render(self)])


class Index(DirItem):
    NOTE_PATTERN = re.compile('^\d{8}-.+\.md$')

    def __init__(self, path, depth=None):
        super(Index, self).__init__(path, depth)
        self.notes = Items('Notes')
        for i in self.children:
            if self.NOTE_PATTERN.match(i.basename):
                self.notes.append(i)
        for i in self.notes:
            self.children.remove(i)

    def url(self):
        return self.base_url

    @classmethod
    def generate(cls):
        with open(INDEX_FILE, 'w') as f:
            f.truncate()
            f.write(Index(ROOT).render())

    def render(self):
        return '\n\n'.join([
            '# %s' % self.basename,
            DESCRIPTION,
            '## Nodes',
            self.notes.render(),
            '## Snippets',
            Items.render(self),
        ]) + '\n'


def test():
    def json_encoder(o):
        if isinstance(o, object):
            return o.__dict__

    print json.dumps(Index(ROOT), default=json_encoder, indent=4)


if __name__ == '__main__':
    # test()
    Index.generate()
