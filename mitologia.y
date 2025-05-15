%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int yylex(void);
void yyerror(const char *s);

typedef struct {
    char *id;
    int tipo;
    union {
        int numero;
        char *texto;
        int booleano;
    } valor;
} Variavel;

Variavel simbolos[100];
int qtd = 0;

Variavel* buscar(char *id) {
    for (int i = 0; i < qtd; i++) {
        if (strcmp(simbolos[i].id, id) == 0)
            return &simbolos[i];
    }
    return NULL;
}

void declarar(char *id, int tipo, void *valor) {
    Variavel *v = malloc(sizeof(Variavel));
    v->id = strdup(id);
    v->tipo = tipo;
    if (tipo == 0) v->valor.numero = *((int *)valor);
    if (tipo == 1) v->valor.texto = strdup((char *)valor);
    if (tipo == 2) v->valor.booleano = *((int *)valor);
    simbolos[qtd++] = *v;
}

void atribuir(char *id, int valor) {
    Variavel *v = buscar(id);
    if (v && v->tipo == 0) v->valor.numero = valor;
}

int obter(char *id) {
    Variavel *v = buscar(id);
    if (v && v->tipo == 0) return v->valor.numero;
    return 0;
}

char* consultar_string() {
    static char buffer[256];
    printf("Digite um texto: ");
    scanf(" %[^\n]", buffer);
    return strdup(buffer);
}

int consultar_int() {
    int x;
    printf("Digite um número: ");
    scanf("%d", &x);
    return x;
}

int consultar_bool() {
    char buffer[10];
    printf("Digite verdadeiro ou falso: ");
    scanf("%s", buffer);
    return strcmp(buffer, "verdadeiro") == 0;
}

void proclamar(char *texto) {
    printf("\"%s\"\n", texto);
}
%}

%union {
    int numero;
    int booleano;
    char *texto;
    char *id;
}

%token ABRE_CHAVES FECHA_CHAVES ABRE_PARENTESES FECHA_PARENTESES
%token PONTO_VIRGULA VIRGULA
%token INVOCAR PROCLAMAR SE SENAO ENQUANTO CONSULTAR_ORACULO
%token PODER PALAVRA DESTINO COMO COM
%token RECEBE
%token SUPERA CEDE UNIR SEPARAR FORTIFICAR ENFRAQUECER
%token BENCAO MALDICAO
%token IGUAL DIFERENTE
%token E_LOGICO OU_LOGICO
%token <numero> NUM
%token <texto> STRING
%token <booleano> BOOLEANO
%token <id> ID

%type <numero> tipo elemento expressao expressao_logica expressao_relacional expressao_aritmetica termo fator

%start programa

%%

programa : ABRE_CHAVES lista_comandos FECHA_CHAVES ;

lista_comandos : /* vazio */
               | lista_comandos comando ;

comando : declaracao
        | atribuicao
        | narrativa
        | condicao
        | ciclo ;

declaracao
    : INVOCAR ID COMO tipo COM expressao PONTO_VIRGULA {
        declarar($2, $4, &$6);
    }
    | INVOCAR ID COMO tipo COM STRING PONTO_VIRGULA {
        declarar($2, $4, $6);
    }
    | INVOCAR ID COMO tipo COM BOOLEANO PONTO_VIRGULA {
        declarar($2, $4, &$6);
    }
    | INVOCAR ID COMO tipo COM CONSULTAR_ORACULO ABRE_PARENTESES FECHA_PARENTESES PONTO_VIRGULA {
        if ($4 == 0) {
            int v = consultar_int();
            declarar($2, $4, &v);
        } else if ($4 == 1) {
            char* v = consultar_string();
            declarar($2, $4, v);
        } else if ($4 == 2) {
            int v = consultar_bool();
            declarar($2, $4, &v);
        }
    }
    ;

tipo : PODER { $$ = 0; }
     | PALAVRA { $$ = 1; }
     | DESTINO { $$ = 2; }
     ;

atribuicao : ID RECEBE expressao PONTO_VIRGULA {
    atribuir($1, $3);
} ;

narrativa : PROCLAMAR ABRE_PARENTESES STRING FECHA_PARENTESES PONTO_VIRGULA {
    proclamar($3);
} ;

condicao : SE ABRE_PARENTESES expressao FECHA_PARENTESES bloco
         | SE ABRE_PARENTESES expressao FECHA_PARENTESES bloco SENAO bloco ;

ciclo : ENQUANTO ABRE_PARENTESES expressao FECHA_PARENTESES bloco ;

bloco : ABRE_CHAVES lista_comandos FECHA_CHAVES ;

expressao : expressao_logica ;

expressao_logica
    : expressao_relacional
    | expressao_relacional E_LOGICO expressao_relacional { $$ = $1 && $3; }
    | expressao_relacional OU_LOGICO expressao_relacional { $$ = $1 || $3; }
    ;

expressao_relacional
    : expressao_aritmetica
    | expressao_aritmetica SUPERA expressao_aritmetica { $$ = $1 > $3; }
    | expressao_aritmetica CEDE expressao_aritmetica { $$ = $1 < $3; }
    | expressao_aritmetica IGUAL expressao_aritmetica { $$ = $1 == $3; }
    | expressao_aritmetica DIFERENTE expressao_aritmetica { $$ = $1 != $3; }
    ;

expressao_aritmetica
    : termo
    | expressao_aritmetica UNIR termo { $$ = $1 + $3; }
    | expressao_aritmetica SEPARAR termo { $$ = $1 - $3; }
    ;

termo
    : fator
    | termo FORTIFICAR fator { $$ = $1 * $3; }
    | termo ENFRAQUECER fator { $$ = $1 / $3; }
    ;

fator
    : BENCAO elemento { $$ = +$2; }
    | MALDICAO elemento { $$ = -$2; }
    | elemento ;

elemento
    : ID { $$ = obter($1); }
    | NUM { $$ = $1; }
    | ABRE_PARENTESES expressao FECHA_PARENTESES { $$ = $2; }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
}

int main() {
    return yyparse();
}
