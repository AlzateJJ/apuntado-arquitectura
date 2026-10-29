# Arquitectura de Apuntado

Repositorio académico independiente de Juan José Alzate Rojas para Fundamentos de Arquitectura de Software, Universidad Nacional de Colombia.

URL: https://github.com/AlzateJJ/apuntado-arquitectura

El sistema ofrece partida única y Apuntado de rondas acumulativas. Se propone un frontend con despliegue independiente y un backend organizado como monolito modular con persistencia PostgreSQL. Los componentes del backend se despliegan juntos.

Este repositorio se inicia desde cero, con historial propio. Reúne los artefactos académicos; no incluye el código del backend anterior. Las versiones se integran de forma incremental y se documentan en `docs/EVOLUCION.md`.

## Versión 2 — diseño y arquitectura de información

Se añaden ADR-03 a ADR-05, UML de componentes, modelos E-R Barker y clases de entidad con tipos y multiplicidades. Las fuentes están en `docs/models/` en formatos drawio y SVG; también hay PDF vectoriales y PNG.

`database/schema.sql` concreta once tablas y una vista de puntaje acumulado. Define PK/FK, perfiles inmutables y restricciones para liquidar rondas de forma consistente. Debe ejecutarse únicamente en una base vacía PostgreSQL 18.

La siguiente versión incorporará el código de apoyo y sus pruebas. En esta versión las verificaciones ejecutables aún no están integradas.
