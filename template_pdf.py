# template_pdf.py
# Genera el HTML del formato de Autorización de Descuento Würth
# Los parámetros vienen del body del request de Make.com

from datetime import datetime

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
}

def generar_html_autorizacion(datos: dict) -> str:
    hoy = datetime.now()

    nombre_completo   = datos.get("nombre_completo", "")
    cedula            = datos.get("cedula", "")
    cargo             = datos.get("cargo", "")
    area              = datos.get("area", "")
    serial_tablet     = datos.get("serial_tablet", "")
    concepto          = datos.get("concepto", "Daño de Display y reposición de cargador")
    costo_reparacion  = datos.get("costo_reparacion", "548.000")
    costo_cargador    = datos.get("costo_cargador", "90.000")
    total             = datos.get("total", "638.000")
    numero_cuotas     = datos.get("numero_cuotas", "1")
    valor_cuota       = datos.get("valor_cuota", total)
    dia               = datos.get("dia", str(hoy.day))
    mes               = datos.get("mes", MESES[hoy.month])
    anio              = datos.get("anio", str(hoy.year))
    ciudad            = datos.get("ciudad", "Bogotá")
    numero_documento  = datos.get("numero_documento", str(hoy.strftime("%y%m%d%H%M")))

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  :root {{
    --red: #CC0000; --dark: #1A1A1A; --mid: #3D3D3D;
    --gray: #6B6B6B; --light: #F5F3F0; --border: #D4CFC8; --cream: #FDFBF8;
  }}
  body {{ background: white; font-family: Georgia, serif; color: var(--dark); margin: 0; padding: 0; }}
  .page {{
    background: var(--cream); width: 794px; min-height: 1123px;
    position: relative; display: flex; flex-direction: column;
    border-left: 6px solid var(--red);
  }}
  .header {{ padding: 36px 52px 0 52px; display: flex; align-items: flex-start; justify-content: space-between; }}
  .logo-area {{ display: flex; flex-direction: column; gap: 6px; }}
  .company-sub {{ font-size: 9px; letter-spacing: 2px; text-transform: uppercase; color: var(--gray); }}
  .doc-meta {{ text-align: right; }}
  .doc-meta-label {{ font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gray); display: block; }}
  .doc-meta-value {{ font-size: 11px; color: var(--mid); display: block; margin-bottom: 6px; }}
  .doc-meta-number {{ font-size: 13px; color: var(--red); font-weight: bold; display: block; margin-bottom: 6px; }}
  .rule {{ margin: 24px 52px 0; border: none; border-top: 1px solid var(--border); }}
  .title-section {{ padding: 28px 52px 16px; text-align: center; }}
  .title-eyebrow {{ font-size: 9px; letter-spacing: 4px; text-transform: uppercase; color: var(--red); margin-bottom: 8px; }}
  h1 {{ font-family: Georgia, serif; font-size: 24px; font-weight: bold; color: var(--dark); }}
  .title-rule {{ width: 60px; height: 2px; background: var(--red); margin: 12px auto 0; }}
  .body {{ padding: 20px 52px; flex: 1; display: flex; flex-direction: column; }}
  .section-label {{
    font-size: 9px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gray);
    margin-bottom: 10px; border-bottom: 1px solid var(--border); padding-bottom: 4px;
  }}
  .employee-card {{
    background: var(--light); border: 1px solid var(--border); border-left: 3px solid var(--red);
    padding: 16px 20px; margin-bottom: 22px;
  }}
  .field-row {{ display: flex; gap: 24px; margin-bottom: 10px; }}
  .field-group {{ flex: 1; }}
  .field-label {{ font-size: 8px; letter-spacing: 2px; text-transform: uppercase; color: var(--gray); display: block; }}
  .field-value {{
    font-size: 13px; font-weight: bold; color: var(--dark);
    border-bottom: 1px solid var(--border); padding-bottom: 3px; display: block; min-height: 20px;
  }}
  .legal-text {{ font-size: 13px; line-height: 1.85; color: var(--mid); text-align: justify; margin-bottom: 22px; }}
  .legal-text strong {{ color: var(--dark); }}
  .legal-text .hl {{ color: var(--red); font-weight: bold; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 12px; margin-bottom: 0; }}
  thead tr {{ background: var(--dark); color: white; }}
  thead th {{ padding: 9px 12px; text-align: left; font-size: 9px; letter-spacing: 1px; text-transform: uppercase; font-weight: normal; }}
  thead th:last-child {{ text-align: right; }}
  tbody tr {{ border-bottom: 1px solid var(--border); }}
  tbody tr:nth-child(even) {{ background: var(--light); }}
  tbody td {{ padding: 10px 12px; color: var(--mid); }}
  tbody td:last-child {{ text-align: right; font-weight: bold; color: var(--dark); }}
  tfoot tr {{ background: var(--red); color: white; }}
  tfoot td {{ padding: 11px 12px; font-weight: bold; font-size: 13px; }}
  tfoot td:last-child {{ text-align: right; font-size: 14px; }}
  .cuotas {{
    margin: 10px 0 22px; background: #FFF8F8; border: 1px solid #F5CCCC;
    border-left: 3px solid var(--red); padding: 11px 14px; font-size: 12px; color: var(--mid);
  }}
  .cuotas strong {{ color: var(--red); }}
  .date-text {{ font-size: 13px; color: var(--mid); margin-bottom: 32px; line-height: 1.85; }}
  .date-text strong {{ color: var(--dark); }}
  .sig-section {{
    margin-top: auto; padding-top: 18px; border-top: 1px solid var(--border);
    display: flex; gap: 40px; margin-bottom: 8px;
  }}
  .sig-block {{ flex: 1; }}
  .sig-line {{ width: 100%; height: 1px; background: var(--dark); margin-bottom: 5px; }}
  .sig-label {{ font-size: 8.5px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--gray); display: block; }}
  .sig-value {{ font-size: 12px; font-weight: bold; color: var(--dark); display: block; }}
  .sig-sub {{ font-size: 11px; color: var(--gray); display: block; }}
  .footer {{
    padding: 14px 52px 18px; border-top: 1px solid var(--border);
    display: flex; align-items: center; justify-content: space-between;
  }}
  .footer-text {{ font-size: 8.5px; color: var(--gray); line-height: 1.6; }}
  .footer-badge {{ font-size: 8px; letter-spacing: 1.5px; text-transform: uppercase; color: var(--red); }}
</style>
</head>
<body>
<div class="page">

  <header class="header">
    <div class="logo-area">
      <svg height="50" viewBox="0 0 320 80" xmlns="http://www.w3.org/2000/svg">
        <path d="M8 4 L8 52 Q8 68 24 72 Q40 76 40 76 Q56 72 56 56 L56 4 Z" fill="#CC0000"/>
        <rect x="8" y="26" width="48" height="16" fill="white"/>
        <rect x="8" y="4" width="12" height="10" fill="white"/>
        <rect x="44" y="4" width="12" height="10" fill="white"/>
        <rect x="8" y="56" width="10" height="10" fill="white"/>
        <rect x="46" y="56" width="10" height="10" fill="white"/>
        <text x="76" y="58" font-family="Arial Black, Arial" font-weight="900" font-size="46" fill="#1A1A1A">WÜRTH</text>
      </svg>
      <span class="company-sub">Colombia SAS · Documento Interno</span>
    </div>
    <div class="doc-meta">
      <span class="doc-meta-label">Tipo de documento</span>
      <span class="doc-meta-value">Autorización de Descuento</span>
      <span class="doc-meta-label">Referencia</span>
      <span class="doc-meta-number">AD-{numero_documento}</span>
      <span class="doc-meta-label">Fecha de emisión</span>
      <span class="doc-meta-value">{dia} de {mes} de {anio}</span>
    </div>
  </header>

  <hr class="rule">

  <div class="title-section">
    <div class="title-eyebrow">Documento de Autorización</div>
    <h1>Autorización de Descuento</h1>
    <div class="title-rule"></div>
  </div>

  <div class="body">

    <div class="section-label">Datos del colaborador</div>
    <div class="employee-card">
      <div class="field-row">
        <div class="field-group" style="flex:2">
          <span class="field-label">Nombre completo</span>
          <span class="field-value">{nombre_completo}</span>
        </div>
      </div>
      <div class="field-row">
        <div class="field-group">
          <span class="field-label">Cédula de ciudadanía</span>
          <span class="field-value">{cedula}</span>
        </div>
        <div class="field-group">
          <span class="field-label">Cargo</span>
          <span class="field-value">{cargo}</span>
        </div>
        <div class="field-group">
          <span class="field-label">Área / Departamento</span>
          <span class="field-value">{area}</span>
        </div>
      </div>
    </div>

    <div class="section-label">Texto de autorización</div>
    <p class="legal-text">
      Por la suscripción del presente documento autorizo expresamente a la sociedad
      <strong>WÜRTH COLOMBIA SAS</strong> para que compense, deduzca, descuente y retenga de los
      salarios ordinarios, extraordinarios, prestaciones sociales, vacaciones y demás derechos que me
      correspondan, los valores descritos a continuación correspondientes al dispositivo
      <strong>Tablet Marca LENOVO</strong> — Serial <strong>{serial_tablet}</strong>,
      por concepto de <span class="hl">{concepto}</span>.
    </p>

    <div class="section-label">Detalle de valores a descontar</div>
    <table>
      <thead>
        <tr>
          <th>Concepto</th>
          <th>Descripción</th>
          <th>Valor</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>Daño de Display</td>
          <td>Reparación pantalla Tablet Lenovo — Serial {serial_tablet}</td>
          <td>$ {costo_reparacion}</td>
        </tr>
        <tr>
          <td>Reposición de Cargador</td>
          <td>Cargador original Lenovo</td>
          <td>$ {costo_cargador}</td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="2"><strong>Total a descontar</strong></td>
          <td><strong>$ {total}</strong></td>
        </tr>
      </tfoot>
    </table>

    <div class="cuotas">
      El descuento se realizará en <strong>{numero_cuotas} cuota(s)</strong> de
      <strong>$ {valor_cuota}</strong> cada una, aplicadas sobre la nómina mensual del colaborador.
    </div>

    <p class="date-text">
      Para constancia, el presente documento se suscribe a los <strong>{dia} días</strong>
      del mes de <strong>{mes}</strong> del año <strong>{anio}</strong>,
      en la ciudad de <strong>{ciudad}</strong>.
    </p>

    <div class="sig-section">
      <div class="sig-block">
        <div class="sig-line"></div>
        <span class="sig-label">Firma del colaborador</span>
        <span class="sig-value">{nombre_completo}</span>
        <span class="sig-sub">C.C. No. {cedula}</span>
      </div>
      <div class="sig-block">
        <div class="sig-line"></div>
        <span class="sig-label">Representante Würth Colombia SAS</span>
        <span class="sig-value">Recursos Humanos</span>
        <span class="sig-sub">Würth Colombia SAS</span>
      </div>
    </div>

  </div>

  <footer class="footer">
    <div class="footer-text">
      Würth Colombia SAS · NIT: 800.182.281-3<br>
      Documento generado automáticamente — uso interno
    </div>
    <div class="footer-badge">&#9679; Documento oficial</div>
  </footer>

</div>
</body>
</html>"""