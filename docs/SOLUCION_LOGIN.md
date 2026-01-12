# 🔐 Solución: Login en Modo Headless

## ❌ El Problema

En modo **headless** (sin interfaz gráfica), NO puedes ver el navegador para hacer login manual. Por eso da error.

---

## ✅ SOLUCIÓN 1: Exportar Cookies desde tu PC (Recomendado)

### Paso 1: En tu PC Local

1. **Desactiva headless temporalmente** en tu `.env`:
```env
HEADLESS_MODE=false
AUTO_MODE=false
```

2. **Ejecuta el bot localmente:**
```bash
python main.py
```

3. **Haz login manualmente** cuando te lo pida

4. **Las cookies se guardan automáticamente** en `data/workana_cookies.pkl`

### Paso 2: Subir Cookies al VPS

```bash
# Desde tu PC local
scp data/workana_cookies.pkl root@157.230.134.177:/root/bot-workana/data/
```

### Paso 3: En el VPS

```bash
# Verificar que las cookies están
ls -la ~/bot-workana/data/workana_cookies.pkl

# Reiniciar el servicio
sudo systemctl restart workana-bot
```

**¡Listo!** El bot usará las cookies y no pedirá login.

---

## ✅ SOLUCIÓN 2: Desactivar Headless Temporalmente

### Paso 1: Cambiar .env en VPS

```bash
cd ~/bot-workana
nano .env
```

Cambiar:
```env
HEADLESS_MODE=false  # Cambiar a false
AUTO_MODE=false     # Cambiar a false
```

### Paso 2: Instalar VNC para Ver el Navegador

```bash
# Instalar VNC y Xvfb
sudo apt install -y xvfb x11vnc fluxbox

# Iniciar Xvfb (servidor gráfico virtual)
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

### Paso 3: Ejecutar Bot Manualmente

```bash
cd ~/bot-workana
python3 main.py
```

**Problema:** Aún así no verás el navegador fácilmente. **Mejor usar Solución 1.**

---

## ✅ SOLUCIÓN 3: Usar Xvfb (Sin Interfaz pero Funcional)

Xvfb permite que Chrome "piense" que hay pantalla sin mostrarla.

### Instalar Xvfb:

```bash
sudo apt install -y xvfb
```

### Modificar el bot para usar Xvfb:

El bot ya debería funcionar con headless, pero si necesitas forzar:

```bash
# Ejecutar con Xvfb
xvfb-run -a python3 main.py
```

**Pero esto no soluciona el login manual.** Necesitas las cookies.

---

## 🎯 RECOMENDACIÓN FINAL

**Usa la Solución 1** (exportar cookies desde tu PC):

1. ✅ Más fácil
2. ✅ Más seguro
3. ✅ No necesitas ver el navegador
4. ✅ Funciona perfecto con headless

**Pasos rápidos:**
```bash
# En tu PC: hacer login y guardar cookies
# Luego subir al VPS:
scp data/workana_cookies.pkl root@157.230.134.177:/root/bot-workana/data/
```

---

## 🔄 Renovar Cookies (Cuando Expiren)

Las cookies expiran después de un tiempo. Cuando el bot diga "LOGIN MANUAL REQUERIDO":

1. Repite la Solución 1
2. O desactiva headless temporalmente, haz login, y vuelve a activar

---

## ⚠️ Nota sobre Headless

**Modo headless = sin interfaz gráfica**
- ✅ Usa menos recursos
- ✅ Más rápido
- ❌ No puedes ver el navegador
- ✅ Perfecto para VPS (no necesitas verlo)

**Para ver el navegador en VPS necesitarías:**
- VNC Server (complejo)
- O simplemente exportar cookies desde tu PC (más fácil)
