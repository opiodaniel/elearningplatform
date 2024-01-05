import os
import time
import json

from django.http.response import JsonResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render

from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
from pusher import Pusher


# Instantiate a Pusher Client
pusher_client = Pusher(app_id=settings.PUSHER['PUSHER_APP_ID'],
                       key=settings.PUSHER['PUSHER_KEY'],
                       secret=settings.PUSHER['PUSHER_SECRET'],
                       ssl=True,
                       cluster=settings.PUSHER['PUSHER_CLUSTER']
                       )


@login_required(login_url='/admin/')
def index(request):
    User = get_user_model()
    all_users = User.objects.exclude(id=request.user.id).only('id', 'username')
    return render(request, 'videocall/index.html', {'allUsers': all_users})


def pusher_auth(request):
    payload = pusher_client.authenticate(
        channel=request.POST['channel_name'],
        socket_id=request.POST['socket_id'],
        custom_data={
            'user_id': request.user.id,
            'user_info': {
                'id': request.user.id,
                'name': request.user.username
            }
        })
    return JsonResponse(payload)


def generate_agora_token(request):
    appID = settings.AGORA['AGORA_APP_ID']
    appCertificate = settings.AGORA['AGORA_APP_CERTIFICATE']
    channelName = json.loads(request.body.decode(
        'utf-8'))['channelName']
    userAccount = request.user.username
    expireTimeInSeconds = 3600
    currentTimestamp = int(time.time())
    privilegeExpiredTs = currentTimestamp + expireTimeInSeconds

    token = RtcTokenBuilder.buildTokenWithAccount(
        appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)

    return JsonResponse({'token': token, 'appID': appID})


def call_user(request):
    body = json.loads(request.body.decode('utf-8'))

    user_to_call = body['user_to_call']
    channel_name = body['channel_name']
    caller = request.user.id

    pusher_client.trigger(
        'presence-online-channel',
        'make-agora-call',
        {
            'userToCall': user_to_call,
            'channelName': channel_name,
            'from': caller
        }
    )
    return JsonResponse({'message': 'call has been placed'})


# import os
# import time
# import json
#
# from django.http.response import JsonResponse
# from django.contrib.auth import get_user_model
# from django.contrib.auth.decorators import login_required
#
# from django.shortcuts import render
#
# from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
# from pusher import Pusher

# Instantiate a Pusher Client
# pusher_client = Pusher(app_id=os.environ.get('PUSHER_APP_ID'),
#                        key=os.environ.get('PUSHER_KEY'),
#                        secret=os.environ.get('PUSHER_SECRET'),
#                        ssl=True,
#                        cluster=os.environ.get('PUSHER_CLUSTER')
#                        )
#
# pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
#
#
# @login_required(login_url='/admin/')
# def index(request):
#     User = get_user_model()
#     all_users = User.objects.exclude(id=request.user.id).only('id', 'username')
#     return render(request, 'videocall/index.html', {'allUsers': all_users})
#
#
# def pusher_auth(request):
#     payload = pusher_client.authenticate(
#         channel=request.POST['channel_name'],
#         socket_id=request.POST['socket_id'],
#         custom_data={
#             'user_id': request.user.id,
#             'user_info': {
#                 'id': request.user.id,
#                 'name': request.user.username
#             }
#         })
#     return JsonResponse(payload)
#
#
# def generate_agora_token(request):
#     appID = os.environ.get('AGORA_APP_ID')
#     appCertificate = os.environ.get('AGORA_APP_CERTIFICATE')
#     channelName = json.loads(request.body.decode(
#         'utf-8'))['channelName']
#     userAccount = request.user.username
#     expireTimeInSeconds = 3600
#     currentTimestamp = int(time.time())
#     privilegeExpiredTs = currentTimestamp + expireTimeInSeconds
#
#     token = RtcTokenBuilder.buildTokenWithAccount(
#         appID, appCertificate, channelName, userAccount, Role_Attendee, privilegeExpiredTs)
#
#     return JsonResponse({'token': token, 'appID': appID})
#
#
# def call_user(request):
#     body = json.loads(request.body.decode('utf-8'))
#
#     user_to_call = body['user_to_call']
#     channel_name = body['channel_name']
#     caller = request.user.id
#
#     pusher_client.trigger(
#         'presence-online-channel',
#         'make-agora-call',
#         {
#             'userToCall': user_to_call,
#             'channelName': channel_name,
#             'from': caller
#         }
#     )
#     return JsonResponse({'message': 'call has been placed'})


# from django.shortcuts import render
# from .agora_service import AgoraService
# from django.conf import settings
#
#
# def video_call(request, room_name):
#     user_id = request.user.id  # Assuming you have user authentication
#
#     # Generate Agora token
#     channel_name = f'room_{room_name}'
#     agora_token = AgoraService.generate_agora_token(channel_name, user_id)
#
#     return render(request, 'video_call.html', {
#         'agora_app_id': settings.AGORA['APP_ID'],
#         'channel_name': channel_name,
#         'user_id': user_id,
#         'agora_token': agora_token,
#})