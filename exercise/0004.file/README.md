## 关于文件和文件系统的操作

#### 创建指定大小的文件

```
with open(filename, 'w') as f:
    f.seek(2 ** 10)  # 1GB
    f.write(chr(0))
```
