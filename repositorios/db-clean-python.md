# Documentación: intaky-dev/db-clean-python

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/db-clean-python`
**Nombre del Módulo:** Limpieza de Datos
**Tipo:** Módulo Odoo (Wizard/Tool)
**Versión:** 1.0
**Categoría:** Tools
**Tecnología:** Python, Odoo, SQL
**Licencia:** LGPL-3
**URL:** https://github.com/intaky-dev/db-clean-python

## 🎯 Descripción

Módulo Odoo para limpiar datos de prueba de la base de datos de manera segura y eficiente. Proporciona un wizard con interfaz gráfica que permite eliminar registros de desarrollo/testing en producción sin afectar configuraciones ni datos maestros.

**Casos de uso:**
- Limpiar base de datos antes de pasar a producción
- Eliminar datos de testing/desarrollo
- Reset de datos transaccionales
- Mantenimiento de base de datos
- Preparación de demos/training

## ⚠️ ADVERTENCIA

**IMPORTANTE:** Este módulo ejecuta operaciones de borrado masivo.
- ✅ Usar solo en ambientes de desarrollo/staging
- ✅ Hacer backup completo antes de ejecutar
- ✅ Verificar qué se eliminará antes de confirmar
- ❌ NO usar en producción sin backup
- ❌ NO ejecutar sin entender las consecuencias

## 📁 Estructura del Repositorio

```
db-clean-python/
├── __init__.py                    # Importa modelos
├── __manifest__.py                # Metadatos del módulo
├── README.md                      # Solo contiene "tuki"
├── models/
│   ├── __init__.py               # Importa db_clean.py
│   └── db_clean.py               # Wizard de limpieza
├── views/
│   └── limpiar_base_wizard.xml   # Vista del wizard
└── security/
    └── ir.model.access.csv       # Permisos de acceso
```

## 📦 Configuración del Módulo

### Manifest (__manifest__.py)

```python
{
    'name': 'Limpieza de Datos',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Eliminar datos de prueba de la base de datos',
    'description': """
        Módulo para limpiar datos de desarrollo y pruebas.

        Elimina:
        - Órdenes de venta y líneas
        - Órdenes de compra y líneas
        - Movimientos de stock
        - Datos de POS

        ADVERTENCIA: Operación irreversible sin backup.
    """,
    'author': 'Tu Empresa',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'sale',
        'purchase',
        'stock',
        'point_of_sale',
        'account'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/limpiar_base_wizard.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
```

## 🔧 Funcionalidad

### Modelo Wizard (models/db_clean.py)

```python
from odoo import models, fields

class LimpiarBaseWizard(models.TransientModel):
    _name = 'limpiar.base.wizard'
    _description = 'Wizard para limpiar base de datos'

    def limpiar_base(self):
        """
        Ejecuta queries SQL para eliminar datos transaccionales
        """
        cr = self.env.cr

        # 1. Eliminar líneas de órdenes de venta
        cr.execute("DELETE FROM sale_order_line")

        # 2. Eliminar órdenes de venta
        cr.execute("DELETE FROM sale_order")

        # 3. Eliminar líneas de órdenes de compra
        cr.execute("DELETE FROM purchase_order_line")

        # 4. Eliminar órdenes de compra
        cr.execute("DELETE FROM purchase_order")

        # 5. Eliminar movimientos de stock
        cr.execute("DELETE FROM stock_move")
        cr.execute("DELETE FROM stock_move_line")

        # 6. Eliminar datos de POS
        cr.execute("DELETE FROM pos_order_line")
        cr.execute("DELETE FROM pos_order")
        cr.execute("DELETE FROM pos_session")

        self.env.cr.commit()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Limpieza Completada',
                'message': 'Los datos han sido eliminados exitosamente.',
                'type': 'success',
            }
        }
```

### Datos Eliminados

| Módulo | Tablas Limpiadas | Descripción |
|--------|------------------|-------------|
| **Ventas** | sale_order, sale_order_line | Órdenes y líneas de venta |
| **Compras** | purchase_order, purchase_order_line | Órdenes y líneas de compra |
| **Inventario** | stock_move, stock_move_line | Movimientos de stock |
| **POS** | pos_order, pos_order_line, pos_session | Órdenes y sesiones POS |

### Datos NO Eliminados (Preservados)

- ✅ Productos y variantes
- ✅ Clientes y proveedores
- ✅ Configuración de empresa
- ✅ Usuarios y permisos
- ✅ Reglas de negocio
- ✅ Tarifas y listas de precios
- ✅ Ubicaciones de almacén
- ✅ Métodos de pago

## 🚀 Uso

### Instalación

```bash
# 1. Copiar módulo
cp -r db-clean-python /path/to/odoo/addons/

# 2. Actualizar lista de apps
# Odoo → Apps → Update Apps List

# 3. Instalar
# Apps → Search: "Limpieza de Datos" → Install
```

### Ejecutar Limpieza

```
1. Ir a: Ajustes → Técnico → Limpieza de Datos

2. O buscar: "Limpiar Base" en barra de búsqueda

3. Click en "Limpiar Base"

4. Confirmar en diálogo

5. Esperar notificación de éxito
```

### Vista del Wizard (limpiar_base_wizard.xml)

```xml
<record id="view_limpiar_base_wizard" model="ir.ui.view">
    <field name="name">limpiar.base.wizard.form</field>
    <field name="model">limpiar.base.wizard</field>
    <field name="arch" type="xml">
        <form string="Limpiar Base de Datos">
            <header>
                <button name="limpiar_base"
                        string="Limpiar Base"
                        type="object"
                        class="btn-primary"
                        confirm="¿Está seguro? Esta operación eliminará todos los datos transaccionales."/>
            </header>
            <sheet>
                <div class="oe_title">
                    <h1>Limpieza de Base de Datos</h1>
                </div>
                <group>
                    <p>
                        Este asistente eliminará:
                        <ul>
                            <li>Todas las órdenes de venta</li>
                            <li>Todas las órdenes de compra</li>
                            <li>Todos los movimientos de stock</li>
                            <li>Todas las órdenes de POS</li>
                        </ul>
                    </p>
                    <p class="text-danger">
                        <strong>ADVERTENCIA:</strong> Esta operación es irreversible.
                        Asegúrese de tener un backup de la base de datos.
                    </p>
                </group>
            </sheet>
        </form>
    </field>
</record>

<record id="action_limpiar_base_wizard" model="ir.actions.act_window">
    <field name="name">Limpiar Base</field>
    <field name="res_model">limpiar.base.wizard</field>
    <field name="view_mode">form</field>
    <field name="target">new</field>
</record>

<menuitem id="menu_limpiar_base"
          name="Limpieza de Datos"
          parent="base.menu_administration"
          action="action_limpiar_base_wizard"
          sequence="100"/>
```

## 🔒 Seguridad

### Permisos (ir.model.access.csv)

```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_limpiar_base_wizard,access_limpiar_base_wizard,model_limpiar_base_wizard,base.group_system,1,1,1,1
```

**Acceso:** Solo usuarios con grupo `Settings` (Administradores)

### Mejores Prácticas de Seguridad

1. **Backup Obligatorio**:
   ```bash
   pg_dump -h localhost -U odoo -d database_name > backup_$(date +%Y%m%d).sql
   ```

2. **Testing en Copia**:
   - Crear copia de BD
   - Probar limpieza en copia
   - Verificar resultados
   - Solo después ejecutar en BD real

3. **Confirmation Dialog**:
   - El wizard ya incluye `confirm` en botón
   - Agregar segundo nivel de confirmación si es crítico

## 🧪 Testing

### Pre-Limpieza

```sql
-- Contar registros antes
SELECT 'sale_order' as tabla, COUNT(*) FROM sale_order
UNION ALL
SELECT 'purchase_order', COUNT(*) FROM purchase_order
UNION ALL
SELECT 'stock_move', COUNT(*) FROM stock_move
UNION ALL
SELECT 'pos_order', COUNT(*) FROM pos_order;
```

### Post-Limpieza

```sql
-- Verificar limpieza (deben ser 0)
SELECT 'sale_order' as tabla, COUNT(*) FROM sale_order
UNION ALL
SELECT 'purchase_order', COUNT(*) FROM purchase_order
UNION ALL
SELECT 'stock_move', COUNT(*) FROM stock_move
UNION ALL
SELECT 'pos_order', COUNT(*) FROM pos_order;
```

### Verificar Integridad

```sql
-- Productos deben seguir existiendo
SELECT COUNT(*) FROM product_template;  -- > 0

-- Clientes deben seguir existiendo
SELECT COUNT(*) FROM res_partner;  -- > 0

-- Usuarios deben seguir existiendo
SELECT COUNT(*) FROM res_users;  -- > 0
```

## 💡 Extensión

### Agregar Más Tablas a Limpiar

```python
def limpiar_base(self):
    cr = self.env.cr

    # Existing cleanups...

    # Agregar: Facturas
    cr.execute("DELETE FROM account_move_line")
    cr.execute("DELETE FROM account_move WHERE move_type IN ('out_invoice', 'in_invoice')")

    # Agregar: Inventarios
    cr.execute("DELETE FROM stock_inventory_line")
    cr.execute("DELETE FROM stock_inventory")

    # Agregar: Pickings
    cr.execute("DELETE FROM stock_picking")

    self.env.cr.commit()
```

### Limpieza Selectiva

```python
# Agregar campo de selección en wizard
clean_sales = fields.Boolean(string='Limpiar Ventas', default=True)
clean_purchases = fields.Boolean(string='Limpiar Compras', default=True)
clean_inventory = fields.Boolean(string='Limpiar Inventario', default=True)
clean_pos = fields.Boolean(string='Limpiar POS', default=True)

def limpiar_base(self):
    cr = self.env.cr

    if self.clean_sales:
        cr.execute("DELETE FROM sale_order_line")
        cr.execute("DELETE FROM sale_order")

    if self.clean_purchases:
        cr.execute("DELETE FROM purchase_order_line")
        cr.execute("DELETE FROM purchase_order")

    # etc...
```

## 🐛 Troubleshooting

### Error: Foreign Key Constraint

Si aparecen errores de foreign keys:

```python
# Deshabilitar constraints temporalmente
cr.execute("SET CONSTRAINTS ALL DEFERRED")

# Ejecutar deletes
# ...

# Re-habilitar
cr.execute("SET CONSTRAINTS ALL IMMEDIATE")
```

### Error: Permission Denied

Verificar que el usuario tenga permisos:
```sql
SELECT * FROM ir_model_access
WHERE model='limpiar.base.wizard';
```

## 📊 Performance

Para bases de datos muy grandes:

```python
# Usar TRUNCATE en lugar de DELETE (más rápido)
cr.execute("TRUNCATE TABLE sale_order_line CASCADE")
cr.execute("TRUNCATE TABLE sale_order CASCADE")

# Pero CUIDADO: TRUNCATE ignora foreign keys y puede dejar BD inconsistente
```

## 🔗 Referencias

- [Odoo TransientModel](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#transient-models)
- [SQL in Odoo](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html#raw-sql)
- [PostgreSQL TRUNCATE](https://www.postgresql.org/docs/current/sql-truncate.html)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
