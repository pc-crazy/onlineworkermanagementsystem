from django.http import JsonResponse
import requests
from django.contrib.auth import authenticate, login

from info.models import User as UserProfile


def SendSMS(request, user, pwd, num, message):
    usr = authenticate(username=user, password=pwd)
    if usr is not None:
        if usr.is_active:
            login(request, usr)
            if len(message) <= 160:
                u = UserProfile.objects.get(user=request.user)
                nums = num.split(',')
                nums_count = len(nums)
                if nums_count <= u.credit:
                    if nums_count <= 1000:
                        payload = {'msisdn': num, 'message': message, 'userID': 'zenvo',
                                   'passwd': '8ed89bfc684900b9b3f78df906268c55'}
                        u.credit = u.credit - nums_count
                        u.save()
                        r = requests.get('https://vas.banglalinkgsm.com/sendSMS/sendSMS', params=payload)
                        return JsonResponse(
                            {"user": user, "destination": num, "message": message, "length": len(message)})
                    else:
                        chunks = [nums[x:x + 1000] for x in xrange(0, len(nums), 1000)]
                        for x in chunks:
                            payload = {'msisdn': chunks, 'message': message, 'userID': 'zenvo',
                                       'passwd': '8ed89bfc684900b9b3f78df906268c55'}
                            u.credit = u.credit - nums_count
                            u.save()
                            r = requests.get('https://vas.banglalinkgsm.com/sendSMS/sendSMS', params=payload)
                        return JsonResponse(
                            {"user": user, "destination": num, "message": message, "length": len(message),
                             "chunk message": "True"})
                else:
                    return JsonResponse({"reply": "You don't have enough credit."})
            else:
                return JsonResponse({"reply": "Message length must be within 160 characters."})
        else:
            return JsonResponse({"reply": "Account is not active at the moment."})
    else:
        return JsonResponse({"reply": "Invalid login credentials."})