import course
import sys

levelFile = open(sys.argv[1],"rb")

level = course.Course()
level.load(levelFile.read())

print(level.toAIString())
