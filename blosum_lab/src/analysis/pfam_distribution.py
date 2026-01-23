from data.stockholm_format import PFAM_SIZE
import matplotlib.pyplot as plt
from config import load_config

config =  load_config(is_test=False)

def extract_pfam_sizes(file_name: str) -> list[int]:
    sizes = []
    with open(file_name) as file:
        for line in file:
            if line.startswith(PFAM_SIZE):
                size = int(line.split()[-1])
                sizes.append(size)
    return sizes

sizes = extract_pfam_sizes(config.PFAM_PATH)



import numpy as np

sizes = np.array(sizes)
sizes.sort()

cdf = np.arange(1, len(sizes) + 1) / len(sizes)

plt.figure()
plt.plot(sizes, cdf)
plt.xscale("log")
plt.xlabel("Nombre de séquences par famille (log)")
plt.ylabel("Fraction cumulée de familles")
plt.title("Fraction cumulée des tailles de familles Pfam")
plt.grid(True)
plt.show()