from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from core import const


class BaseUserCreated(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated_at'), auto_now=True)
    ip = models.GenericIPAddressField(_('ip'))
    user_agent = models.CharField(_('user_agent'), max_length=1024, blank=True)

    class Meta:
        abstract = True


class OrderedTextObjectMixin(models.Model):
    text = models.CharField(_('text'), max_length=500)
    num = models.PositiveIntegerField(_('num'))

    class Meta:
        abstract = True


class Form(BaseUserCreated):
    title = models.CharField(_('form_title'), max_length=150, db_index=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    last_view = models.DateTimeField(_('form_last_view'), auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('form_verbose')
        verbose_name_plural = _('form_verbose_plural')


class Question(OrderedTextObjectMixin, BaseUserCreated):
    form = models.ForeignKey('core.Form', on_delete=models.CASCADE, verbose_name=_('form_verbose'))
    type = models.PositiveSmallIntegerField(_('question_type'), choices=const.QUESTION_TYPE_CHOICES)
    is_required = models.BooleanField(_('question_is_required'))
    is_multiple_allowed = models.BooleanField(_('question_is_multiple_allowed'))
    is_other_allowed = models.BooleanField(_('question_is_other_allowed'))

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = _('question_verbose')
        verbose_name_plural = _('question_verbose_plural')


class AnswerOption(OrderedTextObjectMixin, BaseUserCreated):
    question = models.ForeignKey('core.Question', on_delete=models.CASCADE, verbose_name=_('question_verbose'))

    class Meta:
        verbose_name = _('answer_option_verbose')
        verbose_name_plural = _('answer_option_verbose_plural')


class FormResponse(BaseUserCreated):
    form = models.ForeignKey('core.Form', on_delete=models.CASCADE, verbose_name=_('form_verbose'))

    class Meta:
        verbose_name = _('response_verbose')
        verbose_name_plural = _('response_verbose_plural')


class QuestionResponse(models.Model):
    form_response = models.ForeignKey('core.FormResponse', on_delete=models.CASCADE, verbose_name=_('response_verbose'))
    question = models.ForeignKey('core.Question', on_delete=models.CASCADE, verbose_name=_('question_verbose'))
    answer_options = models.ManyToManyField('core.AnswerOption', verbose_name=_('answer_option_verbose_plural'), blank=True)
    free_input_text = models.CharField(_('question_response_text'), max_length=10000, blank=True)

    class Meta:
        verbose_name = _('questions_response_verbose')
        verbose_name_plural = _('questions_response_verbose_plural')
