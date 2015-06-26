import os
import base64
import urllib

local_file = lambda x: os.path.join(os.path.dirname(__file__), x)


def read_from_local(img_name):
    img_file = open(local_file(img_name), 'rb')
    img_content = img_file.read()
    return img_content


def read_from_remote(url):
    img_resource = urllib.urlopen(url)
    img_content = img_resource.read()
    return img_content


def write_to_local(bin_content, file_name="sample"):
    b64_content = base64.b64encode(bin_content)
    template = '<img src="data:image/png;base64,%s"/>'
    open(local_file(file_name + '.html'), 'w').write(template % b64_content)


def test():
    img_url = 'https://www.python.org/static/img/python-logo.png'
    write_to_local(read_from_remote(img_url), file_name='ignore-remote')
    write_to_local(read_from_local('python-logo.png'), file_name='ignore-local')


if __name__ == '__main__':
    test()

