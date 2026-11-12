import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import numpy as np
    import pandas as pd

    return np, pd


@app.cell
def _(np):
    def hora_morte(k, T):
        tm = -(1/k) * np.log((37-18)/(T-18))
        hh = str(24 + tm).split('.')[0]
        mm = str(np.float64('0.' + str(24 + tm).split('.')[1]) * 60).split('.')[0]
        hora = hh + mm
        return hora

    return (hora_morte,)


@app.cell
def _(np):
    t = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
    Ta = [18, 19.8, 21.2, 22.1, 22.8, 23.3, 23.6, 23.9, 24]
    k = (1/2) * (np.log((25.7-18)/(23.2-18)))
    TL = 18 + (25.7 - 18) * np.exp(k)
    T = []
    T.insert(0, TL)
    L = 4
    h = 0.5
    n = round(L / h)
    tmp = TL
    for i in range(n, 0, -1):
        tmp = tmp - h*(-k*(tmp - Ta[i]))
        T.insert(0, tmp)
    return L, T, TL, Ta, k, t


@app.cell
def _():
    def euler(f, t0, y0, h, n):
        y, t = y0, t0
        for _ in range(n):
            y = y + h * f(t, y)
            t = t + h
        return y

    def rk4(f, t0, y0, h, n):
        y, t = y0, t0
        for _ in range(n):
            k1 = f(t, y)
            k2 = f(t + h/2, y + (h/2) * k1)
            k3 = f(t + h/2, y + (h/2) * k2)
            k4 = f(t + h, y + (h) * k3)
            y = y + (h/6) * (k1 + 2*k2 + 2*k3 + k4)
            t = t + h
        return y

    return euler, rk4


@app.cell
def _(L, T, TL, Ta, hora_morte, k, rk4, t):
    f = lambda x, T: -k * (T - Ta[-1::-1][t[-1::-1].index(x)])
    print(rf'1) Por euler:')
    print(rf'T0 = {T[0]:.2f}')
    print(rf'Hora da morte: {hora_morte(k, T[0])}')
    print(rf'Por RK4:')
    print(rf'T0 = {rk4(f, L, TL, -1, round(L / 1)):.2f}')
    print(rf'Hora da morte: {hora_morte(k, rk4(f, 4, TL, -1, round(4 / 1)))}, sim a hora da morte muda em aproximadamente 14 minutos.')
    return


@app.cell
def _(L, TL, euler, hora_morte, k, pd):
    f_2 = lambda t, T: -k * (T - (18 + 3*t))
    resps_2 = []
    for j in (0.5, 0.25, 0.125):
        tmp_2 = euler(f_2, L, TL, -j, round(L/j))
        resps_2.append({'h': j, 'T' : tmp_2, 'hora_morte' : hora_morte(k, tmp_2), 'dif' : 2152 - int(hora_morte(k, tmp_2))})
    print('2) Na tabela abaixo podemos ver o erro caindo por aproximadamente a metade (em relacao ao horario correto que seria 2152).')
    print(pd.DataFrame(resps_2))
    return (f_2,)


@app.cell
def _(L, TL, euler, f_2, hora_morte, k, pd, rk4):
    resps_3 = []
    for m in (0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.0078125):
        tmp_3 = euler(f_2, L, TL, -m, round(L/m))
        resps_3.append({
            'tipo' : 'euler'
            , 'h': m
            , 'T' : tmp_3
            , 'hora_morte' : hora_morte(k, tmp_3)
            , 'dif' : 2152 - int(hora_morte(k, tmp_3))
        })
    print('3) Na tabela abaixo podemos ver que seria aproximadamente no sexto/setimo passo.')
    print(pd.DataFrame(resps_3))

    print(rf'Para RK4 o primeiro passo (0.5) ja seria suficiente: {hora_morte(k, rk4(f_2, L, TL, -0.5, round(L/0.5)))} (2152 horario oficial).')
    return


if __name__ == "__main__":
    app.run()
