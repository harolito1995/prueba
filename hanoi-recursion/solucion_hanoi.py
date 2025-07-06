# -*- coding: utf-8 -*-

"""
Solución para el problema de las Torres de Hanoi con restricción de colores.
"""

# Colores ANSI para mejorar la presentación visual
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(title):
    """Imprime un encabezado atractivo"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}")
    print(f"🎯 {title}")
    print(f"{'='*60}{Colors.ENDC}\n")

def print_discos(discos):
    """Imprime los discos de forma visual"""
    print(f"{Colors.OKCYAN}📦 Discos iniciales:{Colors.ENDC}")
    for i, (tamaño, color) in enumerate(discos, 1):
        emoji_color = "🔴" if color == "red" else "🔵" if color == "blue" else "🟡"
        print(f"   {emoji_color} Disco {i}: Tamaño {tamaño}, Color {color}")
    print()

def print_resultado(resultado):
    """Imprime el resultado de forma visual"""
    if resultado == -1:
        print(f"{Colors.FAIL}❌ RESULTADO: IMPOSIBLE{Colors.ENDC}")
        print(f"{Colors.WARNING}💡 No existe una solución válida para esta configuración de discos.{Colors.ENDC}")
    else:
        print(f"{Colors.OKGREEN}✅ RESULTADO: POSIBLE{Colors.ENDC}")
        print(f"{Colors.OKBLUE}📋 Secuencia de movimientos ({len(resultado)} pasos):{Colors.ENDC}")
        for i, (tamaño, origen, destino) in enumerate(resultado, 1):
            print(f"   {i:2d}. Mover disco de tamaño {tamaño} de {origen} → {destino}")
    print()

def print_separator():
    """Imprime un separador visual"""
    print(f"{Colors.HEADER}{'─'*60}{Colors.ENDC}")

def torres_hanoi_colores(discos):
    """
    Función principal para resolver el problema.

    Args:
        discos (list): Una lista de tuplas, donde cada tupla es (tamaño, color).

    Returns:
        list or int: Una lista de movimientos o -1 si es imposible.
    """
    n = len(discos)
    # Las varillas se representan como listas. La varilla A (origen) tiene todos los discos.
    varillas = {
        'A': list(reversed(discos)), # Los discos se apilan de mayor a menor tamaño
        'B': [],
        'C': []
    }
    movimientos = []
    
    # Llamamos a la función auxiliar recursiva
    es_posible = resolver_hanoi_recursivo(n, 'A', 'C', 'B', varillas, movimientos)

    if es_posible:
        return movimientos
    else:
        # Si la función recursiva devuelve False, significa que no hay solución.
        return -1

def resolver_hanoi_recursivo(n, origen, destino, auxiliar, varillas, movimientos):
    """
    Función recursiva para mover los discos.

    Args:
        n (int): Número de discos a mover.
        origen (str): Nombre de la varilla de origen ('A', 'B', 'C').
        destino (str): Nombre de la varilla de destino.
        auxiliar (str): Nombre de la varilla auxiliar.
        varillas (dict): El estado actual de las varillas.
        movimientos (list): La lista para registrar los movimientos.

    Returns:
        bool: True si el movimiento es posible, False en caso contrario.
    """
    # Caso base: si no hay discos que mover, terminamos.
    if n == 0:
        return True

    # Mover n-1 discos de la varilla origen a la auxiliar
    if not resolver_hanoi_recursivo(n - 1, origen, auxiliar, destino, varillas, movimientos):
        return False

    # Mover el disco n-ésimo de la varilla origen a la destino
    disco_a_mover = varillas[origen][-1]
    
    # Validación: ¿Se puede colocar el disco en la varilla de destino?
    if varillas[destino]:
        disco_superior_destino = varillas[destino][-1]
        # Restricción de tamaño
        if disco_a_mover[0] > disco_superior_destino[0]:
            return False # No se puede colocar un disco grande sobre uno pequeño
        # Restricción de color
        if disco_a_mover[1] == disco_superior_destino[1]:
            return False # No se puede colocar sobre un disco del mismo color

    # Si el movimiento es válido, lo ejecutamos y registramos
    disco = varillas[origen].pop()
    varillas[destino].append(disco)
    movimientos.append((disco[0], origen, destino))

    # Mover los n-1 discos de la varilla auxiliar a la destino
    if not resolver_hanoi_recursivo(n - 1, auxiliar, destino, origen, varillas, movimientos):
        return False

    return True


# --- EJECUCIÓN DE PRUEBA ---

if __name__ == "__main__":
    print_header("TORRES DE HANOI CON RESTRICCIÓN DE COLORES")
    
    # Ejemplo de Entrada 1
    print_header("EJEMPLO 1: Caso Posible")
    n1 = 3
    discos1 = [(3, "red"), (2, "blue"), (1, "red")]
    print_discos(discos1)
    resultado1 = torres_hanoi_colores(discos1)
    print_resultado(resultado1)
    
    print_separator()
    
    # Ejemplo de Entrada 2 (Caso imposible)
    print_header("EJEMPLO 2: Caso Imposible")
    n2 = 3
    discos2 = [(3, "red"), (2, "red"), (1, "blue")]
    print_discos(discos2)
    resultado2 = torres_hanoi_colores(discos2)
    print_resultado(resultado2)
    
    print_separator()
    
    # Ejemplo adicional para mostrar más casos
    print_header("EJEMPLO 3: Caso con 4 Discos")
    n3 = 4
    discos3 = [(4, "blue"), (3, "red"), (2, "blue"), (1, "red")]
    print_discos(discos3)
    resultado3 = torres_hanoi_colores(discos3)
    print_resultado(resultado3)
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 ¡Análisis completado!{Colors.ENDC}\n")
