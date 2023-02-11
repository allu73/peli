# TEE PELI TÄHÄN
import pygame
import random

class Peli:
    def __init__(self):
        pygame.init()

        self.lataa_kuvat() #ladataan tarvittavat kuvat

        self.naytto = pygame.display.set_mode((640, 480))

        self.kello = pygame.time.Clock()

        self.fontti = pygame.font.SysFont("Arial", 24)

        self.peli_kaynnissa = True #peli alkaa heti


        self.pisteet = 0 #pisteet alussa nolla
        self.kierros = 1 #vain 1 piste per kolikko
        self.ennatys = 0 #ennätys alussa nolla
        self.uusi_ennatys = False #uusi ennätys alussa false

        self.x = 150 #robotin x
        self.y = 480-self.robo.get_height() #robotin y

        self.hyppy = False #hyppääkö robottti
        self.jumpCount = 10 #hypyn kesto
        self.nopeus = 5 #esineiden nopeus
        
        self.x2 = 640 #kolikon tai hirviön x alkupiste
        self.y2 = 480 - self.raha.get_height() #kolikon tai hirviön y koodinaatti

        self.valinta = 1 #alkuun kolikko

        self.silmukka() #silmukka käyntiin


    def lataa_kuvat(self): #ladataan kuvat
        self.robo = pygame.image.load("robo.png")
        self.hirvio = pygame.image.load("hirvio.png")
        self.raha = pygame.image.load("kolikko.png")



    def hyppaa(self): #oma funktio robotin hypylle
        if self.jumpCount >= -10:
            self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.5
            self.jumpCount -= 1
        else: 
            self.jumpCount = 10
            self.hyppy = False


    def esine(self): #vastaan tuleva kolikko tai hirviö

        self.x2 -= self.nopeus #lähenee robottia

        if self.valinta == 1: #raha
            self.y2 = 480- self.raha.get_height()
        else: #hirviö
            self.y2 = 480- self.hirvio.get_height()

        if self.x2 < 0: #kun häviää kuvasta niin uusi esine
            self.x2 = 640
            self.valinta = random.randint(1,2) #robotti vai kolikko

            self.kierros = 1 #nollataan kolikon pisteytys (vain 1 piste per kolikko)

    

    def silmukka(self):
        while True:

            self.tutki_tapahtumat() #luetaan komennot

            if self.hyppy: #jos hypätään niin oma funktio sille
                self.hyppaa()

            self.esine() #haetaan kolikon tai hriviön koodinaatit

            self.piirra_naytto() #piirretään näytölle

            if self.x2 < 190 and self.x2 > 120 and self.y+self.robo.get_height() >= self.y2: #jos koordinaatit osuvat kolikkoon tai hirviöön
                if self.valinta == 1: #kolikosta tulee piste
                    self.laske_pisteet()
                else: #hirviöstä peli päättyy
                    self.peli_ohi()

    
    def laske_pisteet(self):
        if self.kierros == 1 and self.valinta == 1: #pisteitä 1 per kierros ja kolikko
            self.pisteet += 1
            self.kierros -= 1 #pisteet jaettu
            self.nopeus *= 1.05 #nopeus kiihtyy 5% jokaisesta kolikosta


        if self.pisteet > self.ennatys: #jos ylitetään ennätys nii se päivittyy
            self.ennatys = self.pisteet
            self.uusi_ennatys = True #uusi ennätysilmoitus pelaajalle

    

    def peli_ohi(self): #peli päättyy ja esineet pysähtyvät
        self.nopeus = 0
        self.peli_kaynnissa = False


    def uusi_peli(self): #aloitetaan uusi peli
        self.pisteet = 0 #nollataan pistelaskuri
        self.uusi_ennatys = False #nollataan uusi ennätys

        self.x2 = 640 #nollataan kolikon tai hirviön alkupiste
        self.y2 = 480 - self.raha.get_height() #kolikon y koodinaatti (alkaa kolikolla)

        self.valinta = 1 #valitaan kolikko

        self.peli_kaynnissa = True #peli käyntiin
        self.nopeus = 5 #nopeus tasolle 5 (alkuvauhti)


    def piirra_naytto(self):
        pygame.display.set_caption("Hyppypeli") #pelin nimi
        self.naytto.fill((255, 255, 255))

        #piirretään ohjeet ja pisteet
        teksti = self.fontti.render("Ennätys: " + str(self.ennatys), True, (255, 0, 0))
        self.naytto.blit(teksti, (25, 50))
        
        teksti = self.fontti.render("Pisteet: " + str(self.pisteet), True, (255, 0, 0))
        self.naytto.blit(teksti, (200, 50))

        teksti = self.fontti.render("F2 = uusi peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (25, 10))

        teksti = self.fontti.render("Esc = sulje peli", True, (0, 0, 0))
        self.naytto.blit(teksti, (200, 10))

        teksti = self.fontti.render("Välilyönti = hyppy", True, (0, 0, 0))
        self.naytto.blit(teksti, (400, 10))

        #katsotaan onko peli käynnissä ja näytetään alkuun ohjeet pelaajalle
        if self.pisteet < 2 and self.peli_kaynnissa == True:
            teksti = self.fontti.render("Kerää kolikoita ja vältä hirviöitä hyppimällä", True, (0, 0, 0))
            self.naytto.blit(teksti, (25, 200))


        #piirretäätän robotti ja vastaantulevat kolikot ja hirviöt
        self.naytto.blit(self.robo, (self.x, self.y))
        if self.valinta == 1: #piirretään kolikko
            self.naytto.blit(self.raha, (self.x2, self.y2))
        if self.valinta == 2: #piirretään hirviö
            self.naytto.blit(self.hirvio, (self.x2, self.y2))


        #jos peli ei enää käynnissä niin näytetään pistee
        if self.peli_kaynnissa == False:
            teksti = self.fontti.render("Peli ohi! Pisteet: "+ str(self.pisteet), True, (0, 0, 0))
            self.naytto.blit(teksti, (200, 480/2))

            if self.uusi_ennatys == True: #jos uusi ennätys niin ilmoitetaan pelaajalle
                teksti = self.fontti.render("Uusi ennätystulos!", True, (0, 0, 0))
                self.naytto.blit(teksti, (200, 480/2-50))


        pygame.display.flip()

        self.kello.tick(60)


    def tutki_tapahtumat(self): #pelin komennot
        for tapahtuma in pygame.event.get():
                
            if tapahtuma.type == pygame.QUIT:
                exit()
        
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_SPACE:
                    self.hyppy = True
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                if tapahtuma.key == pygame.K_F2:
                    self.uusi_peli()



if __name__ == "__main__":
    Peli()
