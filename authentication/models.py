import string
from typing import Any
from django.db import models
from utils import mixins, builders
from accounting.models import FiscalYear, Account
from django.utils import timezone
import datetime


class Account(models.Model):
    def get_transactions(self) -> models.QuerySet:
        pass

    def yearly_transactions(self, year=FiscalYear.get_active()):
        return self.get_interval_transactions(year.start, year.end)

    def daily_transactions(self, date=timezone.now().date()):
        start = datetime.datetime.combine(date, datetime.time(0, 0, 0))
        end = start + datetime.timedelta(days=1)
        return self.get_interval_transactions(start, end)

    def get_interval_transactions(
        self, start: datetime.date = None, end: datetime.date = None
    ):
        return self.get_transactions().filter(
            created_at__gte=start, created_at__lte=end
        )


class LedgerManager(models.Manager):
    def create(account_id: int):
        pass


class Ledger(models.Model):
    account = models.ForeignKey(to="accounting.Account")
    total_count = models.IntegerField()
    total_amount = models.StandardDecimal()
    total_positive = models.StandardDecimal()
    total_negative = models.StandardDecimal()
    average_amount = models.StandardDecimal()
    start = models.DateTimeField()
    end = models.DateTimeField()
    children = models.ManyToManyField(to="ledgers.Ledger")

    pass


class YearlyLedgerManager(models.Manager):
    def fetch_for_year(
        self, account_id: int, year: FiscalYear, recalculate: bool = False
    ):
        (ledger, created) = super().get_or_create(
            year=year,
            defaults={
                "year": year,
                "account_id": account_id,
                "start": year.start_date,
                "end": year.end_date,
            },
        )
        if created or recalculate:
            # TODO recalculate
            pass
        return ledger

    def fetch(self, account_id: int, recalculate: bool = False):
        year = FiscalYear.get_active()
        return self.retrieve_for_fiscal(account_id, year, recalculate)


class DailyLedgerManager(models.Manager):
    def fetch_for_date(
        self, account_id: int, date: datetime.date, recalculate: bool = False
    ):
        start = datetime.datetime.combine(date, datetime.time(0, 0, 0))
        (ledger, created) = super().get_or_create(
            date=date,
            defaults={
                "date": date,
                "account_id": account_id,
                "start": start,
                "end": start + datetime.timedelta(days=1),
            },
        )
        if created or recalculate:
            # TODO recalculate
            pass
        return ledger

    def fetch(self, account_id: int, recalculate: bool = False):
        return self.retrieve_for_date(account_id, timezone.now().date(), recalculate)

    def get(self, account_id: int, date: datetime.date = timezone.now().date()):
        return super().get(account_id=account_id, date=date)

    def filter(self, account_id, start_date, end_date):
        return super().filter(
            account_id=account_id, date_gte=start_date, date_lte=end_date
        )


class YearlyLedger(Ledger):
    class Meta:
        abstract = True

    year = models.ForeignKey(to="accounting.FiscalYear")

    def get_daily_set(self):
        return DailyLedger.objects.filter(
            acconut=self.account,
            date__gte=self.year.start_date,
            date__lte=self.year.end_date,
        )


class DailyLedger(Ledger):
    class Meta:
        abstract = True

    date = models.DateField()

    def get_daily_set(self):
        return DailyLedger.objects.filter(
            acconut=self.account,
            date__gte=self.year.start_date,
            date__lte=self.year.end_date,
        )


class CodingLedger(Ledger):
    class Meta:
        abstract = True

    account = models.ForeignKey(to="accounting.Coding")


class CodingLedger(Ledger):
    class Meta:
        abstract = True

    account = models.ForeignKey(to="accounting.Coding")


class GeneralLedger(Ledger):
    class Meta:
        abstract = True

    account = models.ForeignKey(to="accounting.General")


class SubsidaryLedger(Ledger):
    class Meta:
        abstract = True

    account = models.ForeignKey(to="accounting.Subsidary")


class StorageLedger(Ledger):
    class Meta:
        abstract = True

    account = models.ForeignKey(to="accounting.Storage")


class DetailLedger(Ledger):
    class Meta:
        abstract = True

    account = models.ForeignKey(to="accounting.Detail")


class DailyCodingLedger(DailyLedger, CodingLedger):
    pass


class Transaction(models.Model):
    pass


class Detail(models.Model):
    pass


class Subsidary(models.Model):
    pass


class Coding(models.Model):
    pass


class General(models.Model):
    pass


def run_task(id):
    task = Task.objects.get(id=id)
    if task.action == "update_ledger":
        pass
    if task.action == "terminate":
        pass
    if task.action == "success":
        pass
    if task.action == "failure":
        job = task.job
        job.status = Job.FAILED
        job.save()
        Job.objects.run_next()
        pass


def update_ledgers(transaction_ids: list):
    pass


class JobManager(models.Manager):
    def get_next(self):
        return self.filter(status=Job.QUEUED).first()


class Job(models.Model):
    objects = JobManager()
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEED = "succeed"
    FAILED = "failed"
    STATUS_CHOICES = (
        (QUEUED, QUEUED),
        (RUNNING, RUNNING),
        (SUCCEED, SUCCEED),
        (FAILED, FAILED),
    )
    type = models.CharField(max_length=20)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=QUEUED)
    start = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True, blank=True, default=None)

    @property
    def duration(self):
        if self.end:
            return self.end - self.start
        else:
            return timezone.now() - self.start

    def finished(self):
        self.end = timezone.now()
        self.status = Job.SUCCEED
        self.save()


class TaskManager(models.Manager):
    def get_next(self):
        return self.filter(job__status=Job.RUNNING, status=Task.QUEUED).first()


class Task(models.Model):
    class Meta:
        ordering = ["order"]

    QUEUED = "queued"
    SUCCEED = "succeed"
    FAILED = "failed"
    STATUS_CHOICES = (
        (QUEUED, QUEUED),
        (SUCCEED, SUCCEED),
        (FAILED, FAILED),
    )
    job = models.ForeignKey(to="Job")
    order = models.FloatField(default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=QUEUED)
    action = models.CharField(max_length=20)
    args = models.JSONField()
