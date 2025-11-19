# Documentación: intaky-dev/forloop

## 📋 Información General

**Nombre del Repositorio:** `intaky-dev/forloop`
**Tipo:** Script de Utilidad
**Tecnología:** Bash Shell Script
**Propósito:** Procesamiento de texto - Inversión de mayúsculas/minúsculas
**URL:** https://github.com/intaky-dev/forloop

## 🎯 Descripción

Script shell simple que implementa un bucle for para procesar caracteres de texto. Invierte el caso de letras: convierte mayúsculas a minúsculas y viceversa, manteniendo otros caracteres sin cambios.

**Casos de uso:**
- Aprendizaje de bash scripting
- Transformación de texto
- Procesamiento de caracteres
- Ejemplo didáctico de bucles for

## 📁 Estructura del Repositorio

```
forloop/
└── forloop.sh    # Script principal
```

## 🔧 Código del Script

```bash
#!/bin/bash
# forloop.sh - Invierte mayúsculas/minúsculas

# Toma argumento de entrada
input=$1

# Itera sobre cada carácter
for (( i=0; i<${#input}; i++ )); do
    char="${input:$i:1}"

    # Verifica si es mayúscula
    if [[ $char =~ [A-Z] ]]; then
        # Convierte a minúscula
        echo -n "${char,,}"
    # Verifica si es minúscula
    elif [[ $char =~ [a-z] ]]; then
        # Convierte a mayúscula
        echo -n "${char^^}"
    else
        # Mantiene otros caracteres
        echo -n "$char"
    fi
done

echo ""  # Nueva línea al final
```

## 🚀 Uso

### Ejecución Básica

```bash
# Dar permisos de ejecución
chmod +x forloop.sh

# Ejecutar con texto
./forloop.sh "Hola Mundo"
# Output: hOLA mUNDO

./forloop.sh "ABC123xyz"
# Output: abc123XYZ

./forloop.sh "Test-Case_2024"
# Output: tEST-cASE_2024
```

### Ejemplos

| Input | Output | Descripción |
|-------|--------|-------------|
| `"Hello"` | `"hELLO"` | Inversión simple |
| `"ABC123"` | `"abc123"` | Números sin cambio |
| `"Test@Home"` | `"tEST@hOME"` | Símbolos sin cambio |
| `"a B c D"` | `"A b C d"` | Espacios preservados |

## 📖 Explicación del Código

### Bucle For en Bash

```bash
for (( i=0; i<${#input}; i++ )); do
    # ${#input} = longitud del string
    # i++ = incremento
done
```

### Extracción de Caracteres

```bash
char="${input:$i:1}"
# ${variable:posición:longitud}
# Extrae 1 carácter en posición i
```

### Regex Matching

```bash
if [[ $char =~ [A-Z] ]]; then
    # =~ = operador de regex
    # [A-Z] = rango de mayúsculas
```

### Transformación de Caso

```bash
"${char,,}"  # Convierte a minúscula (bash 4.0+)
"${char^^}"  # Convierte a mayúscula (bash 4.0+)
```

## 🔧 Variantes y Mejoras

### Versión con tr

```bash
#!/bin/bash
# Alternativa usando comando tr

input=$1
echo "$input" | tr 'A-Za-z' 'a-zA-Z'
```

### Versión con sed

```bash
#!/bin/bash
# Alternativa usando sed

input=$1
echo "$input" | sed 'y/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ/'
```

### Versión con Manejo de Argumentos

```bash
#!/bin/bash

# Verificar argumentos
if [ $# -eq 0 ]; then
    echo "Uso: $0 <texto>"
    exit 1
fi

input="$1"
output=""

for (( i=0; i<${#input}; i++ )); do
    char="${input:$i:1}"

    if [[ $char =~ [A-Z] ]]; then
        output+="${char,,}"
    elif [[ $char =~ [a-z] ]]; then
        output+="${char^^}"
    else
        output+="$char"
    fi
done

echo "$output"
```

## 🧪 Testing

```bash
# Test básico
./forloop.sh "Test" | grep -q "tEST" && echo "✓ PASS" || echo "✗ FAIL"

# Test con números
./forloop.sh "abc123" | grep -q "ABC123" && echo "✓ PASS" || echo "✗ FAIL"

# Test con símbolos
./forloop.sh "a@b" | grep -q "A@B" && echo "✓ PASS" || echo "✗ FAIL"

# Test vacío
[ -z "$(./forloop.sh '')" ] && echo "✓ PASS" || echo "✗ FAIL"
```

## 💡 Conceptos Didácticos

### 1. Bucle For C-style

```bash
for (( inicialización; condición; incremento )); do
    # código
done
```

### 2. Manipulación de Strings

```bash
${#string}      # Longitud
${string:pos:len}  # Substring
${string,,}     # A minúsculas
${string^^}     # A mayúsculas
```

### 3. Pattern Matching

```bash
[[ $var =~ pattern ]]  # Regex match
[[ $var == pattern ]]  # Glob match
```

## 🔄 Aplicaciones Prácticas

### Toggle Case en Archivos

```bash
#!/bin/bash
# Procesar líneas de archivo

while IFS= read -r line; do
    ./forloop.sh "$line"
done < input.txt > output.txt
```

### Pipeline con Otros Comandos

```bash
# Leer de stdin
echo "Hello World" | xargs ./forloop.sh

# Procesar múltiples argumentos
for word in "Hello" "World" "Test"; do
    ./forloop.sh "$word"
done
```

### Función Bash

```bash
# Agregar a ~/.bashrc
toggle_case() {
    local input="$1"
    local output=""

    for (( i=0; i<${#input}; i++ )); do
        char="${input:$i:1}"
        if [[ $char =~ [A-Z] ]]; then
            output+="${char,,}"
        elif [[ $char =~ [a-z] ]]; then
            output+="${char^^}"
        else
            output+="$char"
        fi
    done

    echo "$output"
}

# Uso: toggle_case "Hello"
```

## 📊 Performance

Para strings grandes, `tr` es más eficiente:

```bash
# Benchmark
time ./forloop.sh "$(head -c 10000 /dev/urandom | base64)"
# ~0.5s

time echo "$(head -c 10000 /dev/urandom | base64)" | tr 'A-Za-z' 'a-zA-Z'
# ~0.01s
```

## 🎓 Valor Educativo

Este script es excelente para aprender:
- ✅ Sintaxis de bucles for en bash
- ✅ Manipulación de strings
- ✅ Regex en bash
- ✅ Case transformation
- ✅ String iteration

## 🔗 Referencias

- [Bash String Manipulation](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html)
- [Bash Loops](https://www.gnu.org/software/bash/manual/html_node/Looping-Constructs.html)
- [Bash Regex](https://www.gnu.org/software/bash/manual/html_node/Conditional-Constructs.html)

---

**Última actualización**: 2025-11-18
**Versión de documentación**: 1.0
