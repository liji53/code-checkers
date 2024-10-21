add_library(FileForgetClose MODULE "")
target_compile_options(FileForgetClose PRIVATE -fno-rtti)
target_include_directories(FileForgetClose
    PRIVATE
        ${CLANG_INCLUDE_DIRS}
        ${LLVM_INCLUDE_DIRS}
)
target_sources(FileForgetClose PRIVATE ${CMAKE_CURRENT_LIST_DIR}/FileForgetClose.cpp)
