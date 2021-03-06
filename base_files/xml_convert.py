import pandas as p
import xml.etree.ElementTree as xml
import sys
import os


def convert(path_to_folder):
    rows = []
    for file in os.listdir(path_to_folder):
        if not file.startswith('.'):
            tree = xml.parse(path_to_folder+'/'+file)
            root = tree.getroot()
            for element in root.iter('object'):
                height = float(root.find('size').find('height').text)
                width = float(root.find('size').find('width').text)
                name = element.find('name').text
                if name == 'with_mask':
                    name='mask'
                elif name == 'without_mask':
                    name='no_mask'
                else:
                    name='improper_mask'
                xmin = str(min(1,float(element.find('bndbox').find('xmin').text)/width))
                ymin = str(min(1,float(element.find('bndbox').find('ymin').text)/height))
                xmax = str(min(1,float(element.find('bndbox').find('xmax').text)/width))
                ymax = str(min(1,float(element.find('bndbox').find('ymax').text)/height))
                file = file[:-3]+'png'

                rows.append('UNASSIGNED,gs://bhacks2020/images/'+str(file)+','+str(name)+','+xmin+','+ymin+',,,'+xmax+','+ymax+',,\n')
    return rows

if __name__ == '__main__':
    try:
        p = str(sys.argv[1])
    except:
        print('Missing folder path')
    df = convert(p)

    f = open("training.csv","w")
    f.writelines(df)
