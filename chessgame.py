import random

def attribuer_couleurs():
    couleurs = ["blanc", "noir"]
    random.shuffle(couleurs)

    couleur_humain = couleurs[0]

    return couleur_humain
class Piece():

    def __init__(self,couleur,symbole):
        self.symbole=symbole
        self.couleur=couleur
class ChessGame():
   
    def __init__(self,profondeur):
        self.echiquier = [ [Piece('noir', 'R'), Piece('noir', 'N'), Piece('noir', 'B'), Piece('noir', 'Q'), Piece('noir', 'K'), Piece('noir', 'B'), Piece('noir', 'N'), Piece('noir', 'R')]
                      , [Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P')],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P')],
                      [Piece('blanc', 'R'), Piece('blanc', 'N'), Piece('blanc', 'B'), Piece('blanc', 'Q'), Piece('blanc', 'K'), Piece('blanc', 'B'), Piece('blanc', 'N'), Piece('blanc', 'R')] ]
       
     

   


 

        self.joueur=attribuer_couleurs()          

   
        self.tour='blanc'
        self.compteur=1
       
        self.profondeur=profondeur

   

    def joueuradverse(self,joueur):
        if joueur=='blanc':
            return 'noir'
        else:
            return'blanc'
       
    def print_board(self,echiquier):
        for i in range(8):
            b=[str(i+1)+" ",]
       
            for j in range(8):
                p=self.obtenir_piece([i,j],echiquier)
                if p==0:
                    b.append("  ")
                else:
                    if p.couleur=='blanc':
                        b.append("W"+str(p.symbole))

                    else:
                        b.append("B"+str(p.symbole))

            print(b,'\n',)
        print(["# ","1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ","8 "])

   

    def changement_tour(self): 
        if self.tour=='blanc':
            self.tour='noir'
            self.compteur+=1
        else:
            self.tour='blanc' 
            self.compteur+=1
 
    def obtenir_piece(self, position,echiquier):


        ligne, colonne = position
       
        return echiquier[ligne][colonne]
   
    def case_roi(self,couleur,echiquier):
        for i in range(8):
            for j in range(8):
                piece=self.obtenir_piece([i,j],echiquier)
                if piece !=0:
                    if piece.couleur==couleur and piece.symbole=='K':
                        return[i,j]
                       
                 

    def est_capturable(self,position,couleur,echiquier):
        piece2=self.obtenir_piece(position,echiquier)
        for i in range(8):    
            for j in range(8):

                piece1=self.obtenir_piece([i,j],echiquier)
                if piece1 !=0 and piece1.couleur!=piece2.couleur:
                    if self.coup_legal((i,j),position,self.joueuradverse(couleur),echiquier):
                        return piece2.symbole, True

    def peut_capturer(self,position,couleur,echiquier):
        a=[]
        for i in range(8):
            for j in range(8):
                if self.obtenir_piece([i,j],echiquier)!=0:
                    if self.coup_valide(position,[i,j],couleur):
                        c=self.obtenir_piece([i,j],echiquier)
                        a.append(c)
                   
        return a                            

    def echec(self,joueur,echiquier):
        roi_case=self.case_roi(joueur,echiquier)
        if self.est_capturable(roi_case,joueur,echiquier):          #on utilise la fonction qui verifie si le mouvement de la piece est autorisé
            return True
        return False    
           


    def jouer(self):
        print("Vous jouez les "+str(self.joueur)+"s.\n L'ordinateur joue les "+str(self.joueuradverse(self.joueur))+"s. \n")
        i=input("Pour continuer, appuyez sur entrée \n")
        while self.echec_et_mat(self.tour,self.echiquier) is False:
            self.print_board(self.echiquier)
            self.deroulement()
        print('les',self.joueuradverse(self.tour),'ont gagné')
    def deroulement(self):
        if self.tour=='blanc':
            if self.joueur=='blanc':
                print("C'est au tour des blancs")
                depart=self.choix_piece()
                arrivee=self.choixmouvementjoueur()
                if self.echec(self.tour,self.echiquier):
                    print("Vous êtes en échec")
                    if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                        self.deplacer_piece(depart,arrivee,self.echiquier)
                        t=self.check_promotion_joueur()
                        if t[0]==True:
                            self.promotion_joueur(t[1],t[2],t[3])
                        self.changement_tour()
                    else:
                        print('vous êtes toujours en échec')


                else:
                    if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                        self.deplacer_piece(depart,arrivee,self.echiquier)
                        t=self.check_promotion_joueur()
                        if t[0]==True:
                            self.promotion_joueur(t[1],t[2],t[3])
                        self.changement_tour()
               
                    else:
                        print("Coup impossible, veuillez rejouez")
                        self.deroulement()
                   
            else:
                depart,arrivee=self.minmax('blanc',self.profondeur,self.sauvegarder_etat_echiquier(self.echiquier))[1]
                self.deplacer_piece(depart, arrivee,self.echiquier)
                t=self.check_promotion_ordi()
                if t[0]==True:
                    self.promotion_ordi(t[1],t[2],t[3])
                self.changement_tour()
                   
        else:
            print("C'est au tour des noirs")
            if self.joueur=='noir':
                depart=self.choix_piece()
                arrivee=self.choixmouvementjoueur()
                if self.echec(self.tour,self.echiquier):
                    print("Vous êtes en échec")
                    if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                        self.deplacer_piece(depart,arrivee,self.echiquier)
                        t=self.check_promotion_joueur()
                        if t[0]==True:
                            self.promotion_joueur(t[1],t[2],t[3])
                        self.changement_tour()
                    else:
                        print('vous êtes toujours en échec')
                else:
                    if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                        self.deplacer_piece(depart,arrivee,self.echiquier)
                        t=self.check_promotion_ordi()
                        if t[0]==True:
                            self.promotion_ordi(t[1],t[2],t[3])
                        self.changement_tour()

                    else:
                        print("Coup impossible, veuillez rejouez")
                        self.deroulement()
            else:
                depart,arrivee=self.minmax('noir',self.profondeur,self.sauvegarder_etat_echiquier(self.echiquier))[1]
                self.deplacer_piece(depart, arrivee,self.echiquier)
                t=self.check_promotion_ordi()
                if t[0]==True:
                    self.promotion_ordi(t[1],t[2],t[3])
                self.changement_tour()

       


            if self.echec_et_mat(self.tour,self.echiquier) is True:
                print("C'est fini pour toi, révise tes leçons")
       

    def sauvegarder_etat_echiquier(self,echiquier):
        a=[]
        for i in range(8):
            b=[]
            for j in range (8):
                b.append(echiquier[i][j])
            a.append(b)
        
        return a


 
    def choix_piece(self):
        ligne=input("Ligne de la pièce à jouer de 1 à 8 ")
        colonne=input("Colonne de la pièce à jouer de 1 à 8 ")
       
        coor=['1','2','3','4','5','6','7','8']
       
        if ligne not in coor or colonne not in coor:
            print("Coordonnées de départ invalides, réessayez !") #Evite les arrêts du programme et donc de recommencer la partie
            return self.choix_piece()
       
        else:
            ligne=int(ligne)-1
            colonne=int(colonne)-1
       
        if self.obtenir_piece([ligne,colonne],self.echiquier)==0:
            print('case vide')
            return self.choix_piece()
        elif self.obtenir_piece([ligne,colonne],self.echiquier).couleur!=self.tour: #Impossible de déplacer une pièce adverse
            print("Pièce adverse !")
            return self.choix_piece()
        else:    
            print(self.obtenir_piece([ligne,colonne],self.echiquier).couleur, self.obtenir_piece([ligne,colonne],self.echiquier).symbole)
            return [ligne,colonne]
       
       
   
    def deplacer_piece(self,depart,arrivee,echiquier):
        piece=self.obtenir_piece(depart,echiquier)
        echiquier[arrivee[0]][arrivee[1]]=piece
        echiquier[depart[0]][depart[1]]=0

       

   
    def choixmouvementjoueur(self):
       
        ligne=input("Case d'arrivée de 1 à 8 ")
        colonne=input("Case d'arrivée de 1 à 8 ")
       
        coor=['1','2','3','4','5','6','7','8']
       
        if ligne not in coor or colonne not in coor:
            print("Coordonnées d'arrivée invalides, veuillez réessayer !")
            return self.choixmouvementjoueur()
       
        else:
            ligne=int(ligne)-1
            colonne=int(colonne)-1
        return [ligne,colonne]

       
   
    def mouvement_type(self,piecedepart,piecearrivee,positiondepart,positionarrivee,echiquier): #position de départ
        x=piecedepart
        if x.symbole=='N':
            return self.cavalier(positiondepart,positionarrivee)
        elif x.symbole=='R':
            return self.rook(piecedepart,positiondepart,positionarrivee)
        elif x.symbole=='B':
            return self.fou(piecedepart,positiondepart,positionarrivee,echiquier)
        elif x.symbole=='K':
            return self.roi(positiondepart,positionarrivee)
        elif x.symbole=='Q':
            return self.reine(piecedepart,positiondepart,positionarrivee,echiquier)
        elif x.symbole=='P':
            return self.pion(piecedepart,piecearrivee,positiondepart,positionarrivee)
                       
    def coup_legal(self,positiondepart,positionarrivee,couleur,echiquier):
        piecedepart=self.obtenir_piece(positiondepart,echiquier)
        piecearrivee=self.obtenir_piece(positionarrivee,echiquier)    
       
        if positionarrivee[0]>7 or positionarrivee[0]<0 or positionarrivee[1]>7 or positionarrivee[1]<0:
            return False
       
        elif piecedepart==0: #On ne peut pas sélectionner une case vide
            return False
       
       
        elif  piecearrivee!=0 and piecedepart.couleur==piecearrivee.couleur: #Impossible de jouer sur une case occupée par ses propres pièces
            return False
       
        elif piecedepart.couleur!=couleur:
            return False #On ne joue pas les pieces des autres
        else:
            return self.mouvement_type(piecedepart,piecearrivee,positiondepart,positionarrivee,echiquier)
       
    def echec_et_mat(self,joueur,echiquier):
        if self.echec(joueur,echiquier) is False:  #cas le plus simple où il n'y a pas d'échec au roi
            return False
        for i in range(8):
            for j in range(8):
                piece=self.obtenir_piece([i,j],echiquier)
                if piece !=0 and piece.couleur==joueur:
                    for x in range(8):
                        for y in range(8):
                            if self.coup_valide((i,j),(x,y),joueur,echiquier):
                                a=self.coup_valide((i,j),(x,y),joueur,echiquier)[1]
                                echec=self.echec(joueur,a)
                                if echec is False:
                                    return False

                               
        return True

    def coup_valide(self,positiondepart,positionarrivee,couleur,echiquier):
       
        if self.coup_legal(positiondepart,positionarrivee,couleur,echiquier)==True:
            piecesauvegardee=echiquier[positionarrivee[0]][positionarrivee[1]]
            self.deplacer_piece(positiondepart,positionarrivee,echiquier)
            if self.echec(self.tour,echiquier) or self.echec_et_mat(self.tour,echiquier)==True:
                self.deplacer_piece(positionarrivee,positiondepart,echiquier)
                echiquier[positionarrivee[0]][positionarrivee[1]]=piecesauvegardee
                return False
           
            else:
                a=self.sauvegarder_etat_echiquier(echiquier)
                self.deplacer_piece(positionarrivee,positiondepart,echiquier)
                echiquier[positionarrivee[0]][positionarrivee[1]]=piecesauvegardee
                return True,a
        else:
            return False    
   
   

    def cavalier(self,positiondepart,positionarrivee):
        if abs(positiondepart[0]-positionarrivee[0])==2 and abs(positiondepart[1]-positionarrivee[1])==1:
            return True
        if abs(positiondepart[0]-positionarrivee[0])==1 and abs(positiondepart[1]-positionarrivee[1])==2:
            return True
        else:
            return False
       
   



    def rook(self,piecedepart,positiondepart,positionarrivee):
        x=positiondepart[0]
        y=positiondepart[1]
        c=0
        if positiondepart[0]!=positionarrivee[0] and positiondepart[1]!=positionarrivee[1]:
            return False
        elif positiondepart[0]==positionarrivee[0]:
            if positiondepart[1]< positionarrivee[1]:
                for i in range (positiondepart[1]+1,positionarrivee[1]+1):
                    if self.echiquier[x][i]!=0:
                        if i==positionarrivee[1]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True
                           
                   
            if positiondepart[1]>positionarrivee[1]:
                for i in range (positiondepart[1]-1,positionarrivee[1]-1,-1):
                    if self.echiquier[x][i]!=0:
                        if i==positionarrivee[1]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True
                 
        else:
            if positiondepart[0]< positionarrivee[0]:
                for i in range (positiondepart[0]+1,positionarrivee[0]+1):
                    if self.echiquier[i][y]!=0:
                        if i==positionarrivee[0]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True
                   
                   
            if positiondepart[0]>positionarrivee[0]:
                for i in range (positiondepart[0]-1,positionarrivee[0]-1,-1):
                    if self.echiquier[i][y]!=0:
                        if i==positionarrivee[0]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True

    def fou(self,piecedepart,positiondepart,positionarrivee,echiquier):
        x1=positiondepart[0]
        y1=positiondepart[1]
        x2=positionarrivee[0]
        y2=positionarrivee[1]
       
        if abs(x2-x1)!=abs(y2-y1):
            return False
        else:
            if x1 < x2:
                if y1<y2:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1+i,y1+i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1+i,y1+i],echiquier)!=piecedepart.couleur :
                                return True
                            else:
                                return False
                        else:
                            continue
                   
                    return True
                             
                else:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1+i,y1-i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1+i,y1-i],echiquier)!=piecedepart.couleur :
                                return True
                            else:
                                return False
                        else:
                            continue
                   
                    return True
                           
            else:
                if y1<y2:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1-i,y1+i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1-i,y1+i],echiquier)!=piecedepart.couleur :
                                return True
                            else:
                                return False
                        else:
                            continue
                   
                    return True
                else:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1-i,y1-i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1-i,y1-i],echiquier).couleur!=piecedepart.couleur:
                                return True
                            else:
                                return False
                        else:
                            continue
                    return True
               
       
    def reine(self,piecedepart,positiondepart,positionarrivee,echiquier):
        return self.rook(piecedepart,positiondepart,positionarrivee) or self.fou(piecedepart,positiondepart,positionarrivee,echiquier)        

       
    def pion(self,piecedepart,piecearrivee,positiondepart,positionarrivee):
        x1=positiondepart[0]
        y1=positiondepart[1]
        x2=positionarrivee[0]
        y2=positionarrivee[1]
       
        if piecedepart.couleur=='noir':
            if y1==y2:
                if piecearrivee!=0:
                        return False
                if x1==1:
                    if x2==x1+1 or x2==x1+2:
                        return True
                    else:
                        return False
                else:
                    if x2==x1+1:
                        return True
                    else:
                        return False
                   
            elif abs(y2-y1)==1:
                if  x1-x2==-1:
                    if piecearrivee!=0 and piecearrivee.couleur!='noir':
                        return True
                    else:
                        return False
            else:
                return False
       
        if piecedepart.couleur=='blanc':
            if y1==y2:
                if piecearrivee!=0:
                    return False
                if x1==6:
                    if x2==x1-1 or x2==x1-2:
                        return True
                    else:
                        return False
                else:
                    if x2==x1-1:
                        return True
                    else:
           
                        return False
                   
            elif abs(y2-y1)==1 :
                if x1-x2==1 :
                    if piecearrivee!=0 and piecearrivee.couleur!='blanc':
                        return True
                    else:
                        return False
            else:
                return False

                     

           

   
   
    def roi(self,positiondépart,positionarrivée):
        if abs(positionarrivée[0]-positiondépart[0])<=1 and abs(positionarrivée[1]-positiondépart[1])<=1:
            return True
        else:
            return False
         
               

    def check_promotion_joueur(self):
        for i in range(8):
            a=self.obtenir_piece([7,i],self.echiquier)
            p=i
           
            if a!=0 and self.tour=='noir' and a.couleur=='noir' and a.symbole=='P':
               
                return [True,p,a,7]
            else:
                pass
           
            c=self.obtenir_piece([0,i],self.echiquier)
            p1=i
           
            if c!=0 and c.couleur=='blanc'and self.tour=='blanc' and c.symbole=='P':
                return [True,p1,c,0]
            else:
                pass
               
        return [False,]
           
           


    def promotion_joueur(self,p,c,l):
        b=['P','Q','B','N','R']
        i=input("Promotion ! Quelle pièce choisissez vous ?")
        if i not in b:
            print("Erreur, la pièce n'existe pas")
            self.promotion_joueur(p,c,l)
       
        else:
            self.echiquier[l][p]=Piece(c.couleur,i)
   
    def check_promotion_ordi(self):
        for i in range(8):
            a=self.obtenir_piece([7,i],self.echiquier)
            p=i
           
            if a!=0 and self.tour=='noir' and a.couleur=='noir' and a.symbole=='P':
               
                return [True,p,a,7]
            else:
                pass
           
            c=self.obtenir_piece([0,i],self.echiquier)
            p1=i
           
            if c!=0 and c.couleur=='blanc'and self.tour=='blanc' and c.symbole=='P':
                return [True,p1,c,0]
            else:
                pass
               
        return [False,]
   
    def promotion_ordi(self,p,c,l):
        b=['P','Q','B','N','R']
        i='Q'
        if i not in b:
            print("Erreur, la pièce n'existe pas")
            self.promotion_ordi(p,c,l)
        else:
            self.echiquier[l][p]=Piece(c.couleur,i)
   
 



    def obtenir_tous_les_coups(self,couleur,echiquier):
        departarrivee=[]
        for i in range(8):
            for j in range(8):
                piece=self.echiquier[i][j]
                if piece !=0 and piece.couleur==couleur:
                    for x in range(8):
                        for y in range(8):
                            if self.coup_valide((i,j),(x,y),couleur,echiquier) :
                                departarrivee.append([[i,j],[x,y]])
                            else:
                                continue
        return departarrivee
   
    def meilleurcoup(self,joueur): #joueur=couleur
        valeur_pieces={
            'P': 1,
            'N': 3,
            'B':3,
            'R':5,
            'Q':9,
            'K':100 }
       
        diff=float('-inf')
        a=self.obtenir_tous_les_coups()
        for x in a:
            if self.obtenir_piece(x[1].piece)=='K' and self.obtenir_piece(x[0].couleur)!=joueur:
                diff_2=valeur_pieces['K']-valeur_pieces[self.obtenir_piece(x[0].piece)]
                if diff_2>diff:
                    diff_2=diff
                else:
                    continue
       

    def evaluer_echiquier(self,echiquier,joueur):
       
        valeur_pieces={
            'P': 1,
            'N': 3,
            'B':3,
            'R':5,
            'Q':9,
            'K':10 }
        score_total = 0

        for ligne in range(8):
            for colonne in range (8):
                piece=echiquier[ligne][colonne]

                if piece !=0:
                    score_total+=valeur_pieces[piece.symbole]
                    if piece.symbole in ['P','N','B','R','Q']:
                        score_total+=0.1
                    if piece =='K':
                        if self.est_capturable((ligne,colonne),joueur):
                            score_total -=20
        return score_total



   

   

    def minmax(self,joueur,profondeur,echiquier):
        if profondeur==0 or self.echec_et_mat(joueur,echiquier):
            score=self.evaluer_echiquier(echiquier,joueur)
            if joueur==self.joueuradverse(self.joueur):
                score=score
            else:
                score=-score
   
            return score,None
       
        if joueur==self.joueur:
            meilleur_score=float('inf')
        else:
            meilleur_score = float('-inf')
        for coup in self.obtenir_tous_les_coups(joueur,echiquier):
            depart,arrivee=coup
            piece_deplacee=echiquier[depart[0]][depart[1]]
            piece_capturee=echiquier[arrivee[0]][arrivee[1]]
            echiquier[arrivee[0]][arrivee[1]]=piece_deplacee
            echiquier[depart[0]][depart[1]]=0
            score=self.minmax(self.joueuradverse(joueur),profondeur-1,echiquier)[0]

            echiquier[arrivee[0]][arrivee[1]]=piece_capturee
            echiquier[depart[0]][depart[1]]=piece_deplacee

            if joueur==self.joueur:
                if score< meilleur_score:
                    meilleur_score = score
                    meilleur_mouvement= coup
            else:
                if score>meilleur_score:
                    meilleur_score=score
                    meilleur_mouvement=coup
        return meilleur_score,meilleur_mouvement



   
           



def mode():
    i=input('pvp ou vsIA')
    if i!='pvp' and i!='ia':
        print("Veuillez entrer le mode de jeu")
        return mode()
    else:
        return i
def fonction_profondeur():
    profondeur=input("")
    if profondeur.isdigit() is False:
        print("Veuillez entrer un nombre")
        return fonction_profondeur()
    else:
        if  int(profondeur)<+0:
            print("Veuillez entrer un nombre supérieur à 0")
            return fonction_profondeur()
        else:
            return int(profondeur)
class ChessGame2():
   
    def __init__(self):
        self.echiquier = [ [Piece('noir', 'R'), Piece('noir', 'N'), Piece('noir', 'B'), Piece('noir', 'Q'), Piece('noir', 'K'), Piece('noir', 'B'), Piece('noir', 'N'), Piece('noir', 'R')]
                      , [Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P'), Piece('noir', 'P')],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P'), Piece('blanc', 'P')],
                      [Piece('blanc', 'R'), Piece('blanc', 'N'), Piece('blanc', 'B'), Piece('blanc', 'Q'), Piece('blanc', 'K'), Piece('blanc', 'B'), Piece('blanc', 'N'), Piece('blanc', 'R')] ]
       
     

   


 

   
   
        self.tour='blanc'
        self.compteur=1
       

   

    def joueuradverse(self,joueur):
        if joueur=='blanc':
            return 'noir'
        else:
            return'blanc'
       
    def print_board(self,echiquier):
        for i in range(8):
            b=[str(i+1)+" ",]
       
            for j in range(8):
                p=self.obtenir_piece([i,j],echiquier)
                if p==0:
                    b.append("  ")
                else:
                    if p.couleur=='blanc':
                        b.append("W"+str(p.symbole))

                    else:
                        b.append("B"+str(p.symbole))

            print(b,'\n',)
        print(["# ","1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ","8 "])

   

    def changement_tour(self): #projet-echec1
        if self.tour=='blanc':
            self.tour='noir'
            self.compteur+=1
        else:
            self.tour='blanc' #Deux valeurs possibles uniquement 'noir' ou 'blanc'
            self.compteur+=1
 
    def obtenir_piece(self, position,echiquier):


        ligne, colonne = position
       
        return echiquier[ligne][colonne]
   
    def case_roi(self,couleur,echiquier):
        for i in range(8):
            for j in range(8):
                piece=self.obtenir_piece([i,j],echiquier)
                if piece !=0:
                    if piece.couleur==couleur and piece.symbole=='K':
                        return[i,j]
                       
                 

    def est_capturable(self,position,couleur,echiquier):
        piece2=self.obtenir_piece(position,echiquier)
        for i in range(8):    
            for j in range(8):

                piece1=self.obtenir_piece([i,j],echiquier)
                if piece1 !=0 and piece1.couleur!=piece2.couleur:
                    if self.coup_legal((i,j),position,self.joueuradverse(couleur),echiquier) is True:
                        return piece2.symbole, True

    def peut_capturer(self,position,couleur,echiquier):
        a=[]
        for i in range(8):
            for j in range(8):
                if self.obtenir_piece([i,j],echiquier)!=0:
                    if self.coup_valide(position,[i,j],couleur) is True:
                        c=self.obtenir_piece([i,j],echiquier)
                        a.append(c)
                   
        return a                            

    def echec(self,joueur,echiquier):
        roi_case=self.case_roi(joueur,echiquier)
        if self.est_capturable(roi_case,joueur,echiquier):          #on utilise la fonction qui verifie si le mouvement de la piece est autorisé
            return True
        return False    
           


    def jouer(self):
       
        i=input("Pour continuer, appuyez sur entrée \n")
        while self.echec_et_mat(self.tour,self.echiquier) is False:
            self.print_board(self.echiquier)
            self.deroulement()
        print('les',self.joueuradverse(self.tour),'ont gagné')
   
    def deroulement(self):
        if self.tour=='blanc':
            print("C'est au tour des blancs")
            depart=self.choix_piece()
            arrivee=self.choixmouvementjoueur()
            if self.echec(self.tour,self.echiquier):
                    print("Vous êtes en échec")
                    if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                        self.deplacer_piece(depart,arrivee,self.echiquier)
                        t=self.check_promotion_joueur()
                        if t[0]==True:
                            self.promotion_joueur(t[1],t[2],t[3])
                        self.changement_tour()
                    else:
                        print('vous êtes toujours en échec')
            else:
                if self.coup_valide(depart,arrivee,self.tour,self.echiquier) :
                    self.deplacer_piece(depart,arrivee,self.echiquier)
                    t=self.check_promotion_joueur()
                    if t[0]==True:
                        self.promotion_joueur(t[1],t[2],t[3])
                    self.changement_tour()
               
                else:
                    print("Coup impossible, veuillez rejouez")
                    self.deroulement()
                   
        else:
            print("C'est au tour des noirs")
            depart=self.choix_piece()
            arrivee=self.choixmouvementjoueur()
            if self.echec(self.tour,self.echiquier):
                print("Vous êtes en échec")
                if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                    self.deplacer_piece(depart,arrivee,self.echiquier)
                    t=self.check_promotion_joueur()
                    if t[0]==True:
                        self.promotion_joueur(t[1],t[2],t[3])
                    self.changement_tour()
                else:
                    print('vous êtes toujours en échec')
            else:
                if self.coup_valide(depart,arrivee,self.tour,self.echiquier):
                    self.deplacer_piece(depart,arrivee,self.echiquier)
                    t=self.check_promotion_joueur()
                    if t[0]==True:
                        self.promotion_joueur(t[1],t[2],t[3])
                    self.changement_tour()

                else:
                    print("Coup impossible, veuillez rejouez")
                    self.deroulement()
         
       


            if self.echec_et_mat(self.tour,self.echiquier) is True:
                print("C'est finito pour toi, révise tes leçons")
       

    def sauvegarder_etat_echiquier(self,echiquier):
        a=[]
        for i in range(8):
            b=[]
            for j in range (8):
                b.append(echiquier[i][j])
            a.append(b)
        return a


 
    def choix_piece(self):
        ligne=input("Ligne de la pièce à jouer de 1 à 8 ")
        colonne=input("Colonne de la pièce à jouer de 1 à 8 ")
       
        coor=['1','2','3','4','5','6','7','8']
       
        if ligne not in coor or colonne not in coor:
            print("Coordonnées de départ invalides, réessayez !") #Evite les arrêts du programme et donc de recommencer la partie
            return self.choix_piece()
       
        else:
            ligne=int(ligne)-1
            colonne=int(colonne)-1
       
        if self.obtenir_piece([ligne,colonne],self.echiquier)==0:
            print('case vide')
            return self.choix_piece()
        elif self.obtenir_piece([ligne,colonne],self.echiquier).couleur!=self.tour: #Impossible de déplacer une pièce adverse
            print("Pièce adverse !")
            return self.choix_piece()
        else:    
            print(self.obtenir_piece([ligne,colonne],self.echiquier).couleur, self.obtenir_piece([ligne,colonne],self.echiquier).symbole)
            return [ligne,colonne]
       
   
    def deplacer_piece(self,depart,arrivee,echiquier):
        piece=self.obtenir_piece(depart,self.echiquier)
        echiquier[arrivee[0]][arrivee[1]]=piece
        echiquier[depart[0]][depart[1]]=0


       

   
    def choixmouvementjoueur(self):
       
        ligne=input("Case d'arrivée de 1 à 8 ")
        colonne=input("Case d'arrivée de 1 à 8 ")
       
        coor=['1','2','3','4','5','6','7','8']
       
        if ligne not in coor or colonne not in coor:
            print("Coordonnées d'arrivée invalides, veuillez réessayer !")
            return self.choixmouvementjoueur()
       
        else:
            ligne=int(ligne)-1
            colonne=int(colonne)-1
        return [ligne,colonne]

       
   
    def mouvement_type(self,piecedepart,piecearrivee,positiondepart,positionarrivee,echiquier): #position de départ
        x=piecedepart
        if x.symbole=='N':
            return self.cavalier(positiondepart,positionarrivee)
        elif x.symbole=='R':
            return self.rook(piecedepart,positiondepart,positionarrivee)
        elif x.symbole=='B':
            return self.fou(piecedepart,positiondepart,positionarrivee,echiquier)
        elif x.symbole=='K':
            return self.roi(positiondepart,positionarrivee)
        elif x.symbole=='Q':
            return self.reine(piecedepart,positiondepart,positionarrivee,echiquier)
        elif x.symbole=='P':
            return self.pion(piecedepart,piecearrivee,positiondepart,positionarrivee)
                       
    def coup_legal(self,positiondepart,positionarrivee,couleur,echiquier):
        piecedepart=self.obtenir_piece(positiondepart,echiquier)
        piecearrivee=self.obtenir_piece(positionarrivee,echiquier)    
       
        if positionarrivee[0]>7 or positionarrivee[0]<0 or positionarrivee[1]>7 or positionarrivee[1]<0:
            return False
       
        elif piecedepart==0: #On ne peut pas sélectionner une case vide
            return False
       
       
        elif  piecearrivee!=0 and piecedepart.couleur==piecearrivee.couleur: #Impossible de jouer sur une case occupée par ses propres pièces
            return False
       
        elif piecedepart.couleur!=couleur:
            return False #On ne joue pas les pieces des autres
        else:
            return self.mouvement_type(piecedepart,piecearrivee,positiondepart,positionarrivee,echiquier)
       
    def echec_et_mat(self,joueur,echiquier):
        if self.echec(joueur,echiquier) is False:  #cas le plus simple où il n'y a pas d'échec au roi
            return False
        for i in range(8):
            for j in range(8):
                piece=self.obtenir_piece([i,j],echiquier)
                if piece !=0 and piece.couleur==joueur:
                    for x in range(8):
                        for y in range(8):
                            if self.coup_valide((i,j),(x,y),joueur,self.echiquier) :
                                a=self.coup_valide((i,j),(x,y),joueur,self.echiquier)[1]
                                echec=self.echec(joueur,a)
                                if echec is False:
                                    return False

                               
        return True

    def coup_valide(self,positiondepart,positionarrivee,couleur,echiquier):
       
        if self.coup_legal(positiondepart,positionarrivee,couleur,echiquier)==True:
            piecesauvegardee=echiquier[positionarrivee[0]][positionarrivee[1]]
            self.deplacer_piece(positiondepart,positionarrivee,echiquier)
            if self.echec(self.tour,echiquier) or self.echec_et_mat(self.tour,echiquier)==True:
                self.deplacer_piece(positionarrivee,positiondepart,echiquier)
                echiquier[positionarrivee[0]][positionarrivee[1]]=piecesauvegardee
                return False
           
            else:
                a=self.sauvegarder_etat_echiquier(echiquier)
                self.deplacer_piece(positionarrivee,positiondepart,self.echiquier)
                echiquier[positionarrivee[0]][positionarrivee[1]]=piecesauvegardee
                return True,a
        else:
            return False    
   
   

    def cavalier(self,positiondepart,positionarrivee):
        if abs(positiondepart[0]-positionarrivee[0])==2 and abs(positiondepart[1]-positionarrivee[1])==1:
            return True
        if abs(positiondepart[0]-positionarrivee[0])==1 and abs(positiondepart[1]-positionarrivee[1])==2:
            return True
        else:
            return False
       
   



    def rook(self,piecedepart,positiondepart,positionarrivee):
        x=positiondepart[0]
        y=positiondepart[1]
        c=0
        if positiondepart[0]!=positionarrivee[0] and positiondepart[1]!=positionarrivee[1]:
            return False
        elif positiondepart[0]==positionarrivee[0]:
            if positiondepart[1]< positionarrivee[1]:
                for i in range (positiondepart[1]+1,positionarrivee[1]+1):
                    if self.echiquier[x][i]!=0:
                        if i==positionarrivee[1]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True
                           
                   
            if positiondepart[1]>positionarrivee[1]:
                for i in range (positiondepart[1]-1,positionarrivee[1]-1,-1):
                    if self.echiquier[x][i]!=0:
                        if i==positionarrivee[1]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True
                 
        else:
            if positiondepart[0]< positionarrivee[0]:
                for i in range (positiondepart[0]+1,positionarrivee[0]+1):
                    if self.echiquier[i][y]!=0:
                        if i==positionarrivee[0]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True
                   
                   
            if positiondepart[0]>positionarrivee[0]:
                for i in range (positiondepart[0]-1,positionarrivee[0]-1,-1):
                    if self.echiquier[i][y]!=0:
                        if i==positionarrivee[0]:
                            return True
                        else:
                            return False
                    else:
                        continue
                return True

    def fou(self,piecedepart,positiondepart,positionarrivee,echiquier):
        x1=positiondepart[0]
        y1=positiondepart[1]
        x2=positionarrivee[0]
        y2=positionarrivee[1]
       
        if abs(x2-x1)!=abs(y2-y1):
            return False
        else:
            if x1 < x2:
                if y1<y2:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1+i,y1+i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1+i,y1+i],echiquier)!=piecedepart.couleur :
                                return True
                            else:
                                return False
                        else:
                            continue
                   
                    return True
                             
                else:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1+i,y1-i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1+i,y1-i],echiquier)!=piecedepart.couleur :
                                return True
                            else:
                                return False
                        else:
                            continue
                   
                    return True
                           
            else:
                if y1<y2:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1-i,y1+i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1-i,y1+i],echiquier)!=piecedepart.couleur :
                                return True
                            else:
                                return False
                        else:
                            continue
                   
                    return True
                else:
                    for i in range (1,abs(y1-y2)+1):
                        if self.obtenir_piece([x1-i,y1-i],echiquier)!=0:
                            if i==abs(y1-y2) and self.obtenir_piece([x1-i,y1-i],echiquier).couleur!=piecedepart.couleur:
                                return True
                            else:
                                return False
                        else:
                            continue
                    return True
               
       
    def reine(self,piecedepart,positiondepart,positionarrivee,echiquier):
        return self.rook(piecedepart,positiondepart,positionarrivee) or self.fou(piecedepart,positiondepart,positionarrivee,echiquier)        

       
    def pion(self,piecedepart,piecearrivee,positiondepart,positionarrivee):
        x1=positiondepart[0]
        y1=positiondepart[1]
        x2=positionarrivee[0]
        y2=positionarrivee[1]
       
        if piecedepart.couleur=='noir':
            if y1==y2:
                if piecearrivee!=0:
                        return False
                if x1==1:
                    if x2==x1+1 or x2==x1+2:
                        return True
                    else:
                        return False
                else:
                    if x2==x1+1:
                        return True
                    else:
                        return False
                   
            elif abs(y2-y1)==1:
                if  x1-x2==-1:
                    if piecearrivee!=0 and piecearrivee.couleur!='noir':
                        return True
                    else:
                        return False
            else:
                return False
       
        if piecedepart.couleur=='blanc':
            if y1==y2:
                if piecearrivee!=0:
                    return False
                if x1==6:
                    if x2==x1-1 or x2==x1-2:
                        return True
                    else:
                        return False
                else:
                    if x2==x1-1:
                        return True
                    else:
           
                        return False
                   
            elif abs(y2-y1)==1 :
                if x1-x2==1 :
                    if piecearrivee!=0 and piecearrivee.couleur!='blanc':
                        return True
                    else:
                        return False
            else:
                return False

                     

           

   
   
    def roi(self,positiondépart,positionarrivée):
        if abs(positionarrivée[0]-positiondépart[0])<=1 and abs(positionarrivée[1]-positiondépart[1])<=1:
            return True
        else:
            return False
         
               

    def check_promotion_joueur(self):
        for i in range(8):
            a=self.obtenir_piece([7,i],self.echiquier)
            p=i
           
            if a!=0 and self.tour=='noir' and a.couleur=='noir' and a.symbole=='P':
               
                return [True,p,a,7]
            else:
                pass
           
            c=self.obtenir_piece([0,i],self.echiquier)
            p1=i
           
            if c!=0 and c.couleur=='blanc'and self.tour=='blanc' and c.symbole=='P':
                return [True,p1,c,0]
            else:
                pass
               
        return [False,]
           
           


    def promotion_joueur(self,p,c,l):
        b=['P','Q','B','N','R']
        i=input("Promotion ! Quelle pièce choisissez vous ?")
        if i not in b:
            print("Erreur, la pièce n'existe pas")
            self.promotion_joueur(p,c,l)
       
        else:
            self.echiquier[l][p]=Piece(c.couleur,i)
   




    def obtenir_tous_les_coups(self,couleur,echiquier):
        departarrivee=[]
        for i in range(8):
            for j in range(8):
                piece=self.echiquier[i][j]
                if piece !=0 and piece.couleur==self.tour:
                    for x in range(8):
                        for y in range(8):
                            if self.coup_legal((i,j),(x,y),couleur,echiquier)==True and self.echec(couleur,echiquier)==False:
                                departarrivee.append([[i,j],[x,y]])
                            else:
                                continue
        return departarrivee
def main():
        print("Bienvenue au jeu d'échecs! \n Voici les règles : \n \n Le plateau est  verticalement inversé ainsi il faut compter de 1 à 8 en partant de la colonne la plus haute \n Les pièces blanches sont désignées par W, les noires par B \n Le roi est désigné par K \n La reine par Q \n La tour par R \n Le cavalier par N \n Le fou par B \n Les pions par P \n \n Le roque et la prise en passant n'ont pas été implémentés \n")
        i=input("Pour continuer, appuyez sur entrée \n")
        print('choissiez votre mode de jeu')
        u=mode()
        if u=='pvp':
            partie=ChessGame2()
            partie.jouer()



        else:

            print("Choisissez le niveau de l'ordinateur (minimum 1), nous vous conseillons de ne pas dépasser 3 pour une partie fluide \nVeuillez faire preuve de patience")
            profondeur=fonction_profondeur()    
            partie=ChessGame(profondeur)
       
            print("Vous avez choisi la difficulté suivante : "+ str(profondeur)+"\n")
            confirmation=input("Confirmez-vous ? Tapez O (majuscule) pour validez \n")
            if confirmation!= str("O"):
                main()
            else:
                partie.jouer()
   
main()
