# Evolución del repositorio académico

## Versión 1 — alcance y antecedentes

Se inicia un repositorio académico independiente y se conservan ADR-01, ADR-02 y el antecedente de WebSocket. No se incorpora el directorio del backend antiguo ni su historial Git. La primera versión delimita qué se entregará.

## Versión 2 — diseño y datos

Se concretan el monolito modular del backend, la extensibilidad por estrategias, la persistencia relacional y la comunicación. Se añaden ADR-03 a ADR-05, UML de componentes y entidades, Barker y esquema SQL. Los modelos tienen fuentes editables. Las pruebas se incorporarán en la siguiente versión.

## Versión 3 — código de apoyo y pruebas del cierre

Se incorpora la base TypeScript del cierre de ronda: reglas, contratos, coordinación, persistencia y notificación. Se comprueban tipos, 16 pruebas de dominio/aplicación y una prueba del esquema. Se prepara una prueba de concurrencia y rollback con PostgreSQL real; su ejecución automática se integra en la siguiente versión.

## Versión 4 — gobernanza y riesgos individuales

Se añaden nueve fitness functions, controles negativos, análisis de complejidad por función y pipeline de GitHub Actions con PostgreSQL 18. El registro de Risk Storming documenta nueve riesgos y la adaptación individual de sus tres fases. La verificación local reúne 26 pruebas; CI añade una prueba de integración con PostgreSQL.
