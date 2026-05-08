from django.db import models


class CultureRequest(models.Model):
    class MainCategory(models.TextChoices):
        TRADITION = "TRADITION", "전통문화"
        PERFORMANCE = "PERFORMANCE", "공연"
        EXHIBITION = "EXHIBITION", "전시"
        EXPERIENCE = "EXPERIENCE", "체험"
        ETC = "ETC", "기타"

    class TargetAge(models.TextChoices):
        ALL = "ALL", "전체"
        TEEN = "TEEN", "청소년"
        YOUTH = "YOUTH", "청년"
        SENIOR = "SENIOR", "고령층"

    class PreferredTime(models.TextChoices):
        WEEKDAY_MORNING = "WEEKDAY_MORNING", "평일 오전"
        WEEKDAY_AFTERNOON = "WEEKDAY_AFTERNOON", "평일 오후"
        WEEKDAY_EVENING = "WEEKDAY_EVENING", "평일 저녁"
        WEEKEND_MORNING = "WEEKEND_MORNING", "주말 오전"
        WEEKEND_AFTERNOON = "WEEKEND_AFTERNOON", "주말 오후"
        WEEKEND_EVENING = "WEEKEND_EVENING", "주말 저녁"

    class BudgetRange(models.TextChoices):
        FREE = "FREE", "무료"
        UNDER_10000 = "UNDER_10000", "1만원 이하"
        UNDER_30000 = "UNDER_30000", "3만원 이하"
        UNDER_50000 = "UNDER_50000", "5만원 이하"
        ANY = "ANY", "상관없음"

    sido = models.CharField(max_length=30)
    sigungu = models.CharField(max_length=30)
    region_label = models.CharField(max_length=60, blank=True)

    main_category = models.CharField(
        max_length=30,
        choices=MainCategory.choices,
        default=MainCategory.ETC,
    )
    target_age = models.CharField(
        max_length=30,
        choices=TargetAge.choices,
        default=TargetAge.ALL,
    )
    preferred_time = models.CharField(
        max_length=30,
        choices=PreferredTime.choices,
        default=PreferredTime.WEEKEND_AFTERNOON,
    )
    budget_range = models.CharField(
        max_length=30,
        choices=BudgetRange.choices,
        default=BudgetRange.FREE,
    )

    title = models.CharField(max_length=100, blank=True)
    content = models.TextField()

    embedding = models.JSONField(null=True, blank=True)
    cluster = models.ForeignKey(
        "RequestCluster",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="requests",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.region_label:
            self.region_label = f"{self.sido} {self.sigungu}".strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.region_label}] {self.content[:30]}"


class RequestCluster(models.Model):
    class Status(models.TextChoices):
        COLLECTING = "COLLECTING", "요청 수집 중"
        READY = "READY", "프로그램 생성 가능"
        PROGRAM_CREATED = "PROGRAM_CREATED", "프로그램 생성 완료"

    title = models.CharField(max_length=120)
    summary = models.TextField(blank=True)

    sido = models.CharField(max_length=30)
    sigungu = models.CharField(max_length=30)
    region_label = models.CharField(max_length=60)

    main_category = models.CharField(max_length=30)
    target_age = models.CharField(max_length=30)
    preferred_time = models.CharField(max_length=30)
    budget_range = models.CharField(max_length=30)

    representative_text = models.TextField(blank=True)
    centroid = models.JSONField(null=True, blank=True)

    request_count = models.PositiveIntegerField(default=0)
    threshold = models.PositiveIntegerField(default=3)
    progress_ratio = models.FloatField(default=0.0)
    remaining_count = models.PositiveIntegerField(default=3)

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.COLLECTING,
    )

    fair_score = models.FloatField(default=50.0)
    fair_reason = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_ready(self):
        return self.status == self.Status.READY

    @property
    def status_display(self):
        return self.get_status_display()

    @property
    def status_message(self):
        if self.status == self.Status.READY:
            return "문화 프로그램으로 제안 가능한 상태입니다."
        return f"{self.remaining_count}개의 요청이 더 모이면 프로그램으로 제안할 수 있습니다."

    def __str__(self):
        return f"{self.title} ({self.request_count}/{self.threshold})"


class CultureProgram(models.Model):
    cluster = models.OneToOneField(
        RequestCluster,
        on_delete=models.CASCADE,
        related_name="program",
    )
    title = models.CharField(max_length=120)
    description = models.TextField()
    place_name = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=200, blank=True)

    creator_name = models.CharField(max_length=80, blank=True)
    is_local_creator = models.BooleanField(default=True)
    is_small_creator = models.BooleanField(default=True)
    is_traditional = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title