"""
Módulo de cálculo de costos para tablets Samsung y Lenovo.
Aquí defines todos los costos según marca y novedad.
Puedes reemplazar los valores estáticos por una consulta real a Excel/Google Sheets.
"""
from datetime import datetime

# ─────────────────────────────────────────────
# TABLA DE COSTOS (ajusta los valores según tu Excel)
# Estructura: TABLA_COSTOS[marca][concepto] = costo
# ─────────────────────────────────────────────
TABLA_COSTOS = {
    "samsung": {
        "daño_display": 548000,
        "daño_visor": 372400,
        "sin_cargador": 90000,
        "bloqueo_pin": 175733,
        "restablecimiento_fabrica": 0,   # sin costo adicional
    },
    "lenovo": {
        "daño_display": 100000,
        "daño_visor": 100000,
        "sin_cargador": 90000,
        "bloqueo_pin": 133333,
        "restablecimiento_fabrica": 0,
    }
}

# Palabras clave para identificar marca desde el serial
MARCAS_SERIAL = {
    "samsung": ["SM-", "SAM", "GT-", "HA1", "HA2", "HA3"],  # añade prefijos reales
    "lenovo":  ["LEN", "TB-", "ZA", "LEV"],
}

# Campos que generan alertas de atención
ALERTAS_CONFIG = {
    "bloqueo_pin": "⚠️ Tablet con PIN de bloqueo activo - requiere gestión con el usuario",
    "restablecimiento_fabrica": "🔄 Requiere restablecimiento de fábrica antes de asignar",
    "daño_display": "🖥️ Display dañado - coordinar con proveedor de repuestos",
    "daño_visor": "🔍 Visor dañado - coordinar con proveedor de repuestos",
}


def detectar_marca(serial_id: str) -> str:
    """Detecta la marca de la tablet según el serial."""
    serial_upper = serial_id.upper()
    for marca, prefijos in MARCAS_SERIAL.items():
        if any(serial_upper.startswith(p) or p in serial_upper for p in prefijos):
            return marca
    # Si no detecta, lanza error claro
    raise ValueError(
        f"No se pudo determinar la marca para el serial '{serial_id}'. "
        f"Prefijos reconocidos: Samsung {MARCAS_SERIAL['samsung']}, Lenovo {MARCAS_SERIAL['lenovo']}"
    )


def normalizar_tipo_dano(tipo_dano: str | None) -> str:
    """Normaliza el campo tipo_daño a una clave interna."""
    if not tipo_dano:
        return "sin_dano"
    td = tipo_dano.lower().strip()
    if "display" in td:
        return "daño_display"
    elif "visor" in td:
        return "daño_visor"
    return "sin_dano"


def calcular_costos_tablet(datos: dict) -> dict:
    """
    Lógica central: recibe el dict del formulario y retorna
    el desglose completo de costos.
    """
    serial_id       = datos["serial_id"]
    estado          = datos.get("estado_recibido", "Buen Estado")
    tipo_dano       = datos.get("tipo_dano", "")
    tiene_forro     = datos.get("forro", "No").strip().lower() in ["sí", "si", "yes", "1", "true"]
    tiene_cargador  = datos.get("cargador", "No").strip().lower() in ["sí", "si", "yes", "1", "true"]
    tiene_pin       = datos.get("bloqueo_pin", "No").strip().lower() in ["sí", "si", "yes", "1", "true"]
    restablecer     = datos.get("restablecimiento_fabrica", "No").strip().lower() in ["sí", "si", "yes", "1", "true"]

    marca = detectar_marca(serial_id)
    costos_marca = TABLA_COSTOS[marca]
    tipo_dano_key = normalizar_tipo_dano(tipo_dano)

    items = []
    alertas = []
    
    # ── 2. Daño de pantalla ───────────────────────────────────────────
    if tipo_dano_key in ["daño_display", "daño_visor"]:
        costo_dano = costos_marca[tipo_dano_key]
        items.append({
            "concepto": f"Reparación: {tipo_dano or tipo_dano_key.replace('_', ' ').title()}",
            "aplica": True,
            "costo": costo_dano,
            "observacion": f"Según tabla de costos {marca.title()}"
        })
        for key in ["daño_display", "daño_visor"]:
            if key in tipo_dano_key:
                alertas.append(ALERTAS_CONFIG.get(key, ""))
    else:
        items.append({
            "concepto": "Reparación de pantalla",
            "aplica": False,
            "costo": 0,
            "observacion": "Sin daño de display o visor reportado"
        })

    # ── 3. Cargador faltante ──────────────────────────────────────────
    if not tiene_cargador:
        items.append({
            "concepto": "Reposición de cargador",
            "aplica": True,
            "costo": costos_marca["sin_cargador"],
            "observacion": "No entregó cargador con la tablet"
        })
    else:
        items.append({
            "concepto": "Reposición de cargador",
            "aplica": False,
            "costo": 0,
            "observacion": "Cargador entregado ✓"
        })

    # ── 4. Forro faltante ─────────────────────────────────────────────
    if not tiene_forro:
        items.append({
            "concepto": "Reposición de forro/estuche",
            "aplica": True,
            "costo": costos_marca["sin_forro"],
            "observacion": "No entregó forro con la tablet"
        })
    else:
        items.append({
            "concepto": "Reposición de forro/estuche",
            "aplica": False,
            "costo": 0,
            "observacion": "Forro entregado ✓"
        })

    # ── 5. Bloqueo PIN ────────────────────────────────────────────────
    if tiene_pin:
        items.append({
            "concepto": "Gestión desbloqueo PIN",
            "aplica": True,
            "costo": costos_marca["bloqueo_pin"],
            "observacion": "Tablet llegó con PIN activo"
        })
        alertas.append(ALERTAS_CONFIG["bloqueo_pin"])
    else:
        items.append({
            "concepto": "Gestión desbloqueo PIN",
            "aplica": False,
            "costo": 0,
            "observacion": "Sin bloqueo PIN ✓"
        })

    # ── 6. Restablecimiento de fábrica ────────────────────────────────
    if restablecer:
        items.append({
            "concepto": "Restablecimiento de fábrica",
            "aplica": True,
            "costo": costos_marca["restablecimiento_fabrica"],
            "observacion": "Proceso requerido antes de asignación"
        })
        alertas.append(ALERTAS_CONFIG["restablecimiento_fabrica"])
    else:
        items.append({
            "concepto": "Restablecimiento de fábrica",
            "aplica": False,
            "costo": 0,
            "observacion": "No requerido"
        })

    # ── Totales ───────────────────────────────────────────────────────
    costo_total = sum(item["costo"] for item in items if item["aplica"])

    resumen_partes = []
    if tipo_dano_key != "sin_dano":
        resumen_partes.append(tipo_dano or "daño pantalla")
    if not tiene_cargador:
        resumen_partes.append("sin cargador")
    if not tiene_forro:
        resumen_partes.append("sin forro")
    if tiene_pin:
        resumen_partes.append("PIN activo")
    if restablecer:
        resumen_partes.append("requiere reset")

    resumen = (
        f"Tablet {marca.title()} | Serial: {serial_id} | "
        f"Novedades: {', '.join(resumen_partes) if resumen_partes else 'Ninguna'} | "
        f"Costo total: ${costo_total:,.0f}"
    )

    return {
        "serial_id": serial_id,
        "marca": marca.title(),
        "modelo": serial_id,
        "fecha_procesado": datetime.utcnow().isoformat() + "Z",
        "estado_recibido": estado,
        "items": items,
        "costo_total": costo_total,
        "resumen": resumen,
        "requiere_atencion": [a for a in alertas if a],
    }
