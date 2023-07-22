from rest_framework.throttling import UserRateThrottle


class TenCallsPerMin(UserRateThrottle):
    scope = 'ten'