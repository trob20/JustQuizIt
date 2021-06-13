# Generated by Django 2.2 on 2021-06-13 00:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuizHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=12)),
                ('start_date', models.DateTimeField()),
                ('completed_date', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('quiz_taken', models.ManyToManyField(related_name='assigned_quizzes', to='app.Quiz')),
                ('quiz_taken_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_history', to='app.User')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerSelected',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.BooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer_selected', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.AnswerOption')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.Question')),
            ],
        ),
    ]