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

#from playsound import playsound



scriptPATH = os.path.abspath(inspect.getsourcefile(lambda:0))
scriptDIR  = os.path.dirname(scriptPATH)
images = os.path.join(scriptDIR,"images")
fond = pygame.image.load(os.path.join(images, "background-table.jpg"))
verso_carte = pygame.image.load(os.path.join(images, "verso_carte.png"))
jeton_mise = pygame.image.load(os.path.join(images, "jeton_mise.png"))
#playsound('audio.mp3')



# initialisation de l'écran de jeu
pygame.init()

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
  ["as_coeur.png", 1, None],
  ["as_pique.png", 1, None],
  ["as_trefle.png", 1, None],
  ["as_carreau.png", 1, None],

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
      
      time.sleep(3)
      MancheTerminee = True
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
      
      if self.typeBalance == typeEnum.TypeMontant.BalanceMainJoueur :
        global balance_main_joueur
        for i in range(loop):
          balance_main_joueur += negative
          time.sleep(0.02)

      if self.typeBalance == typeEnum.TypeMontant.BalanceTotaleJoueur :
        global balance_totale_joueur
        for i in range(loop):
          balance_totale_joueur += negative
          time.sleep(0.02)


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
        time.sleep(1.5)

        while GetValeurMain(main_croupier) < 17 and not self.isBlackjack: 
          GiveCard(typeEnum.TypeJoueur.Croupier, GetRandomCarte(), 0)
          time.sleep(1.5)

        
        valeurCroupier = GetValeurMain(main_croupier) 
        valeurJoueur = GetValeurMain(main_joueur) 

        if valeurCroupier > 21 :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -balance_main_joueur)
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, balance_main_joueur*2)

        elif valeurJoueur == 21 : 
          if valeurCroupier == 21 : 
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -balance_main_joueur)
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, balance_main_joueur)
          else :
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -balance_main_joueur)
            ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, balance_main_joueur*2.5)
          
        elif valeurCroupier >= valeurJoueur :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -balance_main_joueur)
        
        else :
          ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, balance_main_joueur*2)
          
        main_en_cours = False 
        ThreadClearCartes().start()




def GiveCard(typeJoueur, carte, time):
  ThreadChangeCarte(typeJoueur, carte, time).start()

      
def ChangeBalanceMainJoueur(montant, typeBalance) :
  ThreadChangeBalance(montant, typeBalance).start()


def GetRandomCarte() :
  j = randrange(len(jeu_actuel))
  carte_distibuee = jeu_actuel[j]
  jeu_actuel.remove(carte_distibuee)
  return carte_distibuee

def GetValeurMain(main) -> int:
  value = 0
  for carte in main : 
    value += carte[1]
  return value 

def main() -> int:

  global balance_totale_joueur
  global balance_main_joueur
  global main_joueur
  global main_croupier
  global police 
  global JoueurStay
  global main_en_cours
  
  #load button images
  jeton_1f = pygame.image.load(os.path.join(images, "jeton_1f.png")).convert_alpha()
  jeton_5f = pygame.image.load(os.path.join(images, "jeton_5f.png")).convert_alpha()
  jeton_10f = pygame.image.load(os.path.join(images, "jeton_10f.png")).convert_alpha()
  jeton_20f = pygame.image.load(os.path.join(images, "jeton_20f.png")).convert_alpha()
  jeton_50f = pygame.image.load(os.path.join(images, "jeton_50f.png")).convert_alpha()
  hit = pygame.image.load(os.path.join(images, "hit.png")).convert_alpha()
  stay = pygame.image.load(os.path.join(images, "stay.png")).convert_alpha()
  reset = pygame.image.load(os.path.join(images, "reset.png")).convert_alpha()
  play = pygame.image.load(os.path.join(images, "play.png")).convert_alpha()
  
  #create button instances
  button_jeton_1f = button.Button(Largeur-75, Hauteur-100-70*1, jeton_1f, 0.3)
  button_jeton_5f = button.Button(Largeur-75, Hauteur-100-70*2, jeton_5f, 0.3)
  button_jeton_10f = button.Button(Largeur-75, Hauteur-100-70*3, jeton_10f, 0.3)
  button_jeton_20f = button.Button(Largeur-75, Hauteur-100-70*4, jeton_20f, 0.3)
  button_jeton_50f = button.Button(Largeur-75, Hauteur-100-70*5, jeton_50f, 0.3)
  button_hit = button.Button(Largeur/2 - 250, Hauteur-100, hit, 1)
  button_stay = button.Button(Largeur/2 - 20 , Hauteur-100, stay, 1)
  button_reset = button.Button(Largeur/2 + 240, Hauteur-110, reset, 0.14)
  button_play = button.Button(50, Hauteur-150, play, 0.65)

  
  jetons = [
    [button_jeton_1f, 1], 
    [button_jeton_5f, 5], 
    [button_jeton_10f, 10], 
    [button_jeton_20f, 20], 
    [button_jeton_50f, 50] 
  ]


  while True : 

    # recupère la liste des évènements du joueur
    event = pygame.event.Event(pygame.USEREVENT)

    # EVENEMENTS
    # détecte le clic sur le bouton close de la fenêtre
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        return 1 
    
    screen.blit(fond,(0,0))

    if button_stay.draw(screen) :
      JoueurStay = True
      thrd = ThreadCroupierHit(False)
      thrd.start()
      #thrd.join() # peut pas attendre vu que les frames s'arrêtent
      




    if button_reset.draw(screen) :
      if not main_en_cours :
        ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceTotaleJoueur, balance_main_joueur)
        ChangeBalanceMainJoueur(typeEnum.TypeMontant.BalanceMainJoueur, -balance_main_joueur)
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
      if not main_en_cours :
        main_en_cours = True 
        for i in range(2) :
          GiveCard(typeEnum.TypeJoueur.Croupier, GetRandomCarte(), i)
          GiveCard(typeEnum.TypeJoueur.Joueur, GetRandomCarte(), 2+i)
        
    if main_en_cours and len(main_joueur) == 2 and GetValeurMain(main_joueur) == 21 :
      ThreadCroupierHit(True) 

          

    for jeton in jetons :
      if jeton[0].draw(screen):
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

    screen.blit(scale(jeton_mise, (x_resize,z_resize)) , ((Largeur-x_resize)/2, 150))
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

    global MancheTerminee
    # Dessine les cartes
    for carte in main_joueur :   
      carte_image = carte[2] if not MancheTerminee else verso_carte
      screen.blit(scale(carte_image, (x_resize,z_resize)) , (x_default+pixels_dacals, Hauteur-250))
      pixels_dacals += 198*multiplier_size+2


    pixels_dacals = 0 
    nombre_carte_main = len(main_croupier) 
    x_default = x_center - x_resize*(nombre_carte_main-1)/2
    compt = 0 
    for carte in main_croupier :
      carte_image = carte[2] if compt != 0 or JoueurStay else verso_carte
      screen.blit(scale(carte_image, (x_resize,z_resize)) , (x_default+pixels_dacals, 20))
      pixels_dacals += 198*multiplier_size+2
      compt += 1

    # Demande à pygame de se caler sur 30 FPS
    clock.tick(30)

    # Bascule l'image dessinée à l'écran
    pygame.display.flip()



  
  return 0

if __name__ == '__main__':
    sys.exit(main()) 