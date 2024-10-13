# 用于生成checker代码模板
import os

checker_category = input("请输入检查器的类别: ")
checker_name = input("请输入检查器的名字(请使用下划线命名法，如abc_def): ")
target_name = ''.join([c[0].upper() + c[1:] for c in checker_name.split('_')])

project_path = os.path.dirname(__file__)
src_path = os.path.join(project_path, "src")
src_makefile = os.path.join(src_path, "CMakeLists.txt")
if not os.path.exists(src_makefile):
    print("error: src目录下不存在CMakeLists.txt！")
    exit(-1)
with open(src_makefile, 'a') as fd:
    fd.write(f"\nadd_subdirectory({checker_name})")

checker_path = os.path.join(src_path, checker_name)
os.mkdir(checker_path)
##
checker_makefile = os.path.join(checker_path, "CMakeLists.txt")
with open(checker_makefile, 'w') as fd:
    fd.write(f"""
        add_library({target_name} MODULE "")
        target_compile_options({target_name} PRIVATE -fno-rtti)
        target_include_directories({target_name}
            PRIVATE
                ${{CLANG_INCLUDE_DIRS}}
                ${{LLVM_INCLUDE_DIRS}}
        )
        target_sources({target_name} PRIVATE ${{CMAKE_CURRENT_LIST_DIR}}/{target_name}.cpp)
    """)
##
checker_file = os.path.join(checker_path, f"{target_name}.cpp")
with open(checker_file, 'w') as fd:
    fd.write(f"""
#include "clang-tidy/ClangTidyModule.h"
#include "clang-tidy/ClangTidyModuleRegistry.h"
#include "clang-tidy/utils/TransformerClangTidyCheck.h"
#include "clang/AST/ASTTypeTraits.h"
#include "clang/AST/Expr.h"
#include "clang/ASTMatchers/ASTMatchers.h"
#include "clang/Tooling/Transformer/RangeSelector.h"  // name
#include "clang/Tooling/Transformer/RewriteRule.h"    // makeRule
#include "clang/Tooling/Transformer/Stencil.h"        // cat

using namespace clang;
using namespace clang::tidy;
using namespace clang::ast_matchers;
using namespace clang::transformer;
using namespace clang::tidy::utils;

auto create{target_name}Rule(){{
    // 请实现
}}


class {target_name}Check : public TransformerClangTidyCheck
{{
public:
    {target_name}Check(StringRef Name, ClangTidyContext* Context) : 
        TransformerClangTidyCheck(create{target_name}Rule(), Name, Context)
    {{
    }}
}};

class {target_name}CheckModule : public ClangTidyModule
{{
public:
    void addCheckFactories(ClangTidyCheckFactories& CheckFactories) override
    {{
        CheckFactories.registerCheck<{target_name}Check>("{checker_category}-{target_name.lower()}check");
    }}
}};


namespace clang::tidy {{
static ClangTidyModuleRegistry::Add<::{target_name}CheckModule> {target_name}CheckInit(
    "{checker_category}-{target_name.lower()}check-module",
    "Adds '{checker_category}-{target_name.lower()}check' checks.");

// This anchor is used to force the linker to link in the generated object file and thus register the module.
volatile int {target_name}CheckAnchorSource = 0;

}}  // namespace clang::tidy
    """)
