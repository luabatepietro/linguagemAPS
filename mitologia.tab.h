/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_MITOLOGIA_TAB_H_INCLUDED
# define YY_YY_MITOLOGIA_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    ABRE_CHAVES = 258,             /* ABRE_CHAVES  */
    FECHA_CHAVES = 259,            /* FECHA_CHAVES  */
    ABRE_PARENTESES = 260,         /* ABRE_PARENTESES  */
    FECHA_PARENTESES = 261,        /* FECHA_PARENTESES  */
    PONTO_VIRGULA = 262,           /* PONTO_VIRGULA  */
    VIRGULA = 263,                 /* VIRGULA  */
    INVOCAR = 264,                 /* INVOCAR  */
    PROCLAMAR = 265,               /* PROCLAMAR  */
    SE = 266,                      /* SE  */
    SENAO = 267,                   /* SENAO  */
    ENQUANTO = 268,                /* ENQUANTO  */
    CONSULTAR_ORACULO = 269,       /* CONSULTAR_ORACULO  */
    PODER = 270,                   /* PODER  */
    PALAVRA = 271,                 /* PALAVRA  */
    DESTINO = 272,                 /* DESTINO  */
    COMO = 273,                    /* COMO  */
    COM = 274,                     /* COM  */
    RECEBE = 275,                  /* RECEBE  */
    SUPERA = 276,                  /* SUPERA  */
    CEDE = 277,                    /* CEDE  */
    UNIR = 278,                    /* UNIR  */
    SEPARAR = 279,                 /* SEPARAR  */
    FORTIFICAR = 280,              /* FORTIFICAR  */
    ENFRAQUECER = 281,             /* ENFRAQUECER  */
    BENCAO = 282,                  /* BENCAO  */
    MALDICAO = 283,                /* MALDICAO  */
    IGUAL = 284,                   /* IGUAL  */
    DIFERENTE = 285,               /* DIFERENTE  */
    E_LOGICO = 286,                /* E_LOGICO  */
    OU_LOGICO = 287,               /* OU_LOGICO  */
    NUM = 288,                     /* NUM  */
    STRING = 289,                  /* STRING  */
    BOOLEANO = 290,                /* BOOLEANO  */
    ID = 291                       /* ID  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 56 "mitologia.y"

    int numero;
    int booleano;
    char *texto;
    char *id;

#line 107 "mitologia.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_MITOLOGIA_TAB_H_INCLUDED  */
