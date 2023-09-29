# maximum-map-labeling

U ovom repozitorijumu se nalazi kod za resavanje sledeceg probema:

https://www.csc.kth.se/~viggo/wwwcompendium/node269.html#8287

Prezentacija se moze pronaci [ovde](https://www.canva.com/design/DAFvwybebbI/6tOCjgIs04zlCXa-88sKJQ/view).

## Podesavanje

Opciono napraviti i aktivirati virtualno okruženje:
```
virtualenv env
source env/bin/activate
```

Instalirati potrebne biblioteke:
```
pip install -r requirements
```

## Pokretanje

Pokretanje skripte se vrši sledećom komandom:
```
python main.py --points=5 --map-size=100 --seed=42
```

Fleg `--points` ili `-p` je obavezan i predstavlja broj tacaka na mapi.
Fleg `--map-size` ili `-m` nije obavezan i predstavlja velicinu kvadratne mape.
Fleg `--seed` ili `-s` nije obevezan i predstavlja seed koji se prosledjuje prilikom generisanja
nasumicnih tacaka mape.

### Merenje performansi
Podesiti parametre merenja i zeljene pretrage na pocetku fajla `measure.py`. Nakon toga pokrenuti:
```
python measure.py
```

Rezultat merenja je `.csv` tabela koja se moze naci u folderu `results`.

## Geometrija

U modulu `geometry` se nalaze klase `Point`, `Square` i `Map`.

### Point
Jednostavna klasa koja se sastoji od `x` i `y` koordinata i implementira nekoliko metoda za laksi
rad sa tackama.

### Square

Klasa koja predstavlja kvadrat a sastoji se od sledecih atributa:
* `point` - instanca klase `Point` koja predstavlja pocetnu tacku kvadrata
* `orientation` - pravac u koji se prostire kvadrat naspram pocetne tacke
* `size` - velicina ivice kvadrata
* `edge_*` - `x` odnosno `y` koordinata leve, desne, donje i gornje ivice kvadrata

Pored toga implementira neke staticke i ne staticke metode koje se koriste u pretragama.

### ProtoSquare

Jednostavniji oblik `Square` klase i sastoji se samo od atributa `point` i `orientation`.

### Map

Klasa koja predstavlja kvadratnu mapu na kojoj se nalaze tacke za koje je potrebno izvrsiti pretragu.
Za iniciranje ove klase potrebni su broj tacaka, velicina i seed. Atributi:
* `seed`
* `num_of_points`
* `size`
* `points` - lista generisanih instanci klase `Point`
* `limits_of_points` - granice svake od tacaka u 4 moguce strane
* `square_size_candidates` - lista `float`-ova koja predstavlja kandidate za optimalnu velicinu


## Pretrage

### Search

`Search` je osnovna abstraktna klasa koju nasledjuje ostale klase. Jedinu metodu koju implementira
je `search_with_time_measure` koja vrsi pretragu i meri trajanje iste.

### OptimalSearch

Apstraktna klasa koja vrsi binarnu pretragu po kandidatima kvadrata i za svaku velicinu proverava
da li je moguce postaviti kvadrate bez preseka.

### BruteForce

Nasledjuje `OptimalSearch`, za zadatu velicinu proverava sve moguce kombinacije postavljanja kvadrata.

### BruteForceCache

Nasledjuje `BruteForce`, ako je pretraga vec pokretana za zadate parametre ucitava rezultat iz fajla.
Ako nije vrsi se pretraga i rezultat se cuva u `cache` direktorijumu.

### B

Nasledjuje `OptimalSearch`. Pretraga bazirana na sledecem radu: https://www.sciencedirect.com/science/article/pii/S0925772196000077

### Genetic

Jednostavan genetski algoritam. Hromozom je predstavljen nizom orijentacja koje mogu
imati vrednost `'ne'`, `'nw'`, `'sw'`, `'se'` i velicinom kvadrata.
Sledeci parametri se prosledjuju prilikom iniciranja algoritma:
* `map` - instanca klase `Map` koju treba pretraziti
* `iterations` - broj generacija
* `population_size` - broj jedinki u populaciji
* `elitism_size` - velicina elitne populacije u procentima
* `tournament_size` - velicina turnira
* `mutation_prob` - verovatnoca mutacije

### ImprovedGenetic

TODO

## Radovi
https://www.sciencedirect.com/science/article/pii/S0925772196000077

https://dspace.cvut.cz/bitstream/handle/10467/69496/F3-DP-2017-Chamra-Tomas-thesis.pdf
https://arxiv.org/pdf/1712.05936.pdf
http://www.eecs.harvard.edu/~shieber/Biblio/Papers/tog-final.pdf
https://www.mdpi.com/2220-9964/6/11/342/htm
http://www.lac.inpe.br/~lorena/missae/sbc_Missae.pdf
http://www.cs.uu.nl/research/techreps/repo/CS-2000/2000-22.pdf
https://www.ac.tuwien.ac.at/wp/wp-content/uploads/Martin-N%C3%B6llenburg-dynlab.pdf


## Napomene

Sever je pozitivno y.
Istok je pozitivno x.

## TODO

* Refaktorisati B algoritam
* Optimizovati Genetic Search
* Napistai Binary Genetic Search
