# Test 使用方法

```shell
$ python manage.py test tests
```

如果需要只测试 `test_user.py`

```shell
$ python manage.py test tests.test_user
```


## 测试编写方法

1.继承DataProvider, 提供初始数据
2.在TestCase类SetUp的时候, 创建TestClient变量, 该类封装了原始的Client。
3.使用self.testClient.do_request进行测试


## BUGs

SetUp的时候会反复创建变量，因此会触发create的UNIQUE KEY异常，目前使用try暴力跳过异常的语句。还需要考虑更好的解决方法