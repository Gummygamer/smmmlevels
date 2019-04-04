import course
import sys
import os

#os.getcwd()+'/predicted/'+str(seq_len)+"_"+str(batch_size)+'_'+str(steps_per_epoch)+'_'+str(epochs)+"/levelN"+str(i)+".txt"

# Loading a stage level to get the meta data. Stage used in the prediction are fine.
levelFile = open("1-1.cdt","rb")

level = course.Course()
level.load(levelFile.read())


#Now we let the script looking at our predicted level folder. It will turn every txt file into normal stage file.
for root, dirs, files in os.walk(os.getcwd()+'/predicted/'):
    for name in files:
        if name.endswith((".txt")):
            stringFile = open(root+'/'+name,"r")
            lvlstr = stringFile.read()
            level.fromAIString(lvlstr)

            #Now we name the stage file
            finalFile = open(root+'/'+name+'.cdt',"wb")
            print(name)

            finalFile.write(level.save())
