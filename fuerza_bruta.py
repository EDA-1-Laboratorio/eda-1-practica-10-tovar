"""Fuerza Bruta (Búsqueda Exhaustiva)
======================================================
"""
import itertools
import time
import math
import statistics

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES
# ─────────────────────────────────────────────────────────────────────────────

DIGITOS      = "0123456789"                        # |Σ| = 10
MINUSCULAS   = "abcdefghijklmnopqrstuvwxyz"        # |Σ| = 26
REPETICIONES = 5   # número de repeticiones para promediar tiempos


# ─────────────────────────────────────────────────────────────────────────────
# PROBLEMA A — Generador de candidatos / búsqueda exhaustiva
# ─────────────────────────────────────────────────────────────────────────────

def buscar_cadena_objetivo(
    objetivo: str,
    alfabeto: str,
    min_len: int = 1
) -> tuple[bool, int, float]:
    """
    Busca `objetivo` generando todas las cadenas de longitud min_len hasta
    len(objetivo) sobre `alfabeto` con producto cartesiano (itertools.product).

    Parámetros
    ----------
    objetivo  : cadena que se quiere encontrar.
    alfabeto  : conjunto de símbolos permitidos (p. ej. "0123456789").
    min_len   : longitud mínima desde la que se empieza a explorar.

    Retorna
    -------
    (encontrada, intentos, tiempo_segundos)
    """
    if not objetivo:
        raise ValueError("El objetivo no puede ser una cadena vacía.")
    if not alfabeto:
        raise ValueError("El alfabeto no puede estar vacío.")
    if min_len < 1:
        raise ValueError("min_len debe ser ≥ 1.")
    if not isinstance(objetivo, str):
        raise TypeError("El objetivo debe ser de tipo str.")

    intentos   = 0
    encontrada = False
    inicio     = time.perf_counter()

    longitud_max = len(objetivo)

    for longitud in range(min_len, longitud_max + 1):
        for candidato_tuple in itertools.product(alfabeto, repeat=longitud):
            intentos += 1
            candidato = "".join(candidato_tuple)
            if candidato == objetivo:
                encontrada = True
                fin = time.perf_counter()
                tiempo = fin - inicio
                tasa = intentos / tiempo if tiempo > 0 else float("inf")
                print(
                    f"  [Encontrado] '{objetivo}' tras {intentos:,} intentos "
                    f"en {tiempo:.6f} s  ({tasa:,.0f} cand/s)"
                )
                return (encontrada, intentos, tiempo)

    fin    = time.perf_counter()
    tiempo = fin - inicio
    print(f"  [No encontrado] '{objetivo}' tras {intentos:,} intentos en {tiempo:.6f} s")
    return (False, intentos, fin - inicio)


def medir_promedio(objetivo: str, alfabeto: str, min_len: int = 1,
                   reps: int = REPETICIONES) -> tuple[bool, int, float]:
    """
    Ejecuta buscar_cadena_objetivo `reps` veces y devuelve el promedio
    de tiempo (la búsqueda es determinista, así que intentos es constante).
    """
    tiempos = []
    resultado_final = None
    for _ in range(reps):
        encontrada, intentos, t = buscar_cadena_objetivo(objetivo, alfabeto, min_len)
        tiempos.append(t)
        resultado_final = (encontrada, intentos, t)
    t_promedio = statistics.mean(tiempos)
    return (resultado_final[0], resultado_final[1], t_promedio)


# ─────────────────────────────────────────────────────────────────────────────
# PROBLEMA B — Análisis de crecimiento (combinaciones teóricas vs tiempo real)
# ─────────────────────────────────────────────────────────────────────────────

def combinaciones_teoricas(longitud_max: int, sigma: int,
                           longitud_min: int = 1) -> int:
    """
    Calcula C(n) = Σ_{k=min}^{n} |Σ|^k
    Fórmula cerrada: |Σ| * (|Σ|^n − 1) / (|Σ| − 1)  cuando min=1 y |Σ|>1.
    """
    if sigma == 1:
        return longitud_max - longitud_min + 1
    total = 0
    for k in range(longitud_min, longitud_max + 1):
        total += sigma ** k
    return total


def experimento_problema_b(
    longitudes: list[int] = [3, 4, 5],
    reps: int = REPETICIONES
) -> None:
    """
    Problema B: mide el tiempo para el peor caso en dos alfabetos
    (dígitos y letras minúsculas) con longitudes máximas 3, 4 y 5.
    El peor caso es la última cadena del espacio = alfabeto[-1] repetido n veces.
    """
    print("\n" + "=" * 70)
    print("PROBLEMA B — Análisis de crecimiento (peor caso)")
    print("=" * 70)

    configs = [
        ("Dígitos (|Σ|=10)",     DIGITOS,    "9"),
        ("Minúsculas (|Σ|=26)",  MINUSCULAS, "z"),
    ]

    for desc, alfabeto, ultimo in configs:
        print(f"\n  Alfabeto: {desc}")
        print(f"  {'Long. n':>8} | {'C(n) teórico':>16} | {'T medido (s)':>14} | Observación")
        print("  " + "-" * 60)
        t_anterior = None
        for n in longitudes:
            objetivo    = ultimo * n       # peor caso: última cadena de longitud n
            c_teorico   = combinaciones_teoricas(n, len(alfabeto))
            _, _, t_med = medir_promedio(objetivo, alfabeto, reps=reps)
            if t_anterior and t_anterior > 0:
                razon = t_med / t_anterior
                obs   = f"×{razon:.1f} vs longitud anterior"
            else:
                obs = "referencia"
            print(f"  {n:>8} | {c_teorico:>16,} | {t_med:>14.6f} | {obs}")
            t_anterior = t_med


# ─────────────────────────────────────────────────────────────────────────────
# PROBLEMA C — Optimización con poda por prefijo
# ─────────────────────────────────────────────────────────────────────────────

def buscar_con_poda(
    objetivo: str,
    alfabeto: str,
    prefijos_validos: set[str],
    min_len: int = 1
) -> tuple[bool, int, float]:
    """
    Variante con poda: si el prefijo de longitud p_len no está en
    `prefijos_validos`, se descarta toda la rama (no se generan sus extensiones).

    Parámetros
    ----------
    prefijos_validos : conjunto de prefijos permitidos de longitud fija
                       (p. ej. {"1", "2", "3"} para solo explorar cadenas
                       que comiencen con 1, 2 o 3 en el primer dígito).

    Retorna
    -------
    (encontrada, intentos, tiempo_segundos)
    """
    if not objetivo:
        raise ValueError("El objetivo no puede ser una cadena vacía.")
    if not alfabeto:
        raise ValueError("El alfabeto no puede estar vacío.")
    if prefijos_validos is None:
        raise TypeError("prefijos_validos debe ser un conjunto (set), no None.")

    longitud_max = len(objetivo)
    # Detectamos la longitud de los prefijos del conjunto (deben ser uniformes)
    p_len = len(next(iter(prefijos_validos))) if prefijos_validos else 1

    intentos   = 0
    encontrada = False
    inicio     = time.perf_counter()

    for longitud in range(min_len, longitud_max + 1):
        for candidato_tuple in itertools.product(alfabeto, repeat=longitud):
            # Poda: verifica si el prefijo de la cadena es válido
            if longitud >= p_len:
                prefijo = "".join(candidato_tuple[:p_len])
                if prefijo not in prefijos_validos:
                    continue              # rama podada ✂

            intentos += 1
            candidato = "".join(candidato_tuple)
            if candidato == objetivo:
                encontrada = True
                break
        if encontrada:
            break

    fin    = time.perf_counter()
    tiempo = fin - inicio
    return (encontrada, intentos, tiempo)


def experimento_problema_c(reps: int = REPETICIONES) -> None:
    """
    Problema C: compara tiempo sin poda vs con poda para un objetivo fijo.
    Prefijos válidos: sólo cadenas que empiezan con '5', '6' o '7'.
    Objetivo: "567" (peor caso dentro del subconjunto podado).
    """
    print("\n" + "=" * 70)
    print("PROBLEMA C — Optimización con poda por prefijo")
    print("=" * 70)

    objetivo         = "567"
    alfabeto         = DIGITOS
    prefijos_validos = {"5", "6", "7"}   # ≈ 30 % del espacio de búsqueda

    print(f"\n  Objetivo         : '{objetivo}'")
    print(f"  Alfabeto         : dígitos (|Σ|=10)")
    print(f"  Prefijos válidos : {prefijos_validos}  (long=1, 3 de 10 primeros dígitos)")

    # Sin poda
    tiempos_sin = []
    intentos_sin = 0
    for _ in range(reps):
        enc, att, t = buscar_cadena_objetivo(objetivo, alfabeto)
        tiempos_sin.append(t)
        intentos_sin = att
    t_sin = statistics.mean(tiempos_sin)

    # Con poda
    tiempos_con = []
    intentos_con = 0
    for _ in range(reps):
        enc, att, t = buscar_con_poda(objetivo, alfabeto, prefijos_validos)
        tiempos_con.append(t)
        intentos_con = att
    t_con = statistics.mean(tiempos_con)

    reduccion_intentos = (1 - intentos_con / intentos_sin) * 100 if intentos_sin else 0
    reduccion_tiempo   = (1 - t_con / t_sin)             * 100 if t_sin       else 0

    print(f"\n  {'Métrica':<28} {'Sin poda':>14} {'Con poda':>14} {'Reducción':>12}")
    print("  " + "-" * 70)
    print(f"  {'Intentos':<28} {intentos_sin:>14,} {intentos_con:>14,} {reduccion_intentos:>11.1f}%")
    print(f"  {'Tiempo promedio (s)':<28} {t_sin:>14.6f} {t_con:>14.6f} {reduccion_tiempo:>11.1f}%")


# ─────────────────────────────────────────────────────────────────────────────
# PROBLEMA D — Análisis de complejidad: experimento de doblamiento
# ─────────────────────────────────────────────────────────────────────────────

def experimento_problema_d(reps: int = REPETICIONES) -> None:
    """
    Problema D.1 — Test de doblamiento para fuerza bruta sobre dígitos.
    Peor caso: objetivo = "9" * n  (última cadena de longitud n).

    D.2 — El término dominante de C(n) es |Σ|^n; la razón T(n)/T(n-1)
    converge a |Σ| = 10, confirmando complejidad O(|Σ|^n) — exponencial.
    """
    print("\n" + "=" * 70)
    print("PROBLEMA D — Experimento de doblamiento (fuerza bruta, |Σ|=10)")
    print("=" * 70)

    longitudes = [1, 2, 3, 4, 5]
    alfabeto   = DIGITOS
    sigma      = len(alfabeto)

    print(f"\n  {'Long. n':>8} | {'Candidatos teóricos':>22} | {'T(n) medido (s)':>16} | {'Razón T(n)/T(n-1)':>18}")
    print("  " + "-" * 72)

    t_anterior = None
    for n in longitudes:
        objetivo  = "9" * n                             # peor caso
        c_teorico = combinaciones_teoricas(n, sigma)
        _, _, t_med = medir_promedio(objetivo, alfabeto, reps=reps)

        if t_anterior and t_anterior > 0:
            razon_str = f"{t_med / t_anterior:.2f}"
        else:
            razon_str = "—"

        print(f"  {n:>8} | {c_teorico:>22,} | {t_med:>16.6f} | {razon_str:>18}")
        t_anterior = t_med

    print()
    print("  Conclusión D.2 — Deducción matemática:")
    print(f"    C(n) = Σ_{{k=1}}^{{n}} {sigma}^k  ≈  {sigma}^n   (término dominante)")
    print(f"    La razón T(n)/T(n-1) converge a |Σ| = {sigma}.")
    print(f"    ∴  T_peor(n) = O({sigma}^n)  →  complejidad EXPONENCIAL.")


# ─────────────────────────────────────────────────────────────────────────────
# SECCIÓN DE PRUEBAS (rúbrica mínima exigida)
# ─────────────────────────────────────────────────────────────────────────────

def ejecutar_pruebas() -> None:
    """
    Casos de prueba mínimos solicitados en la rúbrica:
      - 5 casos válidos
      - 2 casos frontera
      - 1 caso inválido con manejo de error
    """
    print("\n" + "=" * 70)
    print("PRUEBAS UNITARIAS")
    print("=" * 70)

    errores = 0

    def check(nombre, condicion):
        nonlocal errores
        estado = "✓ PASS" if condicion else "✗ FAIL"
        if not condicion:
            errores += 1
        print(f"  {estado}  {nombre}")

    # — Casos válidos ──────────────────────────────────────────────────────────
    enc, att, _ = buscar_cadena_objetivo("5", DIGITOS)
    check("Caso 1 – dígito único '5' encontrado", enc and att == 6)

    enc, att, _ = buscar_cadena_objetivo("0", DIGITOS)
    check("Caso 2 – primer dígito '0' (mejor caso, 1 intento)", enc and att == 1)

    enc, att, _ = buscar_cadena_objetivo("az", MINUSCULAS)
    check("Caso 3 – cadena de 2 letras 'az' encontrada", enc)

    enc, _, _ = buscar_cadena_objetivo("abc", MINUSCULAS)
    check("Caso 4 – cadena de 3 letras 'abc' encontrada", enc)

    enc, att, _ = buscar_cadena_objetivo("99", DIGITOS)
    check("Caso 5 – peor caso len=2 '99' encontrado", enc and att == 110)

    # — Casos frontera ─────────────────────────────────────────────────────────
    enc, att, _ = buscar_cadena_objetivo("0", DIGITOS)
    check("Frontera 1 – cadena de longitud 1 (mínima posible)", enc and att == 1)

    enc, att, _ = buscar_cadena_objetivo("9", DIGITOS)
    check("Frontera 2 – último elemento de longitud 1 (peor caso len=1)", enc and att == 10)

    # — Caso inválido ──────────────────────────────────────────────────────────
    try:
        buscar_cadena_objetivo("", DIGITOS)
        check("Error 1 – objetivo vacío lanza ValueError", False)
    except ValueError:
        check("Error 1 – objetivo vacío lanza ValueError", True)

    print(f"\n  Resultado: {8 - errores}/8 pruebas pasadas.")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║   Práctica 10 · Parte 1: Fuerza Bruta — Búsqueda Exhaustiva    ║")
    print("╚══════════════════════════════════════════════════════════════════╝")

    ejecutar_pruebas()
    experimento_problema_b()
    experimento_problema_c()
    experimento_problema_d()

    print("\n" + "=" * 70)
    print("Fin de la Parte 1.")
    print("=" * 70)


if __name__ == "__main__":
    main()
