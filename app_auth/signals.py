import logging

from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.mail import send_mail

from app_blogs.models import Post, Comment, Category, Tags

User = get_user_model()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@receiver(user_logged_in, sender=User)
def user_logged_in(sender, request, user, **kwargs):
    logger.info(f"User {user} logged in")

@receiver(user_logged_out, sender=User)
def user_logged_out(sender, request, user, **kwargs):
    logger.info(f"User {user} logged out")

@receiver(post_save, sender=User)
def profile_post_save(sender, instance: User, created, **kwargs):
    
    if created:
        logger.info(f"User {instance.username} registered")
        group = Group.objects.get(name="User")
        group.user_set.add(instance)

        send_mail(
            subject='Hi!',
            message='Welcome to the board',
            from_email='admin@localhost',
            recipient_list=[instance.username],
        )
    else:
        logger.info(f"User {instance.username} updated")

@receiver(post_save, sender=Post)
def blogs_post_save(sender, instance, created, **kwargs):
    if created:
        # logger.info(f"User: {user} create post {instance}")
        logger.info(f"Post {instance.title} created by {instance.author}")
    else:
        logger.info(f"Post {instance.title} updated by {instance.author}")

# TODO: Добавить сигналы на другие действия