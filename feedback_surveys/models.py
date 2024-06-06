from django.db import models

# Create your models here.
class Feedback(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comments = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback from {self.user.username} with rating {self.rating}"


class Survey(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class SurveyQuestion(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    
    def __str__(self):
        return self.text


class SurveyResponse(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, related_name='responses', on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Response by {self.user.username} for {self.survey.title}"

class SurveyAnswer(models.Model):
    response = models.ForeignKey(SurveyResponse, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    answer_text = models.TextField()
    
    def __str__(self):
        return f"Answer to {self.question.text} by {self.response.user.username}"

