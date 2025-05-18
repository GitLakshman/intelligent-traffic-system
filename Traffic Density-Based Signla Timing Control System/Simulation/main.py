import cv2
import time
import torch
import numpy as np
import RPi.GPIO as GPIO

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
model.conf = 0.25  # Confidence threshold

# GPIO Pin Setup (Commented for testing)
# GREEN_PIN_A = 17
# YELLOW_PIN_A = 27
# RED_PIN_A = 22
# GREEN_PIN_B = 23
# YELLOW_PIN_B = 24
# RED_PIN_B = 25

# GPIO.setmode(GPIO.BCM)
# GPIO.setup([GREEN_PIN_A, YELLOW_PIN_A, RED_PIN_A, GREEN_PIN_B, YELLOW_PIN_B, RED_PIN_B], GPIO.OUT)

# Initialize USB Webcams (Direction B and C)
cap_b = cv2.VideoCapture(0)  # External webcam 1 (USB)
cap_c = cv2.VideoCapture(1)  # External webcam 2 (USB)

cap_b.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap_b.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap_c.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap_c.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

FRAME_WIDTH = 640
FRAME_HEIGHT = 480

ALLOWED_CLASS_IDS = [0, 2, 3, 5, 7]

def draw_signal_on_frame(frame, signal_status):
    color_map = {
        "GREEN": (0, 255, 0),
        "YELLOW": (0, 255, 255),
        "RED": (0, 0, 255)
    }
    overlay = frame.copy()
    overlay.setflags(write=1)
    color = color_map.get(signal_status, (255, 255, 255))
    cv2.putText(overlay, f"Signal: {signal_status}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, color, 3)
    return overlay

# Commenting out the GPIO signal control for testing
def set_gpio_signal(direction, signal):
    # pins = {
    #     'A': {'RED': RED_PIN_A, 'YELLOW': YELLOW_PIN_A, 'GREEN': GREEN_PIN_A},
    #     'B': {'RED': RED_PIN_B, 'YELLOW': YELLOW_PIN_B, 'GREEN': GREEN_PIN_B}
    # }
    # for pin in pins[direction].values():
    #     GPIO.output(pin, GPIO.LOW)
    # if signal in pins[direction]:
    #     GPIO.output(pins[direction][signal], GPIO.HIGH)
    #     print(f"Direction {direction}: {signal} light ON")
    pass

def process_frame(frame):
    results = model(frame)
    total_area = 0
    frame_area = FRAME_WIDTH * FRAME_HEIGHT

    for *box, conf, cls in results.xyxy[0]:
        label = int(cls)
        if label in ALLOWED_CLASS_IDS:
            x1, y1, x2, y2 = map(int, box)
            area = (x2 - x1) * (y2 - y1)
            total_area += area

    density_percentage = (total_area / frame_area) * 100
    return density_percentage, results

def calculate_dynamic_green_time(density):
    base_time = 10  # seconds
    max_time = 25  # seconds
    return min(max_time, int(base_time + (density / 2)))

def show_signal_with_overlay(results, signal, duration, window_name, direction):
    set_gpio_signal(direction, signal)  # GPIO is commented out
    results.render()
    img = np.asarray(results.ims[0])
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    overlay = draw_signal_on_frame(img, signal)
    start_time = time.time()
    while time.time() - start_time < duration:
        cv2.imshow(window_name, overlay)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit()

def main():
    try:
        while True:
            ret_b, frame_b = cap_b.read()     # USB webcam 1 (Direction B)
            ret_c, frame_c = cap_c.read()     # USB webcam 2 (Direction C)

            if not ret_b or not ret_c:
                print("Failed to read from one of the webcams.")
                break

            # Resize frames to match expected dimensions
            frame_b_resized = cv2.resize(frame_b, (FRAME_WIDTH, FRAME_HEIGHT))
            frame_c_resized = cv2.resize(frame_c, (FRAME_WIDTH, FRAME_HEIGHT))

            # Process the frames to get traffic density
            density_b, results_b = process_frame(frame_b_resized)
            density_c, results_c = process_frame(frame_c_resized)

            print(f"Density B: {density_b:.2f}%, Density C: {density_c:.2f}%")

            # Calculate dynamic green time for each direction based on traffic density
            green_time_b = calculate_dynamic_green_time(density_b)
            green_time_c = calculate_dynamic_green_time(density_c)

            # Decision logic to control traffic signals
            if density_b >= density_c:
                show_signal_with_overlay(results_c, "RED", 5, "Direction C", 'C')
                show_signal_with_overlay(results_b, "YELLOW", 5, "Direction B", 'B')
                show_signal_with_overlay(results_b, "GREEN", green_time_b, "Direction B", 'B')
                show_signal_with_overlay(results_b, "RED", 5, "Direction B", 'B')
            else:
                show_signal_with_overlay(results_b, "RED", 5, "Direction B", 'B')
                show_signal_with_overlay(results_c, "YELLOW", 5, "Direction C", 'C')
                show_signal_with_overlay(results_c, "GREEN", green_time_c, "Direction C", 'C')
                show_signal_with_overlay(results_c, "RED", 5, "Direction C", 'C')

    finally:
        cap_b.release()
        cap_c.release()
        cv2.destroyAllWindows()
        # GPIO.cleanup()  # Uncomment for GPIO cleanup if needed

if __name__ == "__main__":
    main()
