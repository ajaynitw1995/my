import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from scipy.integrate import quad
from scipy.special import dawsn
from pathlib import Path
import csv

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'figures_generated'
OUT.mkdir(exist_ok=True)
DATA=ROOT/'source_data'

def read_rows(name):
    with open(DATA/name, newline='') as f:
        return list(csv.DictReader(f))

plt.rcParams.update({
    'font.size': 8,
    'axes.titlesize': 9,
    'axes.labelsize': 8,
    'legend.fontsize': 7,
    'xtick.labelsize': 7,
    'ytick.labelsize': 7,
    'figure.dpi': 160,
    'savefig.dpi': 300,
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
})

def panel(ax, label):
    ax.text(-0.14, 1.06, label, transform=ax.transAxes, fontweight='bold', fontsize=10, va='top')

def save(fig, name):
    fig.tight_layout(pad=1.0, w_pad=1.2, h_pad=1.2)
    fig.savefig(OUT/name, bbox_inches='tight')
    plt.close(fig)

# ---------------- Figure 1 ----------------
fig, axs = plt.subplots(2,3, figsize=(10.2,6.2))
ax=axs[0,0]; panel(ax,'a')
rho=0.02; t=np.linspace(0,1,700)
B=np.exp(-t/rho); I=1-t+t*np.exp(-1/rho)
ax.plot(t,B,'k-',lw=1.5,label='Exact layer')
ax.plot(t,I,'k--',lw=1.3,label='Nodal interpolant')
ax.scatter([0,1],[1,np.exp(-1/rho)],facecolors='white',edgecolors='k',s=25,zorder=3)
ax.set_xlabel('normalized distance into final cell'); ax.set_ylabel('field value')
ax.set_title(r'Canonical layer, $\varepsilon/h=0.02$'); ax.legend(frameon=False)

ax=axs[0,1]; panel(ax,'b')
rhos=np.logspace(-3,1,400)
a=rhos*(1-np.exp(-1/rhos)); err=1+a*np.log(a)-a
ax.semilogx(rhos,err,'k-',lw=1.5)
ax.axhline(.5,color='0.5',ls='--',lw=.8); ax.axhline(.9,color='0.5',ls=':',lw=.8)
ax.axvline(.188,color='0.65',ls='--',lw=.8); ax.axvline(.0205,color='0.65',ls=':',lw=.8)
ax.set_xlabel(r'layer-resolution ratio $\rho=\varepsilon/h$'); ax.set_ylabel(r'$\|I_hB_\varepsilon-B_\varepsilon\|_\infty$')
ax.set_ylim(0,1.03); ax.set_title('Exact maximum-error law')

ax=axs[0,2]; panel(ax,'c')
N=32; h=1/N
rr=np.logspace(-3,-0.2,35); rel=[]
for r in rr:
    eps=r*h
    xnodes=np.linspace(0,1,N+1); ynodes=np.exp(-(1-xnodes)/eps)
    xd=np.linspace(0,1,200001); yd=np.exp(-(1-xd)/eps); yi=np.interp(xd,xnodes,ynodes)
    num=np.trapezoid((yi-yd)**2,xd); den=eps/2*(1-np.exp(-2/eps))
    rel.append(np.sqrt(num/den))
rel=np.array(rel)
ax.loglog(rr,rel,'ko-',ms=2.5,lw=1,label='Numerical interpolation error')
ax.loglog(rr,np.sqrt(2/(3*rr)),'k--',lw=1.2,label=r'$\sqrt{2/(3\rho)}$')
ax.set_xlabel(r'$\rho=\varepsilon/h$'); ax.set_ylabel(r'relative $L^2$ error')
ax.set_title('Relative-error blow-up'); ax.legend(frameon=False)

ax=axs[1,0]; panel(ax,'d')
_r=read_rows('fig1_2d_resolution_benchmark.csv')
Pe=np.array([float(r['Pe']) for r in _r])
grid=np.array([float(r['grid_relL2_percent']) for r in _r])
cont=np.array([float(r['continuum_relL2_percent']) for r in _r])
ax.semilogx(Pe,grid,'ko-',lw=1.2,ms=4,label='Grid metric')
ax.semilogx(Pe,cont,'ks--',lw=1.2,ms=4,mfc='white',label='Continuum-resolved')
ax.set_xlabel('Peclet number'); ax.set_ylabel(r'mean relative $L^2$ error (%)')
ax.set_yscale('log'); ax.set_title('2D operator-learning stress test'); ax.legend(frameon=False)

ax=axs[1,1]; panel(ax,'e')
eps=1e-3; h=1/31; rho=eps/h
t=np.linspace(0,1,700); B=np.exp(-t/rho); I=1-t+t*np.exp(-1/rho)
ax.plot(1-t*h,B,'k-',lw=1.5,label='Continuum layer')
ax.plot(1-t*h,I,'k--',lw=1.3,label='32-point reconstruction')
ax.scatter([1,1-h],[1,np.exp(-h/eps)],facecolors='white',edgecolors='k',s=25,zorder=3)
ax.set_xlim(1-h,1); ax.set_xlabel('x in final grid cell'); ax.set_ylabel('normalized mode amplitude')
ax.set_title(r'$Pe=1000$ normalized outflow cross-section'); ax.legend(frameon=False)

ax=axs[1,2]; panel(ax,'f'); ax.axis('off')
box=FancyBboxPatch((.08,.18),.84,.62,boxstyle='round,pad=0.03',ec='k',fc='white',lw=1.1,transform=ax.transAxes)
ax.add_patch(box)
ax.text(.5,.63,'Same sampled values',ha='center',va='center',transform=ax.transAxes,fontweight='bold')
ax.text(.5,.48,r'$\Downarrow$',ha='center',va='center',transform=ax.transAxes,fontsize=16)
ax.text(.5,.36,'different continuous error\nwhen the physical scale is subgrid',ha='center',va='center',transform=ax.transAxes)
ax.set_title('Resolution-blind validation')
save(fig,'Figure1_Resolution_Blindness.pdf')

# ---------------- Figure 2 ----------------
fig, axs = plt.subplots(2,2,figsize=(8.6,6.2))
ax=axs[0,0]; panel(ax,'a')
eps=np.array([1e-3,1e-4,1e-5,1e-6])
ax.semilogx(eps,np.ones_like(eps),'k-',lw=1.5)
ax.scatter(eps,np.ones_like(eps),c='white',edgecolors='k',s=30,zorder=3)
ax.set_ylim(0,1.18); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'reaction-diffusion stability factor $K$')
ax.set_title('Uniform coercive certificate')
_s={r['metric']:float(r['value']) for r in read_rows('fig2_certificate_summary.csv')}
ax.text(.05,.14,f"{int(_s['reaction_blind_cases_certified'])}/{int(_s['reaction_total_blind_cases'])} blind cases certified\nmax. effectivity at $10^{{-6}}$: {_s['reaction_max_effectivity_eps_1e-6']:.4f}",transform=ax.transAxes,fontsize=7)

ax=axs[0,1]; panel(ax,'b')
vals=[85,100]; labels=['all blind\ncases','cases with\n$\\varepsilon\\leq10^{-4}$']
ax.bar(np.arange(2),vals,color=['white','0.8'],edgecolor='k',hatch=['//','..'],width=.58)
ax.set_xticks(np.arange(2),labels); ax.set_ylabel('raw residual-certificate violations (%)'); ax.set_ylim(0,108)
ax.set_title('Turning-point residual failure')
ax.text(0,vals[0]+2,f"{int(_s['turning_raw_violations_all'])}/{int(_s['turning_total_cases_all'])}",ha='center',va='bottom')
ax.text(1,min(104,vals[1]+2),f"{int(_s['turning_raw_violations_eps_le_1e-4'])}/{int(_s['turning_total_cases_eps_le_1e-4'])}",ha='center',va='bottom')

ax=axs[1,0]; panel(ax,'c')
_k=read_rows('fig2_turning_stability_factor.csv')
epss=np.array([float(r['epsilon']) for r in _k])
Ks=np.array([float(r['K_exact']) for r in _k]); x=.5*np.log(1/epss)
coef=np.polyfit(x,Ks,1)
ax.semilogx(epss,Ks,'ko',ms=4,label='Exact inverse factor')
ax.semilogx(epss,np.polyval(coef,x),'k--',lw=1.2,label=f'fit slope = {coef[0]:.3f}')
ax.invert_xaxis(); ax.set_xlabel(r'$\varepsilon$'); ax.set_ylabel(r'$K_{\varepsilon,1/2}$')
ax.set_title('Logarithmic inverse instability'); ax.legend(frameon=False)

ax=axs[1,1]; panel(ax,'d')
vals=[_s['turning_worst_true_over_raw_residual'],_s['turning_worst_true_over_stability_certificate']]
names=['raw residual','stability-aware\ncertificate']
ax.bar(np.arange(2),vals,color=['white','0.75'],edgecolor='k',hatch=['//','..'],width=.58)
ax.axhline(1,color='k',ls='--',lw=1,label='validity threshold')
ax.set_xticks(np.arange(2),names); ax.set_ylabel(r'worst $\|e\|_\infty$/certificate'); ax.set_ylim(0,2.25)
ax.set_title('Certification restored'); ax.legend(frameon=False,loc='upper right')
save(fig,'Figure2_Operator_Stability.pdf')

# ---------------- Figure 3 ----------------
fig, axs=plt.subplots(2,2,figsize=(9.0,6.4))
ax=axs[0,0]; panel(ax,'a'); ax.axis('off'); ax.set_title('Reliability-aware fallback')
labels=['Global\nsurrogate','Coarse inverse\n$A_Hz_H=r_H$','Local FEM on\nhigh-risk patch','20-step residual\nsmoothing','Discrete\ncertificate']
xs=np.array([.12,.31,.50,.69,.88])
for i,(x0,lab) in enumerate(zip(xs,labels)):
    w=.15; hbox=.22
    p=FancyBboxPatch((x0-w/2,.39),w,hbox,boxstyle='round,pad=0.015',ec='k',fc='white',lw=1,transform=ax.transAxes)
    ax.add_patch(p); ax.text(x0,.50,lab,ha='center',va='center',transform=ax.transAxes,fontsize=7)
    if i<len(labels)-1:
        arr=FancyArrowPatch((x0+w/2,.50),(xs[i+1]-w/2,.50),arrowstyle='-|>',mutation_scale=9,lw=1,color='k',transform=ax.transAxes)
        ax.add_patch(arr)

_h=read_rows('fig3_hybrid_summary.csv')
Pe=np.array([float(r['Pe']) for r in _h])
active=np.array([float(r['active_area_percent']) for r in _h])
energy=np.array([float(r['captured_error_energy_percent']) for r in _h])
hit=np.array([float(r['max_error_hit_percent']) for r in _h])
ax=axs[0,1]; panel(ax,'b')
ax.plot(Pe,active,'ko-',label='active area (%)')
ax.plot(Pe,energy,'ks--',mfc='white',label='captured error energy (%)')
for x0,y0,h0 in zip(Pe,energy,hit): ax.text(x0,y0+2,f'hit {h0:.0f}%',ha='center',fontsize=6.5)
ax.set_xlabel('Peclet number'); ax.set_ylabel('percent'); ax.set_ylim(0,100); ax.set_title('Sparse localization'); ax.legend(frameon=False)

pred=np.array([float(r['prediction_relL2_percent']) for r in _h])
local=np.array([float(r['local_relL2_percent']) for r in _h])
gmres=np.array([float(r['gmres20_relL2_percent']) for r in _h])
final=np.array([float(r['final_relL2_percent']) for r in _h])
ax=axs[1,0]; panel(ax,'c')
x=np.arange(3); w=.19
for offs,data,lab,hatch,shade in [(-1.5*w,pred,'prediction','',1),(-.5*w,local,'local FEM','//',.92),(.5*w,gmres,'GMRES-20','..',.82),(1.5*w,final,'hybrid','xx',.7)]:
    ax.bar(x+offs,data,width=w,label=lab,edgecolor='k',facecolor=str(shade),hatch=hatch)
ax.set_xticks(x,[str(v) for v in Pe]); ax.set_xlabel('Peclet number'); ax.set_ylabel(r'mean relative $L^2$ error (%)')
ax.set_title('Complementary correction stages'); ax.legend(frameon=False,ncol=2)

cert=np.array([float(r['certificate_ratio_max']) for r in _h])
ax=axs[1,1]; panel(ax,'d')
ax.plot(Pe,cert,'ko-',lw=1.3); ax.axhline(1,color='k',ls='--',lw=1,label='certificate bound')
ax.fill_between(Pe,0,cert,color='0.9')
ax.set_xlabel('Peclet number'); ax.set_ylabel('max. error/certificate ratio'); ax.set_ylim(0,1.1)
ax.set_title('All 75 blind cases certified'); ax.legend(frameon=False)
save(fig,'Figure3_Selective_Correction.pdf')

# ---------------- Figure 4 ----------------
fig, axs=plt.subplots(2,2,figsize=(9.0,6.5))
_p=read_rows('fig4_physical_baselines.csv')
methods=[r['method'] for r in _p]
r1=np.array([float(r['Pe1000_relL2_percent']) for r in _p]); r2=np.array([float(r['Pe2000_relL2_percent']) for r in _p])
l1=np.array([float(r['Pe1000_Linf']) for r in _p]); l2=np.array([float(r['Pe2000_Linf']) for r in _p])
ax=axs[0,0]; panel(ax,'a'); y=np.arange(len(methods)); hh=.34
ax.barh(y+hh/2,r1,height=hh,facecolor='white',edgecolor='k',hatch='//',label='$Pe=1000$')
ax.barh(y-hh/2,r2,height=hh,facecolor='.75',edgecolor='k',hatch='..',label='$Pe=2000$')
ax.set_yticks(y,methods); ax.invert_yaxis(); ax.set_xlabel(r'mean relative $L^2$ error (%)')
ax.set_title('Blind fine-mesh comparison'); ax.legend(frameon=False)

ax=axs[0,1]; panel(ax,'b'); x=np.arange(2); w=.34
mi=methods.index('Mesh-native'); hi=methods.index('Hybrid'); mesh=[r1[mi],r2[mi]]; hybr=[r1[hi],r2[hi]]
ax.bar(x-w/2,mesh,width=w,facecolor='white',edgecolor='k',hatch='//',label='Mesh-native')
ax.bar(x+w/2,hybr,width=w,facecolor='.75',edgecolor='k',hatch='..',label='Certified hybrid')
ax.set_xticks(x,['1000','2000']); ax.set_xlabel('Peclet number'); ax.set_ylabel(r'mean relative $L^2$ error (%)')
ax.set_title('Selective correction'); ax.legend(frameon=False)
for xi,a0,b0 in zip(x,mesh,hybr): ax.text(xi,max(a0,b0)+.5,f'{100*(a0-b0)/a0:.1f}% reduction',ha='center',fontsize=6.5)

ax=axs[1,0]; panel(ax,'c')
mesh_l=[l1[mi],l2[mi]]; hybr_l=[l1[hi],l2[hi]]
ax.bar(x-w/2,mesh_l,width=w,facecolor='white',edgecolor='k',hatch='//',label='Mesh-native')
ax.bar(x+w/2,hybr_l,width=w,facecolor='.75',edgecolor='k',hatch='..',label='Certified hybrid')
ax.set_xticks(x,['1000','2000']); ax.set_xlabel('Peclet number'); ax.set_ylabel(r'mean $L^\infty$ error')
ax.set_title('Maximum-error reduction'); ax.legend(frameon=False)

ax=axs[1,1]; panel(ax,'d')
_q=read_rows('fig4_router_summary.csv')
active=np.array([float(r['active_area_percent']) for r in _q])
energy=np.array([float(r['captured_error_energy_percent']) for r in _q])
cert=np.array([float(r['certificate_ratio_max']) for r in _q])
hit=np.array([float(r['max_error_hit_percent']) for r in _q])
ax.bar(x-w/2,active,width=w,facecolor='white',edgecolor='k',hatch='//',label='active area (%)')
ax.bar(x+w/2,energy,width=w,facecolor='.8',edgecolor='k',hatch='..',label='captured error energy (%)')
ax.set_xticks(x,['1000','2000']); ax.set_xlabel('Peclet number'); ax.set_ylabel('percent'); ax.set_ylim(0,100)
ax.set_title('Physical-benchmark router')
ax2=ax.twinx(); ax2.plot(x,cert,'ko--',lw=1.1,label='max certificate ratio'); ax2.set_ylabel('max error/certificate'); ax2.set_ylim(0,1.05)
for xi,e0,h0 in zip(x,energy,hit): ax.text(xi+w/2,e0+3,f'hit {h0:.0f}%',ha='center',fontsize=6.5)
lines,labs=ax.get_legend_handles_labels(); lines2,labs2=ax2.get_legend_handles_labels()
ax.legend(lines+lines2,labs+labs2,frameon=False,loc='upper left',fontsize=6.5)
save(fig,'Figure4_Physical_Heated_Cylinder_v2.pdf')

print('Generated main figures from source_data in',OUT)
