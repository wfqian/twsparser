# coding=utf-8

__author__ = 'QWF'

import string
import argparse
from twsparser import make_all_ad_parser
from tws import *


def write_diff_file(ads1, ads2):
    content1 = []
    for ad in ads1:
        content1.append(str(ad))
    content1 = ''.join(content1)

    content2 = []
    for ad in ads2:
        content2.append(str(ad))
    content2 = ''.join(content2)

    file_name = r'c:\tws_template.html'
    file_handle = open(file_name, 'r')
    html = file_handle.read()
    html = string.replace(html, "{content1}", content1)
    html = string.replace(html, "{content2}", content2)
    file_handle.close()

    output_file_name = r'c:\tws.html'
    file_handle = open(output_file_name, 'w')
    file_handle.write(html)
    file_handle.close()


def make_ad_compare(ads1, ads2):
    for ad1 in ads1:
        for ad2 in ads2:
            if ad1.adid == ad2.adid:
                ad1.compare(ad2)
                ad2.compare(ad1)

    write_diff_file(ads1, ads2)




'''
parser = argparse.ArgumentParser()
parser.add_argument("echo", help="echo the detail argments about the compare information", type=int)
parser.add_argument("-v", "--verbose", help="verbose infomation about compare", action="store_true")
args = parser.parse_args()
print args.echo
'''


ad_parser = make_all_ad_parser()

#adruns = make_ad_parser().parseString(
#    r"ADDEP  ACTION(ADD) PREWSID(PNCP) PREOPNO( 143) ADDEP  ACTION(ADD) PREWSID(PNCP) PREOPNO( 143)", True)
result_ads1 = ad_parser.parseFile(r"c:\parseTws.txt", parseAll=True)
result_ads2 = ad_parser.parseFile(r"c:\parseTws2.txt", parseAll=True)

make_ad_compare(result_ads1, result_ads2)


'''
ad_dict = {}
ads = ['SITESWCHBTOAM0', 'SITESWCHBTOAM1', 'SITESWCHBTOAM2', 'SITESWCHBTOAM3', 'SITESWCHBTOAM4']
all_job_list = []
all_pred_job_list = []

for ad in result_ads1:
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





