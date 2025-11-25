# Homework: Diseño y Arquitectura de Microservicios para Sistema de Reservación de Habitaciones

## 📋 Descripción General

En este homework vas a diseñar la arquitectura de un sistema de reservación de habitaciones basado en microservicios y a prototipar sus pantallas clave. Usarás **GitHub Copilot** para acelerar la generación de todos los diagramas de arquitectura con **Mermaid** y **Uizard** para crear bocetos responsivos de la interfaz. El entregable final será un único repositorio con un `README.md` que documente toda tu solución.

## 🎯 Objetivos de la Práctica

### 1. 🏗️ Arquitectura (70%)

Generar y refinar con Copilot los siguientes diagramas:

- **a.** Diagrama de arquitectura de software
- **b.** Diagrama UML de componentes
- **c.** Diagrama de secuencia UML del proceso de reserva
- **d.** Diagrama de transición de estados de una Reserva

### 2. 🎨 Prototipado de UI (30%)

Con **Uizard**, diseñar pantallas responsivas para web/móvil (las que permita el plan gratuito):

- Login / Registro
- Búsqueda y listado de habitaciones
- Detalle de habitación + formulario de reserva
- Confirmación de reserva

## 3. 🛠️ Tecnologías Sugeridas

- **Backend:** Python + FastAPI (o Flask)
- **Base de datos:** PostgreSQL, MongoDB o Redis para caché
- **Mensajería:** RabbitMQ, Kafka o AWS SNS/SQS
- **Frontend:** React, Vue o Svelte (solo estructura de carpetas)
- **Infra (opcional):** Docker, Kubernetes, API Gateway

## 📦 Entregable

Un repositorio público que contenga un `README.md` con lo siguiente:

### 📄 El README.md debe incluir:

1. **Introducción:** descripción del sistema y objetivos
2. **Diagrama de arquitectura** en Mermaid
3. **Diagrama UML de componentes**
4. **Diagrama de secuencia**
5. **Diagrama de estado**
6. **Capturas UI** generadas en Uizard
   > 💡 **Tip:** Recuerda que también tiene un agente de IA con el que con solo darle un prompt puedes generar toda la UI del ejercicio. Por ejemplo, [estos diseños](https://app.uizard.io/p/5f80ea55) fueron generados con un prompt en Uizard en el plan gratuito.
7. **Tecnologías y justificación** de elección
