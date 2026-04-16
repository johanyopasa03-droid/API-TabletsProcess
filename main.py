from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn
from datetime import datetime

from costos import calcular_costos_tablet

app = FastAPI(
    title="API Validación Costos Tablets",
    description="Valida costos de reparación de tablets Samsung y Lenovo según novedades recibidas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class TabletIngreso(BaseModel):
    serial_id: str
    estado_recibido: str           # "Dañado" | "Buen Estado"
    tipo_dano: Optional[str] = None  # "Daño de Display" | "Daño de Visor" | "Daño de Display y Visor" | "Sin Daño"
    forro: Optional[str] = "No"   # "Sí" | "No"
   # cargador: Optional[str] = "No"  # "Sí" | "No"
    adaptador_carga: Optional[str] = "No"  # "Sí" | "No"
    cable: Optional[str] = "No"  # "Sí" | "No"
    observaciones: Optional[str] = ""
    restablecimiento_fabrica: Optional[str] = "No"  # "Sí" | "No"
    bloqueo_pin: Optional[str] = "No"  # "Sí" | "No"
    fecha_envio: Optional[str] = None


class ItemCosto(BaseModel):
    concepto: str
    aplica: bool
    costo: float
    observacion: Optional[str] = ""


class RespuestaCostos(BaseModel):
    serial_id: str
    marca: str
    modelo: str
    fecha_procesado: str
    estado_recibido: str
    items: list[ItemCosto]
    costo_total: float
    resumen: str
    requiere_atencion: list[str]


@app.get("/")
def root():
    return {"mensaje": "API Costos Tablets activa", "version": "1.0.0"}


@app.post("/validar-costos", response_model=RespuestaCostos)
def validar_costos(tablet: TabletIngreso):
    """
    Recibe los datos de ingreso de una tablet y retorna el desglose
    de costos según marca, tipo de daño y novedades detectadas.
    """
    try:
        resultado = calcular_costos_tablet(tablet.dict())
        return resultado
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


@app.post("/validar-costos-lote")
def validar_costos_lote(tablets: list[TabletIngreso]):
    """
    Procesa múltiples tablets en un solo request (útil para Make con arrays).
    """
    resultados = []
    errores = []

    for tablet in tablets:
        try:
            resultado = calcular_costos_tablet(tablet.dict())
            resultados.append(resultado)
        except Exception as e:
            errores.append({"serial_id": tablet.serial_id, "error": str(e)})

    return {
        "procesados": len(resultados),
        "errores": len(errores),
        "resultados": resultados,
        "detalle_errores": errores
    }


@app.get("/tabla-costos")
def obtener_tabla_costos():
    """Retorna la tabla de costos configurada actualmente."""
    from costos import TABLA_COSTOS
    return TABLA_COSTOS

class DatosAutorizacion(BaseModel):
    nombre_completo: str
    cedula: str
    cargo: Optional[str] = ""
    area: Optional[str] = ""
    serial_tablet: str
    concepto: Optional[str] = "Daño de Display y reposición de cargador"
    costo_reparacion: Optional[str] = "548.000"
   # costo_cargador: Optional[str] = "90.000"
    adaptador_carga: Optional[str] = "87.500"
    cable: Optional[str] = "23.000"
    total: str
    numero_cuotas: Optional[str] = "1"
    valor_cuota: Optional[str] = None
    dia: Optional[str] = None
    mes: Optional[str] = None
    anio: Optional[str] = None
    ciudad: Optional[str] = "Bogotá"
    numero_documento: Optional[str] = None

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
