# permet d'accéder aux fonctions du module pygame
import pygame
import sys
import button
import typeEnum
import os, inspect
import threading
import time
from random import randrange
from pygame.transform import scale


scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
scriptDIR  = os.path.dirname(scriptPATH)
images = os.path.join(scriptDIR,"images")
confetti = os.path.join(scriptDIR,"confetti-gif")
confetti_v2 = os.path.join(scriptDIR,"confetti-gif-v2")
fond = pygame.image.load(os.path.join(images, "background-table.jpg"))
verso_carte = pygame.image.load(os.path.join(images, "verso_carte.png"))
jeton_mise = pygame.image.load(os.path.join(images, "jeton_mise.png"))

pile_noire = pygame.image.load(os.path.join(images, "pile_noir.png"))
pile_verte = pygame.image.load(os.path.join(images, "pile_verte.png"))
pile_rouge = pygame.image.load(os.path.join(images, "pile_rouge.png"))
pile_bleue = pygame.image.load(os.path.join(images, "pile_bleue.png"))

pile_noire.set_colorkey(pile_noire.get_at((0,0)))
pile_verte.set_colorkey(pile_verte.get_at((0,0)))
pile_rouge.set_colorkey(pile_rouge.get_at((0,0)))
pile_bleue.set_colorkey(pile_bleue.get_at((0,0)))

confetti_gif = []
score_images = []

# initialisation de l'écran de jeu
pygame.init()
      
class ThreadLoadGIF (threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self)  
        
    def run(self):

      global confetti_gif
      global confetti_v2

      

      """
      for i in range(48):
        name = "confetti-29-"+str(i)+".png"
        conf_i = pygame.image.load(os.path.join(confetti, name))
        height,width = conf_i.get_size()
        for h in range(height):
          for w in range(width) :
            colors = conf_i.get_at((h, w))
            if(colors[0]+colors[1]+colors[2] > 252*3):
              colors[3] = 0
              conf_i.set_at((h,w), colors)
        pygame.image.save(conf_i, os.path.join(confetti, "confetti-new-"+str(i)+".png")) 
        confetti_gif.append(conf_i)
        print(i, " success")
      """

for i in range(31):
    if(i == 0) : i += 1
    name = "confetti-v2-"+str(i)+" (glissées).tiff"
    conf_i = pygame.image.load(os.path.join(confetti_v2, name))
    
    confetti_gif.append(conf_i)


#ThreadLoadGIF().start()
  #Clr = confetti_gif[i].get_at((0,0))
  #confetti_gif[i].set_colorkey(Clr)

for i in range(31) :
  name = "total_"+str(i)+".png"
  score = pygame.image.load(os.path.join(images, name))
  score_images.append(score)
  


WHITE = [255, 255, 255]
police = pygame.font.SysFont("arial", 25)

# Initialise la fenêtre de jeu
Largeur = 1024
Hauteur = 603
TailleEcran = [Largeur, Hauteur]
screen = pygame.display.set_mode(TailleEcran)
pygame.display.set_caption("BlackJack Daniel's")

# Gestion du rafraichissement de l'écran
clock = pygame.time.Clock()


cartes = [
  ["as_coeur.png", 11, None],
  ["as_pique.png", 1, None],
  ["as_trefle.png", 1, None],
  ["as_carreau.png", 11, None],

  ["deux_coeur.png", 2, None],
  ["deux_pique.png", 2, None],
  ["deux_trefle.png", 2, None],
  ["deux_carreau.png", 2, None],

  ["trois_coeur.png", 3, None],
  ["trois_pique.png", 3, None],
  ["trois_trefle.png", 3, None],
  ["trois_carreau.png", 3, None],
  
  ["quatre_coeur.png", 4, None],
  ["quatre_pique.png", 4, None],
  ["quatre_trefle.png", 4, None],
  ["quatre_carreau.png", 4, None],
  
  ["cinq_coeur.png", 5, None],
  ["cinq_pique.png", 5, None],
  ["cinq_trefle.png", 5, None],
  ["cinq_carreau.png", 5, None],
  
  ["six_coeur.png", 6, None],
  ["six_pique.png", 6, None],
  ["six_trefle.png", 6, None],
  ["six_carreau.png", 6, None],
  
  ["sept_coeur.png", 7, None],
  ["sept_pique.png", 7, None],
  ["sept_trefle.png", 7, None],
  ["sept_carreau.png", 7, None],
  
  ["huit_coeur.png", 8, None],
  ["huit_pique.png", 8, None],
  ["huit_trefle.png", 8, None],
  ["huit_carreau.png", 8, None],
  
  ["neuf_coeur.png", 9, None],
  ["neuf_pique.png", 9, None],
  ["neuf_trefle.png", 9, None],
  ["neuf_carreau.png", 9, None],
  
  ["dix_coeur.png", 10, None],
  ["dix_pique.png", 10, None],
  ["dix_trefle.png", 10, None],
  ["dix_carreau.png", 10, None],
  
  ["valet_coeur.png", 10, None],
  ["valet_pique.png", 10, None],
  ["valet_trefle.png", 10, None],
  ["valet_carreau.png", 10, None],

  ["dame_coeur.png", 10, None],
  ["dame_pique.png", 10, None],
  ["dame_trefle.png", 10, None],
  ["dame_carreau.png", 10, None],

  ["roi_coeur.png", 10, None],
  ["roi_pique.png", 10, None],
  ["roi_trefle.png", 10, None],
  ["roi_carreau.png", 10, None]
]


jeu_actuel = cartes 
main_croupier = []
main_joueur = []

balance_totale_joueur = 50
balance_main_joueur = 0 
MancheTerminee = False
JoueurStay = False
main_en_cours = False
nb_image_confetti = 0
win = False
isChangeBalance_Main = False
isChangeBalance_Totale = False

for i in range(len(cartes)) :
  carte = cartes[i] 
  carte[2] = pygame.image.load(os.path.join(images, carte[0]))


class ThreadClearCartes (threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self)  # ne pas oublier cette ligne
        # (appel au constructeur de la classe mère)

    def run(self):
      global main_joueur
      global main_croupier
      global MancheTerminee
      global JoueurStay
      
      time.sleep(3)
      MancheTerminee = True
      button.state = 0 
      time.sleep(1.5)
      
      main_joueur = []
      main_croupier = []
      MancheTerminee = False
      JoueurStay = False

      
class ThreadChangeBalance (threading.Thread):
    def __init__(self, typeBalance, montant): 
        threading.Thread.__init__(self)  
        self.montant = montant 
        self.typeBalance = typeBalance 

    def run(self):

      loop = abs(self.montant)
      negative = 1 if self.montant >= 0 else -1

      global isChangeBalance_Main
      global isChangeBalance_Totale
      
      if self.typeBalance == typeEnum.TypeMontant.BalanceMainJoueur :
        isChangeBalance_Main = True
        global balance_main_joueur
        for i in range(loop):
          balance_main_joueur += negative
          time.sleep(0.02)

      if self.typeBalance == typeEnum.TypeMontant.BalanceTotaleJoueur :
        isChangeBalance_Totale = True
        global balance_totale_joueur
        for i in range(loop):
          balance_totale_joueur += negative
          time.sleep(0.02)

      print(">> ", isChangeBalance_Main, ", ", isChangeBalance_Totale)

      if self.typeBalance == typeEnum.TypeMontant.BalanceMainJoueur : isChangeBalance_Main = False
      elif self.typeBalance == typeEnum.TypeMontant.BalanceTotaleJoueur : isChangeBalance_Totale = False



class ThreadChangeCarte (threading.Thread):
    def __init__(self, typeJoueur, carte, time): 
        threading.Thread.__init__(self)  
        self.carte = carte 
        self.typeJoueur = typeJoueur 
        self.time = time 

    def run(self):

        time.sleep(self.time)

        if self.typeJoueur == typeEnum.TypeJoueur.Joueur :
          global main_joueur 
          main_joueur.append(self.carte)

        if self.typeJoueur == typeEnum.TypeJoueur.Croupier :
          global main_croupier 
          main_croupier.append(self.carte)

class ThreadCroupierHit (threading.Thread):
    def __init__(self, BlackJack): 
        threading.Thread.__init__(self)  
        self.isBlackjack = BlackJack

    def run(self):

        global main_en_cours
        global win
        time.sleep(1.5)

        while GetValeurMain(main_croupier) < 17 and not self.isBlackjack: 
          GiveCard(typeEnum.TypeJoueur.Croupier, GetRandomCarte(), 0)
          time.sleep(1.5)

        
        valeurCroupier = GetValeurMain(main_croupier) 
        valeurJoueur = GetValeurMain(main_joueur) 

        bal_tempo = balance_main_joueur

        if valeurJoueur == 21 : 
          if valeurCroupier == 21 : 
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -bal_tempo)
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, bal_tempo)
          else :
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -bal_tempo)
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, bal_tempo*3)
            win = True

        elif valeurCroupier > 21 :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -bal_tempo)
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, bal_tempo*2)
          win = True 
          
        elif valeurCroupier >= valeurJoueur :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -bal_tempo)
        
        else :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, bal_tempo*2)
          win = True 
          
        main_en_cours = False 
        ThreadClearCartes().start()

        if(win) :
          time.sleep(5)
          win = False
        






def GiveCard(typeJoueur, carte, time):
  ThreadChangeCarte(typeJoueur, carte, time).start()

      
def ChangeBalanceMainJoueur(montant, typeBalance) :

  global isChangeBalance_Main
  global isChangeBalance_Totale

  #print(typeEnum.TypeMontant.BalanceMainJoueur == typeEnum.TypeMontant.BalanceMainJoueur)
  #print(typeBalance == typeEnum.TypeMontant.BalanceMainJoueur)
  #print(typeBalance == typeEnum.TypeMontant.BalanceTotaleJoueur)

  print(isChangeBalance_Main, " ", montant == typeEnum.TypeMontant.BalanceMainJoueur)
  print(isChangeBalance_Totale, " ", montant == typeEnum.TypeMontant.BalanceTotaleJoueur) 

  if isChangeBalance_Main and montant == typeEnum.TypeMontant.BalanceMainJoueur : return 
  if isChangeBalance_Totale and montant == typeEnum.TypeMontant.BalanceTotaleJoueur : return 
  
  #print(montant, ", ",typeBalance, ", ", isChangeBalance_Main, ", ", isChangeBalance_Totale)
  ThreadChangeBalance(montant, typeBalance).start()


def GetRandomCarte() :
  j = randrange(len(jeu_actuel))
  carte_distibuee = jeu_actuel[j]
  jeu_actuel.remove(carte_distibuee)
  return carte_distibuee

def GetValeurMain(main) -> int:
  value = [0]
  for carte in main : 
    val_carte = carte[1] 
    for i in range(len(value)) : value[i] += val_carte
    if val_carte == 1:
      copy_values = value.copy()
      for val in copy_values : value.append(val)
      for i in range(len(value)) : 
        if i%2 == 0 : continue 
        value[i] += 10 
      
      for v in value :
        if v > 21 : value.remove(v)

  ##value[0] += carte[1] 
  return value[0]

def main() -> int:

  global balance_totale_joueur
  global balance_main_joueur
  global main_joueur
  global main_croupier
  global police 
  global JoueurStay
  global main_en_cours
  global nb_image_confetti
  global confetti_gif
  global win
  
  #load button images
  jeton_1f = pygame.image.load(os.path.join(images, "Jeton_1.png")).convert_alpha()
  jeton_5f = pygame.image.load(os.path.join(images, "Jeton_5.png")).convert_alpha()
  jeton_10f = pygame.image.load(os.path.join(images, "Jeton_10.png")).convert_alpha()
  jeton_25f = pygame.image.load(os.path.join(images, "Jeton_25.png")).convert_alpha()
  jeton_50f = pygame.image.load(os.path.join(images, "Jeton_50.png")).convert_alpha()
  hit = pygame.image.load(os.path.join(images, "hit.png")).convert_alpha()
  stay = pygame.image.load(os.path.join(images, "stay.png")).convert_alpha()
  reset = pygame.image.load(os.path.join(images, "reset.png")).convert_alpha()
  play = pygame.image.load(os.path.join(images, "play.png")).convert_alpha()

  #load button images
  jeton_1f_tuto = pygame.image.load(os.path.join(images, "Jeton_1_jaune.png")).convert_alpha()
  jeton_5f_tuto = pygame.image.load(os.path.join(images, "Jeton_5_jaune.png")).convert_alpha()
  jeton_10f_tuto = pygame.image.load(os.path.join(images, "Jeton_10_jaune.png")).convert_alpha()
  jeton_25f_tuto = pygame.image.load(os.path.join(images, "Jeton_25_jaune.png")).convert_alpha()
  jeton_50f_tuto = pygame.image.load(os.path.join(images, "Jeton_50_jaune.png")).convert_alpha()
  hit_tuto = pygame.image.load(os.path.join(images, "hit_jaune.png")).convert_alpha()
  stay_tuto = pygame.image.load(os.path.join(images, "stay_jaune.png")).convert_alpha()
  reset_tuto = pygame.image.load(os.path.join(images, "reset_jaune.png")).convert_alpha()
  play_tuto = pygame.image.load(os.path.join(images, "play_jaune.png")).convert_alpha()
  
  #create button instances
  button_jeton_1f = button.Button(Largeur-75, Hauteur-100-70*1, jeton_1f, jeton_1f_tuto, 1, 0)
  button_jeton_5f = button.Button(Largeur-75, Hauteur-100-70*2, jeton_5f, jeton_5f_tuto, 1, 0)
  button_jeton_10f = button.Button(Largeur-75, Hauteur-100-70*3, jeton_10f, jeton_10f_tuto, 1, 0)
  button_jeton_25f = button.Button(Largeur-75, Hauteur-100-70*4, jeton_25f, jeton_25f_tuto, 1, 0)
  button_jeton_50f = button.Button(Largeur-75, Hauteur-100-70*5, jeton_50f, jeton_50f_tuto, 1, 0)
  button_hit = button.Button(Largeur/2 - 250, Hauteur-100, hit,  hit_tuto, 1, 2)
  button_stay = button.Button(Largeur/2 - 20 , Hauteur-100, stay, stay_tuto, 1, 2)
  button_reset = button.Button(Largeur/2 + 210, Hauteur-100, reset, reset_tuto, 1, 1)
  button_play = button.Button(Largeur/2 - 250-230, Hauteur-100, play, play_tuto, 1, 1)

  
  
  jetons = [
    [button_jeton_1f, 1], 
    [button_jeton_5f, 5], 
    [button_jeton_10f, 10], 
    [button_jeton_25f, 25], 
    [button_jeton_50f, 50] 
  ]

  current_frame = 0 

  while True : 

    # recupère la liste des évènements du joueur
    event = pygame.event.Event(pygame.USEREVENT)

    # EVENEMENTS
    # détecte le clic sur le bouton close de la fenêtre
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return 1 
    
    
    screen.blit(fond,(0,0))


    current_frame = (current_frame+1) % 30 
    if(win) :
      screen.blit(confetti_gif[current_frame],(Largeur/2 - 300,0))
    

    if button_stay.draw(screen) :
      if main_en_cours :
        JoueurStay = True
        thrd = ThreadCroupierHit(False)
        thrd.start()
        #thrd.join() # peut pas attendre vu que les frames s'arrêtent
        

    


    if button_reset.draw(screen) :
      if not main_en_cours :
        button.state = 0 
        bal_tempo = balance_main_joueur
        ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, bal_tempo)
        ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -bal_tempo)
        #balance_totale_joueur += balance_main_joueur
        #balance_main_joueur = 0 

    if button_hit.draw(screen) :
      if not main_en_cours : continue
      main_joueur.append(GetRandomCarte())
      i = GetValeurMain(main_joueur)
      if(GetValeurMain(main_joueur) > 21) :
        main_en_cours = False 
        ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -balance_main_joueur)
        ThreadClearCartes().start()
      



    if button_play.draw(screen):
      button.state = 2
      if not main_en_cours :
        main_en_cours = True 
        for i in range(2) :
          GiveCard(typeEnum.TypeJoueur.Croupier, GetRandomCarte(), i)
          GiveCard(typeEnum.TypeJoueur.Joueur, GetRandomCarte(), 2+i)
        
    if main_en_cours and len(main_joueur) == 2 and GetValeurMain(main_joueur) == 21 :
      ThreadCroupierHit(True) 

          

    for jeton in jetons :

      if jeton[0].draw(screen):

        if main_en_cours : continue 

        if button.state == 0 : button.state += 1
        if balance_totale_joueur - jeton[1] < 0 :
          balance_main_joueur += balance_totale_joueur
          balance_totale_joueur = 0 
        else :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, -jeton[1])
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, jeton[1])
        

    
    zone = police.render("Balance : "+str(balance_totale_joueur)+" $", True, WHITE)
    screen.blit(zone,(50, Hauteur-200))


    x_resize = 80
    z_resize = 80

    

    screen.blit(jeton_mise, ((Largeur-x_resize)/2, 150))

    """
    if(balance_main_joueur <= 0) :
      
    elif(balance_main_joueur < 10):
      screen.blit(pile_bleue, ((Largeur-x_resize)/2, 150))
    elif(balance_main_joueur < 20) :
      screen.blit(pile_rouge, ((Largeur-x_resize)/2, 150))
    elif(balance_main_joueur < 30) :
      screen.blit(pile_verte, ((Largeur-x_resize)/2, 150))
    else :
      screen.blit(pile_noire, ((Largeur-x_resize)/2, 150))
    """

    zone = police.render(str(balance_main_joueur)+" $", True, WHITE)
    screen.blit(zone,(((Largeur+x_resize+30)/2, 136+z_resize/2)))

    # 198 × 284

    multiplier_size = 0.4
    pixels_dacals = 0
    nombre_carte_main = len(main_joueur) 

    x_resize = 198*multiplier_size
    z_resize = 284*multiplier_size

    x_center = Largeur/2 - x_resize/2
    x_default = x_center - x_resize*(nombre_carte_main-1)/2

    x_score = x_default-30 if(nombre_carte_main == 0) else x_default-198*multiplier_size
    screen.blit(score_images[GetValeurMain(main_joueur)], (x_score, Hauteur-250+(z_resize/4)))

    global MancheTerminee
    # Dessine les cartes
    for carte in main_joueur :   
      carte_image = carte[2] if not MancheTerminee else verso_carte
      screen.blit(scale(carte_image, (x_resize,z_resize)) , (x_default+pixels_dacals, Hauteur-250))
      pixels_dacals += 198*multiplier_size+2


    pixels_dacals = 0 
    nombre_carte_main = len(main_croupier) 
    x_default = x_center - x_resize*(nombre_carte_main-1)/2

    x_score = x_default-30 if(nombre_carte_main == 0) else x_default-198*multiplier_size
    
    score_croupier = 0
    compt = 0 
    for carte in main_croupier :
      carte_image = carte[2] if compt != 0 or JoueurStay else verso_carte
      if(compt != 0 or JoueurStay) : score_croupier += carte[1]
      screen.blit(scale(carte_image, (x_resize,z_resize)) , (x_default+pixels_dacals, 20))
      pixels_dacals += 198*multiplier_size+2
      compt += 1

    screen.blit(score_images[score_croupier], (x_score, 20+(z_resize/4)))

    # Demande à pygame de se caler sur 30 FPS
    clock.tick(30)

    # Bascule l'image dessinée à l'écran
    pygame.display.flip()



  
  return 0

if __name__ == '__main__':
    sys.exit(main()) 