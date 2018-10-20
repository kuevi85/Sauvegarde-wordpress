# Sauvegarde-wordpress
script en python pour sauvegarder wordpress sur un site distant

Personnaliser les champs avec des **** suivant :

SRV_LOCAL = {
        'dir_wordpress' : '/var/www/*****',                   #Indiquer répertoire de wordpress
        'dir_to_backup' : '/******',                          #Indiquer un répértoire de backup
        'db_username' : '**********',                         #Nom de l'utilisateur de la BDD wordpress
        'db_name' : '*********',                              #Nom de la BDD wordpress
        'db_password' : '******',                             #Mot de passe de la BDD 
    }

SRV_DISTANT = {
        'dir' : '*********',                                    #Chemin du répertoire de backup sur serveur distant
        'server' : '********',                                 #Adresse du serveur distant
        'port' : '*****',                                      #Port de connexion SSH
        'login' : '********',                                  #Nom d'utilisateur
    }
    
    
mailserver.login('*******@gmail.com', '********')               # Email et mot de passe de boite mail
