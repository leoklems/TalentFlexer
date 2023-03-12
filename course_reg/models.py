from django.db import models
import secrets
from .paystack import PayStack

# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    pre_requisites = models.CharField(max_length=300, blank=True, null=True)
    course_type = models.CharField(max_length=50, blank=True, null=True)
    course_duration = models.CharField(max_length=200, blank=True, null=True)
    next_start_date = models.DateField(blank=True, null=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Learner(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                                 blank=True, null=True, related_name="course")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    learner_id = models.SlugField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True)
    address = models.TextField(max_length=500)
    province_state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20)
    zip_code = models.PositiveIntegerField(max_length=10)
    price = models.FloatField()
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

#
# class OrderModel(models.Model):
#     code = models.CharField(max_length=50, null=True)
#     course = models.ManyToManyField(Course)
#     price = models.JSONField(null=True)
#     amount = models.FloatField()
#     created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
#     has_paid = models.BooleanField()
#     status = models.CharField(max_length=20)

#
# class CheckOutModel(models.Model):
#     learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
#     full_name = models.CharField(max_length=150)
#     address = models.TextField()
#     mobile = models.CharField(max_length=20)
#     email = models.EmailField(null=True)
#     payment_method = models.CharField(max_length=20)
#     grand_total = models.FloatField()
#     created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
#     ref = models.CharField(max_length=200)
#     verified = models.BooleanField(default=False)


class Payment(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self)-> str:
        return f"Payment: {self.amount}"

    def save(self, *args, **kwargs) -> None:
        '''
        Whenever a save event is to happen, we need to generate a reference
        :param args:
        :param kwargs:
        :return:
        '''
        while not self.ref: # To check if the current object has no reference
            ref = secrets.token_urlsafe(50) # a safe url token
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref

        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)

        if status:
            if result['amount']/100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False
