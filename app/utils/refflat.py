import json
import pandas as pd
import os


def refflat2names(refFlat_path='/home/commons/Reference/UCSC/hg38/refseq/refFlat_200817.txt'):
    df = pd.read_csv(refFlat_path,sep='\t', names=['geneName', 'name', 'chrom', 'strand',
                                          'txStart', 'txEnd', 'cdsStart', 'cdsEnd',
                                          'exonCount', 'exonStarts', 'exonEnds'])
    name = df[['name','geneName']].to_dict(orient='index').values()
    unique = set(tuple(sorted(d.items())) for d in name)
    # set에 저장된 요소를 다시 딕셔너리로 변환하려면:
    unique_dicts = [dict(t) for t in unique]
    return unique_dicts


def get_refFlat_name(geneName='ATM',
                     refFlat_genename_path=None):
    if refFlat_genename_path == None:
        #./../refFlat/refFlat_names.json'
        refFlat_genename_path = os.path.join(os.path.dirname(__file__), './../../config/refFlat_names.json')
    with open(refFlat_genename_path, 'r', encoding='utf-8') as file:
        refFlat_name = json.load(file)
    if geneName != None:
        filtered_names = []
        for item in refFlat_name:
            if geneName in item['geneName']:
                filtered_names.append(item)
        return filtered_names
    else:
        return refFlat_name
    
    
    