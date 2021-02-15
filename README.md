# TemuSTS
##  (Non-)Semantic Text Similarity for TEMU projects

Esta rama del proyecto sirve para comparar la similitud de documentos de dos corpus (la rama máster es para comparar a nivel de frase). Se utilizan estrategias de análisis superficial, léxica, sin información semántica.

## Dependencias de python:

spacy == 2.2.4

numpy == 1.18.1


rapidfuzz == 1.0.0
(Es una versión más moderna que el de la rama máster, instalar el requirements.txt de esta rama. Si tiene problemas para instalar esta librera mediante pip, utilize el repositorio github: https://github.com/maxbachmann/rapidfuzz)

spacy, con el modelo para español es_core_news_md"

python -m spacy download es_core_news_md


La única información obligatoria es un directorio de archivos "target" que son los que queremos comparar, y encontrar documentos similares, ya sea a otro ("Source"), o a un conjunto de documentos de corpus de referencia, si no se usa la opción "Source", con oraciones del corpus SPACCC y otros.


La opción de method permite elegir entre usar el algoritmo jaccard o una versión optimizada para velocidad de fuzzy search (por defecto)

El umbral de similitud a partir del cual el programa registra las oraciones se define mediante la opción -u, y por defecto es 0.3 en jaccard, y 93 en fuzzy

<pre>
python TemuSTS.py -h

Usage: TemuSTS.py [options]

Options:

-h, --help            show this help message and exit

-s SOURCE, --source=SOURCE
                        source directory

-o FILEOUT, --fileout=FILEOUT
                        output file, tab-separated values extension (.tsv)

-m METHOD, --method=METHOD
                        Comparison method (jaccard, fuzzy [default]) Fuzzy is
                         faster most of the times

-t TARGET, --target=TARGET
                        target directory

-u UMBRAL, --umbral=UMBRAL
                        similarity threshold (default 93, for jaccard use 0.3)

-r REDACT, --redact=REDACT
                        do not write target sentences

</pre>
## Ejemplo:
For a comparison between a 1000 documents vs 981 documents directories:


### Using Fuzzy Search
<pre>
python TemuSTS.py -s /home/crodri/BSC/similitud_cc/corpus_casos_clinicos/radioccc/ -t /home/crodri/BSC/similitud_cc/corpus_casos_clinicos/oncoccc/ -o radioccc_vs_oncoccc.tsv

(...)
processed  in 1046.357162952423 seconds 17.439286049207052 minutes or 0.2906547674867842 hours using fuzzy
</pre>

### Using jaccard
<pre>

python TemuSTS.py -s /home/crodri/BSC/similitud_cc/corpus_casos_clinicos/radioccc/ -t /home/crodri/BSC/similitud_cc/corpus_casos_clinicos/oncoccc/ -o radioccc_vs_oncoccc_jaccard.tsv -m jaccard


(...)
processed  in 598.6335144042969 seconds 9.977225240071615 minutes or 0.1662870873345269 hours using jaccard

</pre>


La salida es un archivo TSV con información sobre el nombre del documento y los siguientes campos:

source_document | score | target_document



