# Pruebas y Cobertura (breve)

Este directorio contiene las pruebas para `finance.py`. El flujo recomendado es iterar: añadir pruebas, ejecutar la suite y mejorar la cobertura.

- **Añadir pruebas:** usar `test_finance.py` como plantilla y pedir ayuda a Copilot para casos límite y normales.
- **Entorno:** crear el entorno virtual y activarlo:

```
python -m venv .venv
.venv\Scripts\Activate.ps1   # PowerShell
```

- **Instalar dependencias:**

```
.venv\Scripts\python -m pip install -U pytest pytest-cov
```

- **Ejecutar pruebas con cobertura:**

```
.venv\Scripts\python -m pytest --cov=finance --cov-report=term-missing
```

Usa Copilot para sugerir casos adicionales, luego vuelve a ejecutar hasta alcanzar la cobertura deseada.

## Experiencia con `pytest-cov` y Copilot

Tuve problemas iniciales para que la interfaz reconociera `pytest-cov` porque el entorno virtual no estaba apuntado correctamente. En lugar de centrarme solo en comandos, trabajé con Copilot paso a paso: describí el problema, recibí sugerencias para crear y usar un `.venv`, y para ajustar la configuración de VS Code para que use ese intérprete. Copilot me ayudó a iterar —probar, leer errores, corregir la configuración y volver a ejecutar— hasta que la UI mostró la cobertura. El enfoque fue colaborativo: explicar el síntoma, aceptar una sugerencia, probarla y repetir.
