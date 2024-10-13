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
constexpr auto msgCheck = "= may be mistakely writen by ==";


auto createAssignMistakeByEqualRule()
{
    const std::string callExprS = "mistakeEqual";
    return makeRule(traverse(clang::TK_AsIs, binaryOperation(hasOperatorName("=="), hasParent(compoundStmt())).bind(callExprS)),
                    noopEdit(node(callExprS)),
                    cat(msgCheck));
}


class AssignMistakeByEqualCheck : public TransformerClangTidyCheck
{
public:
    AssignMistakeByEqualCheck(StringRef Name, ClangTidyContext* Context) : 
        TransformerClangTidyCheck(createAssignMistakeByEqualRule(), Name, Context)
    {
    }
};

class AssignMistakeByEqualCheckModule : public ClangTidyModule
{
public:
    void addCheckFactories(ClangTidyCheckFactories& CheckFactories) override
    {
        CheckFactories.registerCheck<AssignMistakeByEqualCheck>("hs-assignmistakebyequalcheck");
    }
};



namespace clang::tidy {

// Register the module using this statically initialized variable.
static ClangTidyModuleRegistry::Add<::AssignMistakeByEqualCheckModule> AssignMistakeByEqualCheckInit(
    "hs-assignmistakebyequalcheck-module",
    "Adds 'hs-assignmistakebyequalcheck' checks.");

// This anchor is used to force the linker to link in the generated object file and thus register the module.
volatile int AssignMistakeByEqualCheckAnchorSource = 0;

}  // namespace clang::tidy
