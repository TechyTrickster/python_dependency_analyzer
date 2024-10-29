# Static Dependency Analysis made easy!
---
This is a 'simple' (simple to operate) program to analyze large or small python projects and find all of their pypi and recursive custom dependencies.  More specificly, it will instantly find a given script's *minimal* dependencies! 


### Why do you need a dependency analyzer?
Across plenty of different python based projects; small, large, solo, or in a team, I've found that maintaining the project's requirements.txt is a **massive pain**.  People (including me!) will add a new feature requiring a new package from pypi, and then forget to add it to the requirements.txt when they hit commit.  Or, a python script or pypi package will get depricated, with no usage anymore, but will persist in the project for quite some time.  This in particular can have plenty of major impacts.

1. **product bloat** - large amounts of unused code persist in the project while still getting packaged into exports through your CI / CD pipeline.  This results in product bloat, which depending on context is either of negligable consequence, or massively wasteful.
2. **subpar version selection** - due to the nature of package version selection, having more packages than strictly required stick around in your venvs can result in older than necessary package version's being selected.  This will cause you and your team to miss out on new package features, and security updates!
3. **dependency conflict hell** - the more packages that you try to install, the more likely it is that you will end up with *unresolvable dependency conflicts*.  thus removing unused dependencies is always advisable!


### OK, but why not use any of the other dependency analyzers?
There are indeed other python dependency analyzers to choose from!  However, there are two reasons why I ended up writing my own.

1. **Environment Compatibility** - In many corporate environments you can't access any open source repos of any descriptions, be that pypi, the debian repos, the standard docker repos, etc.  Unfortunately, the commercial-grade, corporate repos (like JFrog) meant to replace them often **DO NOT** work with the systems meant to interface with them.  This includes many of the existing python dependency analyzers.
2. **can't identify internal dependencies** - no dependency analyzer I've found can identify *internal* source code dependencies.  i.e: the seperate source code files which were created for your project, which you are importing in other scripts.


## Features

1. identify pypi / repo based dependencies
2. identify internal, custom dependencies, recursively
3. find unused dependencies
4. find unused functions / classes
5. automatically create a downloadable requirements.txt file
6. generate a formatted report of all findings 


## Usage


#### Note
I'm quite sure that once (more like, if!) this application gains any amount of popularity, people will be coming out of the woodwork to tell me about x, y, or z dependency analyzer that can do the same things as mine, and better.  And they will almost certainly be right!  However, I didn't find them!  Regardless, creating this project has given me plenty of valuable experience that has improved my skills!

