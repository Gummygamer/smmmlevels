import course

levelFile = open("level.cdt","r")

level = course.Course()
#gives codec error
level.load(levelFile.read())

print(level.toAIString())
