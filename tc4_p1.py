import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import sympy

    return np, sympy


@app.cell
def _(sympy):
    x = sympy.symbols("x")
    return (x,)


@app.cell
def _(np, sympy, x):
    def max_error_trapezoidal(a, b, n, expr):
        h = (b - a) / n
        f2 = sympy.diff(expr, x, 2)          # f''
        f3 = sympy.diff(f2, x)               # f'''
        # candidatos: raízes reais de f''' dentro de [a, b], mais as bordas
        raizes = sympy.solve(f3, x)
        candidatos = [float(r) for r in raizes if r.is_real and a <= r <= b]
        candidatos += [a, b]
        f2_num = sympy.lambdify(x, f2, "numpy")
        maxf2 = np.max(np.abs(f2_num(np.array(candidatos, dtype=float))))
        return ((b - a) * h**2 / 12) * maxf2

    return (max_error_trapezoidal,)


@app.cell
def n_trapezoidal_rule(np, sympy, x):
    def n_trapezoidal_rule(a, b, n, expr):
        # expr é uma expressão SymPy em x. Gera a versão NumPy aqui.
        f = sympy.lambdify(x, expr, "numpy")
        h = (b - a) / n
        xs = np.linspace(a, b, n + 1)
        pesos = np.full(n + 1, 2.0)
        pesos[0] = 1.0
        pesos[-1] = 1.0
        return (f(xs) @ pesos) * (h / 2)

    return (n_trapezoidal_rule,)


@app.cell
def _(np, sympy, x):
    def simpson_rule(a, b, expr):
        # expr é uma expressão SymPy em x. Gera a versão NumPy aqui.
        f = sympy.lambdify(x, expr, "numpy")
        h = (b - a) / 2
        xs = np.array([a, (a+b)/2, b])
        pesos = np.full(3, 1.0)
        pesos[1] = 4
        return((f(xs)@pesos)*h/3)

    return (simpson_rule,)


@app.cell
def _(np, sympy, x):
    def n_simpson_rule(a, b, n, expr):
        # expr é uma expressão SymPy em x. Gera a versão NumPy aqui.
        if(n%2 == 1):
            raise(ValueError('n precisa ser par'))
        f = sympy.lambdify(x, expr, "numpy")
        h = (b - a) / n
        xs = np.linspace(a, b, n+1)
        pesos = np.full(n+1, 4.0)
        pesos[0::2] = 2
        pesos[0] = 1
        pesos[n] = 1
        return((f(xs)@pesos)*h/3)

    return (n_simpson_rule,)


@app.cell
def _(np):
    def n_simpson_rule_array(a, b, n, y):
        h = (b - a) / n
        pesos = np.full(n+1, 4.0)
        pesos[0::2] = 2
        pesos[0] = 1
        pesos[n] = 1
        return((y@pesos)*h/3)

    return (n_simpson_rule_array,)


@app.cell
def _(np, sympy, x):
    def max_error_simpson(a, b, n, expr):
        h = (b - a) / n
        f4 = sympy.diff(expr, x, 4)          # f''''
        f5 = sympy.diff(f4, x)               # f'''''
        # candidatos: raízes reais de f''''' dentro de [a, b], mais as bordas
        raizes = sympy.solve(f5, x)
        candidatos = [float(r) for r in raizes if r.is_real and a <= r <= b]
        candidatos += [a, b]
        f4_num = sympy.lambdify(x, f4, "numpy")
        maxf4 = np.max(np.abs(f4_num(np.array(candidatos, dtype=float))))
        return(((b - a) * h**4 / 180) * maxf4)

    return (max_error_simpson,)


@app.cell
def _(max_error_trapezoidal, n_trapezoidal_rule, x):
    expr1 = x**4 - 3 * x**3 + 2 * x**2 - 3
    approx_1 = n_trapezoidal_rule(-2, 3, 30, expr1)
    error_max_1 = max_error_trapezoidal(-2, 3, 30, expr1)
    res_1 = 175 / 12
    print(rf'1) aproximacao = {approx_1}, resultado real = {res_1}, diff = {abs(approx_1 - res_1)} menor que erro maximo = {error_max_1}')
    return


@app.cell
def _(max_error_trapezoidal, n_trapezoidal_rule, sympy, x):
    expr2 = sympy.exp(-x**2)
    approx_2 = n_trapezoidal_rule(0, 1, 4, expr2)
    error_max_2 = max_error_trapezoidal(0, 1, 4, expr2)
    print(rf'2) aproximacao = {approx_2}, erro maximo = {error_max_2}. Ou seja o valor real varia em torno de ({approx_2 - error_max_2}, {approx_2 + error_max_2})')
    return


@app.cell
def _(simpson_rule, x):
    expr3 = (2*x**5 + 5*x**3 - 3*x + 1)
    approx_3 = simpson_rule(1, 2, expr3)
    print(rf'3) aproximacao = {approx_3}')
    return


@app.cell
def _(max_error_simpson, n_simpson_rule, np, sympy, x):
    expr4 = (1/(4 + sympy.sin(20*x)))
    a_4 = 0
    b_4 = np.pi
    print('4)')
    for i in range(10, 31, 10):
        print(rf'aproximacao para n = {i}: {n_simpson_rule(a_4, b_4, i, expr4)}, com erro maximo de {max_error_simpson(a_4, b_4, i, expr4)}')
    return


@app.cell
def _(n_simpson_rule_array):
    x_5 = [0, 0.5, 1, 1.5, 2, 2.5, 3.0, 3.5, 4.0]
    y_5 = [0, 4.66, 7.72, 8.76, 9.72, 10.10, 10.53, 10.77, 10.91]
    n_5 = len(y_5)-1
    print(rf'5) ele correu aproximadamente {n_simpson_rule_array(x_5[0], x_5[-1], n_5, y_5):.2f} metros.')
    return


@app.cell
def _(n_simpson_rule_array):
    x_6 = [9, 10, 11, 12, 13, 14, 15, 16]
    y_6 = [75.3, 77, 83.2, 84.8, 86.5, 86.4, 81.1, 78.6]
    n_6 = len(y_6)-1
    simpson_int = n_simpson_rule_array(x_6[0], x_6[-2], n_6-1, y_6[0:-1])
    h_5_t = (x_6[-1]-x_6[-2])/1
    trap_int = (h_5_t/2)*(y_6[-2] + y_6[-1])
    int_total = simpson_int + trap_int
    print(rf'6) O prblema passa 7 intervalos de integracao que nao seria possivel calcular utilizando a regra de simpson, dado que, ela')
    print(rf'precisa de um numero par de intervalos, assim, podemos utilizar a regra para calcular as primeiras 7 horas (6 intervalos).')
    print(rf'O restante do problema sera calculado por regra do trapezio.')
    print(rf'Integracao por regra  de simpson: {simpson_int}. Integracao por regra do trapezio: {trap_int}. Integracao total: {int_total}.')
    print(rf'Assim Tav = {(1/(x_6[-1] - x_6[0])) * int_total:.2f} graus fahrenheit.')
    return


if __name__ == "__main__":
    app.run()
