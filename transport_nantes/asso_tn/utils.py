import datetime

from django.conf import settings
from django.utils.crypto import salted_hmac
from django.utils.crypto import secrets
from django.utils.http import base36_to_int, int_to_base36

from django.contrib.auth.models import User
#from authentication.models import Profile

def make_timed_token(user_id, minutes, persistent=0, test_value_now=None):
    """Make a URL-safe timed token that's valid for minutes minutes.

    This is meant for use with confirmation mails to avoid having to
    hold state on the server.

    The token is tied to a specific user to avoid frauds where a token
    is used to validate a different user than the one intended (i.e.,
    to validate a user whose email the person doesn't control or by
    simple fishing for user id).  We insert a random number (and our
    own secret key) to avoid replay attacks.

    The integer persistent is meant for setting session cookies, but
    these functions make no assumption other than that it is an
    integer.  The auth functions should assume that 0 means unchecked
    "remember me" and 1 means "remember me" and anything else is
    invalid.

    The test_value_now is for testing and should not normally be set.

    """

    # As this function should only be used for auth, once_token value must be set to True before
    # to make token used only once. If not set to True token may not be created

    user = User.objects.get(pk=user_id)

    user.profile.once_token = True
    user.save()

    if user.profile.once_token:

        secret = settings.SECRET_KEY
        rand_value = secrets.token_urlsafe(20)
        if test_value_now is not None:
            now = test_value_now
        else:
            now = datetime.datetime.now().timestamp()
        soon_seconds = int_to_base36(int(now + 60 * minutes))
        persistent_str = int_to_base36(int(persistent))
        hmac = salted_hmac(soon_seconds + persistent_str, rand_value + str(user_id)).hexdigest()[:20]
        return '{rnd}|{u}|{t}|{p}|{h}'.format(
            rnd=rand_value,
            u=user_id,
            t=soon_seconds,
            p=persistent_str,
            h=hmac)

def token_valid(timed_token, test_value_now=None):
    """Validate a timed token.

    Return the user id for which the token is valid, if the token is
    valid.  Return -1 if the token is not (either because it is
    malformed or because it has expired).

    If the token is valid, also return the persistent integer.  If the
    token is not valid, persistent will be zero.

    The test_value_now is for testing and should not normally be set.

    """
    the_rand_value, the_user_id, the_soon, the_persistent, the_hmac = \
        timed_token.split('|')
    computed_hmac = salted_hmac(the_soon + the_persistent,
                                the_rand_value + str(the_user_id)).hexdigest()[:20]
    if computed_hmac != the_hmac:
        return (-1, 0,)
    if test_value_now is not None:
        now = test_value_now
    else:
        now = datetime.datetime.now().timestamp()
    if now > base36_to_int(the_soon):
        return (-1, 0)

    user = User.objects.get(pk=the_user_id)
    if user.profile.once_token:
        user.profile.once_token = False
        user.save()
    else:
        return (-1, 0)
    return (int(the_user_id), base36_to_int(the_persistent),)
