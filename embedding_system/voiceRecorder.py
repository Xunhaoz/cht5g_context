import os
import subprocess
import time
from embeddingSystem import RecorderBase, FileType
from pathlib import Path

class VoiceRecorder(RecorderBase):
    
    @property
    def file_type(self) -> FileType:
        return FileType.VOICE
    
    def __init__(self, device='plughw:3', channels=4, rate=48000, format='S16_LE', output_dir='~/Voice/upload'):
        super().__init__(output_dir)
        self.device = device
        self.channels = channels
        self.rate = rate
        self.format = format
        self.recording_process = None

    def start_recording(self, output_path):
        """
        開始錄音
        :param file_name: 保存錄音的文件名稱
        """            

        print(f"錄音開始，保存至: {output_path}")
        command = [
            'arecord',
            '-D', self.device,
            '-c', str(self.channels),
            '-r', str(self.rate),
            '-f', self.format,
            output_path
        ]

        # 啟動錄音進程
        self.recording_process = subprocess.Popen(command)
    def stop_recording(self, output_path):
        """
        停止錄音
        """
        if self.recording_process:
            print("錄音結束")
            self.recording_process.terminate()
            self.recording_process.wait()
            self.recording_process = None

    def start_recording_session(self):
        """
        控制錄音會話，按下 's' 開始錄音，按 'e' 結束錄音
        """
        try:
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            file_name = f"record_{timestamp}.wav"
            output_path = self.output_dir / file_name

            while True:
                user_input = input("輸入 's' 開始錄音，'e' 結束錄音，或 'q' 退出: ")
                if user_input == 's':
                    self.start_recording(output_path)
                elif user_input == 'e':
                    self.stop_recording(output_path)
                    self.upload_file(output_path, timestamp)
                    print('傳送完成')
                elif user_input == 'q':
                    print("結束錄音會話")
                    break

        except Exception as e:
            print(f"錄音過程中出錯: {e}")
        finally:
            # 確保無論發生什麼情況，錄音設備都被正確釋放
            if self.recording_process:
                print("強制停止錄音...")
                self.stop_recording()
            #Connector.upload_voice(output_path)
            print("錄音資源已釋放")

if __name__ == "__main__":
    recorder = VoiceRecorder()
    recorder.set_place("中壢")
    recorder.start_recording_session()