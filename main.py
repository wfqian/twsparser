# coding=utf-8

__author__ = 'QWF'

import string
from twsparser import make_all_ad_parser
from tws import *


ad_parser = make_all_ad_parser()

#adruns = make_ad_parser().parseString(
#    r"ADDEP  ACTION(ADD) PREWSID(PNCP) PREOPNO( 143) ADDEP  ACTION(ADD) PREWSID(PNCP) PREOPNO( 143)", True)
results = ad_parser.parseFile(r"c:\parseTws.txt", parseAll=True)

'''
ad_dict = {}
ads = ['SITESWCHBTOAM0', 'SITESWCHBTOAM1', 'SITESWCHBTOAM2', 'SITESWCHBTOAM3', 'SITESWCHBTOAM4']
all_job_list = []
all_pred_job_list = []

for ad in results:
    if ad.adid in ads:
        print ad.adid
        ad_dict[ad.adid] = ad
        all_job_list.append(ad.gen_job_list())
        all_pred_job_list.append(ad.gen_pred_job_list(ad_dict))


file_handle = open(r'c:\graph.txt', 'w')
file_handle.write('\r\n'.join(all_job_list))
file_handle.write('\r\n')
file_handle.write('\r\n'.join(all_pred_job_list))



'''
content = []
for ad in results:
    content.append(str(ad))

content = ''.join(content)

file_name = r'c:\tws_template.html'
file_handle = open(file_name, 'r')
html = file_handle.read()
html = string.replace(html, '{content}', content)

file_handle.close()

output_file_name = r'c:\tws.html'
file_handle = open(output_file_name, 'w')
file_handle.write(html)
file_handle.close()




