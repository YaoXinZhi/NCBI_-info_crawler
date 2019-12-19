#! usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Created on 19/12/2019 21:36 
@Author: XinZhi Yao 
"""

import os
import requests
from tqdm import tqdm
from time import sleep
from bs4 import BeautifulSoup


def get_bioname_list(bioname_file):
    bioname_list = []
    with open(bioname_file) as f:
        line = f.readline()
        for line in f:
            l = line.strip().split(',')
            bion = l[ 3 ].strip("\"")
            if len(bion) > 1:
                bioname_list.append(bion)
    return bioname_list

def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ''

def parserPage(url):
    html = getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def extract_five_info(soup):
    BioSample = 'None'
    Organism = 'None'
    IsolationSource = 'None'
    Strain = 'None'
    Host = 'None'
    for d1 in soup.find(attrs={'class': 'docsum'}).children:
        if d1.dt.string == 'Identifiers':
            # TODO: BioSample
            BioSample = d1.dd.span.string
        if d1.dt.string == 'Organism':
            # TODO: Organism
            Organism = d1.dd.a.string
        if d1.dt.string == 'Attributes':
            for tr in d1.dd.table:
                if tr.th.string == 'isolation source':
                    # TODO: isolation source
                    IsolationSource = tr.td.string
                if tr.th.string == 'strain':
                    # TODO: strain
                    Strain = tr.td.string
                if tr.th.string == 'host':
                    # TODO: host
                    Host = tr.td.string
    return (BioSample, Organism, IsolationSource, Strain, Host)

def save_file(result_list, out_file):
    with open(out_file, 'w') as wf:
        wf.write('BioSample\tOrganism\tIsoationSource\tStrain\tHost\n')
        for result in result_list:
            wf.write('{0}\t{1}\t{2}\t{3}\t{4}\n'.\
                     format(result[0], result[1], result[2], result[3], result[4]))
    print('Save done.')

if __name__ == '__main__':

    sleep_time = 5
    bioname_file = r"data/eukaryotes.csv"
    out_file = 'result/crawl_five_info.txt'
    base_url = r'https://www.ncbi.nlm.nih.gov/biosample/?term='
    result_list = []

    bioname_list = get_bioname_list(bioname_file)

    for bioname in tqdm(bioname_list):
        url = base_url + bioname
        soup = parserPage(url)
        five_info = extract_five_info(soup)
        result_list.append(five_info)
        # print('Sleep for {0} seconds'.format(sleep_time))
        sleep(sleep_time)

    save_file(result_list, out_file)






