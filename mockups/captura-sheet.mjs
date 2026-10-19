// Captura COMPLETA del sheet de una vista, en tamaño teléfono (375 px, x2), para
// mostrarle a JC un cambio antes de publicarlo. Chrome headless + CDP, sin npm.
// La captura del panel de vista previa solo ve una pantalla y falla con la ventana
// oculta; esta agranda el alto de la ventana para que el sheet quepa entero.
//
// Uso:  node mockups/captura-sheet.mjs <url> "<texto con que empieza la fila>" <salida.png>
// Ej.:  node mockups/captura-sheet.mjs "http://localhost:8907/?n=Agente%20de%20Ejemplo&tel=8000-0000&wa=80000000&lic=00-0000" "Reportar accidente" accidente.png
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';

const [url, rowText, out] = process.argv.slice(2);
if (!url || !rowText || !out) { console.error('Uso: node captura-sheet.mjs <url> "<texto de la fila>" <salida.png>'); process.exit(1); }
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const PORT = 9333;
const prof = join(process.env.TEMP || '.', 'cap-prof-' + Date.now());
mkdirSync(prof, { recursive: true });

const chrome = spawn(CHROME, [
  '--headless=new', `--remote-debugging-port=${PORT}`, `--user-data-dir=${prof}`,
  '--hide-scrollbars', '--no-first-run', '--no-default-browser-check', 'about:blank'
], { stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));
const fin = async code => {
  chrome.kill();
  for (let i = 0; i < 10; i++) { await sleep(500); try { rmSync(prof, { recursive: true, force: true }); break; } catch {} }
  process.exit(code);
};

let targets = [];
for (let i = 0; i < 50; i++) {
  try { targets = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (targets.find(t => t.type === 'page')) break; } catch {}
  await sleep(200);
}
const page = targets.find(t => t.type === 'page');
if (!page) { console.error('Chrome no abrió'); await fin(1); }
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise(r => ws.addEventListener('open', r, { once: true }));
let id = 0; const pending = new Map();
ws.addEventListener('message', e => { const m = JSON.parse(e.data); if (m.id && pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } });
const send = (method, params = {}) => new Promise(r => { const i = ++id; pending.set(i, r); ws.send(JSON.stringify({ id: i, method, params })); });
const ev = async expr => (await send('Runtime.evaluate', { expression: expr, returnByValue: true, awaitPromise: true })).result?.result?.value;

// El recorte usa el alto del contenido (el sheet tiene min-height 38dvh y en vistas
// cortas dejaría blanco abajo). Alto de sobra: el sheet mide como máximo 90dvh, así que con 3400 px cabe una vista
// de ~3000 px sin scroll interno. Si alguna vista crece más, subir H.
const W = 375, H = 3400;
await send('Emulation.setDeviceMetricsOverride', { width: W, height: H, deviceScaleFactor: 2, mobile: true });
await send('Emulation.setEmulatedMedia', { features: [{ name: 'prefers-reduced-motion', value: 'reduce' }] });
await send('Page.enable');
await send('Page.navigate', { url });
await sleep(4500); // Babel compila en el navegador
const clicked = await ev(`(()=>{const el=[...document.querySelectorAll('button,a,div,[role=button]')].reverse().find(e=>e.textContent.trim().startsWith(${JSON.stringify(rowText)}));if(!el)return false;(el.closest('button,a,[role=button]')||el).click();return true;})()`);
if (!clicked) { console.error('No encontré la fila:', rowText); await fin(1); }
await sleep(2000);
const rect = await ev(`(()=>{const s=document.querySelector('.sh-sheet');if(!s)return null;const r=s.getBoundingClientRect();const b=document.querySelector('.sh-body');const c=b.lastElementChild.getBoundingClientRect().bottom-r.top+8;return {x:r.x,y:r.y,w:r.width,h:Math.min(r.height,c),sh:b.scrollHeight,ch:b.clientHeight};})()`);
if (!rect) { console.error('No se abrió el sheet'); await fin(1); }
if (rect.sh > rect.ch) console.warn(`Ojo: el sheet tiene scroll interno (${rect.sh} > ${rect.ch}); subir H para que salga entero.`);
const shot = await send('Page.captureScreenshot', { format: 'png', clip: { x: rect.x, y: rect.y, width: rect.w, height: rect.h, scale: 1 }, captureBeyondViewport: true });
writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
console.log('ok', out, `${rect.w * 2}x${Math.round(rect.h * 2)}`);
ws.close();
await fin(0);
