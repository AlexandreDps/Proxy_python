# Création d'un proxy en python

Dans ce projet, <code>proxy_entree</code> reçoit les requêtes http issues d'un navigateur configuré pour utiliser le proxy 'localhost' avec le port 9998. Lorsqu'il reçoit une requête, ce proxy chiffre la requête via le mécanisme de RSA puis l'envoi au <code>proxy_sortie</code> qui déchiffrera la requête grace à la clé privé du RSA associée. Il fera la requête à la place du navigateur et recevra une réponse qu'il va chiffrer. Il enverra la réponse chiffré au proxy source qui déchiffrera la réponse pour enfin l'afficher au client (le navigateur web ayant envoyé la requête http)


# Installation
* Ouvrez et lancez les fichiers <code>proxy_entree.py</code> et <code>proxy_sortie.py</code>
* Une fois que ces deux sockets sont en démarrés, vous pouvez accéder à des sites en http:// via internet en configurant le proxy ou vous pouvez éxécuter le fichier <code>client.py</code> qui permet d'afficher une moyenne de délai supplémentaire ajouté par le proxy. Cela tourne autour des 2 secondes.
* Les requêtes https ne sont pas supportées
