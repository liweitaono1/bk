# -*- coding: utf-8 -*-
# from django.db import models

# Create your models here.
from django.db import models


class SelectScript(models.Model):
    scriptname = models.CharField(max_length=50, verbose_name=u"脚本名称")
    scriptcontent = models.TextField(verbose_name=u"脚本内容")

    def __str__(self):
        return self.scriptname


class Doinfo(models.Model):
    status_choice = [(1, "未执行"), (2, "正在执行"), (3, "执行成功"), (4, "执行失败")]
    businessname = models.CharField(max_length=50, verbose_name=u"业务", null=True, blank=True)
    username = models.CharField(max_length=50, verbose_name=u"用户", null=True, blank=True)
    script = models.ForeignKey(to='SelectScript', on_delete=models.CASCADE, verbose_name=u"脚本名称")
    createtime = models.DateTimeField(verbose_name=u"创建时间")
    starttime = models.DateTimeField(verbose_name=u"开始执行时间")
    endtime = models.DateTimeField(verbose_name=u"执行结束时间", null=True, blank=True)
    ipcount = models.IntegerField(verbose_name=u"执行数量")
    details = models.CharField(max_length=200, verbose_name=u"详细", null=True, blank=True)
    jobid = models.IntegerField(verbose_name=u"jobid")
    status = models.IntegerField(choices=status_choice, verbose_name=u"执行状态", default=2)
    log = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.businessname + self.script.scriptname

    class Meta:
        ordering = ["-id"]

    def to_dict(self, biz_map=None):
        if biz_map is None:
            biz_map = {}
        return {
            "id": self.id,
            "username": self.username,
            "starttime": self.starttime.strftime("%Y-%m-%d %H:%M:%S"),
            "businessname": biz_map.get(self.businessname, self.businessname),
            "script": self.script.scriptname,
            "scriptcontent": self.script.scriptcontent,
            "ipcount": self.ipcount,
            "jobid": self.jobid,
            "status": self.status,
            "log": self.log,
        }
