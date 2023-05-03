import nltk
import string

# nltk.download()

from nltk.book import *
from nltk.corpus import gutenberg
from nltk.corpus import brown
from nltk.collocations import *
from nltk.stem.lancaster import LancasterStemmer
bigram_assoc_measures = nltk.collocations.BigramAssocMeasures()
# question 1

s6 = set(text6)

q1a = sorted(w for w in s6 if w[-3:].lower() == 'ise')
q1b = sorted(w for w in s6 if 'z' in w)
q1c = sorted(w for w in s6 if 'pt' in w)
q1d = sorted(w for w in s6 if w.istitle())

# question 2
ballCorpus = gutenberg.words("chesterton-ball.txt")
ballText = Text(ballCorpus)
ballConcordance = ballText.concordance("however")
ballConcordance

brownCorpus = brown.words(categories='news')
brownText = Text(brownCorpus)
brownConcordance = brownText.concordance("however")
brownConcordance

# question 3
genreFrequency = nltk.ConditionalFreqDist(
    (genre, word.lower())
    for genre in brown.categories()
    for word in brown.words(categories=genre)
)
genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
modals = ['cross', 'salvation', 'empower', 'love', 'laugh', 'escape', 'inflation']
genreFrequency.tabulate(conditions=genres, samples=modals)

# question 4
stops = nltk.corpus.stopwords.words('english')
noStopWords = [w for w in Text(text6) if w.lower() not in stops]
numTopBigrams = 25
minAppearances = 2
finder = BigramCollocationFinder.from_words(noStopWords)
finder.apply_freq_filter(minAppearances)
res = finder.nbest(bigram_assoc_measures.pmi, numTopBigrams)
res


# question 5

def which_language(text):
    possibleLanguages = []
    lower = text.lower()
    languages = ['Achehnese-Latin1', 'Achuar-Shiwiar-Latin1', 'Afaan_Oromo_Oromiffa-Latin1', 'Afrikaans-Latin1',
                 'Aguaruna-Latin1', 'Albanian_Shqip-Latin1', 'Amahuaca-Latin1', 'Amarakaeri-Latin1', 'Arabela-Latin1',
                 'Ashaninca-Latin1', 'Asheninca-Latin1', 'Asturian_Bable-Latin1', 'Aymara-Latin1', 'Balinese-Latin1',
                 'Basque_Euskara-Latin1', 'Bemba-Latin1', 'Bichelamar-Latin1', 'Bikol_Bicolano-Latin1', 'Bora-Latin1',
                 'Breton-Latin1', 'Bugisnese-Latin1', 'Cakchiquel-Latin1', 'Campa_Pajonalino-Latin1',
                 'Candoshi-Shapra-Latin1', 'Caquinte-Latin1', 'Cashibo-Cacataibo-Latin1', 'Cashinahua-Latin1',
                 'Catalan-Latin1', 'Catalan_Catala-Latin1', 'Cebuano-Latin1', 'Chamorro-Latin1', 'Chayahuita-Latin1',
                 'Chechewa_Nyanja-Latin1', 'Chickasaw-Latin1', 'Chinanteco-Ajitlan-Latin1', 'Chuuk_Trukese-Latin1',
                 'Cokwe-Latin1', 'Corsican-Latin1', 'Danish_Dansk-Latin1', 'Dutch_Nederlands-Latin1', 'Edo-Latin1',
                 'English-Latin1', 'Estonian_Eesti-Latin1', 'Faroese-Latin1', 'Fijian-Latin1',
                 'Filipino_Tagalog-Latin1', 'Finnish_Suomi-Latin1', 'French_Francais-Latin1', 'Frisian-Latin1',
                 'Friulian_Friulano-Latin1', 'Galician_Galego-Latin1', 'Garifuna_Garifuna-Latin1',
                 'German_Deutsch-Latin1', 'Greenlandic_Inuktikut-Latin1', 'Guarani-Latin1',
                 'HaitianCreole_Kreyol-Latin1', 'HaitianCreole_Popular-Latin1', 'Hani-Latin1', 'Hausa_Haoussa-Latin1',
                 'Hiligaynon-Latin1', 'Hmong_Miao-Sichuan-Guizhou-Yunnan-Latin1',
                 'Hmong_Miao-SouthernEast-Guizhou-Latin1', 'Hmong_Miao_Northern-East-Guizhou-Latin1', 'Huasteco-Latin1',
                 'Huitoto_Murui-Latin1', 'Hungarian_Magyar-Latin1', 'Ibibio_Efik-Latin1', 'Icelandic_Yslenska-Latin1',
                 'Ido-Latin1', 'Iloko_Ilocano-Latin1', 'Indonesian-Latin1', 'Interlingua-Latin1',
                 'Inuktikut_Greenlandic-Latin1', 'IrishGaelic_Gaeilge-Latin1', 'Italian-Latin1',
                 'Italian_Italiano-Latin1', 'Javanese-Latin1', 'Kaonde-Latin1', 'Kapampangan-Latin1',
                 'Kiche_Quiche-Latin1', 'Kicongo-Latin1', 'Kimbundu_Mbundu-Latin1', 'Kinyamwezi_Nyamwezi-Latin1',
                 'Kinyarwanda-Latin1', 'Kituba-Latin1', 'Latin_Latina-Latin1', 'Latin_Latina-v2-Latin1',
                 'Latvian-Latin1', 'Lingala-Latin1', 'Lozi-Latin1', 'Luba-Kasai_Tshiluba-Latin1',
                 'Luganda_Ganda-Latin1', 'Lunda_Chokwe-lunda-Latin1', 'Luvale-Latin1',
                 'Luxembourgish_Letzebuergeusch-Latin1', 'Madurese-Latin1', 'Makonde-Latin1', 'Malagasy-Latin1',
                 'Malay_BahasaMelayu-Latin1', 'Mam-Latin1', 'Maori-Latin1', 'Mapudungun_Mapuzgun-Latin1',
                 'Marshallese-Latin1', 'Matses-Latin1', 'Mayan_Yucateco-Latin1', 'Mazateco-Latin1',
                 'Mikmaq_Micmac-Mikmaq-Latin1', 'Minangkabau-Latin1', 'Miskito_Miskito-Latin1', 'Mixteco-Latin1',
                 'Nahuatl-Latin1', 'Ndebele-Latin1', 'Ngangela_Nyemba-Latin1', 'NigerianPidginEnglish-Latin1',
                 'Nomatsiguenga-Latin1', 'NorthernSotho_Pedi-Sepedi-Latin1', 'Norwegian-Latin1',
                 'Norwegian_Norsk-Bokmal-Latin1', 'Norwegian_Norsk-Nynorsk-Latin1', 'Nyanja_Chechewa-Latin1',
                 'Nyanja_Chinyanja-Latin1', 'OccitanAuvergnat-Latin1', 'OccitanLanguedocien-Latin1',
                 'Oromiffa_AfaanOromo-Latin1', 'Oshiwambo_Ndonga-Latin1', 'Otomi_Nahnu-Latin1', 'Paez-Latin1',
                 'Palauan-Latin1', 'Picard-Latin1', 'Pipil-Latin1', 'Ponapean-Latin1', 'Portuguese_Portugues-Latin1',
                 'Qechi_Kekchi-Latin1', 'Quechua-Latin1', 'Quichua-Latin1', 'Rarotongan_MaoriCookIslands-Latin1',
                 'Rhaeto-Romance_Rumantsch-Latin1', 'Romani-Latin1', 'Rukonzo_Konjo-Latin1', 'Rundi_Kirundi-Latin1',
                 'Runyankore-rukiga_Nkore-kiga-Latin1', 'Sammarinese-Latin1', 'Samoan-Latin1', 'Sango_Sangho-Latin1',
                 'Sardinian-Latin1', 'ScottishGaelic_GaidhligAlbanach-Latin1', 'Sharanahua-Latin1',
                 'Shipibo-Conibo-Latin1', 'Shona-Latin1', 'Siswati-Latin1', 'SolomonsPidgin_Pijin-Latin1',
                 'Somali-Latin1', 'SouthernSotho_Sotho-Sesotho-Sutu-Sesutu-Latin1', 'Spanish-Latin1',
                 'Spanish_Espanol-Latin1', 'Sukuma-Latin1', 'Sundanese-Latin1', 'Swaheli-Latin1',
                 'Swahili_Kiswahili-Latin1', 'Swedish_Svenska-Latin1', 'Tenek_Huasteco-Latin1', 'Tetum-Latin1',
                 'Tiv-Latin1', 'Tojol-abal-Latin1', 'TokPisin-Latin1', 'Tonga-Latin1', 'Tongan_Tonga-Latin1',
                 'Totonaco-Latin1', 'Trukese_Chuuk-Latin1', 'Tzeltal-Latin1', 'Tzotzil-Latin1', 'Uighur_Uyghur-Latin1',
                 'Umbundu-Latin1', 'Urarina-Latin1', 'Uzbek-Latin1', 'Vlach-Latin1', 'Walloon_Wallon-Latin1',
                 'Waray-Latin1', 'Wayuu-Latin1', 'Welsh_Cymraeg-Latin1', 'WesternSotho_Tswana-Setswana-Latin1',
                 'Wolof-Latin1', 'Xhosa-Latin1', 'Yagua-Latin1', 'Yao-Latin1', 'Yapese-Latin1', 'Zapoteco-Latin1',
                 'Zapoteco-SanLucasQuiavini-Latin1', 'Zhuang-Latin1', 'Zulu-Latin1']
    for l in languages:
        words = nltk.corpus.udhr.words(l)
        if lower in words:
            possibleLanguages.append(l)
    return possibleLanguages

print(which_language('hi'))


#question 6
def unusual_words(text):
    st = LancasterStemmer()
    text_vocab = set(st.stem(w.lower()) for w in text if w.isalpha())
    english_vocab = set(st.stem(w.lower()) for w in nltk.corpus.words.words())
    unusual = text_vocab - english_vocab
    return(unusual)

print(unusual_words(nltk.corpus.brown.words()))