from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql
import re
import time

f = open('pw.key', 'r')
pw = f.readline().strip()
f.close()

conn = pymysql.connect(host='localhost', user='root', passwd=pw, db='mysql', charset='utf8')
cur = conn.cursor()
cur.execute("USE wikipedia")

class SolutionFound(RuntimeError):
    def __init__(self, message):
        self.message = message

def getLinks(fromPageId):
    cur.execute("SELECT toPageId FROM links WHERE fromPageId = %s", (fromPageId))
    if cur.rowcount == 0:
        return None
    else:
        return [x[0] for x in cur.fetchall()]

def constructDict(currentPageId):
    links = getLinks(currentPageId)
    if links:
        return dict(zip(links, [{}]*len(links)))
    return {}

# The link tree may either be empty or contain multiple links
def searchDepth(targetPageId, currentPageId, linkTree, depth):
    if depth == 0:
        # Stop recursing and return, regardless
        return linkTree
    if not linkTree:
        linkTree = constructDict(currentPageId)
        if not linkTree:
            # No links found. Cannot continue at this node
            return {}
    if targetPageId in linkTree.keys():
        cur.execute("SELECT url FROM pages WHERE id = %d"%targetPageId)
        tarP = cur.fetchone()
        tarP = re.sub("\'\(\)", "", tarP[0])
        tarP = re.sub("^/wiki/", "", tarP)
        tarP = re.sub("_", " ", tarP)
        print("TARGET ("+str(targetPageId)+") "+tarP+" FOUND!")
        cur.execute("SELECT url FROM pages WHERE id = %d"%currentPageId)
        currP = cur.fetchone()
        currP = re.sub("\'\(\)", "", currP[0])
        currP = re.sub("^/wiki/", "", currP)
        currP = re.sub("_", " ", currP)
        raise SolutionFound("PAGE: ("+str(currentPageId)+") "+str(currP))

    for branchKey, branchValue in linkTree.items():
        try:
            # Recurse here to continue building the tree
            linkTree[branchKey] = searchDepth(targetPageId, branchKey,
                    branchValue, depth-1)
        except SolutionFound as e:
            print(e.message)
            cur.execute("SELECT url FROM pages WHERE id = %d"%currentPageId)
            currP = cur.fetchone()
            currP = re.sub("\'\(\)", "", currP[0])
            currP = re.sub("^/wiki/", "", currP)
            currP = re.sub("_", " ", currP)
            raise SolutionFound("PAGE: ("+str(currentPageId)+") "+str(currP))
    return linkTree

start_time = time.time()
try:
    searchDepth(71048, 1, {}, 4)
    print("No solution found")
except SolutionFound as e:
    print(e.message)

finally:
    cur.close()
    conn.close()
time_taken = (time.time() - start_time)
print("Finding the path took: %.3f seconds" % time_taken)
