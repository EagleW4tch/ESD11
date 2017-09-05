# -*- coding: utf-8 -*-

#############################
# Title - Le jeu du Pendu
# Date - 04/09/2017
# Author - Rémi LIQUETE
#############################


############ FUNCTION ################

############ BODY ####################

from random import randrange

# Lecture du fichier de mots à trouver
dic = open("dico.txt", "r")
secretWord = dic.read().splitlines()
secretWord = secretWord[randrange(0,5)]
# Je décide de mettre chaque caractère du mot dans une liste afin de les compter pour la suite
secretList = list(secretWord)
secretList = set(secretList)
# Je créé 2 listes pour l'utilisateur
letterUsed = []
letterFound = []
# J'initialise les variables du jeu
life = 7
success = False

print "Bienvenu dans le jeu du pendu !!\n\n Le mot à trouver est déjà choisi, voici le nombre de caractère à trouver : "
for letter in secretWord:
	print("*"),

while(life > 0 and success == False):
	# On demande à l'utilisateur de saisir une lettre et on vérifie qu'il saisit bien une seule lettre, sinon on lui redemande
	alreadyUsed = True
	while(alreadyUsed == True):
		userLetter = raw_input("\nChoisissez une lettre : ")
		if(userLetter.isdigit()):
			print("Merci de choisir une lettre valide")
		# On vérifie aussi si la lettre a déjà été utilisée, sinon on l'accepte et on l'ajoute à la liste des lettres utilisées
		else:
			if(len(userLetter) == 1):
				if(userLetter.upper() in letterUsed):
					alreadyUsed = True
					print("Vous avez déjà utilisé cette lettre")
				else:
					alreadyUsed = False
					userLetter = userLetter.upper()
					letterUsed.append(userLetter)

	# On vérifie si la lettre est présente dans le mot mystère
	for i in secretWord:
		if(userLetter == i):
			letterFound.append(userLetter)
			found = True
			break
		else:
			found = False

	# On vérifie si l'utilisateur a gagné, sinon on affiche le nombre de vies restantes
	if(len(secretList) == len(letterFound)):
		print("Félicitation vous avez gagné !!")
		success = True
	else:
		if(found == False):
			life -= 1
			if(life == 0):
				print("Dommage, vous avez perdu :(")
			else:
				print("Il ne vous reste plus que %s vies" % life)
	
	# On affiche quoi qu'il arrive l'avancement de l'utilisateur
	for i in secretWord:
		if i in letterFound:
			print(i),
		else:
			print("*"),
