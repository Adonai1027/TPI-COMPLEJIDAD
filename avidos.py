from datetime import datetime

def hay_superposicion(p1, p2):
    """True si los intervalos [inicio, fin) de p1 y p2 se solapan."""
    return p1['inicio'] < p2['fin'] and p1['fin'] > p2['inicio']

def avido_mayor_beneficio(partidos, presupuesto_max):
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
    e_usado = 0
    for p in candidatos:
        if e_usado + p['costo'] <= presupuesto_max and all(not hay_superposicion(p, s) for s in seleccion):
            seleccion.append(p)
            b_total += p['beneficio']
            e_usado += p['costo']
    seleccion.sort(key=lambda x: x['inicio'])
    return seleccion, round(b_total, 3)

def avido_menor_fin(partidos, presupuesto_max):
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
    e_usado = 0
    for p in candidatos:
        if p['inicio'] >= ultimo_fin and e_usado + p['costo'] <= presupuesto_max:
            seleccion.append(p)
            b_total += p['beneficio']
            ultimo_fin = p['fin']
            e_usado += p['costo']
    return seleccion, round(b_total, 3)
