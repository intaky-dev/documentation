# Documentación: intaky-dev/mssql-docker

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/mssql-docker`
**Tipo:** Dockerfile / Containerización
**Tecnología:** Docker, Microsoft SQL Server 2022, Bash
**Propósito:** Dockerfile para montar y restaurar bases de datos MSSQL
**URL:** https://github.com/intaky-dev/mssql-docker

## 🎯 Descripción

Proporciona un Dockerfile optimizado para crear una imagen Docker de Microsoft SQL Server 2022 con herramientas CLI y automatización para restauración de backups. Simplifica el despliegue de MSSQL en contenedores y facilita procesos de desarrollo y testing.

**Casos de uso:**
- Desarrollo local con MSSQL
- Testing de aplicaciones .NET/SQL
- Restauración rápida de backups
- CI/CD pipelines
- Migración de bases de datos

## 📁 Estructura del Repositorio

```
mssql-docker/
├── Dockerfile                # Imagen Docker SQL Server 2022
├── restore-backup.sh         # Script de restauración
└── README.md                # Instrucciones de uso
```

## 🐳 Dockerfile

### Configuración Base

```dockerfile
FROM mcr.microsoft.com/mssql/server:2022-latest

# Environment Variables
ENV ACCEPT_EULA=Y
ENV SA_PASSWORD=YourStrong!Passw0rd
ENV MSSQL_PID=Express

# Instalar herramientas
RUN apt-get update && apt-get install -y \
    curl \
    apt-transport-https

# MSSQL CLI Tools
RUN curl https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/prod.list \
    > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y \
        msodbcsql17 \
        mssql-tools

# Agregar tools al PATH
ENV PATH="$PATH:/opt/mssql-tools/bin"
```

### Puertos

- **1433**: Puerto por defecto SQL Server

### Volúmenes

- `/var/opt/mssql/data`: Archivos de base de datos
- `/var/opt/mssql/log`: Logs
- `/var/opt/mssql/backup`: Backups

## 🚀 Uso

### Build de Imagen

```bash
# Build
docker build -t mssql:2022 .

# O con tag específico
docker build -t mssql:2022-dev .
```

### Run Container

#### Básico

```bash
docker run -d \
  --name mssql \
  -e "ACCEPT_EULA=Y" \
  -e "SA_PASSWORD=YourStrong!Passw0rd" \
  -p 1433:1433 \
  mssql:2022
```

#### Con Volúmenes

```bash
docker run -d \
  --name mssql \
  -e "ACCEPT_EULA=Y" \
  -e "SA_PASSWORD=YourStrong!Passw0rd" \
  -p 1433:1433 \
  -v /path/to/data:/var/opt/mssql/data \
  -v /path/to/backups:/var/opt/mssql/backup \
  mssql:2022
```

#### Con Docker Compose

```yaml
version: '3.8'

services:
  mssql:
    build: .
    container_name: mssql
    environment:
      ACCEPT_EULA: "Y"
      SA_PASSWORD: "YourStrong!Passw0rd"
      MSSQL_PID: "Express"
    ports:
      - "1433:1433"
    volumes:
      - mssql-data:/var/opt/mssql/data
      - mssql-log:/var/opt/mssql/log
      - ./backups:/var/opt/mssql/backup

volumes:
  mssql-data:
  mssql-log:
```

## 🔧 Operaciones

### Conectar a SQL Server

```bash
# Desde container
docker exec -it mssql /opt/mssql-tools/bin/sqlcmd \
  -S localhost \
  -U SA \
  -P 'YourStrong!Passw0rd'

# Desde host (con sqlcmd instalado)
sqlcmd -S localhost,1433 -U SA -P 'YourStrong!Passw0rd'
```

### Crear Base de Datos

```sql
CREATE DATABASE TestDB;
GO

USE TestDB;
GO

CREATE TABLE Users (
    Id INT PRIMARY KEY IDENTITY,
    Name NVARCHAR(100),
    Email NVARCHAR(100)
);
GO
```

### Backup de Base de Datos

```bash
# Desde SQL
docker exec -it mssql /opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'YourStrong!Passw0rd' -Q "BACKUP DATABASE [TestDB] TO DISK='/var/opt/mssql/backup/TestDB.bak' WITH FORMAT"

# Copiar backup al host
docker cp mssql:/var/opt/mssql/backup/TestDB.bak ./backups/
```

### Restaurar Backup

#### Método 1: Script Incluido

```bash
# Copiar backup al container
docker cp ./backup.bak mssql:/var/opt/mssql/backup/

# Ejecutar script de restauración
docker exec -it mssql bash /restore-backup.sh MyDatabase backup.bak
```

#### Método 2: Manual

```bash
# 1. Ver archivos lógicos del backup
docker exec -it mssql /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong!Passw0rd' \
  -Q "RESTORE FILELISTONLY FROM DISK='/var/opt/mssql/backup/TestDB.bak'"

# 2. Restaurar
docker exec -it mssql /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong!Passw0rd' \
  -Q "RESTORE DATABASE [TestDB] FROM DISK='/var/opt/mssql/backup/TestDB.bak' WITH REPLACE, MOVE 'TestDB' TO '/var/opt/mssql/data/TestDB.mdf', MOVE 'TestDB_log' TO '/var/opt/mssql/log/TestDB_log.ldf'"
```

## 📝 Script restore-backup.sh

```bash
#!/bin/bash
# Restauración automatizada de backup MSSQL

DATABASE_NAME=$1
BACKUP_FILE=$2

if [ -z "$DATABASE_NAME" ] || [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <database_name> <backup_file>"
    exit 1
fi

BACKUP_PATH="/var/opt/mssql/backup/$BACKUP_FILE"

# Obtener nombres lógicos
LOGICAL_NAMES=$(sqlcmd -S localhost -U SA -P "$SA_PASSWORD" \
    -Q "RESTORE FILELISTONLY FROM DISK='$BACKUP_PATH'" -h -1 -W | \
    awk 'NR>2 {print $1}')

DATA_FILE=$(echo "$LOGICAL_NAMES" | head -n 1)
LOG_FILE=$(echo "$LOGICAL_NAMES" | tail -n 1)

# Restaurar
sqlcmd -S localhost -U SA -P "$SA_PASSWORD" -Q "
RESTORE DATABASE [$DATABASE_NAME]
FROM DISK='$BACKUP_PATH'
WITH REPLACE,
    MOVE '$DATA_FILE' TO '/var/opt/mssql/data/${DATABASE_NAME}.mdf',
    MOVE '$LOG_FILE' TO '/var/opt/mssql/log/${DATABASE_NAME}_log.ldf'
"

echo "Database $DATABASE_NAME restored successfully!"
```

## 🔒 Seguridad

### Cambiar SA Password

```bash
# Al crear container
docker run -d \
  --name mssql \
  -e "SA_PASSWORD=SuperSecureP@ssw0rd!" \
  -p 1433:1433 \
  mssql:2022

# Después de crear (desde SQL)
ALTER LOGIN SA WITH PASSWORD = 'NewSecureP@ssw0rd!';
GO
```

### Mejores Prácticas

1. **Password Fuerte**: Mínimo 8 caracteres, mayúsculas, minúsculas, números y símbolos
2. **No usar SA**: Crear usuarios específicos con permisos limitados
3. **Firewall**: Restringir acceso al puerto 1433
4. **Volúmenes**: Usar volúmenes para datos persistentes
5. **Secrets**: Usar Docker secrets o variables de entorno seguras

## 🧪 Testing

### Verificar Instalación

```bash
# 1. Container corriendo
docker ps | grep mssql

# 2. SQL Server activo
docker exec mssql /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong!Passw0rd' \
  -Q "SELECT @@VERSION"

# 3. Listar bases de datos
docker exec mssql /opt/mssql-tools/bin/sqlcmd \
  -S localhost -U SA -P 'YourStrong!Passw0rd' \
  -Q "SELECT name FROM sys.databases"
```

## 💡 Casos de Uso Comunes

### CI/CD Pipeline

```yaml
# .github/workflows/test.yml
services:
  mssql:
    image: ghcr.io/intaky-dev/mssql:2022
    env:
      ACCEPT_EULA: Y
      SA_PASSWORD: TestP@ssw0rd!
    ports:
      - 1433:1433
    options: >-
      --health-cmd "/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P 'TestP@ssw0rd!' -Q 'SELECT 1'"
      --health-interval 10s
      --health-timeout 5s
      --health-retries 5
```

### Desarrollo con .NET

```bash
# docker-compose.yml
version: '3.8'

services:
  api:
    build: ./MyApi
    depends_on:
      - mssql
    environment:
      ConnectionStrings__Default: "Server=mssql;Database=MyDb;User Id=SA;Password=DevP@ssw0rd!;TrustServerCertificate=True"

  mssql:
    build: ./mssql-docker
    environment:
      ACCEPT_EULA: "Y"
      SA_PASSWORD: "DevP@ssw0rd!"
```

## 📊 Recursos del Container

### Mínimos

- **CPU**: 2 cores
- **RAM**: 2GB
- **Disco**: 10GB

### Recomendados (Producción)

- **CPU**: 4+ cores
- **RAM**: 4GB+
- **Disco**: SSD, 50GB+

## 🔗 Referencias

- [SQL Server on Docker](https://learn.microsoft.com/en-us/sql/linux/quickstart-install-connect-docker)
- [SQL Server Express](https://learn.microsoft.com/en-us/sql/sql-server/editions-and-components-of-sql-server-2022)
- [MSSQL Tools](https://learn.microsoft.com/en-us/sql/tools/overview-sql-tools)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
