#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import re
import time
import json


ROOT = os.path.dirname(__file__)
join = lambda dirname, x: '%s/%s' % (dirname, x)
_ = lambda x: join(ROOT, x)
# _ = lambda x: os.path.join(ROOT, x)
# join = os.path.join
DESCRIPTION = u'粘贴板，临时记录一些代码片段或者其他咚咚'.encode('utf-8')  # sys.getfilesystemencoding()
PATTERN = re.compile('^[a-zA-Z0-9\-_]+(\.[a-z]+)?$')
FILE_EXTS = ['', '.markdown', '.md', '.rst', '.txt', '.py', '.c', '.php', '.java', '.js', '.css']
INDEX_FILE = _('README.md')
IGNORE_FILES = ['README.md']
IGNORE_PATHS = [INDEX_FILE, __file__, _('LICENSE')]
BASE_URL = '../../blob/master/'


def ctime(path):
    return os.path.getctime(path)


def time_str(stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp))


class Item(object):
    def __init__(self, path, depth=None):
        self.path = path
        self.depth = depth or 0

    def name(self):
        pass

    def url(self):
        pass

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, repr(self.__dict__))

    def title(self):
        return self.basename

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
    def __init__(self, path, depth=None):
        super(PathItem, self).__init__(path, depth)
        # self.dirname = os.path.dirname(path)
        self.basename = os.path.basename(path)
        self.ctime = ctime(path)

    def name(self):
        return self.basename

    def url(self):
        return BASE_URL + self.basename

    def order(self):
        return self.ctime

    def render(self):
        return '%s- [%s](%s)' % (' ' * 4 * (self.depth - 1), self.title(), self.url())


class FileItem(PathItem):
    def __init__(self, path, depth=None):
        super(FileItem, self).__init__(path, depth)
        self.time = time_str(self.ctime)

    def order(self):
        return self.ctime


class DirItem(PathItem, Items):
    order = 3

    def __init__(self, path, depth=None):
        super(DirItem, self).__init__(path, depth)
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
                items.append(FileItem(path, depth=self.depth+1))
            elif os.path.isdir(path):
                items.append(DirItem(path, depth=self.depth+1))
            else:
                continue
        return items

    def title(self):
        return '**%s/**' % self.basename

    def render(self):
        return '\n'.join([PathItem.render(self), Items.render(self)])


class Index(DirItem):
    NOTE_PATTERN = re.compile('^\d{8}-\d{3}\.md$')

    def __init__(self, path, depth=None):
        super(Index, self).__init__(path, depth)
        self.notes = Items('Notes')
        for i in self.children:
            if self.NOTE_PATTERN.match(i.basename):
                self.notes.append(i)
        for i in self.notes:
            self.children.remove(i)

    @classmethod
    def generate(cls):
        if not os.path.exists(INDEX_FILE):
            open(INDEX_FILE, 'w').close()
        with open(INDEX_FILE, 'rU+') as f:
            f.write(Index(ROOT).render())

    def render(self):
        return '\n\n'.join([
            '# %s' % self.basename,
            DESCRIPTION,
            '## Snippets',
            Items.render(self),
            '## Nodes',
            self.notes.render()
        ]) + '\n'


def test():
    def json_encoder(o):
        if isinstance(o, object):
            return o.__dict__
    print json.dumps(Index(ROOT), default=json_encoder, indent=4)


if __name__ == '__main__':
    # test()
    Index.generate()
