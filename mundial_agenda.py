"""
╔══════════════════════════════════════════════════════════════════╗
║   OPTIMIZACIÓN DE AGENDA TELEVISIVA — MUNDIAL 2026              ║
║   Weighted Interval Scheduling con atractivo ponderado           ║
║                                                                  ║
║   Técnicas: Backtracking | Programación Dinámica | Ávido        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json, sys, time
from datetime import datetime, timedelta

sys.setrecursionlimit(50000)

# ══════════════════════════════════════════════════════════════════
# 1. PARÁMETROS Y DATOS BASE
# ══════════════════════════════════════════════════════════════════

ALPHA = 0.30   # peso historial mundialista  h_i
BETA  = 0.10   # peso talla del plantel      t_i
GAMMA = 0.60   # peso logros recientes       l_i
DUR   = timedelta(minutes=100)   # 90 min reglamentarios + 10 min adicional promedio

with open('squad_data.json')   as f: SQUAD_DATA     = json.load(f)
with open('wc_history.json')   as f: WC_HISTORY     = json.load(f)
with open('recent_titles.json') as f: RECENT_TITLES = json.load(f)

def calcular_beneficio(eq1: str, eq2: str) -> float:
    """
    Atractivo compuesto del partido:
        b_i = α·h_i + β·t_i + γ·l_i

    h_i = promedio del historial mundialista de ambas selecciones (0–10)
          Basado en títulos, finales y semifinales en la Copa del Mundo 1930-2022.

    t_i = promedio de la talla del plantel (0–10)
          Proporción de jugadores que militan en Premier League, La Liga o Serie A,
          más un bonus por jugadores presentes en el ranking mundial top-20.

    l_i = logro reciente máximo entre ambos equipos (0–10)
          10 si alguno ganó el Mundial; 6 si ganó Copa América/Eurocopa/similar;
          valores intermedios según relevancia del título.
    """
    h_i = (WC_HISTORY.get(eq1, 0.0) + WC_HISTORY.get(eq2, 0.0)) / 2
    t_i = (SQUAD_DATA.get(eq1, {}).get('t_i', 0.0) +
           SQUAD_DATA.get(eq2, {}).get('t_i', 0.0)) / 2
    l_i = max(RECENT_TITLES.get(eq1, 0), RECENT_TITLES.get(eq2, 0))
    return round(ALPHA * h_i + BETA * t_i + GAMMA * l_i, 3)


# ══════════════════════════════════════════════════════════════════
# 2. FIXTURE COMPLETO — FASE DE GRUPOS MUNDIAL 2026
# ══════════════════════════════════════════════════════════════════

RAW_FIXTURE = [
    ("2026-06-11 16:00","MEX","RSA","Grupo A"), ("2026-06-11 23:00","KOR","CZE","Grupo A"),
    ("2026-06-12 16:00","CAN","BIH","Grupo B"), ("2026-06-12 22:00","USA","PAR","Grupo D"),
    ("2026-06-13 16:00","QAT","SUI","Grupo B"), ("2026-06-13 19:00","BRA","MAR","Grupo C"),
    ("2026-06-13 22:00","HAI","SCO","Grupo C"), ("2026-06-14 01:00","AUS","TUR","Grupo D"),
    ("2026-06-14 14:00","GER","CUW","Grupo E"), ("2026-06-14 17:00","NED","JPN","Grupo F"),
    ("2026-06-14 20:00","CIV","ECU","Grupo E"), ("2026-06-14 23:00","SWE","TUN","Grupo F"),
    ("2026-06-15 13:00","ESP","CPV","Grupo H"), ("2026-06-15 16:00","BEL","EGY","Grupo G"),
    ("2026-06-15 19:00","KSA","URU","Grupo H"), ("2026-06-15 22:00","IRN","NZL","Grupo G"),
    ("2026-06-16 16:00","FRA","SEN","Grupo I"), ("2026-06-16 19:00","IRQ","NOR","Grupo I"),
    ("2026-06-16 22:00","ARG","ALG","Grupo J"), ("2026-06-17 01:00","AUT","JOR","Grupo J"),
    ("2026-06-17 14:00","POR","COD","Grupo K"), ("2026-06-17 17:00","ENG","CRO","Grupo L"),
    ("2026-06-17 20:00","GHA","PAN","Grupo L"), ("2026-06-17 23:00","UZB","COL","Grupo K"),
    ("2026-06-18 13:00","CZE","RSA","Grupo A"), ("2026-06-18 16:00","SUI","BIH","Grupo B"),
    ("2026-06-18 19:00","CAN","QAT","Grupo B"), ("2026-06-18 22:00","MEX","KOR","Grupo A"),
    ("2026-06-19 16:00","USA","AUS","Grupo D"), ("2026-06-19 19:00","SCO","MAR","Grupo C"),
    ("2026-06-19 21:30","BRA","HAI","Grupo C"), ("2026-06-20 00:00","TUR","PAR","Grupo D"),
    ("2026-06-20 14:00","NED","SWE","Grupo F"), ("2026-06-20 17:00","GER","CIV","Grupo E"),
    ("2026-06-20 21:00","ECU","CUW","Grupo E"), ("2026-06-21 01:00","TUN","JPN","Grupo F"),
    ("2026-06-21 13:00","ESP","KSA","Grupo H"), ("2026-06-21 16:00","BEL","IRN","Grupo G"),
    ("2026-06-21 19:00","URU","CPV","Grupo H"), ("2026-06-21 22:00","NZL","EGY","Grupo G"),
    ("2026-06-22 14:00","ARG","AUT","Grupo J"), ("2026-06-22 18:00","FRA","IRQ","Grupo I"),
    ("2026-06-22 21:00","NOR","SEN","Grupo I"), ("2026-06-23 00:00","JOR","ALG","Grupo J"),
    ("2026-06-23 14:00","POR","UZB","Grupo K"), ("2026-06-23 17:00","ENG","GHA","Grupo L"),
    ("2026-06-23 20:00","PAN","CRO","Grupo L"), ("2026-06-23 23:00","COL","COD","Grupo K"),
    ("2026-06-24 16:00","SUI","CAN","Grupo B"), ("2026-06-24 16:00","BIH","QAT","Grupo B"),
    ("2026-06-24 19:00","SCO","BRA","Grupo C"), ("2026-06-24 19:00","MAR","HAI","Grupo C"),
    ("2026-06-24 22:00","CZE","MEX","Grupo A"), ("2026-06-24 22:00","RSA","KOR","Grupo A"),
    ("2026-06-25 17:00","CUW","CIV","Grupo E"), ("2026-06-25 17:00","ECU","GER","Grupo E"),
    ("2026-06-25 20:00","JPN","SWE","Grupo F"), ("2026-06-25 20:00","TUN","NED","Grupo F"),
    ("2026-06-25 23:00","TUR","USA","Grupo D"), ("2026-06-25 23:00","PAR","AUS","Grupo D"),
    ("2026-06-26 16:00","NOR","FRA","Grupo I"), ("2026-06-26 16:00","SEN","IRQ","Grupo I"),
    ("2026-06-26 21:00","CPV","KSA","Grupo H"), ("2026-06-26 21:00","URU","ESP","Grupo H"),
    ("2026-06-27 00:00","EGY","IRN","Grupo G"), ("2026-06-27 00:00","NZL","BEL","Grupo G"),
    ("2026-06-27 18:00","PAN","ENG","Grupo L"), ("2026-06-27 18:00","CRO","GHA","Grupo L"),
    ("2026-06-27 20:30","COL","POR","Grupo K"), ("2026-06-27 20:30","COD","UZB","Grupo K"),
    ("2026-06-27 23:00","ALG","AUT","Grupo J"), ("2026-06-27 23:00","JOR","ARG","Grupo J"),
]

def parse_fixture():
    partidos = []
    for inicio_str, eq1, eq2, grupo in RAW_FIXTURE:
        inicio = datetime.strptime(inicio_str, "%Y-%m-%d %H:%M")
        partidos.append({
            'inicio': inicio, 'fin': inicio + DUR,
            'eq1': eq1, 'eq2': eq2, 'grupo': grupo,
            'beneficio': calcular_beneficio(eq1, eq2)
        })
    return partidos


# ══════════════════════════════════════════════════════════════════
# 3. PARCIALES — FILTRADO DE CANDIDATOS
# ══════════════════════════════════════════════════════════════════

PARCIALES = [
    {"nombre": "Física 2",                  "inicio": datetime(2026,6,13, 8, 0), "fin": datetime(2026,6,13,10, 0)},
    {"nombre": "Bases de Datos",            "inicio": datetime(2026,6,15,18,10), "fin": datetime(2026,6,15,20,10)},
    {"nombre": "Investigación Operativa",   "inicio": datetime(2026,6,18,18, 5), "fin": datetime(2026,6,18,20,10)},
    {"nombre": "Coloquio TPI Simulación",   "inicio": datetime(2026,6,22,18, 0), "fin": datetime(2026,6,22,20,30)},
    {"nombre": "Diseño Sistemas Inf.",      "inicio": datetime(2026,6,24,18, 0), "fin": datetime(2026,6,24,20, 0)},
    {"nombre": "Parcial Teórico Sim.",      "inicio": datetime(2026,6,27,19, 0), "fin": datetime(2026,6,27,20, 0)},
]

def conflicto_parcial(p):
    """Retorna el nombre del parcial si el partido se superpone con él, o None."""
    for par in PARCIALES:
        if p['inicio'] < par['fin'] and p['fin'] > par['inicio']:
            return par['nombre']
    return None

def hay_superposicion(p1, p2):
    """True si los intervalos [inicio, fin) de p1 y p2 se solapan."""
    return p1['inicio'] < p2['fin'] and p1['fin'] > p2['inicio']


# ══════════════════════════════════════════════════════════════════
# 4. BACKTRACKING CON PODA
# ══════════════════════════════════════════════════════════════════

def backtracking(partidos):
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
    """
    n = len(partidos)

    # Precomputar dp_suf: DP hacia atrás para cota exacta
    # dp_suf[i] = WIS óptimo sobre partidos[i..n-1] sin restricción previa
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

    dp_suf = [0.0] * (n + 1)
    for i in range(n - 1, -1, -1):
        nc = next_compat_from(i)
        dp_suf[i] = max(partidos[i]['beneficio'] + dp_suf[nc], dp_suf[i + 1])

    mejor = {'b': 0.0, 'sel': []}
    nodos = [0]
    NINF = datetime(1900, 1, 1)   # sentinela para "ningún partido seleccionado aún"

    def bt(idx, sel, b_acum, ultimo_fin):
        nodos[0] += 1

        if b_acum > mejor['b']:
            mejor['b'] = b_acum
            mejor['sel'] = list(sel)

        if idx >= n:
            return

        # Poda 2: cota superior no mejora al mejor actual
        if b_acum + dp_suf[idx] <= mejor['b']:
            return

        p = partidos[idx]

        # Rama INCLUIR: solo si el partido empieza después del último seleccionado
        if p['inicio'] >= ultimo_fin:
            sel.append(p)
            bt(idx + 1, sel, b_acum + p['beneficio'], p['fin'])
            sel.pop()

        # Rama NO INCLUIR
        bt(idx + 1, sel, b_acum, ultimo_fin)

    bt(0, [], 0.0, NINF)
    return mejor['sel'], round(mejor['b'], 3), nodos[0]


# ══════════════════════════════════════════════════════════════════
# 5. PROGRAMACIÓN DINÁMICA — Weighted Interval Scheduling
# ══════════════════════════════════════════════════════════════════

def programacion_dinamica(partidos):
    """
    Solución óptima por Programación Dinámica (Weighted Interval Scheduling).

    Definición:
        dp[i] = máximo beneficio acumulable considerando los partidos 0..i

    Función de compatibilidad p(i):
        Índice del último partido j < i tal que fin[j] <= inicio[i].
        Calculado con búsqueda binaria → O(log n) por llamada.

    Recurrencia:
        dp[i] = max( b[i] + dp[p(i)],   dp[i-1] )
                     └─ incluir i ─┘    └─ omitir i ─┘

    La subestructura óptima se verifica porque:
        - Si i está en la solución óptima S*, entonces S* \ {i} es óptimo para p(i).
        - Si i no está en S*, entonces S* es óptimo para i-1.

    Reconstrucción de la solución: recorrido hacia atrás sobre dp[].

    Complejidad: O(n log n) — dominada por el ordenamiento y las búsquedas binarias.

    Parámetros:
        partidos: lista ordenada por hora de fin (requerido por la recurrencia).
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

    dp = [0.0] * n
    dp[0] = partidos[0]['beneficio']
    for i in range(1, n):
        j = ultimo_compatible(i)
        incluir    = partidos[i]['beneficio'] + (dp[j] if j >= 0 else 0.0)
        no_incluir = dp[i - 1]
        dp[i] = max(incluir, no_incluir)

    # Reconstrucción
    seleccion = []
    i = n - 1
    while i >= 0:
        j = ultimo_compatible(i)
        incluir = partidos[i]['beneficio'] + (dp[j] if j >= 0 else 0.0)
        if i == 0 or incluir >= dp[i - 1]:
            seleccion.append(partidos[i])
            i = j
        else:
            i -= 1

    seleccion.reverse()
    return seleccion, round(dp[n - 1], 3)


# ══════════════════════════════════════════════════════════════════
# 6. ALGORITMOS ÁVIDOS
# ══════════════════════════════════════════════════════════════════

def avido_mayor_beneficio(partidos):
    """
    Criterio ávido: seleccionar en cada paso el partido disponible
    con mayor beneficio que no entre en conflicto con los ya elegidos.

    Función de selección: argmax b_i sobre los candidatos restantes.

    Complejidad: O(n²) — ordenamiento + verificación de compatibilidad.

    NOTA IMPORTANTE:
        Este criterio NO garantiza solución óptima para Weighted Interval
        Scheduling. El contraejemplo al final del programa lo demuestra.
        Sin embargo, en la práctica produce soluciones de buena calidad
        y es significativamente más rápido que BT y DP para grandes n.
    """
    candidatos = sorted(partidos, key=lambda x: -x['beneficio'])
    seleccion, b_total = [], 0.0
    for p in candidatos:
        if all(not hay_superposicion(p, s) for s in seleccion):
            seleccion.append(p)
            b_total += p['beneficio']
    seleccion.sort(key=lambda x: x['inicio'])
    return seleccion, round(b_total, 3)

def avido_menor_fin(partidos):
    """
    Criterio ávido clásico: seleccionar el partido que termina más temprano
    y que sea compatible con los ya elegidos.

    Función de selección: argmin fin_i sobre los candidatos restantes.

    Complejidad: O(n log n) — dominada por el ordenamiento.

    Este criterio es ÓPTIMO cuando todos los beneficios son iguales
    (maximiza la cantidad de partidos vistos). Con pesos distintos,
    puede sacrificar beneficio para incluir más partidos de bajo atractivo.
    """
    candidatos = sorted(partidos, key=lambda x: x['fin'])
    seleccion, b_total = [], 0.0
    ultimo_fin = datetime(1900, 1, 1)
    for p in candidatos:
        if p['inicio'] >= ultimo_fin:
            seleccion.append(p)
            b_total += p['beneficio']
            ultimo_fin = p['fin']
    return seleccion, round(b_total, 3)


# ══════════════════════════════════════════════════════════════════
# 7. CONTRAEJEMPLO PARA EL ÁVIDO
# ══════════════════════════════════════════════════════════════════

def mostrar_contraejemplo():
    """
    Demuestra que el criterio 'mayor beneficio' no es óptimo para WIS.

    Construcción:
        A: [16:00–17:45]  b = 6.0   (ESP vs ARG)
        B: [16:30–18:15]  b = 8.5   (FRA vs BRA)  ← el ávido lo elige primero
        C: [18:00–19:45]  b = 7.0   (POR vs ENG)

        A∩B = True   (se solapan → incompatibles)
        B∩C = True   (se solapan → incompatibles)
        A∩C = False  (compatibles: A termina 17:45, C empieza 18:00)

    Decisión del ávido:
        Paso 1 → elige B (mayor b=8.5). B bloquea A y C.
        Resultado: {B} → beneficio = 8.5

    Solución óptima:
        Elegir A + C → beneficio = 6.0 + 7.0 = 13.0

    Pérdida: 13.0 − 8.5 = 4.5 unidades de beneficio.
    """
    A = {'eq1':'ESP','eq2':'ARG','grupo':'Ejemplo',
         'inicio':datetime(2026,6,20,16, 0),'fin':datetime(2026,6,20,17,45),'beneficio':6.0}
    B = {'eq1':'FRA','eq2':'BRA','grupo':'Ejemplo',
         'inicio':datetime(2026,6,20,16,30),'fin':datetime(2026,6,20,18,15),'beneficio':8.5}
    C = {'eq1':'POR','eq2':'ENG','grupo':'Ejemplo',
         'inicio':datetime(2026,6,20,18, 0),'fin':datetime(2026,6,20,19,45),'beneficio':7.0}
    ej = [A, B, C]

    print("  Partidos del contraejemplo:")
    for p in ej:
        print(f"    {p['eq1']} vs {p['eq2']}  "
              f"[{p['inicio'].strftime('%H:%M')}–{p['fin'].strftime('%H:%M')}]  b={p['beneficio']}")

    print(f"\n  Superposiciones:")
    print(f"    A ∩ B = {hay_superposicion(A,B)}    "
          f"B ∩ C = {hay_superposicion(B,C)}    "
          f"A ∩ C = {hay_superposicion(A,C)}")

    sel_av, ben_av = avido_mayor_beneficio(ej)
    sel_dp, ben_dp = programacion_dinamica(ej)

    av_str = ' + '.join(p['eq1']+' vs '+p['eq2'] for p in sel_av)
    dp_str = ' + '.join(p['eq1']+' vs '+p['eq2'] for p in sel_dp)

    print(f"\n  Ávido elige : {av_str}  →  b = {ben_av}")
    print(f"  Óptimo (DP) : {dp_str}  →  b = {ben_dp}")
    print(f"\n  Pérdida ávido = {round(ben_dp - ben_av, 1)} unidades ({round((1-ben_av/ben_dp)*100,1)}% peor)")
    print("  Conclusión: el ávido de mayor beneficio NO es óptimo para WIS.")


# ══════════════════════════════════════════════════════════════════
# 8. EJECUCIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════

def fmt(p):
    fecha = f"{p['inicio'].strftime('%d/%m %H:%M')}–{p['fin'].strftime('%H:%M')}"
    equipos = f"{p['eq1']} vs {p['eq2']}"
    return f"  │ {fecha:<17} │ {equipos:^11} │ {p['grupo']:<9} │ b = {p['beneficio']:>5.3f} │"

def main():
    W = 68
    print("═"*W)
    print("  OPTIMIZACIÓN DE AGENDA TELEVISIVA — MUNDIAL 2026")
    print(f"  Fórmula atractivo: b_i = {ALPHA}·h_i + {BETA}·t_i + {GAMMA}·l_i")
    print("═"*W)

    # ── Preparar dataset ──────────────────────────────────────────
    todos     = parse_fixture()
    candidatos, excluidos = [], []
    for p in todos:
        conf = conflicto_parcial(p)
        if conf:
            excluidos.append((p, conf))
        else:
            candidatos.append(p)

    print(f"\n  Partidos totales fase de grupos : {len(todos)}")
    print(f"  Excluidos por parciales         : {len(excluidos)}")
    for p, nombre in excluidos:
        print(f"    ✗  {p['eq1']} vs {p['eq2']}"
              f"  [{p['inicio'].strftime('%d/%m %H:%M')}]  → {nombre}")
    print(f"  Candidatos disponibles          : {len(candidatos)}\n")

    # Ordenar por hora de fin (requerido por DP y BT)
    cands = sorted(candidatos, key=lambda x: x['fin'])

    # ── Backtracking ──────────────────────────────────────────────
    print("─"*W)
    print("  ▶ 1. BACKTRACKING  (poda conflicto + cota superior exacta)")
    print("─"*W)
    t0 = time.perf_counter()
    sel_bt, ben_bt, nodos = backtracking(cands)
    t_bt = time.perf_counter() - t0
    print(f"  Nodos explorados : {nodos:,}   |   Tiempo: {t_bt*1000:.1f} ms")
    print(f"  Partidos elegidos: {len(sel_bt)}   |   Beneficio total: {ben_bt}")
    for p in sorted(sel_bt, key=lambda x: x['inicio']):
        print(fmt(p))

    # ── Programación Dinámica ─────────────────────────────────────
    print("\n" + "─"*W)
    print("  ▶ 2. PROGRAMACIÓN DINÁMICA  (Weighted Interval Scheduling)")
    print("─"*W)
    t0 = time.perf_counter()
    sel_dp, ben_dp = programacion_dinamica(cands)
    t_dp = time.perf_counter() - t0
    print(f"  Tiempo: {t_dp*1000:.2f} ms")
    print(f"  Partidos elegidos: {len(sel_dp)}   |   Beneficio total: {ben_dp}")
    for p in sorted(sel_dp, key=lambda x: x['inicio']):
        print(fmt(p))

    # ── Ávido mayor beneficio ─────────────────────────────────────
    print("\n" + "─"*W)
    print("  ▶ 3a. ÁVIDO — mayor beneficio primero  (heurístico, no óptimo)")
    print("─"*W)
    t0 = time.perf_counter()
    sel_av1, ben_av1 = avido_mayor_beneficio(cands)
    t_av1 = time.perf_counter() - t0
    print(f"  Tiempo: {t_av1*1000:.2f} ms")
    print(f"  Partidos elegidos: {len(sel_av1)}   |   Beneficio total: {ben_av1}")
    for p in sorted(sel_av1, key=lambda x: x['inicio']):
        print(fmt(p))

    # ── Ávido menor fin ───────────────────────────────────────────
    print("\n" + "─"*W)
    print("  ▶ 3b. ÁVIDO — menor hora de fin  (óptimo en cantidad, no en beneficio)")
    print("─"*W)
    t0 = time.perf_counter()
    sel_av2, ben_av2 = avido_menor_fin(cands)
    t_av2 = time.perf_counter() - t0
    print(f"  Tiempo: {t_av2*1000:.2f} ms")
    print(f"  Partidos elegidos: {len(sel_av2)}   |   Beneficio total: {ben_av2}")
    for p in sorted(sel_av2, key=lambda x: x['inicio']):
        print(fmt(p))

    # ── Tabla comparativa ─────────────────────────────────────────
    print("\n" + "═"*W)
    print("  COMPARACIÓN DE RESULTADOS")
    print("═"*W)
    print(f"  {'Técnica':<44} {'Partidos':>8} {'Beneficio':>10} {'Gap':>7}")
    print(f"  {'─'*44} {'─'*8} {'─'*10} {'─'*7}")
    print(f"  {'Backtracking (exacto)':<44} {len(sel_bt):>8} {ben_bt:>10.3f} {'—':>7}")
    print(f"  {'Prog. Dinámica (exacto)':<44} {len(sel_dp):>8} {ben_dp:>10.3f} {'—':>7}")
    gap1 = (1 - ben_av1/ben_dp)*100 if ben_dp else 0
    gap2 = (1 - ben_av2/ben_dp)*100 if ben_dp else 0
    print(f"  {'Ávido mayor beneficio (heurístico)':<44} {len(sel_av1):>8} {ben_av1:>10.3f} {gap1:>6.1f}%")
    print(f"  {'Ávido menor fin (heurístico)':<44} {len(sel_av2):>8} {ben_av2:>10.3f} {gap2:>6.1f}%")

    # Verificar consistencia BT ↔ DP
    assert abs(ben_bt - ben_dp) < 0.001, \
        f"ERROR: BT ({ben_bt}) y DP ({ben_dp}) no coinciden."
    print(f"\n  ✓ BT y DP coinciden → solución óptima verificada.")

    # ── Contraejemplo ─────────────────────────────────────────────
    print("\n" + "═"*W)
    print("  CONTRAEJEMPLO: por qué el ávido NO garantiza el óptimo en WIS")
    print("═"*W)
    mostrar_contraejemplo()
    print()

    # ── Fixture Final Recomendado ─────────────────────────────────
    print("\n" + "═"*W)
    print("  FIXTURE FINAL RECOMENDADO (SOLUCIÓN ÓPTIMA)")
    print("═"*W)
    print(f"  Este es el calendario exacto de los {len(sel_dp)} partidos que podrás ver:")
    print("─"*W)
    for p in sorted(sel_dp, key=lambda x: x['inicio']):
        print(fmt(p))
    print("═"*W)
    print(f"  Atractivo total acumulado: {ben_dp:.3f}")
    print("═"*W + "\n")

if __name__ == '__main__':
    main()
