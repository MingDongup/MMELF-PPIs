import os
import sys


def F_Physical_properties(protein, Feature_path):
    pro_name_dir = protein
    Physical_properties_dir = Feature_path

    pro_name_file = open(pro_name_dir)
    content_name = pro_name_file.readline()
    content_Physical_properties = pro_name_file.readline().strip()
    Physical_properties_file = open(Physical_properties_dir, 'w')
    for i in range(len(content_Physical_properties)):
        if content_Physical_properties[i] == 'I':
            P_C = '4.19 0.19 4.00 1.80 6.04 0.30 0.45'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'V':
            P_C = '3.67 0.14 3.00 1.22 6.02 0.27 0.49'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'L':
            P_C = '2.59 0.19 4.00 1.70 6.04 0.39 0.31'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'F':
            P_C = '2.94 0.29 5.89 1.79 5.67 0.30 0.38'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'C':
            P_C = '1.77 0.13 2.43 1.54 6.35 0.17 0.41'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'M':
            P_C = '2.35 0.22 4.43 1.23 5.71 0.38 0.32'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'A':
            P_C = '1.28 0.05 1.00 0.31 6.11 0.42 0.23'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'G':
            P_C = '0.00 0.00 0.00 0.00 6.07 0.13 0.15'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'T':
            P_C = '3.03 0.11 2.60 0.26 5.60 0.21 0.36'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'W':
            P_C = '3.21 0.41 8.08 2.25 5.94 0.32 0.42'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'S':
            P_C = '1.31 0.06 1.60 -0.04 5.70 0.20 0.28'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'Y':
            P_C = '2.94 0.30 6.47 0.96 5.66 0.25 0.41'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'P':
            P_C = '2.67 0.00 2.72 0.72 6.80 0.13 0.34'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'H':
            P_C = '2.99 0.23 4.66 0.13 7.69 0.27 0.30'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'E':
            P_C = '1.56 0.15 3.78 -0.64 3.09 0.42 0.21'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'Q':
            P_C = '1.56 0.18 3.95 -0.22 5.65 0.36 0.25'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'D':
            P_C = '1.60 0.11 2.78 -0.77 2.95 0.25 0.20'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'N':
            P_C = '1.60 0.13 2.95 -0.60 6.52 0.21 0.22'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'K':
            P_C = '1.89 0.22 4.77 -0.99 9.99 0.32 0.27'
            Physical_properties_file.writelines(str(P_C) + '\n')
        elif content_Physical_properties[i] == 'R':
            P_C = '2.34 0.29 6.13 -1.01 10.74 0.36 0.25'
            Physical_properties_file.writelines(str(P_C) + '\n')

    Physical_properties_file.close()


    read_file = open(Feature_path)
    write_file = open(Feature_path+".pp", "w")
    while True:
        content = read_file.readline()
        if content == '':
            break
        list = []
        for index in range(len(content)):
            if content[index] == ' ':
                list.append(index)

        a = content[:list[0]]
        b = content[list[0] + 1: list[1]]
        c = content[list[1] + 1: list[2]]
        d = content[list[2] + 1: list[3]]
        e = content[list[3] + 1: list[4]]
        f = content[list[4] + 1: list[5]]
        g = content[list[5] + 1:]

        a = float(a)
        b = float(b)
        c = float(c)
        d = float(d)
        e = float(e)
        f = float(f)
        g = float(g)

        a = (a + 1.01) / (10.47 + 1.01)
        b = (b + 1.01) / (10.74 + 1.01)
        c = (c + 1.01) / (10.74 + 1.01)
        d = (d + 1.01) / (10.74 + 1.01)
        e = (e + 1.01) / (10.74 + 1.01)
        f = (f + 1.01) / (10.74 + 1.01)
        g = (g + 1.01) / (10.74 + 1.01)

        a = round(a, 3)
        b = round(b, 3)
        c = round(c, 3)
        d = round(d, 3)
        e = round(e, 3)
        f = round(f, 3)
        g = round(g, 3)

        write_file.writelines(
            str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d) + ' ' + str(e) + ' ' + str(f) + ' ' + str(g) + '\n')
    write_file.close()