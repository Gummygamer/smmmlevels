import course

levelFile = open("level.cdt","r")

level = course.Course()
level.load(levelfile)

print(level.toAIString())
