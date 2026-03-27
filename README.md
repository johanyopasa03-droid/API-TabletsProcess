# API Validación Costos Tablets 📱

API REST en Python/FastAPI que centraliza la lógica de validación de costos
para tablets Samsung y Lenovo, simplificando tu automatización en Make.

---

## 🚀 Instalación local

```bash
# 1. Crear entorno virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar
python main.py
# → API disponible en http://localhost:8000
# → Docs interactivas en http://localhost:8000/docs
```

---

## 🔗 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/validar-costos` | Valida UNA tablet |
| POST | `/validar-costos-lote` | Valida ARRAY de tablets (ideal para Make) |
| GET  | `/tabla-costos` | Consulta tabla de costos vigente |
| GET  | `/docs` | Documentación interactiva Swagger |

---

## 📦 Ejemplo de Request

```json
POST /validar-costos-lote
Content-Type: application/json

[
  {
    "serial_id": "HA1A2G8B",
    "estado_recibido": "Dañado",
    "tipo_dano": "Daño de Display",
    "forro": "Sí",
    "cargador": "Sí",
    "observaciones": "revisar costos",
    "restablecimiento_fabrica": "Sí",
    "bloqueo_pin": "Sí",
    "fecha_envio": "2026-03-27T18:25:31.722Z"
  }
]
```

## 📦 Ejemplo de Response

```json
{
  "procesados": 1,
  "errores": 0,
  "resultados": [
    {
      "serial_id": "HA1A2G8B",
      "marca": "Samsung",
      "modelo": "HA1A2G8B",
      "fecha_procesado": "2026-03-27T18:30:00Z",
      "estado_recibido": "Dañado",
      "items": [
        { "concepto": "Revisión general", "aplica": true, "costo": 20000, "observacion": "Costo fijo" },
        { "concepto": "Reparación: Daño de Display", "aplica": true, "costo": 280000, "observacion": "Según tabla Samsung" },
        { "concepto": "Reposición de cargador", "aplica": false, "costo": 0, "observacion": "Cargador entregado ✓" },
        { "concepto": "Reposición de forro/estuche", "aplica": false, "costo": 0, "observacion": "Forro entregado ✓" },
        { "concepto": "Gestión desbloqueo PIN", "aplica": true, "costo": 40000, "observacion": "Tablet llegó con PIN activo" },
        { "concepto": "Restablecimiento de fábrica", "aplica": true, "costo": 0, "observacion": "Proceso requerido" }
      ],
      "costo_total": 340000,
      "resumen": "Tablet Samsung | Serial: HA1A2G8B | Novedades: Daño de Display, PIN activo, requiere reset | Costo total: $340,000",
      "requiere_atencion": [
        "🖥️ Display dañado - coordinar con proveedor de repuestos",
        "⚠️ Tablet con PIN de bloqueo activo - requiere gestión con el usuario",
        "🔄 Requiere restablecimiento de fábrica antes de asignar"
      ]
    }
  ],
  "detalle_errores": []
}
```

---

## ⚙️ Integración en Make (paso a paso)

### Flujo simplificado:
```
Webhooks → HTTP (POST a tu API) → Router simple (éxito/error) → Google Sheets / Email
```

### Paso 1 – Nodo HTTP en Make
- **Módulo**: `HTTP > Make a request`
- **URL**: `https://TU-DOMINIO.com/validar-costos-lote`
- **Método**: `POST`
- **Headers**: `Content-Type: application/json`
- **Body**: mapea el array del webhook directamente

```
Body (raw JSON):
{{body}}
```

O si recibes un objeto único del formulario:
```json
[{{body}}]
```

### Paso 2 – Parsear respuesta en Make
Del response de la API usas directamente:
- `resultados[0].costo_total` → para registrar en Excel
- `resultados[0].items` → para el detalle del acta
- `resultados[0].resumen` → para el email
- `resultados[0].requiere_atencion` → para alertas condicionales
- `resultados[0].marca` → para el Router (Samsung/Lenovo)

### Paso 3 – Router simplificado (solo 2 condiciones)
```
Router:
├── Éxito (procesados > 0) → Registrar en Sheets + Generar Acta + Email
└── Error (errores > 0)    → Email de alerta al administrador
```

---

## ☁️ Despliegue en producción (opciones gratuitas)

### Opción A – Railway (recomendado, más fácil)
```bash
# 1. Crear cuenta en railway.app
# 2. Conectar repo de GitHub
# 3. Railway detecta Python automáticamente
# 4. Variable de entorno: PORT=8000
```

### Opción B – Render
```bash
# 1. Crear cuenta en render.com
# 2. New Web Service → conectar repo
# 3. Build Command: pip install -r requirements.txt
# 4. Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Opción C – Servidor propio / VPS
```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## 🔧 Configurar costos desde Excel (opcional)

En `costos.py` puedes reemplazar `TABLA_COSTOS` por una lectura real de Excel:

```python
import openpyxl

def cargar_costos_desde_excel(ruta: str) -> dict:
    wb = openpyxl.load_workbook(ruta)
    ws = wb.active
    costos = {"samsung": {}, "lenovo": {}}
    for row in ws.iter_rows(min_row=2, values_only=True):
        marca, concepto, valor = row[0], row[1], row[2]
        costos[marca.lower()][concepto] = valor
    return costos
```

---

## 🔑 Detectar marca por serial

En `costos.py` ajusta `MARCAS_SERIAL` con los prefijos reales de tus seriales:

```python
MARCAS_SERIAL = {
    "samsung": ["SM-", "SAM", "GT-", "HA1", "HA2"],
    "lenovo":  ["LEN", "TB-", "ZA", "LEV"],
}
```
