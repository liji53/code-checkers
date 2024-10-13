
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

constexpr auto msgCheck = "using = in if/while/do/for statment";

auto createIfWhileMistakeByAssignRule() {
    // 检查 if / while / do..while 
    const std::string callExprS = "cexpr";
    return makeRule(
        traverse(
            clang::TK_IgnoreUnlessSpelledInSource,
            binaryOperation(hasOperatorName("="),
                anyOf(hasParent(whileStmt()), hasParent(ifStmt()), hasParent(doStmt())))
            .bind(callExprS)),
        noopEdit(node(callExprS)),
        cat(msgCheck));
}

auto createForMistakeByAssignRule() {
    // 检查for 
    const std::string callExprS = "cexpr";
    return makeRule(
        traverse(
            clang::TK_IgnoreUnlessSpelledInSource,
            forStmt(hasCondition(binaryOperation(hasOperatorName("=")).bind(callExprS)))),
        noopEdit(node(callExprS)),
        cat(msgCheck));
}

auto createConditionMistakeByAssignRule(){
    // 请实现
    return applyFirst(
        { createIfWhileMistakeByAssignRule(), createForMistakeByAssignRule() });

}


class ConditionMistakeByAssignCheck : public TransformerClangTidyCheck
{
public:
    ConditionMistakeByAssignCheck(StringRef Name, ClangTidyContext* Context) : 
        TransformerClangTidyCheck(createConditionMistakeByAssignRule(), Name, Context)
    {
    }
};

class ConditionMistakeByAssignCheckModule : public ClangTidyModule
{
public:
    void addCheckFactories(ClangTidyCheckFactories& CheckFactories) override
    {
        CheckFactories.registerCheck<ConditionMistakeByAssignCheck>("hs-conditionmistakebyassigncheck");
    }
};


namespace clang::tidy {
static ClangTidyModuleRegistry::Add<::ConditionMistakeByAssignCheckModule> ConditionMistakeByAssignCheckInit(
    "hs-conditionmistakebyassigncheck-module",
    "Adds 'hs-conditionmistakebyassigncheck' checks.");

// This anchor is used to force the linker to link in the generated object file and thus register the module.
volatile int ConditionMistakeByAssignCheckAnchorSource = 0;

}  // namespace clang::tidy
    