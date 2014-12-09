__author__ = 'QWF'

from pyparsing import *

from tws import Job, JobSR, JobDep, Ad, AdRule, AdRun


def make_all_ad_parser():
    t_lpare = Literal('(').suppress()
    t_rpare = Literal(')').suppress()

    def make_list(t):
        pass

    def create_ad():
        pass

    def create_expr(literalname, resultname):
        return Literal(literalname + '(').suppress() + Word(alphanums)(resultname) + t_rpare

    def make_job_deps_parser():
        pre_adid = Literal('PREADID(').suppress() + Word(alphanums)("preadid") + t_rpare
        pre_wsid = Literal('PREWSID(').suppress() + Word(alphanums)("prewsid") + t_rpare
        pre_opno = Literal('PREOPNO(').suppress() + Word(alphanums)("preopno") + t_rpare
        pre_jobn = Literal('PREJOBN(').suppress() + Word(alphanums)("prejobn") + t_rpare
        transpt = Literal('PREJOBN(').suppress() + Word(alphanums)("transpt") + t_rpare
        descr = Literal('PREJOBN(').suppress() + Word(alphanums)("descr") + t_rpare
        job_dep = Literal('ADDEP').suppress() + Literal('ACTION(ADD)').suppress() + OneOrMore(
            pre_wsid | pre_opno | pre_jobn | pre_adid | transpt | descr)
        job_dep.setParseAction(lambda t: JobDep(t))

        # job_dep.parseWithTabs()
        return job_dep

    def make_job_adsr_parser():
        def create_job_adsr(t):
            return JobSR(t)
            # if not t.haskeys('resource'):
            # #raise ParseException("")
            # pass

        action = create_expr("ACTION", 'action')
        resource = Literal('RESOURCE(\'').suppress() + Word(alphanums)('resource') + Literal('\')').suppress()
        usage = create_expr("USAGE", 'usage')
        quantity = create_expr("QUANTITY", 'quantity')
        job_adsr = Literal('ADSR') + Each([resource, Optional(action), Optional(usage), Optional(quantity)])
        job_adsr.setParseAction(lambda t: create_job_adsr(t))
        return job_adsr

    def make_job_parser():
        action = create_expr('ACTION', 'action')
        opno = create_expr('OPNO', 'opno')
        # jobn = create_expr('JOBN', 'jobn')
        jobn = (Literal('jobN(').suppress() | Literal('JOBN(').suppress()) + Word(alphanums)('jobn') + t_rpare
        wsid = create_expr('WSID', 'wsid')
        adopcatm = create_expr('ADOPCATM', 'adopcatm')
        adopexpjcl = create_expr('ADOPEXPJCL', 'adopexpjcl')
        adopjobcrt = create_expr('ADOPJOBCRT', 'adopjobcrt')
        adopjobpol = create_expr('ADOPJOBPOL', 'adopjobpol')
        adoppwto = create_expr('ADOPPWTO', 'adoppwto')
        adopusrsys = create_expr('ADOPUSRSYS', 'adopusrsys')
        adopwlmclass = create_expr('ADOPWLMCLASS', 'adopwlmclass')
        aec = create_expr('AEC', 'aec')
        ajr = create_expr('AJR', 'ajr')
        ajsub = create_expr('AJSUB', 'ajsub')
        clate = create_expr('CLATE', 'clate')
        condrjob = create_expr('CONDRJOB', 'condrjob')
        cscript = create_expr('CSCRIPT', 'cscript')
        descr = create_expr('DESCR', 'descr')
        dlday = create_expr('DLDAY', 'dlday')
        dltime = create_expr('DLTIME', 'dltime')
        duration = create_expr('DURATION', 'duration')
        form = create_expr('FORM', 'form')
        highrc = create_expr('HIGHRC', 'highrc')
        jobclass = create_expr('JOBCLASS', 'jobclass')
        limfdbk = create_expr('LIMFDBK', 'limfdbk')
        monitor = create_expr('MONITOR', 'monitor')
        prejobn = create_expr('PREJOBN', 'prejobn')
        prewsid = create_expr('PREWSID', 'prewsid')
        preopno = create_expr('PREOPNO', 'preopno')
        prtclass = create_expr('PRTCLASS', 'prtclass')
        psnum = create_expr('PSNUM', 'psnum')
        reroutable = create_expr('REROUTABLE', 'reroutable')
        restartable = create_expr('RESTARTABLE', 'restartable')
        smoothing = create_expr('SMOOTHING', 'smoothing')
        startday = create_expr('STARTDAY', 'startday')
        starttime = create_expr('STARTTIME', 'starttime')
        time = create_expr('TIME', 'time')
        usesai = create_expr('USESAI', 'usesai')
        usextname = create_expr('USEXTNAME', 'usextname')
        usextse = create_expr('USEXTSE', 'usextse')

        job_dep = make_job_deps_parser()
        job_adsr = make_job_adsr_parser()

        job = Literal('ADOP') + OneOrMore(action | opno | jobn | wsid | adopcatm | adopexpjcl | adopjobcrt |
                                          adopjobpol | adoppwto | adopusrsys |
                                          adopwlmclass | aec | ajr | ajsub | clate | condrjob | cscript | descr | dlday | dltime |
                                          duration | form | highrc | jobclass | limfdbk | monitor | prejobn | prewsid | preopno | prewsid |
                                          prtclass | psnum | reroutable | restartable | smoothing | startday | starttime | time | usesai |
                                          usextname | usextse | job_adsr) + ZeroOrMore(job_dep)('deps')
        job.setParseAction(lambda t: Job(t))
        return job

    def make_adrun_parser():
        action = create_expr('ACTION', 'action')
        iatime = create_expr('IATIME', 'iatime')
        dlday = create_expr('DLDAY', 'dlday')
        dltime = create_expr('DLTIME', 'dltime')
        name = create_expr('NAME', 'name')
        rule = create_expr('RULE', 'rule')
        adrun_type = create_expr('TYPE', 'type')
        valfrom = create_expr('VALFROM', 'valfrom')
        valto = create_expr('VALTO', 'valto')
        adrun = Literal('ADRUN') + OneOrMore(
            action | dlday | dltime | valfrom | valto | name | rule | adrun_type | iatime)
        return adrun

    def make_adrule_parser():
        def make_optional_list(name):
            delimited_list = OneOrMore(Word(alphanums))
            #print delimited_list
            rule_list = Optional(Literal('(') + delimited_list + Literal(')'))
            rule_list.setParseAction(lambda t: make_list(t))
            return Group(Literal(name) + rule_list)(name.lower())

        every = make_optional_list("EVERY")
        only = make_optional_list("ONLY")
        last = make_optional_list("LAST")
        day = make_optional_list("DAY")
        week = make_optional_list("WEEK")
        month = make_optional_list("MONTH")
        period = make_optional_list("PERIOD")
        year = Literal('YEAR')
        originshift = make_optional_list("ORIGINSHIFT")

        adrule = Literal('ADRULE') + OneOrMore(every | only | last | day | week | month | period | year | originshift)

        return adrule

    def make_ad_parser():
        action = create_expr('ACTION', 'action')
        adid = create_expr('ADID', 'adid')
        adgroupid = create_expr('ADGROUPID', 'adgroupid')
        adstat = create_expr('ADSTAT', 'adstat')
        adtype = create_expr('ADTYPE', 'adtype')
        advalfrom = create_expr('ADVALFROM', 'advalfrom')
        calendar = create_expr('CALENDAR', 'calendar')
        descr = Literal('DESCR(\'').suppress() + Optional(ZeroOrMore(Word(alphanums + '\&'))) + Literal('\')').suppress()
        dlimfdbk = create_expr('DLIMFDBK', 'dlimfdbk')
        dsmoothing = create_expr('DSMOOTHING', 'dsmoothing')
        group = create_expr('GROUP', 'group')
        odescr = Literal('ODESCR(\'').suppress() + Word(alphanums)('odescr') + Literal('\')').suppress()
        owner = Literal('OWNER(\'').suppress() + Word(alphanums)('owner') + Literal('\')').suppress()
        priority = create_expr('PRIORITY', 'priority')

        ad_parts_list = [adid, Optional(action), Optional(owner), Optional(adgroupid), Optional(adstat),
                         Optional(adtype),
                         Optional(advalfrom), Optional(calendar), Optional(descr), Optional(dlimfdbk),
                         Optional(dsmoothing), Optional(odescr), Optional(group), Optional(priority)]

        adrun = make_adrun_parser()
        adrun.setResultsName('adrun')
        adrun.setParseAction(lambda t: AdRun(t))

        adrule = make_adrule_parser()
        adrule.setResultsName('adrule')
        adrule.setParseAction(lambda t: AdRule(t))
        #print adrule

        job = make_job_parser()
        adsr = make_job_adsr_parser()

        jobsr = Group(job('job') + ZeroOrMore(adsr)('srs'))
        jobsr.setResultsName('jobsr')

        # ad = Literal('ADSTART') + Each(ad_parts_list) + ZeroOrMore(adrun | adrule) + OneOrMore(job)('jobs')
        ad_run_rule = Group(adrun + adrule)('runrule')
        ad = Literal('ADSTART') + Each(ad_parts_list) + ZeroOrMore(ad_run_rule)('runrules') + OneOrMore(jobsr)('jobsrs')
        return ad.setParseAction(lambda t: Ad(t))

    #return make_adrule_parser()
    return OneOrMore(make_ad_parser())













