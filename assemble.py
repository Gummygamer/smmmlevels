import course
import sys
import os

#Loading a stage level to get the meta data Stage used in the prediction are fine


levelFile = open("1-1.cdt","rb")

level = course.Course()
level.load(levelFile.read())


#Now we let the script looking at our predicted level folder. It will turn every txt file into normal stage file.
for root, dirs, files in os.walk('predicted/'):
    for name in files:
        if name.endswith((".txt")):
            stringFile = open(root+'/'+name,"r")
            lvlstr = stringFile.read()
            level.fromAIString(lvlstr)
            #Now we name the stage file
            finalFile = open(root+'/'+name+'.cdt',"wb")
            finalFile.write(level.save())
