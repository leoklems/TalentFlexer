from django.db import models
import secrets
from ckeditor.fields import RichTextField


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    course_id = models.SlugField(default=0, max_length=10, null=True, blank=True)
    # pre_requisites = models.ForeignKey(CoursePreRequisite, on_delete=models.CASCADE,
    #                                    blank=True, null=True, related_name="pre_requisites")
    # benefits = models.ForeignKey(CourseBenefit, on_delete=models.CASCADE,
    #                              blank=True, null=True, related_name="benefits")
    course_type = models.CharField(max_length=50, blank=True, null=True)
    course_duration = models.CharField(max_length=200, blank=True, null=True)
    description = RichTextField()
    dp = models.ImageField(upload_to='courses/', default="media/course.png", null=True, blank=True)
    next_start_date = models.DateField(blank=True, null=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class CoursePreRequisite(models.Model):
    content = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="pre_requisites")

    def __str__(self):
        return f"{self.content}"


class CourseBenefit(models.Model):
    content = models.CharField(max_length=50, blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="benefits")

    def __str__(self):
        return f"{self.content}"


class Learner(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               blank=True, null=True, related_name="course")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    learner_id = models.SlugField(max_length=20, null=True, blank=True)
    phone_no = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    province_state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=20)
    zip_code = models.PositiveIntegerField()
    price = models.FloatField()
    vat = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Payment(models.Model):
    learner = models.OneToOneField(Learner, on_delete=models.CASCADE,
                                   related_name="learner", blank=True)
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self) -> str:
        return f"{self.learner}: {self.amount}"

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
