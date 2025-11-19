# Documentación: intaky-dev/langflow-infra

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/langflow-infra`
**Tipo:** Infraestructura como Código (IaC)
**Tecnología:** Terraform, Helm, Kubernetes
**Propósito:** Despliegue production-ready de Langflow en Kubernetes
**Compatibilidad:** Kubernetes 1.25+, Terraform >= 1.5.0, Helm >= 3.0
**URL:** https://github.com/intaky-dev/langflow-infra

## 🎯 Descripción

Infrastructure as Code (IaC) completa para desplegar Langflow en Kubernetes con alta disponibilidad, auto-scaling (KEDA) y observabilidad completa. Implementa arquitectura Kubernetes nativa con componentes enterprise-grade para entornos productivos.

**Langflow** es una plataforma de desarrollo de workflows con IA que permite crear flujos de trabajo mediante interfaz visual drag-and-drop.

## 🏗️ Arquitectura

### Componentes Principales

#### 1. **Langflow IDE** (Web UI)
- Deployment con múltiples réplicas
- HPA (Horizontal Pod Autoscaler)
- Session affinity para UX
- Interfaz visual para diseño de flujos
- Ejecución read-only

#### 2. **Langflow Runtime** (Workers)
- StatefulSet para identidad persistente
- KEDA autoscaling basado en queue
- Escala de 2 a 10+ workers según carga
- Ejecución de flujos en background

#### 3. **Message Broker** (Cola de Tareas)
**Opciones:**
- **RabbitMQ** (Recomendado producción)
  - Cluster de 3 nodos
  - Quorum queues
  - Persistencia
  - Mejor observabilidad

- **Redis** (Desarrollo/Staging)
  - Sentinel mode
  - Master-replica
  - AOF persistence
  - Menor uso de recursos

#### 4. **PostgreSQL** (Base de Datos)
- PostgreSQL-HA con PgPool
- 3 réplicas con streaming replication
- Automatic failover con repmgr
- Connection pooling y load balancing
- Volúmenes persistentes

#### 5. **Vector Database** (Embeddings)
**Opciones:**
- **Qdrant** (Default)
  - Fácil deploy
  - Buen rendimiento
  - Native filtering

- **Weaviate**
  - GraphQL API
  - Hybrid search
  - Sistema de módulos

- **Milvus**
  - Alto rendimiento
  - Arquitectura distribuida
  - Mejor para large-scale

#### 6. **KEDA** (Event-Driven Autoscaling)
Escala workers basado en:
- Longitud de queue (RabbitMQ/Redis)
- Utilización de CPU
- Utilización de memoria

#### 7. **Observability Stack**
- **Prometheus**: Colección de métricas
- **Grafana**: Visualización y dashboards
- **Loki**: Agregación de logs
- **Alertmanager**: Routing de alertas

#### 8. **Ingress & TLS**
- Nginx Ingress Controller
- cert-manager para certificados automáticos
- Integración Let's Encrypt
- TLS/HTTPS automático

### Diagrama de Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│                      Ingress + TLS                           │
│          (nginx-ingress + cert-manager)                      │
└────────────┬─────────────────────────────┬───────────────────┘
             │                             │
             │                             │
        ┌────▼────┐                   ┌────▼────┐
        │Langflow │                   │Langflow │
        │   IDE   │                   │   API   │
        │ (Web UI)│                   │ Runtime │
        └────┬────┘                   └────┬────┘
             │                             │
             │     ┌──────────┐           │
             └─────►PostgreSQL◄───────────┘
                   │(HA 3 nodes│
                   └────┬──────┘
                        │
              ┌─────────▼──────────┐
              │   Message Broker   │
              │  RabbitMQ / Redis  │
              │   (Cluster Mode)   │
              └─────────┬──────────┘
                        │
              ┌─────────▼──────────┐
              │   Vector Database  │
              │Qdrant/Weaviate/... │
              └────────────────────┘

     ┌──────────────────────────────────┐
     │   Observability Stack             │
     │ Prometheus + Grafana + Loki       │
     └───────────────────────────────────┘
```

## 📁 Estructura del Repositorio

```
langflow-infra/
├── main.tf                        # Módulo raíz Terraform
├── variables.tf                   # Variables de entrada
├── outputs.tf                     # Valores de salida
├── locals.tf                      # Variables locales
├── terraform.tfvars.example       # Configuración ejemplo
├── terraform.tfvars.server        # Config para servidor
├── Makefile                       # Comandos útiles
├── README.md                      # Documentación (520+ líneas)
├── ARCHITECTURE.md                # Arquitectura detallada
├── DEPLOYMENT.md                  # Guía de despliegue
├── QUICKSTART.md                  # Inicio rápido
├── setup-helm-repos.sh            # Script de repos Helm
├── setup-minikube.sh              # Alternativa con Minikube
└── modules/
    ├── message-broker/            # RabbitMQ/Redis
    ├── database/                  # PostgreSQL HA
    ├── vector-db/                 # Qdrant/Weaviate/Milvus
    ├── langflow-ide/              # Deployment IDE
    ├── langflow-runtime/          # StatefulSet runtime
    ├── keda/                      # KEDA autoscaling
    ├── observability/             # Prometheus + Grafana + Loki
    └── ingress/                   # Nginx Ingress + cert-manager
```

## 🚀 Despliegue Rápido

### Prerrequisitos

- Cluster Kubernetes 1.25+
- kubectl configurado
- Terraform >= 1.5.0
- Helm >= 3.0

**Plataformas soportadas:**
- AWS EKS
- Google GKE
- Azure AKS
- On-premises Kubernetes
- Minikube/Kind (testing)

### Instalación en 4 Pasos

```bash
# 1. Clonar y configurar
git clone https://github.com/intaky-dev/langflow-infra.git
cd langflow-infra
cp terraform.tfvars.example terraform.tfvars

# 2. Editar configuración
vim terraform.tfvars

# 3. Desplegar
terraform init
terraform plan
terraform apply

# 4. Obtener outputs
terraform output
```

## ⚙️ Configuración

### Variables Principales

```hcl
# Kubernetes
kubeconfig_path = "~/.kube/config"
namespace       = "langflow"
environment     = "prod"  # dev, staging, prod

# Langflow
langflow_version = "1.0.0"

# Message Broker (elegir uno)
broker_type = "rabbitmq"  # o "redis"

# Vector Database (elegir uno)
vector_db_type = "qdrant"  # o "weaviate" o "milvus"

# Ingress Hosts
ide_ingress_host     = "langflow.yourdomain.com"
runtime_ingress_host = "api.langflow.yourdomain.com"
grafana_ingress_host = "grafana.langflow.yourdomain.com"

# Autoscaling
runtime_min_replicas = 2
runtime_max_replicas = 10
keda_queue_threshold = 5  # mensajes por worker
```

### Configuración de Recursos

```hcl
# IDE Resources
ide_resources = {
  requests = { cpu = "500m", memory = "1Gi" }
  limits   = { cpu = "2000m", memory = "4Gi" }
}

# Runtime Worker Resources
runtime_resources = {
  requests = { cpu = "1000m", memory = "2Gi" }
  limits   = { cpu = "4000m", memory = "8Gi" }
}
```

### Configuración KEDA

```hcl
# Thresholds de Autoscaling
keda_queue_threshold  = 5   # Mensajes por worker
keda_cpu_threshold    = 70  # Porcentaje CPU
keda_memory_threshold = 80  # Porcentaje memoria

# Scaling Limits
runtime_min_replicas = 2
runtime_max_replicas = 10
```

### Configuración por Ambiente

#### Desarrollo
```hcl
environment = "dev"

# Reducir réplicas
postgres_replicas    = 1
rabbitmq_replicas    = 1
vector_db_replicas   = 1
ide_replicas         = 1
runtime_min_replicas = 1
runtime_max_replicas = 3

# Deshabilitar observability
enable_observability = false
```

#### Producción
```hcl
environment = "prod"

# Alta disponibilidad
postgres_replicas    = 3
rabbitmq_replicas    = 3
vector_db_replicas   = 2
ide_replicas         = 2
runtime_min_replicas = 2
runtime_max_replicas = 10

# Observabilidad completa
enable_observability = true
```

## 📊 Alta Disponibilidad

### Database HA
- 3 réplicas PostgreSQL
- Streaming replication
- PgPool: connection pooling + load balancing
- Automatic failover con repmgr
- Persistent volumes

### Message Broker HA

**RabbitMQ:**
- Cluster de 3 nodos
- Quorum queues
- Persistent storage
- Automatic cluster recovery

**Redis:**
- Master-replica con Sentinel
- Automatic failover
- AOF persistence

### Application HA
- Múltiples réplicas IDE con session affinity
- StatefulSet para runtime workers
- PodDisruptionBudget (mínimo 50% disponible)
- Anti-affinity rules (distribución entre nodos)

## 📈 Estrategia de Escalado

### HPA (IDE)
Escala basado en:
- CPU utilization (70%)
- Memory utilization (80%)

### KEDA (Runtime Workers)

**Métrica Primaria:** Longitud de queue
- Escala UP cuando queue > threshold
- Escala DOWN cuando queue vacío

**Métricas Secundarias:**
- CPU utilization
- Memory utilization (safety metric)

**Comportamiento:**
```yaml
Scale Up:
  - 100% incremento cada 30s (agresivo)
  - O agregar 2 pods cada 30s
  - Sin stabilization window

Scale Down:
  - 50% decremento cada 60s (conservador)
  - Stabilization window de 5 minutos
  - Previene flapping
```

## 📊 Observabilidad

### Acceso a Grafana
```
URL: https://grafana.yourdomain.com
```

**Dashboards Pre-configurados:**
- Langflow Overview
- Kubernetes Cluster Monitoring
- PostgreSQL Metrics
- Message Broker Status
- KEDA Autoscaling Metrics

### Prometheus Queries Útiles

```promql
# Longitud de queue
keda_scaler_metrics_value{scaledObject="langflow-runtime-scaler"}

# CPU usage de workers
rate(container_cpu_usage_seconds_total{pod=~"langflow-runtime-.*"}[5m])

# Memory usage de workers
container_memory_usage_bytes{pod=~"langflow-runtime-.*"}

# Request rate
rate(http_requests_total{service="langflow-runtime"}[5m])
```

### Alertas Pre-configuradas

- High memory/CPU usage en workers
- Queue backlog excede threshold
- Database connection issues
- Pod restart loops

## 🔒 Seguridad

### Network Policies
```bash
kubectl apply -f examples/network-policies.yaml
```

### Secrets Management
Credenciales generadas automáticamente:

```bash
# PostgreSQL password
kubectl get secret -n langflow postgresql-credentials \
  -o jsonpath='{.data.password}' | base64 -d

# Grafana password
kubectl get secret -n langflow grafana-credentials \
  -o jsonpath='{.data.admin-password}' | base64 -d
```

### TLS Configuration
```hcl
tls_enabled          = true
cert_manager_enabled = true
letsencrypt_email    = "admin@yourdomain.com"
```

## 💾 Backup & Recovery

### Backup Automático de BD

```hcl
# Habilitar en modules/database/main.tf
backup = {
  enabled = true
  cronjob = {
    schedule = "0 2 * * *"  # Diario 2 AM
  }
}
```

### Backup Manual
```bash
kubectl exec -n langflow postgresql-0 -- \
  pg_dump -U langflow langflow > backup.sql
```

### Restore
```bash
kubectl exec -i -n langflow postgresql-0 -- \
  psql -U langflow langflow < backup.sql
```

## 🔧 Operaciones

### Acceder a Servicios

```bash
# Port-forward (sin ingress)
kubectl port-forward -n langflow svc/langflow-ide 7860:7860
kubectl port-forward -n langflow svc/langflow-runtime-lb 8000:8000

# Acceso via ingress
echo "Langflow IDE: https://langflow.yourdomain.com"
echo "Langflow API: https://api.langflow.yourdomain.com"
```

### Escalar Workers Manualmente
```bash
kubectl scale statefulset -n langflow langflow-runtime --replicas=5
```

### Actualizar Langflow
```hcl
# terraform.tfvars
langflow_version = "1.1.0"
```
```bash
terraform apply
```

### Actualizar Configuración
```bash
# Editar ConfigMap
kubectl edit configmap -n langflow langflow-ide-config

# Restart pods
kubectl rollout restart deployment -n langflow langflow-ide
kubectl rollout restart statefulset -n langflow langflow-runtime
```

## 🐛 Troubleshooting

### Check Pod Status
```bash
kubectl get pods -n langflow
kubectl describe pod -n langflow <pod-name>
kubectl logs -n langflow <pod-name>
```

### Check KEDA Scaling
```bash
kubectl get scaledobject -n langflow
kubectl describe scaledobject -n langflow langflow-runtime-scaler
```

### Check Database
```bash
kubectl exec -it -n langflow postgresql-0 -- \
  psql -U langflow -d langflow -c "SELECT version();"
```

### Check Message Broker

**RabbitMQ:**
```bash
kubectl exec -n langflow rabbitmq-0 -- rabbitmqctl cluster_status
kubectl exec -n langflow rabbitmq-0 -- rabbitmqctl list_queues
```

**Redis:**
```bash
kubectl exec -n langflow redis-master-0 -- redis-cli info replication
```

### Problemas Comunes

**Workers no escalan:**
```bash
# Check KEDA operator logs
kubectl logs -n keda-system -l app=keda-operator

# Verificar ScaledObject
kubectl get scaledobject -n langflow -o yaml
```

**Database connection errors:**
```bash
# Check PostgreSQL logs
kubectl logs -n langflow postgresql-0

# Verificar service
kubectl get svc -n langflow postgresql-pgpool
```

**Ingress no funciona:**
```bash
# Check ingress controller
kubectl get pods -n ingress-nginx

# Verificar ingress
kubectl describe ingress -n langflow
```

## 💰 Optimización de Costos

### Desarrollo (Mínimo)
```hcl
# terraform.tfvars
environment = "dev"
postgres_replicas    = 1
rabbitmq_replicas    = 1
vector_db_replicas   = 1
ide_replicas         = 1
runtime_min_replicas = 1
runtime_max_replicas = 3
enable_observability = false
```

**Recursos estimados:** ~4 vCPU, ~8GB RAM

### Producción (HA Completa)
```hcl
environment = "prod"
postgres_replicas    = 3
rabbitmq_replicas    = 3
vector_db_replicas   = 2
ide_replicas         = 2
runtime_min_replicas = 2
runtime_max_replicas = 10
enable_observability = true
```

**Recursos estimados:** ~12 vCPU, ~24GB RAM (baseline)

## 📚 Documentación Adicional

- **README.md**: Documentación completa (520+ líneas)
- **ARCHITECTURE.md**: Detalles de arquitectura
- **DEPLOYMENT.md**: Guía de despliegue paso a paso
- **QUICKSTART.md**: Inicio rápido

## 🌟 Características Destacadas

1. **Production-ready**: HA, auto-scaling, monitoring
2. **Modular**: Elección de componentes (broker, vector DB)
3. **KEDA Autoscaling**: Event-driven, eficiente
4. **Observabilidad Completa**: Prometheus + Grafana + Loki
5. **Multi-cloud**: AWS, GCP, Azure, on-prem
6. **Terraform Modules**: Reutilizables y mantenibles
7. **TLS Automático**: cert-manager + Let's Encrypt
8. **Backup Integrado**: Backup automático de BD

## 🔗 Referencias

- [Langflow](https://github.com/logspace-ai/langflow)
- [KEDA](https://keda.sh)
- [Bitnami Helm Charts](https://github.com/bitnami/charts)
- [Prometheus Operator](https://github.com/prometheus-operator/kube-prometheus)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
