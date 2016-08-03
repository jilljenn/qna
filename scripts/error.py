import matplotlib.pyplot as plt

fig, ax = plt.subplots()
irt = [3, 4, 8, 6, 7]
ax.errorbar(range(1, len(irt) + 1), irt, yerr=[1, 0.5, 1, 0.5, 1], color='blue')
ax.set_title('Test barre d\'erreur')
plt.show()
