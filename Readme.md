# Chat IA (Streamlit + Ollama DeepSeek‑R1)
**Docker + GPU (RTX 4060) + Túnel público para embeber en Moodle**

Pequeña app de chat hecha con **Streamlit** que consume **Ollama** (modelo `deepseek-r1:8b`). Incluye:
- **Docker Compose** con 3 servicios: `ollama`, `model-pull` (descarga el modelo) y `app` (Streamlit).
- Soporte **GPU** (probado con **GeForce RTX 4060 8 GB**).
- **Cloudflare Tunnel** para exponer la app con una **URL pública** y embeberla en el campus (Moodle).

---

## 🚀 Stack
- **Frontend**: Streamlit
- **LLM runtime**: Ollama (`deepseek-r1:8b`, quant Q4_K_M)
- **Infra**: Docker & Docker Compose
- **Opcional**: Cloudflare Tunnel para URL pública efímera

---

## 📁 Estructura
```
tu-proyecto/
├─ app/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ .streamlit/
│     └─ config.toml
├─ Dockerfile.app
└─ docker-compose.yml
```

**Puntos clave**
- `app.py` usa `ollama.Client(host=OLLAMA_HOST)` para hablar con `ollama` en red interna.
- `config.toml` desactiva CORS/XSRF para permitir `<iframe>` (en producción controlar con CSP en proxy).

---

## ✅ Requisitos
- **Windows 10/11** con **Docker Desktop (backend WSL2)**.
- **GPU activa en Docker**: Docker Desktop → *Settings → Resources → GPU*.
- Drivers NVIDIA actualizados.

**Test rápido de GPU en Docker**
```powershell
wsl --update
docker run --rm --gpus all nvidia/cuda:12.5.0-base-ubuntu22.04 nvidia-smi
```
Debe listar tu **RTX 4060**.

---

## ⚙️ Configuración de la app

### `app/.streamlit/config.toml`
```toml
[server]
headless = true
enableCORS = false
enableXsrfProtection = false
port = 8501
```

### Variables de entorno usadas
- `MODEL_NAME` (por defecto `deepseek-r1:8b`)
- `OLLAMA_HOST` (por defecto `http://ollama:11434` dentro de la red Docker)

---

## ▶️ Levantar todo (local)
```powershell
docker compose up --build -d
```

Abrí: **http://localhost:8501**

> **Nota**: el servicio `model-pull` descarga el modelo al iniciar. Si ves 404 de modelo, ejecutá:  
> `docker exec -it ollama ollama pull deepseek-r1:8b`

---

## 🧠 Usar GPU
El servicio `ollama` ya tiene `gpus: all`. Verificaciones:

```powershell
# ¿Ve la GPU dentro del contenedor?
docker exec -it ollama sh -lc 'ls /dev/nvidia* || true'

# Disparar una generación y ver logs (deberían mencionar CUDA/GPU)
curl -sS http://localhost:11434/api/generate -d '{ "model":"deepseek-r1:8b", "prompt":"hola" }' > NUL
docker logs -n 200 ollama | findstr /i cuda
```

Si no aparece GPU en logs:
- Confirmá GPU en Docker Desktop (Settings → Resources → GPU).
- Reiniciá servicios: `docker compose down && docker compose up -d`.

---

## 🌍 URL pública (Cloudflare Tunnel)
El `docker-compose.yml` incluye un servicio `tunnel` que crea una URL efímera:

```powershell
docker compose up -d tunnel
docker logs -f cf-tunnel
```

Buscá la línea con `https://<algo>.trycloudflare.com`. Esa es tu **URL pública**.

> La URL cambia si reiniciás el túnel. Para una URL fija (p. ej., `https://chat.tu-dominio.edu.ar`), usar **Named Tunnel** (se configura luego).

---

## 🧩 Embeber en Moodle

**Opción A (recomendada):** *Recurso → URL*  
- Pegar la URL pública (del túnel).
- **Apariencia**: _Embed_ / _En marco_.

**Opción B:** *Recurso → Página/Etiqueta* (modo HTML)  
```html
<iframe
  src="https://<tu-url>.trycloudflare.com"
  width="100%"
  height="720"
  style="border:1px solid #ddd;border-radius:12px;overflow:hidden"
  allow="clipboard-read; clipboard-write">
</iframe>
```

> Si el iframe queda en blanco por políticas de seguridad (*frame-ancestors*), en producción agregá en tu proxy (Nginx/Caddy/Cloudflare) un **CSP** con el dominio del campus:  
> `Content-Security-Policy: frame-ancestors 'self' https://campus.tuuni.edu.ar`

---

## 🔧 Troubleshooting

**`model "deepseek-r1:8b" not found (404)`**
```powershell
docker exec -it ollama ollama list
docker exec -it ollama ollama pull deepseek-r1:8b
```

**La app no llega a Ollama**
```powershell
docker exec -it streamlit-app sh -lc 'printenv OLLAMA_HOST && curl -sS $OLLAMA_HOST/api/tags'
```
Debe apuntar a `http://ollama:11434` y listar el modelo.

**GPU no usada**
- Ver `gpus: all` en `ollama`.
- Docker Desktop con GPU habilitada.
- Logs de `ollama` deberían mencionar CUDA tras una respuesta.

**URL pública no carga**
- Esperá unos segundos tras crear el túnel.
- Revisá `docker logs -f cf-tunnel`.
- Verificá que `app` esté arriba: `docker logs -f streamlit-app`.

---

## 🧱 Seguridad
- **No** expongas el puerto de **Ollama** a Internet; sólo la app.
- Para producción: TLS, dominio propio y **CSP `frame-ancestors`** para limitar quién puede embeber.

---

## 📜 Comandos útiles

```powershell
# Logs
docker compose logs -f app
docker compose logs -f ollama
docker compose logs -f cf-tunnel

# Reconstruir
docker compose down
docker compose up --build -d

# Borrar modelos (¡destruye la caché!)
docker stop ollama && docker rm ollama
docker volume rm tu-proyecto_ollama
```
