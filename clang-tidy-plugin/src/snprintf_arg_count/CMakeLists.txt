
        add_library(SnprintfArgCount MODULE "")
        target_compile_options(SnprintfArgCount PRIVATE -fno-rtti)
        target_include_directories(SnprintfArgCount
            PRIVATE
                ${CLANG_INCLUDE_DIRS}
                ${LLVM_INCLUDE_DIRS}
                ${CLANG_TIDY_INCLUDE_DIRS}
        )
        target_sources(SnprintfArgCount PRIVATE ${CMAKE_CURRENT_LIST_DIR}/SnprintfArgCount.cpp)
    