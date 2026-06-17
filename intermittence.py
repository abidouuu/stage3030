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

epsilons=[-0.01,-0.1]
kappas=[0.01,0.1, 1]
Lambdas=[0.01,0.1]
inter_epsilon=False
workdir = os.path.dirname(os.path.abspath(__file__))
datadir=os.path.join(workdir, "data/intermittence")
params = list(product(epsilons, kappas, Lambdas))

def simu_intermittence():
    for epsilon, kappa, Lambda in tqdm(
        params,
        total=len(params),
        desc="Simulations",
        unit="sim"
    ):
        cfg=config(datadir=datadir, term='mid', epsiloneq=epsilon, 
                Lambda=Lambda,kappaeq=kappa, inter_epsilon=inter_epsilon,
                tfin=10)
        cfg.thetaepsilon=1e-2
        cfg.thetakappa=1e-4
        cfg.deltaepsilon=1e-3
        cfg.deltakappa=1e-3
        data=cfg.run(save=True)
        cfg.write_config_file()
        minimas=cfg.stat_analysis(data)
        for type in ["Bb", "epsilon", "kappa"] if inter_epsilon else ["Bb","kappa"]: 
            cfg.plot_time(data, type=type, show=False, name=f"{type}.eps", minimas=minimas)
            cfg.plot_time(data, type=type, show=False, name=f"{type}.png", minimas=minimas)
        cfg.write_stat_file(minimas)

simu_intermittence()