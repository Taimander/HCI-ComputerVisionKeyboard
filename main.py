import cv2
from hand_recognition import HandRecognition
from voice_recognition import VoiceRecognition
from threading import Thread
from python_event_bus import EventBus

# Open a video capture object (0 for the default camera)
cap = cv2.VideoCapture(0)

hand_req = HandRecognition()
voice_req = VoiceRecognition()

voice_req_thread = Thread(target=voice_req.voice_req_loop, daemon=True)
voice_req_thread.start()

last_pos = None

@EventBus.on('click')
def on_click():
    global last_pos
    if last_pos:
        print(f'Click en la posicion {last_pos}')

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        continue
    
    landmark = hand_req.process_hand(frame)
    if landmark:
        last_pos = landmark
        x, y = landmark
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    
    # Display the frame with hand landmarks
    cv2.imshow('Hand Recognition', frame)
    
    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()