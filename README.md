# Linguagem Mitológica

Uma linguagem de programação inspirada na mitologia grega, onde escrever código é também narrar o desenrolar de uma nova lenda.

## Tipos de Essências

| Mitologia | Tipo Tradicional | Significado                        |
| --------- | ---------------- | ---------------------------------- |
| `poder`   | `int`            | Força vital, energia ou magia      |
| `palavra` | `str`            | Nomeações, mensagens ou invocações |
| `destino` | `bool`           | Verdades e vontades (sim/não)      |

---

## Entidades do Mundo

- **Heróis, Deuses e Criaturas**:

  - `poder` → Força do ser
  - `palavra` → Nome eterno
  - `destino` → Existência ou ruína

- **Artefatos Sagrados ou Locais Místicos**:

  - `palavra` → Nome ou descrição
  - `poder` → Potência mágica

- **Eventos do Tecido do Destino**:
  - `palavra` → Descrição do evento
  - `destino` → Se ocorreu
  - `poder` → Intensidade do impacto

---

## Feitiços (Comandos)

| Palavra Mitológica  | Ação Tradicional | Propósito                                           |
| ------------------- | ---------------- | --------------------------------------------------- |
| `invocar`           | `def`            | Dá existência a uma nova entidade ou elemento       |
| `proclamar`         | `print`          | Narra palavras aos deuses e mortais                 |
| `se`                | `if/else`        | Escolhas no entrelaçar dos destinos                 |
| `enquanto`          | `while`          | Repetição eterna enquanto a vontade divina permitir |
| `consultar_oraculo` | `input()`        | Busca respostas do além                             |

---

## Forças e Conflitos (Operadores)

| Palavra Mitológica | Símbolo | Significado                   |
| ------------------ | ------- | ----------------------------- |
| `supera`           | `>`     | Um poder é maior que outro    |
| `cede`             | `<`     | Um poder é menor que outro    |
| `unir`             | `+`     | Juntar forças ou palavras     |
| `separar`          | `-`     | Diluir forças                 |
| `fortificar`       | `*`     | Multiplicar forças            |
| `enfraquecer`      | `/`     | Dividir forças                |
| `e`                | `and`   | Ambos destinos se cumprem     |
| `ou`               | `or`    | Um ou outro destino se cumpre |

---

## Exemplo de Código: A Jornada de Perseu

```myth
{
    # Perseu surge ao mundo
    invocar forca_perseu como poder com 100;
    invocar nome_perseu como palavra com "Perseu";
    invocar vivo_perseu como destino com verdadeiro;

    # Nasce sua inimiga, Medusa
    invocar forca_medusa como poder com 80;
    invocar nome_medusa como palavra com "Medusa";
    invocar viva_medusa como destino com verdadeiro;

    # Forjado nas estrelas, uma arma é entregue
    invocar nome_espada como palavra com "Espada de Hermes";
    invocar poder_espada como poder com 50;

    # O oráculo proclama o início
    proclamar("No início dos tempos, heróis e monstros despertaram...");

    # Se Perseu mostrar grande poder
    se (forca_perseu supera 50) {
        proclamar("Perseu recebeu a bênção dos deuses!");
        forca_perseu recebe forca_perseu fortificar 2;
    }

    # Enquanto Medusa respira e é fraca diante de Perseu
    enquanto (viva_medusa e (forca_medusa cede forca_perseu)) {
        proclamar("A batalha entre Perseu e Medusa ecoa pelos tempos!");
        forca_perseu recebe forca_perseu unir 10;
        forca_medusa recebe forca_medusa enfraquecer 2;
    }
}
```