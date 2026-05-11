---
name: especialista-asistencia-autos
description: ESPECIALISTA APP ASISTENCIA SEGURO AUTOS — Mini-app móvil React single-file con guías de emergencia INS para automóviles (accidentes, asistencia vial, robo, vandalismo) + directorio de contactos del agente. Marca SDI fija. 2 agentes hardcoded (JC default + Fernando ?a=FHV) leídos desde query param de URL fija (no localStorage, no modal de config). Stack HTML + React 18 vía Babel CDN + Tailwind CDN + Sora. Deploy en Netlify desde main. Usar este skill cuando JC pida cualquier cambio, mejora o agregue un agente al proyecto APP-ASISTENCIA-SEGURO-AUTOS.
---

# Especialista App Asistencia Seguro Autos

Contexto completo del proyecto para retomar trabajo sin perder contexto. Leer COMPLETO antes de tocar código.

## Qué es

Mini-app móvil para clientes de agentes de Seguros Digitales SDI. El agente comparte SU URL fija (con query param `?a=<id>` en sus plantillas masivas de correo y WhatsApp). El cliente abre el link y ve:

- Guías paso a paso de emergencias INS (qué hacer en accidente / avería / robo / vandalismo)
- Directorio de contactos: tarjeta destacada de SU agente (llamar / WhatsApp / correo) + 3 líneas oficiales INS

El cliente NUNCA configura nada — los datos del agente vienen hardcodeados en el código y se eligen por el `?a=` de la URL.

## Estado actual

- **`80d78e6` (11 may 2026):** README.md público con tabla de URLs y guía para agregar agentes
- **`72f0972` (11 may 2026):** agentes hardcoded por query param `?a=` (JC default + Fernando `fhv`). Elimina modal, localStorage y botón ⚙
- **`9a45453` (11 may 2026):** rediseño completo estilo cotizador (header navy + logo INS, footer navy + logo SDI, tarjeta agente tricolor en Contactos)
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
├── index.html              # App completa (~660 líneas)
├── ins-blanco.png          # Logo INS para header navy
├── INS BLANCO.png          # Copia legacy con espacios (no tocar)
├── sdi-logo-blanco.svg     # Logo SDI negativo para footer navy
├── README.md               # Doc pública en GitHub
├── SKILL.md                # Este archivo
├── .gitignore              # Excluye .claude/ y *.b64.txt
└── .claude/launch.json     # Config preview local (gitignored)
```

## Agentes registrados

El objeto `AGENTES` está en el `<script type="text/babel">` de `index.html` (aprox. línea 477).

| id  | Nombre | Correo | Teléfono | WhatsApp | Licencia | Web |
|---|---|---|---|---|---|---|
| `jc` (default) | Juan Carlos Hernández Vargas | jhernandez@segurosdelins.com | 8822-1348 | 50688221348 | 08-1318 | www.segurosdelins.com |
| `fhv` | Fernando Hernández Vargas | fhernandez@segurosdelins.com | 8526-3532 | 50685263532 | 08-1319 | (vacío) |

### URLs para plantillas
- JC: `https://appasistenciaseguroautos.netlify.app/`
- Fernando: `https://appasistenciaseguroautos.netlify.app/?a=FHV`

El `?a=` es **case-insensitive** (`?a=FHV` y `?a=fhv` cargan al mismo agente).

### Agregar un nuevo agente

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

### Componentes clave
- `.app-header` — navy sticky con logo INS BLANCO + brand-text + botón ☎
- `.agent-strip` — debajo del header, "Tu agente: <nombre> · Licencia <id>"
- `.action-card` — cards de home con `.action-icon` circular coloreado (red/amber/purple/teal/green)
- `.hero-card` — cuadro azul tenue "¿Tienes una emergencia?"
- `.section-card` — cards de las vistas internas con `.section-card-header` coloreado
- `.btn-emergency` — botón verde grande con gradient + glow (`linear-gradient(180deg, --green, --green-dark)`)
- `.agent-card` — tarjeta gradient navy→blue en Directorio de Contactos con 3 botones (Llamar / WhatsApp verde / Correo)
- `.app-footer` — navy con logo SDI centrado (svg) + `.footer-agent` bloque destacado + leyenda

## Vistas

1. **Home** — Hero + 5 action-cards (Accidente, Vial, Robo, Vandalismo, Contactos)
2. **Accidente** — Reporte 800-800-8000 (verde) + Pacto Amistoso (4 condiciones check) + trámites 7/10 días
3. **Vial** — 800-800-8001 + servicios (grúa, batería, cerrajero, llanta) + taxi al aeropuerto
4. **Robo** — Denuncia 911 OIJ (gris) + reporte INS (verde) + trámites según tipo (total/parcial)
5. **Cobertura H** — Vandalismo/Naturaleza/Otros, 800-800-8000, CED 10 días
6. **Contactos** — Tarjeta del agente + 3 líneas INS (8000, 8001, 8353467) + oficinas centrales

## Lógica de carga (resumen)

```js
function getAgent() {
  const id = (new URLSearchParams(location.search).get('a') || 'jc').toLowerCase();
  return AGENTES[id] || AGENTES.jc;
}

function App() {
  const [view, setView] = useState('home');
  const profile = getAgent();  // se evalúa una vez en cada render
  // ...
}
```

Sin `useEffect`, sin localStorage, sin modal, sin estado de perfil — el agente sale directo de la URL.

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
- **Modal forzado primera vez** — el cliente del agente lo veía y quedaba atrapado sin poder usar la app. Eliminado.
- **Botón ⚙ en header** — sin sentido si no hay configuración. Eliminado.
- **Logo INS BLANCO.png embebido base64** — se intentó por problema del panel preview de Launch que no servía assets. Se resolvió usando `npx serve` real (puerto 8900).

## Pendiente

- **Subdominio** `asistencia.appsegurosdigitales.com` siguiendo el patrón del portal SDI (DNS + Netlify custom domain)
- **Fernando debe probar end-to-end** con `?a=FHV` y confirmar que sus datos están correctos
- **PWA opcional** (manifest + service worker) para que el cliente pueda "instalar" en su iPhone como app

## Reglas de trabajo con Juan Carlos (JC)

- JC NO programa. Necesita código completo y/o cambios ya pusheados.
- Pushear a main directo cuando JC autorice ("listo", "ok", "push", "actualiza github").
- Si JC pide "mockup previo" — crear archivo separado para evaluar sin tocar `index.html`.
- Verificación visual obligatoria antes de marcar completo: `preview_screenshot` después de cada cambio observable.
- Si JC se equivoca sobre algo (ej: "el archivo INS BLANCO no es el correcto"), validar con hash MD5 antes de cambiar — el archivo puede estar bien y el problema ser otro (cache, servidor, path).
