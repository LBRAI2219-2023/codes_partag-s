# vanGenuchten.py - Lien entre le stock d'eau et MARSHAL

### Ce script python permet de mettre à jour le stock d'eau utilisé dans MARSHAL

#### Auteur : Mattias Van Eetvelt, Basile Delvoie

## 1. Principe 
MARSHAL prend comme input un fichier `soil.csv` qui décrit le potentiel matriciel du sol. Pour un certain type de sol et un certain potentiel matriciel on peut déterminer une valeur de $\theta$, le contenu en eau du sol via une courbe de rétention d'eau. En particulier, on considère ici le modèle de van Genuchten pour un sol limoneux. En faisant la moyenne des valeurs $\theta_{sup}$ et $\theta_{inf}$ on peut calculer le stock d'eau contenu dans un profil de sol et donc calculer le stock d'eau initial dans MARSHAL. 

Après le premier run de MARSHAL, il suffit de soustraire la valeur de transpiration calculée afin de déterminer le stock d'eau restant. Il suffit alors de faire le chemin inverse pour pouvoir calculer les valeurs de $\theta$ correspondante et mettre à jour les valeurs du potentiel matriciel $\Psi_m$ dans le fichier `soil.csv`.

### 1.1 Description des équations
On fait comme hypothèse que $\theta_{z=0}$ est constant et fixé à -15 000 hPa et que le contenu en eau évolue linéairement entre $z=0$ et $z=-40$, permettant de calculer une moyenne pour $\theta$. 

$$
\begin{split}
\Sum_S &= S_1 + S_2 +S_3 \qquad \text{avec} \qquad S_1 = \frac{\theta_1+\theta_2}{2}40 \qquad \text{et} \qquad S_2 = S_3
&= S_1 + 2S_2
&= \frac{\theta_1+\theta_2}{2}40 + 2(\theta_2 40)
\end{split}
$$

