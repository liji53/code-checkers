
        add_library(ConditionMistakeByAssign MODULE "")
        target_compile_options(ConditionMistakeByAssign PRIVATE -fno-rtti)
        target_include_directories(ConditionMistakeByAssign
            PRIVATE
                ${CLANG_INCLUDE_DIRS}
                ${LLVM_INCLUDE_DIRS}
                ${CLANG_TIDY_INCLUDE_DIRS}
        )
        target_sources(ConditionMistakeByAssign PRIVATE ${CMAKE_CURRENT_LIST_DIR}/ConditionMistakeByAssign.cpp)
    