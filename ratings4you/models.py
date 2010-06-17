from django.db import models

# Create your models here.

# 
class RatingThemesDirectory(models.Model):
    """
    Справочник тем для голосований.
    """
    pass

class RegionDirectory(models.Model):
    """
    Справочник регионов - здесь могут быть как страны, города, области, так и всё что угодно.
    """
    pass

class  Rating(models.Model):
    """
    Сам рейтинг, содержащий пункты для голосования.
    """
    pass

class RatingItem(models.Model):
    """
    Пункт рейтинга в @see: Rating .
    """
    pass

class Vote(models.Model):
    """
    Голос, отданный за тот или иной пункт рейтинга.
    """
    pass