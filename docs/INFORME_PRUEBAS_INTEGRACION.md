# Informe de Pruebas de Integración - Blacklist API

**Repositorio del proyecto:** [https://github.com/Emiro-Mendez/blacklist-app](https://github.com/Emiro-Mendez/blacklist-app)[cite: 3]

---

## 1. Resumen Ejecutivo
Este informe documenta la implementación, ejecución e integración continua de las pruebas de integración para el microservicio **Blacklist API**. Se validaron las capacidades principales del servicio mediante **Postman** y **Newman**[cite: 1, 2], automatizando el proceso dentro del pipeline de **GitHub Actions**[cite: 1, 2].

---

## 2. Definición de la Colección de Pruebas (Postman)

Se diseñó la colección `blacklist-api.postman_collection.json` con los siguientes endpoints[cite: 1]:

1. **GET `/blacklists/ping`**[cite: 1]
   * **Propósito:** Healthcheck básico del servicio[cite: 1].
   * **Validación:** Garantizar respuesta `200 OK` y cuerpo con `{"message": "pong"}`[cite: 1].

2. **GET `/health`**[cite: 1]
   * **Propósito:** Confirmar el estado general operativo del microservicio[cite: 1].
   * **Validación:** Respuesta `200 OK` y estado `"healthy"`[cite: 1].

3. **POST `/blacklists`**[cite: 1]
   * **Propósito:** Registrar un correo electrónico en la lista negra global[cite: 1].
   * **Headers:** `Authorization: Bearer dev-token-12345`, `Content-Type: application/json`[cite: 1].
   * **Pre-request Script:** Generación dinámica de email con timestamp (`test${Date.now()}@example.com`) para evitar el error `409 CONFLICT` por duplicados[cite: 1].
   * **Validación:** Estado `201 CREATED` y coincidencia del email en la respuesta[cite: 1].

4. **GET `/blacklists/{email}`**[cite: 1]
   * **Propósito:** Consultar si un email específico existe en la lista negra[cite: 1].
   * **Headers:** `Authorization: Bearer dev-token-12345`[cite: 1].
   * **Validación:** Estado `200 OK` y propiedad `is_blacklisted: true`[cite: 1].

---

## 3. Ejecución Local con Newman

Las pruebas se ejecutaron sobre los contenedores desplegados con Docker Compose mediante el comando[cite: 1]:

```bash
newman run blacklist-api.postman_collection.json \
  --env-var baseUrl=http://localhost:5001 \
  --env-var token=dev-token-12345
```[cite: 1]

### Resultados Obtenidos:
* **Total de iteraciones:** 1[cite: 1]
* **Peticiones ejecutadas:** 4 / 4[cite: 1]
* **Aserciones exitosas:** 7 / 7[cite: 1]
* **Fallos:** 0[cite: 1]

---

## 4. Integración en GitHub Actions (CI/CD)

Se creó e integró el job `pruebas_integracion` en el pipeline de GitHub Actions (`.github/workflows/tests.yml`)[cite: 1, 2].

### Pasos del Workflow:
1. **Checkout del código**: Obtiene la última versión del repositorio[cite: 1].
2. **Configuración del entorno**: Crea dinámicamente el archivo `.env` necesario para CI[cite: 1].
3. **Despliegue de Servicios**: Inicia los contenedores de la aplicación y PostgreSQL mediante `docker compose up -d --build`[cite: 1].
4. **Espera de Disponibilidad**: Bucle `curl` de verificación hasta obtener respuesta satisfactoria del endpoint de ping[cite: 1].
5. **Ejecución de Pruebas**: Instalación automatizada de Node.js, **Newman** y ejecución de la colección de pruebas[cite: 1, 2].
6. **Limpieza**: Cierre y remoción de servicios mediante `docker compose down`[cite: 1].

---

## 5. Conclusión
La suite de pruebas de integración se integró correctamente al flujo CI/CD[cite: 1]. Esto asegura que cada cambio enviado a la rama principal valide de forma automatizada la interacción entre el microservicio, la base de datos PostgreSQL y las rutas HTTP expuestas.