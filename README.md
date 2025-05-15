# Linguagem Mitológica

Uma linguagem de programação inspirada na mitologia grega, onde escrever código é também narrar uma nova lenda.

## Tipos de Essência

| Mitologia | Tipo Tradicional | Significado                        |
| --------- | ---------------- | ---------------------------------- |
| `poder`   | `int`            | Força vital, energia ou magia      |
| `palavra` | `str`            | Nomeações, mensagens ou invocações |
| `destino` | `bool`           | Verdades e vontades (sim/não)      |

## Comandos Místicos

| Palavra              | Equivalente | Função                                 |
|----------------------|-------------|----------------------------------------|
| `invocar`            | declaração  | Criação de uma variável                |
| `proclamar`          | `print`     | Exibe uma mensagem na tela             |
| `recebe`             | `=`         | Atribuição de valor                    |
| `se` / `senao`       | `if`/`else` | Condicional                            |
| `enquanto`           | `while`     | Repetição                              |
| `consultar_oraculo()`| `input()`   | Entrada do usuário via terminal        |

## Operadores Mitológicos

| Palavra        | Símbolo | Significado                     |
|----------------|---------|---------------------------------|
| `supera`       | `>`     | maior que                       |
| `cede`         | `<`     | menor que                       |
| `unir`         | `+`     | adição                          |
| `separar`      | `-`     | subtração                       |
| `fortificar`   | `*`     | multiplicação                   |
| `enfraquecer`  | `/`     | divisão                         |
| `e`            | `&&`    | conjunção lógica                |
| `ou`           | `||`    | disjunção lógica                |

## Exemplo de Código Completo

```myth
{
    proclamar("Iniciando a jornada...");

    invocar energia como poder com 10;
    invocar mensagem como palavra com "Energia duplicada!";
    proclamar(mensagem);

    energia recebe energia fortificar 2;

    se (energia supera 10) {
        proclamar("Força lendária reconhecida.");
    } senao {
        proclamar("Energia ainda fraca.");
    }

    enquanto (energia cede 25) {
        proclamar("↻ Loop: fortalecendo energia...");
        energia recebe energia unir 3;
    }

    proclamar("🏁 Jornada concluída.");
}
