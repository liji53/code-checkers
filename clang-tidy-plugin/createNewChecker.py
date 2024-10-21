# 用于生成checker代码模板
import os

checker_category = input("请输入检查器的类别: ")
checker_name = input("请输入检查器的名字(请使用下划线命名法，如abc_def): ")
target_name = ''.join([c[0].upper() + c[1:] for c in checker_name.split('_')])
print("请选择实现的方法:")
print("1. clang static analyzer.")
print("2. clang ast rule.")
print("3. clang ast matcher.")
checker_type = input("输入选项数字：")

while checker_type not in ['1', '2', '3']:
    print("输入错误，请重新输入选项数字。")
    checker_type = input("输入选项数字：")

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
        {"${CLANG_TIDY_INCLUDE_DIRS}" if checker_type != '1' else "" }
)
target_sources({target_name} PRIVATE ${{CMAKE_CURRENT_LIST_DIR}}/{target_name}.cpp)
    """)
##
if checker_type == '1':
    code = f"""
#include "clang/StaticAnalyzer/Core/BugReporter/BugType.h"
#include "clang/StaticAnalyzer/Core/Checker.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/CallEvent.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/CallDescription.h"
#include "clang/StaticAnalyzer/Core/PathSensitive/CheckerContext.h"
#include "clang/StaticAnalyzer/Frontend/CheckerRegistry.h"
#include <utility>

constexpr const char* CHECKER_PLUGIN_NAME = "{checker_category}.{target_name}";
constexpr const char* CHECKER_PLUGIN_DOCS_URI = "nonexistent";

using namespace clang;
using namespace ento;



class {target_name}Checker : public Checker<check::PostCall, check::PreCall>
{{
public:
    {target_name}Checker(){{}}
    
    void checkPostCall(const CallEvent& Call, CheckerContext& C) const
    {{
        // todo
    }}

    void checkPreCall(const CallEvent& Call, CheckerContext& C) const
    {{
        // todo 
    }}
}};

// See clang/StaticAnalyzer/Core/CheckerRegistry.h for details on  creating
// plugins for the clang static analyzer. The requirements are that each
// plugin include the version string and registry function below. The checker
// should then be usable with:
//
//   clang -cc1 -load </path/to/plugin> -analyze \
//     -analyzer-checker=<prefix.checkername>
//
// You can double check that it is working/found by listing the available
// checkers with the -analyzer-checker-help option.

extern "C" __attribute__((visibility("default"))) const char clang_analyzerAPIVersionString[] = CLANG_ANALYZER_API_VERSION_STRING;

extern "C" __attribute__((visibility("default"))) void clang_registerCheckers(CheckerRegistry & registry)
{{
    registry.addChecker<{target_name}Checker>(CHECKER_PLUGIN_NAME, "Invokes the {target_name}Checker", CHECKER_PLUGIN_DOCS_URI);
}}
    """
elif checker_type == '2':
    code = f"""
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
    """
else:
    code = f"""
#include "clang/AST/ASTContext.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang-tidy/ClangTidy.h"
#include "clang-tidy/ClangTidyCheck.h"
#include "clang-tidy/ClangTidyModule.h"
#include "clang-tidy/ClangTidyModuleRegistry.h"

using namespace clang;
using namespace clang::tidy;
using namespace clang::ast_matchers;

class {target_name}Check : public ClangTidyCheck
{{
public:
    {target_name}Check(StringRef Name, ClangTidyContext* Context) : ClangTidyCheck(Name, Context)
    {{
    }}
    void registerMatchers(ast_matchers::MatchFinder* Finder) override;
    void check(const ast_matchers::MatchFinder::MatchResult& Result) override;
}};

void {target_name}Check::registerMatchers(MatchFinder* Finder)
{{
    // todo
    // Finder->addMatcher(functionDecl().bind("add_awesome_prefix"), this);
}}

void {target_name}Check::check(const MatchFinder::MatchResult& Result)
{{
    // todo    
}}

namespace {{

class {target_name}CheckModule : public ClangTidyModule
{{
public:
    void addCheckFactories(ClangTidyCheckFactories& CheckFactories) override
    {{
        CheckFactories.registerCheck<{target_name}Check>("{checker_category}-{target_name.lower()}check");
    }}
}};
}}  // namespace

namespace clang::tidy {{

// Register the module using this statically initialized variable.
static ClangTidyModuleRegistry::Add<::{target_name}CheckModule> {target_name}CheckInit("{checker_category}-{target_name.lower()}check-module",
                                                                                       "Adds '{checker_category}-{target_name.lower()}check' checks.");
// This anchor is used to force the linker to link in the generated object file and thus register the module.
volatile int {target_name}CheckAnchorSource = 0;

}}  // namespace clang::tidy

"""

checker_file = os.path.join(checker_path, f"{target_name}.cpp")
with open(checker_file, 'w') as fd:
    fd.write(code)

test_sh_file = os.path.join(checker_path, "test.sh")
with open(test_sh_file, 'w') as fd:
    fd.write(f"""
#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail
if [[ "${{TRACE-0}}" == "1" ]]; then
    set -o xtrace
fi

buildDirectory=${{1-build}}
updateExpected=${{2-0}}

SCRIPT_DIRECTORY="$(cd "$(dirname "$0")"; pwd -P)"
source "$SCRIPT_DIRECTORY/../../testFramework.sh"

testClangTidyReplacement \\
    "$buildDirectory" \\
    "$updateExpected" \\
    "$SCRIPT_DIRECTORY/Test{target_name}.cpp" \\
    "$SCRIPT_DIRECTORY/Expected{target_name}.cpp" \\
    "{checker_category}-{target_name.lower()}check" \\
    "lib{target_name}.so"
    """)

with open(os.path.join(checker_path, f'Test{target_name}.cpp'), 'w'):
    pass

with open(os.path.join(checker_path, f'Expected{target_name}.cpp'), 'w'):
    pass
