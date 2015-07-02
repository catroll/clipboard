# 转换对象为字典和列表

from: https://gist.github.com/john1king/9243817

只要对象定义了 `keys` 方法，就使用 `keys` 和 `__getitem__` 来生成 dict
没有定义 `keys` 方法的对象，尝试先使用 `__iter__` 转换为 list 后再转换为 dict


```python
class Properties(object):

    def __init__(self, data):
        self._data = data
    
    def __iter__(self):
        return iter(list(self._data.values()))
    
    def __getitem__(self, key):
        return self._data[key]
    
    def keys(self):
        return list(self._data)


prop = Properties({'foo': 'bar'})
print dict(prop) # => {'foo': 'bar'}
print list(prop) # => ['bar']
```

对象转换为 list 优先迭代 `__iter__` 方法，没有定义 `__iter__` 方法的， 尝试用`__getitem__`方法索引对象，直到捕捉到 `IndexError`。
两种方式都会调用 `__len__` 方法，但是不会使用 `__len__` 的返回值来做索引

```python
class Foo(object):

    def __getitem__(self, key):
        if key < 3:
            return key
        raise IndexError

print list(Foo()) # => [0, 1, 2]
```

