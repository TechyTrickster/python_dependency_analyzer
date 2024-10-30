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

from source import example


#TODO: Write DocString
def generateSourceTokens(inputSource: str) -> list[str]:
    output = []

    return output


def generateProjectTree(rootPath: Path) -> list[str]:    
    genLocal = lambda node, leaves : reduce(lambda y, x : y + [node / x], leaves, [])
    walkResults = os.walk(rootPath)
    output = reduce(lambda y, x : y + genLocal(Path(x[0]), x[2]), walkResults, [])
    return output


def generateImportAliases(projectRoot: Path, paths: list[Path], venvPath: Path) -> list[str]:    
    projectRootStr = str(projectRoot)
    venvPathStr = str(venvPath)
    createImportAlias = lambda x : str(x).replace(projectRootStr, "").replace("/", ".")
    filterLeadingDot = lambda x : x[1:] if x[0] == "." else x    
    containsVenvPath = lambda x : not startsWith2(venvPathStr, str(x))
    isAPyFile = lambda x : x.suffix == ".py"
    removePythonExtension = lambda x : re.sub(r'\.py$', '', x)
    buffer0 = list(filter(isAPyFile, paths))
    buffer1 = list(filter(containsVenvPath, buffer0))
    buffer2 = list(map(createImportAlias, buffer1))
    buffer3 = list(map(filterLeadingDot, buffer2))    
    buffer4 = list(map(removePythonExtension, buffer3))
    output = list(zip(buffer1, buffer4))    
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


def startsWith2(pattern: str, body: str) -> bool:
    """
    determines if the string in body starts with the string in pattern, as a non-isolated token

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

    regex = f'^{pattern}'
    hits = re.findall(regex, body)
    output = (len(hits) > 0)
    return output


#TODO: Write DocString
def endsWith(pattern: str, body: str) -> bool:
    regex = f' {pattern}^'
    hits = re.findall(regex, body)
    output = (len(hits) > 0)
    return output


#TODO: Write DocString
def advancedContains(pattern: str, body: str) -> bool:
    start = startsWith(pattern, body)
    mid = (" " + pattern + " ") in body
    end = endsWith(pattern, body)
    output = start or mid or end
    return output


#TODO: Write DocString
def isLineImport(input: str) -> bool:
    keywords = list(keyword.kwlist)
    keywords.remove("import")
    keywords.remove("from")
    containsForbiddens = any(map(lambda x : advancedContains(x, input), keywords))
    output = startsWith("import", input) and not containsForbiddens
    return output


#TODO: Write DocString
def isLineFrom(input: str) -> bool:
    keywords = list(keyword.kwlist)
    keywords.remove("import")
    keywords.remove("from")
    containsForbiddens = any(map(lambda x : advancedContains(x, input), keywords))
    midImport = " import " in input
    output = startsWith("from", input) and midImport and not containsForbiddens
    return output


#TODO: Write DocString
def processImportLine(inputLine: str) -> list[str]:    
    buffer0 = re.sub(r'^import ', '', inputLine)    
    buffer1 = buffer0.split(",")
    output = list(map(lambda x : x.strip(), buffer1))
    return output


#TODO: Write DocString
def processFromLine(inputLine: str) -> tuple[str, list[str]]:    
    processedLine = re.sub(r'\s+', ' ', inputLine)
    buffer = processedLine.split(" ")
    rootImport = buffer[1]
    leafImportString = processedLine.replace(rootImport, "").replace("import", "").replace("from", "").strip()
    leafImports = list(map(lambda x : x.strip(), leafImportString.split(",")))
    output = list(map(lambda x : rootImport + "." + x, leafImports))    
    return output



#TODO: Write DocString
def main(initialScript: Path, projectRootDirectory: Path, venvDirectory: Path) -> dict:    
    fileHandle = open(initialScript, "r")
    data = fileHandle.read()
    fileHandle.close()
    lines = data.split("\n")
    importDependencies = list(filter(isLineImport, lines))
    fromDependencies = list(filter(isLineFrom, lines))
    processedImports = list(reduce(lambda y, x : y + processImportLine(x), importDependencies, []))
    processedFroms = list(reduce(lambda y, x : y + processFromLine(x), fromDependencies, []))
    
    allImports = []
    allImports.extend(processedImports)
    allImports.extend(processedFroms)    
    paths = generateProjectTree(projectRootDirectory)
    customAssets = generateImportAliases(projectRootDirectory, paths, venvDirectory)
    customAssetsShortNames = list(map(lambda x : x[1], customAssets))
    rootFileShortName = list(filter(lambda x : x[0] == initialScript, customAssets))[0][1]
    allImports.append(rootFileShortName)
    usedSources = list(filter(lambda x : x[1] in allImports, customAssets))
    
    standardImportsBuffer = []
    standardImportsBuffer.extend(processedImports)
    standardImportsBuffer.extend(processedFroms)    
    standardImports = list(filter(lambda x : x not in customAssetsShortNames, standardImportsBuffer))

    unusedSourceFiles = list(filter(lambda x : x not in usedSources, customAssets))

    output = {
        'standard imports': standardImports,
        'all source files': customAssets,
        'used source files': usedSources,
        'unused source files': unusedSourceFiles
    }
    
    return output


#TODO: Write DocString
if __name__ == "__main__":
    startingScript = Path(sys.argv[1]).resolve()
    projectRootDirectory = Path(sys.argv[2]).resolve()
    venvDirectory = Path(sys.argv[3]).resolve()
    buffer = main(startingScript, projectRootDirectory, venvDirectory)
    print(buffer)
