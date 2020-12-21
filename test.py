import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HostelChai.settings')
import django
django.setup()

from pathlib import Path
from my_modules import utilities

base_dir = Path(__file__).resolve().parent
media_files_dir = os.path.join(base_dir, 'media')
main_app_media_dir = os.path.join(media_files_dir, 'main_app')

print(f'{base_dir}')
print(f'{media_files_dir}')
print(f'{main_app_media_dir}')
print(f'{main_app_media_dir}\\H-1_HOS-2_electbill.png')

# path_to_save = utilities.process_path_to_save(main_app_media_dir)
#
# print(f'{path_to_save}')
# print(f'{utilities.process_path_to_use(path_to_save)}')

