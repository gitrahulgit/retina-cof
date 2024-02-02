import csv
from typing import Any
from django.db import transaction
from django.conf import settings
from retina.models import PatientImage, PatientInfo
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        # Path to your CSV file
        PatientInfo.objects.all().delete()
        PatientImage.objects.all().delete()

        # Read the CSV file and populate data
        with Path(settings.BASE_DIR, "image_ids_v2.csv").open("r") as csvfile:
            reader = csv.DictReader(csvfile)

            pinfo = {0: 0, 1: 0}
            pimage = {0: 0, 1: 0}
            with transaction.atomic():
                for row in reader:
                    if len(row) >= 2:
                        imagelink = row["link"]
                        patientid = row["Patient_ID_new"]
                        imagetype = row["Patient_Eye"]

                        pat, created = PatientInfo.objects.get_or_create(pat_id=patientid)
                        if created:
                            pinfo[1] += 1
                        else:
                            pinfo[0] += 1
                        PatientImage.objects.create(patient_id=pat, img_link=imagelink, img_type=imagetype)
                        pimage[1] += 1
        self.stdout.write(f"{pinfo=}, {pimage=}")
        self.stdout.write("Database updated successfully.")
