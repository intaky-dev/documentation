# Documentación: intaky-dev/lxc-langflow-infra

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/lxc-langflow-infra`
**Tipo:** Infraestructura como Código (IaC)
**Tecnología:** Terraform, Proxmox LXC, HCL
**Propósito:** Despliegue de Langflow en Proxmox usando contenedores LXC
**Compatibilidad:** Proxmox VE 7.0+, Terraform >= 1.5.0
**URL:** https://github.com/intaky-dev/lxc-langflow-infra

## 🎯 Descripción

Infrastructure as Code para desplegar Langflow en Proxmox usando contenedores LXC en lugar de Kubernetes. Proporciona solución escalable y de alta disponibilidad con menor overhead que VMs completas, ideal para entornos on-premise o edge computing.

**Ventajas de LXC vs K8s:**
- Menor consumo de recursos
- Boot más rápido
- Más simple de gestionar
- Ideal para hardware limitado
- Acceso directo a recursos del host

## 🏗️ Arquitectura

### Topología de Red

```
┌──────────────────────────────────────────────────────┐
│              Proxmox VE Host                          │
│                                                       │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐    │
│  │ Langflow   │  │ Runtime    │  │ Runtime    │    │
│  │    IDE     │  │  Worker 1  │  │  Worker 2  │    │
│  │ (LXC 10)   │  │ (LXC 20)   │  │ (LXC 21)   │    │
│  │Port 7860   │  │            │  │            │    │
│  └─────┬──────┘  └─────┬──────┘  └─────┬──────┘    │
│        │               │                │           │
│  ┌─────▼───────────────▼────────────────▼──────┐   │
│  │          PostgreSQL/MySQL                    │   │
│  │             (LXC 30)                         │   │
│  │            Port 5432                         │   │
│  └─────┬──────────────────────────────────────┘    │
│        │                                            │
│  ┌─────▼──────────────────────────────────────┐   │
│  │       Redis/RabbitMQ                        │   │
│  │          (LXC 40)                           │   │
│  │       Port 6379/5672                        │   │
│  └─────┬──────────────────────────────────────┘    │
│        │                                            │
│  ┌─────▼──────────────────────────────────────┐   │
│  │       Vector DB (Qdrant/Weaviate)          │   │
│  │          (LXC 50)                           │   │
│  │          Port 6333                          │   │
│  └────────────────────────────────────────────┘    │
│                                                     │
│  ┌────────────────────────────────────────────┐   │
│  │  Monitoring (Prometheus + Grafana)         │   │
│  │          (LXC 60) - Opcional               │   │
│  │       Port 9090/3000                       │   │
│  └────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────┘
```

### Componentes LXC

| LXC ID | Componente | Puerto | CPU | RAM | Disco |
|--------|-----------|--------|-----|-----|-------|
| 10 | Langflow IDE | 7860 | 2 | 4GB | 20GB |
| 20-2X | Runtime Workers | 8000 | 2 | 4GB | 20GB |
| 30 | PostgreSQL/MySQL | 5432/3306 | 2 | 4GB | 40GB |
| 40 | Redis/RabbitMQ | 6379/5672 | 2 | 2GB | 10GB |
| 50 | Vector DB | 6333 | 2 | 4GB | 40GB |
| 60 | Monitoring (opcional) | 9090/3000 | 2 | 4GB | 20GB |

## 📁 Estructura del Repositorio

```
lxc-langflow-infra/
├── main.tf                        # Módulo raíz
├── variables.tf                   # Variables de entrada
├── providers.tf                   # Configuración Proxmox provider
├── outputs.tf                     # Outputs (IPs, puertos, etc.)
├── terraform.tfvars.example       # Configuración ejemplo
├── Makefile                       # Comandos útiles
├── README.md                      # Documentación
└── modules/
    ├── lxc-base/                  # Base LXC template
    ├── database/                  # PostgreSQL/MySQL LXC
    ├── message-broker/            # Redis/RabbitMQ LXC
    ├── vector-db/                 # Qdrant/Weaviate/Milvus LXC
    ├── langflow-ide/              # IDE LXC
    ├── langflow-runtime/          # Runtime workers LXC
    └── observability/             # Prometheus + Grafana LXC
```

## 🚀 Despliegue Rápido

### Prerrequisitos

- Proxmox VE 7.0+
- Terraform >= 1.5.0
- Token API de Proxmox
- Template Ubuntu 22.04 LXC

### Configurar Proxmox API

```bash
# En Proxmox
pveum user add terraform@pve
pveum aclmod / -user terraform@pve -role PVEAdmin
pveum user token add terraform@pve terraform-token --privsep=0
```

### Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/intaky-dev/lxc-langflow-infra.git
cd lxc-langflow-infra

# 2. Configurar variables
cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars

# 3. Inicializar
terraform init

# 4. Desplegar
terraform plan
terraform apply
```

## ⚙️ Configuración

### Variables Principales

```hcl
# Proxmox Connection
proxmox_api_url      = "https://proxmox.local:8006/api2/json"
proxmox_api_token_id = "terraform@pve!terraform-token"
proxmox_api_token_secret = "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
proxmox_node         = "pve"

# LXC Template
lxc_template         = "local:vztmpl/ubuntu-22.04-standard_22.04-1_amd64.tar.zst"
lxc_storage          = "local-lvm"

# Network
network_bridge       = "vmbr0"
network_gateway      = "192.168.1.1"
network_nameserver   = "8.8.8.8"

# Langflow
langflow_version     = "1.0.0"

# Component Choices
database_type        = "postgresql"  # o "mysql"
broker_type          = "redis"       # o "rabbitmq"
vector_db_type       = "qdrant"      # o "weaviate" o "milvus"

# Scaling
runtime_workers      = 2             # Número de workers
enable_observability = true          # Monitoring stack
```

### Configuración de Recursos por LXC

```hcl
# IDE
ide_cpu      = 2
ide_memory   = 4096  # MB
ide_disk     = "20"  # GB

# Runtime Workers
runtime_cpu    = 2
runtime_memory = 4096
runtime_disk   = "20"

# Database
db_cpu      = 2
db_memory   = 4096
db_disk     = "40"
```

## 🔧 Operaciones

### Acceder a LXCs

```bash
# SSH a IDE
ssh root@<ide-ip>

# O desde Proxmox
pct enter 10  # IDE
pct enter 20  # Runtime Worker 1
pct enter 30  # Database
```

### Ver Status

```bash
# Desde Proxmox
pvesh get /nodes/pve/lxc

# O con Terraform
terraform show
```

### Acceder a Langflow

```bash
# Port-forward (si no hay proxy reverso)
ssh -L 7860:localhost:7860 root@<ide-ip>
# Abrir: http://localhost:7860

# O acceso directo
http://<ide-ip>:7860
```

### Escalar Workers

```hcl
# terraform.tfvars
runtime_workers = 4  # Aumentar de 2 a 4
```

```bash
terraform apply
```

### Actualizar Langflow

```hcl
# terraform.tfvars
langflow_version = "1.1.0"
```

```bash
terraform apply
```

## 📊 Monitoring

### Si observability está habilitado

**Prometheus:**
```
http://<monitoring-ip>:9090
```

**Grafana:**
```
http://<monitoring-ip>:3000
```

**Métricas disponibles:**
- CPU/Memory usage por LXC
- Database connections
- Queue length (broker)
- Request rate Langflow

## 💾 Backup

### Backup de LXCs

```bash
# Backup manual de un LXC
vzdump 10 --dumpdir /var/lib/vz/dump --mode snapshot

# Backup de database
pct exec 30 -- pg_dump langflow > backup.sql
```

### Snapshot de LXC

```bash
# Crear snapshot
pct snapshot 10 pre-upgrade

# Restaurar snapshot
pct rollback 10 pre-upgrade
```

## 🔒 Seguridad

### Firewall en LXCs

```bash
# En cada LXC, habilitar UFW
ufw allow from <proxmox-network> to any port 7860  # IDE
ufw allow from <proxmox-network> to any port 5432  # PostgreSQL
ufw enable
```

### Secrets

Credenciales se generan automáticamente y se almacenan:
```bash
# Ver credenciales en outputs
terraform output database_password
terraform output grafana_password
```

## 🐛 Troubleshooting

### LXC no inicia

```bash
# Ver logs
pct console 10

# Ver status
pct status 10

# Restart
pct restart 10
```

### Database connection issues

```bash
# Verificar que PostgreSQL esté corriendo
pct exec 30 -- systemctl status postgresql

# Test connection
pct exec 30 -- psql -U langflow -d langflow -c "SELECT 1;"
```

### Check Message Broker

```bash
# Redis
pct exec 40 -- redis-cli ping

# RabbitMQ
pct exec 40 -- rabbitmqctl status
```

## 💰 Costos y Recursos

### Configuración Mínima (Dev)

```hcl
runtime_workers      = 1
enable_observability = false
database_type        = "postgresql"
broker_type          = "redis"
```

**Total:** ~6 vCPU, ~12GB RAM, ~130GB disco

### Configuración Producción

```hcl
runtime_workers      = 4
enable_observability = true
```

**Total:** ~14 vCPU, ~28GB RAM, ~230GB disco

## 🌟 Ventajas vs Kubernetes

| Aspecto | LXC | Kubernetes |
|---------|-----|------------|
| **Overhead** | Muy bajo | Alto |
| **Boot time** | 5-10s | 30-60s |
| **RAM usage** | 100MB | 500MB+ |
| **Complejidad** | Baja | Alta |
| **Escalabilidad** | Manual | Automática |
| **Multi-tenancy** | Limitado | Excelente |
| **Ideal para** | On-prem, edge | Cloud, multi-app |

## 🔗 Referencias

- [Proxmox LXC](https://pve.proxmox.com/wiki/Linux_Container)
- [Terraform Proxmox Provider](https://registry.terraform.io/providers/Telmate/proxmox/latest/docs)
- [Langflow Documentation](https://docs.langflow.org)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
