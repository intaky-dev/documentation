# Documentación: intaky-dev/my-library

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/my-library`
**Sistema:** kast-system (Kubernetes Arcane Spelling Technology)
**Tipo:** Framework de Test-Driven Development (TDD) para Helm
**Licencia:** GNU GPL v3
**URL:** https://github.com/intaky-dev/my-library

## 🎯 Descripción

kast-system es un framework de desarrollo basado en Test-Driven Development (TDD) para despliegues de Kubernetes usando Helm charts. Implementa una arquitectura modular llamada "glyphs" (glifos) que son plantillas de Helm reutilizables y componibles, diseñadas para facilitar la gestión de infraestructura de Kubernetes de manera declarativa y testeable.

El sistema utiliza una nomenclatura temática basada en magia/arcano:
- **Glyphs (Glifos)**: Plantillas Helm reutilizables
- **Kaster**: Orquestador de glifos
- **Summon**: Chart base para despliegue de workloads
- **Librarian**: Orquestador de ArgoCD App of Apps
- **Bookrack**: Gestión de configuración usando patrón book/chapter/spell
- **Trinkets**: Wrappers opinados alrededor de glyphs

## 🏗️ Arquitectura

### Componentes Principales

#### 1. **Glyphs** (Biblioteca de Plantillas)
Ubicación: `charts/glyphs/`

Plantillas Helm reutilizables que proporcionan funcionalidades específicas:

| Glyph | Propósito |
|-------|-----------|
| `vault` | Integración con HashiCorp Vault para gestión de secretos |
| `istio` | Configuración de service mesh (VirtualService, Gateway) |
| `summon` | Plantillas para workloads (Deployment, Service, etc.) |
| `certManager` | Gestión de certificados TLS |
| `crossplane` | Provisión de infraestructura multi-cloud |
| `gcp` | Recursos específicos de Google Cloud Platform |
| `keycloak` | Gestión de identidad y acceso |
| `argo-events` | Procesamiento de eventos y triggers |
| `common` | Helpers y funciones comunes |
| `freeForm` | Recursos Kubernetes en formato libre |
| `runic-system` | Sistema de indexación y descubrimiento |

#### 2. **Kaster** (Orquestador de Glyphs)
Chart que coordina múltiples glyphs, itera a través de definiciones de glyphs e invoca las plantillas correspondientes.

#### 3. **Summon** (Chart Base de Workload)
Maneja el despliegue de workloads con soporte para:
- Deployment / StatefulSet
- Service (ClusterIP, NodePort, LoadBalancer)
- PersistentVolumeClaim
- HorizontalPodAutoscaler
- ServiceAccount

#### 4. **Librarian** (ArgoCD App of Apps)
Lee "books" desde `bookrack/` y genera automáticamente ArgoCD Applications.

#### 5. **Bookrack** (Gestión de Configuración)
Sistema de configuración usando el patrón book/chapter/spell:
```
bookrack/
└── my-app-of-apps/
    ├── index.yaml          # Metadatos del book
    ├── infrastructure/     # Capítulo de infraestructura
    │   ├── 00-metallb.yaml
    │   ├── 01-istio-base.yaml
    │   └── 03-istio-ingressgateway.yaml
    └── applications/       # Capítulo de aplicaciones
        └── langflow.yaml
```

#### 6. **Trinkets** (Wrappers Especializados)
Wrappers opinados alrededor de glyphs para casos de uso específicos:

- **Microspell**: Microservicios con integración Istio + Vault
- **Tarot**: Generación dinámica de workflows de Argo Workflows
- **Covenant**: Gestión de identidad y acceso (Keycloak + Vault + RBAC)

### Flujo de Datos

```
Book (bookrack/)
  ├─ index.yaml          # Metadatos del book, versiones de charts
  └─ chapters/
      └─ spell.yaml      # Configuración de aplicación
          ↓
Librarian (ArgoCD ApplicationSet)
  ├─ Lee archivos spell
  ├─ Detecta estrategia de despliegue
  └─ Genera ArgoCD Application
          ↓
ArgoCD Application
  ├─ Source 1: Helm chart (kaster/summon/trinket)
  └─ Source 2: Values desde bookrack
          ↓
Helm Rendering
  ├─ Kaster → Itera glyphs → Llama plantillas de glyph
  ├─ Summon → Genera recursos de workload
  └─ Trinket → Envuelve glyphs con configuración opinada
          ↓
Kubernetes Resources
  └─ Desplegados en el cluster
```

### Sistema Lexicon y Runic Indexer

**Lexicon**: Registro global en `Values.lexicon` que contiene información de infraestructura disponible (servidores vault, gateways, bases de datos).

**Runic Indexer**: Función de plantilla que consulta entradas del lexicon usando selectores de etiquetas. Permite que los glyphs descubran dinámicamente la infraestructura necesaria.

Ejemplo:
```go
{{- $infrastructure := include "runicIndexer.runicIndexer"
     (list $root.Values.lexicon
           $glyphDefinition.selector
           "resource-type"
           $root.Values.chapter.name) | fromJson }}
```

## 🧪 Metodología TDD

### Filosofía Red-Green-Refactor

kast-system está construido 100% con TDD. Cada feature, plantilla y glyph sigue el ciclo:

1. **🔴 RED**: Escribir tests/ejemplos que fallen primero
2. **🟢 GREEN**: Implementar código mínimo para que pasen los tests
3. **🔵 REFACTOR**: Mejorar el código manteniendo la cobertura de tests

### Comandos TDD Principales

```bash
# Workflow TDD
make tdd-red         # Ejecutar tests esperando fallos (fase Red)
make tdd-green       # Ejecutar tests esperando éxito (fase Green)
make tdd-refactor    # Ejecutar tests después de refactorizar (fase Blue)

# Testing
make test            # Tests TDD comprensivos (rendering + completitud)
make test-all        # TODOS los tests (comprehensive + snapshots + glyphs)
make test-comprehensive  # Test rendering + completitud de recursos
make test-snapshots  # Test snapshots + validación de esquema K8s
make test-syntax     # Validación rápida de sintaxis

# Estado de Testing
make test-status     # Mostrar estado de testing para todos los charts/glyphs

# Testing de Glyphs
make glyphs <name>         # Test de glyph específico (ej: make glyphs vault)
make test-glyphs-all       # Test de todos los glyphs automáticamente
make list-glyphs           # Listar todos los glyphs disponibles

# Snapshots
make generate-snapshots CHART=<name>     # Generar snapshots para chart
make update-snapshot CHART=<name> EXAMPLE=<example>
make update-all-snapshots                # Actualizar todos los snapshots
make show-snapshot-diff CHART=<name> EXAMPLE=<example>

# Desarrollo
make create-example CHART=summon EXAMPLE=my-test
make inspect-chart CHART=summon EXAMPLE=basic-deployment
make watch          # Auto-ejecutar tests al cambiar archivos
make lint           # Helm lint de todos los charts
```

### Workflow de Desarrollo TDD

#### Agregar Nueva Feature

```bash
# 1. RED PHASE - Escribir test que falle
make create-example CHART=summon EXAMPLE=my-new-feature
# Editar charts/summon/examples/my-new-feature.yaml

# 2. Confirmar que falla
make tdd-red
# Debería mostrar: ❌ summon-my-new-feature (expectations failed)

# 3. GREEN PHASE - Implementar feature
# Editar plantillas de summon

# 4. Verificar que pasa
make tdd-green
# Debería mostrar: ✅ summon-my-new-feature

# 5. REFACTOR PHASE - Limpiar implementación
# Mejorar código, agregar documentación
make tdd-refactor

# 6. SNAPSHOT PHASE - Fijar output esperado
make generate-snapshots CHART=summon
```

#### Desarrollo de Glyphs

```bash
# 1. RED PHASE - Agregar ejemplo de feature
# Editar charts/glyphs/vault/examples/new-feature.yaml

# 2. Ver fallo (Red)
make glyphs vault
# Debería mostrar: ❌ vault-new-feature (rendering failed)

# 3. GREEN PHASE - Implementar glyph feature
# Editar charts/glyphs/vault/templates/

# 4. Ver éxito (Green)
make glyphs vault
# Debería mostrar: ✅ vault-new-feature

# 5. Generar output esperado
make generate-expected GLYPH=vault

# 6. REFACTOR PHASE
make glyphs vault
```

## 📁 Estructura del Repositorio

```
kast-system/
├── charts/
│   ├── glyphs/              # Biblioteca de plantillas reutilizables
│   │   ├── vault/           # Integración con Vault
│   │   ├── istio/           # Service mesh
│   │   ├── summon/          # Plantillas de workload
│   │   ├── certManager/     # Certificados TLS
│   │   ├── crossplane/      # Provisión multi-cloud
│   │   ├── gcp/             # Recursos GCP
│   │   ├── keycloak/        # IAM
│   │   ├── argo-events/     # Procesamiento de eventos
│   │   ├── common/          # Helpers comunes
│   │   ├── freeForm/        # Recursos libres
│   │   ├── runic-system/    # Sistema de indexación
│   │   ├── s3/              # Almacenamiento S3
│   │   ├── postgres-cloud/  # PostgreSQL cloud
│   │   └── default-verbs/   # Verbos por defecto
│   ├── kaster/              # Orquestador de glyphs
│   ├── summon/              # Chart base de workload
│   └── trinkets/            # Wrappers opinados
│       ├── microspell/      # Microservicios
│       ├── tarot/           # Argo Workflows
│       └── covenant/        # Gestión de identidad
├── librarian/               # ArgoCD App of Apps
├── bookrack/                # Books de configuración
│   └── my-app-of-apps/
│       ├── index.yaml       # Metadatos del book
│       ├── infrastructure/  # Infraestructura base
│       └── applications/    # Aplicaciones
├── docs/                    # Documentación
│   ├── TDD_COMMANDS.md      # Referencia de comandos TDD
│   ├── TAROT.md             # Workflows Tarot
│   ├── GETTING_STARTED.md   # Guía de inicio
│   ├── LIBRARIAN.md         # Documentación Librarian
│   ├── GLYPHS_REFERENCE.md  # Referencia de glyphs
│   ├── GLOSSARY.md          # Glosario de términos
│   └── glyphs/              # Documentación por glyph
├── tests/                   # Infraestructura de testing TDD
│   └── scripts/             # Scripts de validación
├── output-test/             # Outputs de tests generados (auto)
├── Makefile                 # Comandos TDD (730 líneas)
├── README.md                # Documentación principal
├── CLAUDE.md                # Instrucciones para Claude Code
├── CODING_STANDARDS.md      # Estándares de código
├── DEPLOY_APP_OF_APPS.md    # Guía de despliegue
├── LICENSE                  # GNU GPL v3
└── argocd-app-of-apps.yaml  # ArgoCD application
```

## 🎓 Conceptos Clave

| Concepto | Descripción |
|----------|-------------|
| **Spell** | Archivo YAML en bookrack chapter que define despliegue de aplicación |
| **Chapter** | Agrupación lógica de spells en un book (ej: intro, services, monitoring) |
| **Book** | Contexto de despliegue (environment, cluster, team) |
| **Glyph** | Plantilla Helm nombrada para funcionalidad específica |
| **Rune** | Chart Helm adicional desplegado junto al spell principal |
| **Lexicon** | Registro de infraestructura global con descubrimiento basado en labels |
| **Position** | Orden de ejecución de carta Tarot (foundation, action, challenge, outcome) |
| **Kaster** | Orquestador que itera glyphs y llama sus plantillas |
| **Trinket** | Wrapper opinado alrededor de glyphs para casos de uso específicos |

## 🚀 Quick Start

```bash
# Clonar el repositorio
git clone https://github.com/intaky-dev/my-library.git
cd my-library

# Verificar que el sistema TDD funciona
make test

# Ver todos los comandos disponibles
make help

# Explorar glyphs disponibles
make list-glyphs

# Probar un glyph específico
make glyphs vault

# Crear primera feature usando TDD
make create-example CHART=summon EXAMPLE=my-feature
make tdd-red      # Debería fallar inicialmente
# Implementar feature
make tdd-green    # Debería pasar después de implementación
make tdd-refactor # Debería seguir pasando después de limpieza

# Ver estado de testing
make test-status
```

## 📊 Sistema de Testing

### Capas de Testing

1. **Validación de Sintaxis** (`make test-syntax`)
   - Valida sintaxis de plantillas Helm
   - Feedback rápido durante desarrollo
   - No requiere cluster K8s

2. **Testing Comprensivo** (`make test-comprehensive`)
   - Validación de rendering
   - Checks de completitud de recursos
   - Valida que se generen los recursos K8s esperados

3. **Testing de Snapshots** (`make test-snapshots`)
   - Comparación de snapshots: Output coincide con YAML esperado
   - Validación de esquema K8s: `helm install --dry-run` valida contra API K8s
   - Detecta cambios no intencionales y valores inválidos

4. **Testing de Glyphs** (`make test-glyphs-all`)
   - Tests de todos los glyphs a través de orquestación kaster
   - Descubrimiento automático de glyphs con examples/
   - Validación basada en snapshots

5. **Testing de Covenant Books** (`make test-covenant`)
   - Tests de covenant books (IAM)
   - Lee estructura completa del book, no spells individuales
   - Valida recursos Keycloak (Realm, Clients, Users, Groups)
   - Valida generación de secretos Vault para OIDC

### Validación de Completitud de Recursos

El sistema valida que se generen todos los recursos esperados:
- **Workload Resources**: Deployment cuando `workload.type=deployment`, StatefulSet cuando `workload.type=statefulset`
- **Service Resources**: Service cuando `service.enabled=true`
- **Storage Resources**: PVC cuando `volumes.*.type=pvc`
- **Scaling Resources**: HPA cuando `autoscaling.enabled=true`
- **Security Resources**: ServiceAccount cuando `serviceAccount.enabled=true`

## 🔧 Estándares de Desarrollo

### Convenciones de Nomenclatura

**Templates de Glyph:**
```helm
# ✅ Correcto
{{- define "istio.virtualService" }}
{{- define "vault.secret" }}
{{- define "summon.persistentVolumeClaim" }}

# ❌ Incorrecto
{{- define "summon.pvc" }}        # Abreviación
{{- define "istio.vs" }}          # Abreviación
```

### Patrón de Parámetros Estándar

```helm
# Patrón estándar para todos los glyphs:
{{- $root := index . 0 -}}
{{- $glyphDefinition := index . 1 -}}

# Uso:
{{- include "glyph.template" (list $root $glyphDefinition) }}
```

### Reglas TDD

#### Hacer ✅
- Escribir tests primero
- Ejecutar `tdd-red` para verificar que los tests fallen
- Hacer cambios mínimos para que pasen los tests
- Refactorizar de manera segura manteniendo cobertura de tests
- Probar completitud de recursos
- Usar ejemplos como documentación

#### No Hacer ❌
- Saltar la fase red
- Implementar sin tests
- Romper tests existentes
- Saltar validación
- Hacer commit de tests que fallen

## 📚 Documentación Adicional

- **TDD Commands Reference**: `docs/TDD_COMMANDS.md`
- **Coding Standards**: `CODING_STANDARDS.md`
- **Tarot Workflows**: `docs/TAROT.md`
- **ApplicationSets Guide**: `docs/applicationset-guide.md`
- **Claude Code Instructions**: `CLAUDE.md`
- **Getting Started**: `docs/GETTING_STARTED.md`
- **Glyphs Reference**: `docs/GLYPHS_REFERENCE.md`
- **Glossary**: `docs/GLOSSARY.md`

## 🎯 Estrategias de Despliegue

Librarian detecta la estrategia de despliegue desde la configuración del spell:

1. **Simple Application**: Tiene `name`, `image` → Usa chart Summon
2. **Infrastructure**: Tiene `glyphs` → Usa chart Kaster
3. **Multi-Source**: Tiene `runes` → Múltiples fuentes de charts (Summon + Kaster + charts adicionales)
4. **External Chart**: Tiene `repository`, `chart` → Despliegue directo de chart

## 💡 Casos de Uso

### Desplegar Microservicio Simple

```yaml
# bookrack/my-book/chapter/my-app.yaml
name: my-app
image: registry.io/my-app:v1.0
replicas: 3
service:
  enabled: true
  type: ClusterIP
  port: 8080
```

### Infraestructura con Glyphs

```yaml
# bookrack/my-book/chapter/vault-setup.yaml
glyphs:
  vault:
    - type: secret
      path: secret/data/myapp
      data:
        username: admin
        password: secret123
```

### Microservicio con Istio + Vault

```yaml
# Usando trinket microspell
name: api-service
microservice:
  image: registry.io/api:v2.0
  routing:
    istio:
      enabled: true
      host: api.example.com
  secrets:
    vault:
      enabled: true
      path: secret/data/api
```

## 🔒 Seguridad

- Todos los archivos incluyen header de copyright con licencia GNU GPL v3
- Gestión de secretos a través de HashiCorp Vault
- Integración con Keycloak para IAM
- Validación de esquemas K8s en CI/CD
- Testing automático de recursos de seguridad (ServiceAccounts, RBAC)

## 🤝 Integración GitOps

- Diseñado para despliegue con ArgoCD
- GitHub Actions sincronizan automáticamente componentes a repositorios separados
- Los cambios disparan etiquetado y releases automáticos
- Librarian genera ApplicationSets de ArgoCD automáticamente

## 📈 Estado de Cobertura de Testing

Ver estado actual con: `make test-status`

**Completamente Testeado** (✅ Examples + Snapshots):
- summon: 17 ejemplos
- argo-events: 5 ejemplos
- vault: 11 ejemplos
- istio: 2 ejemplos
- common: 2 ejemplos

**Necesita Snapshots** (⚠️ Ejemplos existen):
- kaster: 1 ejemplo
- certManager: 2 ejemplos
- crossplane: 2 ejemplos
- freeForm: 2 ejemplos
- gcp: 3 ejemplos
- runic-system: 3 ejemplos
- microspell: 8 ejemplos
- tarot: 14 ejemplos

**Necesita Trabajo TDD** (❌ Sin examples/):
- librarian
- default-verbs
- keycloak
- postgres-cloud
- covenant

## 🌟 Características Destacadas

1. **TDD Obligatorio**: Todo el framework está construido con metodología TDD
2. **Descubrimiento Automático**: Sistema de testing descubre automáticamente charts, glyphs y trinkets
3. **Validación Multi-Capa**: Sintaxis, rendering, completitud de recursos, snapshots, esquema K8s
4. **Arquitectura Modular**: Glyphs componibles y reutilizables
5. **GitOps Native**: Integración profunda con ArgoCD
6. **Lexicon & Runic Indexer**: Descubrimiento dinámico de infraestructura
7. **Testing de Regresión**: Snapshots previenen cambios no intencionales
8. **Documentación Viva**: Ejemplos sirven como tests y documentación

## 📞 Contacto y Soporte

Para contribuir o reportar issues, visita el repositorio en GitHub:
https://github.com/intaky-dev/my-library

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
