import random
import logging
import json
from itertools import combinations, filterfalse

logger = logging.getLogger(__name__)


class BalanceService:
    def CombinaisonsJoueurs(self, listeNJEJ):
        logger.info('Création liste équipe possible')
        EquipesPossibles = combinations(listeNJEJ, 4)
        EquipesPossibles = list(EquipesPossibles)

        result = []
        
        for equipe in EquipesPossibles:
            equipe = list(equipe) \
            + list(filterfalse(lambda joueur: joueur in equipe, listeNJEJ))
            result.append(equipe)
        return result

    def EquilibrageEquipes(self, listeJoueur):
        logger.info('Service Equilibrage d\'équipe')
        combinaisonPossible = self.CombinaisonsJoueurs(listeJoueur)
        listeJoueurRandomiser = list(listeJoueur)
        logger.info('Equipe initiale : ' + json.dumps(listeJoueurRandomiser))

        eloSumSave = self.CalculEloEquipes(listeJoueur)
    
        for combinaison in combinaisonPossible:
            eloSumCalculated = self.CalculEloEquipes(combinaison)
            if self.differenceEloEquipe(eloSumCalculated) < self.differenceEloEquipe(eloSumSave):
                listeJoueur = list(combinaison)
                eloSumSave = eloSumCalculated
            if eloSumSave == 0:
                return listeJoueur
        self.enregistrementTeam(listeJoueur)
        logger.info('Repartition d\'équipe finale : ' +
                    json.dumps(listeJoueur))
        return listeJoueur

    def enregistrementTeam(self, listeJoueur): 
        return 'NotImplemented'

    def differenceEloEquipe(self, EloSumEquipe):
        logger.info('Calcul de la différence de niveau de l\'équipe : ' +
                    str(abs(EloSumEquipe[0]-EloSumEquipe[1])))
        return abs(EloSumEquipe[0]-EloSumEquipe[1])

    def melangeEquipe(self, listeJoueur):
        random.shuffle(listeJoueur)
        logger.info('Melange aléatoire de l\'équipe : ' +
                    json.dumps(listeJoueur))

    def CalculEloEquipes(self, listeJoueur):
        logger.info('Calcul Niveau de l\'équipe')
        SumE1 = 0
        SumE2 = 0
        c = 0
        while c < 4:
            SumE1 += listeJoueur[c]["rating"]
            SumE2 += listeJoueur[c+4]["rating"]
            c += 1
        sortie = [SumE1, SumE2]
        return sortie

    def CalculBonusEco(self, listeJoueur):
        logger.info('Calcul du bonus ECO de l\'équipe')
        liste = [0, 0]
        CompteurEquipe = 0
        while CompteurEquipe < 2:
            CompteurJoueur = 0
            while CompteurJoueur < 4:
                RangCiv = self.ListeCiv.index(
                    listeJoueur[CompteurJoueur+4*CompteurEquipe]['civ'])
                NoteCiv = self.BonusEco[RangCiv][1]
                liste[CompteurEquipe] += NoteCiv
                CompteurJoueur += 1
            CompteurEquipe += 1
        return liste
    # Retourne une liste avec la note des bonus civ de chaque équipe.

    def EquivalenceBonusEco(self, liste):
        logger.info('Calcul Equivalence Bonus Eco')
        if abs(liste[1]-liste[0]) < random.randint(0, 5):
            return 0
        return 1
    # Vérification que les bonus eco des civs sont assez équilibrés.

    def creationEquipe(self, equipeExemple, equipeCible): 
        compteurPala = self.compteurCivPala(equipeExemple)
        compteurChalou = self.compteurCivChaLou(equipeExemple)
        return self.creationEquipeCible(equipeCible, compteurPala, compteurChalou)

    def compteurCivPala(self, equipe):
        return 'NotImplemented'

    def compteurCivChaLou(self, equipe):
        return 'NotImplemented'

    def creationEquipeCible(self, equipe, compteurPala, compteurChalou):
        return 'NotImplemented'
        
    def TirageSortCiv(self, listeJoueurs):
        logger.info('Determination des Civ et position')
        CopieListeJoueurs = list(listeJoueurs)
        CopieCivPocket = list(self.CivPocket)
        CopieCivFlank = list(self.CivFlank)
        config = [[1, CopieCivFlank], [2, CopieCivPocket],
                  [3, CopieCivPocket], [4, CopieCivFlank]]
        listeResultatJoueur = []
        numeroEquipe = 0
        while numeroEquipe < 2:
            numeroJoueur = 0
            while numeroJoueur < 4:
                joueur = CopieListeJoueurs.pop(
                    random.randint(0, 3-numeroJoueur))
                # On va maintenant  supprimer cette civilisation de la liste en question pour ne pas qu'un autre joueur tombe dessus, il y a donc 2 cas (cf CivPocket et CivFlank)
                joueur['color'] = self.calculPositionEquipe(
                    config[numeroJoueur], numeroEquipe)
                joueur['civ'] = self.popCiv(config[numeroJoueur][1])
                logger.info('Joueur : ' + json.dumps(joueur))
                listeResultatJoueur.append(joueur)
                numeroJoueur += 1
            numeroEquipe += 1
        return listeResultatJoueur
    # Fonction permettant d'attribuer au hasard des civs et des positions à chaque joueur en évitant les doublons mais pas forcément les inégalités au niveau des bonus eco. La sortie est sous format (NomJoueur,Couleur,Civ)

    def popCiv(self, listCivilization):
        random.shuffle(listCivilization)
        return listCivilization.pop()

    def calculPositionEquipe(self, config, numeroEquipe):
        return config[0] + 4*numeroEquipe

    # Partie donnnées:

    ListeCiv = ['Aztecs', 'Berbers', 'Britons', 'Bulgarians', 'Burmese', 'Byzantines', 'Celts', 'Chinese', 'Cumans', 'Ethiopians', 'Franks', 'Goths', 'Huns', 'Incas', 'Indians', 'Italians', 'Japanese',
                'Khmer', 'Koreans', 'Lithuanians', 'Magyars', 'Malay', 'Malians', 'Mayans', 'Mongols', 'Persians', 'Portuguese', 'Saracens', 'Slavs', 'Spanish', 'Tatars', 'Teutons', 'Turks', 'Vietnamese', 'Vikings']
    # Simple liste des civilisations par ordre alphabétique.

    BonusEco = [['Aztecs', 10], ['Berbers', 5], ['Britons', 9], ['Bulgarians', 5], ['Burmese', 7], ['Byzantines', 6], ['Celts', 7], ['Chinese', 8], ['Cumans', 6], ['Ethiopians', 6], ['Franks', 8], ['Goths', 5], ['Huns', 9], ['Incas', 6], ['Indians', 9], ['Italians', 7], ['Japanese', 6], [
        'Khmer', 11], ['Koreans', 4], ['Lithuanians', 6], ['Magyars', 4], ['Malay', 8], ['Malians', 9], ['Mayans', 10], ['Mongols', 8], ['Persians', 10], ['Portuguese', 5], ['Saracens', 4], ['Slavs', 8], ['Spanish', 7], ['Tatars', 5], ['Teutons', 5], ['Turks', 6], ['Vietnamese', 7], ['Vikings', 10]]
    # Civilisations notées en fonction de la puissance de leur bonus éco sur une map de type arabia (8 moutons, 2 sangliers des baies et des cerfs, mais pas de poissons).

    CivPocket = ['Berbers', 'Bulgarians', 'Burmese', 'Chinese', 'Cumans', 'Franks', 'Goths', 'Huns', 'Indians', 'Khmer',
                 'Lithuanians', 'Malians', 'Magyars', 'Mongols', 'Persians', 'Slavs', 'Spanish', 'Tatars', 'Teutons', 'Turks']
    # Civilisations que les joueurs experts ont estimé être viable en pocket sur une map type Arabia.

    CivFlank = ['Aztecs', 'Britons', 'Byzantines', 'Celts', 'Chinese', 'Ethiopians', 'Incas', 'Italians', 'Japanese',
                'Koreans', 'Malay', 'Mayans', 'Mongols', 'Portuguese', 'Saracens', 'Tatars', 'Vietnamese', 'Vikings']
    # Civilisations que les joueurs experts ont estimé être viable en flank sur une map type Arabia.

    # Partie entrée:

    def run(self, listeJoueur):
        logger.info('Lancement de l\'équilibrage : ')
        ListeBonus = [0, 3]
        listeJoueur = self.EquilibrageEquipes(listeJoueur)
        listeJoueur = self.TirageSortCiv(listeJoueur)
        ListeBonus = self.CalculBonusEco(listeJoueur)
        while self.EquivalenceBonusEco(ListeBonus) != 0:
            listeJoueur = self.TirageSortCiv(listeJoueur)
            ListeBonus = self.CalculBonusEco(listeJoueur)

        logger.info('Match Final : ' + json.dumps(listeJoueur))


print("Idée de only_ju, codé par Rokafly et Spirit_White sur les conseils de Barney, OGN, Sitaux et Slidou.")
