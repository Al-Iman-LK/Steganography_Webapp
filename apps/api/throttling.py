from rest_framework.throttling import UserRateThrottle

class SteganoFileRateThrottle(UserRateThrottle):
    rate = '10/minute'

class ProfileRateThrottle(UserRateThrottle):
    rate = '30/minute'
