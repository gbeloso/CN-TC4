# CN-TC4 — Integração Numérica

Trabalho de Cálculo Numérico (UNIFESP) sobre **integração numérica**: implementação das
regras do **trapézio** e de **Simpson 1/3** (versões simples e compostas) e das respectivas
**cotas de erro**, usando entrada simbólica com SymPy.

O código está em um notebook [marimo](https://marimo.io/) (`tc4_p1.py`).

## Conteúdo

| Função | Descrição |
| --- | --- |
| `n_trapezoidal_rule(a, b, n, expr)` | Regra do trapézio composta para `n` subintervalos. |
| `simpson_rule(a, b, expr)` | Regra de Simpson 1/3 simples (3 pontos). |
| `n_simpson_rule(a, b, n, expr)` | Regra de Simpson 1/3 composta (exige `n` par). |
| `n_simpson_rule_array(a, b, n, y)` | Simpson 1/3 composta a partir de valores tabelados `y` (sem expressão). |
| `max_error_trapezoidal(a, b, n, expr)` | Cota de erro do trapézio, `O(h²)`, via `max\|f''\|`. |
| `max_error_simpson(a, b, n, expr)` | Cota de erro de Simpson, `O(h⁴)`, via `max\|f⁽⁴⁾\|`. |

As funções que recebem `expr` esperam uma **expressão SymPy** na variável `x`
(ex.: `x**4 - 3*x**3`, `sympy.exp(-x**2)`). Internamente a expressão é convertida para
uma função NumPy via `sympy.lambdify`, servindo como fonte única para o cálculo numérico
e para as derivadas usadas nas cotas de erro.

## Requisitos

- Python 3.12+
- Dependências em [`requirements.txt`](requirements.txt) — principais: `numpy`, `sympy`
  e `marimo` (para abrir o notebook).

Instalação em um ambiente virtual:

```bash
python -m venv .venv
# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Como executar

Há duas formas, dependendo do que você quer:

### 1. Visualizar como notebook marimo (interativo)

Com o ambiente ativado e o `marimo` instalado:

```bash
# Modo edição (interativo, abre no navegador)
marimo edit tc4_p1.py

# Modo aplicativo (somente execução, abre no navegador)
marimo run tc4_p1.py
```

> **Observação sobre o kernel:** o marimo usa o Python do ambiente em que foi iniciado.
> Para que ele use o `.venv` do projeto, ative o `.venv` **antes** de rodar `marimo`
> (ou chame o executável dentro dele, ex.: `.venv/bin/marimo` ou
> `.\.venv\Scripts\marimo.exe`).

### 2. Executar apenas o código (sem interface)

O arquivo também roda como um script Python comum. Basta ter todas as dependências
instaladas (`pip install -r requirements.txt`):

```bash
python tc4_p1.py
```

Isso executa todas as células em sequência e imprime os resultados no terminal, sem
abrir o navegador.

## Estrutura

```
CN-TC4/
├── tc4_p1.py          # notebook marimo com as implementações e os testes
├── requirements.txt   # dependências do projeto
├── .gitignore
└── README.md
```

## Notas

- A regra de Simpson 1/3 composta exige número **par** de subintervalos; `n_simpson_rule`
  valida isso e levanta `ValueError` caso contrário.
- As cotas de erro usam o valor máximo da derivada relevante no intervalo `[a, b]`,
  avaliado nas raízes reais da derivada seguinte (pontos críticos) e nas bordas `a` e `b`.
- Para funções sem primitiva elementar (ex.: `exp(-x²)`) não há valor exato de referência;
  nesses casos o resultado é apresentado junto da cota de erro.
