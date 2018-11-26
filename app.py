from var_dump import var_dump

from data import singles, bigram, trigram, quadram, quintgram


def sort(dict, force_lower_case=False):
    tuples = sorted(dict.items(), key=lambda kv: kv[1], reverse=True)
    result = {}
    for item in tuples:
        if item[0].strip():
            if force_lower_case:
                result[item[0].strip().lower()] = item[1]
            else:
                result[item[0].strip()] = item[1]
    return result


def letter_comes_after(needle, haystack):
    index = 0
    result = {}
    for letter in haystack:
        try:
            key = letter + haystack[index + 1] + haystack[index + 2]
            if key == needle:
                print(key)
                if haystack[index + 3] in result.keys():
                    result[haystack[index + 3]] += 1
                else:
                    result[haystack[index + 3]] = 1
        except Exception:
            pass
        index += 1
    return sort(result)


singles = sort(singles, True)
bigram = sort(bigram, True)
trigram = sort(trigram, True)
quadram = sort(quadram, True)
quintgram = sort(quintgram, True)

with open("cipher.txt") as f:
    content = f.read()


def char_frequency(str1):
    dict = {}
    for n in str1:
        keys = dict.keys()
        if n in keys:
            dict[n] += 1
        else:
            dict[n] = 1
    return dict


def char_frequency_bigram(str1):
    dict = {}
    index = 0
    for n in str1:
        keys = dict.keys()
        try:
            key = n + str1[index + 1]
            if key in keys:
                dict[key] += 1
            else:
                dict[key] = 1
            index += 1
        except Exception:
            print('last letter')
    return dict


def char_frequency_trigram(str1):
    dict = {}
    index = 0
    for n in str1:
        keys = dict.keys()
        try:
            key = n + str1[index + 1] + str1[index + 2]
            if key in keys:
                dict[key] += 1
            else:
                dict[key] = 1
            index += 1
        except Exception:
            print('last letter')
    return dict


def char_frequency_quadram(str1):
    dict = {}
    index = 0
    for n in str1:
        keys = dict.keys()
        try:
            key = n + str1[index + 1] + str1[index + 2] + str1[index + 3]
            if key in keys:
                dict[key] += 1
            else:
                dict[key] = 1
        except Exception:
            print('last letter')
        index += 1
    return dict


def char_frequency_quintgram(str1):
    dict = {}
    index = 0
    for n in str1:
        keys = dict.keys()
        try:
            key = n + str1[index + 1] + str1[index + 2] + str1[index + 3] + str1[index + 4]
            if key in keys:
                dict[key] += 1
            else:
                dict[key] = 1
        except Exception:
            print('last letter')
        index += 1
    return dict


def decrypt(mapping, cipher):
    c = cipher
    for old, new in mapping.items():
        c = c.replace(old, new)
    return c


# Single letter analysis
freq = char_frequency(content)
freq = sort(freq)

var_dump(list(freq.keys())[0:5])
var_dump(list(singles.keys())[0:5])

# First insight.
# g(e), x(t), a(o), y(a), o(i) -> e!, t!, a!, o!, i!

# Bigram analysis
freq_bi = char_frequency_bigram(content)
freq_bi = sort(freq_bi)

# var_dump(list(freq_bi.keys())[0:10])
# var_dump(list(bigram.keys())[0:10])
# Second insight
# xz(th), zg(he), gt(er), ol(in), yl(an), am(o?), tg(de), ox(it), xa(to), zy(ha)
# -> th!, he!, in!, er!, an!, re, es, on, st, nt

# Trigram analysis
freq_tri = char_frequency_trigram(content)
freq_tri = sort(freq_tri)

# var_dump(list(freq_tri.keys())[0:15])
# var_dump(list(trigram.keys())[0:10])
# Most repeated trigrams are xzg(the), ylr(and), olk(ing), zgt(her), uam,
# gtg(e?e), xzy(tha), zyx(hat), oxz(ith), vat(for)
# qyi (?a?), qox(?it), axz(?th), glx(ent), xzo(thi)
# In English the!, and!, ing!, ent, ion, her!, for!, tha!, nth, int
# assumption l -> n
mapping = {
    'r': 'd',
    't': 'r',
    'x': 't',
    'z': 'h',
    'g': 'e',
    'l': 'n',
    'a': 'o',
    'y': 'a',
    'o': 'i',
    'k': 'g',
    'v': 'f',

}

freq_quad = char_frequency_quadram(content)
freq_quad = sort(freq_quad)

# var_dump(list(freq_quad.keys())[0:5])
# var_dump(list(quadram.keys())[0:5])
# xzgt(ther), qoxz(eith), xzyx(that), zgtg(hete), axzg(?the) -> tion, nthe, ther, that, ofth


freq_quint = char_frequency_quintgram(content)
freq_quint = sort(freq_quint)
var_dump(list(freq_quint.keys())[0:20])
var_dump(list(quintgram.keys())[0:20])
# yxzgt(ather), avxzg(ofthe), xzgtg(there), ghrgt(e?der), vyxzg(fathe), xaxzg(tothe), yxxzg (atthe),olxzg(inthe)
# aboxc(o?it?), boxcz, xzggh(thee?), zgghr(hee?d), gghrg(ee?de), xzamk(th??g), axzgt(?thed), ylrxz(andth), xzolk(thing), zgqyi, hoxxh
#->  ofthe, ation, inthe!, there!, ingth, tothe, ngthe, andth, ndthe, onthe, other, atthe, tions, edthe
# their, tiona, orthe, forth, ingto, ction,


# I will solve the equation with most probable ones
# h -> z, e -> g
# 25 = 7a + b mod 26
# 6 = 4a + b mod 26
# ------------
# 19 = 3a mod 26
# a = 19 * 3^-1 mod 26 = 19 * 9 mod 26 = -7 * 9 mod 26 = -63 mod 26 = 15
# a = 15
# 6 = 4 * 15 + b mod 26 = -b = 54 mod 26 = b = 24