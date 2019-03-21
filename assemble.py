import course
import sys

levelFile = open(sys.argv[1],"rb")

level = course.Course()
level.load(levelFile.read())

stringFile = open(sys.argv[2],"r")

lvlstr = stringFile.read()

level.fromAIString(lvlstr)

finalFile = open(sys.argv[3],"wb")

finalFile.write(level.save())
