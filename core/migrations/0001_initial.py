from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswerOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('ip', models.GenericIPAddressField(verbose_name='ip')),
                ('user_agent', models.CharField(blank=True, max_length=1024, verbose_name='user_agent')),
                ('text', models.CharField(max_length=500, verbose_name='text')),
                ('num', models.PositiveIntegerField(verbose_name='num')),
            ],
            options={
                'verbose_name': 'answer_option_verbose',
                'verbose_name_plural': 'answer_option_verbose_plural',
            },
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('ip', models.GenericIPAddressField(verbose_name='ip')),
                ('user_agent', models.CharField(blank=True, max_length=1024, verbose_name='user_agent')),
                ('title', models.CharField(db_index=True, max_length=150, verbose_name='form_title')),
                ('last_view', models.DateTimeField(auto_now_add=True, verbose_name='form_last_view')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'form_verbose',
                'verbose_name_plural': 'form_verbose_plural',
            },
        ),
        migrations.CreateModel(
            name='FormResponse',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('ip', models.GenericIPAddressField(verbose_name='ip')),
                ('user_agent', models.CharField(blank=True, max_length=1024, verbose_name='user_agent')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.form', verbose_name='form_verbose')),
            ],
            options={
                'verbose_name': 'response_verbose',
                'verbose_name_plural': 'response_verbose_plural',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('ip', models.GenericIPAddressField(verbose_name='ip')),
                ('user_agent', models.CharField(blank=True, max_length=1024, verbose_name='user_agent')),
                ('text', models.CharField(max_length=500, verbose_name='text')),
                ('num', models.PositiveIntegerField(verbose_name='num')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'question_free_input_type'), (2, 'question_choice_type')], verbose_name='question_type')),
                ('is_required', models.BooleanField(verbose_name='question_is_required')),
                ('is_multiple_allowed', models.BooleanField(verbose_name='question_is_multiple_allowed')),
                ('is_other_allowed', models.BooleanField(verbose_name='question_is_other_allowed')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.form', verbose_name='form_verbose')),
            ],
            options={
                'verbose_name': 'question_verbose',
                'verbose_name_plural': 'question_verbose_plural',
            },
        ),
        migrations.CreateModel(
            name='QuestionResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('free_input_text', models.CharField(blank=True, max_length=10000, verbose_name='question_response_text')),
                ('answer_options', models.ManyToManyField(blank=True, to='core.answeroption', verbose_name='answer_option_verbose_plural')),
                ('form_response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.formresponse', verbose_name='response_verbose')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question', verbose_name='question_verbose')),
            ],
            options={
                'verbose_name': 'questions_response_verbose',
                'verbose_name_plural': 'questions_response_verbose_plural',
            },
        ),
        migrations.AddField(
            model_name='answeroption',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.question', verbose_name='question_verbose'),
        ),
    ]
