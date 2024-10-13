#include "clang/AST/ASTContext.h"
#include "clang/ASTMatchers/ASTMatchFinder.h"
#include "clang-tidy/ClangTidy.h"
#include "clang-tidy/ClangTidyCheck.h"
#include "clang-tidy/ClangTidyModule.h"
#include "clang-tidy/ClangTidyModuleRegistry.h"

using namespace clang;
using namespace clang::tidy;
using namespace clang::ast_matchers;


class SnprintfArgCountCheck : public ClangTidyCheck
{
public:
    SnprintfArgCountCheck(StringRef Name, ClangTidyContext* Context) : ClangTidyCheck( Name, Context)
    {
    }
    void registerMatchers(ast_matchers::MatchFinder* Finder) override;
    void check(const ast_matchers::MatchFinder::MatchResult& Result) override;
};
void SnprintfArgCountCheck::registerMatchers(MatchFinder* Finder)
{
    Finder->addMatcher(callExpr(callee(functionDecl(hasName("snprintf"))), hasArgument(2, stringLiteral())).bind("snprintf"), this);
}

// 统计占位符个数
int countPlaceholders(const llvm::StringRef& str)
{
    int count = 0;
    for (int i = 0; i < str.size(); ++i) {
        if (str[i] == '%' && ++i < str.size() && str[i] != '%')
            count++;
    }
    return count;
}

void SnprintfArgCountCheck::check(const MatchFinder::MatchResult& Result)
{
       
    const auto* MatchedNode = Result.Nodes.getNodeAs<CallExpr>("snprintf");
    auto count = MatchedNode->getNumArgs();
    auto* expr = dyn_cast<StringLiteral>(MatchedNode->getArg(2)->IgnoreImplicit());
    //MatchedNode->getArg(2)->dump();
    if (expr) {
        auto str = expr->getString();
        if (countPlaceholders(str) != count - 3) {
            diag(MatchedNode->getBeginLoc(), "the argument count of snprintf is error...");
        }
    }
}


class SnprintfArgCountCheckModule : public ClangTidyModule
{
public:
    void addCheckFactories(ClangTidyCheckFactories& CheckFactories) override
    {
        CheckFactories.registerCheck<SnprintfArgCountCheck>("hs-snprintfargcountcheck");
    }
};


namespace clang::tidy {
static ClangTidyModuleRegistry::Add<::SnprintfArgCountCheckModule> SnprintfArgCountCheckInit(
    "hs-snprintfargcountcheck-module",
    "Adds 'hs-snprintfargcountcheck' checks.");

// This anchor is used to force the linker to link in the generated object file and thus register the module.
volatile int SnprintfArgCountCheckAnchorSource = 0;

}  // namespace clang::tidy
    