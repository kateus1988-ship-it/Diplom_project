from django.db import models
from django.conf import settings

class Car(models.Model):
    RENT = 'rent'
    SALE = 'sale'
    TYPE_CHOICES = ((RENT, 'rent'), (SALE, 'sale'))

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars'
    )
    title = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text='$')
    brand_avto = models.CharField(max_length=100)
    engine_capacity = models.FloatField(help_text='m3')
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=100)
    year_manufacture = models.PositiveSmallIntegerField()
    body_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to='cars_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def cars_count(cls):
        return cls.objects.count()

    @classmethod
    def available_cars_count(cls):
        return cls.objects.filter(available=True).count()

    @classmethod
    def sold_cars_count(cls):
        return cls.objects.filter(available=False).count()


class DealRequest(models.Model):
    WAITING = 'waiting'
    APPROVED = 'approved'
    REJECTED = 'rejected'
    STATUS_CHOICES = [(WAITING, 'Waiting'),
                          (APPROVED, 'Approved'),
                          (REJECTED, 'Rejected'),
    ]
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    seeker = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='deal_requests')
    comment = models.TextField()
    date_approved = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=WAITING)

    def __str__(self):
        return f"Request №{self.id} on {self.car.title}"

    @classmethod
    def requests_count(cls):
        return cls.objects.count()

    @classmethod
    def approved_requests_count(cls):
        return cls.objects.filter(status=cls.APPROVED).count()

    @classmethod
    def waiting_requests_count(cls):
        return cls.objects.filter(status=cls.WAITING).count()

    @classmethod
    def rejected_requests_count(cls):
        return cls.objects.filter(status=cls.REJECTED).count()