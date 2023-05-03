import nltk


def convert_to_pig_latin(word):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    graphemes = ['b', 'bb', 'd', 'dd', 'ed', 'f', 'ff', 'ph', 'gh', 'lf', 'ft', 'g', 'gg', 'gh', 'gu', 'gue', 'h', 'wh',
                 'j', 'ge', 'g', 'dge', 'di', 'gg', 'k', 'c', 'ch', 'cc', 'lk', 'qu', 'ck', 'x', 'l', 'll', 'm', 'mm',
                 'mb', 'mn', 'lm', 'n', 'nn', 'kn', 'gn', 'pn', 'mn', 'p', 'pp', 'r', 'rr', 'wr', 'rh', 's', 'ss', 'c',
                 'sc', 'ps', 'st', 'ce', 'se', 't', 'tt', 'th', 'ed', 'v', 'f', 'ph', 've', 'w', 'wh', 'u', 'o', 'z',
                 'zz', 's', 'ss', 'x', 'ze', 'se', 's', 'si', 'z', 'ch', 'tch', 'tu', 'te', 'sh', 'ce', 's', 'ci', 'si',
                 'ch', 'sci', 'ti', 'th', 'th', 'ng', 'n', 'ngue', 'y', 'i', 'j', ]

    pig_graphs = set([g for g in graphemes if len(g) > 1])
    pig_word = ''

    # if first letter is a vowel

    if word[0] in vowels:
        pig_word += word
        pig_word += 'ay'
        return pig_word

    for g in graphemes:
        if word.startswith(g):
            g_len = len(g)
            pig_word += word[g_len:]
            pig_word += word[:g_len]
            pig_word += 'ay'
            return pig_word

    # we want to look at the first phoneme of the word for cases like 'qu', 'th'
    for i in range(len(word)):
        if word[i] in vowels:
            pig_word += word[i:]
            pig_word += word[:i]
            pig_word += 'ay'
            return pig_word

        # if we get here the word has no vowels
    pig_word += word
    pig_word += 'ay'
    return pig_word


print(convert_to_pig_latin('quick'))
