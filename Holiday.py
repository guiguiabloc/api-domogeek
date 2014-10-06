#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Source : Les recettes Python de Tyrtamos
         http://python.jpvweb.com/mesrecettespython/doku.php?id=date_de_paques
"""


class jourferie:

  def datepaques(self,an):
      """Calcule la date de Pâques d'une année donnée an (=nombre entier)"""
      a=an//100
      b=an%100
      c=(3*(a+25))//4
      d=(3*(a+25))%4
      e=(8*(a+11))//25
      f=(5*a+b)%19
      g=(19*f+c-e)%30
      h=(f+11*g)//319
      j=(60*(5-d)+b)//4
      k=(60*(5-d)+b)%4
      m=(2*j-k-g+h)%7
      n=(g-h+m+114)//31
      p=(g-h+m+114)%31
      jour=p+1
      mois=n
      return [jour, mois, an]
  
  def dateliste(self,c, sep='/'):
      """Transforme une date chaîne 'j/m/a' en une date liste [j,m,a]"""
      j, m, a = c.split(sep)
      return [int(j), int(m), int(a)]
  
  def datechaine(self,d, sep='/'):
      """Transforme une date liste=[j,m,a] en une date chaîne 'jj/mm/aaaa'"""
      return ("%02d" + sep + "%02d" + sep + "%0004d") % (d[0], d[1], d[2])
  
  
  def jourplus(self,d, n=1):
      """Donne la date du nième jour suivant d=[j, m, a] (n>=0)"""
      j, m, a = d
      fm = [0,31,28,31,30,31,30,31,31,30,31,30,31]
      if (a%4==0 and a%100!=0) or a%400==0:  # bissextile?
          fm[2] = 29
      for i in xrange(0,n):
          j += 1
          if j > fm[m]:
              j = 1
              m += 1
              if m>12:
                  m = 1
                  a += 1
      return [j,m,a]
  
  def jourmoins(self,d, n=-1):
      """Donne la date du nième jour précédent d=[j, m, a] (n<=0)"""
      j, m, a = d
      fm = [0,31,28,31,30,31,30,31,31,30,31,30,31]
      if (a%4==0 and a%100!=0) or a%400==0:  # bissextile?
          fm[2] = 29
      for i in xrange(0,abs(n)):
          j -= 1
          if j < 1:
              m -= 1
              if m<1:
                  m = 12
                  a -= 1
              j = fm[m]
      return [j,m,a]
  
  
  def numjoursem(self,d):
      """Donne le numéro du jour de la semaine d'une date d=[j,m,a]
         lundi=1, mardi=2, ..., dimanche=7
         Algorithme de Maurice Kraitchik (1882?1957)"""
      j, m, a = d
      if m<3:
          m += 12
          a -= 1
      n = (j +2*m + (3*(m+1))//5 +a + a//4 - a//100 + a//400 +2) % 7
      return [6, 7, 1, 2, 3, 4, 5][n]
   
  def joursem(self,d):
      """Donne le jour de semaine en texte à partir de son numéro
         lundi=1, mardi=2, ..., dimanche=7"""
      return ["", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
               "dimanche"][self.numjoursem(d)]
  
  def joursferiesliste(self,an, sd=0):
      """Liste des jours fériés France en date-liste de l'année an (nb entier). 
           sd=0 (=defaut): tous les jours fériés. 
           sd=1: idem sans les sammedis-dimanches. 
           sd=2: tous + les 2 jours fériés supplémentaires d'Alsace-Moselle. 
           sd=3: idem sd=2 sans les samedis-dimanches"""
      F = []  # =liste des dates des jours feries en date-liste d=[j,m,a]
      L = []  # =liste des libelles du jour ferie
      dp = self.datepaques(an)
   
      # Jour de l'an
      d = [1,1,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Jour de l'an")
   
      # Vendredi saint (pour l'Alsace-Moselle)
      d = self.jourmoins(dp, -2)
      if sd>=2:
          F.append(d)
          L.append(u"Vendredi saint (Alsace-Moselle)")
   
      # Dimanche de Paques
      d = dp
      if (sd==0) or (sd==2):
          F.append(d)
          L.append(u"Dimanche de Paques")
   
      # Lundi de Paques
      d = self.jourplus(dp, +1)
      F.append(d)
      L.append(u"Lundi de Paques")
   
      # Fête du travail
      d = [1,5,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Fete du travail")
   
      # Victoire des allies 1945
      d = [8,5,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Victoire des allies 1945")
   
      # Jeudi de l'Ascension
      d = self.jourplus(dp, +39)
      F.append(d)
      L.append(u"Jeudi de l'Ascension")
   
      # Dimanche de Pentecote
      d = self.jourplus(dp, +49)
      if (sd==0) or (sd==2):
          F.append(d)
          L.append(u"Dimanche de Pentecote")
   
      # Lundi de Pentecote
      d = self.jourplus(d, +1)
      F.append(d)
      L.append(u"Lundi de Pentecote")
   
      # Fete Nationale
      d = [14,7,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Fete Nationale")
   
      # Assomption
      d = [15,8,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Assomption")
   
      # Toussaint
      d = [1,11,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Toussaint")
   
      # Armistice 1918
      d = [11,11,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Armistice 1918")
   
      # Jour de Noel
      d = [25,12,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Jour de Noel")

      # Saint Etienne Alsace
      d = [26,12,an]
      nj = self.numjoursem(d)
      if (sd==0) or (sd==1 and nj<6) or (sd==2) or (sd==3 and nj<6):
          F.append(d)
          L.append(u"Saint-Etienne (Alsace)")
   
      return F, L
  
  def joursferies(self,an, sd=0, sep='/'):
      """Liste des jours fériés France en date-chaine de l'année an (nb entier). 
           sd=0 (=defaut): tous les jours fériés. 
           sd=1: idem sans les sammedis-dimanches. 
           sd=2: tous + les 2 jours fériés supplémentaires d'Alsace-Moselle. 
           sd=3: idem sd=2 sans les samedis-dimanches"""
      C = []
      J = []
      F, L = self.joursferiesliste(an, sd)
      for i in xrange(0,len(F)):
          C.append(self.datechaine(F[i]))  # conversion des dates-liste en dates-chaine
          J.append(self.joursem(F[i]))  # ajout du jour de semaine
      return C, J, L
  
  def estferie(self,d,sd=0):
      """estferie(d,sd=0): => dit si une date d=[j,m,a] donnée est fériée France
         si la date est fériée, renvoie son libellé
         sinon, renvoie une chaine vide"""
      j,m,a = d
      F, L = self.joursferiesliste(a, sd)
      for i in xrange(0, len(F)):
          if j==F[i][0] and m==F[i][1] and a==F[i][2]:
              return L[i]
      return "False"    

