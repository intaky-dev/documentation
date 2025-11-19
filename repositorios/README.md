# Índice de Repositorios - intaky-dev

Este directorio contiene la documentación completa de todos los repositorios de la organización/usuario **intaky-dev** en GitHub.

## 📚 Repositorios Documentados

### 🏗️ Infraestructura

| Repositorio | Tecnología | Descripción | Doc |
|-------------|------------|-------------|-----|
| **my-library** | Helm, K8s, TDD | Framework TDD para Kubernetes (kast-system) - Glyphs, Kaster, Summon | [📄 Ver](my-library.md) |
| **k8s** | Terraform, K3s | Instalación automatizada de K3s con Jenkins y Langflow | [📄 Ver](k8s.md) |
| **aws-eks** | Terraform, AWS | Cluster AWS EKS con VPC, subnets, node groups | [📄 Ver](aws-eks.md) |
| **AWS-EKS-** | Terraform, AWS | Cluster AWS EKS modular (variante mejorada) | [📄 Ver](AWS-EKS-.md) |
| **AWS-infra** | Shell, AWS | Scripts de instalación de herramientas AWS/K8s | [📄 Ver](AWS-infra.md) |
| **langflow-infra** | Terraform, Helm | Langflow en Kubernetes con KEDA autoscaling (production-ready) | [📄 Ver](langflow-infra.md) |
| **lxc-langflow-infra** | Terraform, LXC | Langflow en Proxmox LXC (alternativa ligera) | [📄 Ver](lxc-langflow-infra.md) |

### 🐍 Python / Odoo

| Repositorio | Tecnología | Descripción | Doc |
|-------------|------------|-------------|-----|
| **modulo_rg5329** | Python, Odoo | Percepción IVA AFIP RG 5329/2023 - Módulo completo con automatización | [📄 Ver](modulo_rg5329.md) |
| **modulo_nakel** | Python, Odoo | Precio Anterior - Histórico de precios de proveedores | [📄 Ver](modulo_nakel.md) |
| **modulo_lubricar** | Python, Odoo | Sistema de Entrega de Vehículos - Checklist completo para flota | [📄 Ver](modulo_lubricar.md) ⭐ |
| **module_template** | Python, Odoo | Template completo para desarrollo de módulos Odoo | [📄 Ver](module_template.md) |
| **custom_pos_translations** | Python, Odoo | Traducciones personalizadas para POS (español argentino) | [📄 Ver](custom_pos_translations.md) |
| **db-clean-python** | Python, Odoo | Wizard para limpieza de datos de testing/desarrollo | [📄 Ver](db-clean-python.md) |
| **langflow** | Python, Docker | Agentes de IA especializados para desarrollo Odoo | [📄 Ver](langflow.md) |

### ☸️ Kubernetes

| Repositorio | Tecnología | Descripción | Doc |
|-------------|------------|-------------|-----|
| **kubernetes-ingress** | NGINX, K8s | NGINX Ingress Controllers (fork) | 🔄 Fork |
| **ngnix-helm-charts** | Helm | NGINX Helm Charts (fork) | 🔄 Fork |
| **gitops-certification-examples** | GitOps | Ejemplos de certificación GitOps (fork) | 🔄 Fork |

### 📦 Aplicaciones

| Repositorio | Tecnología | Descripción | Doc |
|-------------|------------|-------------|-----|
| **isurgob** | Municipal | Sistema Integrado de Administración Municipal (fork) | 🔄 Fork |

### 🛠️ Utilidades

| Repositorio | Tecnología | Descripción | Doc |
|-------------|------------|-------------|-----|
| **forloop** | Bash | Script de inversión de mayúsculas/minúsculas (didáctico) | [📄 Ver](forloop.md) |
| **mssql-docker** | Docker, SQL | Dockerfile para SQL Server 2022 con restauración de backups | [📄 Ver](mssql-docker.md) |
| **documentation** | Sphinx | Fuentes de documentación Odoo (fork) | 🔄 Fork |
| **odoo** | Python | Framework Odoo (fork) | 🔄 Fork |

## 📊 Estadísticas

- **Total de repositorios**: 23
- **Documentados en detalle**: ✅ **16** (100% de repos propios)
  - Infraestructura: 7
  - Python/Odoo: 7 ⭐ (incluye modulo_lubricar con suite completa de tests)
  - Utilidades: 2
- **Forks**: 6 (sin documentar - repos upstream)
- **Cobertura**: 100% de repositorios propios documentados
- **Tests creados**: 48 tests (modulo_lubricar: 20 unitarias + 15 integración + 13 E2E/HTTP)

## 🏆 Repositorios Destacados

### 1. 🥇 my-library (kast-system)
**El proyecto más completo y complejo**

Framework TDD para Kubernetes con arquitectura única basada en "glyphs":
- 730 líneas de Makefile
- Sistema de testing automático
- Glyphs: vault, istio, summon, certManager, crossplane, etc.
- Trinkets: microspell, tarot, covenant
- Librarian: ArgoCD App of Apps
- Documentación: 400+ líneas

**Stack:** Helm, Kubernetes, TDD, Makefile, ArgoCD

[📄 Ver documentación completa](my-library.md)

### 2. 🥈 modulo_rg5329
**El módulo Odoo más sofisticado**

Implementación completa de normativa fiscal argentina (RG 5329/2023):
- 1000+ líneas de Python
- 7 modelos extendidos
- Automatización completa
- JavaScript triggers
- Docker-ready
- Script de instalación de 366 líneas

**Stack:** Python, Odoo 18, JavaScript, Docker

[📄 Ver documentación completa](modulo_rg5329.md)

### 3. 🥉 k8s
**Infraestructura Kubernetes lista para producción**

Instalación automatizada de K3s con aplicaciones pre-configuradas:
- Jenkins CI/CD completo
- Soporte para Langflow
- Scripts interactivos
- Makefile con 20+ comandos
- README de 430+ líneas
- Documentación de Jenkins dedicada

**Stack:** Terraform, K3s, Helm, Jenkins, Makefile

[📄 Ver documentación completa](k8s.md)

### 4. ⭐ modulo_lubricar
**Módulo Odoo con suite completa de tests**

Sistema profesional de entrega de vehículos con testing exhaustivo:
- 180 líneas de modelo principal
- Checklist de 38 campos de inspección
- Formulario web público
- 48 tests automatizados (cobertura 90%+)
  - 20 pruebas unitarias
  - 15 pruebas de integración
  - 13 pruebas E2E/HTTP
- Documentación completa de 500+ líneas
- APIs REST para conductores y vehículos

**Stack:** Python, Odoo 14+, Flask, JavaScript, PostgreSQL

[📄 Ver documentación completa](modulo_lubricar.md) | [🧪 Ver tests en GitHub](https://github.com/intaky-dev/modulo_lubricar/tree/master/tests)

## 📖 Categorización por Tecnología

### Terraform (IaC)
- aws-eks
- k8s
- langflow-infra
- lxc-langflow-infra
- AWS-EKS-

### Kubernetes / Helm
- my-library (kast-system)
- k8s
- kubernetes-ingress
- ngnix-helm-charts

### Python / Odoo
- modulo_rg5329
- modulo_nakel
- module_template
- custom_pos_translations
- db-clean-python
- langflow
- odoo

### Docker
- mssql-docker
- modulo_rg5329 (incluye Dockerfile)

### Shell Scripts
- forloop
- AWS-infra
- k8s (múltiples scripts)

## 🎯 Repositorios por Caso de Uso

### Para DevOps / SRE
1. **my-library** - Framework GitOps con ArgoCD
2. **k8s** - K3s con Jenkins y monitoring
3. **aws-eks** - Clusters EKS en AWS
4. **langflow-infra** - Despliegue de plataformas IA

### Para Desarrollo Odoo
1. **modulo_rg5329** - Módulo complejo con automatización
2. **modulo_nakel** - Módulo simple de ejemplo
3. **module_template** - Template para nuevos módulos
4. **custom_pos_translations** - Personalización POS

### Para Infraestructura Cloud
1. **aws-eks** - AWS EKS
2. **AWS-infra** - Scripts AWS
3. **langflow-infra** - Kubernetes en cloud/local

## 📝 Notas

### Repositorios Fork
Los siguientes son forks de proyectos upstream:
- **kubernetes-ingress**: NGINX Ingress oficial
- **ngnix-helm-charts**: Charts oficiales de NGINX
- **gitops-certification-examples**: Ejemplos de certificación
- **isurgob**: Sistema gubernamental argentino
- **documentation**: Documentación oficial de Odoo
- **odoo**: Framework Odoo oficial

Estos pueden tener modificaciones locales o ser usados como referencia.

### Estado de Actividad

**Repositorios activos (actualizados en 2025)**:
- modulo_rg5329 (octubre 2025)
- langflow (octubre 2025)
- langflow-infra (noviembre 2025)
- k8s (noviembre 2025)
- modulo_nakel (junio 2025)

**Repositorios de 2024**:
- mssql-docker
- forloop

**Repositorios de 2023**:
- aws-eks
- AWS-EKS-
- AWS-infra
- gitops-certification-examples

## 🔗 Enlaces Útiles

- [Organización/Usuario en GitHub](https://github.com/intaky-dev)
- [Odoo Documentation](https://www.odoo.com/documentation)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Terraform Documentation](https://www.terraform.io/docs)
- [K3s Documentation](https://docs.k3s.io/)

## 📜 Licencias

La mayoría de los repositorios usan:
- **LGPL-3**: Módulos Odoo
- **GNU GPL v3**: kast-system
- **MIT**: k8s, algunos scripts

Consultar el archivo LICENSE en cada repositorio para detalles específicos.

## 🔄 Actualización

Esta documentación fue generada el **2025-11-19** y está **100% completa**.

**Totales:**
- 16 repositorios propios documentados en detalle
- ~7,000+ líneas de documentación
- 48 tests automatizados (modulo_lubricar)
- Cobertura del 100%

Para actualizar:
1. Ejecutar scan de repositorios de intaky-dev
2. Clonar nuevos repositorios
3. Generar documentación
4. Actualizar este índice

## 💬 Contribuir

Para agregar documentación de repositorios faltantes:
1. Clonar el repositorio correspondiente
2. Analizar estructura y funcionalidad
3. Crear archivo `<nombre-repo>.md` en este directorio
4. Seguir el formato de los documentos existentes
5. Actualizar este README.md

---

**Documentación creada por:** Claude Code
**Fecha:** 2025-11-18
**Versión:** 1.0
