

##### 启动服务
```
. venv/bin/activate
nohup python3 run.py &
```
##### 结束服务
```
kill -9 `ps -aux | grep "python3 run.py"  | grep -v grep  | awk '{print $2}'`
```