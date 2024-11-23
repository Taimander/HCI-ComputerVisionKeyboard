import cv2
from hand_recognition import HandRecognition
from voice_recognition import VoiceRecognition
from threading import Thread
from python_event_bus import EventBus
import buttons

keyboard_img = cv2.imread('kbd.png', cv2.IMREAD_UNCHANGED)

# Split overlay into BGR and Alpha channels
overlay_bgr = keyboard_img[:, :, :3]
overlay_alpha = keyboard_img[:, :, 3] / 255.0  # Normalize alpha to 0-1


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
        # print(f'Click en la posicion {last_pos}')
        x, y = last_pos
        key = buttons.get_button(x, y)
        if key:
            print(f'Click en la tecla {key}')

while cap.isOpened():
    ret, frame = cap.read()
    
    if not ret:
        continue

    # If frame is not 640x480, resize it
    if frame.shape[0] != 480 or frame.shape[1] != 640:
        frame = cv2.resize(frame, (640, 480))
    
    # Flip frame
    frame = cv2.flip(frame, 1)
    
    landmark = hand_req.process_hand(frame)
    if landmark:
        last_pos = landmark
        x, y = landmark
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    
    # Display the keyboard image

    # Blend the overlay with the webcam frame
    for c in range(3):  # Apply alpha blending to each channel
        frame[:, :, c] = (
            overlay_alpha * overlay_bgr[:, :, c] +
            (1 - overlay_alpha) * frame[:, :, c]
        )
    
    # Display the frame with hand landmarks
    cv2.imshow('Hand Recognition', frame)
    
    # Exit when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close the OpenCV windows
cap.release()
cv2.destroyAllWindows()