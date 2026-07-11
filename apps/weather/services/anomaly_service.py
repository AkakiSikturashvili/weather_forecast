"""
Service Layer #2 — Signature Feature: Statistical Anomaly Detection.

Rolling mean + std-dev ისტორიულ WeatherLog მონაცემებზე დაყრდნობით
ითვლის z-score-ს დღევანდელი ტემპერატურისთვის და აღნიშნავს, არის თუ არა
ის სტატისტიკური ანომალია (Variant seed%3 → threshold = 2σ).
"""
import statistics
from dataclasses import dataclass

from django.conf import settings

from ..models import WeatherLog


@dataclass
class AnomalyResult:
    is_anomaly: bool
    z_score: float | None
    mean: float | None
    std_dev: float | None
    sample_size: int
    threshold: float


class AnomalyDetectionService:
    """
    გამოთვლის z-score-ს:  z = (x - μ) / σ
    სადაც μ და σ გამოთვლილია ბოლო N დღის max_temp მონაცემებზე დაყრდნობით.
    """

    def __init__(self, window_days: int = 30, threshold: float | None = None):
        self.window_days = window_days
        self.threshold = threshold or settings.ANOMALY_ZSCORE_THRESHOLD

    def detect(self, location, current_temp: float) -> AnomalyResult:
        history = list(
            WeatherLog.objects.filter(location=location)
            .order_by('-date')
            .values_list('max_temp', flat=True)[: self.window_days]
        )

        if len(history) < 2:
            # საკმარისი ისტორია არ არსებობს ჯერ სანდო სტატისტიკისთვის
            return AnomalyResult(
                is_anomaly=False,
                z_score=None,
                mean=None,
                std_dev=None,
                sample_size=len(history),
                threshold=self.threshold,
            )

        mean = statistics.mean(history)
        std_dev = statistics.stdev(history)

        if std_dev == 0:
            z_score = 0.0
        else:
            z_score = (current_temp - mean) / std_dev

        return AnomalyResult(
            is_anomaly=abs(z_score) >= self.threshold,
            z_score=round(z_score, 2),
            mean=round(mean, 2),
            std_dev=round(std_dev, 2),
            sample_size=len(history),
            threshold=self.threshold,
        )
