import { pathToFileURL } from 'node:url';
const base = new URL('../', import.meta.url);
const mod = new URL('../sources/primary/port_js.mjs', import.meta.url);
process.argv = [process.argv[0], mod.pathname, '--n', '100', '--reps', '15', '--seed', '42', '--out', new URL('../results/node_port_output.json',import.meta.url).pathname.replace(/^\/(.:\/)/,'$1')];
await import(mod.href);
