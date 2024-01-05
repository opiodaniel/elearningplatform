# from agora_restful_api import RtcTokenBuilder, RtcRole
# from .agora_key.RtcTokenBuilder import RtcTokenBuilder, Role_Attendee
# from django.conf import settings
#
#
# class AgoraService:
#     @staticmethod
#     def generate_agora_token(channel_name, user_id, role=RtcRole.PUBLISHER, expiration_time_in_seconds=3600):
#         key = settings.AGORA['APP_ID']
#         secret = settings.AGORA['APP_SECRET']  # Make sure to add your Agora App Secret to settings.py
#
#         expiration_time = int(expiration_time_in_seconds)
#
#         token = RtcTokenBuilder.build_token_with_uid(
#             key,
#             secret,
#             channel_name,
#             user_id,
#             role,
#             expiration_time
#         )
#
#         return token
