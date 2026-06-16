from datetime import datetime

def backtracking(partidos, presupuesto_max):
    """
    Exploración exhaustiva del árbol de decisiones con dos podas:

    Poda 1 — Conflicto de horario:
        Solo se explora la rama "incluir partido i" si su horario de inicio
        es posterior o igual al fin del último partido seleccionado.
        Esto es correcto porque los partidos están ordenados por hora de fin.

    Poda 2 — Cota superior exacta (Branch & Bound):
        Se precomputa dp_suf[i] = máximo beneficio alcanzable con los
        partidos i..n-1 de forma independiente (sin considerar los ya elegidos).
        Si b_acumulado + dp_suf[idx] no supera al mejor conocido, se poda.

    Complejidad: O(2^n) en el peor caso teórico, pero con estas podas
    el árbol real explorado es drásticamente menor (verificado empíricamente).

    Parámetros:
        partidos: lista ordenada por hora de fin (requerido por la poda 1).
        presupuesto_max: presupuesto E global en minutos.
    """
    n = len(partidos)

    # Precomputar dp_suf: DP hacia atrás para cota exacta con presupuesto
    # dp_suf[i][e] = WIS óptimo sobre partidos[i..n-1] con presupuesto e disponible
    def next_compat_from(i):
        """Primer j > i con partidos[j].inicio >= partidos[i].fin (búsqueda binaria)."""
        lo, hi, res = i + 1, n - 1, n
        target = partidos[i]['fin']
        while lo <= hi:
            mid = (lo + hi) // 2
            if partidos[mid]['inicio'] >= target:
                res = mid; hi = mid - 1
            else:
                lo = mid + 1
        return res

    dp_suf = [[0.0] * (presupuesto_max + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        nc = next_compat_from(i)
        ci = partidos[i]['costo']
        bi = partidos[i]['beneficio']
        for e in range(presupuesto_max + 1):
            no_incluir = dp_suf[i + 1][e]
            incluir = 0.0
            if e >= ci:
                incluir = bi + dp_suf[nc][e - ci]
            dp_suf[i][e] = max(incluir, no_incluir)

    mejor = {'b': 0.0, 'sel': []}
    nodos = [0]
    NINF = datetime(1900, 1, 1)   # sentinela para "ningún partido seleccionado aún"

    def bt(idx, sel, b_acum, ultimo_fin, e_usado):
        nodos[0] += 1

        if b_acum > mejor['b']:
            mejor['b'] = b_acum
            mejor['sel'] = list(sel)

        if idx >= n:
            return

        # Poda 2: cota superior (considerando presupuesto remanente) no mejora al mejor actual
        e_disponible = presupuesto_max - e_usado
        if b_acum + dp_suf[idx][e_disponible] <= mejor['b']:
            return

        p = partidos[idx]

        # Rama INCLUIR: solo si el partido empieza después del último seleccionado y hay presupuesto
        if p['inicio'] >= ultimo_fin and e_usado + p['costo'] <= presupuesto_max:
            sel.append(p)
            bt(idx + 1, sel, b_acum + p['beneficio'], p['fin'], e_usado + p['costo'])
            sel.pop()

        # Rama NO INCLUIR
        bt(idx + 1, sel, b_acum, ultimo_fin, e_usado)

    bt(0, [], 0.0, NINF, 0)
    return mejor['sel'], round(mejor['b'], 3), nodos[0]
