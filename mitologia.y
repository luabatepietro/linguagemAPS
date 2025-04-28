%{
#include <stdio.h>
#include <stdlib.h>

void yyerror(const char *s);
int yylex();
%}

%union {
    int numero;
    int booleano;
    char *texto;
    char *id;
}

/* Tokens */
%token ABRE_CHAVES FECHA_CHAVES ABRE_PARENTESES FECHA_PARENTESES
%token PONTO_VIRGULA VIRGULA
%token INVOCAR PROCLAMAR SE SENAO ENQUANTO CONSULTAR_ORACULO
%token PODER PALAVRA DESTINO
%token RECEBE
%token SUPERA CEDE UNIR SEPARAR FORTIFICAR ENFRAQUECER
%token BENCAO MALDICAO
%token IGUAL DIFERENTE
%token E_LOGICO OU_LOGICO
%token NUM STRING BOOLEANO
%token ID

%start programa

%%

programa
    : ABRE_CHAVES lista_comandos FECHA_CHAVES
    ;

lista_comandos
    : /* vazio */
    | lista_comandos comando
    ;

comando
    : declaracao
    | atribuicao
    | narrativa
    | condicao
    | ciclo
    ;

declaracao
    : INVOCAR ID "como" tipo [ "com" expressao ] PONTO_VIRGULA
    ;

tipo
    : PODER
    | PALAVRA
    | DESTINO
    ;

atribuicao
    : ID RECEBE expressao PONTO_VIRGULA
    ;

narrativa
    : PROCLAMAR ABRE_PARENTESES expressao FECHA_PARENTESES PONTO_VIRGULA
    ;

condicao
    : SE ABRE_PARENTESES expressao FECHA_PARENTESES bloco [ SENAO bloco ]
    ;

ciclo
    : ENQUANTO ABRE_PARENTESES expressao FECHA_PARENTESES bloco
    ;

bloco
    : ABRE_CHAVES lista_comandos FECHA_CHAVES
    ;

expressao
    : expressao_logica
    ;

expressao_logica
    : expressao_relacional
    | expressao_relacional E_LOGICO expressao_relacional
    | expressao_relacional OU_LOGICO expressao_relacional
    ;

expressao_relacional
    : expressao_aritmetica
    | expressao_aritmetica SUPERA expressao_aritmetica
    | expressao_aritmetica CEDE expressao_aritmetica
    | expressao_aritmetica IGUAL expressao_aritmetica
    | expressao_aritmetica DIFERENTE expressao_aritmetica
    ;

expressao_aritmetica
    : termo
    | expressao_aritmetica UNIR termo
    | expressao_aritmetica SEPARAR termo
    ;

termo
    : fator
    | termo FORTIFICAR fator
    | termo ENFRAQUECER fator
    ;

fator
    : BENCAO elemento
    | MALDICAO elemento
    | elemento
    ;

elemento
    : ID
    | NUM
    | STRING
    | BOOLEANO
    | CONSULTAR_ORACULO ABRE_PARENTESES FECHA_PARENTESES
    | ABRE_PARENTESES expressao FECHA_PARENTESES
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Erro de sintaxe: %s\n", s);
}

int main() {
    return yyparse();
}
