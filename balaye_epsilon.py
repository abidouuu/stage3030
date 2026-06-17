import numpy as np
import matplotlib.pyplot as plt
import os
from simu import config
from tqdm import tqdm
from math import sqrt
from matplotlib.cm import Blues, Oranges

workdir = os.path.dirname(os.path.abspath(__file__))
datadir = os.path.join(workdir, "data/balaye_epsilon")
show=False

epsilons = np.linspace(-3, 3, 10000)
kappas = 10.0**np.arange(-2, 2)
Lambdas=10.0**np.arange(-3,1)


for Lambda_idx, Lambda in tqdm(enumerate(Lambdas), total=len(Lambdas), desc="Lamba", position=0) :
    cfg = config(datadir=datadir, simu_title="Lambda="+str(Lambda)+"_")
    cfg.Lambda=Lambda
    fig, (axB, axb) = plt.subplots(2, 1,figsize=(10, 10),sharex=True)

    blues = Blues(np.linspace(0.35, 0.95, len(kappas)))
    oranges = Oranges(np.linspace(0.35, 0.95, len(kappas)))

    first = True

    for kappa_idx, kappa in tqdm(enumerate(kappas),total=len(kappas),desc="kappa",position=1,leave=False):
        cfg.kappaeq = kappa
        B = []
        b = []
        B_landau = []
        b_landau = []

        for epsilon in tqdm(epsilons,desc="sigmaB",position=2,leave=False):
            cfg.epsiloneq = epsilon
            (B_eq, b_eq) = cfg.get_eq()[0]
            B.append(B_eq)
            b.append(b_eq)
            if epsilon > 0:
                B_landau.append(sqrt(epsilon / Lambda))
            else:
                B_landau.append(0)
            b_landau.append(1)

        label_kappa = rf"$\kappa={kappa:.1e}$"

        axB.plot(epsilons, B_landau,color='green',ls="--",lw=1.5,label="B_landau" if first else None)
        axB.plot(epsilons, B,color=blues[kappa_idx],lw=1.5,label=label_kappa)
        axb.plot(epsilons, b_landau,color='green',ls="--",lw=1.5,label="b_landau" if first else None)
        axb.plot(epsilons, b,color=oranges[kappa_idx],lw=1.5,label=label_kappa)

        first = False

    axB.set_ylabel("B")
    axB.grid(True)
    axB.legend(fontsize=8)

    axb.set_xlabel(r"$\varepsilon$")
    axb.set_ylabel("b")
    axb.grid(True)
    axb.legend(fontsize=8)

    fig.tight_layout()
    cfg.write_config_file()
    savefile_eps = os.path.join(cfg.folder, f"lambda={str(Lambda)}.eps")
    savefile_png = os.path.join(cfg.folder, f"lambda={str(Lambda)}.png")
    plt.savefig(savefile_eps)
    plt.savefig(savefile_png)
    if show : plt.show()
    plt.close(fig)