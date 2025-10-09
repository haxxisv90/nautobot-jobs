"""Init for Nautobot Jobs"""
from nautobot.apps.jobs import register_jobs

from .populate_prefixes import PopulatePrefix


register_jobs(PopulatePrefix)
