import course

levelFile = open("level.cdt","r")

level = course.Course()
level.load(levelFile)

print(level.toAIString())
