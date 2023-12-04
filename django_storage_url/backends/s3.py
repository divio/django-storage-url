import furl
from storages.backends import s3boto3


def boolean_str(s):
    return str(s).lower() in ["1", "true", "yes", "on"]


class S3Storage(s3boto3.S3Boto3Storage):
    def __init__(self, dsn):
        for needle in [
            ".s3-accesspoint-fips.dualstack.",
            ".s3-fips.dualstack.",
            ".s3-accesspoint.dualstack.",
            ".s3.dualstack.",
            ".s3-accesspoint.",
            ".s3-fips.",
            ".s3-",
            ".s3.",
        ]:
            bucket_name, marker, storage_host = dsn.host.partition(needle)
            if not marker:
                continue
            region_name = storage_host.split(".", 1)[0]
            if region_name == "amazonaws":
                region_name = None
            elif region_name in ["control", "control-fips"]:
                # Variants with account_id in the endpoint are unsupported
                continue
            storage_host = marker.lstrip(".") + storage_host
            break
        else:
            # Fall back to old static behavior
            endpoint = dsn.host.rsplit(".", 3)
            bucket_name = endpoint[0]
            storage_host = ".".join(endpoint[1:])
            region_name = (
                dsn.args.get("region_name", endpoint[1].partition("-")[2]) or None
            )

        location = str(dsn.path).lstrip("/")
        addressing_style = dsn.args.get("addressing_style")
        if not addressing_style:
            if "." in bucket_name:
                addressing_style = "path"
            else:
                addressing_style = "auto"

        if "url" in dsn.args:
            base_url = furl.furl(dsn.args.get("url"))
            url_protocol = "{}:".format(base_url.scheme)
            custom_domain = base_url.netloc
        else:
            url_protocol = "https:"
            custom_domain = dsn.args.get("domain")
            base_url = furl.furl()
            base_url.scheme = "https"
            base_url.host = custom_domain or dsn.host
            base_url.path = location.rstrip("/") + "/"

        super().__init__(
            access_key=dsn.username or "",
            secret_key=dsn.password or "",
            bucket_name=bucket_name,
            use_ssl=True,
            endpoint_url="https://{}/".format(storage_host),
            addressing_style=addressing_style,
            signature_version=dsn.args.get("auth", None),
            location=location,
            region_name=region_name,
            custom_domain=custom_domain,
            # TODO: Make the default `private` and explicitly set the ACL to
            #       `public-read` during provisioning
            object_parameters={"ACL": dsn.args.get("acl", "public-read")},
            # TODO: Support querystring_auth=True + custom_domain
            querystring_auth=boolean_str(dsn.args.get("qs_auth", "false")),
            url_protocol=url_protocol,
            # TODO: Enforce encryption everywhere. Check status on non-AWS
            #       providers.
            # encryption=True,
            max_memory_size=10 * 1024**2,  # Roll over to disk after 10 MB
        )

        self.base_url = str(base_url)
