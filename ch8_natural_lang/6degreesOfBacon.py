from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

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
        print("TARGET "+str(targetPageId)+" FOUND!")
        raise SolutionFound("PAGE: "+str(currentPageId))

    for branchKey, branchValue in linkTree.items():
        try:
            # Recurse here to continue building the tree
            linkTree[branchKey] = searchDepth(targetPageId, branchKey,
                    branchValue, depth-1)
        except SolutionFound as e:
            print(e.message)
            raise SolutionFound("PAGE: "+str(currentPageId))
    return linkTree

try:
    searchDepth(1, 3, {}, 4)
    print("No solution found")
except SolutionFound as e:
    print(e.message)

finally:
    cur.close()
    conn.close()
