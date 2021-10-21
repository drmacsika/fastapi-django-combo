import math
# from spamfighter.models import BlockedIps
import os
import random
import re
import string
import unicodedata

from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = "5242880"


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    size = random.randint(30, 45)
    key_id = random_string_generator(size=size)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(key=key_id).exists()
    if qs_exists:
        return unique_slug_generator(instance)
    return key_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def get_ip_address(request):
    ip = request.META.get('HTTP_X_FORWARDED_FOR')  # more reliable
    if ip:
        ip = ip.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')  # less reliable
    return ip


# def check_ip_address(ip):
#     return BlockedIps.objects.filter(ip_address=ip).exists()


def validate_doc_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.doc', '.docx']
    if not ext in valid_extensions:
        raise ValidationError(
            _('File not supported!'),
            code='invalid',
            params={'value': value},
        )
    else:
        return value


def validate_doc_image_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg',
                        '.png', '.xlsx', '.xls', '.txt', '.zip', '.rar']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            _('Unsupported file extension.'),
            code='invalid',
            params={'value': value},
        )
    else:
        return value


# Size less than # 5MB - 5242880
def validate_file_size(value):
    filesize = value.size
    if filesize < 0 or filesize > 5242880:
        raise ValidationError(
            _("The file size is unacceptable! Enter size less than 5MB."),
            code='invalid',
            params={'value': value},
        )
    else:
        return value


def validate_fullname(self):
    fullname = self.split()
    if len(fullname) <= 1:
        raise ValidationError(
            _('Kindly enter more than one name, please.'),
            code='invalid',
            params={'value': self},
        )
    for x in fullname:
        if x.isalpha() is False or len(x) < 2:
            raise ValidationError(
                _('Please enter your name correctly.'),
                code='invalid',
                params={'value': self},
            )


def get_first_name(self):
    if isinstance(self, bool):
        pass
    else:
        names = self.split()
        return names[0]


def get_last_name(self):
    if isinstance(self, bool):
        pass
    else:
        names = self.split()
        return names[-1]


def generate_username(self, full_name, Model):
    name = full_name.lower()
    name = name.split(' ')
    lastname = name[-1]
    firstname = name[0]
    self.username = '%s%s' % (firstname[0], lastname)
    if Model.objects.filter(username=self.username).count() > 0:
        username = '%s%s' % (firstname, lastname[0])
        if Model.objects.filter(username=self.username).count() > 0:
            users = Model.objects.filter(username__regex=r'^%s[1-9]{1,}$' % firstname).order_by(
                'username').values(
                'username')
            if len(users) > 0:
                last_number_used = sorted(
                    map(lambda x: int(x['username'].replace(firstname, '')), users))
                last_number_used = last_number_used[-1]
                number = last_number_used + 1
                self.username = '%s%s' % (firstname, number)
            else:
                self.username = '%s%s' % (firstname, 1)
    return self.username



def random_string(size: int, chars: str = string.ascii_lowercase+string.digits) -> str:
    """
    Generate random strings from a given size
    """
    return "".join(random.choices(chars, k = size))


def slugify(value, allow_unicode=False):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def unique_slug_generator(value, new_slug=False):
    """
    This generates a unique slug using your model slug value
    assuming there's a model with a slug field and 
    a title character (char) field.
    If a slug exists, it generates a unique slug with the old and random
    otherwise, it generates a new slug
    """
    if new_slug:
        return f"{slugify(value)}-{random_string(4)}"
    return slugify(value)


def count_words(content):
    """Count all the words received from a parameter."""
    matching_words = re.findall(r'\w+', content)
    count = len(matching_words)
    return count


def get_read_time(content):
    """Get the read length by dividing with an average of 200wpm """
    count = count_words(content)
    read_length_min = math.ceil(count/200.0)
    return int(read_length_min)
