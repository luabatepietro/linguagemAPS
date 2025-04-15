# Linguagem Mitológica

Uma linguagem de programação temática baseada na mitologia grega, onde cada elemento de programação é representado por conceitos mitológicos, permitindo a criação de narrativas mitológicas interativas.

## Elementos da Linguagem

### Tipos de Dados Básicos

| Linguagem Mitológica | Python | Descrição                                          |
| -------------------- | ------ | -------------------------------------------------- |
| `poder`              | `int`  | Representa valores numéricos (poder, força, nível) |
| `texto`              | `str`  | Representa strings (nomes, descrições, mensagens)  |
| `destino`            | `bool` | Representa estados booleanos (verdadeiro/falso)    |

### Representação de Entidades Mitológicas

Cada entidade mitológica é representada usando combinações dos tipos básicos:

1. **Herói/Deus/Criatura**:

   - `poder` para força/habilidade
   - `texto` para nome
   - `destino` para estado (vivo/morto, ativo/inativo)

2. **Artefato/Local**:

   - `texto` para nome e descrição
   - `poder` para nível de magia/importância

3. **Evento**:
   - `texto` para descrição
   - `destino` para ocorreu/não ocorreu
   - `poder` para impacto/consequências

### Comandos (Funções em Python)

| Linguagem Mitológica | Python                  | Descrição                                                 |
| -------------------- | ----------------------- | --------------------------------------------------------- |
| `criar`              | `def criar_entidade():` | Declara uma nova entidade mitológica usando tipos básicos |
| `contar`             | `print()`               | Exibe texto na narrativa                                  |
| `quando`             | `if/else`               | Estrutura condicional para momentos decisivos             |
| `enquanto`           | `while`                 | Estrutura de repetição para criar tensão                  |
| `consultar`          | `input()`               | Recebe entrada do usuário                                 |

### Operadores (Operadores em Python)

| Linguagem Mitológica | Python | Descrição                                        |
| -------------------- | ------ | ------------------------------------------------ |
| `supera`             | `>`    | Comparação "maior que" para `poder`              |
| `cede`               | `<`    | Comparação "menor que" para `poder`              |
| `unir`               | `+`    | Adição para `poder` ou concatenação para `texto` |
| `separar`            | `-`    | Subtração para `poder`                           |
| `fortificar`         | `*`    | Multiplicação para `poder`                       |
| `enfraquecer`        | `/`    | Divisão para `poder`                             |
| `bênção`             | `+`    | Sinal positivo para `poder`                      |
| `maldição`           | `-`    | Sinal negativo para `poder`                      |
| `e`                  | `and`  | Operador lógico AND para `destino`               |
| `ou`                 | `or`   | Operador lógico OR para `destino`                |

## Exemplo de Código

```myth
{
    # Criando um herói usando tipos básicos
    criar forca_perseu como poder com 100;  # Equivalente a: forca_perseu = 100
    criar nome_perseu como texto com "Perseu";  # Equivalente a: nome_perseu = "Perseu"
    criar vivo_perseu como destino com verdadeiro;  # Equivalente a: vivo_perseu = True

    # Criando uma criatura
    criar forca_medusa como poder com 80;
    criar nome_medusa como texto com "Medusa";
    criar viva_medusa como destino com verdadeiro;

    # Criando um artefato
    criar nome_espada como texto com "Espada de Hermes";
    criar poder_espada como poder com 50;

    contar("No início dos tempos...");  # Equivalente a: print("No início dos tempos...")

    quando (forca_perseu supera 50) {  # Equivalente a: if forca_perseu > 50:
        contar("Perseu recebeu a bênção dos deuses");
        forca_perseu recebe forca_perseu fortificar 2;  # Equivalente a: forca_perseu *= 2
    }

    enquanto (viva_medusa == verdadeiro e forca_medusa cede forca_perseu) {
        contar("A batalha se intensifica");
        forca_perseu recebe forca_perseu unir 10;  # Equivalente a: forca_perseu += 10
        forca_medusa recebe forca_medusa enfraquecer 2;  # Equivalente a: forca_medusa /= 2
    }
}
```
