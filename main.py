# coding=utf-8

__author__ = 'QWF'

import string
import argparse
import twsparser
import xlwt


def write_diff_file(ads1, ads2):
    content1 = []
    for ad in ads1:
        content1.append(str(ad))
    content1 = ''.join(content1)

    content2 = []
    for ad in ads2:
        content2.append(str(ad))
    content2 = ''.join(content2)

    file_name = r'assets/tws_template.html'
    file_handle = open(file_name, 'r')
    html = file_handle.read()
    html = string.replace(html, "{content1}", content1)
    html = string.replace(html, "{content2}", content2)
    file_handle.close()

    output_file_name = r'tws.html'
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


def write_to_xsl(ads):
    def format_adrule(adrule):
        if hasattr(adrule, 'every'):
            if hasattr(adrule, 'day') and hasattr(adrule, 'week'):
                return 'EVERYDAY'
            else:
                return ''
        else:
            pass

    book = xlwt.Workbook()
    sheet_ad = book.add_sheet('AD')
    line_no = 0

    ad_job_dict = {}
    for ad in ads:
        '''
        if ad.adid != 'SCACSYSBKP':
            continue
        '''
        ad_job_dict[ad.adid] = ad.job_dict
        sheet_ad.write(line_no, 0, 'NOVAS2')
        sheet_ad.write(line_no, 1, '909315004167')
        sheet_ad.write(line_no, 2, ad.adid)
        sheet_ad.write(line_no, 3, ad.adtype)
        sheet_ad.write(line_no, 4, ad.owner)
        sheet_ad.write(line_no, 5, 'N/A')
        sheet_ad.write(line_no, 6, 'NEW')

        if hasattr(ad, 'runrules'):
            cell_content = ''
            for runrule in ad.runrules:
                rule = format_adrule(runrule[1])
                if rule == 'EVERYDAY':
                    cell_content = 'EVERYDAY'
                else:
                    # cell_content = ''
                    cell_content += "%s{%s}" % (runrule[0].type, rule)

                    #sheet_ad.write(line_no, 7, cell_content)
        line_no += 1

    sheet_job = book.add_sheet('JOB')
    line_no = 0
    for ad in ads:
        for jobsr in ad.jobsrs:
            sheet_job.write(line_no, 0, 'NOVAS2')
            sheet_job.write(line_no, 1, '909315004167')
            col2_job = jobsr.job.jobn
            sheet_job.write(line_no, 2, jobsr.job.jobn)
            sheet_job.write(line_no, 3, 'NEW')
            col4_adid = ad.adid
            sheet_job.write(line_no, 4, ad.adid)
            col5_highrc = '0'
            if hasattr(jobsr.job, 'highrc'):
                col5_highrc = jobsr.job.highrc
                sheet_job.write(line_no, 5, col5_highrc)
            col6_time = jobsr.job.time
            sheet_job.write(line_no, 6, jobsr.job.time)

            col7_starttime = ''
            if hasattr(jobsr.job, 'startday') and hasattr(jobsr.job, 'starttime'):
                starttime = jobsr.job.starttime[0:2] + ':' + jobsr.job.starttime[2:]
                sheet_job.write(line_no, 7, '0' + jobsr.job.startday + ' ' + starttime)
                col7_starttime = '0' + jobsr.job.startday + ' ' + starttime
            else:
                sheet_job.write(line_no, 7, 'N/A')
                col7_starttime = 'N/A'

            sheet_job.write(line_no, 8, 'N/A')

            col10_str = 'N/A'
            sr_str = ''
            if hasattr(jobsr, 'srs') and getattr(jobsr, 'srs') != '':
                for sr in jobsr.srs:
                    sr_str += sr.resource + '\n'
            else:
                sr_str = 'N/A'

            if sr_str == 'N/A':
                sheet_job.write(line_no, 9, 'N/A')
            else:
                sheet_job.write(line_no, 9, 'ADD')

            sheet_job.write(line_no, 10, sr_str)
            sheet_job.write(line_no, 11, 'N/A')
            sheet_job.write(line_no, 12, 'P')
            sheet_job.write(line_no, 13, 'Y')
            sheet_job.write(line_no, 14, 'Y')
            sheet_job.write(line_no, 15, 'Y')
            sheet_job.write(line_no, 16, 'Y')
            line_no += 1

            if hasattr(jobsr.job, 'deps'):
                for dep in jobsr.job.deps:
                    sheet_job.write(line_no, 0, 'NOVAS2')
                    sheet_job.write(line_no, 1, '909315004167')
                    sheet_job.write(line_no, 2, col2_job)
                    sheet_job.write(line_no, 3, 'UPDATE')
                    sheet_job.write(line_no, 4, col4_adid)
                    sheet_job.write(line_no, 5, col5_highrc)
                    sheet_job.write(line_no, 6, col6_time)
                    sheet_job.write(line_no, 7, col7_starttime)
                    sheet_job.write(line_no, 8, 'N/A')
                    sheet_job.write(line_no, 9, 'ADD')
                    sheet_job.write(line_no, 10, col10_str)
                    opno = dep.preopno
                    ad_name = ad.adid
                    job_name = ''
                    if dep.is_external():
                        ad_name = dep.preadid

                    if ad_name in ad_job_dict.keys():
                        try:
                            job_name = ad_job_dict[ad_name][opno]
                        except KeyError:
                            job_name = '------'
                    else:
                        job_name = 'XXXXXX'
                    sheet_job.write(line_no, 11, job_name)
                    sheet_job.write(line_no, 12, 'P')
                    sheet_job.write(line_no, 13, 'Y')
                    sheet_job.write(line_no, 14, 'Y')
                    sheet_job.write(line_no, 15, 'Y')
                    sheet_job.write(line_no, 16, 'Y')
                    line_no += 1

    book.save(r'applications_output.xls')


try:
    parser = argparse.ArgumentParser(description='TWS Useful Tool')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c", "--comp", nargs=2, help='compare two file in html format', metavar=('file1', 'file2'))
    group.add_argument("-x", "--xsl", nargs=1, metavar='file')
    args = parser.parse_args()
except Exception, e:
    print e


if args.xsl:
    # print args.xsl[0]
    try:
        ad_parser = twsparser.make_all_ad_parser()
        result_ads1 = ad_parser.parseFile(args.xsl[0], parseAll=True)
        write_to_xsl(result_ads1)
    except Exception, e:
        print 'An error occurred, please send following message to boss Qian: ', e
elif args.comp:
    try:
        file1 = args.comp[0]
        file2 = args.comp[1]
        ad_parser = twsparser.make_all_ad_parser()
        result_ads1 = ad_parser.parseFile(file1, parseAll=True)
        result_ads2 = ad_parser.parseFile(file2, parseAll=True)
        make_ad_compare(result_ads1, result_ads2)
    except Exception, e:
        print 'An error occurred, please send following message to boss Qian: ', e
else:
        print 'please type twsbox -h and refer to the user manual'


'''
ad_parser = make_all_ad_parser()
result_ads1 = ad_parser.parseFile(r"c:\TWSNOVA.UNLOAD.AD.TEMP.D141218A", parseAll=True)
write_to_xsl(result_ads1)
'''
'''
#result_ads1 = ad_parser.parseFile(r"c:\parseTws.txt", parseAll=True)
result_ads2 = ad_parser.parseFile(r"c:\parseTws2.txt", parseAll=True)
make_ad_compare(result_ads1, result_ads2)
'''

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

