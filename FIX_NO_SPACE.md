# 🔧 SOLUCIÓN: "No space left on device"

## ❌ Error Encontrado

```json
{
  "error": "Data processing error: CAS service error : IO Error: No space left on device (os error 28)"
}
```

## 🎯 Causa

El **Container Disk es muy pequeño**. RunPod necesita espacio para:
- Sistema operativo base
- Logs
- Cache temporal
- Modelos
- Overhead de RunPod

---

## ✅ SOLUCIÓN INMEDIATA

### Paso 1: Aumentar Container Disk

**Ve a tu Template y cambia**:
- **Antes**: Container Disk = `5 GB` ❌
- **Ahora**: Container Disk = **`15 GB`** ✅

### Paso 2: Actualizar

1. **Editar Template**: https://runpod.io/console/serverless/user/templates
   - Encuentra tu template Piper
   - Edit → Container Disk = **15 GB**
   - Save

2. **Recrear Endpoint** (o actualizar):
   - Delete endpoint actual
   - Create new endpoint con template actualizado
   - O: Edit endpoint → cambiar template

---

## 📊 Requerimientos de Espacio

| Componente | Tamaño |
|------------|--------|
| Python base | ~200 MB |
| Piper binary | ~10 MB |
| Modelo español | ~10 MB |
| Dependencias | ~100 MB |
| **RunPod overhead** | **~5 GB** |
| **Margen seguridad** | **~5 GB** |
| **TOTAL RECOMENDADO** | **15 GB** |

---

## 🔄 CONFIGURACIONES ACTUALIZADAS

### Para Piper TTS

```
Container Disk: 15 GB (antes 5 GB)
```

### Para MeloTTS

```
Container Disk: 20 GB (antes 10 GB)
```

### Para Chatterbox

```
Container Disk: 40 GB (sin cambios)
```

---

## 📝 Dockerfile Actualizado

He actualizado `Dockerfile.piper` con mejor limpieza:
- ✅ Limpia cache de apt
- ✅ Limpia cache de pip
- ✅ Remueve archivos temporales
- ✅ Optimizado para mínimo espacio

---

## 🚀 Pasos Completos para Deploy

### 1. Commit Dockerfile Actualizado

```bash
cd /Users/mimac/mining/testApi/git/chatterbox
git add Dockerfile.piper
git commit -m "Optimize Dockerfile.piper - better cleanup for disk space"
git push origin master
```

### 2. Actualizar Template en RunPod

1. Ve a: https://runpod.io/console/serverless/user/templates
2. Edit tu template Piper
3. **Container Disk**: Cambiar a **15 GB**
4. Save

### 3. Recrear Endpoint

1. Delete endpoint actual
2. Create new endpoint
3. Selecciona template actualizado
4. Deploy

### 4. Esperar Build (7-8 min)

5. Probar nuevamente

---

## 💡 ¿Por Qué 15 GB?

RunPod necesita espacio extra para:

1. **Logs**: RunPod guarda logs extensivos
2. **Cache**: Sistema de cache para optimizar
3. **Temp files**: Archivos temporales durante ejecución
4. **Build artifacts**: Archivos del build
5. **Margen**: Para evitar problemas futuros

**15 GB es el mínimo seguro para Piper**

---

## ⚠️ Si Aún Falla

### Opción 1: Aumentar a 20 GB

Si 15 GB no es suficiente:
- Container Disk = **20 GB**

### Opción 2: Usar MeloTTS

MeloTTS es más estable con disco:
- Dockerfile: `Dockerfile.melo`
- Container Disk: **20 GB**

### Opción 3: Volver a Chatterbox

Si quieres algo probado:
- Dockerfile: `Dockerfile.simple` o `Dockerfile.lightweight`
- Container Disk: **40 GB**

---

## 📊 Comparación Actualizada

| Worker | Container Disk | Build | Deploy |
|--------|----------------|-------|--------|
| Piper | **15 GB** | 5 min | 7-8 min |
| MeloTTS | **20 GB** | 10 min | 15 min |
| Chatterbox | **40 GB** | 20 min | 30+ min |

---

## ✅ Checklist de Solución

```
[ ] 1. Actualizar Dockerfile.piper en GitHub
[ ] 2. Editar Template en RunPod
[ ] 3. Cambiar Container Disk a 15 GB
[ ] 4. Delete endpoint antiguo
[ ] 5. Crear nuevo endpoint
[ ] 6. Esperar build (7-8 min)
[ ] 7. Probar request
[ ] 8. ✅ Debería funcionar
```

---

## 🎯 Resumen

**Problema**: Container Disk muy pequeño (5 GB)
**Solución**: Aumentar a 15 GB
**Tiempo**: 5 minutos para cambiar + 7-8 min rebuild

---

## 📞 Si Sigue Fallando

Avísame y podemos:
1. Intentar con 20 GB
2. Cambiar a MeloTTS (más estable)
3. Usar Chatterbox lightweight (más probado)

---

**¡Con 15 GB debería funcionar perfectamente!** 🚀
