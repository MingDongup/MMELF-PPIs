from DataProcess import Dataprocess
from torch.utils.data import DataLoader
from torch.autograd import Variable
import torch
import os
from DESNET import Residual_Block
from DESNET import ResNet
import sys

def run(path):
    return path

#print(sys.argv[1])

protein_file_path = run(sys.argv[1])

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)


model_num = 18
thred = 0.75

def Compute_data(validation_loader, savemodel):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    file_out = open(protein_file_path + 'PredictResult', 'w')
    file_lab = open(protein_file_path + 'Lable', 'w')

    for i, data in enumerate(validation_loader):
        features, labels, _ = data
        features = Variable(features)
        labels = Variable(labels.float())
        features = torch.FloatTensor(features).to(device)
        labels = torch.FloatTensor(labels).to(device)
        features = torch.unsqueeze(features, 1)
        output = 0
        for modelnum in range(model_num):
            model1 = ResNet(Residual_Block, [2, 2, 2, 2]).to(device)
            model1.load_state_dict(torch.load(savemodel + 'resnet'+str(modelnum+1), map_location='cpu'), strict=True)
            model1.eval()
            out1 = model1(features)
            output += out1
        output = output/model_num


        for ii in range(len(output)):
            out = output[ii].data
            labe = labels[ii].data
            out = round(float(out), 3)
            labe = float(labe)

            out = str(out)
            labe = str(labe)

            file_out.write(out + '\n')
            file_lab.write(labe + '\n')


        for index in range(len(labels)):
            if output[index] < thred:
                if labels[index] == 0:
                    TN += 1
                else:
                    FN += 1
            elif output[index] >= thred:
                if labels[index] == 1:
                    TP += 1
                else:
                    FP += 1

    Acc = (TP+TN)/(TP+FN+FP+TN)
    Acc = round(Acc, 3)
    if (TP+FN)!=0:
        Sen = TP/(TP+FN)
        Sen = round(Sen, 3)
    else:
        Sen="none"
    if (TN+FP)!=0:
        Spe = TN/(TN+FP)
        Spe = round(Spe, 3)
    else:
        Spe = "none"
    if (TP+FP)!=0:
        Pre = TP/(TP+FP)
        Pre = round(Pre, 3)
    else:
        Pre = "none"
    if ((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) ** 0.5!=0:
        MCC = (TP * TN - FN * FP) / (((TP + FP) * (TP + FN) * (TN + FP) * (TN + FN)) ** 0.5)
        MCC = round(MCC, 3)
    else:
        MCC = "none"
    print('ACC=', Acc," ", 'SEN=',Sen," ", 'SPE=',Spe," ", 'PRE=', Pre, " ",'MCC=', MCC)
    print("TP=",TP, " ","TN=", TN," ", "FP=", FP," ", "FN=", FN)
    file_out.close()
    file_lab.close()
    return TP, TN, FP, FN

pro_name = protein_file_path+"protein/"
pssm_path = protein_file_path+"pssm/"
psa_path = protein_file_path+"psa/"
Physical_properties_path = protein_file_path+"Physical_properties/"
position_path = protein_file_path+"position/"
savemodel ="models/"

win_size = 17
batch_size = 100

Get_Data_Validation = Dataprocess(pro_name, pssm_path, psa_path, Physical_properties_path,position_path, win_size)

validation_loader = DataLoader(dataset=Get_Data_Validation, batch_size=batch_size, shuffle=False)

result = Compute_data(validation_loader,savemodel)

#G:/ywjcodefile_msa/xxxxxxxx/ProteinCase/2dvwA

