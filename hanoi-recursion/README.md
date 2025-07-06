# Pregunta 1: Torres de Hanoi con Restricción de Colores

## 📋 Descripción

Este proyecto implementa una variante del clásico problema de las **Torres de Hanoi** con restricciones adicionales de colores. El objetivo es mover todos los discos desde la varilla A hasta la varilla C, respetando las siguientes reglas:

### Reglas del Juego
1. **Regla de tamaño**: Un disco grande no puede colocarse sobre uno pequeño
2. **Regla de color**: Un disco no puede colocarse sobre otro del mismo color
3. **Movimiento**: Solo se puede mover un disco a la vez desde la parte superior de cualquier varilla

## 🚀 Cómo Ejecutar el Proyecto

### Prerrequisitos
- Python 3.x instalado en tu sistema

### Instalación y Ejecución

1. **Clona o descarga el proyecto**
   ```bash
   git clone https://github.com/tu-usuario/technical-test-imexhs.git
   cd technical-test-imexhs/hanoi-recursion
   ```

2. **Ejecuta el programa**
   ```bash
   # En Windows
   py solucion_hanoi.py
   
   # En Linux/Mac
   python3 solucion_hanoi.py
   ```

## 📊 Ejemplos de Uso

El programa incluye tres casos de prueba predefinidos:

### Ejemplo 1: 3 Discos
```
Discos: [(3, "red"), (2, "blue"), (1, "red")]
Resultado: IMPOSIBLE
```

### Ejemplo 2: 3 Discos (Caso Imposible)
```
Discos: [(3, "red"), (2, "red"), (1, "blue")]
Resultado: IMPOSIBLE
```

### Ejemplo 3: 4 Discos
```
Discos: [(4, "blue"), (3, "red"), (2, "blue"), (1, "red")]
Resultado: IMPOSIBLE
```

## 🔧 Estructura del Código

### Funciones Principales

#### `torres_hanoi_colores(discos)`
- **Entrada**: Lista de tuplas `(tamaño, color)`
- **Salida**: Lista de movimientos o `-1` si es imposible
- **Descripción**: Función principal que inicializa el estado y llama al algoritmo recursivo

#### `resolver_hanoi_recursivo(n, origen, destino, auxiliar, varillas, movimientos)`
- **Descripción**: Implementación recursiva del algoritmo de Hanoi
- **Validaciones**: 
  - Verifica restricción de tamaño
  - Verifica restricción de color
- **Retorna**: `True` si es posible, `False` si es imposible


## 🎨 Características Visuales

El programa utiliza:
- **Colores ANSI** para mejorar la presentación
- **Emojis** para representar discos y colores:
  - 🔴 Disco rojo
  - 🔵 Disco azul
  - 🟡 Disco amarillo
- **Formato estructurado** para mostrar movimientos paso a paso

## 🧠 Algoritmo

### Estrategia Recursiva
1. **Caso base**: Si no hay discos que mover, retorna `True`
2. **Paso recursivo**:
   - Mover `n-1` discos de origen a auxiliar
   - Mover el disco `n` de origen a destino
   - Mover `n-1` discos de auxiliar a destino

### Validaciones
```python
# Restricción de tamaño
if disco_a_mover[0] > disco_superior_destino[0]:
    return False

# Restricción de color
if disco_a_mover[1] == disco_superior_destino[1]:
    return False
```

## 📈 Complejidad

- **Tiempo**: O(2^n) - Exponencial debido a la naturaleza recursiva
- **Espacio**: O(n) - Profundidad de la pila de recursión

## 🔍 Análisis de los Casos de Prueba

### ¿Por qué todos los casos son imposibles?

#### **Ejemplo 1: [(3, "red"), (2, "blue"), (1, "red")]**
**Configuración inicial:**
```
Varilla A: [🔴3, 🔵2, 🔴1] (base → tope)
Varilla B: []
Varilla C: []
```

**Análisis paso a paso:**
1. **Primer movimiento**: Para mover el disco 🔴3, necesitamos mover 🔵2 y 🔴1 a la varilla auxiliar
2. **Problema**: Al mover 🔴1 a cualquier varilla, no puede colocarse sobre 🔴3 (mismo color)
3. **Resultado**: Es imposible separar los discos rojos, bloqueando toda la solución

#### **Ejemplo 2: [(3, "red"), (2, "red"), (1, "blue")]**
**Configuración inicial:**
```
Varilla A: [🔴3, 🔴2, 🔵1] (base → tope)
Varilla B: []
Varilla C: []
```

**Análisis paso a paso:**
1. **Problema inmediato**: Los discos 🔴3 y 🔴2 no pueden apilarse juntos (mismo color)
2. **Movimiento requerido**: Para mover 🔴3, necesitamos mover 🔴2 y 🔵1
3. **Bloqueo**: 🔴2 no puede colocarse sobre 🔴3, y no hay otra varilla disponible
4. **Resultado**: Los discos rojos están bloqueados desde el inicio

#### **Ejemplo 3: [(4, "blue"), (3, "red"), (2, "blue"), (1, "red")]**
**Configuración inicial:**
```
Varilla A: [🔵4, 🔴3, 🔵2, 🔴1] (base → tope)
Varilla B: []
Varilla C: []
```

**Análisis paso a paso:**
1. **Primer movimiento**: Para mover 🔵4, necesitamos mover 🔴3, 🔵2, y 🔴1
2. **Problema de distribución**: Los discos azules (🔵4, 🔵2) no pueden apilarse juntos
3. **Limitación de varillas**: Solo tenemos 3 varillas, pero necesitamos separar 4 discos
4. **Bloqueo**: No hay forma de distribuir los discos sin violar las reglas de color
5. **Resultado**: La configuración es matemáticamente imposible

### **Conclusión General**

La restricción de colores introduce un **bloqueo fundamental** que hace imposible resolver estas configuraciones:

- **En Hanoi clásico**: Cualquier configuración de n discos es solucionable
- **Con restricción de colores**: Muchas configuraciones se vuelven imposibles porque:
  - Los discos del mismo color no pueden apilarse
  - El número limitado de varillas (3) no permite la separación necesaria
  - La recursión se bloquea en el primer paso al intentar mover discos grandes

**Teorema**: Para que una configuración sea solucionable, debe ser posible distribuir los discos del mismo color en diferentes varillas sin violar las reglas de tamaño.

## 🛠️ Personalización

Para probar con tus propios casos:

```python
# Modifica la sección de ejemplos en el archivo
discos_personalizados = [(5, "red"), (4, "blue"), (3, "red"), (2, "blue"), (1, "red")]
resultado = torres_hanoi_colores(discos_personalizados)
```

