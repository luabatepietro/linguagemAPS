%{
#include "mitologia.tab.h"
%}

%option noyywrap

%%

"{"             { return ABRE_CHAVES; }
"}"             { return FECHA_CHAVES; }
"("             { return ABRE_PARENTESES; }
")"             { return FECHA_PARENTESES; }
";"             { return PONTO_VIRGULA; }
","             { return VIRGULA; }

"invocar"       { return INVOCAR; }
"proclamar"     { return PROCLAMAR; }
"se"            { return SE; }
"senao"         { return SENAO; }
"enquanto"      { return ENQUANTO; }
"consultar_oraculo" { return CONSULTAR_ORACULO; }

"poder"         { return PODER; }
"palavra"       { return PALAVRA; }
"destino"       { return DESTINO; }

"como"          { return COMO; }
"com"           { return COM; }

"recebe"        { return RECEBE; }

"supera"        { return SUPERA; }
"cede"          { return CEDE; }
"unir"          { return UNIR; }
"separar"       { return SEPARAR; }
"fortificar"    { return FORTIFICAR; }
"enfraquecer"   { return ENFRAQUECER; }
"bênção"        { return BENCAO; }
"maldição"      { return MALDICAO; }

"=="            { return IGUAL; }
"!="            { return DIFERENTE; }
"e"             { return E_LOGICO; }
"ou"            { return OU_LOGICO; }

"verdadeiro"    { yylval.booleano = 1; return BOOLEANO; }
"falso"         { yylval.booleano = 0; return BOOLEANO; }

[0-9]+          { yylval.numero = atoi(yytext); return NUM; }
\"([^\\\"]|\\.)*\" { yylval.texto = strdup(yytext); return STRING; }

[a-zA-Z_][a-zA-Z0-9_]* { yylval.id = strdup(yytext); return ID; }

[ \t\n\r]+      ; // ignora espaços e quebras
.               ; // ignora outros
