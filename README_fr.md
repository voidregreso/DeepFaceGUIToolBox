# DeepFace GUI Toolbox



*Lisez-le dans d'autres langues: [Anglais](README.md), [Espagnol](README_es.md), [Français](README_fr.md), [Portugais du Brésil](README_pt-BR.md), [Arabe](README_ar.md), [Chinois Simplifié](README_zh-CN.md).*

### 1. Introduction

> Deepface est un cadre léger en Python pour la reconnaissance faciale et l'analyse des attributs faciaux (âge, sexe, émotion et race). Il s'agit d'un cadre hybride de reconnaissance des visages, enveloppé de modèles de pointe. VGG-Face, Google FaceNet, OpenFace, Facebook DeepFace, DeepID, ArcFace, Dlib et SFace.

Cependant, le projet initial ne comportait qu'un module API et un programme console d'exemple, qui n'étaient pas pratiques à utiliser et à exploiter ; de plus, comme les fichiers modèles correspondants devaient être téléchargés à partir d'Internet pour reconnaître les traits du visage, et que ces fichiers sont très volumineux et que leurs URL dans certains pays (la Chine, l'Iran, le Venezuela, ...) sont bloqués, j'ai développé un programme avec une interface visuelle en utilisant Python+PyQt5. Il prend en charge les fonctionnalités suivantes : 

- Représenter les zones faciales reconnues au moyen de cases rectangulaires; 
- Effectuer une analyse complète de l'âge, du sexe, de la race et des émotions, l'analyse de la race et de l'expression pouvant être précise jusqu'au pourcentage de chaque résultat de reconnaissance possible;
- Vérifier si deux visages représentent la même personne, c'est-à-dire déduire la similarité avec le pourcentage;
- Options multiples pour les backends des détecteurs de visage et les modèles de vérification;
- Configuration du proxy pour accélérer le téléchargement des fichiers du modèle (actuellement, seul le protocole HTTP(S) est supporté, le proxy du protocole SOCKS doit encore être étudié et amélioré);
- Une interface utilisateur conviviale.

### 2. Utilisation

1. Téléchargez et installez Python 3.9;

2. Installez les paquets en utilisant les commandes suivantes:

   ```bash
   pip install deepface dlib configparser urllib3 PyQt5 PyQt5-tools
   ```

3. Lancez main.py

L'environnement d'exécution monofichier est également en cours d'empaquetage et sera publié dans des versions ultérieures.

Si vous souhaitez redessiner les fichiers d'interface utilisateur, vous devez régénérer les fichiers de code d'initialisation correspondants après les avoir édités à l'aide des commandes suivantes:

```bash
pyuic5 -o ventana.py ventana.ui
```

### 3. Exemple d'atouts de l'image faciale

J'ai mis les photos des visages des races correspondantes dans cinq dossiers: *asian, black, hispanic, india_arab, white*, où chaque dossier comporte environ 15 photos. Vous êtes libre de les utiliser à des fins d'analyse et de test.

### 4. Capture d'écran de l'interface

![](scrshot.jpg)
