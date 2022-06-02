import configparser
import os
import numpy as np
import math
from Physical_properties import F_Physical_properties
from position_information import F_position



def getFeature(profile_path):

    pro_file_ = open(profile_path)
    protein_name = pro_file_.readline()
    protein_name = protein_name[1:].strip()
    pro_file_.close()

    config = configparser.ConfigParser()
    config.read("Config.ini", encoding='utf-8')


    Result_path = config.get("Result", "Result_Path")
    if os.path.exists(Result_path):
        pass
    else:
        os.makedirs(Result_path)

    #1-pssm
    Psi_Blast_Path = config.get("PeatureTool", "Psi_Blast_Path")
    DB_PATH = config.get("Database", "DB_PATH")

    command1 = Psi_Blast_Path+"bin/psiblast"+" -query "
    command2 = " -db "+DB_PATH + "/swissprot -evalue 0.001 -num_iterations 3 -out_ascii_pssm " #这个命令后期要该先这么写
    #command2 = " -db " + DB_PATH + " -evalue 0.001 -num_iterations 3 -out_ascii_pssm "  # 这个命令后期要该先这么写

    if os.path.exists(Result_path+"/pssm/"):
        pass
    else:
        os.makedirs(Result_path+"/pssm/")

    os.system(command1 + profile_path + command2 + Result_path+"/pssm/"+protein_name+".pssm")
    print(command1)
    print(profile_path)
    print(command2)
    print(Result_path+"/pssm/"+protein_name+".pssm")
    #normalized pssm
    content = np.genfromtxt(Result_path+"/pssm/"+protein_name+".pssm", skip_header=3, skip_footer=4)[:, 2:22]

    new_file = open(Result_path+"/pssm/"+protein_name+".pssm".strip(".pssm")+".opssm", 'w')

    for m in range((content.shape)[0]):
        content_new = content[m:m + 1, :]
        content_new = np.array(content_new)
        content_new = content_new.tolist()

        for j in range(len(content_new[0])):
            (content_new[0])[j] = 1 / (1 + math.exp(-(content_new[0])[j]))
            (content_new[0])[j] = round((content_new[0])[j], 3)
            (content_new[0])[j] = str((content_new[0])[j])

        content_new[0] = ' '.join(content_new[0])
        new_file.writelines(content_new[0]+'\n')
    new_file.close()

    #2-psa

    Sann_Runner_Path = config.get("PeatureTool", "Sann_Runner_Path")


    command3 = Sann_Runner_Path + " "+ profile_path +" " + Result_path+"/psa/"+protein_name+".sa" #这个命令也要改的

    if os.path.exists(Result_path+"/psa/"):
        pass
    else:
        os.makedirs(Result_path+"/psa/")
    if os.path.exists(Sann_Runner_Path):
        os.system(command3 + Result_path+"psa/"+protein_name+".sa")
    else:
        print('\n'+"Sann is not installed correctly!"+'\n')
        pass

    #3-Physical_properties
    if os.path.exists(Result_path+"/Physical_properties/"):
        pass
    else:
        os.makedirs(Result_path+"/Physical_properties/")

    F_Physical_properties(profile_path, Result_path+"/Physical_properties/"+protein_name)

    #4-position
    if os.path.exists(Result_path+"/position/"):
        pass
    else:
        os.makedirs(Result_path+"/position/")

    F_position(profile_path, Result_path+"/position/"+protein_name+".pos")

    return Result_path
