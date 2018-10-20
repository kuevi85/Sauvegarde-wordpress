#!/usr/bin/python
# -*- coding: utf-8 -*-
# ====================================================
# TITLE           : Sauvegarde wordpress sur site distant
# DESCRIPTION     :
# - Sauvegarde de la bases de donnée présente sur le serveur
# - Sauvegarde de la bases de donnée sur serveur distant
# AUTHORS         : Jessy EKUE
# DATE            : 20/10/2018
#https://github.com/kuevi85
# ====================================================


import getopt, os, sys, subprocess
import time
from datetime import datetime
from time import strftime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
from subprocess import Popen, call, PIPE
from numpy import * 

current_dir = os.getcwd()                                   #Répertoire courant
d = datetime.now()                                          #Variable de la date
date = d.strftime("%d_%m_%Y")                               #Format de la date
WARNING_DISK = 5                                            #Espace en GO minimum avant WARNING sur l'espace disque restant

SRV_LOCAL = {
        'dir_wordpress' : '/var/www/*****',                  #Indiquer répertoire de wordpress
        'dir_to_backup' : '/******',         #Indiquer un répértoire de backup
        'db_username' : '**********',                    #Nom de l'utilisateur de la BDD wordpress
        'db_name' : '*********',                            #Nom de la BDD wordpress
        'db_password' : '******',                           #Mot de passe de la BDD 
    }

SRV_DISTANT = {
        'dir' : '*********',                    #Chemin du répertoire de backup sur serveur distant
        'server' : '********',                        #Adresse du serveur distant
        'port' : '*****',                                      #Port de connexion SSH
        'login' : '********',                                  #Nom d'utilisateur
    }

#Réinitialisation des fichiers de log

os.system("echo ' ' > "+current_dir+"/Script_log.log")      #Fichier de log du script dans répertoire courant
os.system("echo ' ' > "+current_dir+"/disk_space.txt")      #Fichier info espace disque du serveur distant

#Création du fichier de log

logging.basicConfig(filename='Script_log.log',level=logging.DEBUG,\
      format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')




#Récupération d'information sur serveur distant ( tailles des disques) 
try:

    process = Popen(['ssh', '-t', SRV_DISTANT['login']+'@'+SRV_DISTANT['server'],'df','-h'], bufsize=4096, stdout=PIPE)
    output = process.communicate()[0]
    disk_space = open(current_dir+'disk_space.txt', 'a')
    disk_space.write(output)
    disk_space.close()

    if output != False:
        logging.info('Connection SSH ok')

except BaseException as e:
        logging.error(str(e))
        logging.error('Problème au niveau de la connexion SSH!!')

try:

    disksize = open(current_dir+'disk_space.txt', 'r')
    tab=[]
#boucle de création du tableau, extraction de donnée, et conversion en int
    for ligne in disksize:
        tab.append(ligne.split())
    disksize.close()

    tab = array(tab)
    print tab.ravel()[0:1]
    for x in tab.ravel()[0:1]:
        print type(x)

    tab = tab[1][3]
    longue= len(tab)
    print (tab)
    print(longue)
    int_disk =int(tab[0:longue-1])



    if (int(int_disk) < WARNING_DISK):
        logging.warning('Warning Error : Erreur disk space')
    else:
        logging.info('Espace disque pour la sauvegarde %sG: ok' % int_disk)

except BaseException as e:
        logging.error(str(e))
        logging.error('Problème au niveau del"extraction des données taille de disque  !!')

#Vérification des chemins 
try:

    if not os.path.exists(SRV_LOCAL['dir_wordpress']):
        print("\nERREUR: Le répértoire cible \n>> "+SRV_LOCAL[production]['dir_wordpress']+" << \nn'est pas valide!!\n\n")

 
    if not os.path.exists(SRV_LOCAL['dir_to_backup']):
        os.system('mkdir -rf %s',  (SRV_LOCAL['dir_to_backup']))


except BaseException as e:
    logging.error(str(e))
    logging.error('Problème au niveau des répertoires cibles!!')

#Sauvegarde de la base de donnée & dossier en local

try:    
    os.system('mysqldump -u '+SRV_LOCAL['db_username']+' -p'+SRV_LOCAL['db_password']+' -d '+SRV_LOCAL['db_name']+' > '+SRV_LOCAL['dir_to_backup']+'/db_wordpress_backup_'+date+'.sql')
    os.system('mysqldump -u '+SRV_LOCAL['db_username']+' -p'+SRV_LOCAL['db_password']+' -d '+SRV_LOCAL['db_name']+' > '+SRV_LOCAL['dir_to_backup']+'/db_wordpress_backup_Update.sql')
    logging.info('Dump base de donnée realisés : ok ')

except BaseException as e:
    logging.error(str(e))
        logging.error('Le Dump de la base de donnée à échoué')
    
try:
    os.system('tar -cvzf '+SRV_LOCAL['dir_to_backup']+'/wordpress_'+date+'.tar.gz '+SRV_LOCAL['dir_wordpress'])
    os.system('tar -cvzf '+SRV_LOCAL['dir_to_backup']+'/wordpress_save_Update.tar.gz '+SRV_LOCAL['dir_wordpress'])
    logging.info('La sauvegarde du dossier wordpress :  ok')

except BaseException as e:
    logging.error(str(e))
        logging.error('La sauvegarde du du site wordpress a échoué')

#Sauvegarde incrementiel BDD & Dossier wordpress sur serveur distant
try:
    
    os.system('rsync -avrz '+SRV_LOCAL['dir_to_backup']+' '+SRV_DISTANT['login']+'@'+SRV_DISTANT['server']+':'+SRV_DISTANT['dir']+'/')
    logging.info('La sauvegarde incrémentiel du dossier wordpress & de la base sql a bien été effectuée :  ok')
    print("### sauvegarde effectuée.") 

except BaseException as e:
    logging.error(str(e))
        logging.error('La sauvegarde incrémentiel sur le serveur distant du site wordpress a échoué')







#Envoie d'un email des logs
    
body = open(current_dir+"/Script_log.log", "r")
lecture = body.read()

msg = MIMEMultipart()
msg['From'] = '********@gmail.com'
msg['To'] = '*********@gmail.com'
msg['Subject'] = 'Rapport de Sauvegarde' 
message = str(lecture)  
msg.attach(MIMEText(message))

filename = "Script_log.log"
attachment = open(current_dir+"/Script_log.log", "rb")

part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

mailserver = smtplib.SMTP('smtp.gmail.com', 587)
mailserver.ehlo()
mailserver.starttls()
mailserver.ehlo()
mailserver.login('*******@gmail.com', '********')
mailserver.sendmail('******@gmail.com', '******@gmail.com', msg.as_string())
mailserver.quit()

       