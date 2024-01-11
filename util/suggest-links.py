# pip install python-frontmatter
import frontmatter
import glob
import re
import sys

def findmatches(filepath):
    keys = buildmap()
    matches = []
    fulllineno = len(open(filepath).readlines())
    with open(filepath) as f:
        content =  frontmatter.loads(f.read()).content.lower()
        lineno = content.count( "\n" ) + 1 
        # Add lines to account from frontmatter length
        pad = fulllineno - lineno + 1
        for k in keys:
            if(keys[k].count(get_slug(filepath)) == 0):
                r = list(find_with_line_numbers(k, content, keys[k], pad))
                matches += r
    matches = list(filter(disallow_links, matches))
    #sort by line number
    matches.sort(key=lambda tup: tup[2])
    return matches
        
def buildmap():
    keys = {}
    files = glob.glob('./**/*.md', recursive=True)
    for f in files:
        keys = combine_dict(keys, links(f))
    return keys

# we want to preserve keys with duplicate values so we can see conflicting articles
# so we use {"keyword":["page1", "page2", ...]} as the datastructure
def combine_dict(d1, d2):
    d = {}
    d2_keys_not_in_d1 = d2.keys() - d1.keys()
    d1_keys_not_in_d2 = d1.keys() - d2.keys()
    common_keys = d2.keys() & d1.keys()

    for i in common_keys:
        d[i]=d1[i]+d2[i]
    for i in d1_keys_not_in_d2:
        d[i]=d1[i]
    for i in d2_keys_not_in_d1:
        d[i]=d2[i]
    return d

def links(filepath):
    try:
        with open(filepath) as f:
            post = frontmatter.loads(f.read())
            keywords = post["internal-links"]
            dic = { key.strip() : [get_slug(filepath)] for key in keywords}
            return dic
    except Exception:
        return {}

def disallow_links(m):
    banned = r"[]()"
    return not any(elem in m[1] for elem in banned)

# from https://stackoverflow.com/a/45142535/135202
def find_with_line_numbers(phrase, string, links, padline = 0):
    import re
    # capture two words before and one after the phrase
    # also make sure its a whole word that might end in punctuation (\s,.?)
    # also handle it being the first word of a line (then no space before it)
    pattern = "((( +[^\s]*){2})? +"+ phrase + "(\s|\.|\?|,)([^\s]* +)?)|(\s"+phrase+"(\s|\.|\?|,))"
    matches = list(re.finditer(pattern, string))
    if not matches:
        return []

    end = matches[-1].start()
    # -1 so a failed 'rfind' maps to the first line.
    newline_table = {-1: 0}
    for i, m in enumerate(re.finditer(r'\n', string), 1):
        # don't find newlines past our last match
        offset = m.start()
        if offset > end:
            break
        newline_table[offset] = i

    # Failing to find the newline is OK, -1 maps to 0.
    for m in matches:
        newline_offset = string.rfind('\n', 0, m.start())
        line_number = newline_table[newline_offset]
        yield (phrase, m.group(0), line_number + padline, links)

get_file = {}

# remove date and extention from filename
def get_slug(filename : str):
    r = filename
    try:
        m = re.search(r"(\d\d\d\d\-\d\d\-\d\d\-)(.*)(\.md)",filename)
        r = m.group(2)
    except Exception:
        r= filename
    get_file[r] = filename
    return r

if __name__ == "__main__":
    filename = sys.argv[1]
    matches = findmatches(filename)
    for m in matches:
        context = "\"... " + m[1].replace('\n', ' ') + " ... \""
        for l1 in m[3]:
            print(f"Match:\t{m[0]}:\t{context}\t -> \t[{m[0]}](/blog/{l1})\t{filename}:{m[2]}")
