def programacion_dinamica(partidos, presupuesto_max):
    """
    Solución óptima por Programación Dinámica (Weighted Interval Scheduling + Knapsack).

    Definición:
        dp[i][e] = máximo beneficio acumulable considerando los partidos 0..i
                   con un presupuesto consumido a lo sumo 'e'.

    Función de compatibilidad p(i):
        Índice del último partido j < i tal que fin[j] <= inicio[i].
        Calculado con búsqueda binaria → O(log n) por llamada.

    Recurrencia:
        dp[i][e] = max(
            dp[i-1][e],  # omitir i
            b[i] + dp[p(i)][e - costo[i]]  # incluir i, solo si e >= costo[i]
        )

    Reconstrucción de la solución: recorrido hacia atrás sobre dp[][].

    Complejidad: O(n log n + n * E)
    """
    n = len(partidos)
    if n == 0:
        return [], 0.0

    def ultimo_compatible(i):
        """Mayor j < i con partidos[j].fin <= partidos[i].inicio."""
        lo, hi, res = 0, i - 1, -1
        target = partidos[i]['inicio']
        while lo <= hi:
            mid = (lo + hi) // 2
            if partidos[mid]['fin'] <= target:
                res = mid; lo = mid + 1
            else:
                hi = mid - 1
        return res

    # dp[i][e]
    dp = [[0.0] * (presupuesto_max + 1) for _ in range(n)]

    # Caso base i=0
    c0 = partidos[0]['costo']
    b0 = partidos[0]['beneficio']
    for e in range(presupuesto_max + 1):
        if e >= c0:
            dp[0][e] = b0

    for i in range(1, n):
        j = ultimo_compatible(i)
        ci = partidos[i]['costo']
        bi = partidos[i]['beneficio']
        
        for e in range(presupuesto_max + 1):
            no_incluir = dp[i - 1][e]
            incluir = 0.0
            if e >= ci:
                incluir = bi + (dp[j][e - ci] if j >= 0 else 0.0)
            dp[i][e] = max(incluir, no_incluir)

    # Reconstrucción
    seleccion = []
    i = n - 1
    e = presupuesto_max
    while i >= 0:
        j = ultimo_compatible(i)
        ci = partidos[i]['costo']
        bi = partidos[i]['beneficio']
        
        incluir = bi + (dp[j][e - ci] if j >= 0 else 0.0) if e >= ci else -float('inf')
        # Comparamos con no_incluir (dp[i-1][e] o 0 si i=0)
        no_incluir = dp[i - 1][e] if i > 0 else 0.0
        
        if incluir >= no_incluir and e >= ci:
            seleccion.append(partidos[i])
            e -= ci
            i = j
        else:
            i -= 1

    seleccion.reverse()
    return seleccion, round(dp[n - 1][presupuesto_max], 3)
