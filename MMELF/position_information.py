import os
import sys


def F_position(Protein_path, Feature_path):
    pro_name_dir = Protein_path
    position_dir = Feature_path
    name_list = os.listdir(pro_name_dir)

    for pro_name in name_list:
        pro_name_file = open(pro_name_dir+pro_name)
        content_name = pro_name_file.readline()
        content_position = pro_name_file.readline().strip()
        pro_name_file.close()
        position_file = open(position_dir +pro_name +".pos", 'a')
        for position in range(1,len(content_position)+1):
            position_score = position/len(content_position)
            position_score = round(position_score,3)
            position_file.writelines(str(position_score)+'\n')

        pro_name_file.close()

Protein_path = sys.argv[1]
Feature_path = sys.argv[2]

F_position(Protein_path, Feature_path)
print("Complete !")

