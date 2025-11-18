# Documentación: intaky-dev/modulo_rg5329

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/modulo_rg5329`
**Nombre del Módulo:** AFIP RG 5329 - Percepción IVA Simplificado
**Tipo:** Módulo Odoo (Aplicación completa)
**Versión:** 18.0.1.0.0
**Categoría:** Accounting/Localizations/Argentina
**Tecnología:** Python, XML, JavaScript, Odoo Framework
**Autor:** Tu Empresa
**Licencia:** LGPL-3
**Compatibilidad:** Odoo 18.0+
**URL:** https://github.com/intaky-dev/modulo_rg5329

## 🎯 Descripción

Módulo Odoo que implementa el régimen de percepción de IVA establecido por la Resolución General (RG) 5329/2023 de AFIP (Administración Federal de Ingresos Públicos) en Argentina.

**Normativa RG 5329/2023:**
- Percepción del 3% para productos con IVA 21%
- Percepción del 1.5% para productos con IVA 10.5%
- Mínimo no imponible de $100,000 en total de compra
- Solo aplica a clientes IVA Responsables Inscriptos
- Permite exención por cliente individual
- Creación automática de cuenta contable 2.1.3.03.041

## 🏗️ Arquitectura

### Flujo de Percepción Automática

```
Usuario crea/modifica Orden de Venta/Compra
    ↓
Sistema detecta cambios (cantidad, precio, cliente)
    ↓
Verifica elegibilidad del cliente
    ├─ ¿Es Responsable Inscripto? (código AFIP '1')
    ├─ ¿Está exento de RG5329?
    └─ ¿Tiene productos con apply_rg5329=True?
    ↓
Calcula base imponible total
    ↓
¿Total >= $100,000?
    ├─ SÍ → Aplica impuestos RG5329 según alícuota IVA
    │         - IVA 21% → Percepción 3%
    │         - IVA 10.5% → Percepción 1.5%
    └─ NO → Remueve impuestos RG5329
    ↓
Factura incluye percepción automáticamente
```

### Modelos Extendidos

#### 1. ProductTemplate & ProductProduct
**Archivo:** `models/product_template.py`

**Campo:**
- `apply_rg5329` (Boolean, Default: False)
  - Marca si el producto está sujeto a percepción RG 5329
  - Heredado en ProductProduct como campo relacionado

#### 2. ResPartner (Clientes/Proveedores)
**Archivo:** `models/res_partner.py`

**Campo:**
- `rg5329_exempt` (Boolean, Default: False)
  - Marca cliente/proveedor exento del régimen
  - Permite exclusiones específicas

#### 3. AccountTax (Impuestos)
**Archivo:** `models/account_tax.py`

**Campo:**
- `is_rg5329_perception` (Boolean, Default: False)
  - Identifica impuestos de percepción RG 5329

**Método:**
- `compute_all()`: Filtra impuestos RG5329 en contexto de aplicación automática

#### 4. AccountMove (Facturas - 220 líneas)
**Archivo:** `models/account_move.py`

**Campos Computados:**
- `rg5329_perception_amount` (Monetary, Stored)
  - Monto total de percepción RG 5329
- `rg5329_base_amount` (Monetary, Stored)
  - Base imponible para cálculo de percepción

**Métodos Clave:**
- `_compute_rg5329_perception()`: **Lógica central de cálculo**
  - Valida tipo de factura (out_invoice, out_refund)
  - Verifica exención de cliente
  - Valida categoría fiscal AFIP (solo Responsables Inscriptos)
  - Calcula base imponible por alícuota de IVA
  - Aplica automáticamente impuestos RG 5329
  - Respeta mínimo de $100,000

- `_is_customer_eligible_for_rg5329()`: Verifica elegibilidad
  - Busca `l10n_ar_afip_responsibility_type_id`
  - Solo aplica si código es '1' (Responsable Inscripto)
  - Manejo robusto de errores

- `_get_line_iva_rate()`: Extrae alícuota de IVA de línea
- `_auto_apply_rg5329_taxes()`: Aplica impuestos automáticamente

#### 5. SaleOrder (Órdenes de Venta - 287 líneas)
**Archivo:** `models/sale_order.py`

**Métodos Públicos:**
- `apply_rg5329_logic_manual()`: Dispara lógica manualmente
- `apply_rg5329_via_js()`: Interfaz para JavaScript
- `apply_rg5329_manual_button()`: Botón en UI

**Lógica Central:**
- `_apply_rg5329_logic()`: **Método unificado**
  - Procesa todas las líneas de venta
  - Verifica elegibilidad del cliente
  - Valida categoría fiscal AFIP
  - Aplica/remueve impuestos según montos
  - Fuerza actualización de UI

**Triggers:**
- `_onchange_partner_rg5329_unified()`: Al cambiar cliente
- `_compute_amounts()`: Al recalcular montos
- JavaScript auto-trigger en cambios de líneas

#### 6. PurchaseOrder (Órdenes de Compra - 433 líneas)
**Archivo:** `models/purchase_order.py`

**Características Especiales:**
- Cálculo cuidadoso de totales (excluye RG5329 para evitar recursión)
- Validación de proveedores como Responsables Inscriptos
- `button_confirm()`: Override para preservar impuestos
- `_store_rg5329_taxes_before_confirm()`: Guarda impuestos antes de confirmación
- `_restore_rg5329_taxes_after_confirm()`: Restaura si se pierden
- `_get_stock_move_price_unit()`: Incluye impuestos en movimientos de stock

#### 7. AccountSetup (Modelo Transitorio - 85 líneas)
**Archivo:** `models/account_setup.py`

**Propósito:** Configuración automática de cuentas contables

**Método:**
- `setup_rg5329_accounts()`: Crea cuenta 2.1.3.03.041 y asigna a impuestos

## 📁 Estructura del Repositorio

```
modulo_rg5329/
├── __init__.py
├── __manifest__.py
├── README.md                          # Documentación completa
├── LICENSE
├── .gitignore
├── .github/
├── Dockerfile                          # Containerización
├── docker-compose.yml                  # Stack Docker completo
├── install.sh                          # Script de instalación (366 líneas)
├── git.sh                              # Utilidad git
├── models/
│   ├── __init__.py
│   ├── product_template.py            # Marcado de productos (2 clases)
│   ├── res_partner.py                 # Exenciones de clientes
│   ├── account_tax.py                 # Identificación de impuestos
│   ├── account_move.py                # Lógica en facturas (220 líneas)
│   ├── account_setup.py               # Setup automático (85 líneas)
│   ├── sale_order.py                  # Lógica en ventas (287 líneas)
│   └── purchase_order.py              # Lógica en compras (433 líneas)
├── security/
│   └── ir.model.access.csv            # 3 reglas de acceso
├── views/
│   ├── product_template_views.xml     # Campo en productos
│   ├── res_partner_views.xml          # Campo en clientes
│   ├── account_tax_views.xml          # Vistas de impuestos
│   └── sale_order_rg5329_button.xml   # Botón manual en SO
├── data/
│   └── tax_data.xml                   # Impuestos y cuentas
└── static/
    └── src/js/
        └── rg5329_auto_trigger.js     # Triggers automáticos JS
```

## 📦 Datos Pre-configurados

### Cuenta Contable (tax_data.xml)
```xml
<record id="account_rg5329" model="account.account">
    <field name="code">2.1.3.03.041</field>
    <field name="name">Percepciones de IVA RG 5329</field>
    <field name="account_type">liability_current</field>
    <field name="reconcile">True</field>
</record>
```

### Impuestos de Venta
1. **tax_perception_rg5329_3**
   - Nombre: Percepción IVA RG 5329 - 3%
   - Alícuota: 3.0% (para IVA 21%)
   - Tipo: Venta
   - Cuenta: 2.1.3.03.041
   - Marcado: `is_rg5329_perception = True`

2. **tax_perception_rg5329_1_5**
   - Nombre: Percepción IVA RG 5329 - 1,5%
   - Alícuota: 1.5% (para IVA 10.5%)
   - Tipo: Venta
   - Cuenta: 2.1.3.03.041
   - Marcado: `is_rg5329_perception = True`

### Impuestos de Compra
3. **tax_perception_rg5329_3_purchase** (3% - Compras)
4. **tax_perception_rg5329_1_5_purchase** (1.5% - Compras)

## 🚀 Instalación

### Requisitos
- Odoo 18.0+
- Python >= 3.8
- Módulo `l10n_ar` (localización argentina) instalado
- Categorías fiscales AFIP configuradas en clientes

### Método 1: Manual

```bash
# 1. Clonar en addons path
cd /path/to/odoo/addons/
git clone https://github.com/intaky-dev/modulo_rg5329.git

# 2. Actualizar lista de aplicaciones
# Odoo → Apps → Update Apps List

# 3. Buscar e instalar
# Apps → Search: "RG 5329"
# Click "Install"
```

### Método 2: Script de Instalación

```bash
# Clonar repositorio
git clone https://github.com/intaky-dev/modulo_rg5329.git
cd modulo_rg5329

# Ejecutar script de instalación
./install.sh
```

El script:
- Copia el módulo al contenedor Odoo
- Instala vía API
- Crea datos de demostración
- Configura cuentas contables

### Método 3: Docker Compose

```bash
# Levantar stack completo
docker-compose up -d

# Ver logs
docker-compose logs -f
```

## ⚙️ Configuración

### 1. Configurar Productos

```
Ventas → Productos → Productos
→ Abrir producto
→ Pestaña "Compra" o "Ventas"
→ Marcar ☑ "Aplicar Percepción RG 5329"
```

### 2. Marcar Clientes Exentos (opcional)

```
Contactos → Clientes
→ Abrir cliente
→ Pestaña "Ventas y Compras"
→ Marcar ☑ "Exento RG 5329"
```

### 3. Verificar Categoría Fiscal AFIP

```
Contactos → Clientes
→ Abrir cliente
→ Pestaña "Ventas y Compras"
→ Verificar "Tipo de Responsabilidad AFIP" = "IVA Responsable Inscripto"
```

### 4. Configurar Cuentas (Automático)

Las cuentas se crean automáticamente al instalar, pero puedes ejecutar manualmente:

```python
# En consola Odoo
env['rg5329.account.setup'].create({}).setup_rg5329_accounts()
```

## 🎯 Uso

### Escenario 1: Orden de Venta con Percepción

```
1. Crear Orden de Venta
   Cliente: "Empresa SA" (Responsable Inscripto)
   Producto: "Laptop Dell" (apply_rg5329=True, IVA 21%)
   Cantidad: 5
   Precio unitario: $25,000
   Subtotal: $125,000

2. Sistema Automáticamente:
   ✓ Detecta que total >= $100,000
   ✓ Cliente es Responsable Inscripto
   ✓ Producto tiene apply_rg5329=True
   ✓ Alícuota IVA 21% → Percepción 3%

3. Resultado:
   Subtotal: $125,000
   IVA 21%: $26,250
   Percepción RG5329 (3%): $3,750
   Total: $155,000
```

### Escenario 2: Total Menor al Mínimo

```
1. Crear Orden de Venta
   Producto: "Mouse" (apply_rg5329=True)
   Subtotal: $50,000

2. Sistema Automáticamente:
   ✗ Total < $100,000
   → NO aplica percepción RG 5329
```

### Escenario 3: Cliente Exento

```
1. Crear Orden de Venta
   Cliente: "Gobierno XYZ" (rg5329_exempt=True)
   Subtotal: $200,000

2. Sistema Automáticamente:
   ✗ Cliente exento
   → NO aplica percepción RG 5329
```

### Escenario 4: Aplicación Manual

```
1. Crear Orden de Venta
2. Click botón "Apply RG5329 Tax" en header
3. Sistema recalcula y aplica impuestos
```

## 🔧 Funcionalidades Avanzadas

### Triggers Automáticos

El módulo recalcula percepción automáticamente cuando:
- Cambia el cliente/proveedor
- Se agrega/modifica/elimina una línea
- Cambia cantidad o precio unitario
- Se modifican impuestos en líneas

### Logging

El módulo genera logs detallados:
```python
_logger.info("RG5329: Cliente %s es Responsable Inscripto", partner.name)
_logger.info("RG5329: Total = $%.2f, Mínimo = $100,000", total)
_logger.info("RG5329: Aplicando percepción 3%% en línea %s", line.product_id.name)
```

### Preservación en Confirmación

En compras, el módulo:
1. Guarda impuestos RG5329 antes de confirmar
2. Confirma la orden
3. Verifica si impuestos se perdieron
4. Restaura impuestos si es necesario

### Manejo de Recursión

En cálculo de totales de compras:
```python
# Excluye impuestos RG5329 para evitar recursión infinita
taxes = line.taxes_id.filtered(lambda t: not t.is_rg5329_perception)
```

## 🐛 Troubleshooting

### Percepción no se aplica automáticamente

**Verificar:**
1. ¿Cliente es Responsable Inscripto?
   ```
   Contactos → Cliente → Tipo Responsabilidad AFIP = "IVA Responsable Inscripto"
   ```

2. ¿Producto tiene marca RG5329?
   ```
   Productos → Producto → ☑ Aplicar Percepción RG 5329
   ```

3. ¿Total >= $100,000?
   ```
   Ver subtotal de orden
   ```

4. ¿Cliente NO está exento?
   ```
   Contactos → Cliente → ☐ Exento RG 5329 (debe estar desmarcado)
   ```

### Impuestos se pierden al confirmar

El módulo ya maneja esto automáticamente. Si persiste:
```python
# Forzar restauración manual
order._restore_rg5329_taxes_after_confirm()
```

### Percepción incorrecta

**Verificar alícuotas:**
- IVA 21% → Percepción 3%
- IVA 10.5% → Percepción 1.5%

```
Contabilidad → Configuración → Impuestos
→ Buscar "RG 5329"
→ Verificar alícuotas
```

## 📊 Reportes y Análisis

### Ver Percepciones en Facturas

```
Contabilidad → Clientes → Facturas
→ Abrir factura
→ Ver campos:
   - "RG5329 Base Amount"
   - "RG5329 Perception Amount"
```

### Reporte de Percepciones Aplicadas

```sql
-- Query SQL para analizar percepciones
SELECT
    am.name AS factura,
    rp.name AS cliente,
    am.rg5329_base_amount AS base,
    am.rg5329_perception_amount AS percepcion,
    am.amount_total AS total
FROM account_move am
JOIN res_partner rp ON am.partner_id = rp.id
WHERE am.rg5329_perception_amount > 0
ORDER BY am.date DESC;
```

## 🔒 Seguridad

### Permisos (ir.model.access.csv)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_account_setup,rg5329.account.setup,model_rg5329_account_setup,base.group_user,1,1,1,0
access_sale_order,sale.order,sale.model_sale_order,base.group_user,1,1,1,0
access_sale_order_line,sale.order.line,sale.model_sale_order_line,base.group_user,1,1,1,0
```

- Usuarios base pueden leer/escribir/crear
- No pueden eliminar (unlink=0)

## 💰 Impacto Contable

### Asiento Contable Generado

```
Debe:
  [Cliente] (1.1.x.xx)                     $155,000

Haber:
  [Ventas] (4.1.x.xx)                      $125,000
  [IVA Débito Fiscal] (2.1.x.xx)            $26,250
  [Percepciones IVA RG5329] (2.1.3.03.041)   $3,750
```

## 🌟 Características Destacadas

1. **100% Automático**: Sin intervención manual
2. **Robusto**: Manejo de errores y casos edge
3. **Completo**: Ventas + Compras + Facturas
4. **Auditable**: Logging detallado
5. **Flexible**: Exenciones por cliente
6. **Normativo**: Cumple RG 5329/2023
7. **Docker-ready**: Incluye Dockerfile y compose
8. **Documentado**: README + código comentado

## 📚 Referencias Legales

- [RG 5329/2023 AFIP](https://www.afip.gob.ar/)
- Implementa percepción de IVA según normativa argentina
- Válido para operaciones desde 2023

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
