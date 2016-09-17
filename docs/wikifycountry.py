
import json, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--facet", help="facetname e.g. 'endangered'")
args = parser.parse_args()

if (args.facet==None):
    print("must give --facet")
    quit() 

facetname = args.facet
print ("facet "+facetname)

JSON_ROOT="/Users/pm286/workspace/dictionaries/json/"

CMDOT="CM."
CONTENTMINE="contentmine"
ENTRIES="entries"
ID="id"
IDENTIFIERS="identifiers"
NAME="name"
RAW_SUFF=".raw.json"
TERM_LABEL="termLabel"
TERM="term"
WIKIDATA="wikidata"

def enrich(termlist, facetname):
    """
    Iterate over a list of terms and add an enumerating identifier.
    """
    return [reformat(d, i, facetname) for i,d in enumerate(termlist) \
                                      if not digit_present(d.get(TERM_LABEL))]

def digit_present(s):
    """
    Returns true for entities that have no common/scientific name in wikidata
    and get assigned something like 't307596644'.
    """
    return any(i.isdigit() for i in s)

def reformat(d, i, facetname):
    """
    Reformats the dictionaries into facets.
    """
    new = {}
    new[TERM] = d.get(TERM_LABEL)
    new[NAME] = d.get(TERM_LABEL)
    new[IDENTIFIERS] = {}
    # "https://www.wikidata.org/wiki/Q4661045" -> "Q4661045"
    new[IDENTIFIERS][WIKIDATA] = d.get(TERM).split("/")[-1]
    new[IDENTIFIERS][CONTENTMINE] = CMDOT+facetname+str(i)
    return new

def make_facet(wikidatajsonpath, facetname):
    """
    Reads downloaded JSON from a wikidata query,
    builds structure around a list of terms,
    returns facet.
    """
    with open(wikidatajsonpath) as infile:
        raw = json.load(infile)
        entries = enrich(raw, facetname)
        
        facet= {}
        facet[ID] = CMDOT+facetname
        facet[NAME] = facetname
        facet[ENTRIES] = entries
        return facet

print ("transforming dictionaries")

new_facet = make_facet(JSON_ROOT+facetname+RAW_SUFF, facetname)

with open("{0}.json".format(facetname), "w") as outfile:
    json.dump(new_facet, outfile, indent=4)

