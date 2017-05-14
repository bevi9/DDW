from collections import Counter
from itertools import chain, combinations 
 
def frequentItems(transactions, support):
     counter = Counter()
     for trans in transactions:
         counter.update(frozenset([t]) for t in trans)
     return set(item for item in counter if float(counter[item]) / len(transactions) >= support), counter

def generateCandidates(L, k):
     candidates = set()
     for a in L:
         for b in L:
             union = a | b
             if len(union) == k and a != b:
                 candidates.add(union)
     return candidates 

def filterCandidates(transactions, itemsets, support):
     counter = Counter()
     for trans in transactions:
         subsets = [itemset for itemset in itemsets if itemset.issubset(trans)]
         counter.update(subsets)
     return set(item for item in counter if float(counter[item]) / len(transactions) >= support), counter 

def apriori(transactions, support):
     result = list()
     resultc = Counter()
     candidates, counter = frequentItems(transactions, support)
     result += candidates
     resultc += counter
     k = 2 
     while candidates:
         candidates = generateCandidates(candidates, k)
         candidates, counter = filterCandidates(transactions, candidates, support)
         result += candidates
         resultc += counter
         k += 1
     resultc = {item: (float(resultc[item]) / len(transactions)) for item in resultc}
     return result, resultc 

def genereateRules(frequentItemsets, supports, minConfidence):
    rules = []
    for itemSet in frequentItemsets:
        subsets = chain.from_iterable(combinations(itemSet, n + 1) for n in range(len(itemSet)))
        for subset in subsets:
            sub = frozenset(subset)
            if len(sub) > 1:
                diff = itemSet-sub
                if len(diff) > 0 and supports.get(itemSet)/supports.get(diff) >= minConfidence:
                        conf = supports[itemSet]/supports[diff]
                        sup = supports[itemSet]
                        rules.append((list(itemSet-sub), "->", list(subset),conf,sup))
    return rules

 
# bank dataset preprocessing
import pandas as pd
cli = pd.read_csv("./clicks.csv")
vis = pd.read_csv("./visitors.csv")
print "Number of clicks: " + str(len(cli.index))
print "Number of visits: " + str(len(vis.index))

print Counter(" ".join(cli["TopicName"]).split()).most_common(10)

#preproces
cli = cli[cli.TopicID!=-1]
cli = cli[cli.ExtCatID!=-1]
vis = vis[vis.Length_seconds > 20]
vis = vis[vis.Length_pagecount > 2]
print "Preprocessing"
print "Number of clicks: " + str(len(cli.index))
print "Number of visits: " + str(len(vis.index))
print Counter(" ".join(cli["TopicName"]).split()).most_common(10)

data = pd.merge(cli,vis,on=['VisitID'])

print "APPLICATION: " + str(len(data[data.PageName == "APPLICATION"]))
print "CATALOG: " + str(len(data[data.PageName == "CATALOG"]))
print "DISCOUNT: " + str(len(data[data.PageName == "DISCOUNT"]))
print "HOWTOJOIN: " + str(len(data[data.PageName == "HOWTOJOIN"]))
print "INSURANCE: " + str(len(data[data.PageName == "INSURANCE"]))
print "WHOWEARE: " + str(len(data[data.PageName == "WHOWEARE"]))

dataset = []
visits = set(data["VisitID"])
for v in visits:
     pn = data[data.VisitID == v]["PageName"]
     cn = data[data.VisitID == v]["CatName"]
     i = data[data.VisitID == v]
     row = [(x['CatName'], x['PageName']) for x in i.to_dict(orient="records")]
     dataset.append(row)

frequentItemsets, supports = apriori(dataset, 0.1)
rules = genereateRules(frequentItemsets, supports, 0.01)

print("Confidence: ")
for s in sorted(rules, key=lambda s: s[3], reverse=True)[0:10]:
     print(s) 

print("Support: ")
for s in sorted(rules, key=lambda s: s[4], reverse=True)[0:10]:
     print(s)


