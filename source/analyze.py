import sys, os, re, keyword
from pathlib import Path
from functools import reduce
from  multiprocessing import Process, Pool


projectName = "python_dependency_analyzer"
originalDir = os.getcwd()
scriptPath = Path(__file__)
scriptDir = scriptPath.parent
moveUpDegrees = lambda originalPath, amount : reduce(lambda x, y : x.parent, range(0, amount), originalPath)
potentials = list(map(lambda x : moveUpDegrees(scriptPath, x), range(0, len(scriptPath.parts))))
rootDir: Path = list(filter(lambda x : x.name == projectName, potentials))[-1] #should always grab the shortest possible, and therefore most likely to be actual root path, even if the root directory name was reused.
sys.path.append(str(rootDir))
sys.path = sorted(list(set(sys.path)))
initial = str(Process.pid)


def generateSourceTokens(inputSource: str) -> list[str]:
    output = []

    return output


def startsWith(pattern: str, body: str) -> bool:
    """
    determines if the string in body starts with the string in pattern

    Parameters
    ----------
    pattern : str
        the string to search for in the body parameter.  only use string literals
    body : str
        the body of text to search using the given pattern

    Returns
    -------
    bool
        indication of whether the pattern string was found at the beginning of the body    
    """

    regex = f'^{pattern} '
    hits = re.findall(regex, body)
    output = (len(hits) > 0)
    return output


def endsWith(pattern: str, body: str) -> bool:
    regex = f' {pattern}^'
    hits = re.findall(regex, body)
    output = (len(hits) > 0)
    return output


def advancedContains(pattern: str, body: str) -> bool:
    start = startsWith(pattern, body)
    mid = (" " + pattern + " ") in body
    end = endsWith(pattern, body)
    output = start or mid or end
    return output


def isLineImport(input: str) -> bool:
    keywords = list(keyword.kwlist)
    keywords.remove("import")
    keywords.remove("from")
    containsForbiddens = any(map(lambda x : advancedContains(x, input), keywords))
    output = startsWith("import", input) and not containsForbiddens
    return output

    
def isLineFrom(input: str) -> bool:
    keywords = list(keyword.kwlist)
    keywords.remove("import")
    keywords.remove("from")
    containsForbiddens = any(map(lambda x : advancedContains(x, input), keywords))
    midImport = " import " in input
    output = startsWith("from", input) and midImport and not containsForbiddens
    return output


def processImportLine(inputLine: str) -> list[str]:
    print(inputLine)
    buffer0 = re.sub(r'^import ', '', inputLine)
    print(buffer0)
    buffer1 = buffer0.split(",")
    output = list(map(lambda x : x.strip(), buffer1))
    return output


def processFromLine(inputLine: str) -> tuple[str, list[str]]:    
    processedLine = re.sub(r'\s+', ' ', inputLine)
    buffer = processedLine.split(" ")
    rootImport = buffer[1]
    leafImportString = processedLine.replace(rootImport, "").replace("import", "").replace("from", "").strip()
    leafImports = list(map(lambda x : x.strip(), leafImportString.split(",")))
    output = (rootImport, leafImports)
    return output



def main(initialScript: Path):
    output = []
    fileHandle = open(initialScript, "r")
    data = fileHandle.read()
    fileHandle.close()
    lines = data.split("\n")
    importDependencies = list(filter(isLineImport, lines))
    fromDependencies = list(filter(isLineFrom, lines))
    processedImports = list(reduce(lambda y, x : y + processImportLine(x), importDependencies, []))
    processedFroms = list(reduce(lambda y, x : y + [processFromLine(x)], fromDependencies, []))
    output.extend(processedImports)
    output.extend(processedFroms)
    return output


if __name__ == "__main__":
    startingScript = sys.argv[1]
    buffer = main(startingScript)
    print(buffer)
