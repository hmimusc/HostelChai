import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

print(f'Path: {os.path.join(BASE_DIR, "text_files")}')
