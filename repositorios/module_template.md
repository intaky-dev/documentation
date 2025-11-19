# Documentación: intaky-dev/module_template

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/module_template`
**Tipo:** Template/Boilerplate
**Tecnología:** Python, Odoo 18, Docker
**Propósito:** Template completo para crear módulos Odoo personalizados
**Licencia:** LGPL-3
**URL:** https://github.com/intaky-dev/module_template

## 🎯 Descripción

Template listo para usar en GitHub que proporciona una estructura completa y mejores prácticas para desarrollar módulos Odoo. Incluye configuración Docker para desarrollo y testing, estructura de carpetas estándar, y ejemplos de código funcionales.

**Ideal para:**
- Iniciar nuevos proyectos de módulos Odoo
- Estandarizar estructura de equipo
- Aprendizaje de desarrollo Odoo
- Prototipos rápidos

## 📁 Estructura Completa

```
module_template/
├── Dockerfile                      # Imagen Docker para Odoo
├── docker-compose.yml              # Stack completo (Odoo + PostgreSQL)
├── README.md                       # Documentación del template
├── LICENSE                         # LGPL-3
└── my_module/                      # Módulo ejemplo
    ├── __init__.py                # Importa modelos
    ├── __manifest__.py            # Metadatos del módulo
    ├── models/                    # Modelos de negocio
    │   ├── __init__.py
    │   └── my_model.py           # Ejemplo de modelo
    ├── views/                     # Vistas XML
    │   └── my_model_views.xml    # Formularios y listas
    ├── security/                  # Permisos y accesos
    │   ├── security.xml          # Grupos de seguridad
    │   └── ir.model.access.csv   # Permisos de modelo
    ├── data/                      # Datos iniciales
    │   └── demo_data.xml         # Datos de demostración
    ├── static/                    # Assets estáticos
    │   └── description/
    │       ├── index.html        # Descripción del módulo
    │       └── icon.png          # Icono del módulo
    └── tests/                     # Tests unitarios
        └── test_my_model.py      # Ejemplo de test
```

## 🚀 Uso Rápido

### Opción 1: Use This Template (GitHub)

1. Click en "Use this template" en GitHub
2. Crear nuevo repositorio
3. Clonar tu nuevo repositorio
4. Renombrar `my_module` a tu nombre de módulo

### Opción 2: Manual

```bash
# 1. Clonar template
git clone https://github.com/intaky-dev/module_template.git mi_nuevo_modulo
cd mi_nuevo_modulo

# 2. Renombrar módulo
mv my_module mi_nuevo_modulo

# 3. Actualizar references
# Editar __manifest__.py, README.md, etc.

# 4. Inicializar git propio
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"
```

## 🐳 Docker Development

### Levantar Stack

```bash
# Iniciar Odoo + PostgreSQL
docker-compose up -d

# Ver logs
docker-compose logs -f

# Acceder a Odoo
http://localhost:8069
```

### Configuración Docker Compose

```yaml
services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: odoo
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

  odoo:
    build: .
    depends_on:
      - db
    ports:
      - "8069:8069"
    volumes:
      - ./my_module:/mnt/extra-addons/my_module
    environment:
      - HOST=db
      - USER=odoo
      - PASSWORD=odoo
```

## 📝 Contenido del Template

### Manifest (__manifest__.py)

```python
{
    'name': 'My Module',
    'version': '1.0.0',
    'category': 'Tools',
    'summary': 'A custom Odoo module',
    'description': """
        Detailed description of my module
    """,
    'author': 'Your Name',
    'website': 'https://yourwebsite.com',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/my_model_views.xml',
        'data/demo_data.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
```

### Modelo Ejemplo (models/my_model.py)

```python
from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model Description'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    date = fields.Date(string='Date')

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if not record.name:
                raise ValidationError("Name is required!")
```

### Vistas Ejemplo (views/my_model_views.xml)

Incluye:
- Tree view (lista)
- Form view (formulario)
- Search view (filtros y búsqueda)
- Action y menu item

### Seguridad (security/)

**security.xml:**
- Grupo de seguridad `group_my_model_user`
- Categoría del módulo

**ir.model.access.csv:**
- Permisos de acceso al modelo
- read, write, create, unlink

### Tests (tests/test_my_model.py)

```python
from odoo.tests.common import TransactionCase

class TestMyModel(TransactionCase):

    def setUp(self):
        super().setUp()
        self.MyModel = self.env['my.model']

    def test_create_record(self):
        record = self.MyModel.create({
            'name': 'Test Record',
            'description': 'Test Description'
        })
        self.assertEqual(record.name, 'Test Record')
        self.assertTrue(record.active)
```

## 🔧 Personalización

### 1. Renombrar Módulo

```bash
# Renombrar carpeta
mv my_module <tu_nombre_modulo>

# Actualizar en archivos:
# - __manifest__.py: 'name'
# - __init__.py: imports
# - models/*.py: _name del modelo
# - views/*.xml: model references
# - security/*.csv: model_id
```

### 2. Actualizar Metadatos

Editar `__manifest__.py`:
```python
{
    'name': 'Tu Nombre de Módulo',
    'author': 'Tu Nombre',
    'website': 'https://tuwebsite.com',
    'category': 'Tu Categoría',  # Sales, Inventory, etc.
    'depends': ['base', 'sale', ...],  # Dependencias
}
```

### 3. Agregar Campos al Modelo

```python
# models/my_model.py
class MyModel(models.Model):
    _name = 'my.model'

    # Nuevos campos
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    partner_id = fields.Many2one('res.partner', string='Partner')
    line_ids = fields.One2many('my.model.line', 'model_id', string='Lines')
```

### 4. Agregar Nuevas Vistas

```xml
<!-- views/my_model_views.xml -->
<record id="view_my_model_kanban" model="ir.ui.view">
    <field name="name">my.model.kanban</field>
    <field name="model">my.model</field>
    <field name="arch" type="xml">
        <kanban>
            <field name="name"/>
            <templates>
                <t t-name="kanban-box">
                    <div class="oe_kanban_global_click">
                        <field name="name"/>
                    </div>
                </t>
            </templates>
        </kanban>
    </field>
</record>
```

## 🧪 Testing

### Ejecutar Tests

```bash
# En container Docker
docker-compose exec odoo odoo -c /etc/odoo/odoo.conf \
  --test-enable \
  --stop-after-init \
  -u my_module

# O directamente
docker-compose run --rm odoo odoo \
  -d odoo -u my_module --test-enable --stop-after-init
```

### Agregar Tests

```python
# tests/test_my_feature.py
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestMyFeature(TransactionCase):

    def test_feature_x(self):
        # Tu test aquí
        pass
```

## 📦 Instalación del Módulo

### En Docker

```bash
# El módulo ya está disponible
# 1. Acceder a Odoo: http://localhost:8069
# 2. Activar modo desarrollador
# 3. Apps → Update Apps List
# 4. Buscar "My Module"
# 5. Install
```

### En Odoo Existente

```bash
# 1. Copiar módulo a addons path
cp -r my_module /path/to/odoo/addons/

# 2. Actualizar lista de apps
# Apps → Update Apps List

# 3. Instalar desde UI
```

## 🌟 Mejores Prácticas Incluidas

1. **Estructura estándar**: Sigue convenciones Odoo
2. **Seguridad**: Grupos y permisos incluidos
3. **Tests**: Framework de testing configurado
4. **Docker**: Desarrollo containerizado
5. **Demo data**: Datos de ejemplo
6. **Documentación**: README y descripción HTML
7. **Iconografía**: Icon.png placeholder
8. **Licencia**: LGPL-3 incluida

## 📚 Recursos Adicionales

### Documentación Odoo
- [Odoo Developer Documentation](https://www.odoo.com/documentation/18.0/developer.html)
- [ORM API Reference](https://www.odoo.com/documentation/18.0/developer/reference/backend/orm.html)

### Tutoriales
- [Building a Module](https://www.odoo.com/documentation/18.0/developer/tutorials/getting_started.html)
- [Testing in Odoo](https://www.odoo.com/documentation/18.0/developer/reference/backend/testing.html)

## 🔄 Actualización

Para actualizar el template con cambios upstream:

```bash
# Agregar remote del template original
git remote add template https://github.com/intaky-dev/module_template.git

# Fetch cambios
git fetch template

# Merge selectivo
git cherry-pick <commit-hash>
```

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
