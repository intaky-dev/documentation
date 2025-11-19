# Documentación: intaky-dev/AWS-EKS-

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/AWS-EKS-`
**Tipo:** Infraestructura como Código (IaC)
**Tecnología:** Terraform, AWS, HCL
**Propósito:** Provisión de cluster AWS EKS con módulos
**URL:** https://github.com/intaky-dev/AWS-EKS-

## 🎯 Descripción

Módulos de Terraform para crear infraestructura AWS EKS completa incluyendo VPC, subnets públicas y privadas, security groups, y cluster EKS con node groups. Similar al repositorio `aws-eks` pero con estructura modular más organizada.

**Componentes:**
- VPC personalizada
- Subnets públicas y privadas en múltiples AZs
- Internet Gateway y Route Tables
- Security Groups específicos para EKS
- Cluster EKS

## 📁 Estructura del Repositorio

```
AWS-EKS-/
├── main.tf                  # Configuración principal (VPC, Subnets, IGW)
├── variables.tf             # Variables de entrada
├── output.tf                # Outputs del módulo
├── README.md                # Documentación (solo título)
└── modules/
    ├── eks/                 # Módulo EKS
    │   ├── eks.tf          # Configuración del cluster
    │   ├── variables.tf    # Variables del módulo
    │   └── output.tf       # Outputs del módulo
    └── sg_eks/              # Módulo Security Groups
        ├── sg.tf           # Security groups para EKS
        ├── variables.tf    # Variables del módulo
        └── output.tf       # Outputs del módulo
```

## 🏗️ Arquitectura

### Componentes de Red

#### VPC
- CIDR configurable
- DNS hostnames habilitados
- DNS support habilitado

#### Subnets
- **2 Subnets Públicas** (diferentes AZs)
  - Auto-assign public IP habilitado
  - Para Load Balancers y NAT Gateways

- **2 Subnets Privadas** (diferentes AZs)
  - Para EKS worker nodes
  - Acceso a internet via NAT Gateway

#### Internet Gateway
- Conectado a VPC
- Ruta 0.0.0.0/0 para tráfico de salida

#### Route Tables
- Route table para subnets públicas
- Asociaciones a todas las subnets

### Módulos

#### Módulo sg_eks
**Propósito:** Security Groups para cluster EKS

**Recursos:**
- Security group para control plane
- Security group para worker nodes
- Reglas de ingress/egress

**Variables:**
```hcl
variable "vpc_id" {
  description = "ID del VPC"
  type        = string
}
```

**Outputs:**
```hcl
output "security_group_public" {
  description = "ID del security group público"
  value       = aws_security_group.public.id
}
```

#### Módulo eks
**Propósito:** Cluster EKS y node groups

**Recursos:**
- EKS Cluster
- IAM roles para cluster
- IAM roles para workers
- Node groups
- Policies necesarias

**Variables:**
```hcl
variable "vpc_id" {
  description = "ID del VPC"
  type        = string
}

variable "subnet_ids" {
  description = "Lista de subnet IDs"
  type        = list(string)
}

variable "sg_ids" {
  description = "Security group IDs"
  type        = string
}
```

## ⚙️ Variables Principales

```hcl
# main.tf variables

variable "location" {
  description = "AWS Region"
  type        = string
  default     = "us-east-1"
}

variable "vpc-cidr" {
  description = "CIDR block para VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet1-cidr" {
  description = "CIDR para subnet pública 1"
  type        = string
  default     = "10.0.1.0/24"
}

variable "public_subnet2-cidr" {
  description = "CIDR para subnet pública 2"
  type        = string
  default     = "10.0.2.0/24"
}

variable "private_subnet1-cidr" {
  description = "CIDR para subnet privada 1"
  type        = string
  default     = "10.0.3.0/24"
}

variable "private_subnet2-cidr" {
  description = "CIDR para subnet privada 2"
  type        = string
  default     = "10.0.4.0/24"
}

variable "subnet_az-1" {
  description = "Availability Zone 1"
  type        = string
  default     = "us-east-1a"
}

variable "subnet_az-2" {
  description = "Availability Zone 2"
  type        = string
  default     = "us-east-1b"
}
```

## 🚀 Uso

### Despliegue Básico

```bash
# 1. Clonar repositorio
git clone https://github.com/intaky-dev/AWS-EKS-.git
cd AWS-EKS-

# 2. Crear terraform.tfvars
cat > terraform.tfvars <<EOF
location = "us-east-1"
vpc-cidr = "10.0.0.0/16"
public_subnet1-cidr = "10.0.1.0/24"
public_subnet2-cidr = "10.0.2.0/24"
private_subnet1-cidr = "10.0.3.0/24"
private_subnet2-cidr = "10.0.4.0/24"
subnet_az-1 = "us-east-1a"
subnet_az-2 = "us-east-1b"
EOF

# 3. Inicializar Terraform
terraform init

# 4. Planear
terraform plan

# 5. Aplicar
terraform apply

# 6. Configurar kubectl
aws eks update-kubeconfig --name <cluster-name> --region us-east-1
```

### Verificación

```bash
# Verificar VPC
aws ec2 describe-vpcs --filters "Name=tag:Name,Values=demo-vpc"

# Verificar Subnets
aws ec2 describe-subnets --filters "Name=vpc-id,Values=<vpc-id>"

# Verificar cluster EKS
aws eks describe-cluster --name <cluster-name>

# Verificar nodos
kubectl get nodes
```

## 📊 Recursos Creados

| Recurso | Cantidad | Descripción |
|---------|----------|-------------|
| VPC | 1 | Red virtual aislada |
| Subnets Públicas | 2 | En diferentes AZs |
| Subnets Privadas | 2 | En diferentes AZs |
| Internet Gateway | 1 | Acceso a internet |
| Route Tables | 1 | Tabla de ruteo |
| Route Table Associations | 4 | 2 públicas + 2 privadas |
| Security Groups | 2+ | Para cluster y workers |
| EKS Cluster | 1 | Kubernetes control plane |
| Node Groups | 1+ | Worker nodes |

## 🔒 Seguridad

### Security Groups

El módulo `sg_eks` crea security groups con reglas apropiadas:

**Control Plane SG:**
- Ingress: API Server (443) desde workers
- Egress: Todo el tráfico

**Worker Nodes SG:**
- Ingress: Desde control plane
- Ingress: Entre workers (all ports)
- Egress: Todo el tráfico

### IAM Roles

**Cluster Role:**
- AmazonEKSClusterPolicy
- AmazonEKSServicePolicy
- AmazonEKSVPCResourceController

**Worker Role:**
- AmazonEKSWorkerNodePolicy
- AmazonEKS_CNI_Policy
- AmazonEC2ContainerRegistryReadOnly

## 💰 Costos Estimados

**Control Plane:** ~$0.10/hora (~$73/mes)

**Worker Nodes (ejemplo t3.medium x2):**
- Instancias: ~$0.042/hora cada (~$61/mes cada)
- Total workers: ~$122/mes

**Otros:**
- NAT Gateway: ~$0.045/hora (~$32/mes)
- Data transfer: Variable

**Total estimado:** ~$227/mes (configuración mínima)

## 🔧 Customización

### Agregar NAT Gateway

```hcl
# En main.tf, agregar:

resource "aws_eip" "nat" {
  domain = "vpc"
}

resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_subnet-1.id

  tags = {
    Name = "demo-nat"
  }
}

# Crear route table para subnets privadas
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.demo-vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "private-rt"
  }
}
```

### Múltiples Node Groups

En módulo `eks`, agregar:

```hcl
resource "aws_eks_node_group" "spot" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "spot-workers"
  node_role_arn   = aws_iam_role.worker.arn
  subnet_ids      = var.subnet_ids

  capacity_type = "SPOT"
  instance_types = ["t3.medium", "t3a.medium"]

  scaling_config {
    desired_size = 2
    max_size     = 10
    min_size     = 1
  }
}
```

## 🐛 Troubleshooting

### VPC ya existe

```bash
# Destruir recursos existentes
terraform destroy

# O importar VPC existente
terraform import aws_vpc.demo-vpc <vpc-id>
```

### Subnets en misma AZ

Verificar que `subnet_az-1` y `subnet_az-2` sean diferentes:
```hcl
subnet_az-1 = "us-east-1a"
subnet_az-2 = "us-east-1b"  # Diferente!
```

### Error de permisos IAM

Verificar que el usuario AWS tenga permisos:
```bash
aws iam get-user
aws sts get-caller-identity
```

## 📝 Mejoras Sugeridas

1. **Agregar NAT Gateway** para subnets privadas
2. **Separar route tables** (público/privado)
3. **VPC Endpoints** para servicios AWS (S3, ECR)
4. **Flow Logs** para debugging de red
5. **Tags consistentes** para todos los recursos
6. **Variables para node group** (tipo instancia, replicas)
7. **README completo** con ejemplos

## 🔄 Diferencias vs aws-eks

| Aspecto | AWS-EKS- | aws-eks |
|---------|----------|---------|
| **Estructura** | Modular | Monolítico |
| **SG Module** | ✅ Sí | ❌ Inline |
| **EKS Module** | ✅ Sí | ❌ Inline |
| **README** | ⚠️ Incompleto | ✅ Básico |
| **Organización** | ✅ Mejor | ⚠️ Puede mejorar |

## 🔗 Referencias

- [Amazon EKS](https://docs.aws.amazon.com/eks/)
- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [EKS Best Practices](https://aws.github.io/aws-eks-best-practices/)
- [VPC Design](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
