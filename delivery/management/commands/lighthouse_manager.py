import os
import tempfile
import requests
import joblib
from django.conf import settings
from django.core.management.base import BaseCommand
from lighthouseweb3 import Lighthouse


class LighthouseManager:
    def __init__(self):
        self.lighthouse = Lighthouse(token=settings.LIGHT_HOUSE_API_KEY)

    def upload_model(self, model_path):
        """Upload model to Lighthouse IPFS and save CID in Django settings"""
        try:
            result = self.lighthouse.upload(source=model_path)

            if 'data' in result and 'Hash' in result['data']:
                model_cid = result['data']['Hash']
                settings.LIGHT_HOUSE_MODEL_CID = model_cid
                return model_cid

            raise Exception("Upload failed: No CID returned from Lighthouse")

        except Exception as e:
            raise Exception(f"Upload failed: {str(e)}")


    def download_model(self, cid=None):
        """Download model from Lighthouse IPFS using stored CID"""
        try:
            if not cid:
                cid = settings.LIGHT_HOUSE_MODEL_CID
                if not cid:
                    raise ValueError("No CID found in settings. Upload a model first or provide a CID.")

            url = f"https://gateway.lighthouse.storage/ipfs/{cid}"
            response = requests.get(url)

            if response.status_code == 200:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as temp_file:
                    temp_file.write(response.content)
                    model = joblib.load(temp_file.name)
                return model

            raise Exception(f"Download failed with status {response.status_code}")

        except Exception as e:
            raise Exception(f"Download error: {str(e)}")
