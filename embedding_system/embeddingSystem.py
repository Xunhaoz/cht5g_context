import os, requests
from abc import ABC, abstractmethod
from dotenv import load_dotenv
from enum import Enum
from pathlib import Path


load_dotenv()

class FileType(Enum):
    VIDEO = 'video'
    VOICE = 'voice'
    
class RecorderBase(ABC):
    API_URL = os.getenv("API_URL")
    VIDEO_URL = f"{API_URL}/video"
    VOICE_URL = f"{API_URL}/voice"
    
    def __init__(self, output_dir):
        self.output_dir = Path(output_dir).expanduser()  
        if not self.output_dir.exists():  
            self.output_dir.mkdir(parents=True) 
    
    @property
    @abstractmethod
    def file_type(self):
        pass
    
    def upload_file(self, file_path):
        if self.file_type == FileType.VIDEO:
            url = self.VIDEO_URL
        elif self.file_type == FileType.VOICE:
            url = self.VOICE_URL
        else:
            print("不支援的文件類型:", self.file_type)
            return
        try:
            with open(file_path, 'rb') as f:
                files = {self.file_type.value: f}
                response = requests.post(url, files=files)
                if response.status_code == 200:
                    print(f"{'影片' if self.file_type == 'video' else '音檔'}上傳成功:", response.json())
                else:
                    print("上傳失敗，狀態碼:", response.status_code)
        except Exception as e:
            print(f"上傳過程中出錯: {e}")
            