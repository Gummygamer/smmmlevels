import course

levelFile = open("level.cdt","rb")

level = course.Course()
level.load(levelFile.read())

print(level.toAIString())
