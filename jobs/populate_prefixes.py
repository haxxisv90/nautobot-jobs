from nautobot.apps.jobs import Job, register_jobs
from nautobot.ipam.models import Prefix, Namespace
from nautobot.extras.models import Status


class PopulatePrefix(Job):
    """Job to populate synthetic IPv4 Prefixes for testing in Nautobot"""

    class Meta:
        name = "Populate IPv4 Prefixes"
        description = "Populate synthetic IPv4 prefixes for testing"
        has_sensitive_variables = False

    def run(self):
        """Execute Job to create Prefixes"""

        prefixes_to_add = ["172.16.0.0/20", "172.17.0.0/20", "172.18.0.0/20"]

        namespace, created = Namespace.objects.get_or_create(
            name="Engineering",
            defaults={
                "description": "Campus devices for engineering staff"
            }
        )

        if created:
            self.logger.info(f"Created namespace: {namespace.name}")

        active_status = Status.objects.get(name="Active")

        for new_prefix in prefixes_to_add:
            prefix, created = Prefix.objects.get_or_create(
                prefix=new_prefix,
                namespace=namespace,
                status=active_status,
                defaults={
                    "description": "Added via populate prefix job"
                }
            )

            if created:
                self.logger.info(f"Created prefix: {prefix.prefix}")
            else:
                self.logger.warning(f"Prefix already exists: {prefix.prefix}")

        self.logger.info("Prefix population completed!")


register_jobs(PopulatePrefix)