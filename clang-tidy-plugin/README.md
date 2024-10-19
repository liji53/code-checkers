# clang-tidy plugins

参考资料：https://clang.llvm.org/docs/LibASTMatchersReference.html

https://github.com/coveooss/clang-tidy-plugin-examples.git

### 部署
```
cd clang-tidy-plugin/
```
##### 安装clang
```
chmod +x installClang16.sh
./installClang16.sh
```
##### 编译插件库
```shell
CC=clang-16 CXX=clang++-16 cmake -B build -G Ninja -S .
cmake --build build
```

### 使用

##### 查看是否支持某个检查
```shell
clang-tidy-16 \
		--checks='*' \
		--load build/lib/libAwesomePrefixCheck.so \
		--list-checks \
	| grep coveo-awesomeprefixcheck
```
##### 生成编译命令
```shell
cmake -B buildTestedCpp -S tested_cpp \
	-DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build buildTestedCpp
```
##### 指定检查器进行检查
```shell
clang-tidy-16 \
	--checks='coveo-awesomeprefixcheck' \
	--load build/lib/libAwesomePrefixCheck.so \
	-p buildTestedCpp/compile_commands.json \
	tested_cpp/src/code.cpp
```

### 开发

##### 开发一个新的checker
使用脚本来生成checker的代码模板
```shell
python createNewChecker.py
```

### 测试

##### 编写被测试的代码
在src/[检查器]目录下编写该检查器需要检查的异常代码(TestXXX.cpp)和期望代码(ExpectedXXX.cpp) 

##### 执行全部测试
```
chmod +x testAll.sh
./testAll.sh
```
