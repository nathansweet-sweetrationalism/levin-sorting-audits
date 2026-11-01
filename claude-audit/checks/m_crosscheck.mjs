// Independent Node.js re-derivation of M2 and M6 (no shared code with the Python checks).
// Uses BigInt rationals for M6. Exit code 0 iff all assertions hold.
import fs from 'node:fs';
const inv = v => { let c = 0; for (let i = 0; i < v.length; i++) for (let j = i + 1; j < v.length; j++) if (v[i] > v[j]) c++; return c; };
function* perms(a) { if (a.length <= 1) { yield a; return; } for (let i = 0; i < a.length; i++) for (const p of perms([...a.slice(0, i), ...a.slice(i + 1)])) yield [a[i], ...p]; }
let ok2 = true, nsw = 0;
for (let n = 2; n <= 8; n++) for (const p of perms([...Array(n).keys()])) for (let i = 0; i < n - 1; i++) if (p[i] > p[i + 1]) {
  const q = p.slice(); [q[i], q[i + 1]] = [q[i + 1], q[i]]; if (inv(q) - inv(p) !== -1) ok2 = false; nsw++; }
// M6: enumerate label arrangements via bitmasks, sum H, compare to b(b-1)+s(s-1) / N^2 exactly
const gcd = (a, b) => b === 0n ? a : gcd(b, a % b);
let ok6 = true;
for (let b = 1; b <= 7; b++) for (let s = 1; s <= 7; s++) {
  const N = b + s; let sumH = 0n, cnt = 0n;
  for (let m = 0; m < (1 << N); m++) { let pc = 0; for (let k = 0; k < N; k++) pc += (m >> k) & 1; if (pc !== b) continue;
    let H = 0; for (let k = 0; k < N - 1; k++) if (((m >> k) & 1) === ((m >> (k + 1)) & 1)) H++; sumH += BigInt(H); cnt++; }
  // E[A] = sumH / (cnt * N)  vs  (b(b-1)+s(s-1)) / N^2
  const lhsN = sumH * BigInt(N * N), rhsN = BigInt(b * (b - 1) + s * (s - 1)) * cnt * BigInt(N);
  if (lhsN !== rhsN) ok6 = false; }
const out = { M2_node: { pass: ok2, swaps_checked: nsw }, M6_node: { pass: ok6, range: 'b,s in 1..7' } };
fs.mkdirSync('results', { recursive: true });
fs.writeFileSync('results/m_crosscheck_node.json', JSON.stringify(out, null, 2));
console.log(JSON.stringify(out)); process.exit(ok2 && ok6 ? 0 : 1);
