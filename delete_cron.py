from board.models import Upvote


def delete_votes():
    Upvote.objects.all().delete()


delete_votes()
