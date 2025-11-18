# Documentación: intaky-dev/modulo_nakel

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/modulo_nakel`
**Nombre del Módulo:** Precio Anterior
**Tipo:** Módulo Odoo
**Versión:** 1.0
**Categoría:** Sales (Ventas)
**Tecnología:** Python, XML, Odoo Framework
**Autor:** Nakel
**Licencia:** LGPL-3
**URL:** https://github.com/intaky-dev/modulo_nakel

## 🎯 Descripción

Módulo Odoo que agrega funcionalidad para rastrear y mostrar los precios anteriores de proveedores en productos. Cuando el precio de un proveedor se actualiza, el sistema automáticamente guarda el precio anterior para referencia y análisis comparativo.

**Casos de uso:**
- Análisis de variación de precios de proveedores
- Negociación con proveedores (mostrar histórico)
- Auditoría de cambios de precios
- Comparación de precios actuales vs anteriores

## 🏗️ Arquitectura

### Modelos Extendidos

#### 1. ProductTemplate (product.template)
**Archivo:** `models/product_template.py`

**Campo agregado:**
- `previous_price` (Float, Computed)
  - No almacenado (calculado dinámicamente)
  - Busca el precio anterior del proveedor asociado
  - Retorna 0.0 si no encuentra precio anterior

**Método:**
- `_compute_previous_price()`: Busca en `product.supplierinfo` el precio anterior del primer proveedor con precio anterior > 0

#### 2. SupplierInfo (product.supplierinfo)
**Archivo:** `models/product_supplierinfo.py`

**Campo agregado:**
- `previous_price` (Float, Readonly)
  - Almacenado en base de datos
  - Solo lectura en interfaz
  - Guarda el precio anterior cada vez que cambia

**Métodos sobreescritos:**
- `create()`: Al crear nuevo registro, copia precio inicial al campo previous_price
- `write()`: Al actualizar, guarda precio actual como previous_price antes de aplicar nuevo precio

## 📁 Estructura del Repositorio

```
modulo_nakel/
├── __init__.py                 # Inicializador del módulo
├── __manifest__.py             # Metadatos del módulo Odoo
├── README.md                   # Documentación básica
├── models/
│   ├── __init__.py            # Importa modelos
│   ├── product_template.py    # Extensión de product.template
│   └── product_supplierinfo.py # Extensión de product.supplierinfo
├── security/
│   └── ir.model.access.csv    # Permisos de acceso (vacío)
└── views/
    └── product_views.xml      # Vistas heredadas
```

## 🔧 Funcionalidad Detallada

### Flujo de Trabajo

1. **Creación de Proveedor-Producto**:
   ```python
   # Usuario crea supplierinfo con precio inicial de $100
   supplierinfo.create({
       'partner_id': proveedor_id,
       'price': 100.0
   })
   # Sistema automáticamente: previous_price = 100.0
   ```

2. **Actualización de Precio**:
   ```python
   # Usuario cambia precio a $120
   supplierinfo.write({'price': 120.0})
   # Sistema ANTES de actualizar: previous_price = 100.0
   # Sistema DESPUÉS: price = 120.0, previous_price = 100.0
   ```

3. **Visualización**:
   - En formulario de producto: Muestra "Precio Anterior" (readonly)
   - En formulario de proveedor: Muestra precio anterior del proveedor (readonly)
   - Campo calculado dinámicamente en ProductTemplate

### Lógica de Cálculo

```python
def _compute_previous_price(self):
    for record in self:
        # Buscar primer supplierinfo con precio anterior > 0
        supplier_info = self.env['product.supplierinfo'].search([
            ('product_tmpl_id', '=', record.id),
            ('previous_price', '>', 0)
        ], limit=1)

        # Asignar precio anterior o 0.0
        record.previous_price = supplier_info.previous_price if supplier_info else 0.0
```

### Captura de Cambios

```python
def write(self, vals):
    # Si se está actualizando el precio
    if 'price' in vals:
        for record in self:
            # Guardar precio actual como previous_price
            vals['previous_price'] = record.price
    return super().write(vals)
```

## 🖼️ Vistas

### Vista de Producto (product_template_view_form_inherit_nakel)

```xml
<field name="list_price"/>
<field name="previous_price" readonly="1"/>
```

Agrega el campo "Precio Anterior" debajo del precio de lista en el formulario de producto.

### Vista de Proveedor (product_supplierinfo_form_view_inherit_nakel)

```xml
<field name="price"/>
<field name="previous_price" readonly="1"/>
```

Agrega el campo "Precio Anterior" debajo del precio en el formulario de información de proveedor.

## 📦 Instalación

### Requisitos
- Odoo 14.0+ (compatible con versiones superiores)
- Módulo `product` (viene en Odoo base)

### Pasos de Instalación

```bash
# 1. Clonar repositorio en addons path
cd /path/to/odoo/addons/
git clone https://github.com/intaky-dev/modulo_nakel.git

# 2. Actualizar lista de aplicaciones en Odoo
# Apps → Update Apps List

# 3. Buscar "Precio Anterior"
# Apps → Search: "Precio Anterior"

# 4. Instalar módulo
# Click en "Install"
```

### Configuración
No requiere configuración adicional. Funciona automáticamente después de la instalación.

## 🎯 Uso

### Ver Precio Anterior de Producto

1. Ir a **Ventas → Productos → Productos**
2. Abrir un producto
3. En la pestaña "Compra" ver el campo "Precio Anterior"

### Ver Precio Anterior de Proveedor

1. Ir a **Ventas → Productos → Productos**
2. Abrir un producto
3. Tab "Compra" → Proveedores
4. Abrir un registro de proveedor
5. Ver campo "Precio Anterior" debajo del precio

### Ejemplo Práctico

```
Escenario:
1. Crear producto "Laptop Dell"
2. Agregar proveedor "TechCorp" con precio $1000
   → previous_price = $1000

3. Semana después, actualizar precio a $1100
   → previous_price = $1000 (guardado)
   → price = $1100 (nuevo)

4. Ver en formulario:
   Precio: $1100
   Precio Anterior: $1000

5. Análisis: Aumento del 10%
```

## 🔒 Seguridad

- Archivo `security/ir.model.access.csv` está vacío
- Usa permisos heredados de módulo `product`
- Campo `previous_price` es readonly, no modificable por usuarios
- Solo se actualiza automáticamente por el sistema

## 💡 Ventajas

1. **Automático**: Sin intervención del usuario
2. **Simple**: Solo 2 campos agregados
3. **Eficiente**: Campo computado no consume espacio extra en ProductTemplate
4. **Auditable**: Histórico básico de cambios de precio
5. **Visual**: Comparación directa en misma pantalla

## ⚠️ Limitaciones

1. **Solo último precio**: No mantiene histórico completo, solo el precio inmediatamente anterior
2. **Primer proveedor**: En ProductTemplate muestra solo el precio del primer proveedor con previous_price
3. **Sin fecha**: No registra cuándo ocurrió el cambio de precio
4. **Sin usuario**: No registra quién hizo el cambio

## 🚀 Posibles Mejoras

- Mantener histórico completo de precios (tabla dedicada)
- Agregar fecha y usuario del cambio
- Graficar evolución de precios en el tiempo
- Alertas de cambios significativos de precio
- Comparación entre múltiples proveedores

## 🔧 Desarrollo

### Estructura de Código

**Modelo ProductTemplate:**
```python
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    previous_price = fields.Float(
        string="Precio Anterior",
        compute='_compute_previous_price',
        store=False,
        digits='Product Price'
    )
```

**Modelo SupplierInfo:**
```python
class SupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    previous_price = fields.Float(
        string="Precio Anterior",
        readonly=True,
        digits='Product Price'
    )
```

## 📊 Dependencias

```python
'depends': ['product']
```

Solo depende del módulo core de productos de Odoo.

## 🧪 Testing

**Caso de prueba manual:**

1. Crear producto nuevo
2. Agregar proveedor con precio $500
3. Verificar: previous_price = $500
4. Cambiar precio a $600
5. Verificar: price = $600, previous_price = $500
6. Verificar visualización en vistas

## 🌟 Características Técnicas

- **ORM Odoo**: Uso correcto de `_inherit`
- **Computed Fields**: Campo calculado eficientemente
- **View Inheritance**: Herencia de vistas existentes
- **CRUD Hooks**: Override de create() y write()
- **Search Domain**: Búsqueda eficiente con limit=1

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
