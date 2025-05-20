import sys
import os
import re

# === Code: responsável por armazenar e gerar LLVM IR ===
class Code:
    def __init__(self):
        self.instructions = []

    def append(self, instruction):
        if isinstance(instruction, list):
            self.instructions.extend(instruction)
        else:
            self.instructions.append(instruction)

    def dump(self, input_filename="output.mit"):
        output_name = os.path.splitext(input_filename)[0] + ".ll"

        with open(output_name, "w") as f:
            f.write("; === LLVM IR Module ===\n")
            f.write('@.int_print_fmt = private unnamed_addr constant [4 x i8] c"%d\\0A\\00"\n')
            f.write('@.str_read_fmt = private unnamed_addr constant [3 x i8] c"%s\\00"\n')
            f.write('@.int_read_fmt = private unnamed_addr constant [3 x i8] c"%d\\00"\n')
            f.write('@.true_str = private constant [5 x i8] c"true\\00"\n')
            f.write('@.false_str = private constant [6 x i8] c"false\\00"\n')
            f.write('declare i32 @printf(i8*, ...)\n')
            f.write('declare i32 @scanf(i8*, ...)\n')
            f.write('declare i8* @malloc(i64)\n')
            f.write('declare i8* @strcpy(i8*, i8*)\n')
            f.write('declare i8* @strcat(i8*, i8*)\n')
            f.write('define i32 @main() {\n')

            for instr in self.instructions:
                f.write("  " + instr + "\n")

            f.write("  ret i32 0\n")
            f.write("}\n")


# === SymbolTable: armazena declarações e valores ===
class SymbolTable:
    def __init__(self):
        self.table = {}

    def declare(self, name, type_):
        if name in self.table:
            raise Exception(f"Variável '{name}' já declarada.")
        self.table[name] = {"type": type_, "value": None}

    def set(self, name, value):
        if name not in self.table:
            raise Exception(f"Variável '{name}' não declarada.")
        self.table[name]["value"] = value

    def get(self, name):
        if name not in self.table:
            raise Exception(f"Variável '{name}' não declarada.")
        return self.table[name]["value"]

    def get_type(self, name):
        if name not in self.table:
            raise Exception(f"Variável '{name}' não declarada.")
        return self.table[name]["type"]


# === Base para todos os nós da AST ===
class Node:
    current_id = 0

    def __init__(self, value=None, children=None):
        self.value = value
        self.children = children or []
        self.id = Node.current_id
        Node.current_id += 1

    def Evaluate(self, symbol_table):
        raise NotImplementedError

    def Generate(self, symbol_table):
        raise NotImplementedError

# === IntVal: representa valores inteiros ===
class IntVal(Node):
    def Evaluate(self, symbol_table):
        return self.value, "poder"

    def Generate(self, symbol_table):
        temp = f"%int_{self.id}"
        return [f"{temp} = add i32 0, {self.value}"]


# === BoolVal: representa verdadeiro/falso ===
class BoolVal(Node):
    def Evaluate(self, symbol_table):
        val = 1 if self.value == "verdadeiro" else 0
        return val, "destino"

    def Generate(self, symbol_table):
        temp = f"%bool_{self.id}"
        val = "1" if self.value == "verdadeiro" else "0"
        return [f"{temp} = icmp eq i1 {val}, 1"]


# === StrVal: representa texto ===
class StrVal(Node):
    def Evaluate(self, symbol_table):
        return self.value, "palavra"

    def Generate(self, symbol_table):
        temp = f"%str_{self.id}"
        string_constant = f"@.str_{self.id}"
        length = len(self.value) + 1
        code = [
            f'{string_constant} = private unnamed_addr constant [{length} x i8] c"{self.value}\\00"',
            f'{temp} = getelementptr inbounds [{length} x i8], [{length} x i8]* {string_constant}, i32 0, i32 0'
        ]
        return code


# === Identifier: acesso a variáveis já declaradas ===
class Identifier(Node):
    def Evaluate(self, symbol_table):
        return symbol_table.get(self.value), symbol_table.get_type(self.value)

    def Generate(self, symbol_table):
        var_type = symbol_table.get_type(self.value)
        temp = f"%{self.id}"
        if var_type in ["poder", "destino"]:
            return [f"{temp} = load i32, i32* @{self.value}"]
        elif var_type == "palavra":
            return [f"{temp} = load i8*, i8** @{self.value}"]
        else:
            raise Exception(f"Tipo não suportado: {var_type}")



# === VarDec: invocar ... como ... com ... ===
class VarDec(Node):
    def Evaluate(self, symbol_table):
        name = self.children[0].value
        type_ = self.children[1]
        expr = self.children[2] if len(self.children) > 2 else None

        symbol_table.declare(name, type_)
        if expr:
            value, vtype = expr.Evaluate(symbol_table)
            if vtype != type_:
                raise Exception(f"Tipo incompatível em {name}: esperado {type_}, recebido {vtype}")
            symbol_table.set(name, value)
            return value, type_
        return None, type_

    def Generate(self, symbol_table):
        name = self.children[0].value
        type_ = self.children[1]
        expr = self.children[2] if len(self.children) > 2 else None
        code = []

        if type_ == "poder" or type_ == "destino":
            code.append(f"@{name} = global i32 0")
        elif type_ == "palavra":
            code.append(f"@{name} = global i8* null")
        else:
            raise Exception(f"Tipo inválido: {type_}")

        symbol_table.declare(name, type_)

        if expr:
            # Define tipo esperado para leitura
            symbol_table.expecting_type = type_

            expr_code = expr.Generate(symbol_table)
            code.extend(expr_code)

            symbol_table.expecting_type = None

            temp = f"%{expr.id}" if isinstance(expr, Identifier) else f"%temp_{expr.id}"
            if type_ == "palavra":
                code.append(f"store i8* {temp}, i8** @{name}")
            else:
                code.append(f"store i32 {temp}, i32* @{name}")
            symbol_table.set(name, "init")

        return code



# === Assignment: nome recebe expressao ===
class Assignment(Node):
    def Evaluate(self, symbol_table):
        name = self.children[0].value
        expr = self.children[1]
        value, vtype = expr.Evaluate(symbol_table)

        expected_type = symbol_table.get_type(name)
        if vtype != expected_type:
            raise Exception(f"Tipo incompatível em atribuição: variável '{name}' espera '{expected_type}', mas recebeu '{vtype}'")

        symbol_table.set(name, value)
        return value, vtype

    def Generate(self, symbol_table):
        name = self.children[0].value
        expr = self.children[1]
        var_type = symbol_table.get_type(name)

        symbol_table.expecting_type = var_type
        expr_code = expr.Generate(symbol_table)
        symbol_table.expecting_type = None

        code = expr_code
        temp = f"%{expr.id}" if isinstance(expr, Identifier) else f"%temp_{expr.id}"

        if var_type == "palavra":
            code.append(f"store i8* {temp}, i8** @{name}")
        else:
            code.append(f"store i32 {temp}, i32* @{name}")

        symbol_table.set(name, "init")
        return code


# === BinOp: operações binárias ===
class BinOp(Node):
    def Evaluate(self, symbol_table):
        left_val, left_type = self.children[0].Evaluate(symbol_table)
        right_val, right_type = self.children[1].Evaluate(symbol_table)

        if self.value in ["unir", "separar", "fortificar", "enfraquecer"]:
            if left_type != "poder" or right_type != "poder":
                raise Exception("Operações aritméticas requerem tipo 'poder'")
            if self.value == "unir":
                return left_val + right_val, "poder"
            elif self.value == "separar":
                return left_val - right_val, "poder"
            elif self.value == "fortificar":
                return left_val * right_val, "poder"
            elif self.value == "enfraquecer":
                return left_val // right_val, "poder"

        elif self.value in ["supera", "cede", "igual", "diferente"]:
            if left_type != right_type:
                raise Exception("Comparação requer operandos do mesmo tipo")
            if self.value == "supera":
                return int(left_val > right_val), "destino"
            elif self.value == "cede":
                return int(left_val < right_val), "destino"
            elif self.value == "igual":
                return int(left_val == right_val), "destino"
            elif self.value == "diferente":
                return int(left_val != right_val), "destino"

        elif self.value in ["e", "ou"]:
            if left_type != "destino" or right_type != "destino":
                raise Exception("Lógicos requerem 'destino'")
            if self.value == "e":
                return int(left_val and right_val), "destino"
            elif self.value == "ou":
                return int(left_val or right_val), "destino"

        elif self.value == "concatena":
            return str(left_val) + str(right_val), "palavra"

        else:
            raise Exception(f"Operador inválido: {self.value}")

    def Generate(self, symbol_table):
        code = []
        code += self.children[0].Generate(symbol_table)
        code += self.children[1].Generate(symbol_table)

        left_temp = f"%{self.children[0].id}" if isinstance(self.children[0], Identifier) else f"%temp_{self.children[0].id}"
        right_temp = f"%{self.children[1].id}" if isinstance(self.children[1], Identifier) else f"%temp_{self.children[1].id}"
        result = f"%temp_{self.id}"

        if self.value == "unir":
            code.append(f"{result} = add i32 {left_temp}, {right_temp}")
        elif self.value == "separar":
            code.append(f"{result} = sub i32 {left_temp}, {right_temp}")
        elif self.value == "fortificar":
            code.append(f"{result} = mul i32 {left_temp}, {right_temp}")
        elif self.value == "enfraquecer":
            code.append(f"{result} = sdiv i32 {left_temp}, {right_temp}")
        elif self.value == "supera":
            code.append(f"{result} = icmp sgt i32 {left_temp}, {right_temp}")
        elif self.value == "cede":
            code.append(f"{result} = icmp slt i32 {left_temp}, {right_temp}")
        elif self.value == "igual":
            code.append(f"{result} = icmp eq i32 {left_temp}, {right_temp}")
        elif self.value == "diferente":
            code.append(f"{result} = icmp ne i32 {left_temp}, {right_temp}")
        elif self.value == "e":
            code.append(f"{result} = and i1 {left_temp}, {right_temp}")
        elif self.value == "ou":
            code.append(f"{result} = or i1 {left_temp}, {right_temp}")
        elif self.value == "concatena":
            malloc_var = f"%malloc_{self.id}"
            strcat1 = f"%strcat1_{self.id}"
            strcat2 = f"%strcat2_{self.id}"
            code.append(f"{malloc_var} = call i8* @malloc(i64 256)")
            code.append(f"{strcat1} = call i8* @strcat(i8* {malloc_var}, i8* {left_temp})")
            code.append(f"{strcat2} = call i8* @strcat(i8* {strcat1}, i8* {right_temp})")
            code.append(f"{result} = bitcast i8* {strcat2} to i8*")
        else:
            raise Exception(f"Operador binário desconhecido: {self.value}")

        return code


# === UnOp: operadores unários (+, -, nao) ===
class UnOp(Node):
    def Evaluate(self, symbol_table):
        value, vtype = self.children[0].Evaluate(symbol_table)
        if self.value == "nao":
            if vtype != "destino":
                raise Exception("nao requer destino")
            return int(not value), "destino"
        elif self.value == "mais":
            return +value, vtype
        elif self.value == "menos":
            return -value, vtype
        else:
            raise Exception("Operador unário inválido")

    def Generate(self, symbol_table):
        code = self.children[0].Generate(symbol_table)
        operand = f"%{self.children[0].id}" if isinstance(self.children[0], Identifier) else f"%temp_{self.children[0].id}"
        result = f"%temp_{self.id}"

        if self.value == "nao":
            code.append(f"{result} = xor i1 {operand}, true")
        elif self.value == "mais":
            code.append(f"{result} = add i32 0, {operand}")
        elif self.value == "menos":
            code.append(f"{result} = sub i32 0, {operand}")
        else:
            raise Exception("Operador unário desconhecido")

        return code

# === Print: proclamar(expr) ===
class Print(Node):
    def Evaluate(self, symbol_table):
        if not self.children or len(self.children) != 1:
            print(f"[ERRO DEBUG] Print.children = {self.children}")
            raise Exception("Print sem filhos ou com número inválido de filhos!")
        val, vtype = self.children[0].Evaluate(symbol_table)
        print(val if vtype != "destino" else ("verdadeiro" if val else "falso"))
        return val, vtype

    def Generate(self, symbol_table):
        code = self.children[0].Generate(symbol_table)
        result = f"%{self.children[0].id}" if isinstance(self.children[0], Identifier) else f"%temp_{self.children[0].id}"
        call = f"%call_{self.id}"
        vtype = symbol_table.get_type(self.children[0].value) if isinstance(self.children[0], Identifier) else self.children[0].Evaluate(symbol_table)[1]

        if vtype == "poder":
            code.append(f"{call} = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([4 x i8], [4 x i8]* @.int_print_fmt, i32 0, i32 0), i32 {result})")
        elif vtype == "destino":
            ptr = f"%bool_ptr_{self.id}"
            code.append(f"{ptr} = select i1 {result}, i8* @.true_str, i8* @.false_str")
            code.append(f"{call} = call i32 (i8*, ...) @printf(i8* {ptr})")
        elif vtype == "palavra":
            code.append(f"{call} = call i32 (i8*, ...) @printf(i8* {result})")
        else:
            raise Exception(f"Tipo inválido em proclamar: {vtype}")
        return code


# === Read: consultar_oraculo() ===
class Read(Node):
    def Evaluate(self, symbol_table):
        raw = input()
        if raw.isdigit():
            return int(raw), "poder"
        elif raw.lower() in ["verdadeiro", "falso"]:
            return int(raw.lower() == "verdadeiro"), "destino"
        else:
            return raw, "palavra"

    def Generate(self, symbol_table):
        result = f"%temp_{self.id}"
        ptr = f"%ptr_{self.id}"
        code = []

        expected = getattr(symbol_table, "expecting_type", "palavra")

        if expected == "poder":
            code += [
                f"{ptr} = alloca i32",
                f"%scan_{self.id} = call i32 (i8*, ...) @scanf(i8* @.int_read_fmt, i32* {ptr})",
                f"{result} = load i32, i32* {ptr}"
            ]
        elif expected == "palavra":
            code += [
                f"{ptr} = alloca [256 x i8]",
                f"%gep_{self.id} = getelementptr inbounds [256 x i8], [256 x i8]* {ptr}, i32 0, i32 0",
                f"%scan_{self.id} = call i32 (i8*, ...) @scanf(i8* @.str_read_fmt, i8* %gep_{self.id})",
                f"{result} = add i8* %gep_{self.id}, 0"
            ]
        else:
            raise Exception("Tipo não suportado em consultar_oraculo")
        return code



# === If: se (...) { ... } senao { ... } ===
class If(Node):
    def Evaluate(self, symbol_table):
        cond, t = self.children[0].Evaluate(symbol_table)
        if t != "destino":
            raise Exception("Condição de se deve ser destino")
        if cond:
            return self.children[1].Evaluate(symbol_table)
        elif len(self.children) > 2:
            return self.children[2].Evaluate(symbol_table)
        return None, None

    def Generate(self, symbol_table):
        code = self.children[0].Generate(symbol_table)
        cond = f"%temp_{self.children[0].id}"
        then_label = f"if_then_{self.id}"
        else_label = f"if_else_{self.id}"
        end_label = f"if_end_{self.id}"

        if len(self.children) == 3:
            code.append(f"br i1 {cond}, label %{then_label}, label %{else_label}")
            code.append(f"{then_label}:")
            code += self.children[1].Generate(symbol_table)
            code.append(f"br label %{end_label}")
            code.append(f"{else_label}:")
            code += self.children[2].Generate(symbol_table)
            code.append(f"br label %{end_label}")
        else:
            code.append(f"br i1 {cond}, label %{then_label}, label %{end_label}")
            code.append(f"{then_label}:")
            code += self.children[1].Generate(symbol_table)
            code.append(f"br label %{end_label}")
        code.append(f"{end_label}:")
        return code


# === While: enquanto (...) { ... } ===
class While(Node):
    def Evaluate(self, symbol_table):
        val, typ = self.children[0].Evaluate(symbol_table)
        while val:
            self.children[1].Evaluate(symbol_table)
            val, _ = self.children[0].Evaluate(symbol_table)
        return None, None

    def Generate(self, symbol_table):
        code = []
        cond_label = f"while_cond_{self.id}"
        body_label = f"while_body_{self.id}"
        end_label = f"while_end_{self.id}"

        code.append(f"br label %{cond_label}")
        code.append(f"{cond_label}:")
        code += self.children[0].Generate(symbol_table)
        cond = f"%temp_{self.children[0].id}"
        code.append(f"br i1 {cond}, label %{body_label}, label %{end_label}")
        code.append(f"{body_label}:")
        code += self.children[1].Generate(symbol_table)
        code.append(f"br label %{cond_label}")
        code.append(f"{end_label}:")
        return code


# === Block: conjunto de comandos ===
class Block(Node):
    def __init__(self, children):
        super().__init__(None, children)

    def Evaluate(self, symbol_table):
        print(f"[DEBUG] Block.Evaluate com {len(self.children)} filhos")
        for child in self.children:
            print(f"[DEBUG] Avaliando filho: {type(child).__name__}")
            child.Evaluate(symbol_table)
        return None, None


    def Generate(self, symbol_table):
        code = []
        if not self.children:
            print("[DEBUG] Block sem filhos!")
        else:
            print(f"[DEBUG] Block com {len(self.children)} filhos")
            for child in self.children:
                print(f"[DEBUG] Gerando código para: {type(child).__name__}")
                generated = child.Generate(symbol_table)
                if generated:
                    code += generated
        return code




# === NoOp: instrução vazia ===
class NoOp(Node):
    def Evaluate(self, symbol_table):
        return None, None

    def Generate(self, symbol_table):
        return []

# === Token: representa tipo e valor ===
class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value


# === Tokenizer: quebra o código fonte em tokens ===
class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.keywords = {
            "invocar": "INVOCAR",
            "como": "COMO",
            "com": "COM",
            "proclamar": "PROCLAMAR",
            "recebe": "RECEBE",
            "se": "SE",
            "senao": "SENAO",
            "enquanto": "ENQUANTO",
            "consultar_oraculo": "CONSULTAR",
            "poder": "TIPO",
            "palavra": "TIPO",
            "destino": "TIPO",
            "supera": "OP",
            "cede": "OP",
            "igual": "OP",
            "diferente": "OP",
            "unir": "OP",
            "separar": "OP",
            "fortificar": "OP",
            "enfraquecer": "OP",
            "e": "OP",
            "ou": "OP",
            "nao": "OP",
            "verdadeiro": "BOOL",
            "falso": "BOOL"
        }
        self.select_next()  # ✅ Isso precisa estar aqui


    def select_next(self):
        while self.position < len(self.source) and self.source[self.position] in " \n\t\r":
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF", None)
            return

        char = self.source[self.position]

        if char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token("NUM", int(num))

        elif char == '"':
            self.position += 1
            text = ""
            while self.source[self.position] != '"':
                text += self.source[self.position]
                self.position += 1
            self.position += 1
            self.next = Token("STR", text)

        elif char.isalpha():
            word = ""
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == "_"):
                word += self.source[self.position]
                self.position += 1
            self.next = Token(self.keywords.get(word, "ID"), word)

        elif char == "(":
            self.position += 1
            self.next = Token("LPAREN", "(")
        elif char == ")":
            self.position += 1
            self.next = Token("RPAREN", ")")
        elif char == "{":
            self.position += 1
            self.next = Token("LBRACE", "{")
        elif char == "}":
            self.position += 1
            self.next = Token("RBRACE", "}")
        elif char == ";":
            self.position += 1
            self.next = Token("SEMI", ";")
        else:
            raise Exception(f"Caractere inesperado: {char}")


# === Parser: monta a árvore sintática (AST) ===
class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse_factor(self):
        token = self.tokenizer.next
        if token.type == "NUM":
            self.tokenizer.select_next()
            return IntVal(token.value)
        elif token.type == "STR":
            self.tokenizer.select_next()
            return StrVal(token.value)
        elif token.type == "BOOL":
            self.tokenizer.select_next()
            return BoolVal(token.value)
        elif token.type == "ID":
            self.tokenizer.select_next()
            return Identifier(token.value)
        elif token.type == "CONSULTAR":
            self.tokenizer.select_next()
            self.expect("LPAREN")
            self.expect("RPAREN")
            return Read()
        elif token.type == "OP" and token.value in ["mais", "menos", "nao"]:
            op = token.value
            self.tokenizer.select_next()
            return UnOp(op, self.parse_factor())
        elif token.type == "LPAREN":
            self.tokenizer.select_next()
            expr = self.parse_expression()
            self.expect("RPAREN")
            return expr
        else:
            raise Exception("Fator inválido")

    def parse_term(self):
        node = self.parse_factor()
        while self.tokenizer.next.value in ["fortificar", "enfraquecer"]:
            op = self.tokenizer.next.value
            self.tokenizer.select_next()
            node = BinOp(op, [node, self.parse_factor()])
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.tokenizer.next.value in ["unir", "separar", "concatena"]:
            op = self.tokenizer.next.value
            self.tokenizer.select_next()
            node = BinOp(op, [node, self.parse_term()])
        return node

    def parse_relational(self):
        node = self.parse_expression()
        while self.tokenizer.next.value in ["supera", "cede", "igual", "diferente"]:
            op = self.tokenizer.next.value
            self.tokenizer.select_next()
            node = BinOp(op, [node, self.parse_expression()])
        return node

    def parse_logic(self):
        node = self.parse_relational()
        while self.tokenizer.next.value in ["e", "ou"]:
            op = self.tokenizer.next.value
            self.tokenizer.select_next()
            node = BinOp(op, [node, self.parse_relational()])
        return node

    def parse_statement(self):
        token = self.tokenizer.next
        if token.type == "INVOCAR":
            self.tokenizer.select_next()
            name = self.tokenizer.next.value
            self.expect("ID")
            self.expect("COMO")
            tipo = self.tokenizer.next.value
            self.expect("TIPO")
            self.expect("COM")
            expr = self.parse_logic()
            self.expect("SEMI")
            return VarDec([Identifier(name), tipo, expr])
        elif token.type == "ID":
            name = token.value
            self.tokenizer.select_next()
            self.expect("RECEBE")
            expr = self.parse_logic()
            self.expect("SEMI")
            return Assignment([Identifier(name), expr])

        elif token.type == "PROCLAMAR":
            self.tokenizer.select_next()
            self.expect("LPAREN")
            
            if self.tokenizer.next.type in ["SEMI", "RPAREN"]:
                raise Exception("Erro de sintaxe: proclamar() sem expressão")

            expr = self.parse_logic()
            self.expect("RPAREN")
            self.expect("SEMI")

            if expr is None:
                raise Exception("Erro: expressão de proclamar retornou None!")
            return Print([expr])

        elif token.type == "SE":
            self.tokenizer.select_next()
            self.expect("LPAREN")
            cond = self.parse_logic()
            self.expect("RPAREN")
            true_block = self.parse_block()
            if self.tokenizer.next.type == "SENAO":
                self.tokenizer.select_next()
                false_block = self.parse_block()
                return If([cond, true_block, false_block])
            return If([cond, true_block])
        elif token.type == "ENQUANTO":
            self.tokenizer.select_next()
            self.expect("LPAREN")
            cond = self.parse_logic()
            self.expect("RPAREN")
            body = self.parse_block()
            return While([cond, body])
        else:
            return NoOp()

    def parse_block(self):
        self.expect("LBRACE")
        statements = []
        while self.tokenizer.next.type not in ["RBRACE", "EOF"]:
            print(f"[DEBUG] Parsing statement with token: {self.tokenizer.next.type}")
            stmt = self.parse_statement()
            print(f"[DEBUG] Nó retornado por parse_statement: {type(stmt).__name__}")
            if not isinstance(stmt, NoOp):
                statements.append(stmt)
        self.expect("RBRACE")
        print(f"[DEBUG] Total de statements neste bloco: {len(statements)}")
        return Block(statements)

    def parse(self):
        if self.tokenizer.next.type == "LBRACE":
            block = self.parse_block()
        else:
            statements = []
            while self.tokenizer.next.type != "EOF":
                stmt = self.parse_statement()
                if not isinstance(stmt, NoOp):
                    statements.append(stmt)
            block = Block(statements)

        # Consome tokens residuais (ex: espaços, tabs após } )
        while self.tokenizer.next.type == "SEMI":
            self.tokenizer.select_next()
        if self.tokenizer.next.type != "EOF":
            raise Exception(f"Token inesperado após fim do programa: {self.tokenizer.next.type}")

        return block



    def expect(self, type_):
        if self.tokenizer.next.type != type_:
            raise Exception(f"Esperado {type_}, encontrado {self.tokenizer.next.type}")
        self.tokenizer.select_next()



# === Execução Principal ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 main.py arquivo.mit")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "r") as f:
        source = f.read()

    tokenizer = Tokenizer(source)
    print(f"[DEBUG] Primeiro token: {tokenizer.next.type}, valor: {tokenizer.next.value}")

    parser = Parser(tokenizer)
    ast = parser.parse()

    st = SymbolTable()
    ast.Evaluate(st)
    print(f"[DEBUG] AST gerada: {ast}")


    code = Code()
    print(f"[DEBUG] Total de filhos no bloco: {len(ast.children)}")
    generated = ast.Generate(st)
    code.append(generated)
    print("Instruções geradas:")
    for instr in code.instructions:
        print(instr)
    code.dump(filename)

    print(f"✅ LLVM IR gerado com sucesso: {filename.replace('.mit', '.ll')}")
