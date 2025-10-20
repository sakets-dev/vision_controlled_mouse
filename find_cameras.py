import cv2

def find_cameras():
    """Find all available cameras"""
    available_cameras = []
    
    print("Scanning for available cameras...")
    
    # Check camera indices from 0 to 10
    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            # Try to read a frame to confirm camera works
            ret, frame = cap.read()
            if ret:
                # Get camera properties
                width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                fps = cap.get(cv2.CAP_PROP_FPS)
                
                print(f"Camera {i}: {int(width)}x{int(height)} @ {fps} FPS")
                available_cameras.append(i)
            cap.release()
    
    if available_cameras:
        print(f"\nFound {len(available_cameras)} camera(s): {available_cameras}")
        print("\nTo test a specific camera, run:")
        for cam in available_cameras:
            print(f"  python3 -c \"import cv2; cap=cv2.VideoCapture({cam}); print('Camera {cam} test:', cap.isOpened())\"")
    else:
        print("No cameras found!")
    
    return available_cameras

if __name__ == "__main__":
    find_cameras()
