from pathlib import Path
import json,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1];j=json.loads((ROOT/'results/historical_replay_summary.json').read_text());f=json.loads((ROOT/'results/fish_independent_audit.json').read_text());z=j['summary']
fig,ax=plt.subplots(1,2,figsize=(12,4.7),layout='constrained');cs=[x['C'] for x in z]
for key,label,col in [('mean_A','Mixed model','#1769aa'),('mean_stable_A','Stable-sort control','#b45f06'),('mean_conditional_A','Within-key permutation mean','#318248')]:ax[0].plot(cs,[x[key] for x in z],marker='o',label=label,color=col,linewidth=1.8)
ax[0].axhline(.4875,color='#666',ls='--',label='Unconditional fixed-count mean');ax[0].set_xscale('log',base=2);ax[0].set_xticks(cs,labels=[str(c) for c in cs]);ax[0].set(xlabel='Copies per key (80 cells, 15 runs per setting)',ylabel='Mean final aggregation, H / 80',title='Historical sequential-model replay');ax[0].legend(fontsize=8,loc='upper left');ax[0].grid(alpha=.2)
vals=[f['full30_vs_consensus']['median_model'],f['full30_vs_nearest']['median_nearest'],f['thompson7_vs_consensus']['median_model'],f['full30_vs_consensus']['median_baseline']];names=['Full 30-D','Nearest relative','Thompson 7-mode','Consensus'];ax[1].barh(names,vals,color=['#1769aa','#709abb','#318248','#888']);ax[1].invert_yaxis();ax[1].set(xlabel='Median absolute error in body-depth / length',title='FishShapes: 1,122 species within 50 Myr');ax[1].set_xlim(0,.112)
for i,v in enumerate(vals):ax[1].text(v+.0015,i,f'{v:.5f}',va='center',fontsize=9)
ax[1].text(.02,-.24,'Full 30-D has 4.12% lower median error than nearest.\nIts preregistered advantage test fails at alpha = 0.01 (p = 0.06068).',transform=ax[1].transAxes,fontsize=8.7,va='top');ax[1].grid(axis='x',alpha=.2)
fig.suptitle('Levin / Dietz / Sweet audit: reproduced values and interpretation boundaries',fontsize=12)
fig.savefig(ROOT/'results/audit_summary.png',dpi=180,bbox_inches='tight');fig.savefig(ROOT/'results/audit_summary.svg',bbox_inches='tight');plt.close(fig)
