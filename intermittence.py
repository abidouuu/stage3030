#run des longues simulations (tfin~50k) pour les paramètres de charbonneau
#peut-être avoir comme balaye sigma, plusieurs courbes (différents couplages) selon les paramètres
#calculer les statistiques : fraction de temps passé en minimum; faire l'histogramme analogue à la table 2
#tracer les courbes de fraction en fonction de paramètres d'intérêt ?

import numpy as np
import matplotlib.pyplot as plt
import os
from simu import config
from tqdm import tqdm
from itertools import product

epsilons=[-0.1,-0.01, 0, 0.01, 0.1]
kappas=[0.01,0.1, 1]
Lambdas=[0.01,0.1]
inter_epsilon=False
workdir = os.path.dirname(os.path.abspath(__file__))
datadir=os.path.join(workdir, "data/intermittence")
params = list(product(epsilons, kappas, Lambdas))

def simu_intermittence():
    for idx, (epsilon, kappa, Lambda) in tqdm(
        enumerate(params),
        total=len(params),
        desc="Simulations",
        unit="sim"
    ):
        cfg=config(datadir=datadir, term='mid', epsiloneq=epsilon, 
                Lambda=Lambda,kappaeq=kappa, inter_epsilon=inter_epsilon,
                tfin=100000)
        data=cfg.run(save=True)
        cfg.write_config_file()
        minimas=cfg.stat_analysis(data)
        fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10, 10),sharex=True)

        first = True
        t=data[:,0]
        B=data[:,1]
        b=data[:,2]
        kappa=data[:,3]
        if inter_epsilon : epsilon=data[:,4]

        ax1.plot(t, B,color='blue',lw=1.5,label=r"$B(t)$")
        ax1.plot(t, b,color='orange',lw=1.5,label=r"$b(t)$")
        ax2.plot(t, kappa,color='red',lw=1.5,label=r"$\kappa(t)$")
        if inter_epsilon : ax2.plot(t, kappa,color='green',lw=1.5,label=r"$\varepsilon(t)$")
        ax1.set_ylabel("Magnetic Amplitudes")
        if inter_epsilon : ax2.set_ylabel("Stochastic parameters")
        else : ax2.set_ylabel("Coupling factor")
        ax1.grid(True)
        ax2.grid(True)
        ax1.legend(fontsize=8)
        ax2.legend(fontsize=8)

        fig.tight_layout()
        savefile_eps = os.path.join(cfg.folder, f"simu_{str(idx)}.eps")
        savefile_png = os.path.join(cfg.folder, f"simu_{str(idx)}.png")
        plt.savefig(savefile_eps)
        plt.savefig(savefile_png)
        plt.close(fig)

        cfg.write_stat_file(minimas)

simu_intermittence()