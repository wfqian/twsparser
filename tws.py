__author__ = 'QWF'


class JobDep(object):
    def __init__(self, token):
        self.is_different = False
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

    def is_external(self):
        return hasattr(self, 'preadid')

    def compare(self, rhs):
        lhs = self
        for k, v in vars(lhs).items():
            if hasattr(rhs, k) and v == getattr(rhs, k):
                pass
            else:
                return False
        return True


class JobSR(object):
    def __init__(self, token):
        resource = ''
        # print token.keys()
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)


class Job(object):
    html_job = '<div class="ad-job">%s</div>'
    html_job_attr = '<div class="ad-job-attr">%s:%s</div>'
    html_job_body = '<div class="ad-job-body">%s</div>'

    def __init__(self, token):
        self.diff_prop_dict = {}
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

    def __str__(self):

        job_body_attrs = []
        for k, v in vars(self).items():
            job_body_attrs.append(Job.html_job_attr % (k.upper(), v))
        job_body_attrs = ''.join(job_body_attrs)
        return (Job.html_job % self.jobn) + (Job.html_job_body % job_body_attrs)

    def compare(self, rhs):
        lhs = self
        for k, v in vars(lhs).items():
            if k not in ['deps']:
                if hasattr(rhs, k):
                    rhs_value = getattr(rhs, k)
                    if v != rhs_value:
                        lhs.diff_prop_dict[k] = 1
                else:
                    lhs.diff_prop_dict[k] = 2
            else:
                for left_dep in lhs.deps:
                    found = False
                    for right_dep in rhs.deps:
                        if left_dep.compare(right_dep):
                            found = True
                    if not found:
                        left_dep.is_different = True
                        lhs.diff_prop_dict['deps'] = 1


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
        self.diff_prop_dict = {}
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

        # print ad_body_others
        ad_job_title = Ad.html_ad_job_title % self.job_numbers
        ad_jobs = Ad.html_ad_attr % ('Jobs', ad_job_title + ad_job_body)
        ad_body = Ad.html_ad_body % (ad_body_others + ad_jobs)
        return Ad.html_ad % (ad_title + ad_body)

    def compare(self, rhs):
        lhs = self
        for k, v in vars(lhs).items():
            if k not in ['jobs', 'job_dict']:
                if hasattr(rhs, k):
                    rhs_value = getattr(rhs, k)
                    if v != rhs_value:
                        lhs.diff_prop_dict[k] = 1
                else:
                    lhs.diff_prop_dict[k] = 2
            else:
                if k == 'jobs':
                    for left_job in lhs.jobs:
                        found = False
                        for right_job in rhs.jobs:
                            if left_job.jobn == right_job.jobn:
                                left_job.compare(right_job)
                                found = True
                        if not found:
                            left_job.diff_prop_dict['job'] = 2


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
                    job_pred_list.append(ad_dict[adid].job_dict[dep.preopno] + ',' + job.jobn)
        return '\r\n'.join(job_pred_list)




