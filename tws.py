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
    HTML_JOB = '<div class="ad-job">%s</div>'
    HTML_JOB_ATTR = '<div class="ad-job-attr">%s:%s</div>'
    HTML_JOB_BODY = '<div class="ad-job-body">%s</div>'

    def __init__(self, token):
        self.diff_attr_dict = {}
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

    def __str__(self):

        job_body_attrs = []
        for k, v in vars(self).items():
            if k in self.diff_attr_dict:
                job_body_attrs.append(Job.HTML_JOB_ATTR % (k.upper(), v))
        job_body_attrs = ''.join(job_body_attrs)
        return (Job.HTML_JOB % self.jobn) + (Job.HTML_JOB_BODY % job_body_attrs)

    def has_diff_attr(self):
        if len(self.diff_attr_dict) > 0:
            return True
        else:
            return False

    def compare(self, rhs):
        lhs = self
        for k, v in vars(lhs).items():
            if k not in ['deps', 'diff_attr_dict']:
                if hasattr(rhs, k):
                    rhs_value = getattr(rhs, k)
                    if v != rhs_value:
                        #print k
                        lhs.diff_attr_dict[k] = 1
                else:
                    lhs.diff_attr_dict[k] = 2
            else:
                if k == 'deps':
                    for left_dep in lhs.deps:
                        match = False
                        for right_dep in rhs.deps:
                            if left_dep.compare(right_dep):
                                match = True
                        if not match:
                            left_dep.is_different = True
                            lhs.diff_attr_dict['deps'] = 1
        return self.has_diff_attr()

    def has_deps(self):
        return hasattr(self, 'deps')


class Ad(object):
    HTML_AD = '<div class="ad">%s</div>'
    HTML_AD_TITLE = '<div class="ad-title">%s</div>'
    HTML_AD_BODY = '<div class="ad-body">%s</div>'
    HTML_AD_ATTR = '<div class = "ad-body-attr">%s : %s</div>'
    HTML_AD_JOB_TITLE = '<div class="ad-job-title">All Jobs(Total Number is %s)</div>'

    def __init__(self, token):
        self.job_numbers = 0
        self.job_dict = {}
        self.diff_attr_dict = {}
        for key in token.keys():
            self.__dict__[key] = getattr(token, key)

        self.job_numbers = len(self.jobs)
        for job in self.jobs:
            self.job_dict[job.opno] = job.jobn

    def __str__(self):
        ad_title = Ad.HTML_AD_TITLE % self.adid
        ad_job_body = []
        for job in self.jobs:
            if job.has_diff_attr():
                ad_job_body.append(str(job))
        ad_job_body = ''.join(ad_job_body)

        ad_body_others = []
        for k, v in vars(self).items():
            if k not in ['jobs', 'job_dict'] and k in self.diff_attr_dict:
                ad_body_others.append(Ad.HTML_AD_ATTR % (k.upper(), v))
        ad_body_others = ''.join(ad_body_others)

        # print ad_body_others
        ad_jobs = ''
        print self.diff_attr_dict
        if 'job' in self.diff_attr_dict:
            print self.diff_attr_dict
            ad_job_title = Ad.HTML_AD_JOB_TITLE % self.job_numbers
            ad_jobs = Ad.HTML_AD_ATTR % ('Jobs', ad_job_title + ad_job_body)

        ad_body = Ad.HTML_AD_BODY % (ad_body_others + ad_jobs)
        return Ad.HTML_AD % (ad_title + ad_body)

    def has_diff_attr(self):
        if len(self.diff_attr_dict) > 0:
            return True
        else:
            return False

    def compare(self, rhs):
        lhs = self
        #print "Compare executed here"
        '''
        if self.adid == 'SITESWCHBTOAM0':
            print self.__dict__
            print rhs.__dict__
        '''
        for k, v in vars(lhs).items():
            if k not in ['jobs', 'job_dict', 'diff_attr_dict']:
                if hasattr(rhs, k):
                    rhs_value = getattr(rhs, k)
                    if v != rhs_value:
                        lhs.diff_attr_dict[k] = 1
                else:
                    lhs.diff_attr_dict[k] = 2
            else:
                if k == 'jobs':
                    for left_job in lhs.jobs:
                        has_diff = False
                        for right_job in rhs.jobs:
                            if left_job.jobn == right_job.jobn:
                                #print "begin job compare"
                                has_diff = left_job.compare(right_job)
                        if has_diff:
                            lhs.diff_attr_dict['job'] = 2

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




