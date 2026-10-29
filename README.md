# Arquitectura de Apuntado

Repositorio académico independiente de Juan José Alzate Rojas para Fundamentos de Arquitectura de Software, Universidad Nacional de Colombia.

URL: https://github.com/AlzateJJ/apuntado-arquitectura

El sistema ofrece partida única y Apuntado de rondas acumulativas. Se propone un frontend con despliegue independiente y un backend organizado como monolito modular con persistencia PostgreSQL. Los componentes del backend se despliegan juntos.

Este repositorio se inicia desde cero, con historial propio. Reúne los artefactos académicos; no incluye el código del backend anterior. Las versiones se integran de forma incremental y se documentan en `docs/EVOLUCION.md`.

## Versión 3 — cierre de ronda comprobable

Se implementan contratos, reglas de ambas modalidades, coordinación del cierre, adaptadores de persistencia, proyección de privacidad y notificación posterior al commit en `design/src/`.

Con Node.js 24, ejecutar:

```sh
npm ci --ignore-scripts
npm run verify
```

La verificación actual comprueba tipos, 16 pruebas de dominio/aplicación y una prueba de esquema SQL. `npm run test:postgres` requiere `ARCH_TEST_DATABASE_URL` apuntando a una base efímera, vacía y exclusiva; se añadirá un servicio automático de PostgreSQL en la siguiente versión.

Los módulos completos de sala, reparto, robo, descarte, autenticación, WebSocket y pantallas siguen pendientes de integración. La siguiente versión incorpora las reglas de gobernanza y el Risk Storming individual.
