# ✝️ Intégration Daily Saint pour Home Assistant

[![HACS Badge](https://img.shields.io/badge/Disponible%20via-HACS-41BDF5?logo=home-assistant)](https://my.home-assistant.io/redirect/hacs_repository/?owner=pa-martin&repository=ha-dailysaint&category=integration)
[![Home Assistant](https://img.shields.io/badge/Home--Assistant-2026.7+-blue?logo=home-assistant)](https://www.home-assistant.io/blog/2026/07/01/release-20267/)

[![Licence MIT](https://img.shields.io/github/license/pa-martin/ha-dailysaint?label=Licence&logo=github)](https://github.com/pa-martin/ha-dailysaint/blob/main/LICENSE)
[![Latest Release](https://img.shields.io/github/v/release/pa-martin/ha-dailysaint?label=Version&logo=github)](https://github.com/pa-martin/ha-dailysaint/releases)
[![Last Commit](https://img.shields.io/github/last-commit/pa-martin/ha-dailysaint?label=Derni%C3%A8re%20mise%20%C3%A0%20jour&logo=github)](https://github.com/pa-martin/ha-dailysaint/commits/main)
[![GitHub Stars](https://img.shields.io/github/stars/pa-martin/ha-dailysaint?label=Favoris&style=social)](https://github.com/pa-martin/ha-dailysaint/stargazers)
<br>

Récupérez le saint du jour depuis un ou plusieurs fournisseurs dans Home Assistant.

Cette documentation est également disponible en :
- [Anglais - English](./README.md)

---

## 📦 Installation

### 1. Via HACS (recommandé)

> Nécessite HACS installé dans Home Assistant

1. Ouvrez **HACS**
2. Recherchez **Daily Saint**
3. Installez l’intégration, puis redémarrez Home Assistant

### 2. Manuel (sans HACS)

1. Téléchargez ce dépôt
2. Copiez le dossier `dailysaint` dans `config/custom_components/`
3. Redémarrez Home Assistant

---

## ⚙️ Configuration

1. Allez dans **Paramètres → Appareils et services → Ajouter une intégration**
2. Recherchez **Daily Saint**
3. Sélectionnez les fournisseurs à activer

Cette intégration autorise uniquement **une seule entrée de configuration**.
Vous pouvez modifier les fournisseurs activés ensuite via les options de l’intégration.

---

## 🌐 Fournisseurs pris en charge

- **Nominis** (`nominis.cef.fr`)
- **Fête du jour** (`fetedujour.fr`)

---

## 📊 Capteurs créés

Un capteur est créé pour chaque fournisseur activé.

Identifiants d’entités typiques :
- `sensor.nominis_saint_of_the_day`
- `sensor.fete_du_jour_saint_of_the_day`

État du capteur :
- **État** : nom du saint

Attributs du capteur :
- `attribution` : libellé du fournisseur
- `provider` : clé du fournisseur
- `description` : description du saint (si disponible)
- `link` : lien fournisseur (si disponible)
- `day`, `month`, `year` : champs de date du fournisseur (si disponibles)

---

## 🛠 Développement

Compatible avec Home Assistant `2026.7+`.
Consultez [DEV.md](./DEV.md) pour les détails de développement local.

Structure :
- `translations/*.json` : traductions de l’intégration
- `__init__.py` : chargement / déchargement de l’intégration
- `api.py` : client API des fournisseurs
- `config_flow.py` : assistant de configuration UI
- `const.py` : constantes
- `coordinator.py` : logique de polling et rafraîchissement
- `manifest.json` : métadonnées et dépendances
- `sensor.py` : entités capteur

---

## 👨‍💻 Auteur

Développé par [pa-martin](https://github.com/pa-martin)
Les contributions sont bienvenues via **Pull Requests** et **Issues**.

---

## 📄 Licence

Code open source sous licence **MIT**.
