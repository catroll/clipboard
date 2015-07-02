def dd(filename, size=None):
    with open(filename, 'w') as f:
        f.seek(2 ** 10)  # 1GB
        f.write(chr(0))


dd('./tmp')
