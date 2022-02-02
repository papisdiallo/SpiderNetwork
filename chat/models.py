from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Q, F
User = get_user_model()

# create a single room between 2 connected users


class singleOneToOneRoom(models.Model):
    first_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="first_user")
    second_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="second_user")

    room_name = models.CharField(max_length=200, blank=True, null=True)
    # class Meta:
    #     unique_together = ["first_user", "second_user"]
    #     constraints = [
    #         models.CheckConstraint(check=Q(first_user__id__lt=F(
    #             'second_user__id')), name='unique_user_pair'),
    #     ]


class messages(models.Model):
    room = models.ForeignKey(
        singleOneToOneRoom, on_delete=models.CASCADE, related_name="messages")
    message_body = models.TextField()
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="msg_sender")
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="msg_receiver")
    date_sent = models.DateTimeField(auto_now_add=True)
    # class Meta:
    #     constraints = [
    #         models.CheckConstraint(
    #             check=Q(sender=F('room__first_user')) & Q(
    #                 receiver=F('room__second_user'))
    #             | Q(sender=F('room__second_user')) & Q(receiver=F('room__first_user')),
    #             name='valid_sender_and_receiver'
    #         ),
    #     ]

    def __str__(self):
        return f'{self.sender}_to_{self.receiver}'
