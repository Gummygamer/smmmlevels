#seems to be imported the wrong way
import course

levelFile = open("level.cdt","r")

level = Course()
level.load(levelfile)

print(level.toAIString())
