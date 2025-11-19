# Documentación: intaky-dev/langflow

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/langflow`
**Tipo:** Aplicación / Configuración Docker
**Tecnología:** Python, Langflow, Docker, JSON
**Propósito:** Agentes de IA especializados para desarrollo Odoo
**URL:** https://github.com/intaky-dev/langflow

## 🎯 Descripción

Repositorio que contiene configuración Docker de Langflow y flujos (flows) de agentes especializados para asistir en diferentes aspectos del desarrollo de módulos Odoo. Incluye 4 agentes principales: Arquitecto, Desarrollador, Testing y Despliegue.

**Langflow** es una plataforma visual para construir workflows de IA mediante interfaz drag-and-drop, basada en LangChain.

## 📁 Estructura del Repositorio

```
langflow/
├── README.md                              # Documentación básica
├── docker-compose.yml                     # Stack Docker
├── flows/                                 # Flujos de agentes
│   ├── agente-arquitecto/                # Diseño de arquitectura
│   │   ├── Agente_Arquitecto_Odoo.json  # Flow v1
│   │   ├── agente_arquitecto_v2.json    # Flow v2 (mejorado)
│   │   ├── generate_flow.py             # Script generador
│   │   ├── INSTRUCCIONES_IMPORTACION_FINAL.md
│   │   ├── CONSTRUCCION_MANUAL.md
│   │   ├── GUIA_INSTALACION.md
│   │   └── [múltiples guías...]
│   ├── agente-desarrollador/             # Asistencia en código
│   │   ├── Agente_Desarrollador_Odoo.json
│   │   ├── prompts.py                   # Prompts personalizados
│   │   └── README.md
│   ├── agente-despliegue/                # Automatización deploy
│   │   ├── Agente_Despliegue_Odoo.json
│   │   └── proyecto-agente-despliegue.md
│   └── agente-testing/                   # Testing y QA
│       ├── Agente_Testing_Odoo.json
│       └── proyecto-agente-testing.md
├── langflow_data/                        # Datos persistentes
│   ├── langflow.db                      # Base de datos SQLite
│   ├── profile_pictures/                # Avatares
│   └── [configuración MCP servers]
├── proyecto-agentes-odoo.md             # Doc general del proyecto
└── proyecto-agentes-odoo-desarrollador.md  # Doc agente desarrollador
```

## 🐳 Docker Setup

### docker-compose.yml

```yaml
version: '3.8'

services:
  langflow:
    image: langflowai/langflow:latest
    ports:
      - "7860:7860"
    environment:
      - LANGFLOW_DATABASE_URL=sqlite:////app/langflow/langflow.db
    volumes:
      - langflow_data:/app/langflow
      - ./flows:/app/flows
    restart: unless-stopped

volumes:
  langflow_data:
    driver: local
```

### Características

- **Persistencia**: Datos mantenidos en volumen `langflow_data`
- **Flows locales**: Directorio `./flows` montado
- **Base de datos**: SQLite integrada
- **Auto-restart**: Reinicio automático
- **Puerto**: 7860 (estándar Langflow)

## 🚀 Uso

### Instalación y Ejecución

```bash
# 1. Clonar repositorio
git clone https://github.com/intaky-dev/langflow.git
cd langflow

# 2. Iniciar Langflow
docker-compose up -d

# 3. Ver logs
docker-compose logs -f

# 4. Acceder a la interfaz
# Abrir navegador: http://localhost:7860
```

### Detener Servicio

```bash
# Detener contenedores
docker-compose down

# Detener y eliminar volúmenes (¡cuidado!)
docker-compose down -v
```

## 🤖 Agentes Especializados

### 1. Agente Arquitecto

**Archivo:** `flows/agente-arquitecto/agente_arquitecto_v2.json`

**Propósito:**
- Diseño de arquitectura de módulos Odoo
- Definición de modelos y relaciones
- Estructura de vistas y seguridad
- Mejores prácticas de desarrollo

**Documentación:**
- `GUIA_INSTALACION.md` - Setup y configuración
- `INSTRUCCIONES_IMPORTACION_FINAL.md` - Cómo importar el flow
- `CONSTRUCCION_MANUAL.md` - Construcción paso a paso
- Múltiples guías específicas

**Características:**
- Versión 2 mejorada con más capacidades
- Script Python para generación automática
- Integración con modelos de IA
- Prompts especializados en Odoo

### 2. Agente Desarrollador

**Archivo:** `flows/agente-desarrollador/Agente_Desarrollador_Odoo.json`

**Propósito:**
- Asistencia en escritura de código Python
- Generación de modelos Odoo
- Creación de vistas XML
- Debugging y optimización

**Archivos:**
- `prompts.py` - Sistema de prompts personalizados
- `README.md` - Documentación del agente

**Características:**
- Prompts específicos para desarrollo Odoo
- Comprensión del ORM de Odoo
- Generación de código siguiendo best practices
- Sugerencias de optimización

### 3. Agente Testing

**Archivo:** `flows/agente-testing/Agente_Testing_Odoo.json`

**Propósito:**
- Creación de tests unitarios
- Validación de funcionalidad
- Testing de vistas y seguridad
- QA y control de calidad

**Documentación:**
- `proyecto-agente-testing.md` - Descripción del proyecto

**Características:**
- Generación de tests para modelos
- Validación de permisos
- Testing de workflows
- Cobertura de código

### 4. Agente Despliegue

**Archivo:** `flows/agente-despliegue/Agente_Despliegue_Odoo.json`

**Propósito:**
- Automatización de despliegues
- Gestión de dependencias
- Configuración de ambientes
- CI/CD para módulos Odoo

**Documentación:**
- `proyecto-agente-despliegue.md` - Descripción del proyecto

**Características:**
- Scripts de despliegue
- Validación pre-deploy
- Rollback automático
- Monitoreo post-deploy

## 📝 Importar Flows

### Método 1: Via UI

```
1. Acceder a http://localhost:7860
2. Click en "Import"
3. Seleccionar archivo JSON del flow
4. Ej: flows/agente-arquitecto/agente_arquitecto_v2.json
5. Click "Import"
```

### Método 2: Via Archivo

```bash
# Copiar flow a directorio de Langflow
docker cp flows/agente-arquitecto/agente_arquitecto_v2.json \
    langflow:/app/flows/
```

### Método 3: Script Python

```bash
# Usar script generador
cd flows/agente-arquitecto
python generate_flow.py
```

## 🔧 Configuración

### Base de Datos

**Ubicación:** `langflow_data/langflow.db`

**Tipo:** SQLite

**Contenido:**
- Flows guardados
- Configuraciones
- Historial de ejecuciones
- Datos de usuarios

### Variables de Entorno

```yaml
# docker-compose.yml
environment:
  - LANGFLOW_DATABASE_URL=sqlite:////app/langflow/langflow.db
  - LANGFLOW_CONFIG_DIR=/app/langflow/config
  - LANGFLOW_LOG_LEVEL=INFO
  - LANGFLOW_CACHE_TYPE=memory
```

### Personalización

```bash
# Editar docker-compose.yml
vim docker-compose.yml

# Agregar variables de entorno
environment:
  - OPENAI_API_KEY=<tu-key>
  - ANTHROPIC_API_KEY=<tu-key>
  - LANGCHAIN_API_KEY=<tu-key>
```

## 💾 Backup

### Backup de Datos

```bash
# Backup de volumen
docker run --rm \
    -v langflow_langflow_data:/data \
    -v $(pwd):/backup \
    alpine tar czf /backup/langflow-backup.tar.gz -C /data .

# Backup de flows
tar czf flows-backup.tar.gz flows/
```

### Restaurar

```bash
# Restaurar volumen
docker run --rm \
    -v langflow_langflow_data:/data \
    -v $(pwd):/backup \
    alpine tar xzf /backup/langflow-backup.tar.gz -C /data

# Restaurar flows
tar xzf flows-backup.tar.gz
```

## 🎯 Casos de Uso

### Desarrollo de Módulo Odoo Completo

```
1. Usar Agente Arquitecto
   - Definir modelos
   - Diseñar vistas
   - Planear seguridad

2. Usar Agente Desarrollador
   - Generar código Python
   - Crear vistas XML
   - Implementar lógica de negocio

3. Usar Agente Testing
   - Crear tests unitarios
   - Validar funcionalidad
   - Verificar permisos

4. Usar Agente Despliegue
   - Preparar despliegue
   - Validar dependencias
   - Deploy a producción
```

### Workflow Recomendado

```mermaid
Arquitecto → Desarrollador → Testing → Despliegue
    ↓           ↓              ↓           ↓
  Design     Código        Tests       Deploy
```

## 📊 Estructura de Flows

### Formato JSON

Los flows de Langflow usan formato JSON con:
- **Nodos**: Componentes del flow (LLMs, Prompts, Tools)
- **Edges**: Conexiones entre nodos
- **Data**: Configuración de cada nodo

Ejemplo simplificado:
```json
{
  "nodes": [
    {
      "id": "llm-1",
      "type": "ChatOpenAI",
      "data": {
        "model": "gpt-4",
        "temperature": 0.7
      }
    },
    {
      "id": "prompt-1",
      "type": "PromptTemplate",
      "data": {
        "template": "Eres un experto en Odoo..."
      }
    }
  ],
  "edges": [
    {
      "source": "prompt-1",
      "target": "llm-1"
    }
  ]
}
```

## 🔒 Seguridad

### API Keys

**Importante:** No commitear API keys en git

```bash
# Usar .env file (no commiteado)
echo "OPENAI_API_KEY=sk-..." > .env

# Actualizar docker-compose.yml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}

# Cargar y ejecutar
docker-compose --env-file .env up -d
```

### Acceso

Por defecto Langflow no tiene autenticación. Para producción:

```yaml
environment:
  - LANGFLOW_AUTH_ENABLED=true
  - LANGFLOW_AUTH_SECRET_KEY=<secret-key>
  - LANGFLOW_SUPERUSER=admin
  - LANGFLOW_SUPERUSER_PASSWORD=<password>
```

## 🐛 Troubleshooting

### Langflow no inicia

```bash
# Ver logs
docker-compose logs langflow

# Verificar puerto
netstat -tulpn | grep 7860

# Reiniciar servicio
docker-compose restart langflow
```

### Flows no aparecen

```bash
# Verificar montaje de volumen
docker inspect langflow | grep -A 10 Mounts

# Verificar permisos
ls -la flows/
```

### Error de base de datos

```bash
# Recrear base de datos
docker-compose down -v
docker-compose up -d
```

## 📚 Referencias

- [Langflow Documentation](https://docs.langflow.org/)
- [LangChain Documentation](https://python.langchain.com/)
- [Odoo Development](https://www.odoo.com/documentation/18.0/developer.html)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
