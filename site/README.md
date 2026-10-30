# Site Fortezza.bj

Site statique (HTML/CSS/JS) + un script PHP pour les formulaires. Rapide en 3G/4G, hébergeable sur n'importe quel hébergement mutualisé PHP.

## Modifier le contenu
- Textes, coordonnées, téléphone, WhatsApp : `build.py` (bloc `CONFIG` en haut, puis `POLES` pour les services)
- Design : `public/assets/css/style.css`
- Photos sources : `src_img/` (converties en WebP par le script)
- Puis relancer : `python build.py`

## Aperçu local
    php -S localhost:8080 -t public

## Mise en ligne sur Netlify
1. Déposer le dossier `public/` (glisser-déposer sur app.netlify.com/drop, ou « Add new site » puis « Deploy manually »).
2. Formulaires : Netlify les détecte seul (Site configuration → Forms). Activer les emails dans *Forms → Form notifications → Add notification → Email* : devis@fortezza.bj pour le formulaire « devis », contact@fortezza.bj pour « contact ». (Offre gratuite : 100 envois/mois.)
3. Domaine : *Domain management → Add a domain* → fortezza.bj, puis suivre les instructions DNS. Le HTTPS est automatique.

Alternative hébergement PHP classique : `archive-php/` contient `send.php` et `.htaccess` (à remettre dans `public/` et à brancher dans les formulaires).
