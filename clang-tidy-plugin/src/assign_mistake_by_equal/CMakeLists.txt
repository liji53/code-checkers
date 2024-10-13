add_library(AssignMistakeByEqual MODULE "")
target_compile_options(AssignMistakeByEqual PRIVATE -fno-rtti)
target_include_directories(AssignMistakeByEqual
    PRIVATE
        ${CLANG_INCLUDE_DIRS}
        ${LLVM_INCLUDE_DIRS}
)
target_sources(AssignMistakeByEqual PRIVATE ${CMAKE_CURRENT_LIST_DIR}/AssignMistakeByEqual.cpp)
