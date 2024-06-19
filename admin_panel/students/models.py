import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Student(UUIDMixin):
    name = models.CharField(_('name'), max_length=255, null=False, blank=False)
    class_name = models.CharField(_('class_name'), max_length=5, null=False, blank=False)
    age = models.IntegerField(_('age'), null=False)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'students'
        verbose_name = _('student')
        verbose_name_plural = _('students')
        ordering = ['-name']
        indexes = [
            models.Index(
                fields=['name'],
                name='students_name_idx',
            ),
        ]


class StudentsMarks(UUIDMixin):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        verbose_name=_('student'),
        related_name='marks'
    )
    subject = models.TextField(_('subject'), null=False, blank=False)
    mark = models.IntegerField(_('mark'), null=False, default=5)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)

    def __str__(self):
        return f'{self.student.name=} {self.subject=} {self.mark=}'

    class Meta:
        db_table = 'students_marks'
        verbose_name = _('students_mark')
        verbose_name_plural = _('students_marks')
        ordering = ['-created_at']
        indexes = [
            models.Index(
                fields=['student_id'],
                name='students_marks_student_id_idx',
            ),
        ]
