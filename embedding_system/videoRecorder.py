import os
import cv2, time
from embeddingSystem import RecorderBase, FileType
from pathlib import Path


class VideoRecorder(RecorderBase):
    @property
    def file_type(self) -> FileType:
        return FileType.VIDEO 
    
    def __init__(self, output_dir='./Video/upload'):
        super().__init__(output_dir)
        # 設定攝影機
        self.cap = cv2.VideoCapture(0)
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))   
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = 10
        self.fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    
    def start_interval_recording(self, recording_interval = 10):
        """開始錄影並每10秒保存到指定的目錄"""
        try:
            while True:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                output_path  = self.output_dir / f"record_{timestamp}.mp4"
                out = cv2.VideoWriter(output_path, self.fourcc, self.fps,  (self.width,  self.height))
                start_time = time.time()

                while (time.time() - start_time) < recording_interval:
                    ret, frame = self.cap.read()
                    if not ret:
                        print("未能從攝像頭獲取畫面")
                        break
                    out.write(frame)
                    cv2.imshow('Recording', frame)
                    if cv2.waitKey(1) == ord('q'):
                        return  

                # 完成本次錄製，釋放VideoWriter資源
                out.release()
                self.upload_video(output_path)

        except KeyboardInterrupt:
            print("錄製中斷")

        finally:
            # 釋放攝像頭和關閉所有窗口
            self.cap.release()
            out.release()
            cv2.destroyAllWindows()
             
        def test_capture(self):
            #測試鏡頭有沒有在運作
            cap = self.cap
            if not cap.isOpened():
                print('無法打開攝像頭')
                exit()
            while True:
                ret, frame = cap.read()
                if not ret:
                    print('無法讀取畫面')
                    break
                cv2.imshow('實時視頻', frame)
                if cv2.waitKey(1) == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()

# # 使用 VideoRecorder 類
# if __name__ == "__main__":
#     recorder = VideoRecorder()  
#     recorder.start_interval_recording()