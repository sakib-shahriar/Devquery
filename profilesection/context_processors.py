from profilesection.models import UserInfo, Interest
from newsfeed.models import Notification
from django.db.models import Count


def add_variable_to_context(request):
    if request.user.is_authenticated:
        try:
            user_profile_pic = UserInfo.objects.get(user=request.user)
            notf_num = Notification.objects.filter(owner=request.user, is_read=False).aggregate(num=Count('id'))['num']
            if notf_num > 9:
                notf_num = '9+'
        except UserInfo.DoesNotExist:
            return {'': ''}
        if user_profile_pic:
            user_profile_pic = user_profile_pic.image
        return {
            'user_profile_pic': user_profile_pic,
            'notf_num': notf_num
        }
    return {'': ''}
