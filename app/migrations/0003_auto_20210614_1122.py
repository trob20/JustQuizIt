# Generated by Django 2.2 on 2021-06-14 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_answerselected_quizhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerselected',
            name='answer_selected',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_answers', to='app.QuizHistory'),
        ),
    ]
