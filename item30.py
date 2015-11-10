# Item 30: Consider @property Instead of Refactoring Attributes

# Suppose you have a class to implement a bucket quota that keeps track of how much quota remains:
from datetime import timedelta, datetime


class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.quota = 0

    def __repr__(self):
        return 'Bucket(quota=%d)' % self.quota

# A filled bucket's quota does not carry from one period to the next:
def fill(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        bucket.quota = 0
        bucket.reset_time = 0
    bucket.quota += amount

# Deduct ensures that the requested amount is available:
def deduct(bucket, amount):
    now = datetime.now()
    if now - bucket.reset_time > bucket.period_delta:
        return False
    if bucket.quota - amount < 0:
        return False
    bucket.quota -= amount
    return True

bucket = Bucket(60)
fill(bucket, 100)
print(bucket)

# Bucket(quota=100)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print(bucket)

# Had 99 quota
# Bucket(quota=1)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print(bucket)

# Not enough for 3 quota
# Bucket(quota=1)

# The problem with this bucket implementation is that it does not tell which level it started with and how much
# was consumed. We can fix this by adding two attributes and using @property:
class Bucket(object):
    def __init__(self, period):
        self.period_delta = timedelta(seconds=period)
        self.reset_time = datetime.now()
        self.max_quota = 0
        self.quota_consumed = 0

    def __repr__(self):
        return('Bucket(max_quota=%d, quota_consumed=%d' %
               (self.max_quota, self.quota_consumed))

    @property
    def quota(self):
        return self.max_quota - self.quota_consumed

    @quota.setter
    def quota(self, amount):
        delta = self.max_quota - amount
        if amount == 0:
            # Quota being reset for a new period
            self.quota_consumed = 0
            self.max_quota = 0
        elif delta < 0:
            # Quota being filled for the new period
            assert self.quota_consumed == 0
            self.max_quota = amount
        else:
            # Quota being consumed during the period
            assert self.max_quota  >= self.quota_consumed
            self.quota_consumed += delta

bucket = Bucket(60)
print('Initial', bucket)
fill(bucket, 100)
print('Filled', bucket)

if deduct(bucket, 99):
    print('Had 99 quota')
else:
    print('Not enough for 99 quota')
print('Now', bucket)

if deduct(bucket, 3):
    print('Had 3 quota')
else:
    print('Not enough for 3 quota')
print('Still', bucket)

# Initial Bucket(max_quota=0, quota_consumed=0
# Filled Bucket(max_quota=100, quota_consumed=0
# Had 99 quota
# Now Bucket(max_quota=100, quota_consumed=99
# Not enough for 3 quota
# Still Bucket(max_quota=100, quota_consumed=99

# We did not have to change the Bucket-using code, because the changes were transparent to the user.
# Ideally, fill and deduct should have been instance methods (see item #22). @property helps in incrementally
# improving your data model, but if it is used too heavily, it may be an indicator for refactoring classes.



