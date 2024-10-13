# clang-tidy plugins

参考资料：https://clang.llvm.org/docs/LibASTMatchersReference.html
https://github.com/coveooss/clang-tidy-plugin-examples.git

## 部署&使用

测试环境ubuntu
#### 安装clang-16
```shell
CC=clang-16 CXX=clang++-16 cmake -B build -G Ninja -S .
cmake --build build
```

#### 使用clang-tidy检查
1. 查看是否支持某个检查
    ```shell
    clang-tidy-16 \
            --checks='*' \
            --load build/lib/libAwesomePrefixCheck.so \
            --list-checks \
        | grep coveo-awesomeprefixcheck
    ```
1. 生成编译命令
    ```shell
    cmake -B buildTestedCpp -S tested_cpp \
        -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
    cmake --build buildTestedCpp
    ```
1. 指定检查器进行检查
    ```shell
    clang-tidy-16 \
        --checks='coveo-awesomeprefixcheck' \
        --load build/lib/libAwesomePrefixCheck.so \
        -p buildTestedCpp/compile_commands.json \
        tested_cpp/src/code.cpp
    ```
	
#### 开发一个checker
使用脚本来生成checker的代码模板
```shell
python createNewChecker.py
```
