# =============================================================
#  SISTEMA DE GESTION DE SUPERMERCADO
#  Algoritmos y Estructuras de Datos - ISI - Ciclo 2026
#  Escenario 12: Gestion de Supermercado
# =============================================================

import os
from datetime import datetime

# -------------------------------------------------------------
# DATOS INICIALES DE PRODUCTOS (catalogo del supermercado)
# -------------------------------------------------------------
# Estructura: { codigo: [nombre, precio, categoria] }
CATALOGO = {
    "001": ["Leche 1L",        150.00, "Lacteos"],
    "002": ["Yogur Natural",    90.00, "Lacteos"],
    "003": ["Pan de Molde",    120.00, "Panaderia"],
    "004": ["Medialunas x6",   200.00, "Panaderia"],
    "005": ["Manzanas 1kg",    180.00, "Frutas y Verduras"],
    "006": ["Bananas 1kg",     130.00, "Frutas y Verduras"],
    "007": ["Arroz 1kg",       250.00, "Almacen"],
    "008": ["Fideos 500g",     140.00, "Almacen"],
    "009": ["Aceite 900ml",    450.00, "Almacen"],
    "010": ["Gaseosa 2L",      350.00, "Bebidas"],
    "011": ["Agua Mineral 2L",  80.00, "Bebidas"],
    "012": ["Jabon en Polvo",  600.00, "Limpieza"],
    "013": ["Detergente 500ml",280.00, "Limpieza"],
    "014": ["Shampoo 400ml",   380.00, "Higiene"],
    "015": ["Papel Higienico", 320.00, "Higiene"],
}

# Promociones activas: { codigo_producto: porcentaje_descuento }
PROMOCIONES = {
    "007": 10,   # Arroz 10% off
    "010": 15,   # Gaseosa 15% off
    "012": 20,   # Jabon en Polvo 20% off
}

# Medios de pago disponibles
MEDIOS_PAGO = {
    "1": "Efectivo",
    "2": "Debito",
    "3": "Credito",
}

# Descuento adicional por medio de pago
DESCUENTO_PAGO = {
    "1": 5,   # 5% descuento en efectivo
    "2": 0,
    "3": 0,
}

# Archivo donde se guardan las ventas del dia
ARCHIVO_VENTAS = "ventas.txt"

# Archivo donde se guarda el catalogo de productos
ARCHIVO_PRODUCTOS = "productos.txt"


# =============================================================
#  FUNCIONES DE ARCHIVOS
# =============================================================

def guardar_venta_en_archivo(numero_ticket, items, subtotal,
                              descuento_promo, descuento_pago_monto,
                              total, medio_pago):
    """
    Guarda el detalle de una venta en el archivo ventas.txt.
    Args:
        numero_ticket (int): numero de ticket de la venta
        items (list): lista de productos vendidos
        subtotal (float): subtotal antes de descuentos
        descuento_promo (float): monto descontado por promociones
        descuento_pago_monto (float): monto descontado por medio de pago
        total (float): total final a pagar
        medio_pago (str): medio de pago utilizado
    """
    try:
        with open(ARCHIVO_VENTAS, "a", encoding="utf-8") as archivo:
            archivo.write("=" * 40 + "\n")
            archivo.write(f"TICKET #{numero_ticket}\n")
            archivo.write(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
            archivo.write("-" * 40 + "\n")
            for item in items:
                archivo.write(
                    f"  {item['nombre']:<22} x{item['cantidad']}  "
                    f"${item['subtotal']:.2f}\n"
                )
            archivo.write("-" * 40 + "\n")
            archivo.write(f"Subtotal:          ${subtotal:.2f}\n")
            if descuento_promo > 0:
                archivo.write(f"Desc. promociones: -${descuento_promo:.2f}\n")
            if descuento_pago_monto > 0:
                archivo.write(f"Desc. {medio_pago:<13}  -${descuento_pago_monto:.2f}\n")
            archivo.write(f"TOTAL:             ${total:.2f}\n")
            archivo.write(f"Pago con:          {medio_pago}\n")
            archivo.write("=" * 40 + "\n\n")
    except OSError as e:
        print(f"  [!] No se pudo guardar la venta en el archivo: {e}")


def guardar_catalogo_en_archivo():
    """
    Guarda el catalogo de productos en productos.txt.
    """
    try:
        with open(ARCHIVO_PRODUCTOS, "w", encoding="utf-8") as archivo:
            archivo.write("CATALOGO DE PRODUCTOS\n")
            archivo.write("=" * 45 + "\n")
            archivo.write(f"{'COD':<5} {'PRODUCTO':<25} {'PRECIO':>8}  CATEGORIA\n")
            archivo.write("-" * 45 + "\n")
            for codigo, datos in CATALOGO.items():
                nombre, precio, categoria = datos
                promo = f" [{PROMOCIONES[codigo]}% OFF]" if codigo in PROMOCIONES else ""
                archivo.write(
                    f"{codigo:<5} {nombre:<25} ${precio:>7.2f}  {categoria}{promo}\n"
                )
        print("  Catalogo guardado en 'productos.txt'.")
    except OSError as e:
        print(f"  [!] No se pudo guardar el catalogo: {e}")


def leer_ventas_del_archivo():
    """
    Lee y devuelve el contenido del archivo de ventas.
    Returns:
        str: contenido del archivo o mensaje de error
    """
    try:
        with open(ARCHIVO_VENTAS, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
            if not contenido.strip():
                return "  No hay ventas registradas todavia."
            return contenido
    except FileNotFoundError:
        return "  No hay ventas registradas todavia."
    except OSError as e:
        return f"  [!] Error al leer el archivo: {e}"


# =============================================================
#  FUNCIONES DE VISUALIZACION
# =============================================================

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_encabezado(titulo):
    """
    Muestra un encabezado formateado.
    Args:
        titulo (str): titulo a mostrar
    """
    print("=" * 45)
    print(f"  {titulo}")
    print("=" * 45)


def mostrar_menu_principal():
    """Muestra el menu principal del sistema."""
    limpiar_pantalla()
    mostrar_encabezado("SUPERMERCADO - SISTEMA DE GESTION")
    print("  1. Nueva compra (abrir caja)")
    print("  2. Ver catalogo de productos")
    print("  3. Ver historial de ventas del dia")
    print("  4. Ver estadisticas")
    print("  5. Guardar catalogo en archivo")
    print("  0. Salir")
    print("=" * 45)


def mostrar_catalogo():
    """Muestra todos los productos disponibles en pantalla."""
    limpiar_pantalla()
    mostrar_encabezado("CATALOGO DE PRODUCTOS")
    print(f"  {'COD':<5} {'PRODUCTO':<23} {'PRECIO':>8}  PROMO")
    print("  " + "-" * 42)
    categoria_actual = ""
    for codigo, datos in CATALOGO.items():
        nombre, precio, categoria = datos
        if categoria != categoria_actual:
            print(f"\n  --- {categoria} ---")
            categoria_actual = categoria
        promo_texto = f"{PROMOCIONES[codigo]}% OFF" if codigo in PROMOCIONES else ""
        print(f"  {codigo:<5} {nombre:<23} ${precio:>7.2f}  {promo_texto}")
    print()


def mostrar_ticket(numero_ticket, items, subtotal,
                   descuento_promo, descuento_pago_monto, total, medio_pago):
    """
    Muestra el ticket final de la compra en pantalla.
    Args:
        numero_ticket (int): numero de ticket
        items (list): productos del carrito
        subtotal (float): subtotal sin descuentos
        descuento_promo (float): descuento por promociones
        descuento_pago_monto (float): descuento por medio de pago
        total (float): total a pagar
        medio_pago (str): metodo de pago elegido
    """
    print()
    print("=" * 45)
    print(f"  TICKET #{numero_ticket} - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 45)
    for item in items:
        print(
            f"  {item['nombre']:<22} x{item['cantidad']}  "
            f"${item['subtotal']:.2f}"
        )
    print("-" * 45)
    print(f"  Subtotal:          ${subtotal:.2f}")
    if descuento_promo > 0:
        print(f"  Desc. promociones: -${descuento_promo:.2f}")
    if descuento_pago_monto > 0:
        print(f"  Desc. {medio_pago:<13}  -${descuento_pago_monto:.2f}")
    print(f"  TOTAL A PAGAR:     ${total:.2f}")
    print(f"  Pago con:          {medio_pago}")
    print("=" * 45)


# =============================================================
#  FUNCIONES DE VALIDACION
# =============================================================

def validar_entero_positivo(texto_input):
    """
    Valida que el input sea un entero mayor a 0.
    Args:
        texto_input (str): string ingresado por el usuario
    Returns:
        int o None: el entero si es valido, None si no lo es
    """
    try:
        valor = int(texto_input)
        if valor > 0:
            return valor
        print("  [!] Debe ingresar un numero mayor a cero.")
        return None
    except ValueError:
        print("  [!] Ingrese solo numeros enteros.")
        return None


def validar_opcion_menu(opcion, opciones_validas):
    """
    Valida que la opcion elegida este dentro de las permitidas.
    Args:
        opcion (str): opcion ingresada
        opciones_validas (list): lista de opciones aceptadas
    Returns:
        bool: True si es valida
    """
    if opcion not in opciones_validas:
        print(f"  [!] Opcion invalida. Ingrese: {', '.join(opciones_validas)}")
        return False
    return True


def validar_codigo_producto(codigo):
    """
    Verifica si el codigo existe en el catalogo.
    Args:
        codigo (str): codigo ingresado
    Returns:
        bool: True si existe en el catalogo
    """
    if codigo not in CATALOGO:
        print(f"  [!] Codigo '{codigo}' no encontrado en el catalogo.")
        return False
    return True


# =============================================================
#  FUNCIONES DE LOGICA DE NEGOCIO
# =============================================================

def calcular_precio_con_promo(codigo, precio_unitario, cantidad):
    """
    Calcula el subtotal aplicando promocion si corresponde.
    Args:
        codigo (str): codigo del producto
        precio_unitario (float): precio sin descuento
        cantidad (int): unidades
    Returns:
        tuple: (subtotal_final, monto_descuento)
    """
    subtotal_bruto = precio_unitario * cantidad
    if codigo in PROMOCIONES:
        porcentaje = PROMOCIONES[codigo]
        descuento = subtotal_bruto * porcentaje / 100
        return subtotal_bruto - descuento, descuento
    return subtotal_bruto, 0.0


def agregar_producto_al_carrito(carrito, codigo, cantidad):
    """
    Agrega un producto al carrito o incrementa su cantidad si ya existe.
    Args:
        carrito (list): lista actual de items
        codigo (str): codigo del producto
        cantidad (int): cantidad a agregar
    Returns:
        float: monto de descuento por promocion aplicado
    """
    nombre, precio, _ = CATALOGO[codigo]
    subtotal, descuento = calcular_precio_con_promo(codigo, precio, cantidad)

    # Buscar si el producto ya esta en el carrito
    for item in carrito:
        if item["codigo"] == codigo:
            item["cantidad"] += cantidad
            item["subtotal"] += subtotal
            if descuento > 0:
                print(f"  Promocion aplicada: {PROMOCIONES[codigo]}% de descuento!")
            return descuento

    # Si no estaba, agregarlo
    carrito.append({
        "codigo": codigo,
        "nombre": nombre,
        "cantidad": cantidad,
        "subtotal": subtotal,
    })
    if descuento > 0:
        print(f"  Promocion aplicada: {PROMOCIONES[codigo]}% de descuento!")
    return descuento


def mostrar_carrito(carrito):
    """
    Muestra el estado actual del carrito de compras.
    Args:
        carrito (list): lista de items en el carrito
    """
    if not carrito:
        print("  El carrito esta vacio.")
        return
    print("\n  --- Carrito actual ---")
    for item in carrito:
        print(
            f"  {item['nombre']:<22} x{item['cantidad']}  ${item['subtotal']:.2f}"
        )
    total_parcial = sum(i["subtotal"] for i in carrito)
    print(f"  {'Total parcial':<26} ${total_parcial:.2f}")
    print()


def elegir_medio_de_pago():
    """
    Solicita al usuario que elija el medio de pago.
    Returns:
        tuple: (clave_medio, nombre_medio, porcentaje_descuento)
    """
    print("\n  --- Medio de pago ---")
    for clave, nombre in MEDIOS_PAGO.items():
        descuento = DESCUENTO_PAGO[clave]
        extra = f"  ({descuento}% descuento)" if descuento > 0 else ""
        print(f"  {clave}. {nombre}{extra}")

    while True:
        opcion = input("  Elija medio de pago: ").strip()
        if validar_opcion_menu(opcion, list(MEDIOS_PAGO.keys())):
            return opcion, MEDIOS_PAGO[opcion], DESCUENTO_PAGO[opcion]


def procesar_compra(carrito, descuento_promo_total, numero_ticket):
    """
    Calcula totales, aplica descuento por pago y cierra la venta.
    Args:
        carrito (list): items de la compra
        descuento_promo_total (float): total descontado por promociones
        numero_ticket (int): numero de ticket
    Returns:
        float: total cobrado (para acumulador de ventas del dia)
    """
    subtotal = sum(item["subtotal"] for item in carrito)
    clave_pago, nombre_pago, porc_pago = elegir_medio_de_pago()
    descuento_pago_monto = subtotal * porc_pago / 100
    total = subtotal - descuento_pago_monto

    mostrar_ticket(
        numero_ticket, carrito, subtotal,
        descuento_promo_total, descuento_pago_monto,
        total, nombre_pago
    )
    guardar_venta_en_archivo(
        numero_ticket, carrito, subtotal,
        descuento_promo_total, descuento_pago_monto,
        total, nombre_pago
    )
    print("  Venta guardada correctamente.")
    return total


# =============================================================
#  FUNCIONES DE ESTADISTICAS
# =============================================================

def mostrar_estadisticas(ventas_del_dia, contador_tickets,
                          productos_vendidos):
    """
    Muestra las estadisticas del dia en curso.
    Args:
        ventas_del_dia (float): total recaudado en el dia
        contador_tickets (int): cantidad de ventas realizadas
        productos_vendidos (dict): { nombre_producto: cantidad_total }
    """
    limpiar_pantalla()
    mostrar_encabezado("ESTADISTICAS DEL DIA")
    print(f"  Ventas realizadas:   {contador_tickets}")
    print(f"  Total recaudado:     ${ventas_del_dia:.2f}")
    if contador_tickets > 0:
        promedio = ventas_del_dia / contador_tickets
        print(f"  Ticket promedio:     ${promedio:.2f}")
    print()

    if productos_vendidos:
        print("  --- Productos mas vendidos ---")
        # Ordenar por cantidad (mayor a menor) sin usar sorted con lambda compleja
        lista_productos = list(productos_vendidos.items())
        # Ordenamiento burbuja descendente por cantidad
        n = len(lista_productos)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if lista_productos[j][1] < lista_productos[j + 1][1]:
                    lista_productos[j], lista_productos[j + 1] = (
                        lista_productos[j + 1],
                        lista_productos[j],
                    )
        for nombre, cantidad in lista_productos[:5]:
            print(f"  {nombre:<25} {cantidad} unidades")
    else:
        print("  Aun no hay productos vendidos hoy.")
    print()
    input("  Presione Enter para volver al menu...")


# =============================================================
#  FLUJO DE UNA COMPRA COMPLETA
# =============================================================

def nueva_compra(numero_ticket, productos_vendidos):
    """
    Gestiona el flujo completo de una compra: carga de productos,
    visualizacion del carrito y cierre con pago.
    Args:
        numero_ticket (int): numero de ticket actual
        productos_vendidos (dict): acumulador de productos vendidos
    Returns:
        float: total de esta venta (0 si fue cancelada)
    """
    limpiar_pantalla()
    mostrar_encabezado(f"NUEVA COMPRA - Ticket #{numero_ticket}")
    print("  Ingrese los productos de la compra.")
    print("  Escriba 'FIN' para terminar de cargar productos.")
    print("  Escriba 'VER' para ver el carrito.")
    print("  Escriba 'CANCEL' para cancelar la compra.")
    print()

    carrito = []
    descuento_promo_total = 0.0  # acumulador de descuentos por promo

    while True:
        codigo = input("  Codigo de producto: ").strip().upper()

        if codigo == "FIN":
            if not carrito:
                print("  [!] El carrito esta vacio. Compra cancelada.")
                input("  Presione Enter para volver al menu...")
                return 0.0
            break

        if codigo == "CANCEL":
            print("  Compra cancelada.")
            input("  Presione Enter para volver al menu...")
            return 0.0

        if codigo == "VER":
            mostrar_carrito(carrito)
            continue

        if not validar_codigo_producto(codigo):
            continue

        cantidad_str = input("  Cantidad: ").strip()
        cantidad = validar_entero_positivo(cantidad_str)
        if cantidad is None:
            continue

        nombre_prod = CATALOGO[codigo][0]
        descuento = agregar_producto_al_carrito(carrito, codigo, cantidad)
        descuento_promo_total += descuento

        # Acumular para estadisticas
        if nombre_prod in productos_vendidos:
            productos_vendidos[nombre_prod] += cantidad
        else:
            productos_vendidos[nombre_prod] = cantidad

        print(f"  '{nombre_prod}' agregado correctamente.")

    mostrar_carrito(carrito)
    confirmar = input("  Confirmar compra? (S/N): ").strip().upper()
    if confirmar != "S":
        print("  Compra cancelada.")
        input("  Presione Enter para volver al menu...")
        return 0.0

    total = procesar_compra(carrito, descuento_promo_total, numero_ticket)
    input("\n  Presione Enter para volver al menu...")
    return total


# =============================================================
#  PROGRAMA PRINCIPAL
# =============================================================

def main():
    """
    Funcion principal que controla el flujo del programa.
    Contiene el loop del menu principal y llama a cada modulo.
    """
    # Acumuladores del dia
    total_recaudado = 0.0       # acumulador de ventas
    contador_tickets = 0        # contador de ventas
    productos_vendidos = {}     # dict para estadisticas

    print("\n  Iniciando Sistema de Supermercado...")
    input("  Presione Enter para continuar...")

    continuar = True
    while continuar:
        mostrar_menu_principal()
        opcion = input("  Seleccione una opcion: ").strip()

        if opcion == "1":
            contador_tickets += 1
            total_venta = nueva_compra(contador_tickets, productos_vendidos)
            total_recaudado += total_venta  # acumulador

        elif opcion == "2":
            mostrar_catalogo()
            input("  Presione Enter para volver al menu...")

        elif opcion == "3":
            limpiar_pantalla()
            mostrar_encabezado("HISTORIAL DE VENTAS DEL DIA")
            print(leer_ventas_del_archivo())
            input("  Presione Enter para volver al menu...")

        elif opcion == "4":
            mostrar_estadisticas(
                total_recaudado, contador_tickets, productos_vendidos
            )

        elif opcion == "5":
            guardar_catalogo_en_archivo()
            input("  Presione Enter para volver al menu...")

        elif opcion == "0":
            print("\n  Cerrando el sistema...")
            print(f"  Ventas del dia: {contador_tickets}")
            print(f"  Total recaudado: ${total_recaudado:.2f}")
            print("  Hasta luego!\n")
            continuar = False

        else:
            print("  [!] Opcion no valida. Intente nuevamente.")
            input("  Presione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    main()
