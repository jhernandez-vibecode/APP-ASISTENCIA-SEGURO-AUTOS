---
name: especialista-asistencia-autos
description: ESPECIALISTA APP ASISTENCIA SEGURO AUTOS — Mini-app móvil React single-file con guías de emergencia INS para automóviles (accidentes, asistencia vial, robo, vandalismo) + directorio de contactos del agente. Marca SDI fija. Multi-agente: la ficha del agente (nombre, contacto, licencia, web) llega por parámetros de URL (?n,tel,wa,em,lic,web) que el cotizador arma desde el perfil ⚙; roster hardcodeado por ?a=<id> (JC default + Fernando) como fallback retrocompatible. Sin localStorage ni modal. PWA instalable (manifest + iconos de carro propios + vista "Instalá la app"; manifest dinámico conserva al agente en el start_url). Stack HTML + React 18 vía Babel CDN + Tailwind CDN + Sora. Deploy en Netlify desde main. Usar este skill cuando JC pida cualquier cambio, mejora o agregue un agente al proyecto APP-ASISTENCIA-SEGURO-AUTOS.
---

# Especialista App Asistencia Seguro Autos

Contexto completo del proyecto para retomar trabajo sin perder contexto. Leer COMPLETO antes de tocar código.

## Qué es

Mini-app móvil para clientes de agentes de Seguros Digitales SDI. El agente comparte SU URL fija (con query param `?a=<id>` en sus plantillas masivas de correo y WhatsApp). El cliente abre el link y ve:

- Guías paso a paso de emergencias INS (qué hacer en accidente / avería / robo / vandalismo)
- Directorio de contactos: tarjeta destacada de SU agente (llamar / WhatsApp / correo) + 3 líneas oficiales INS

El cliente NUNCA configura nada. Los datos del agente llegan **en la URL**: el cotizador (módulo Pólizas Activas) arma el link con la ficha del agente por parámetros (`?n,tel,wa,em,lic,web`) tomada de su perfil ⚙. Si esos parámetros no vienen, se cae a un **roster fijo** por `?a=<id>` (JC / Fernando). Así la guía muestra a **cualquier** agente sin tocar el código.

## Estado actual

- **`72f0972` (11 may 2026):** agentes hardcoded por query param `?a=` (JC default + Fernando `fhv`). Elimina modal, localStorage y botón ⚙
- **`9a45453` (11 may 2026):** rediseño estilo cotizador (header navy + logo INS, footer navy + logo SDI, tarjeta agente tricolor en Contactos)
- **`98537f4`:** **Rediseño Sereno** — home con saludo "¿Qué pasó con tu vehículo?" + chip de agente en el header + banner SOS rojo + lista dividida de tipos de asistencia. **Este es el diseño vigente** (ya NO el cotizador original).
- **`77b7626`:** pin de CDN a versión fija (React 18.3.1, Babel `@7.29.7`) tras caída por Babel 8. **NUNCA usar CDN flotante.**
- **`6aa91c1` (26 jun 2026):** nueva sección **"¿Qué cubre tu asistencia?"** (ver sección dedicada abajo).
- **`46cffc3` (26 jun 2026):** SKILL.md sincronizado en las **3 ubicaciones** con el estado real del código.
- **`b3a1e1a` (1 jul 2026) — Ficha del agente por URL (multi-agente):** `getAgent()` lee `?n,tel,wa,em,lic,web` (saneados) y arma el perfil del agente; si no viene `?n=`, cae al roster fijo `?a=<id>` (retrocompatible). El cotizador (`js/poliza-email.js`) **embebe automáticamente** esos parámetros en el link "Abrir mi guía" del correo de Póliza Activa, tomándolos del perfil ⚙ del agente. **Cualquier agente aparece con solo llenar su perfil en el cotizador — ya no hay que hardcodearlo aquí.** Cambio coordinado con el repo `COTIZADOR-AUTOS` (deben desplegar juntos).
- **`d5bbd9d` (24 ago 2026) — PWA instalable:** `manifest.webmanifest` + iconos propios (carro FA6 `car-side` blanco sobre gradiente navy→azul: `favicon.svg`, `favicon.ico` 16/32/48, `icon-180` opaco iOS, `icon-192/512` any, `icon-maskable-512`) + metas iOS + vista nueva **"Instalá la app"** (pasos iPhone/Android, botón nativo `beforeinstallprompt`, detección de plataforma y de app ya instalada) + fila al final de la lista del Home. **Sin service worker** (patrón del cotizador viajero: instala igual y siempre carga fresco). 🔑 **Manifest dinámico:** si la URL trae `?n=` o `?a=`, un script en el `<head>` reemplaza el manifest por un `data:` URL cuyo `start_url` CONSERVA esos parámetros (iconos en URL absoluta, porque en un manifest `data:` las rutas relativas no resuelven) — así la app instalada por un cliente de Fernando abre con Fernando, sin localStorage. Icono generado con el glifo oficial FA 6.4.0 (CC BY 4.0), NO es logo inventado.
- **`ef7b342` + `2089464` (29 ago 2026) — Apple Motion (rollback tag `pre-apple-motion-29ago`):** física de interfaz según la skill `apple-design` (WWDC *Designing Fluid Interfaces*), aprobada por JC sobre mockup interactivo. (1) **Las 7 vistas internas ya NO cambian de pantalla: se presentan dentro de un sheet arrastrable** (componente `Sheet` en el babel script, renderizado con `ReactDOM.createPortal` sobre `<body>`): drag 1:1 SOLO desde la cabecera `.sh-head` (para no pelear con el scroll del contenido en `.sh-body`), rubber-band arriba del tope, proyección de momentum al soltar (decide abrir/cerrar por dónde IBA el gesto) y resorte interrumpible (agarrarlo en vuelo lo detiene y sigue desde el valor de presentación). El home queda SIEMPRE montado de fondo y se hunde 1:1 con el gesto (`.app` scale+brightness, restaurado en el cleanup). `key={view}` en el Sheet: sin él, el `onClosed` de una guía cerrándose pisaba a otra recién abierta. (2) **El header perdió la mutación** back-btn/detail-title (ya no existen): queda la barra compacta sticky (logo + ☎) que gana **material translúcido** (`.app-header.mat`, blur+saturate) al pasar de 90px de scroll; el greet + agent-chip viven en `.hero-navy`, bloque navy NO sticky con radio inferior 24 — libera media pantalla que antes viajaba fija. (3) **Feedback al pointer-down (90ms)** en todas las superficies tocables (bloque "APPLE MOTION" al final del `<style>`). (4) Física compartida en **`window.SDIPhysics`** (script normal pre-Babel: `springStepper(dampingRatio, response)`, `project`, `rubberband`, `reduced`). (5) `prefers-reduced-motion` → aparece/cierra sin física; `prefers-reduced-transparency` → materiales sólidos (verificado: el pane de preview lo tiene activo y el fallback navy sólido respondió). ✅ **Smoke de JC OK el 29 ago 2026 en su teléfono** ("quedaron muy bien"). 🧊 Cooldown hasta ~5 sep 2026.
- **Producción:** [appasistenciaseguroautos.netlify.app](https://appasistenciaseguroautos.netlify.app) (auto-deploy desde `main`)
- **Repo:** [jhernandez-vibecode/APP-ASISTENCIA-SEGURO-AUTOS](https://github.com/jhernandez-vibecode/APP-ASISTENCIA-SEGURO-AUTOS)

## Stack técnico

- **Frontend:** HTML + React 18 + Babel standalone (single-file, sin build, sin npm install)
- **Estilos:** CSS custom inline + Tailwind CDN + FontAwesome 6 CDN
- **Fuente:** Sora (Google Fonts preloaded)
- **Hosting:** Netlify, deploy automático desde `main` (1-2 min)
- **Sin backend, sin DB, sin localStorage** — todo estático

## Estructura del repo

```
APP-ASISTENCIA-SEGURO-AUTOS/
├── index.html              # App completa (1133 líneas · verificado 24 ago 2026)
├── manifest.webmanifest    # PWA (start_url "/" — el dinámico vive en el <head>)
├── favicon.svg             # Favicon vectorial (carro + gradiente)
├── favicon.ico             # Fallback pestañas desktop (16/32/48)
├── icon-180.png            # apple-touch-icon iOS (cuadrado OPACO)
├── icon-192.png            # PWA any
├── icon-512.png            # PWA any (esquinas redondeadas)
├── icon-maskable-512.png   # PWA maskable (full-bleed, zona segura 80%)
├── ins-blanco.png          # Logo INS para header navy
├── INS BLANCO.png          # Copia legacy con espacios (no tocar)
├── sdi-logo-blanco.svg     # Logo SDI negativo para footer navy
├── README.md               # Doc pública en GitHub
├── SKILL.md                # Este archivo
├── .gitignore              # Excluye .claude/ y *.b64.txt
└── .claude/launch.json     # Config preview local (gitignored)
```

### Procedencia de los logos (NUNCA regenerar ni inventar)

| Archivo | Origen | Verificación |
|---|---|---|
| `ins-blanco.png` | `C:/Users/segur/Downloads/LOGOS INS/LOGOS INS NUEVO/INS BLANCO.png` (copia idéntica · ojo: la carpeta padre es `LOGOS INS`, no está suelta en `Downloads/`) | MD5 `a02c976fccdb0bbb7a02b6c9ea9d4bb7` |
| `INS BLANCO.png` | Copia legacy con espacios en el nombre, del repo original | Mismo MD5 `a02c976...` que `ins-blanco.png` |
| `sdi-logo-blanco.svg` | `SDI-Brand-Kit-v1/02-Logos-SVG/04-sdi-logo-negativo.svg` (logo SDI negativo) | — |

Si JC dice "el logo no es el correcto", **primero comparar el MD5** contra el original antes de reemplazar: el archivo puede estar bien y el problema ser caché, servidor o path.

## Agentes registrados

`getAgent()` (en el `<script type="text/babel">` de `index.html`, línea 338) resuelve al agente con esta prioridad:

1. **Ficha por URL (mecanismo principal, multi-agente).** Si viene `?n=<nombre>`, el perfil se arma con los parámetros de la URL:

   | Param | Campo | Notas |
   |---|---|---|
   | `n`   | nombre    | obligatorio (dispara este modo) |
   | `tel` | teléfono  | se limpia a caracteres de teléfono |
   | `wa`  | WhatsApp  | dígitos; si son 8 se antepone `506` |
   | `em`  | correo    | validado como email o se descarta |
   | `lic` | licencia  | |
   | `web` | sitio web | http/https o dominio; `javascript:` se descarta |

   Estos los **arma el cotizador** (`js/poliza-email.js`) desde el perfil ⚙ del agente y los mete en el link "Abrir mi guía" del correo de Póliza Activa. Todo se sanea (React escapa el texto; los helpers `_qEmail/_qWeb/_qPhone/_qWa` filtran).

2. **Roster fijo por `?a=<id>` (fallback / blast masivo).** Si NO viene `?n=`, se usa el objeto `AGENTES` hardcodeado (línea 314). `?a=` es **case-insensitive**; sin nada válido → `jc`.

   | id  | Nombre | Correo | Teléfono | WhatsApp | Licencia | Web |
   |---|---|---|---|---|---|---|
   | `jc` (default) | Juan Carlos Hernández Vargas | jhernandez@segurosdelins.com | 8822-1348 | 50688221348 | 08-1318 | www.segurosdelins.com |
   | `fhv` | Fernando Hernández Vargas | fhernandez@segurosdelins.com | 8526-3532 | 50685263532 | 08-1319 | (vacío) |

   - JC: `https://appasistenciaseguroautos.netlify.app/`
   - Fernando: `https://appasistenciaseguroautos.netlify.app/?a=FHV`

### Agregar un agente al roster `?a=` (solo para el blast masivo)

Para agentes que solo comparten el link fijo por plantilla (sin pasar por el cotizador). Si el agente usa el cotizador, **NO hace falta**: con llenar su perfil ⚙ su ficha ya viaja por URL.

1. Editar el objeto `AGENTES` en `index.html`:

```js
const AGENTES = {
  jc:  { /* ... */ },
  fhv: { /* ... */ },
  nuevoid: {
    name:     'Nombre Completo del Agente',
    email:    'correo@dominio.com',
    phone:    '8888-8888',
    whatsapp: '50688888888',   // formato internacional sin +
    license:  '00-0000',
    website:  ''                // string vacío si no tiene
  }
};
```

2. Push a `main` → Netlify auto-deploya.
3. URL del nuevo agente para plantillas: `https://appasistenciaseguroautos.netlify.app/?a=nuevoid`

## Diseño visual

> ⚠️ NOTA: las clases de abajo (`.action-card`, `.agent-strip`, `.hero-card`, `.btn-emergency`) son del cotizador original y **ya no existen** tras el Rediseño Sereno (`98537f4`). El diseño vigente usa: header navy con greet + `.agent-chip`, banner `.sos`, lista `.list`/`.row`, `.section-card` en vistas internas, y la familia `cob-*` en la sección de cobertura. La paleta (tokens `:root`) sigue siendo válida como referencia. Leer el `:root` y los componentes reales en `index.html` antes de tocar CSS.

Estilo **basado en el cotizador-autos** (NO Modern SaaS Bento Tricolor — ese es de Reclamos-SDI).

### Paleta
```css
--navy:       #0c2340   /* header, footer */
--navy-soft:  #143055
--blue:       #0369a1
--blue-light: #0ea5e9
--green:      #16a34a   /* botones emergencia */
--green-dark: #15803d
--amber:      #d97706
--red:        #dc2626
--red-dark:   #991b1b
```

### Tokens
- Fuente: Sora, 400-800
- Radius: 8px inputs, 10-12px botones, 14px cards, 16-18px modal
- Shadow: layered (`shadow-sm/md/lg`) — capa difusa + sharp
- **Layout mobile-first: `max-width: 480px`** en el contenedor `.app` (centrado con `margin:0 auto`), lo que encuadra también header y footer. Es la medida fija de la app — no ensanchar sin orden de JC.

### Componentes clave
- `.app-header` — barra compacta navy sticky con logo INS BLANCO + `.brand-text` + botón ☎, SIEMPRE igual (desde 29 ago 2026 ya NO muta a back-btn/detail-title: las vistas van en sheet y `titleByView[view]` es el título de la cabecera del sheet). Con scroll >90px gana `.mat` (material translúcido). El `.brand-text` lleva dos textos **literales, no tocar**: `.brand-t1` → **"Asistencia Autos"** y `.brand-t2` → **"Instituto Nacional de Seguros"**. El greet + `.agent-chip` viven en `.hero-navy` (bloque navy no sticky)
- `.agent-strip` — debajo del header, "Tu agente: <nombre> · Licencia <id>"
- `.action-card` — cards de home con `.action-icon` circular coloreado (red/amber/purple/teal/green)
- `.hero-card` — cuadro azul tenue "¿Tienes una emergencia?"
- `.section-card` — cards de las vistas internas con `.section-card-header` coloreado
- `.btn-emergency` — botón verde grande con gradient + glow (`linear-gradient(180deg, --green, --green-dark)`)
- `.agent-card` — tarjeta gradient navy→blue en Directorio de Contactos con 3 botones (Llamar / WhatsApp verde / Correo)
- `.app-footer` — navy con logo SDI centrado (svg) + `.footer-agent` bloque destacado del agente (nombre, licencia, correo y website si tiene) + dos textos **literales, no tocar**:
  - `.footer-plataforma` → **"Plataforma de Seguros Digitales SDI®"** (la marca sale de `BRAND.empresa = 'Seguros Digitales SDI®'`, con el ® incluido)
  - `.footer-legal` → **"© 2026 Propiedad Intelectual de Juan Carlos Hernández Vargas. Todos los derechos reservados."** (`BRAND.legal`)

## Vistas

(En `index.html` el estado de vista es `view` en `App()`; cada vista es un componente y el header muestra `titleByView[view]`.)

1. **Home** — saludo + chip de agente + banner SOS (accidente) + tarjeta **"¿Qué cubre tu asistencia?"** (abre `cobertura`) + lista dividida (Vial, Robo, Vandalismo, Contactos, Instalar)
2. **Accidente** — Reporte 800-800-8000 + Pacto Amistoso (4 condiciones check) + trámites 7/10 días
3. **Vial** — 800-800-8001 + servicios (grúa, batería, cerrajero, llanta) + taxi al aeropuerto
4. **Robo** — Denuncia 911 OIJ + reporte INS + trámites según tipo (total/parcial)
5. **Cobertura H** (`coberturaH`) — Vandalismo/Naturaleza/Otros, 800-800-8000, CED 10 días
6. **Contactos** — Tarjeta del agente + 3 líneas oficiales INS + oficinas centrales (Calle 9 y 11, Av. 7, San José · contactenos@grupoins.com)
   - `800-800-8000` — Reporte de accidentes (choques / daños, 24/7)
   - `800-800-8001` — Asistencia vial (grúa, batería, cerrajero)
   - `800-8353467` — Consultas generales (línea Teleins) — **número completo, NO es `8353467` suelto**
7. **Cobertura** (`cobertura`) — **"¿Qué cubre tu asistencia?"**: el cliente elige el año del modelo y ve su plan de Multiasistencia + beneficios (ver sección dedicada).
8. **Instalar** (`instalar`) — **"Instalá la app"** (24 ago 2026): preview del icono como se ve en la pantalla de inicio + pasos iPhone (Safari → Compartir → Añadir a pantalla de inicio) y Android (Chrome; si `beforeinstallprompt` disparó, botón verde de instalación nativa con un toque). Detecta plataforma por UA (la del cliente se muestra primero) y modo standalone (`display-mode` / `navigator.standalone`) → card "¡Ya la tenés instalada!". CSS namespaced `pwa-`. El prompt nativo se captura en un `<script>` del `<head>` (ANTES de que Babel compile) en `window._pwaPrompt` + evento `pwa-prompt-ready`.

## Sección "¿Qué cubre tu asistencia?" (vista `cobertura`)

Feature de auto-consulta: el cliente elige el **año del modelo** de su carro (menú desplegable) y la app calcula qué **plan de Multiasistencia INS** le corresponde por antigüedad, mostrando un hero card del plan + beneficios agrupados en acordeones.

- **Alcance:** SOLO **Uso Personal · Particulares y Carga Liviana** (autos, SUV, pick-up, carga liviana). NO incluye Uso Comercial, motos, buses ni camiones (decisión de JC, 26 jun 2026).
- **Lógica año→plan** (`cobPlanForAge`, antigüedad = año actual − año modelo):
  - 0–6 años → **Plan Plus** (acento teal)
  - 7–15 años → **Plan Básico** (acento azul)
  - 16–20 años → **Plan Limitado** (acento ámbar, "Solo CR", sin internacional)
  - 21+ años → **No aplica** asistencia gratuita → hero gris + CTA WhatsApp al agente (captar lead)
- **Datos:** copiados LITERAL del contrato `CONDICIONES OPERATIVAS MULTIASISTENCIA DE AUTOMÓVILES.pdf` (en `OneDrive/ARCHIVO DIGITAL/Automóviles/`). Constantes `COB_PLUS_NAC`, `COB_BASICO_NAC`, `COB_LIMITADO_NAC`, `COB_INTL` con `{g, n, ev, amt}` (grupo, nombre, nº eventos, monto). **NUNCA inventar montos/eventos** — son cifras SUGESE; salen del PDF.
- **Grupos** (`COB_GROUPS`): road / med / info / plus (exclusivos Plus) / intl (solo Plus y Básico).
- **CSS namespaced `cob-`** para no chocar con el resto de la app. El WhatsApp del CTA usa el **agente actual** (`profile.whatsapp` según `?a=`), no hardcodeado.
- **Selector de año:** menú desplegable `<select>` grande (`.cob-yearsel`), no chips horizontales (se cambió 26 jun por ser poco intuitivo). Acordeones = `<details>` nativos; `key={year}` resetea al cambiar año.

## Lógica de carga (resumen)

```js
function getAgent() {
  const qp = new URLSearchParams(location.search);
  const name = _q(qp.get('n'));
  if (name) {                    // 1) ficha personalizada por URL (la arma el cotizador)
    return {
      name, email: _qEmail(qp.get('em')), phone: _qPhone(qp.get('tel')),
      whatsapp: _qWa(qp.get('wa')) || _qWa(qp.get('tel')),
      license: _q(qp.get('lic')), website: _qWeb(qp.get('web'))
    };
  }
  const id = (qp.get('a') || 'jc').toLowerCase();   // 2) roster fijo
  return AGENTES[id] || AGENTES.jc;
}

function App() {
  const [view, setView] = useState('home');
  const profile = getAgent();  // se evalúa en cada render
  // ...
}
```

Sin `useEffect`, sin localStorage, sin modal, sin estado de perfil — el agente sale directo de la URL (parámetros del cotizador o roster `?a=`).

## Flujo de trabajo (cómo hacer cambios)

1. Editar `index.html` en `C:/Users/segur/APP-ASISTENCIA-SEGURO-AUTOS/`
2. Verificar local con `npx serve . -p 8900` (ya está en `.claude/launch.json`)
3. `git add` + `git commit` + `git push origin main`
4. Netlify auto-deploya en 1-2 min
5. **Sincronizar SKILL.md en las 3 ubicaciones** (ver siguiente sección)

## Sincronización del SKILL.md (REGLA 🔴)

Cuando se actualice este SKILL.md, sincronizar en las 3 ubicaciones:

1. **Repo (visible en GitHub):** `C:/Users/segur/APP-ASISTENCIA-SEGURO-AUTOS/SKILL.md`
2. **Skill instalado (Claude Code):** `C:/Users/segur/.claude/skills/especialista-asistencia-autos/SKILL.md`
3. **Backup en Downloads:** `C:/Users/segur/Downloads/SKILL_APP_ASISTENCIA_AUTOS.md`

Comando rápido para syncar las 3:

```bash
cp C:/Users/segur/APP-ASISTENCIA-SEGURO-AUTOS/SKILL.md \
   C:/Users/segur/.claude/skills/especialista-asistencia-autos/SKILL.md && \
cp C:/Users/segur/APP-ASISTENCIA-SEGURO-AUTOS/SKILL.md \
   C:/Users/segur/Downloads/SKILL_APP_ASISTENCIA_AUTOS.md
```

## Decisiones de diseño descartadas

- **localStorage + modal de configuración multi-agente** (commit `9a45453`) — descartado porque el link es masivo y fijo en plantillas, no se puede personalizar por cliente. Reemplazado por agentes hardcoded por query param.
  - **Ojo — la ficha por URL (1 jul 2026) NO revive esto.** Los parámetros `?n,tel,...` SÍ funcionan por cliente porque el agente los hornea en el link que comparte (los arma el cotizador); no dependen del navegador del cliente. Es lo contrario del localStorage descartado (que solo vivía en el navegador del agente).
- **Modal forzado primera vez** — el cliente del agente lo veía y quedaba atrapado sin poder usar la app. Eliminado.
- **Botón ⚙ en header** — sin sentido si no hay configuración. Eliminado.
- **Logo INS BLANCO.png embebido base64** — se intentó por problema del panel preview de Launch que no servía assets. Se resolvió usando `npx serve` real (puerto 8900).

## Pendiente

1. **Subdominio** `asistencia.appsegurosdigitales.com` siguiendo el patrón del portal SDI (DNS + Netlify custom domain). ⚠️ Al migrar de dominio, revisar el manifest dinámico y los iconos absolutos (usan `location.origin`, se adaptan solos) y avisar que las apps YA instaladas siguen apuntando al dominio viejo.
2. **Fernando debe probar end-to-end** con `?a=FHV` y confirmar que sus datos están correctos — ahora incluye instalar la PWA desde su link y verificar que la app instalada abre con Fernando.
3. (Opcional, no pedido) **Service worker para modo offline** de las guías de emergencia. Se decidió NO incluirlo el 24 ago 2026 para evitar caché viejo — el patrón viajero instala sin SW. Solo si JC lo pide.

✅ ~~PWA (manifest + icono + explicación de instalación)~~ — **HECHO 24 ago 2026 (`d5bbd9d`)**, pedido del 26 jun.

## Reglas de trabajo con Juan Carlos (JC)

- JC NO programa. Necesita código completo y/o cambios ya pusheados.
- Pushear a main directo cuando JC autorice ("listo", "ok", "push", "actualiza github").
- Si JC pide "mockup previo" — crear archivo separado para evaluar sin tocar `index.html`.
- Verificación visual obligatoria antes de marcar completo: `preview_screenshot` después de cada cambio observable.
- Si JC se equivoca sobre algo (ej: "el archivo INS BLANCO no es el correcto"), validar con hash MD5 antes de cambiar — el archivo puede estar bien y el problema ser otro (cache, servidor, path).
