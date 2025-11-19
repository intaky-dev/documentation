# Documentación: intaky-dev/custom_pos_translations

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/custom_pos_translations`
**Nombre del Módulo:** Custom POS Translations
**Tipo:** Módulo Odoo
**Versión:** 18.0.1.0.0
**Categoría:** Point of Sale
**Tecnología:** Python, Odoo, XML (i18n)
**Licencia:** LGPL-3
**URL:** https://github.com/intaky-dev/custom_pos_translations

## 🎯 Descripción

Módulo Odoo 18.0 para personalizar traducciones del módulo Point of Sale (POS). Permite sobrescribir textos predeterminados del POS con traducciones customizadas, especialmente útil para adaptar la terminología a regiones específicas o necesidades del negocio.

**Casos de uso:**
- Adaptar terminología POS a región (ej: español argentino)
- Personalizar mensajes al cliente
- Traducir términos específicos del negocio
- Override de traducciones oficiales

## 📁 Estructura del Repositorio

```
custom_pos_translations/
├── __init__.py                 # Módulo inicializador (vacío)
├── __manifest__.py             # Metadatos del módulo
└── i18n/
    └── es_AR.po               # Traducción español argentino
```

## 📦 Configuración del Módulo

### Manifest (__manifest__.py)

```python
{
    'name': 'Custom POS Translations',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Custom translations for POS module',
    'description': """
        Módulo para personalizar traducciones del POS
        Sobrescribe traducciones predeterminadas
        Adaptado para español argentino
    """,
    'author': 'Tu Empresa',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [],
    'installable': False,  # Template/Example
    'application': False,
    'auto_install': False,
}
```

### Características

- **Dependencias**: Solo `point_of_sale`
- **No instala archivos**: Solo traducciones (i18n)
- **Template**: `installable: False` (debe activarse para uso)
- **Sin modelos**: No agrega funcionalidad, solo traducciones

## 🌍 Traducción Español Argentino (es_AR.po)

### Formato PO File

```po
# Translation of Odoo Server.
# This file contains the translation of the following modules:
#   * point_of_sale
#
msgid ""
msgstr ""
"Project-Id-Version: Odoo Server 18.0\n"
"Report-Msgid-Bugs-To: \n"
"PO-Revision-Date: 2025-08-14 12:00+0000\n"
"Last-Translator: \n"
"Language-Team: \n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: \n"
"Language: es_AR\n"

#. module: point_of_sale
msgid "Price"
msgstr "Precio"

#. module: point_of_sale
msgid "Quantity"
msgstr "Cantidad"

#. module: point_of_sale
msgid "Total"
msgstr "Total"
```

### Términos Comúnmente Traducidos

| Original (EN) | Traducción (es_AR) | Contexto |
|---------------|-------------------|----------|
| Cart | Carrito | Carrito de compras |
| Checkout | Pagar / Finalizar | Proceso de pago |
| Receipt | Recibo / Ticket | Comprobante |
| Cash | Efectivo | Método de pago |
| Credit Card | Tarjeta de Crédito | Método de pago |
| Discount | Descuento | Precio |
| Tax | Impuesto | IVA, otros |
| Subtotal | Subtotal | Precio antes de impuestos |
| Change | Vuelto / Cambio | Dinero devuelto |

## 🚀 Uso

### Instalación

```bash
# 1. Copiar módulo a addons path
cp -r custom_pos_translations /path/to/odoo/addons/

# 2. Activar modo instalable
# Editar __manifest__.py:
'installable': True,

# 3. Actualizar lista de apps
# Odoo → Apps → Update Apps List

# 4. Instalar módulo
# Apps → Search: "Custom POS Translations" → Install
```

### Activar Idioma

```bash
# 1. Habilitar idioma en Odoo
Settings → Translations → Languages → Activate (es_AR)

# 2. Cambiar idioma de usuario
Preferences → Language → Español (AR)

# 3. Recargar POS
Point of Sale → Dashboard → Open POS
```

## ✏️ Personalización

### Agregar Nuevas Traducciones

```bash
# 1. Editar i18n/es_AR.po
vim i18n/es_AR.po

# 2. Agregar entrada
#. module: point_of_sale
msgid "New Term"
msgstr "Nuevo Término"

# 3. Actualizar módulo en Odoo
Apps → Custom POS Translations → Upgrade
```

### Generar Archivo PO

```bash
# Desde Odoo CLI
odoo -d database --i18n-export=i18n/es_AR.po \
  --modules=point_of_sale \
  --language=es_AR

# O desde UI
Settings → Translations → Import/Export → Export
```

### Crear Traducción para Otro Idioma

```bash
# 1. Copiar template
cp i18n/es_AR.po i18n/es_MX.po

# 2. Editar header
# Cambiar Language: es_MX

# 3. Traducir términos

# 4. Actualizar módulo
```

## 🔧 Desarrollo

### Estructura de Entrada PO

```po
#. module: <module_name>
#: <model_name>,<field_name>:<line_number>
#: <view_path>:<line_number>
#, <flags>
msgid "<source text>"
msgstr "<translated text>"
```

**Ejemplo:**
```po
#. module: point_of_sale
#: model:ir.ui.menu,name:point_of_sale.menu_point_root
msgid "Point of Sale"
msgstr "Punto de Venta"
```

### Flags Comunes

- `python-format`: Contiene placeholders Python `%(name)s`
- `fuzzy`: Traducción aproximada, necesita revisión

### Plurales

```po
msgid "Product"
msgid_plural "Products"
msgstr[0] "Producto"
msgstr[1] "Productos"
```

## 🧪 Testing

### Verificar Traducciones

1. **POS Interface**:
   ```
   Point of Sale → Open Session → Verify UI text
   ```

2. **Receipt**:
   ```
   Completar venta → Print Receipt → Verify printed text
   ```

3. **Backend**:
   ```
   Point of Sale → Orders → Verify column names, buttons
   ```

### Debug Traducciones

```bash
# Ver traducciones cargadas
SELECT * FROM ir_translation
WHERE module='point_of_sale'
AND lang='es_AR'
AND src='Price';

# Limpiar cache de traducciones
Settings → Technical → Translations → Clear
```

## 💡 Mejores Prácticas

1. **Consistencia**: Usar mismo término para mismo concepto
2. **Contexto**: Incluir comentarios para contexto
3. **Validación**: Probar todas las traducciones en POS real
4. **Backup**: Mantener copia del archivo .po
5. **Versionado**: Commit cambios de traducción en git

## 🌍 Localización Avanzada

### Números y Moneda

Las traducciones no afectan formato de números/moneda. Configurar en:

```
Settings → General Settings → Companies
→ Edit Company → Localization
→ Language: Español (AR)
→ Currency: ARS
→ Number Format: 1.234.567,89
```

### Formatos de Fecha/Hora

```python
# res.lang configuración
Date Format: %d/%m/%Y
Time Format: %H:%M:%S
```

## 📊 Estado del Módulo

- **Instala**: ❌ No (Template)
- **Funcional**: ✅ Sí (tras activar installable)
- **Completo**: ⚠️ Parcial (ejemplo básico)
- **Producción**: ⚠️ Requiere personalización

## 🔗 Referencias

- [Odoo Translations](https://www.odoo.com/documentation/18.0/developer/reference/backend/translations.html)
- [PO File Format](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html)
- [Babel i18n](http://babel.pocoo.org/en/latest/)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
