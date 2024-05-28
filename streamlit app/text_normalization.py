import re
import string
import unicodedata
import nltk
from nltk.tokenize import word_tokenize, RegexpTokenizer
# from spellchecker import SpellChecker
import spacy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

# RegexpTokenizer
regexp = RegexpTokenizer("[\w']+")


def convert_to_lowercase(text):
    return text.lower()


def remove_whitespace(text):
    return text.strip()


def remove_http(text):
    http = "https?://\S+|www\.\S+" # matching strings beginning with http (but not just "http")
    pattern = r"({})".format(http) # creating pattern
    return re.sub(pattern, "", text)


def remove_punctuation(text):
    punct_str = string.punctuation
    punct_str = punct_str.replace("'", "") # discarding apostrophe from the string to keep the contractions intact
    return text.translate(str.maketrans("", "", punct_str))


def remove_html(text):
    return re.sub(r'<.*?>', '', text)


def remove_emoji(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)


def remove_problematic(text):
    # Remove non-ASCII characters using regular expression
    text = re.sub(r'[^\x00-\x7F]+', "'", text)
    # Normalize and encode to remove any remaining non-ASCII characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # Remove any double spaces that may have been introduced
    text = re.sub(' +', ' ', text)
    return text.strip()


acronyms_dict = {
    "aka": "also known as",
    "asap": "as soon as possible",
    "brb": "be right back",
    "btw": "by the way",
    "dob": "date of birth",
    "faq": "frequently asked questions",
    "fyi": "for your information",
    "idk": "i don't know",
    "idc": "i don't care",
    "iirc": "if i recall correctly",
    "imo": "in my opinion",
    "irl": "in real life",
    "lmk": "let me know",
    "lol": "laugh out loud",
    "ngl": "not gonna lie",
    "noyb": "none of your business",
    "nvm": "never mind",
    "ofc": "of course",
    "omg": "oh my god",
    "pfa": "please find attached",
    "rofl": "rolling on the floor laughing",
    "stfu": "shut the fuck up",
    "tba": "to be announced",
    "tbc": "to be continued",
    "tbd": "to be determined",
    "tbh": "to be honest",
    "ttyl": "talk to you later",
    "wtf": "what the fuck",
    "wth": "what the heck"
}
acronyms_list = list(acronyms_dict.keys())

def convert_acronyms(text):
    words = []
    for word in regexp.tokenize(text):
        if word in acronyms_list:
            words = words + acronyms_dict[word].split()
        else:
            words = words + word.split()

    text_converted = " ".join(words)
    return text_converted


contractions_dict = {
    "'aight": "alright",
    "ain't": "are not",
    "amn't": "am not",
    "arencha": "are not you",
    "aren't": "are not",
    "'bout": "about",
    "can't": "cannot",
    "cap'n": "captain",
    "'cause": "because",
    "'cept": "except",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "dammit": "damn it",
    "daren't": "dare not",
    "daresn't": "dare not",
    "dasn't": "dare not",
    "didn't": "did not",
    "doesn't": "does not",
    "doin'": "doing",
    "don't": "do not",
    "dunno": "do not know",
    "d'ye": "do you",
    "e'en": "even",
    "e'er": "ever",
    "'em": "them",
    "everybody's": "everybody is",
    "everyone's": "everyone is",
    "fo'c'sle": "forecastle",
    "finna": "fixing to",
    "'gainst": "against",
    "g'day": "good day",
    "gimme": "give me",
    "giv'n": "given",
    "gonna": "going to",
    "gon't": "go not",
    "gotcha": "got you",
    "gotta": "got to",
    "gtg": "got to go",
    "hadn't": "had not",
    "had've": "had have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he had",
    "he'll": "he shall",
    "helluva": "hell of a",
    "he's": "he is",
    "here's": "here is",
    "he've": "he have",
    "how'd": "how would",
    "howdy": "how do you do",
    "how'll": "how will",
    "how're": "how are",
    "how's": "how is",
    "i'd": "i would",
    "i'd've": "i would have",
    "i'll": "i shall",
    "i'm": "i am",
    "imma": "i am about to",
    "i'm'a": "i am about to",
    "i'm'o": "i am going to",
    "innit": "is it not",
    "ion": "i do not",
    "i've": "i have",
    "i'd": "i had",
    "i'd've": "i would have",
    "i'll": "i shall",
    "i'm": "i am",
    "i'm'a": "i am about to",
    "i'm'o": "i am going to",
    "innit": "is it not",
    "i've": "i have",
    "isn't": "is not",
    "it'd": "it would",
    "it'll": "it shall",
    "it's": "it is",
    "iunno": "i do not know",
    "kinda": "kind of",
    "let's": "let us",
    "li'l": "little",
    "ma'am": "madam",
    "mayn't": "may not",
    "may've": "may have",
    "methinks": "me thinks",
    "mightn't": "might not",
    "might've": "might have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "must've": "must have",
    "'neath": "beneath",
    "needn't": "need not",
    "nal": "and all",
    "ne'er": "never",
    "o'clock": "of the clock",
    "o'er": "over",
    "ol'": "old",
    "oughtn't": "ought not",
    "'round": "around",
    "'s": "is",
    "shalln't": "shall not",
    "shan't": "shall not",
    "she'd": "she had",
    "she'll": "she shall",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "somebody's": "somebody is",
    "someone's": "someone is",
    "something's": "something is",
    "so're": "so are",
    "so's": "so is",
    "so've": "so have",
    "that'll": "that shall",
    "that're": "that are",
    "that's": "that is",
    "that'd": "that would",
    "there'd": "there had",
    "there'll": "there shall",
    "there're": "there are",
    "there's": "there is",
    "these're": "these are",
    "these've": "these have",
    "they'd": "they had",
    "they'll": "they shall",
    "they're": "they are",
    "they've": "they have",
    "this's": "this is",
    "those're": "those are",
    "those've": "those have",
    "'thout": "without",
    "'til": "until",
    "'tis": "it is",
    "to've": "to have",
    "'twas": "it was",
    "'tween": "between",
    "'twhere": "it were",
    "wanna": "want to",
    "wasn't": "was not",
    "we'd": "we had",
    "we'd've": "we would have",
    "we'll": "we shall",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "whatcha": "what are you",
    "what'd": "what did",
    "what'll": "what shall",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "where'd": "where did",
    "where'll": "where shall",
    "where're": "where are",
    "where's": "where is",
    "where've": "where have",
    "which'd": "which had",
    "which'll": "which shall",
    "which're": "which are",
    "which's": "which is",
    "which've": "which have",
    "who'd": "who would",
    "who'd've": "who would have",
    "who'll": "who shall",
    "who're": "who are",
    "who's": "who is",
    "who've": "who have",
    "why'd": "why did",
    "why're": "why are",
    "why's": "why is",
    "willn't": "will not",
    "won't": "will not",
    "wonnot": "will not",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'all'd've": "you all would have",
    "y'all'd'n't've": "you all would not have",
    "y'all're": "you all are",
    "y'all'ren't": "you all are not",
    "y'at": "you at",
    "yes'm": "yes madam",
    "yessir": "yes sir",
    "you'd": "you had",
    "you'll": "you shall",
    "you're": "you are",
    "you've": "you have",
    "aight": "alright",
    "aint": "are not",
    "amnt": "am not",
    "arent": "are not",
    "cant": "cannot",
    "cause": "because",
    "couldve": "could have",
    "couldnt": "could not",
    "couldntve": "could not have",
    "darent": "dare not",
    "daresnt": "dare not",
    "dasnt": "dare not",
    "didnt": "did not",
    "doesnt": "does not",
    "doin": "doing",
    "dont": "do not",
    "eer": "ever",
    "everybodys": "everybody is",
    "everyones": "everyone is",
    "finna": "fixing to",
    "gday": "good day",
    "givn": "given",
    "gont": "go not",
    "hadnt": "had not",
    "hadve": "had have",
    "hasnt": "has not",
    "havent": "have not",
    "hed": "he had",
    "hell": "he shall",
    "hes": "he is",
    "heve": "he have",
    "howd": "how did",
    "howdy": "how do you do",
    "howll": "how will",
    "howre": "how are",
    "hows": "how is",
    "idve": "i would have",
    "ill": "i shall",
    "im": "i am",
    "ima": "i am about to",
    "imo": "i am going to",
    "innit": "is it not",
    "ive": "i have",
    "isnt": "is not",
    "itd": "it would",
    "itll": "it shall",
    "its": "it is",
    "lets": "let us",
    "lil": "little",
    "maam": "madam",
    "maynt": "may not",
    "mayve": "may have",
    "methinks": "me thinks",
    "mightnt": "might not",
    "mightve": "might have",
    "mustnt": "must not",
    "mustntve": "must not have",
    "mustve": "must have",
    "neednt": "need not",
    "neer": "never",
    "oclock": "of the clock",
    "oer": "over",
    "ol": "old",
    "oughtnt": "ought not",
    "shallnt": "shall not",
    "shant": "shall not",
    "shed": "she had",
    "shell": "she shall",
    "shes": "she is",
    "shouldve": "should have",
    "shouldnt": "should not",
    "shouldntve": "should not have",
    "somebodys": "somebody is",
    "someones": "someone is",
    "somethings": "something is",
    "thatll": "that shall",
    "thatre": "that are",
    "thatd": "that would",
    "thered": "there had",
    "therell": "there shall",
    "therere": "there are",
    "theres": "there is",
    "thesere": "these are",
    "theseve": "these have",
    "theyd": "they had",
    "theyll": "they shall",
    "theyre": "they are",
    "theyve": "they have",
    "thiss": "this is",
    "thosere": "those are",
    "thoseve": "those have",
    "tis": "it is",
    "tove": "to have",
    "twas": "it was",
    "wanna": "want to",
    "wasnt": "was not",
    "wed": "we had",
    "wedve": "we would have",
    "were": "we are",
    "weve": "we have",
    "werent": "were not",
    "whatd": "what did",
    "whatll": "what shall",
    "whatre": "what are",
    "whats": "what is",
    "whatve": "what have",
    "whens": "when is",
    "whered": "where did",
    "wherell": "where shall",
    "wherere": "where are",
    "wheres": "where is",
    "whereve": "where have",
    "whichd": "which had",
    "whichll": "which shall",
    "whichre": "which are",
    "whichs": "which is",
    "whichve": "which have",
    "whod": "who would",
    "whodve": "who would have",
    "wholl": "who shall",
    "whore": "who are",
    "whos": "who is",
    "whove": "who have",
    "whyd": "why did",
    "whyre": "why are",
    "whys": "why is",
    "wont": "will not",
    "wouldve": "would have",
    "wouldnt": "would not",
    "wouldntve": "would not have",
    "yall": "you all",
    "yalldve": "you all would have",
    "yallre": "you all are",
    "youd": "you had",
    "youll": "you shall",
    "youre": "you are",
    "youve": "you have",
    "'re": "are",
    "that's": "that is",
    "thats": "that is"
}
# List of contractions
contractions_list = list(contractions_dict.keys())

# Function to convert contractions in a text
def convert_contractions(text):
    words = []
    for word in regexp.tokenize(text):
        if word in contractions_list:
            words = words + contractions_dict[word].split()
        else:
            words = words + word.split()

    text_converted = " ".join(words)
    return text_converted


abbreviations = {
    "$" : "dollar",
    "€" : " euro ",
    "4ao" : "for adults only",
    "a.m" : "before midday",
    "a3" : "anytime anywhere anyplace",
    "aamof" : "as a matter of fact",
    "acct" : "account",
    "adih" : "another day in hell",
    "afaic" : "as far as i am concerned",
    "afaict" : "as far as i can tell",
    "afaik" : "as far as i know",
    "afair" : "as far as i remember",
    "afk" : "away from keyboard",
    "app" : "application",
    "approx" : "approximately",
    "apps" : "applications",
    "asap" : "as soon as possible",
    "asl" : "age, sex, location",
    "atk" : "at the keyboard",
    "ave." : "avenue",
    "aymm" : "are you my mother",
    "ayor" : "at your own risk",
    "b&b" : "bed and breakfast",
    "b+b" : "bed and breakfast",
    "b.c" : "before christ",
    "b2b" : "business to business",
    "b2c" : "business to customer",
    "b4" : "before",
    "b4n" : "bye for now",
    "b@u" : "back at you",
    "bae" : "before anyone else",
    "bak" : "back at keyboard",
    "bbbg" : "bye bye be good",
    "bbc" : "british broadcasting corporation",
    "bbias" : "be back in a second",
    "bbl" : "be back later",
    "bbs" : "be back soon",
    "be4" : "before",
    "bfn" : "bye for now",
    "blvd" : "boulevard",
    "bout" : "about",
    "brb" : "be right back",
    "bros" : "brothers",
    "brt" : "be right there",
    "bsaaw" : "big smile and a wink",
    "btw" : "by the way",
    "bwl" : "bursting with laughter",
    "c/o" : "care of",
    "cet" : "central european time",
    "cf" : "compare",
    "cia" : "central intelligence agency",
    "csl" : "can not stop laughing",
    "cu" : "see you",
    "cul8r" : "see you later",
    "cv" : "curriculum vitae",
    "cwot" : "complete waste of time",
    "cya" : "see you",
    "cyt" : "see you tomorrow",
    "dae" : "does anyone else",
    "dbmib" : "do not bother me i am busy",
    "diy" : "do it yourself",
    "dm" : "direct message",
    "dwh" : "during work hours",
    "e123" : "easy as one two three",
    "eet" : "eastern european time",
    "eg" : "example",
    "embm" : "early morning business meeting",
    "encl" : "enclosed",
    "encl." : "enclosed",
    "etc" : "and so on",
    "faq" : "frequently asked questions",
    "fawc" : "for anyone who cares",
    "fb" : "facebook",
    "fc" : "fingers crossed",
    "fig" : "figure",
    "fimh" : "forever in my heart",
    "ft." : "feet",
    "ft" : "featuring",
    "ftl" : "for the loss",
    "ftw" : "for the win",
    "fwiw" : "for what it is worth",
    "fyi" : "for your information",
    "g9" : "genius",
    "gahoy" : "get a hold of yourself",
    "gal" : "get a life",
    "gcse" : "general certificate of secondary education",
    "gfn" : "gone for now",
    "gg" : "good game",
    "gl" : "good luck",
    "glhf" : "good luck have fun",
    "gmt" : "greenwich mean time",
    "gmta" : "great minds think alike",
    "gn" : "good night",
    "g.o.a.t" : "greatest of all time",
    "goat" : "greatest of all time",
    "goi" : "get over it",
    "gps" : "global positioning system",
    "gr8" : "great",
    "gratz" : "congratulations",
    "gyal" : "girl",
    "h&c" : "hot and cold",
    "hp" : "horsepower",
    "hr" : "hour",
    "hrh" : "his royal highness",
    "ht" : "height",
    "ibrb" : "i will be right back",
    "ic" : "i see",
    "icq" : "i seek you",
    "icymi" : "in case you missed it",
    "idc" : "i do not care",
    "idgadf" : "i do not give a damn fuck",
    "idgaf" : "i do not give a fuck",
    "idk" : "i do not know",
    "ie" : "that is",
    "i.e" : "that is",
    "ifyp" : "i feel your pain",
    "IG" : "instagram",
    "iirc" : "if i remember correctly",
    "ilu" : "i love you",
    "ily" : "i love you",
    "imho" : "in my humble opinion",
    "imo" : "in my opinion",
    "imu" : "i miss you",
    "iow" : "in other words",
    "irl" : "in real life",
    "j4f" : "just for fun",
    "jic" : "just in case",
    "jk" : "just kidding",
    "jsyk" : "just so you know",
    "l8r" : "later",
    "lb" : "pound",
    "lbs" : "pounds",
    "ldr" : "long distance relationship",
    "lmao" : "laugh my ass off",
    "lmfao" : "laugh my fucking ass off",
    "lol" : "laughing out loud",
    "ltd" : "limited",
    "ltns" : "long time no see",
    "m8" : "mate",
    "mf" : "motherfucker",
    "mfs" : "motherfuckers",
    "mfw" : "my face when",
    "mofo" : "motherfucker",
    "mph" : "miles per hour",
    "mr" : "mister",
    "mrw" : "my reaction when",
    "ms" : "miss",
    "mte" : "my thoughts exactly",
    "nagi" : "not a good idea",
    "nbc" : "national broadcasting company",
    "nbd" : "not big deal",
    "nfs" : "not for sale",
    "ngl" : "not going to lie",
    "nhs" : "national health service",
    "nrn" : "no reply necessary",
    "nsfl" : "not safe for life",
    "nsfw" : "not safe for work",
    "nth" : "nice to have",
    "nvr" : "never",
    "nyc" : "new york city",
    "oc" : "original content",
    "og" : "original",
    "ohp" : "overhead projector",
    "oic" : "oh i see",
    "omdb" : "over my dead body",
    "omg" : "oh my god",
    "omw" : "on my way",
    "p.a" : "per annum",
    "p.m" : "after midday",
    "pm" : "prime minister",
    "poc" : "people of color",
    "pov" : "point of view",
    "pp" : "pages",
    "ppl" : "people",
    "prw" : "parents are watching",
    "ps" : "postscript",
    "pt" : "point",
    "ptb" : "please text back",
    "pto" : "please turn over",
    "qpsa" : "what happens", #"que pasa",
    "ratchet" : "rude",
    "rbtl" : "read between the lines",
    "rlrt" : "real life retweet",
    "rofl" : "rolling on the floor laughing",
    "roflol" : "rolling on the floor laughing out loud",
    "rotflmao" : "rolling on the floor laughing my ass off",
    "rt" : "retweet",
    "ruok" : "are you ok",
    "sfw" : "safe for work",
    "sk8" : "skate",
    "smh" : "shake my head",
    "sq" : "square",
    "srsly" : "seriously",
    "ssdd" : "same stuff different day",
    "tbh" : "to be honest",
    "tbs" : "tablespooful",
    "tbsp" : "tablespooful",
    "tfw" : "that feeling when",
    "thks" : "thank you",
    "tho" : "though",
    "thx" : "thank you",
    "tia" : "thanks in advance",
    "til" : "today i learned",
    "tl;dr" : "too long i did not read",
    "tldr" : "too long i did not read",
    "tmb" : "tweet me back",
    "tntl" : "trying not to laugh",
    "ttyl" : "talk to you later",
    "u" : "you",
    "u2" : "you too",
    "u4e" : "yours for ever",
    "utc" : "coordinated universal time",
    "w/" : "with",
    "w/o" : "without",
    "w8" : "wait",
    "wassup" : "what is up",
    "wb" : "welcome back",
    "wtf" : "what the fuck",
    "wtg" : "way to go",
    "wtpa" : "where the party at",
    "wuf" : "where are you from",
    "wuzup" : "what is up",
    "wywh" : "wish you were here",
    "yd" : "yard",
    "ygtr" : "you got that right",
    "ynk" : "you never know",
    "zzz" : "sleeping bored and tired",
    "lol" : "laugh out loud",
    "lit": "exciting",
    "btw":"by the way",
    # Indian slangs
    "namaste" : "hello",
    "Bakchodi" : "senseless talk",
    "chai-pani" : "bribes",
    "jugaad" : "quick, improvised solution to a problem",
    "chillax" : "calm down",
    "funda" : "basic concept",
    "maggi" : "instant noodles; something quick or easy",
    "firangi" : "foreigner",
    "kya" :  "hey",
    "pinne" : "drink",
    "bhai" : "friend",
    "aaj": "today",
    "jaye": "will go",
    "macha" : "close friend",
    "machi" : "close friend",
    "item" : "attractive person",
    "sutta" : "cigarette",
    "thulla" : "policeman",
    "panga" : "getting into a fight",
    "gedi" : "casual drive",
    "lafda" : "trouble",
    "rs": "rupees",
}
def convert_abbrev_in_text(text):
    tokens = word_tokenize(text)
    tokens = [abbreviations[word.lower()] if word.lower() in abbreviations else word for word in tokens]
    text = ' '.join(tokens)
    return text


# pyspellchecker
# spell = SpellChecker()

# def pyspellchecker(text):
#     word_list = regexp.tokenize(text)
#     word_list_corrected = []
#     for word in word_list:
#         if word in spell.unknown(word_list):
#             word_corrected = spell.correction(word)
#             if word_corrected == None:
#                 word_list_corrected.append(word)
#             else:
#                 word_list_corrected.append(word_corrected)
#         else:
#             word_list_corrected.append(word)
#     text_corrected = " ".join(word_list_corrected)
#     return text_corrected


# Lemmatization
spacy_lemmatizer = spacy.load("en_core_web_sm", disable = ['parser', 'ner'])

def text_lemmatizer(text):
    text_spacy = " ".join([token.lemma_ for token in spacy_lemmatizer(text)])
    return text_spacy


def discard_non_alpha(text):
    word_list_non_alpha = [word for word in regexp.tokenize(text) if word.isalpha()]
    text_non_alpha = " ".join(word_list_non_alpha)
    return text_non_alpha


def keep_pos(text):
    tokens = regexp.tokenize(text)
    tokens_tagged = nltk.pos_tag(tokens)
    #keep_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'FW']
    keep_tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'PRPS','JJ',
                 'RB', 'RBR', 'RBS', 'VB', 'VBD', 'VBG', 'VBN', 'VBP','WP$',
                 'VBZ', 'WDT', 'WP', 'WPS', 'WRB']

    keep_words = [x[0] for x in tokens_tagged if x[1] in keep_tags]
    return " ".join(keep_words)

stops = stopwords.words("english")
alphabets = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
others = ["'","tell","ok","okay","mine","my","still","think","feel","facebook","come","soon",
          "meaning","say","said","told","tell","easy","easyif","if","use","way","earth","thinking",
          "put","got","read","readed","reading","want","well","type","typing","yeah","english","china","lemon","eye",
          "mebecause","because","limited","account","text","texting","chat","chatting","come","coming","sumthe","neighbor","last","features","features",
          "someone","go","sometimes","thing","people","make","know","known","whatsapp","status","sent","send","received","receive","seen","saw","remove",
          "removed","admin","message","messages", "ã", "å", "ì", "û", "ûªm", "ûó", "ûò", "ìñ", "ûªre", "ûªve", "ûª", "ûªs", "ûówe","one"]

all_stops =  stops + alphabets + others
def remove_stopwords(text):
    return " ".join([word for word in regexp.tokenize(text) if word not in all_stops])


def text_normalizer(text):
    text = convert_to_lowercase(text)
    text = remove_whitespace(text)
    text = re.sub('\n', '', text)
    text = re.sub(r'\.com\b', '', text)
    text = remove_http(text)
    text = remove_punctuation(text)
    text = remove_html(text)
    text = remove_emoji(text)
    text = remove_problematic(text)
    text = convert_acronyms(text)
    text = convert_contractions(text)
    text = convert_abbrev_in_text(text)
    # text = pyspellchecker(text)
    text = text_lemmatizer(text)
    text = discard_non_alpha(text)
    text = keep_pos(text)
    text = convert_to_lowercase(text)
    text = remove_stopwords(text)

    return text
