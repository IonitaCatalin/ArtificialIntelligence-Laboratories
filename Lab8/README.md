# Requirements

## Construit, i reprezentarea vectorial ̆a a unui text (de minim 500 de cuvinte).

### 
- (0.1p) citirea textului (din fis, ier)
- (0.2p) preprocesarea textului: ˆımp ̆art, irea ˆın propozit, ii, tokenizare (p ̆astreaz ̆a
doar cuvinte), convertes, te la litere mici, elimin ̆a cuvintele stopwords (o
list ̆a de stopwords poate fi descarcat ̆a de aici)
- (0.1p) generarea datelor de antrenare: vectori one-hot (pentru cuvˆantul
t, int ̆a s, i cuvintele din context)
- (0.6p) ˆınv ̆at,area reprezent ̆arii vectoriale, utilizˆand modelul Skip-gram
- (0.3p) alternativ, puteti utiliza modelul pre-antrenat din libraria gensim
- (0.2p) pentru o list ̆a de cuvinte, afis,at, i cuvintele cele mai similare cu aces-
tea
- (0.2) opt, ional: utilizeaz ̆a algoritmul t-SNE din libraria sklearn.manifold pentru reducerea dimensionalit ̆at, ii s, i pentru vizualizarea vectorilor de cu-
vinte
