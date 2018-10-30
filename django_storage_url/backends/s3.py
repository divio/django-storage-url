import six
import furl
from storages.backends import s3boto3


class S3Storage(s3boto3.S3Boto3Storage):
    addressing_styles = {"subdomain": "virtual", "ordinary": "path"}

    def __init__(self, dsn):
        bucket_name, host = dsn.host.split(".", 1)
        addressing_style = dsn.args.get("calling_format")
        if addressing_style:
            addressing_style = self.addressing_styles[addressing_style]
        else:
            addressing_style = "virtual"

        super(S3Storage, self).__init__(
            access_key=dsn.username,
            secret_key=dsn.password,
            bucket_name=bucket_name,
            endpoint_url="https://{}/".format(host),
            addressing_style=addressing_style,
            location=six.text_type(dsn.path).lstrip("/"),
            custom_domain=furl.furl(dsn.args.get("url")).netloc,
            default_acl=dsn.args.get("acl", "private"),
            querystring_auth=False,
        )
