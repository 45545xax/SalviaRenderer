set( SALVIA_LLVM_TEST_CASE_HEADERS "" )
set( SALVIA_LLVM_TEST_CASE_SOURCES	"" )

if( SALVIA_BUILD_WITH_LLVM )
	set( SALVIA_LLVM_TEST_CASE_HEADERS cgllvm_cases.h )
	set( SALVIA_LLVM_TEST_CASE_SOURCES	cgllvm_cases.cpp )
endif( SALVIA_BUILD_WITH_LLVM )