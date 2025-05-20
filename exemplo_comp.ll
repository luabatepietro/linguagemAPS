; === LLVM IR Module ===
@.int_print_fmt = private unnamed_addr constant [4 x i8] c"%d\0A\00"
@.str_read_fmt = private unnamed_addr constant [3 x i8] c"%s\00"
@.int_read_fmt = private unnamed_addr constant [3 x i8] c"%d\00"
@.true_str = private constant [5 x i8] c"true\00"
@.false_str = private constant [6 x i8] c"false\00"
declare i32 @printf(i8*, ...)
declare i32 @scanf(i8*, ...)
declare i8* @malloc(i64)
declare i8* @strcpy(i8*, i8*)
declare i8* @strcat(i8*, i8*)
define i32 @main() {
  ret i32 0
}
