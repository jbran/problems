'''
match a regex of a-z, . (any character), or * (any thing 0 or more times)
'''

def char_match(string, regex):
    exact = string is regex
    dotmatch = string and regex is '.'
    return exact or dotmatch

def match_regex(string, regex):
    #If no regex, it matches a nonstring.
    if not regex:
        return not string

    if (len(regex) > 1 and regex[1] is '*'):
        #handle star output of this char    
        # Star can match 0 !
        return match_regex(string, regex[2:]) or (char_match(string[0], regex[0]) and match_regex(string[1:], regex))
    else:
        #handle this char
        return char_match(string[0],regex[0]) and match_regex(string[1:],regex[1:])


print "\tGoods"
print match_regex("aabbt","aabbt")
print match_regex("aabbt","a.b.t")
print match_regex("abbt","ab*.")
print match_regex("b","b*")
print match_regex("","")
print match_regex("","a*b*c*")
print match_regex("aat","a*.*")
print match_regex("babababa","a*b*a*.*")
print match_regex("bbbbbbbbbbbbbbbbbbbbbbabb","bb*bbb*b.*b")

print "\tBads"
print match_regex("aat","aaa")
print match_regex("aat","t*.")
print match_regex("bbbbbbbbbbbbbbbbbbbbbbabb","bb*bbb*b.b")

