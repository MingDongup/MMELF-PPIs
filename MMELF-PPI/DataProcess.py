from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import configparser
import os
import torch
import random
import numpy as np

def set_seed(seed=1):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
set_seed()


config = configparser.ConfigParser()
config.read("Config.ini", encoding='utf-8')



# ***************************************************Train************************************************************
class Dataprocess(Dataset):
    def __init__(self, pro_name_path, pssm_path, psa_path, Physical_properties_path, position_path, win_size):
        super(Dataprocess, self).__init__()
        self.pro_name_path = pro_name_path
        self.pssm_path = pssm_path
        self.psa_path = psa_path
        self.Physical_properties_path = Physical_properties_path
        self.position_path = position_path
        self.win_size = win_size
        self.stride = win_size // 2
        self.pro_list = os.listdir(pro_name_path)


        self.allresidues = self.GetAllResidues()



    def __len__(self):
        return len(self.allresidues)

    def __getitem__(self, index):
        feature, label, residue_num = self.allresidues[index]
        return feature, label, residue_num

    def GetAllResidues(self):
        all_residues = []
        num = 0
        for index in range(len(self.pro_list)):


            pro_name = self.pro_list[index]

            pro_name = pro_name[:-6]



            # pssm
            pssm_name_path = os.path.join(self.pssm_path, pro_name + '.opssm')


            pssm = np.genfromtxt(pssm_name_path, skip_footer=0, skip_header=0)[:, :20]
            # print(pssm.shape)

            pro_length, pssm_dim = pssm.shape
            pssm_padding = np.zeros((self.stride, pssm_dim))
            fea_pssm = np.append(pssm_padding, pssm, axis=0)
            fea_pssm = np.append(fea_pssm, pssm_padding, axis=0)

            # psa
            psa_name_path = os.path.join(self.psa_path, pro_name + '.sa')
            psa = np.genfromtxt(psa_name_path, skip_footer=0, skip_header=0)[:, 3:6]
            pro_length, psa_dim = psa.shape
            psa_padding = np.zeros((self.stride, psa_dim))
            fea_psa = np.append(psa_padding, psa, axis=0)
            fea_psa = np.append(fea_psa, psa_padding, axis=0)

            # Physical_properties
            Physical_properties_name_path = os.path.join(self.Physical_properties_path, pro_name + '.pp')
            Physical_properties = np.genfromtxt(Physical_properties_name_path, skip_footer=0, skip_header=0)
            pro_length, Physical_properties_dim = Physical_properties.shape
            Physical_properties_padding = np.zeros((self.stride, Physical_properties_dim))
            fea_Physical_properties = np.append(Physical_properties_padding, Physical_properties, axis=0)
            fea_Physical_properties = np.append(fea_Physical_properties, Physical_properties_padding, axis=0)

            # position
            position_name_path = os.path.join(self.position_path, pro_name + '.pos')
            position = np.genfromtxt(position_name_path, skip_footer=0, skip_header=0)
            position = position.reshape(pro_length, 1)
            pro_length, position_dim = position.shape
            position_padding = np.zeros((self.stride, position_dim))
            fea_position = np.append(position_padding, position, axis=0)
            fea_position = np.append(fea_position, position_padding, axis=0)


            fea_pssm = torch.FloatTensor(fea_pssm)
            fea_psa = torch.FloatTensor(fea_psa)
            fea_Physical_properties = torch.FloatTensor(fea_Physical_properties)
            fea_position = torch.FloatTensor(fea_position)

            #feature_padding
            feature_padding = np.zeros((2*self.stride+pro_length, Physical_properties_dim))
            feature_padding = torch.FloatTensor(feature_padding)


            feature_padding_pssm = np.zeros((2*self.stride+pro_length, pssm_dim))
            feature_padding_pssm = torch.FloatTensor(feature_padding_pssm)

            feature_padding_psa = np.zeros((2 * self.stride + pro_length, psa_dim))
            feature_padding_psa = torch.FloatTensor(feature_padding_psa)

            feature_padding_position = np.zeros((2 * self.stride + pro_length, position_dim))
            feature_padding_position = torch.FloatTensor(feature_padding_position)

            feature_padding_Physical_properties = np.zeros((2 * self.stride + pro_length, Physical_properties_dim))
            feature_padding_Physical_properties = torch.FloatTensor(feature_padding_Physical_properties)

            #new_feature = torch.cat((fea_pssm, fea_psa), 1)
            #new_feature = torch.cat((new_feature, fea_Physical_properties), 1)
            #new_feature = torch.cat((new_feature, feature_padding_position), 1)



            new_feature = torch.cat((fea_pssm, fea_psa), 1)
            new_feature = torch.cat((new_feature, fea_Physical_properties), 1)
            new_feature = torch.cat((new_feature, fea_position), 1)


            file = open(os.path.join(self.pro_name_path, pro_name+".fasta"))
            label = file.readline()
            label = file.readline()
            label = file.readline()
            file.close()
            label = list(label.strip())
            label = list(map(int, label))
            label = np.array(label)
            label = label.reshape(len(label), 1)
            # 定义滑动窗口

            PadDing = np.zeros((position_dim+pssm_dim+psa_dim+Physical_properties_dim, 15-self.stride))
            PadDing = torch.FloatTensor(PadDing)

            for i in range(self.stride, pro_length + self.stride):
                num += 1
                residue_fea = np.transpose(new_feature[i - self.stride:i + self.stride + 1])
                residue_fea = torch.cat((PadDing, residue_fea, PadDing), 1)
                all_residues.append((residue_fea, label[i - self.stride], num))
        np.random.shuffle(all_residues)
        return all_residues
