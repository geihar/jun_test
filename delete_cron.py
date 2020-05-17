from board.models import Upvotes


def delete_votes():
    Upvotes.objects.all().delete()


delete_votes()



