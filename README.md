[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/4GweuraT)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23707584&assignment_repo_type=AssignmentRepo)
# Práctica 10. Estrategias para la construcción de algoritmos I

## Objetivo general
Implementar, contrastar y analizar tres estrategias de diseño de algoritmos:

- Fuerza bruta
- Algoritmo ávido (greedy)
- Estrategia incremental

El equipo deberá justificar, con evidencia experimental, cuándo una estrategia es adecuada y cuándo no produce resultados óptimos.

## Sesión de clase relacionada

En las sesiones previas al inicio de esta práctica se estudió el **problema de ordenar un arreglo lineal** y el grupo dedujo colectivamente el algoritmo de **insertion sort**. También se practicó un método para estimar el comportamiento de la función de tiempo de ejecución $T(n)$ a partir de mediciones experimentales. Esta práctica aprovecha esas dos experiencias:

- **Insertion sort** es revisitado como ejemplo canónico de la estrategia incremental. Su análisis de complejidad sirve de referencia para comparar con los otros dos algoritmos.
- El **método experimental** —medir $T(n)$ para valores crecientes de $n$, calcular razones $T(2n)/T(n)$ y estimar la clase de crecimiento— se aplica a los tres algoritmos de la práctica.

## Competencias a desarrollar
Al finalizar la práctica, el equipo será capaz de:

- Modelar un problema y elegir una estrategia algorítmica apropiada.
- Implementar soluciones correctas en Python con mediciones reproducibles.
- Analizar complejidad temporal y comportamiento empírico.
- Comparar soluciones subóptimas vs óptimas en casos concretos.
- Comunicar resultados técnicos con tablas, gráficas y conclusiones argumentadas.

## Requisitos técnicos
- Python 3.10 o superior.
- Bibliotecas permitidas: itertools, time, random, math, statistics, matplotlib (opcional para gráficas).
- Entorno sugerido: VS Code.

## Entregables
- Código fuente organizado por módulos (sus repositorios).
- Reporte técnico con código fuente organizado, metodología, resultados y conclusiones.
- Evidencia de ejecución (capturas o bitácora de terminal).

## Estructura sugerida de carpetas
```text
practica_10/
  src/
    fuerza_bruta.py
    greedy_cambio.py
    incremental_insertion.py
    experimento.py
  data/
    pruebas.json
  reporte/
    reporte.pdf
```

---

## Parte 0. Marco metodológico: estimación experimental de complejidad

Antes de trabajar cada algoritmo, familiarízate con este procedimiento. Lo aplicarás en las Partes 1, 2 y 3.

### 0.1 Medición de tiempo en Python

```python
import time

inicio = time.perf_counter()
resultado = funcion_a_medir(entrada)
fin = time.perf_counter()
t = fin - inicio  # tiempo en segundos
```

Para obtener mediciones estables, repite cada experimento al menos **5 veces** y reporta el promedio (o el mínimo para eliminar el ruido del sistema operativo).

### 0.2 Test de doblamiento

Ejecuta el algoritmo con tamaños n, 2n, 4n, 8n, … Calcula la **razón de doblamiento**:

$$r(n) = \frac{T(2n)}{T(n)}$$

Interpreta el valor de r:

| r aproximado | Clase de complejidad |
|:---:|:---|
| ≈ 1 | O(1) – constante |
| ≈ 2 | O(n) – lineal |
| ≈ 4 | O(n²) – cuadrático |
| ≈ 8 | O(n³) – cúbico |
| crece sin límite | O(kⁿ) – exponencial |

### 0.3 Modelo de tabla para el reporte

Para cada algoritmo, completa una tabla de esta forma al registrar tus experimentos:

| n | T(n) mejor caso (s) | T(n) peor caso (s) | r = T(2n_peor)/T(n_peor) | Clase estimada |
|---:|---:|---:|:---:|:---|
| … | | | — | |
| … | | | | |

### 0.4 Verificación matemática

Después del experimento, analiza el código del algoritmo:

1. Identifica los **bucles** (o la recursión) y su número máximo de iteraciones en función de n.
2. Escribe T(n) como una suma de términos.
3. Aplica la **regla del término dominante**: conserva sólo el de mayor crecimiento.
4. Expresa el resultado en notación **Big O**.

> **Definición informal de Big O:** T(n) = O(f(n)) si existen constantes c > 0 y n₀ ≥ 1 tales que T(n) ≤ c · f(n) para todo n ≥ n₀. Dicho de otra forma: f(n) es una **cota superior** del crecimiento de T(n).

---

## Parte 1. Fuerza bruta: búsqueda exhaustiva

### Marco conceptual
La estrategia de fuerza bruta explora exhaustivamente todas las posibilidades hasta encontrar una solución. Su ventaja principal es la simplicidad y su principal limitante es el costo computacional.

### Descubrimiento guiado

Responde en equipo antes de implementar:

1. **Escenario:** Olvidaste el PIN de 3 dígitos de un candado (la combinación es algún número del 000 al 999). Sin más información, ¿cuál es la única estrategia que **garantiza** encontrarlo?
2. ¿Hay alguna combinación que puedas saltarte con seguridad? ¿Por qué sí o por qué no?
3. ¿Cuántas combinaciones probarías en el **peor caso**? ¿Y en el **mejor caso**?
4. Si el PIN tuviera 4 dígitos en lugar de 3, ¿cuántas combinaciones habría? ¿En qué factor creció respecto al de 3 dígitos?
5. Generaliza: si la longitud del PIN es n dígitos (alfabeto de 10 símbolos), ¿cuántos intentos son necesarios en el peor caso? Expresa la respuesta en función de n y del tamaño del alfabeto |Σ|.

La estrategia que describiste es **fuerza bruta**: explorar el espacio de soluciones de forma sistemática y exhaustiva, sin atajos. Es **completa** (siempre encuentra una solución si existe) pero tiene **costo exponencial** en el parámetro de entrada.

### Problema A (implementación)
Implementa un generador de candidatos de longitud fija para un alfabeto dado usando producto cartesiano.

Requisitos:
- Usa itertools.product.
- Permite longitudes de 1 hasta n.
- Detén la búsqueda al encontrar una cadena objetivo.
- Registra:
  - Total de candidatos probados.
  - Tiempo total.
  - Tasa de prueba (candidatos/segundo).

Firma sugerida:
```python
def buscar_cadena_objetivo(objetivo: str, alfabeto: str, min_len: int = 1):
    """Regresa (encontrada, intentos, tiempo_segundos)."""
```

### Problema B (análisis de crecimiento)
Para cada configuración, estima el número teórico de combinaciones:

$$
\sum_{k=min}^{n} |\Sigma|^k
$$

Donde $|\Sigma|$ es el tamaño del alfabeto y $n$ la longitud máxima.

Configura experimentos con:
- Alfabeto 1: dígitos (10 símbolos)
- Alfabeto 2: letras minúsculas (26 símbolos)
- Longitudes máximas: 3, 4, 5

Entrega una tabla con:
- Combinaciones teóricas
- Tiempo medido
- Observación de escalamiento

### Problema C (optimización de poda)
Implementa una variante con poda por prefijo usando un conjunto de prefijos válidos.

Objetivo:
- Mostrar cómo una restricción de dominio reduce drásticamente la exploración.

Debes reportar:
- Tiempo sin poda
- Tiempo con poda
- Reducción porcentual

### Problema D – Análisis de complejidad: fuerza bruta

**D.1 – Experimento de doblamiento**

Usando `buscar_cadena_objetivo` sobre el alfabeto de dígitos (|Σ| = 10), busca siempre el **peor caso**: un objetivo que sea la última cadena revisada para la longitud indicada (p. ej., la cadena `"999…9"` de longitud n).

Completa la tabla (usa el módulo `time.perf_counter` tal como se describe en la Parte 0):

| Longitud n | Candidatos teóricos (acumulado) | T(n) medido (s) | Razón T(n)/T(n−1) |
|:---:|---:|---:|:---:|
| 1 | 10 | | — |
| 2 | 110 | | |
| 3 | 1 110 | | |
| 4 | 11 110 | | |
| 5 | 111 110 | | |

¿Hacia qué valor converge la razón a medida que n crece? ¿Qué clase de crecimiento sugiere eso?

**D.2 – Deducción matemática (cota superior)**

El número total de candidatos para cadenas de longitud 1 hasta n con alfabeto Σ es:

$$
C(n) = \sum_{k=1}^{n} |\Sigma|^k = |\Sigma| \cdot \frac{|\Sigma|^n - 1}{|\Sigma| - 1}
$$

El término dominante es $|\Sigma|^n$, por lo que:

$$
T_{\text{peor}}(n) = O\!\left(|\Sigma|^n\right) \quad \text{(exponencial en } n\text{)}
$$

1. Verifica numéricamente: para |Σ| = 10 y n = 5, ¿cuántos candidatos hay? ¿Coincide con tu tabla?
2. Escribe la **cota superior** de la fuerza bruta en notación Big O.
3. Si duplicas la longitud (de n a 2n), ¿en qué factor crece el número de candidatos?
4. Con |Σ| = 26 (letras minúsculas) y la tasa de exploración que mediste (candidatos/segundo), estima a partir de qué longitud n el tiempo de ejecución superaría 1 minuto, 1 hora y 1 año.

---

## Parte 2. Algoritmos ávidos: cambio de monedas

### Marco conceptual
La estrategia greedy toma decisiones locales (moneda de mayor valor disponible) con la expectativa de acercarse a la mejor solución global. No siempre garantiza optimalidad.

### Descubrimiento guiado

Trabaja estos escenarios en equipo antes de implementar:

1. **Caja registradora:** Debes devolver $\$11$ de cambio. Dispones de monedas de [1, 2, 5, 10, 20]. ¿Qué moneda usas primero? ¿Por qué esa y no otra?
2. Aplica la misma decisión en cada paso hasta llegar a $\$0$. ¿Cuántas monedas usaste en total?
3. Describe la regla que seguiste en una oración: *"En cada paso, tomo la moneda…"*
4. Ahora prueba con monedas [1, 3, 4] y monto $\$6$. Aplica exactamente la misma regla. ¿Cuántas monedas?
5. Busca manualmente la solución con **menor número de monedas** para $\$6$ con [1, 3, 4]. ¿Es la misma que produjo la regla?
6. ¿Qué falla cuando el sistema de monedas no es "canónico"?

La estrategia **ávida (greedy)** elige la opción localmente óptima en cada paso. Es muy eficiente, pero no garantiza la solución globalmente óptima en todos los casos.

### Problema A (implementación greedy)
Implementa el problema de cambio de monedas:

Entrada:
- Monto entero positivo
- Denominaciones enteras positivas

Salida:
- Lista de monedas usadas
- Conteo total de monedas

Condiciones:
- Ordena denominaciones de mayor a menor.
- Usa división entera y residuo.
- Si no hay solución exacta, informa fallo.

Firma sugerida:
```python
def cambio_greedy(monto: int, monedas: list[int]):
    """Regresa (solucion, total_monedas) o None si no hay solución exacta."""
```

### Problema B (referencia óptima)
Implementa una solución óptima por programación dinámica para comparar con greedy.

Firma sugerida:
```python
def cambio_optimo_dp(monto: int, monedas: list[int]):
    """Regresa una solución de mínimo número de monedas o None."""
```

### Problema C (contraejemplos)
Evalúa ambos enfoques en dos sistemas de monedas:

Sistema 1 (canónico):
- [1, 2, 5, 10, 20, 50]

Sistema 2 (no canónico):
- [1, 3, 4]

Para montos del 1 al 60, calcula:
- Casos donde greedy = óptimo
- Casos donde greedy es subóptimo
- Máxima diferencia en número de monedas

Incluye al menos 3 montos concretos donde greedy falle en el sistema no canónico.

### Problema D (discusión técnica)
Responde en el reporte:
- Por qué greedy funciona bien en algunos sistemas monetarios y falla en otros.
- Qué propiedad estructural del sistema influye en la optimalidad.

### Problema E – Análisis de complejidad: algoritmo ávido

**E.1 – Experimento empírico**

Mide `cambio_greedy` y `cambio_optimo_dp` para montos crecientes m. Para cada monto, llama a la función **500 veces** consecutivas y divide el tiempo total entre 500 para obtener el tiempo promedio por llamada (en microsegundos).

| Monto m | T_greedy (µs) | T_dp (µs) | Razón T_dp / T_greedy |
|---:|---:|---:|---:|
| 100 | | | |
| 1 000 | | | |
| 10 000 | | | |
| 100 000 | | | |

Aplica el test de doblamiento sólo a `cambio_optimo_dp`:

| m | T_dp (µs) | Razón T_dp(2m) / T_dp(m) |
|---:|---:|:---:|
| 1 000 | | — |
| 2 000 | | |
| 4 000 | | |
| 8 000 | | |

¿La razón converge a 2? ¿Qué sugiere eso sobre la complejidad de `cambio_optimo_dp`?

**E.2 – Deducción matemática**

Analiza el núcleo de cada función (k = número de denominaciones, constante en la práctica):

`cambio_greedy`:

```
sorted(monedas, reverse=True)   →  O(k log k)
for moneda in monedas_ord:      →  k iteraciones
─────────────────────────────────────────────────────
T_greedy = O(k log k) = O(1)   (k es constante, independiente de m)
```

`cambio_optimo_dp`:

```
for i in range(1, m + 1):       →  m iteraciones
    for moneda in monedas:      →  k iteraciones
─────────────────────────────────────────────────────
T_dp = O(m · k) = O(m)         (con k constante)
```

1. ¿Por qué `cambio_greedy` tiene complejidad O(1) respecto al monto m?
2. Verifica en la tabla de E.1: ¿el tiempo de `cambio_greedy` crece al aumentar m? ¿Y el de `cambio_optimo_dp`?
3. ¿Qué implica "O(1)" sobre la escalabilidad del algoritmo ávido para montos muy grandes?
4. ¿La mayor velocidad de greedy justifica siempre su uso en lugar de DP? ¿Cuándo no?

---

## Parte 3. Estrategia incremental: insertion sort instrumentado

### Marco conceptual
La estrategia incremental construye la solución gradualmente. Insertion sort mantiene un prefijo ordenado y coloca cada nuevo elemento en su posición correcta.

### Conexión con la sesión de clase

En clase dedujiste **insertion sort** a partir de la pregunta: *"¿cómo ordenarías estas tarjetas numéricas desordenadas?"* El proceso que describiste naturalmente fue:

1. Toma la carta en la posición 1 e insértala antes o después de la carta en posición 0, según su valor.
2. Toma la carta en la posición 2 e insértala en el lugar correcto dentro del segmento ya ordenado.
3. Repite hasta que el prefijo ordenado cubra todo el arreglo.

Esa estrategia —mantener un **prefijo ordenado** y expandirlo elemento a elemento— es la **estrategia incremental**.

### Descubrimiento guiado: traza manual

Antes de escribir código, ordena $[5, 2, 7, 1, 4]$ aplicando insertion sort a mano y registra cuántas comparaciones y movimientos realizas en cada paso:

| Paso i | Arreglo antes del paso | Llave | Comparaciones | Movimientos | Arreglo después del paso |
|:---:|---|:---:|:---:|:---:|---|
| 1 | [5, 2, 7, 1, 4] | 2 | | | |
| 2 | | 7 | | | |
| 3 | | 1 | | | |
| 4 | | 4 | | | |
| **Total** | | | | | **[1, 2, 4, 5, 7]** |

Responde antes de continuar:

- ¿Cuántas comparaciones y movimientos hiciste en total?
- Si el arreglo ya estuviera ordenado $[1, 2, 4, 5, 7]$, ¿cuántas comparaciones necesitarías?
- Si estuviera en orden inverso $[7, 5, 4, 2, 1]$, ¿cuántas?
- ¿Qué relación hay entre esas cantidades y n (el tamaño del arreglo)?

### Problema A (implementación base)
Implementa insertion sort y registra métricas:
- Comparaciones
- Movimientos (asignaciones/desplazamientos)
- Tiempo

Firma sugerida:
```python
def insertion_sort_metricas(arr: list[int]):
    """Regresa (arreglo_ordenado, comparaciones, movimientos, tiempo_segundos)."""
```

### Problema B (escenarios de entrada)
Genera arreglos de tamaño n en tres escenarios:
- Mejor caso: ya ordenado
- Promedio: aleatorio
- Peor caso: inversamente ordenado

Usa tamaños: 1000, 2000, 4000, 8000.

Para cada caso registra:
- Comparaciones
- Movimientos
- Tiempo

### Problema C (validación teórica y Big O)
Contrasta resultados con complejidades esperadas:
- Mejor caso: $\Theta(n)$
- Promedio: $\Theta(n^2)$
- Peor caso: $\Theta(n^2)$

Incluye una gráfica de tiempo vs tamaño por escenario (opcional con matplotlib, obligatorio al menos en tabla).

**C.1 – Test de doblamiento (peor caso)**

Completa con los datos de `medir_escenarios`:

| n | T_peor (s) | Razón T_peor(2n) / T_peor(n) | Clase estimada |
|---:|---:|:---:|:---|
| 1 000 | | — | |
| 2 000 | | | |
| 4 000 | | | |
| 8 000 | | | |

¿La razón se aproxima a 2 o a 4? ¿Coincide con lo que dedujiste a mano en la traza manual?

**C.2 – Deducción matemática del peor caso**

Analiza el doble bucle de insertion sort:

```
for i in 1 .. n−1:                        ← n−1 iteraciones externas
    while j ≥ 0 and arr[j] > llave:       ← hasta i iteraciones internas
        desplaza arr[j]
        j -= 1
```

En el **peor caso** (arreglo en orden inverso), el while itera exactamente i veces para cada paso i:

$$
T_{\text{peor}}(n) = \sum_{i=1}^{n-1} i = \frac{n(n-1)}{2}
$$

El término dominante es $n^2/2$, por lo que:

$$
T_{\text{peor}}(n) = O(n^2)
$$

**C.3 – Deducción matemática del mejor caso**

Si el arreglo ya está ordenado, el while nunca ejecuta su cuerpo (la primera comparación siempre falla):

$$
T_{\text{mejor}}(n) = \sum_{i=1}^{n-1} 1 = n - 1 \implies T_{\text{mejor}}(n) = O(n)
$$

Verifica: para n = 8 000 en el mejor caso, ¿cuántas comparaciones registra tu implementación? ¿Es ≈ 7 999?

**C.4 – Cota superior como garantía de peor caso**

La cota superior garantiza que para **cualquier** arreglo de n elementos:

$$
T_{\text{insertion sort}}(n) = O(n^2)
$$

Estima la **constante oculta** c tal que $T_{\text{peor}}(n) \approx c \cdot n^2$ a partir de tus mediciones:

| n | T_peor (s) | c = T_peor / n² |
|---:|---:|---:|
| 1 000 | | |
| 2 000 | | |
| 4 000 | | |
| 8 000 | | |

¿Es c aproximadamente constante entre los distintos valores de n? ¿Qué factores del hardware o del sistema operativo podrían hacerla variar?

### Problema D (mejora incremental)
Implementa una versión híbrida:
- Si el tamaño del subarreglo es menor que un umbral t, usa insertion sort.
- Si es mayor, usa merge sort o quicksort (implementación propia o estándar documentada).

Evalúa valores de t en {8, 16, 32, 64} y reporta el mejor para tus datos.

---

## Parte 4. Síntesis: comparación de complejidades

### Problema A – Cuadro comparativo

Con los datos recolectados en las Partes 1, 2 y 3, completa el cuadro (las celdas experimentales son las que tú mides):

| Algoritmo | Estrategia | Parámetro n | T(n) mejor caso | T(n) peor caso | Big O peor caso |
|-----------|-----------|:---:|:---:|:---:|:---:|
| Búsqueda exhaustiva | Fuerza bruta | longitud cadena | O(1) | O(\|Σ\|ⁿ) | **exponencial** |
| Cambio greedy | Ávida | monto m (k fijo) | O(1) | O(1) | **constante** |
| Cambio DP | Programación dinámica | monto m (k fijo) | O(m) | O(m·k) | **lineal** |
| Insertion sort | Incremental | tamaño arreglo n | O(n) | O(n²) | **cuadrático** |

### Problema B – Predicción y verificación experimental

Usando la constante c que estimaste en la Parte 3, Problema C.4:

1. **Predice** el tiempo de ejecución de insertion sort para n = 16 000 en el peor caso: $T_{\text{pred}} = c \cdot (16\,000)^2$.
2. **Mide** experimentalmente $T_{\text{peor}}(16\,000)$ con `medir_escenarios([16000])`.
3. Reporta el **error porcentual**: $\varepsilon = |T_{\text{pred}} - T_{\text{med}}| / T_{\text{med}} \times 100\%$.

Este experimento ilustra la utilidad práctica del análisis de complejidad: permite **predecir** el comportamiento para entradas grandes antes de ejecutar el programa.

### Problema C – Análisis crítico

Responde en el reporte técnico:

1. ¿Por qué la fuerza bruta es exponencial mientras que insertion sort (otro algoritmo "simple") es cuadrático? ¿Qué diferencia estructural explica eso?
2. Greedy para cambio de monedas resulta O(1) respecto al monto. ¿Ese resultado depende de que k (número de denominaciones) sea una constante pequeña? ¿Qué pasaría si k también creciera con m?
3. En la práctica, Python usa Timsort (merge sort + insertion sort). ¿Para qué tamaños de subarreglo conviene usar insertion sort dentro de ese algoritmo? ¿Por qué O(n²) puede ser preferible a O(n log n) en esos casos?
4. Diseña un escenario real donde:
   - La fuerza bruta sea la **única opción razonable** (no hay estructura que explotar).
   - Greedy sea **preferible a DP**, aunque no garantice optimalidad.
   - Insertion sort supere a algoritmos de O(n log n).

### Problema D – Reflexión: el caso integrador (del manual MADO-19)

Un sistema de validación debe: (1) buscar códigos cortos bajo un patrón restringido, (2) asignar cambio con denominaciones no estándar, (3) mantener una lista casi ordenada de eventos en tiempo real.

Para cada subproblema:
- Elige la estrategia más adecuada y justifica con el análisis de complejidad que realizaste.
- Propón una alternativa si la primera elección falla o produce resultados subóptimos.
- Indica la **cota superior** de tiempo de ejecución de tu solución propuesta.

---

## Criterios de evaluación (100 puntos)
- Corrección funcional de implementaciones: 25
- Calidad del análisis experimental (tablas de doblamiento, escenarios, tasa de exploración): 25
- Deducción matemática de Big O (por cada uno de los tres algoritmos, 5 pts c/u): 15
- Comparación crítica entre estrategias (Parte 4): 15
- Claridad del reporte técnico: 10
- Calidad de código (estructura, nombres, pruebas): 10

Penalizaciones:
- Resultados experimentales sin evidencia reproducible: -10
- Conclusiones sin datos que las respalden: -10
- Big O afirmado sin deducción algebraica: -5
- Código sin modularidad mínima: -5

---

## Rúbrica mínima de pruebas
Cada módulo debe incluir, como mínimo:
- 5 casos de prueba válidos.
- 2 casos frontera.
- 1 caso inválido con manejo explícito de error.

Sugerencia de validaciones:
- Entradas vacías.
- Tipos incorrectos.
- Montos imposibles de construir.
- Arreglos con repetidos y negativos.

---

## Preguntas guía para discusión final
- ¿Cuándo conviene una solución simple y exhaustiva aunque sea computacionalmente cara?
- ¿Cuál es el riesgo de asumir que greedy siempre produce la solución óptima?
- ¿Por qué insertion sort sigue siendo útil en arreglos pequeños o casi ordenados, a pesar de ser O(n²)?
- ¿Qué relación hay entre el análisis Big O y la predicción práctica del tiempo de ejecución?
- ¿En qué sentido el "mejor caso" y el "peor caso" son cotas distintas de la misma función T(n)?
- ¿Cómo cambiaría la cota superior de insertion sort si se garantizara que el arreglo de entrada siempre tiene a lo sumo k elementos fuera de lugar (con k constante pequeño)?
- ¿Puede un algoritmo con Big O más grande ser preferible en la práctica a uno con Big O más pequeño? ¿Bajo qué condiciones?

---

## Extensiones opcionales (extra)
- Paralelizar la exploración de fuerza bruta por bloques.
- Diseñar un detector automático de sistemas monetarios donde greedy no es óptimo (en un rango de montos).
- Comparar insertion sort con timsort (sorted de Python) en entradas parcialmente ordenadas.

---

## Bibliografía base recomendada
- Introducción a la sección de estrategias en MADO-19 (páginas 130 a 136).
- Cormen, Leiserson, Rivest, Stein. Introduction to Algorithms.
- Miller y Ranum. Problem Solving with Algorithms and Data Structures using Python.
- Documentación oficial de Python:
  - itertools.product
  - lectura y escritura de archivos
  - medición de tiempo (time/perf_counter)
