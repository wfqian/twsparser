import types

__author__ = 'QWF'


class JobDep(object):

    def __init__(self, token):
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

    def is_external(self):
        return hasattr(self, 'preadid')


class JobSR(object):

    def __init__(self, token):
        resource = ''
        #print token.keys()
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)


class Job(object):

    html_job = '<div class="ad-job">%s</div>'
    html_job_attr = '<div class="ad-job-attr">%s:%s</div>'
    html_job_body = '<div class="ad-job-body">%s</div>'

    def __init__(self, token):
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

    def __str__(self):

        job_body_attrs = []
        for k, v in vars(self).items():
            job_body_attrs.append(Job.html_job_attr % (k.upper(), v))
        job_body_attrs = ''.join(job_body_attrs)

        return (Job.html_job % self.jobn) + (Job.html_job_body % job_body_attrs)

    def has_deps(self):
        return hasattr(self, 'deps')


class Ad(object):
    html_ad = '<div class="ad">%s</div>'
    html_ad_title = '<div class="ad-title">%s</div>'
    html_ad_body = '<div class="ad-body">%s</div>'
    html_ad_attr = '<div class = "ad-body-attr">%s : %s</div>'
    html_ad_job_title = '<div class="ad-job-title">All Jobs(Total Number is %s)</div>'

    def __init__(self, token):
        self.job_numbers = 0
        self.job_dict = {}
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

        self.job_numbers = len(self.jobs)
        for job in self.jobs:
            self.job_dict[job.opno] = job.jobn

    def __str__(self):
        ad_title = Ad.html_ad_title % self.adid
        ad_job_body = []
        for job in self.jobs:
            ad_job_body.append(str(job))
        ad_job_body = ''.join(ad_job_body)

        ad_body_others = []
        for k, v in vars(self).items():
            if k not in ['jobs', 'job_dict']:
                ad_body_others.append(Ad.html_ad_attr % (k.upper(), v))
        ad_body_others = ''.join(ad_body_others)

        #print ad_body_others
        ad_job_title = Ad.html_ad_job_title % self.job_numbers
        ad_jobs = Ad.html_ad_attr % ('Jobs', ad_job_title + ad_job_body)
        ad_body = Ad.html_ad_body % (ad_body_others + ad_jobs)
        return Ad.html_ad % (ad_title + ad_body)

    def gen_job_list(self):
        job_list = []
        for job in self.jobs:
            job_list.append(job.jobn)
        return '\r\n'.join(job_list)

    def gen_pred_job_list(self, ad_dict):
        job_pred_list = []
        for job in self.jobs:
            if job.has_deps():
                for dep in job.deps:
                    adid = self.adid
                    if dep.is_external():
                        adid = dep.preadid
                    #print ad_dict[adid].job_dict
                    job_pred_list.append(ad_dict[adid].job_dict[dep.preopno] + ',' + job.jobn)
        return '\r\n'.join(job_pred_list)




