# Documentación: intaky-dev/k8s

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/k8s`
**Tipo:** Infraestructura como Código (IaC)
**Tecnología:** Terraform + K3s + Kubernetes
**Propósito:** Instalación automatizada de cluster K3s con Jenkins y Langflow
**Lenguaje:** HCL, Shell, Makefile
**URL:** https://github.com/intaky-dev/k8s

## 🎯 Descripción

Módulo de Terraform que instala y configura un cluster de Kubernetes usando **K3s** en servidores Ubuntu. K3s es una distribución certificada de Kubernetes, ligera y fácil de mantener, perfecta para deployments en servidores locales o edge computing.

Este repositorio incluye soporte completo para:
- **Langflow**: Plataforma de desarrollo de workflows con IA
- **Jenkins CI/CD**: Sistema completo de integración y deployment continuo

## ¿Qué es K3s?

K3s es una distribución de Kubernetes:
- **Ligera**: ~100MB binario
- **Rápida**: Instalación en segundos
- **Certificada**: 100% Kubernetes compatible
- **Production-ready**: Usado por miles de empresas
- **Incluye todo**: Ingress, storage, métricas

## 🏗️ Arquitectura

### Componentes del Cluster

1. **K3s Server** (Control Plane + Worker)
   - API Server en puerto 6443
   - etcd embebido
   - Traefik deshabilitado (para usar nginx-ingress)

2. **Storage**
   - Local Path Provisioner (storage class por defecto)
   - Soporte para PersistentVolumes locales
   - Configuración automática de storage class

3. **Metrics**
   - Metrics Server instalado automáticamente
   - kubectl top nodes/pods disponible

4. **Aplicaciones Pre-configuradas**
   - Jenkins CI/CD con agentes dinámicos
   - Soporte para Langflow

## 📁 Estructura del Repositorio

```
k8s/
├── main.tf                        # Configuración principal de K3s
├── variables.tf                   # Variables de entrada
├── outputs.tf                     # Outputs (kubeconfig path, etc.)
├── jenkins.tf                     # Configuración de Jenkins
├── locals.tf                      # Variables locales
├── terraform.tfvars.example       # Ejemplo de configuración
├── terraform.tfvars.server        # Configuración para servidor
├── Makefile                       # Comandos útiles (130+ líneas)
├── README.md                      # Documentación completa (430+ líneas)
├── QUICKSTART.md                  # Guía de inicio rápido
├── JENKINS.md                     # Documentación detallada de Jenkins
├── check-prerequisites.sh         # Script de verificación
├── quick-start.sh                 # Instalación rápida
├── deploy-jenkins.sh              # Despliegue interactivo de Jenkins
├── deploy-langflow.sh             # Despliegue interactivo de Langflow
├── expose-jenkins-nodeport.sh     # Exponer Jenkins
├── setup-helm-repos.sh            # Configurar repositorios Helm
├── setup-minikube.sh              # Alternativa con Minikube
├── lib/                           # Funciones de utilidad
└── templates/
    └── kubeconfig.tpl             # Template de kubeconfig
```

## 🚀 Instalación Rápida

### Método 1: Quick Start Script

```bash
# 1. Verificar prerrequisitos
./check-prerequisites.sh

# 2. Instalar k3s
./quick-start.sh

# 3. Configurar kubectl
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```

### Método 2: Terraform

```bash
# 1. Configurar variables
cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars

# 2. Inicializar Terraform
terraform init

# 3. Revisar plan
terraform plan

# 4. Aplicar (instalar k3s)
terraform apply

# 5. Configurar kubectl
export KUBECONFIG=$(pwd)/kubeconfig
kubectl get nodes
```

### Método 3: Makefile

```bash
# Instalar k3s
make setup

# Configurar kubectl
eval $(make kubeconfig)

# Ver estado
make status
```

## ⚙️ Variables de Configuración

| Variable | Descripción | Default | Ejemplo |
|----------|-------------|---------|---------|
| `k3s_version` | Versión de k3s | `""` (latest) | `"v1.28.5+k3s1"` |
| `k3s_install_options` | Opciones de instalación | `"server --disable traefik"` | Ver abajo |
| `server_ip` | IP del servidor | `"127.0.0.1"` | `"192.168.1.100"` |
| `server_port` | Puerto API server | `6443` | `6443` |
| `setup_local_storage` | Configurar storage local | `true` | `true/false` |
| `install_metrics_server` | Instalar metrics-server | `true` | `true/false` |
| `jenkins_enabled` | Habilitar Jenkins | `false` | `true/false` |

### Opciones de K3s

```hcl
# Configuración básica (recomendada)
k3s_install_options = "server --disable traefik"

# Configuración avanzada
k3s_install_options = "server --disable traefik --write-kubeconfig-mode 644 --cluster-cidr 10.42.0.0/16"

# Sin desactivar nada
k3s_install_options = "server"
```

**Opciones útiles**:
- `--disable traefik`: Desactiva Traefik (para usar nginx-ingress)
- `--disable servicelb`: Desactiva service load balancer (para MetalLB)
- `--write-kubeconfig-mode 644`: Kubeconfig legible por todos
- `--cluster-cidr`: CIDR personalizado para pods
- `--service-cidr`: CIDR personalizado para servicios

## 🎯 Despliegue de Aplicaciones

### Jenkins CI/CD

#### Método Interactivo
```bash
./deploy-jenkins.sh
```

#### Con Makefile
```bash
# Desplegar
make jenkins-deploy

# Ver estado
make jenkins-status

# Obtener password
make jenkins-password

# Acceder
kubectl port-forward -n jenkins svc/jenkins 8080:8080
# Abrir: http://localhost:8080
```

#### Con Terraform
```bash
cat >> terraform.tfvars <<EOF
jenkins_enabled = true
EOF
terraform apply
```

**Características de Jenkins:**
- ✅ Agentes Kubernetes dinámicos
- ✅ Docker-in-Docker para builds
- ✅ Plugins pre-instalados (Git, Docker, Pipeline, Blue Ocean)
- ✅ Integración con GitHub/GitLab/Bitbucket
- ✅ 20Gi almacenamiento persistente
- ✅ Métricas Prometheus
- ✅ Configuration as Code (JCasC)

Ver [JENKINS.md](https://github.com/intaky-dev/k8s/blob/main/JENKINS.md) para documentación completa.

### Langflow (Plataforma de Workflows IA)

```bash
# 1. Obtener ruta del kubeconfig
export K3S_KUBECONFIG=$(terraform output -raw kubeconfig_path)

# 2. Ir al directorio de langflow-infra
cd ../langflow-infra

# 3. Configurar
cat > terraform.tfvars <<EOF
kubeconfig_path = "$K3S_KUBECONFIG"
namespace       = "langflow"
environment     = "prod"

# Configuración reducida para servidor local
postgres_replicas    = 1
rabbitmq_replicas    = 1
vector_db_replicas   = 1
ide_replicas         = 1
runtime_min_replicas = 1
runtime_max_replicas = 5

enable_observability = false
ingress_enabled      = true
ide_ingress_host     = "langflow.local"
tls_enabled          = false
EOF

# 4. Desplegar
terraform init
terraform apply

# 5. Acceder
kubectl port-forward -n langflow svc/langflow-ide 7860:7860
# Abrir: http://localhost:7860
```

## 🔧 Operaciones Comunes

### Ver Información del Cluster

```bash
# Información general
kubectl cluster-info

# Recursos del sistema
kubectl top nodes
kubectl top pods -A

# Logs de k3s
sudo journalctl -u k3s -f
```

### Backup del Cluster

```bash
# Backup de etcd
sudo k3s etcd-snapshot save --name backup-$(date +%Y%m%d-%H%M%S)

# Los backups se guardan en:
# /var/lib/rancher/k3s/server/db/snapshots/

# Usando Makefile
make backup
```

### Restaurar Backup

```bash
# Detener k3s
sudo systemctl stop k3s

# Restaurar snapshot
sudo k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=/var/lib/rancher/k3s/server/db/snapshots/backup-20240101-120000

# Iniciar k3s
sudo systemctl start k3s
```

### Actualizar K3s

```bash
# Opción 1: Via Terraform
vim terraform.tfvars
# k3s_version = "v1.29.0+k3s1"
terraform apply

# Opción 2: Manual
curl -sfL https://get.k3s.io | \
  INSTALL_K3S_VERSION="v1.29.0+k3s1" sh -
```

### Agregar Nodos Worker

```bash
# En el servidor master, obtener el token
sudo cat /var/lib/rancher/k3s/server/node-token

# En el worker node
curl -sfL https://get.k3s.io | \
  K3S_URL=https://IP_MASTER:6443 \
  K3S_TOKEN=TOKEN sh -
```

## 📊 Comandos Makefile

```bash
# Setup y Gestión
make setup              # Instalar k3s
make status             # Ver estado del cluster
make backup             # Crear backup de etcd
make destroy            # Destruir cluster

# Jenkins
make jenkins-deploy     # Desplegar Jenkins
make jenkins-status     # Ver estado de Jenkins
make jenkins-password   # Obtener password de admin
make jenkins-logs       # Ver logs de Jenkins
make jenkins-destroy    # Eliminar Jenkins

# Utilidades
make kubeconfig         # Mostrar comando para configurar kubectl
make help               # Ver todos los comandos disponibles
```

## 🐛 Troubleshooting

### K3s no inicia
```bash
# Ver logs
sudo journalctl -u k3s -n 100 --no-pager

# Verificar estado
sudo systemctl status k3s

# Reiniciar
sudo systemctl restart k3s
```

### kubectl no funciona
```bash
# Verificar kubeconfig
export KUBECONFIG=$(pwd)/kubeconfig
cat $KUBECONFIG

# Verificar que k3s está corriendo
sudo systemctl status k3s

# Re-generar kubeconfig
sudo cp /etc/rancher/k3s/k3s.yaml ./kubeconfig
sudo chown $USER:$USER ./kubeconfig
```

### Pods en estado Pending
```bash
# Verificar recursos
kubectl describe node

# Verificar eventos
kubectl get events -A --sort-by='.lastTimestamp'

# Verificar storage
kubectl get pv
kubectl get pvc -A
```

### Problemas de Storage
```bash
# Verificar storage class
kubectl get storageclass

# Ver persistent volumes
kubectl get pv

# Hacer local-path default
kubectl patch storageclass local-path \
  -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
```

## 💻 Requisitos del Sistema

### Configuración Mínima (Dev/Test)
- Ubuntu 20.04+
- 2GB RAM
- 2 CPU cores
- 20GB disco

### Configuración Recomendada (Producción)
- Ubuntu 20.04+
- 8GB RAM
- 4 CPU cores
- 100GB disco SSD

### Con Langflow Completo
- Ubuntu 22.04
- 16GB RAM
- 8 CPU cores
- 200GB disco SSD

## 🔒 Acceso Remoto

Para acceder al cluster desde otra máquina:

1. Cambiar `server_ip` a la IP real:
```hcl
server_ip = "192.168.1.100"
```

2. Permitir el puerto en firewall:
```bash
sudo ufw allow 6443/tcp
```

3. Copiar kubeconfig a máquina remota:
```bash
scp usuario@servidor:~/k8s/kubeconfig ~/.kube/config-k3s
export KUBECONFIG=~/.kube/config-k3s
kubectl get nodes
```

## 🗑️ Desinstalación

### Solo destruir Langflow
```bash
cd ~/langflow-infra
terraform destroy
```

### Destruir K3s completo
```bash
cd ~/k8s
terraform destroy
# O usando Makefile
make destroy
```

Esto ejecuta `/usr/local/bin/k3s-uninstall.sh` que:
- Detiene todos los servicios
- Elimina todos los containers
- Limpia iptables rules
- Elimina archivos de configuración
- Preserva logs en `/var/log/`

## 🌟 Características Destacadas

1. **Instalación en 3 comandos**: Quick start script
2. **Makefile completo**: 20+ comandos útiles
3. **Jenkins pre-configurado**: Con plugins y agentes K8s
4. **Métricas incluidas**: kubectl top funcionando
5. **Storage automático**: Local path provisioner
6. **Backup/Restore**: Scripts de backup de etcd
7. **Multi-plataforma**: Ubuntu, Debian, RHEL compatible
8. **Production-ready**: Usado en producción

## 📚 Documentación Adicional

- **README.md**: Documentación completa (430+ líneas)
- **QUICKSTART.md**: Guía de inicio rápido
- **JENKINS.md**: Documentación detallada de Jenkins

## 🔗 Referencias

- [K3s Documentation](https://docs.k3s.io/)
- [K3s GitHub](https://github.com/k3s-io/k3s)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Jenkins on Kubernetes](https://www.jenkins.io/doc/book/installing/kubernetes/)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
