# Proyecto FastAPI de Ejemplo 🚀

Bienvenido a este proyecto de FastAPI, listo para escalar y usar en tus desarrollos. Aquí encontrarás una aplicación modular que integra FastAPI, SQLAlchemy y `databases` para conectar con una base de datos SQLite.

---

## 🔧 Instalación y Configuración

### 1. Crear el Entorno Virtual 🐍

Abre una terminal en la raíz del proyecto y ejecuta:

```bash
python -m venv venv
source venv/bin/activate
o
venv\Scripts\activate
```

### 2. Instalar Dependencias 📦

Con el entorno virtual activado, instala las dependencias con:

```bash
pip install -r requirements.txt
```

### 3. Ejecutar la Aplicación 🚀

Inicia el servidor de desarrollo con Uvicorn:

```bash
uvicorn app.main:app --reload
```

Abre tu navegador en [http://127.0.0.1:8000](http://127.0.0.1:8000) para ver la aplicación en acción.

---

## 🧪 Tests

### Ejecutar Tests

Para correr todos los tests, ejecuta:

```bash
pytest
```

### Crear Nuevos Tests

Agrega nuevos archivos que comiencen con `test_` dentro de la carpeta `tests/` siguiendo la convención de [pytest](https://docs.pytest.org/en/latest/). Esto asegurará que tus tests sean detectados y ejecutados correctamente.

---

## 🐳 Uso de Docker

### Construir la Imagen Docker

Desde la raíz del proyecto, construye la imagen ejecutando:

```bash
docker build -t fastapi-app .
```

### Ejecutar el Contenedor

Levanta el contenedor con:

```bash
docker run -d -p 8000:8000 fastapi-app
```

La aplicación se ejecutará en el puerto 8000 y estará accesible en [http://localhost:8000](http://localhost:8000).

---

## 🚀 Despliegue

Puedes desplegar esta aplicación en cualquier entorno que soporte Docker. Solo necesitas:

1. **Construir la imagen:** `docker build -t fastapi-app .`
2. **Ejecutar el contenedor:** `docker run -d -p 8000:8000 fastapi-app`

---

¡Disfruta programando y extendiendo este proyecto! Si encuentras algún problema o tienes sugerencias, siéntete libre de abrir un _issue_ o enviar un _pull request_.

Happy Coding! 😄
