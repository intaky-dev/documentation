# Documentación: intaky-dev/aws-eks

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/aws-eks`
**Tipo:** Infraestructura como Código (IaC)
**Tecnología:** Terraform + AWS
**Propósito:** Cluster AWS EKS
**Lenguaje:** HCL (HashiCorp Configuration Language)
**URL:** https://github.com/intaky-dev/aws-eks

## 🎯 Descripción

Módulo de Terraform para crear y configurar un cluster de Amazon Elastic Kubernetes Service (EKS) en AWS. Incluye toda la infraestructura de red necesaria (VPC, subnets, gateways) y configuración de nodos worker con políticas IAM apropiadas.

## 🏗️ Arquitectura

### Componentes de Red

1. **VPC (Virtual Private Cloud)**
   - CIDR block configurable
   - Internet Gateway
   - Route Tables

2. **Subnets**
   - 2 subnets públicas (en diferentes AZs)
   - 2 subnets privadas (en diferentes AZs)
   - Todas con IPs públicas habilitadas

3. **Routing**
   - Route table con ruta a Internet Gateway
   - Asociaciones para todas las subnets

### Componentes EKS

#### Cluster Master
- **IAM Roles y Policies**:
  - AmazonEKSClusterPolicy
  - AmazonEKSServicePolicy
  - AmazonEKSVPCResourceController

#### Worker Nodes
- **Tipo de instancia**: t2.small
- **Disco**: 20GB
- **Scaling**:
  - Desired: 2 nodos
  - Min: 1 nodo
  - Max: 3 nodos
- **Capacity Type**: ON_DEMAND
- **SSH Access**: Configurado con keypair

- **IAM Policies para Workers**:
  - AmazonEKSWorkerNodePolicy
  - AmazonEKS_CNI_Policy
  - AmazonSSMManagedInstanceCore
  - AmazonEC2ContainerRegistryReadOnly
  - AmazonPrometheusQueryAccess
  - AWSXRayDaemonWriteAccess
  - AmazonS3ReadOnlyAccess
  - Cluster Autoscaler Policy (custom)
  - Amazon EBS CSI Driver Policy (custom)

### Seguridad

- **Security Groups**: Módulo dedicado (`./sg_eks`)
- **SSH Key**: 01-keypair (debe existir en AWS)
- **IAM Instance Profile**: Para workers

## 📁 Estructura del Repositorio

```
aws-eks/
├── main.tf                     # Configuración principal (VPC, Subnets, Routing)
├── variables.tf                # Variables de entrada
├── output.tf                   # Outputs del módulo
├── eks/
│   ├── eks.tf                  # Configuración del cluster EKS y node groups
│   ├── variables.tf            # Variables del módulo EKS
│   └── output.tf               # Outputs del módulo EKS
├── sg_eks/
│   ├── sg.tf                   # Security groups
│   ├── variables.tf            # Variables de security groups
│   └── output.tf               # Outputs de security groups
├── pod-specs/
│   ├── claim.yaml              # PVC example
│   └── storage-class.yaml      # StorageClass example
└── grafana.yaml                # Deployment de Grafana
```

## 🚀 Uso

### Requisitos Previos

- Terraform >= 0.12
- AWS CLI configurado con credenciales
- Keypair SSH "01-keypair" creado en AWS
- Permisos IAM suficientes para crear recursos

### Despliegue

```bash
# 1. Configurar variables
cp terraform.tfvars.example terraform.tfvars
vim terraform.tfvars

# 2. Inicializar Terraform
terraform init

# 3. Ver plan de ejecución
terraform plan

# 4. Aplicar configuración
terraform apply

# 5. Configurar kubectl
aws eks update-kubeconfig --name ed-eks-01 --region <tu-region>

# 6. Verificar cluster
kubectl get nodes
```

### Variables Principales

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `location` | Región de AWS | `us-east-1` |
| `vpc-cidr` | CIDR del VPC | `10.0.0.0/16` |
| `public_subnet1-cidr` | CIDR subnet pública 1 | `10.0.1.0/24` |
| `public_subnet2-cidr` | CIDR subnet pública 2 | `10.0.2.0/24` |
| `private_subnet1-cidr` | CIDR subnet privada 1 | `10.0.3.0/24` |
| `private_subnet2-cidr` | CIDR subnet privada 2 | `10.0.4.0/24` |
| `subnet_az-1` | Availability Zone 1 | `us-east-1a` |
| `subnet_az-2` | Availability Zone 2 | `us-east-1b` |

## 🔧 Características

### Alta Disponibilidad
- Subnets en múltiples AZs
- Node group con auto-scaling
- Health checks automáticos

### Monitoring y Observabilidad
- Integración con Prometheus
- Soporte para AWS X-Ray
- Ejemplo de despliegue de Grafana incluido

### Storage
- EBS CSI Driver habilitado
- Ejemplos de StorageClass y PVC
- Soporte para volúmenes persistentes

### Auto-scaling
- Cluster Autoscaler policy configurada
- Auto Scaling Groups para workers
- Configuración de min/max replicas

## 📦 Recursos de Ejemplo

### Grafana Deployment
El repositorio incluye un archivo `grafana.yaml` con un deployment básico de Grafana:
- Deployment con 1 replica
- Service tipo LoadBalancer
- Puerto 3000

### Storage Examples
- **storage-class.yaml**: StorageClass para AWS EBS
- **claim.yaml**: PersistentVolumeClaim de ejemplo

## 💰 Costos Estimados

**Componentes con costo**:
- EKS Cluster Control Plane: ~$0.10/hora (~$72/mes)
- EC2 t2.small (2 nodos): ~$0.023/hora cada uno (~$34/mes cada uno)
- EBS Volumes: ~$0.10/GB-mes
- Data Transfer: Variable
- Load Balancers: Si se crean

**Total estimado**: ~$140-180/mes (sin contar tráfico y LBs)

## 🔒 Seguridad

- IAM roles con principio de mínimo privilegio
- Security groups configurados
- Subnets privadas para workers sensibles
- SSH access controlado por keypair
- Integration con AWS Systems Manager (SSM)

## 🛠️ Mantenimiento

### Actualizar Kubernetes
```bash
# Ver versión actual
kubectl version

# Actualizar cluster desde AWS Console o CLI
aws eks update-cluster-version --name ed-eks-01 --kubernetes-version 1.28

# Actualizar node group
aws eks update-nodegroup-version --cluster-name ed-eks-01 --nodegroup-name dev
```

### Escalar Nodos
```bash
# Via Terraform
# Editar main.tf o variables, cambiar desired_size, min_size, max_size
terraform apply

# Via AWS CLI
aws eks update-nodegroup-config \
  --cluster-name ed-eks-01 \
  --nodegroup-name dev \
  --scaling-config minSize=1,maxSize=5,desiredSize=3
```

## 🗑️ Destrucción

```bash
# ADVERTENCIA: Esto eliminará todos los recursos
terraform destroy

# Confirmar cuando se solicite
```

**Importante**: Eliminar manualmente cualquier Load Balancer o volúmenes creados por Kubernetes antes de destruir.

## 📝 Notas

- El cluster se llama "ed-eks-01"
- Los workers tienen el label `env=dev`
- Traefik está deshabilitado por defecto
- Se requiere el keypair "01-keypair" existente en AWS
- El node group permite max 1 nodo unavailable durante updates

## 🔗 Referencias

- [Amazon EKS Documentation](https://docs.aws.amazon.com/eks/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
