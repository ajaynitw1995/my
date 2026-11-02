from pathlib import Path
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'figures_generated'
DATA=ROOT/'source_data'
OUT.mkdir(parents=True, exist_ok=True)

def read_rows(name):
    with open(DATA/name, newline='') as f:
        return list(csv.DictReader(f))

plt.rcParams.update({
    'font.size': 9,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'legend.fontsize': 8,
    'xtick.labelsize': 8,
    'ytick.labelsize': 8,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

styles = [
    dict(color='black', marker='o', linestyle='-'),
    dict(color='0.25', marker='s', linestyle='--'),
    dict(color='0.5', marker='^', linestyle='-.'),
    dict(color='0.7', marker='D', linestyle=':'),
]

def panel_label(ax, label):
    ax.text(-0.14, 1.04, label, transform=ax.transAxes, fontsize=10, fontweight='bold', va='top')

def save(fig, n):
    fig.tight_layout()
    for ext in ('pdf','png'):
        fig.savefig(OUT / f'Supplementary_Figure_{n}.{ext}', dpi=300, bbox_inches='tight')
    plt.close(fig)

# Figure 1: Benchmark A
fig, axes = plt.subplots(1,2, figsize=(7.2,3.0))
_a=read_rows('supp1_benchmark_A.csv')
eps=np.array([float(r['epsilon']) for r in _a])
uniform=np.array([float(r['uniform_N128_max_error']) for r in _a])
shish=np.array([float(r['shishkin_N128_max_error']) for r in _a])
ax=axes[0]
ax.semilogx(eps,uniform,label='Uniform mesh',**styles[0])
ax.semilogx(eps,shish,label='Shishkin mesh',**styles[1])
ax.invert_xaxis(); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'maximum error')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'a')
_a2=[r for r in _a if r['FNO_layer_Linf']!='']
eps2=np.array([float(r['epsilon']) for r in _a2])
fno=np.array([float(r['FNO_layer_Linf']) for r in _a2])
deep=np.array([float(r['DeepONet_layer_Linf']) for r in _a2])
lift=np.array([float(r['LayerLift_layer_Linf']) for r in _a2])
ax=axes[1]
for y,lab,st in [(fno,'FNO',styles[0]),(deep,'DeepONet',styles[1]),(lift,'Layer-lift diagnostic',styles[2])]:
    ax.semilogx(eps2,y,label=lab,**st)
ax.invert_xaxis(); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'layer-region $L^\infty$ error')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'b')
save(fig,1)

# Figure 2: Benchmark B
_b=read_rows('supp2_benchmark_B.csv')
epsb=np.array([float(r['epsilon']) for r in _b])
flag=np.array([float(r['active_interval_percent']) for r in _b])
energy=np.array([float(r['error_energy_covered_percent']) for r in _b])
before=np.array([float(r['Linf_before']) for r in _b])
after=np.array([float(r['Linf_after']) for r in _b])
fig,axes=plt.subplots(1,2,figsize=(7.2,3.0))
ax=axes[0]
ax.semilogx(epsb,flag,label='Active interval',**styles[0])
ax.semilogx(epsb,energy,label='Error energy covered',**styles[1])
ax.invert_xaxis(); ax.set_ylim(0,100); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel('percentage')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'a')
ax=axes[1]
ax.semilogx(epsb,before,label='Before correction',**styles[0])
ax.semilogx(epsb,after,label='After correction',**styles[1])
ax.invert_xaxis(); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'mean $L^\infty$ error')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'b')
save(fig,2)

# Figure 3: Benchmark C turning point
_c=read_rows('supp3_turning_point.csv')
k_eps=np.array([float(r['epsilon']) for r in _c]); K=np.array([float(r['K_stability']) for r in _c])
_c2=[r for r in _c if r['Linf_before']!='']
ceps=np.array([float(r['epsilon']) for r in _c2])
cbefore=np.array([float(r['Linf_before']) for r in _c2])
cafter=np.array([float(r['Linf_after']) for r in _c2])
active=np.array([float(r['active_interval_percent']) for r in _c2])
raw_ratio=np.array([float(r['worst_raw_ratio']) for r in _c2])
fig,axes=plt.subplots(2,2,figsize=(7.2,5.5))
ax=axes[0,0]; ax.semilogx(k_eps,K,**styles[0]); ax.invert_xaxis()
ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'$K_{\varepsilon,\xi}$'); ax.grid(alpha=.2); panel_label(ax,'a')
ax=axes[0,1]
ax.semilogx(ceps,cbefore,label='Before',**styles[0])
ax.semilogx(ceps,cafter,label='After structure-aware correction',**styles[1])
ax.invert_xaxis(); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'mean $L^\infty$ error'); ax.set_yscale('log')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'b')
ax=axes[1,0]; ax.semilogx(ceps,active,**styles[0]); ax.invert_xaxis()
ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel('active interval (%)'); ax.grid(alpha=.2); panel_label(ax,'c')
ax=axes[1,1]; ax.semilogx(ceps,raw_ratio,**styles[0]); ax.axhline(1,color='0.5',linestyle='--',linewidth=1); ax.invert_xaxis()
ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'worst $\|e\|_\infty/\|r\|_\infty$'); ax.grid(alpha=.2); panel_label(ax,'d')
save(fig,3)

# Figure 4: 2D resolution blindness
_d=read_rows('supp4_benchmark_D.csv')
Pe=np.array([float(r['Pe']) for r in _d])
grid=np.array([float(r['grid_relL2_percent']) for r in _d])
resolved=np.array([float(r['resolved_relL2_percent']) for r in _d])
linf_before=np.array([float(r['resolved_Linf_before']) for r in _d])
linf_after=np.array([float(r['resolved_Linf_after']) for r in _d])
fig,axes=plt.subplots(1,2,figsize=(7.2,3.0))
ax=axes[0]
ax.loglog(Pe,grid,label='Grid-level relative $L^2$',**styles[0])
ax.loglog(Pe,resolved,label='Continuum-resolved relative $L^2$',**styles[1])
ax.set_xlabel('Peclet number'); ax.set_ylabel('relative error (%)'); ax.legend(frameon=False); ax.grid(alpha=.2,which='both'); panel_label(ax,'a')
ax=axes[1]
ax.semilogx(Pe,linf_before,label='Before correction',**styles[0])
ax.semilogx(Pe,linf_after,label='After correction',**styles[1])
ax.set_xlabel('Peclet number'); ax.set_ylabel(r'continuum-resolved $L^\infty$ error')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'b')
save(fig,4)

# Figure 5: curved obstacle representation bottleneck
_e=read_rows('supp5_curved_obstacle.csv')
Pe5=np.array([float(r['Pe']) for r in _e])
r2b=np.array([float(r['relL2_before_percent']) for r in _e])
r2a=np.array([float(r['relL2_after_percent']) for r in _e])
lib=np.array([float(r['Linf_before']) for r in _e])
lia=np.array([float(r['Linf_after']) for r in _e])
fig,axes=plt.subplots(1,3,figsize=(8.2,2.8))
ax=axes[0]
ax.add_patch(Rectangle((0,0),1,1,fill=False,color='black'))
ax.add_patch(Circle((0.72,0.5),0.15,fill=False,color='black',linewidth=1.5))
ax.arrow(0.08,0.5,0.22,0,width=.005,head_width=.04,head_length=.04,color='black',length_includes_head=True)
ax.text(.08,.56,'advection'); ax.set_xlim(-.03,1.03); ax.set_ylim(-.03,1.03); ax.set_aspect('equal')
ax.set_xticks([0,.5,1]); ax.set_yticks([0,.5,1]); ax.set_xlabel('$x$'); ax.set_ylabel('$y$'); panel_label(ax,'a')
ax=axes[1]
ax.plot(Pe5,r2b,label='Before',**styles[0]); ax.plot(Pe5,r2a,label='After local correction',**styles[1])
ax.set_xlabel('Peclet number'); ax.set_ylabel('relative $L^2$ error (%)'); ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'b')
ax=axes[2]
ax.plot(Pe5,lib,label='Before',**styles[0]); ax.plot(Pe5,lia,label='After local correction',**styles[1])
ax.set_xlabel('Peclet number'); ax.set_ylabel(r'$L^\infty$ error'); ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'c')
save(fig,5)

# Figure 6: negative routing results
_f=read_rows('supp6_negative_routing.csv')
Pe6=np.array([float(r['Pe']) for r in _f])
base=np.array([float(r['baseline_coordinate_relL2_percent']) for r in _f])
fine=np.array([float(r['continuum_finetuned_relL2_percent']) for r in _f])
_f2=[r for r in _f if r['sparse_before_relL2_percent']!='']
Pe6b=np.array([float(r['Pe']) for r in _f2])
sparse_b=np.array([float(r['sparse_before_relL2_percent']) for r in _f2])
sparse_a=np.array([float(r['sparse_after_relL2_percent']) for r in _f2])
fig,axes=plt.subplots(1,2,figsize=(7.2,3.0))
ax=axes[0]
ax.semilogx(Pe6,base,label='Baseline coordinate surrogate',**styles[0])
ax.semilogx(Pe6,fine,label='Continuum-aware fine-tuned',**styles[1])
ax.set_xlabel('Peclet number'); ax.set_ylabel('basis mean relative $L^2$ error (%)')
ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'a')
ax=axes[1]; x=np.arange(2); w=.34
ax.bar(x-w/2,sparse_b,w,label='Before',facecolor='white',edgecolor='black',hatch='//')
ax.bar(x+w/2,sparse_a,w,label='After 14.5% sparse patch',facecolor='0.75',edgecolor='black',hatch='..')
ax.set_xticks(x,['1000','2000']); ax.set_xlabel('Peclet number'); ax.set_ylabel('relative $L^2$ error (%)')
ax.legend(frameon=False); panel_label(ax,'b')
save(fig,6)

# Figure 7: final hybrid ablations
_g=read_rows('supp7_hybrid_ablation.csv')
Pe7=np.array([float(r['Pe']) for r in _g])
pred=np.array([float(r['prediction_relL2_percent']) for r in _g])
local=np.array([float(r['local_relL2_percent']) for r in _g])
final=np.array([float(r['final_relL2_percent']) for r in _g])
pred_inf=np.array([float(r['prediction_Linf']) for r in _g])
local_inf=np.array([float(r['local_Linf']) for r in _g])
final_inf=np.array([float(r['final_Linf']) for r in _g])
active7=np.array([float(r['active_area_percent']) for r in _g])
energy7=np.array([float(r['captured_error_energy_percent']) for r in _g])
gm=np.array([float(r['gmres20_reduction_percent']) for r in _g])
hyb=np.array([float(r['hybrid_reduction_percent']) for r in _g])
cert=np.array([float(r['certificate_ratio_max']) for r in _g])
fig,axes=plt.subplots(2,2,figsize=(7.2,5.5))
ax=axes[0,0]
for y,lab,st in [(pred,'Prediction',styles[0]),(local,'Local FEM',styles[1]),(final,'Final hybrid',styles[2])]:
    ax.plot(Pe7,y,label=lab,**st)
ax.set_xlabel('Peclet number'); ax.set_ylabel('relative $L^2$ error (%)'); ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'a')
ax=axes[0,1]
for y,lab,st in [(pred_inf,'Prediction',styles[0]),(local_inf,'Local FEM',styles[1]),(final_inf,'Final hybrid',styles[2])]:
    ax.plot(Pe7,y,label=lab,**st)
ax.set_xlabel('Peclet number'); ax.set_ylabel(r'$L^\infty$ error'); ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'b')
ax=axes[1,0]
ax.plot(Pe7,active7,label='Active area',**styles[0]); ax.plot(Pe7,energy7,label='Initial error energy captured',**styles[1])
ax.set_ylim(0,100); ax.set_xlabel('Peclet number'); ax.set_ylabel('percentage'); ax.legend(frameon=False); ax.grid(alpha=.2); panel_label(ax,'c')
ax=axes[1,1]; x=np.arange(3); w=.34
ax.bar(x-w/2,gm,w,facecolor='white',edgecolor='black',hatch='//')
ax.bar(x+w/2,hyb,w,facecolor='0.75',edgecolor='black',hatch='..')
ax.plot(x,100*cert,'ko--')
ax.set_xticks(x,['500','1000','2000']); ax.set_xlabel('Peclet number'); ax.set_ylabel('reduction / ratio (%)'); panel_label(ax,'d')
save(fig,7)

# Figure 8: physical strong baselines including GINO reimplementation
_p=read_rows('fig4_physical_baselines.csv')
methods=[r['method'] for r in _p]
rel1000=np.array([float(r['Pe1000_relL2_percent']) for r in _p])
rel2000=np.array([float(r['Pe2000_relL2_percent']) for r in _p])
li1000=np.array([float(r['Pe1000_Linf']) for r in _p])
li2000=np.array([float(r['Pe2000_Linf']) for r in _p])
fig,axes=plt.subplots(1,2,figsize=(8.5,3.3)); x=np.arange(len(methods)); w=.36
ax=axes[0]
ax.bar(x-w/2,rel1000,w,label='Pe=1000',facecolor='white',edgecolor='black',hatch='//')
ax.bar(x+w/2,rel2000,w,label='Pe=2000',facecolor='0.75',edgecolor='black',hatch='..')
ax.set_xticks(x,methods,rotation=35,ha='right'); ax.set_ylabel('mean relative $L^2$ error (%)'); ax.legend(frameon=False); panel_label(ax,'a')
ax=axes[1]
ax.bar(x-w/2,li1000,w,label='Pe=1000',facecolor='white',edgecolor='black',hatch='//')
ax.bar(x+w/2,li2000,w,label='Pe=2000',facecolor='0.75',edgecolor='black',hatch='..')
ax.set_xticks(x,methods,rotation=35,ha='right'); ax.set_ylabel(r'mean $L^\infty$ error'); ax.legend(frameon=False); panel_label(ax,'b')
save(fig,8)

print(f'Generated figures in {OUT}')
