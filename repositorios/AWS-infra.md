# Documentación: intaky-dev/AWS-infra

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/AWS-infra`
**Tipo:** Script de Instalación
**Tecnología:** Bash Shell Script
**Propósito:** Instalación automatizada de herramientas AWS y Kubernetes
**URL:** https://github.com/intaky-dev/AWS-infra

## 🎯 Descripción

Script bash que automatiza la instalación de herramientas esenciales para trabajar con AWS EKS y Kubernetes. Instala y configura AWS CLI, eksctl, kubectl, Docker, Helm, Terraform y otras dependencias necesarias para desarrollo de infraestructura cloud.

**Ideal para:**
- Setup de ambiente de desarrollo AWS
- Configuración de workstations nuevas
- CI/CD runners
- Servidores jump/bastion
- Ambientes de training/labs

## 📁 Estructura del Repositorio

```
AWS-infra/
└── start.sh    # Script de instalación completo
```

## 🛠️ Herramientas Instaladas

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| **AWS CLI v2** | Latest | Cliente de línea de comandos AWS |
| **eksctl** | Latest | Creación y gestión de clusters EKS |
| **kubectl** | Latest | Cliente Kubernetes |
| **Docker** | Latest (snap) | Containerización |
| **Helm** | Latest | Package manager K8s |
| **aws-iam-authenticator** | Latest | Autenticación IAM para EKS |
| **Terraform** | Latest | Infrastructure as Code |

### Dependencias del Sistema

- `unzip` - Descompresión de archivos
- `curl` - Descarga de archivos
- `gnupg` - Verificación de firmas
- `software-properties-common` - Gestión de repositorios
- `lsb-release` - Información del sistema
- `ca-certificates` - Certificados SSL

## 🚀 Uso

### Instalación Rápida

```bash
# Clonar repositorio
git clone https://github.com/intaky-dev/AWS-infra.git
cd AWS-infra

# Dar permisos de ejecución
chmod +x start.sh

# Ejecutar (requiere sudo)
sudo ./start.sh
```

### Instalación con Logging

```bash
# Ejecutar con log
sudo ./start.sh 2>&1 | tee install.log

# Verificar instalación
cat install.log | grep -E "(successfully|installed|configured)"
```

## 📝 Detalle del Script

### 1. Actualización del Sistema

```bash
# Actualizar apt
apt-get update -y
apt-get upgrade -y

# Instalar dependencias base
apt-get install -y \
    unzip \
    curl \
    gnupg \
    software-properties-common \
    lsb-release \
    ca-certificates
```

### 2. AWS CLI v2

```bash
# Descargar e instalar AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
./aws/install

# Verificar
aws --version
```

**Configurar credenciales:**
```bash
aws configure
# AWS Access Key ID: <tu-key>
# AWS Secret Access Key: <tu-secret>
# Default region: us-east-1
# Default output format: json
```

### 3. eksctl

```bash
# Descargar última versión
curl --silent --location \
    "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" \
    | tar xz -C /tmp

# Mover a /usr/local/bin
mv /tmp/eksctl /usr/local/bin

# Verificar
eksctl version
```

**Uso:**
```bash
# Crear cluster EKS
eksctl create cluster \
    --name my-cluster \
    --region us-east-1 \
    --nodegroup-name standard-workers \
    --node-type t3.medium \
    --nodes 3

# Listar clusters
eksctl get cluster
```

### 4. kubectl

```bash
# Agregar repositorio Kubernetes
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key \
    | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg

echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] \
    https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' \
    | tee /etc/apt/sources.list.d/kubernetes.list

# Instalar kubectl
apt-get update
apt-get install -y kubectl

# Verificar
kubectl version --client
```

**Configurar kubeconfig:**
```bash
# Automático con eksctl
eksctl utils write-kubeconfig --cluster=my-cluster

# Manual
aws eks update-kubeconfig --name my-cluster --region us-east-1
```

### 5. Docker

```bash
# Instalar via snap
snap install docker

# Agregar usuario al grupo docker
usermod -aG docker $USER

# Verificar
docker --version
docker run hello-world
```

**Nota:** Requiere logout/login para aplicar permisos de grupo.

### 6. Helm

```bash
# Descargar script de instalación
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Verificar
helm version
```

**Agregar repos comunes:**
```bash
helm repo add stable https://charts.helm.sh/stable
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### 7. aws-iam-authenticator

```bash
# Descargar binario
curl -Lo aws-iam-authenticator \
    https://github.com/kubernetes-sigs/aws-iam-authenticator/releases/download/v0.6.11/aws-iam-authenticator_0.6.11_linux_amd64

# Dar permisos y mover
chmod +x ./aws-iam-authenticator
mv ./aws-iam-authenticator /usr/local/bin/

# Verificar
aws-iam-authenticator version
```

### 8. Terraform

```bash
# Agregar HashiCorp GPG key
wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    tee /usr/share/keyrings/hashicorp-archive-keyring.gpg

# Agregar repositorio
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/hashicorp.list

# Instalar
apt-get update
apt-get install -y terraform

# Verificar
terraform --version
```

## ✅ Verificación Post-Instalación

### Script de Verificación

```bash
#!/bin/bash
# verify-install.sh

echo "=== Verificando instalaciones ==="

# AWS CLI
if command -v aws &> /dev/null; then
    echo "✓ AWS CLI: $(aws --version)"
else
    echo "✗ AWS CLI: No instalado"
fi

# eksctl
if command -v eksctl &> /dev/null; then
    echo "✓ eksctl: $(eksctl version)"
else
    echo "✗ eksctl: No instalado"
fi

# kubectl
if command -v kubectl &> /dev/null; then
    echo "✓ kubectl: $(kubectl version --client --short)"
else
    echo "✗ kubectl: No instalado"
fi

# Docker
if command -v docker &> /dev/null; then
    echo "✓ Docker: $(docker --version)"
else
    echo "✗ Docker: No instalado"
fi

# Helm
if command -v helm &> /dev/null; then
    echo "✓ Helm: $(helm version --short)"
else
    echo "✗ Helm: No instalado"
fi

# aws-iam-authenticator
if command -v aws-iam-authenticator &> /dev/null; then
    echo "✓ aws-iam-authenticator: Instalado"
else
    echo "✗ aws-iam-authenticator: No instalado"
fi

# Terraform
if command -v terraform &> /dev/null; then
    echo "✓ Terraform: $(terraform version | head -1)"
else
    echo "✗ Terraform: No instalado"
fi
```

## 🔧 Configuración Post-Instalación

### 1. Configurar AWS CLI

```bash
# Método interactivo
aws configure

# O con variables de entorno
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_DEFAULT_REGION="us-east-1"

# Verificar configuración
aws sts get-caller-identity
```

### 2. Configurar kubectl Autocomplete

```bash
# Para bash
echo 'source <(kubectl completion bash)' >> ~/.bashrc
echo 'alias k=kubectl' >> ~/.bashrc
echo 'complete -o default -F __start_kubectl k' >> ~/.bashrc

# Para zsh
echo 'source <(kubectl completion zsh)' >> ~/.zshrc
```

### 3. Configurar Docker sin sudo

```bash
# Agregar usuario actual al grupo docker
sudo usermod -aG docker $USER

# Aplicar cambios (requiere re-login)
newgrp docker

# Verificar
docker run hello-world
```

## 📦 Casos de Uso

### Crear Cluster EKS Completo

```bash
# 1. Crear cluster
eksctl create cluster \
    --name production \
    --version 1.28 \
    --region us-east-1 \
    --nodegroup-name workers \
    --node-type t3.large \
    --nodes 3 \
    --nodes-min 2 \
    --nodes-max 5 \
    --managed

# 2. Configurar kubectl
aws eks update-kubeconfig --name production

# 3. Verificar
kubectl get nodes

# 4. Instalar apps con Helm
helm install nginx-ingress bitnami/nginx-ingress-controller
```

### Desplegar con Terraform

```bash
# 1. Inicializar Terraform
terraform init

# 2. Planear
terraform plan

# 3. Aplicar
terraform apply

# 4. Obtener kubeconfig
terraform output kubeconfig > ~/.kube/config
```

## 🐛 Troubleshooting

### AWS CLI no encuentra credenciales

```bash
# Verificar archivo de credenciales
cat ~/.aws/credentials

# Verificar configuración
aws configure list

# Probar conexión
aws sts get-caller-identity
```

### kubectl no conecta a cluster

```bash
# Verificar kubeconfig
cat ~/.kube/config

# Re-configurar
aws eks update-kubeconfig --name <cluster-name> --region <region>

# Verificar contexto
kubectl config current-context
```

### Docker permission denied

```bash
# Verificar grupo
groups | grep docker

# Si no está, agregar y re-login
sudo usermod -aG docker $USER
newgrp docker
```

## 💡 Mejoras Sugeridas

### Versión Idempotente

```bash
#!/bin/bash
# Verificar antes de instalar

install_if_missing() {
    local cmd=$1
    local install_func=$2

    if ! command -v $cmd &> /dev/null; then
        echo "Instalando $cmd..."
        $install_func
    else
        echo "✓ $cmd ya instalado"
    fi
}

# Uso
install_if_missing "aws" install_aws_cli
install_if_missing "kubectl" install_kubectl
```

### Con Logging

```bash
#!/bin/bash
LOG_FILE="/var/log/aws-infra-install.log"

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

log "Iniciando instalación..."
# ... resto del script
```

## 📊 Requisitos del Sistema

- **OS**: Ubuntu 20.04+ / Debian 11+
- **RAM**: 2GB mínimo
- **Disco**: 10GB libre
- **Permisos**: sudo/root
- **Red**: Acceso a internet

## 🔗 Referencias

- [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
- [eksctl Documentation](https://eksctl.io/)
- [kubectl Documentation](https://kubernetes.io/docs/reference/kubectl/)
- [Helm Documentation](https://helm.sh/docs/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
