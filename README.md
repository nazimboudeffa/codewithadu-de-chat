# RAG Chat

Interface web pour interroger un RAG (Retrieval-Augmented Generation) alimenté par tes publications Facebook. Recherche TF-IDF sans IA, avec affichage des sources.

## Structure du projet

```
.
├── app.py               # Serveur Flask (interface web)
├── rag_posts.py          # Moteur RAG (indexation, recherche, CLI)
├── rag_index.pkl         # Index TF-IDF pré-construit
├── requirements.txt      # Dépendances Python
├── Dockerfile            # Image Docker pour le déploiement
├── .dockerignore
└── templates/
    └── index.html        # Interface de chat (HTML/CSS/JS)
```

## Prérequis

- Python 3.11+
- Un export JSON de tes posts Facebook (fichier `your_posts__check_ins__photos_and_videos_1.json`)

## Installation locale

```bash
git clone https://github.com/ton-user/codewithadu-de-chat.git
cd codewithadu-de-chat
pip install -r requirements.txt
```

## Construire l'index

Le fichier `rag_index.pkl` est déjà inclus, mais si tu veux le reconstruire à partir de ton propre export JSON :

```bash
python rag_posts.py build --json your_posts__check_ins__photos_and_videos_1.json
```

## Utilisation

### Interface web

```bash
python app.py
```

Ouvre `http://localhost:5000` dans ton navigateur.

### CLI

```bash
# Recherche simple (sans LLM)
python rag_posts.py ask "Qu'est-ce que j'ai posté sur la musique ?"

# Chat interactif dans le terminal
python rag_posts.py chat

# Statistiques sur tes publications
python rag_posts.py stats --json your_posts__check_ins__photos_and_videos_1.json

# Exporter une mémoire Markdown classée par thème
python rag_posts.py memory
```

### Commandes CLI disponibles

| Commande  | Description |
|-----------|-------------|
| `build`   | Construit l'index TF-IDF à partir du JSON |
| `ask`     | Pose une question (recherche + affichage des résultats) |
| `chat`    | Chat interactif dans le terminal |
| `stats`   | Statistiques détaillées (activité, types, thèmes LDA) |
| `memory`  | Export Markdown de tes posts classés par thème |

## Déploiement

### Avec Dokploy (recommandé)

1. Push le repo sur GitHub
2. Dans Dokploy, crée une **Application Docker**
3. Connecte le repo GitHub
4. Configure :
   - **Port** : `5000`
   - **Dockerfile** : détecté automatiquement
5. Déploie

L'index `rag_index.pkl` est inclus dans l'image Docker. Pour le mettre à jour sans reconstruire l'image, passe-le en volume Dokploy.

### Docker (manuel)

```bash
# Build
docker build -t rag-chat .

# Run
docker run -d -p 5000:5000 --name rag-chat rag-chat
```

### Docker Compose

```yaml
services:
  rag-chat:
    build: .
    ports:
      - "5000:5000"
    restart: unless-stopped
```

```bash
docker compose up -d
```

## Mettre à jour l'index

Si tu obtiens un nouvel export Facebook :

1. Remplace le fichier JSON à la racine du projet
2. Reconstruis l'index :
   ```bash
   python rag_posts.py build --json nouveau_export.json
   ```
3. Relance le serveur ou redéploie le conteneur
