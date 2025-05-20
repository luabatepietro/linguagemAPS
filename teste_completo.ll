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
  @a = global i32 0
  %temp_0 = add i32 0, 10
  store i32 %temp_0, i32* @a
  @b = global i32 0
  %temp_3 = add i32 0, 20
  store i32 %temp_3, i32* @b
  @soma = global i32 0
  %6 = load i32, i32* @a
  %7 = load i32, i32* @b
  %temp_8 = add i32 %6, %7
  store i32 %temp_8, i32* @soma
  @texto = global i8* null
  %ptr_11 = alloca [256 x i8]
  %gep_11 = getelementptr inbounds [256 x i8], [256 x i8]* %ptr_11, i32 0, i32 0
  %scan_11 = call i32 (i8*, ...) @scanf(i8* @.str_read_fmt, i8* %gep_11)
  %temp_11 = add i8* %gep_11, 0
  store i8* %temp_11, i8** @texto
  @resultado = global i8* null
  %14 = load i8*, i8** @texto
  @.str_15 = private unnamed_addr constant [2 x i8] c"!\00"
  %temp_15 = getelementptr inbounds [2 x i8], [2 x i8]* @.str_15, i32 0, i32 0
  %malloc_16 = call i8* @malloc(i64 256)
  %strcat1_16 = call i8* @strcat(i8* %malloc_16, i8* %14)
  %strcat2_16 = call i8* @strcat(i8* %strcat1_16, i8* %temp_15)
  %temp_16 = bitcast i8* %strcat2_16 to i8*
  store i8* %temp_16, i8** @resultado
  %19 = load i8*, i8** @resultado
  %call_20 = call i32 (i8*, ...) @printf(i8* %19)
  @condicao = global i32 0
  %temp_21 = add i1 0, 1
  store i32 %temp_21, i32* @condicao
  %24 = load i32, i32* @condicao
  br i1 %temp_24, label %if_then_31, label %if_else_31
  if_then_31:
  @.str_25 = private unnamed_addr constant [24 x i8] c"Condição era verdadeira\00"
  %temp_25 = getelementptr inbounds [24 x i8], [24 x i8]* @.str_25, i32 0, i32 0
  %call_26 = call i32 (i8*, ...) @printf(i8* %temp_25)
  br label %if_end_31
  if_else_31:
  @.str_28 = private unnamed_addr constant [19 x i8] c"Condição era falsa\00"
  %temp_28 = getelementptr inbounds [19 x i8], [19 x i8]* @.str_28, i32 0, i32 0
  %call_29 = call i32 (i8*, ...) @printf(i8* %temp_28)
  br label %if_end_31
  if_end_31:
  @i = global i32 0
  %temp_32 = add i32 0, 0
  store i32 %temp_32, i32* @i
  br label %while_cond_46
  while_cond_46:
  %35 = load i32, i32* @i
  %temp_36 = add i32 0, 5
  %temp_37 = icmp slt i32 %35, %temp_36
  br i1 %temp_37, label %while_body_46, label %while_end_46
  while_body_46:
  %38 = load i32, i32* @i
  %call_39 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.int_print_fmt, i32 0, i32 0), i32 %38)
  %40 = load i32, i32* @i
  %temp_41 = add i32 0, 1
  %temp_42 = add i32 %40, %temp_41
  store i32 %temp_42, i32* @i
  br label %while_cond_46
  while_end_46:
  @verdade = global i32 0
  %temp_47 = add i1 0, 1
  store i32 %temp_47, i32* @verdade
  %50 = load i32, i32* @verdade
  %temp_51 = xor i1 %50, true
  %bool_ptr_52 = select i1 %temp_51, i8* @.true_str, i8* @.false_str
  %call_52 = call i32 (i8*, ...) @printf(i8* %bool_ptr_52)
  ret i32 0
}
