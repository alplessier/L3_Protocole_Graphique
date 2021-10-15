#######################
# Alexis PLESSIER     #
# 2020-2021           #
# L3 Informatique UCA #
#######################


#Librairies
import os

import svgwrite as sw
import math
import time

import numpy as np
from PIL import Image, ImageDraw
from resizeimage import resizeimage


#Création du SVG
dwg = sw.Drawing('ResultatProtocoleGraphique.svg', profile='full')

#Centre du cercle
c = (650,310)


#Menu

choix = -1

#Avec les codes ASCII
while(choix <48 or choix >51):
   print("================== Menu ===================")
   print("0. Quitter le programme")
   print("1. Coder une information SANS image")
   print("2. Coder une information AVEC image")

   try:
      choix = ord((input("Choisir un numéro du Menu : ")))
   except TypeError:
      print("Ne rentrez qu'une valeur ! Réessayez ! ")
   except KeyboardInterrupt:
      print()
      exit()

#Choix 0
if(choix == 48):
   exit()

#Choix 2
if(choix == 50):

   #Gestion de l'ajout d'une image
   TAILLE = [100,100]

   while True:
      try:
         print()
         nomPhoto = input("Nom de la photo dans le dossier avec l'extension : ")
         img = Image.open(nomPhoto)
         break
      #Gestion nom du fichier introuvable
      except FileNotFoundError:
         print("Nom du fichier inconnu ou pas dans le dossier ! Reessayez !")
         print()

      #Gestion interruption du programme
      except KeyboardInterrupt:
         print()
         exit()


   #Met l'image en carré
   print()
   if img.size[0]>img.size[1]:
      ajust = img.size[1]
   else:
      ajust = img.size[0]

   img = resizeimage.resize_contain(img,(ajust,ajust))
   img.save('inter1.PNG')

   # Converti l'image en matrice RGB
   img1=Image.open('inter1.PNG').convert("RGB")
   npImage=np.array(img1) 
   h,w=img1.size


   # Creer un masque en cercle de la taille de l'image (redefini plus tot)
   alpha = Image.new('L', img1.size,0)
   draw = ImageDraw.Draw(alpha)
   draw.pieslice([0,0,h,w],0,360,fill=255)

   # Converti l'image en tableau 
   npAlpha=np.array(alpha)

   # Add alpha layer to RGB
   npImage=np.dstack((npImage,npAlpha))

   # Sauvegarde le tableau en image 
   Image.fromarray(npImage).save('inter2.PNG')

   #Redimensionne l'image
   img2 = Image.open('inter2.PNG')
   img2 = resizeimage.resize_thumbnail(img2, TAILLE)
   img2.save('final.PNG')




#Choix 1 ou 2 -> Code l'information
if(choix == 49 or choix == 50):

   #Ryon du cercle
   r = [200,250,300]

   chaine =''
   while(len(chaine) == 0 or len(chaine) >255):
      chaine = input("Entrez votre chaine de caractère (entre 1 et 255 caractères) : ")

   #Temps d'execution a titre indicatif
   start_time = time.time()

   #Mots de 8 bits
   nbMot = len(chaine)+1               #+1 pour coder la longueur,

   # Matrice char en ASCII 
   def ASCII(chaine):
      res = [nbMot-1]
      for ele in chaine:
         res.extend(ord(num) for num in ele)
      return res

   
   #Ajoute la redondance
   def ajoutRedondance(li):

      matFin = []

      for m in range(2):
         if len(li)%5 == 0:
            for j in range(int(len(li)/5)):
               R1 = 128
               R2 = 128

               for i in range(5):
                  matFin.append(li[5*j+i])
                  R1 += li[5*j+i]
                  R2 += li[5*j+i]*(i+1)

               matFin.append(R1-128)
               matFin.append(R2-128)

         else:
            for j in range(int(len(li)/5)):
               R1 = 128
               R2 = 128

               for i in range(5):
                  matFin.append(li[5*j+i])
                  R1 += li[5*j+i]
                  R2 += li[5*j+i]*(i+1)

               matFin.append(R1-128)
               matFin.append(R2-128)

            R1 = 128
            R2 = 128
            for k in range(len(li)%5,0,-1):

               matFin.append(li[len(li)-k])
               R1 += li[len(li)-k]
               R2 += li[len(li)-k]*(k+1)

            matFin.append(R1-128)
            matFin.append(R2-128)

      #Ajout octet signifiant la fin mis a 1 et graphiquement reconnaissable      
      matFin.append(127)

      return li+matFin

   #Int to bin 8 ou 16(pour les données de redondance) bits
   def decToBin8or16bits(n):
      if n<=127:
         return bin(n).replace("0b", "").zfill(8)
      else:
         return bin(n-128).replace("0b", "").zfill(16)

   #Transforme 16 bits en 2 fois 8 bits
   def change16To8(li):

      for i in range(len(li)):
         A = []
         B = []
         if len(li[i]) == 16:
            for j in range(8):
               A = li[i][:8]
               
            for j in range(8,16):
               B = li[i][-8:]

            li.insert(i+1,A)
            li.insert(i+2,B)
            del li[i]
            change16To8(li)

      return li

   #Matrice ASCII complète, Transforme les entiers en bits
   def remplaceDecEnBin(mat):
      for i in range(len(mat)):
         tmp = mat[i]
         mat[i] = decToBin8or16bits(tmp)
         mat[i] = mat[i][::-1]         #renverse les bits pour convenir à ma future fonction

      return mat

   #CONSTRUCTION GRAPHIQUE
   if nbMot <=85:
      radius = r[0]
   elif nbMot <=170:
      radius = r[1]
   elif nbMot <=256:
      radius = r[2]

   #Rayon du cercle du milieu
   radiusCercleMilieu = 70

   #Nb de mots Correcteurs
   if nbMot%5 == 0:
      nbMotsCorrecteur = int((nbMot/5))*4*2           #2 fois 2 octets correcteurs(codés sur 2 cotets) pour 5 octets de données (max 2033 octets, atteignable sur 10 bits) = 2*2*nbMots par paquets de 5 mots
   else:
      nbMotsCorrecteur = (((int(nbMot/5)+1)*4*2))

   #Nb mots totaux
   nbTotaux = len(change16To8(remplaceDecEnBin(ajoutRedondance(ASCII(chaine)))))        #Matrice de bits final

   if(nbTotaux %8 == 0):
      nbCercle = int(nbTotaux/8)
   else:
      nbCercle = int((nbTotaux)/8)+1

   #Decalage du à la calibration
   if (nbTotaux*8+nbCercle %64 == 0):
      nbCercle += int(nbCercle/64)
   elif((nbCercle*8)*8 - (nbTotaux*8+nbCercle)) <0 :
      nbCercle += int(nbCercle/64)+1

   distRadius = (radius-radiusCercleMilieu)/nbCercle

   #Création des cercles de tailles égales
   for i in range(nbCercle+1):
      dwg.add(dwg.circle(center=c,
         #Creer le nombre de cercle necessaire et les equilibre
         r=radius - distRadius*i, 
         stroke=sw.rgb(0, 0, 0, '%'),
         fill='white'))
      
   if int(int((nbMot*3)/8)) == 0:
         dwg.add(dwg.circle(center=c,
         #Creer le nombre de cercle necessaire et les equilibre
         r=radius - (radius-radiusCercleMilieu), 
         stroke=sw.rgb(0, 0, 0, '%'),
         fill='white'))

   #Construit toutes les lignes sauf les cercles
   for i in range(64):
      dwg.add(dwg.line(start = (c[0]+radiusCercleMilieu*(math.cos(math.radians((360/64)*i))),c[1]-radiusCercleMilieu*(math.sin(math.radians((360/64)*i)))),
   end = (c[0]+radius*(math.cos(math.radians((360/64)*i))),c[1]-radius*(math.sin(math.radians((360/64)*i)))),
      stroke=sw.rgb(10, 10, 16, '%')
      )
   )

   #Calcule les coordonnées de chaques cases nécessaire au codage de l'information
   def case(cercle):

      L = []
      A = []

      for i in range(64*cercle):
         L.append([0]*22)

      for i in range(64*cercle):
         A.append([0]*22)
      
      for m in range(cercle):
         for i in range(64):
            for j in range(11):

               L[i+m*64][j] = ((c[0]+((radiusCercleMilieu+(m*distRadius)))*math.sin(math.radians((5.625*i)+(j*0.5625))))),((c[1]-((radiusCercleMilieu+(m*distRadius)))*math.cos(math.radians((5.625*i)+(j*0.5625)))))

            for j in range(11,22):
               L[i+m*64][j] = ((c[0]+((radiusCercleMilieu+((m+1)*distRadius)))*math.sin(math.radians((5.625*i)+((j-11)*0.5625))))),((c[1]-((radiusCercleMilieu+((m+1)*distRadius)))*math.cos(math.radians((5.625*i)+((j-11)*0.5625)))))
      
      #inverse la fin des deux listes pour former une suite de coordonnes (un ensemble joint de points)
      for k in range(64*cercle):
         A[k] = L[k][22:10:-1]

      for k in range(64*cercle):
         for i in range(11):
            L[k].pop()

      for k in range(64*cercle):
         L[k] = L[k] + A[k]

      return L
   

   data = change16To8(remplaceDecEnBin(ajoutRedondance(ASCII(chaine))))

   print()
   print("========== INFORMATIONS ==========")
   print("Nb octets a coder: ")
   print(len(data))
   print("Nb bits coder: ")
   print((len(data))*8)           #Octets+longueurMessage*8


   final = case(nbCercle)

   #Si bit a 1 rempli de noir sinon de blanc ET si case%64 == 0, changement de couleur et décalage de l'information
   def rempliData(li):
      nbDecalage = 0
      for i in range(len(li)):
         for j in range(8):
            if ((i*8+j+nbDecalage)%64 == 0) and ((i*8+j+nbDecalage)%32 == 0):
               if(nbDecalage %2 == 0):
                  dwg.add(dwg.polyline(points=final[(i*8+j+nbDecalage)],stroke="blue",fill="blue"))
               else:
                  dwg.add(dwg.polyline(points=final[(i*8+j+nbDecalage)],stroke="green",fill="green"))

               nbDecalage += 1
            
            if i == len(li)-1:
               dwg.add(dwg.polyline(points=final[(i*8+j+nbDecalage)],stroke="red",fill="red"))

            elif li[i][j] == '1':
               dwg.add(dwg.polyline(points=final[(i*8+j+nbDecalage)],stroke="black",fill="black"))
            else:
               dwg.add(dwg.polyline(points=final[(i*8+j+nbDecalage)],stroke="white",fill="white"))
         
      #Rempli les cases non concernées en blanc
      for i in range(len(li)*8+nbCercle,(nbCercle*8*8),1):
         dwg.add(dwg.polyline(points=final[i],stroke="white",fill="white"))


   #Calibrage Milieu

   dwg.add(dwg.circle(center=c, r=radiusCercleMilieu-5.5, stroke='black', stroke_width=3.5,fill='white'))
   dwg.add(dwg.circle(center=c, r=radiusCercleMilieu-12.5, stroke='black', stroke_width=4.5,fill='white'))

   vide = [c]

   for i in range(90):
      vide.append(((c[0]+((radiusCercleMilieu-1)*math.sin(math.radians((i*0.5625))))),((c[1]-((radiusCercleMilieu-1)*math.cos(math.radians(i*0.5625)))))))

   dwg.add(dwg.polyline(points=vide,stroke="white",fill="white"))

   #Versionnage et calibrage

   if(radius == r[0]):
      dwg.add(dwg.circle(center=(c[0]-radius-100,c[1]-(radius/2)-50), r=25, stroke='black', stroke_width=3.5,fill='white'))
      dwg.add(dwg.circle(center=(c[0]-radius-100,c[1]+(radius/2)+50), r=25, stroke='black', stroke_width=3.5,fill='black'))
      dwg.add(dwg.circle(center=(c[0]+radius+100,c[1]), r=25, stroke='black', stroke_width=3.5,fill='white'))
   elif(radius == r[1]):
      dwg.add(dwg.circle(center=(c[0]-radius-100,c[1]-(radius/2)-50), r=25, stroke='black', stroke_width=3.5,fill='black'))
      dwg.add(dwg.circle(center=(c[0]-radius-100,c[1]+(radius/2)+50), r=25, stroke='black', stroke_width=3.5,fill='white'))
      dwg.add(dwg.circle(center=(c[0]+radius+100,c[1]), r=25, stroke='black', stroke_width=3.5,fill='white'))
   else:
      dwg.add(dwg.circle(center=(c[0]-radius-100,c[1]-(radius/2)-50), r=25, stroke='black', stroke_width=3.5,fill='white'))
      dwg.add(dwg.circle(center=(c[0]-radius-100,c[1]+(radius/2)+50), r=25, stroke='black', stroke_width=3.5,fill='white'))
      dwg.add(dwg.circle(center=(c[0]+radius+100,c[1]), r=25, stroke='black', stroke_width=3.5,fill='black'))

   #Execution
   rempliData(data)
   print("Temps d'execution : --- %s secondes ---" % (time.time() - start_time))

   if(choix == 50):
      #Ajout de l'image au centre
      dwg.add(dwg.image('final.PNG',insert=(c[0]-50,c[1]-50)))

dwg.save()
