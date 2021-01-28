# Requirements

## Construit, i reprezentarea vectorial ̆a a unui text (de minim 500 de cuvinte).

### 
- (0.1p) citirea textului (din fișier)
- (0.2p) preprocesarea textului: împărtirea în propoziții, tokenizare (se pastreaza
doar cuvinte), converteste la litere mici, elimina cuvintele stopwords
- (0.1p) generarea datelor de antrenare: vectori one-hot (pentru cuvântul
t de intrare s, i cuvintele din context)
- (0.6p) învățarea reprezentarii vectoriale, utilizând modelul Skip-gram
- (0.3p) alternativ, puteti utiliza modelul pre-antrenat din libraria gensim
- (0.2p) pentru o list ̆de cuvinte, afișați cuvintele cele mai similare cu acesta
- (0.2) optional: utilizeaza-ți algoritmul t-SNE din libraria sklearn.manifold pentru reducerea dimensionalit
