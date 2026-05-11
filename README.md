# Asistencia Seguro Automóviles · SDI

Mini-app móvil con guías paso a paso de emergencias del INS para automóviles (accidentes, asistencia vial, robo, vandalismo) + directorio de contactos del agente. Cada agente de [Seguros Digitales SDI®](https://www.segurosdelins.com) comparte SU URL fija en sus plantillas masivas de correo y WhatsApp; el cliente abre el link y ve la app lista con los datos de su agente.

🌐 **Producción:** [appasistenciaseguroautos.netlify.app](https://appasistenciaseguroautos.netlify.app)

---

## URLs por agente

Cada agente tiene su propio link fijo. Ponelo tal cual en tus plantillas de correo y WhatsApp.

| Agente | Licencia | URL para plantillas |
|---|---|---|
| Juan Carlos Hernández Vargas | 08-1318 | [`/`](https://appasistenciaseguroautos.netlify.app/) (default, sin params) |
| Fernando Hernández Vargas | 08-1319 | [`/?a=FHV`](https://appasistenciaseguroautos.netlify.app/?a=FHV) |

El parámetro `a` es **case-insensitive**: `?a=FHV`, `?a=fhv` y `?a=Fhv` cargan al mismo agente.

---

## Agregar un nuevo agente

Editar el objeto `AGENTES` dentro del `<script>` de [`index.html`](./index.html):

```js
const AGENTES = {
  jc: {  /* ... */  },
  fhv: { /* ... */  },
  // nuevo:
  nuevoid: {
    name:     'Nombre Completo del Agente',
    email:    'correo@dominio.com',
    phone:    '8888-8888',
    whatsapp: '50688888888',   // formato internacional sin +
    license:  '00-0000',
    website:  ''                // dejar vacío si no tiene
  }
};
```

Push a `main`. Netlify auto-deploya en 1-2 min. El nuevo link para plantillas: `appasistenciaseguroautos.netlify.app/?a=nuevoid`.

---

## Stack

- **Frontend:** HTML + React 18 + Babel standalone (single-file, sin build)
- **Estilos:** CSS custom (paleta navy/blue/green del cotizador-SDI) + Tailwind CDN + FontAwesome 6
- **Fuente:** Sora (Google Fonts)
- **Hosting:** Netlify (auto-deploy desde `main`)
- **Sin backend, sin base de datos, sin localStorage** — todo es estático

## Estructura

```
.
├── index.html              # App completa (~660 líneas)
├── ins-blanco.png          # Logo INS para header navy
├── INS BLANCO.png          # Copia con espacios (legacy)
├── sdi-logo-blanco.svg     # Logo SDI negativo para footer navy
└── README.md
```

## Local dev

```bash
npx serve . -p 8900
# luego abrir http://localhost:8900
```

## Vistas

1. **Home** — Hero "¿Tienes una emergencia?" + 5 acciones
2. **Accidente de Tránsito** — Reporte 800-800-8000 + Pacto Amistoso + trámites
3. **Asistencia Vial** — 800-800-8001 + servicios (grúa, batería, cerrajero, llanta, aeropuerto)
4. **Robo Total/Parcial** — Denuncia OIJ 911 + reporte INS + trámites según tipo
5. **Cobertura H** — Vandalismo/Naturaleza/Otros, trámite CED 10 días
6. **Directorio de Contactos** — Tarjeta del agente (Llamar/WhatsApp/Correo) + 3 líneas oficiales INS

---

© 2026 Propiedad Intelectual de Juan Carlos Hernández Vargas. Todos los derechos reservados.
