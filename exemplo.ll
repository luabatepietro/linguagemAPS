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
  @texto = global i8* null
  %ptr_0 = alloca [256 x i8]
  %gep_0 = getelementptr inbounds [256 x i8], [256 x i8]* %ptr_0, i32 0, i32 0
  %scan_0 = call i32 (i8*, ...) @scanf(i8* @.str_read_fmt, i8* %gep_0)
  %temp_0 = add i8* %gep_0, 0
  store i8* %temp_0, i8** @texto
  %3 = load i8*, i8** @texto
  %call_4 = call i32 (i8*, ...) @printf(i8* %3)
  ret i32 0
}
