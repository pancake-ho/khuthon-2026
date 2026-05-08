"""
공공공간 및 문화공간 위치 데이터를 저장하는 모델 파일
"""

from django.db import models


class RequestCluster(models.Model):
    """
    비슷한 문화 요청들이 묶인 군집입니다.

    예:
    - 동대문구 청년 전통공예 체험 요청
    - 인천 중구 주말 가족 공연 요청
    - 강원도 춘천시 평일 저녁 지역문화 체험 요청
    """

    STATUS_CHOICES = [
        ("GATHERING", "요청 수집 중"),
        ("READY", "프로그램 생성 가능"),
        ("PROPOSED", "프로그램 후보 생성됨"),
        ("CLOSED", "종료"),
    ]

    title = models.CharField(
        max_length=150,
        verbose_name="군집 제목",
    )

    summary = models.TextField(
        blank=True,
        default="",
        verbose_name="군집 요약",
    )

    sido = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="시/도",
        help_text="예: 서울, 인천, 강원도, 전라도",
    )

    sigungu = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="시/군/구",
        help_text="예: 중구, 춘천시, 전주시",
    )

    region_label = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="지역 표시명",
        help_text="예: 인천 중구, 강원도 춘천시",
    )

    main_category = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="대표 문화 분야",
    )

    target_age = models.CharField(
        max_length=50,
        blank=True,
        default="전체",
        verbose_name="주요 대상",
    )

    preferred_time = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="대표 선호 시간대",
    )

    budget_range = models.CharField(
        max_length=50,
        blank=True,
        default="",
        verbose_name="대표 예산 범위",
    )

    request_count = models.PositiveIntegerField(
        default=0,
        verbose_name="요청 수",
    )

    threshold = models.PositiveIntegerField(
        default=30,
        verbose_name="프로그램 생성 기준 요청 수",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="GATHERING",
        verbose_name="군집 상태",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
    )

    class Meta:
        verbose_name = "요청 군집"
        verbose_name_plural = "요청 군집 목록"
        ordering = ["-request_count", "-created_at"]

    def __str__(self):
        return self.title

    def refresh_request_count(self):
        """
        이 군집에 연결된 요청 수를 다시 계산합니다.
        """
        self.request_count = self.requests.count()
        self.update_status_by_count(save=False)
        self.save(update_fields=["request_count", "status", "updated_at"])

    def update_status_by_count(self, save=True):
        """
        요청 수가 threshold 이상이면 READY 상태로 변경합니다.
        """
        if self.status == "GATHERING" and self.request_count >= self.threshold:
            self.status = "READY"

        if save:
            self.save(update_fields=["status", "updated_at"])


class CultureRequest(models.Model):
    """
    사용자가 직접 작성한 문화 요청입니다.

    FE에서 선택한 지역, 시간대, 예산, 대상, 카테고리와
    자유롭게 작성한 요청 내용을 함께 저장합니다.
    """

    CATEGORY_CHOICES = [
        ("TRADITIONAL", "전통문화"),
        ("PERFORMANCE", "공연"),
        ("EXHIBITION", "전시"),
        ("CRAFT", "공예"),
        ("MUSIC", "음악"),
        ("LOCAL", "지역문화"),
        ("CLASS", "체험/클래스"),
        ("ETC", "기타"),
    ]

    TIME_SLOT_CHOICES = [
        ("WEEKDAY_MORNING", "평일 오전"),
        ("WEEKDAY_AFTERNOON", "평일 오후"),
        ("WEEKDAY_EVENING", "평일 저녁"),
        ("FRIDAY_EVENING", "금요일 저녁"),
        ("SATURDAY_MORNING", "토요일 오전"),
        ("SATURDAY_AFTERNOON", "토요일 오후"),
        ("SUNDAY_AFTERNOON", "일요일 오후"),
        ("ANYTIME", "상관없음"),
    ]

    BUDGET_CHOICES = [
        ("FREE", "무료"),
        ("UNDER_30000", "3만원 이내"),
        ("UNDER_50000", "5만원 이내"),
        ("UNDER_100000", "10만원 이내"),
        ("OVER_100000", "10만원 이상"),
    ]

    TARGET_AGE_CHOICES = [
        ("TEEN", "청소년"),
        ("YOUTH", "청년"),
        ("ADULT", "성인"),
        ("SENIOR", "고령층"),
        ("FAMILY", "가족"),
        ("ALL", "전체"),
    ]

    STATUS_CHOICES = [
        ("SUBMITTED", "요청 등록"),
        ("CLUSTERED", "군집 연결 완료"),
        ("USED_FOR_PROGRAM", "프로그램 후보 반영"),
        ("ARCHIVED", "보관"),
    ]

    cluster = models.ForeignKey(
        RequestCluster,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="requests",
        verbose_name="연결된 요청 군집",
    )

    requester_nickname = models.CharField(
        max_length=50,
        blank=True,
        default="익명",
        verbose_name="요청자 닉네임",
    )

    title = models.CharField(
        max_length=150,
        verbose_name="요청 제목",
    )

    content = models.TextField(
        verbose_name="요청 내용",
        help_text="사용자가 자유롭게 작성한 문화 요청 내용",
    )

    sido = models.CharField(
        max_length=50,
        verbose_name="시/도",
        help_text="예: 인천, 강원도, 전라도",
    )

    sigungu = models.CharField(
        max_length=50,
        verbose_name="시/군/구",
        help_text="예: 중구, 춘천시, 전주시",
    )

    region_label = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="지역 표시명",
        help_text="예: 인천 중구, 강원도 춘천시",
    )

    category = models.CharField(
        max_length=30,
        choices=CATEGORY_CHOICES,
        default="ETC",
        verbose_name="문화 분야",
    )

    target_age = models.CharField(
        max_length=30,
        choices=TARGET_AGE_CHOICES,
        default="ALL",
        verbose_name="대상 연령",
    )

    preferred_time = models.CharField(
        max_length=30,
        choices=TIME_SLOT_CHOICES,
        default="ANYTIME",
        verbose_name="선호 시간대",
    )

    budget_range = models.CharField(
        max_length=30,
        choices=BUDGET_CHOICES,
        default="UNDER_30000",
        verbose_name="예산 범위",
    )

    mobility_limit = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="이동 제약 조건",
        help_text="예: 대중교통 가능, 도보 20분 이내, 이동 제약 있음",
    )

    keywords = models.CharField(
        max_length=255,
        blank=True,
        default="",
        verbose_name="추출 키워드",
        help_text="AI/키워드 군집화에 사용할 키워드",
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="SUBMITTED",
        verbose_name="요청 상태",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일",
    )

    class Meta:
        verbose_name = "문화 요청"
        verbose_name_plural = "문화 요청 목록"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        region_label이 비어 있으면 sido + sigungu로 자동 생성합니다.
        """
        if not self.region_label:
            self.region_label = f"{self.sido} {self.sigungu}".strip()

        super().save(*args, **kwargs)