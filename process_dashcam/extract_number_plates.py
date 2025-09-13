import cv2
import numpy as np
import easyocr
import pandas as pd
import os
import re
from datetime import datetime
import argparse
from pathlib import Path
import logging
from tqdm import tqdm

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NumberPlateExtractor:
    def __init__(self, video_path, output_path="number_plates_output.xlsx"):
        """
        Initialize the number plate extractor
        
        Args:
            video_path (str): Path to the input video file
            output_path (str): Path for the output Excel file
        """
        self.video_path = video_path
        self.output_path = output_path
        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR for English text
        self.results = []
        
        # Specific number plate pattern for AB12CD3456 format
        self.plate_patterns = [
            # AB12CD3456 format: 2 letters, 2 numbers, 2 letters, 4 numbers
            r'[A-Z]{2}\d{2}[A-Z]{2}\d{4}',
            # Allow for spaces: AB12 CD3456
            r'[A-Z]{2}\d{2}\s*[A-Z]{2}\d{4}',
            # Allow for partial matches in case of OCR errors
            r'[A-Z]{2}\d{2}[A-Z]{1,2}\d{3,4}',
            r'[A-Z]{1,2}\d{2}[A-Z]{2}\d{3,4}',
        ]
        
    def preprocess_frame_multiple_methods(self, frame):
        """
        Apply multiple preprocessing methods to enhance number plate detection
        
        Args:
            frame: Input frame from video
            
        Returns:
            list: List of preprocessed frames using different methods
        """
        processed_frames = []
        
        # Method 1: Standard preprocessing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh1 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                      cv2.THRESH_BINARY, 11, 2)
        processed_frames.append(thresh1)
        
        # Method 2: Edge detection approach
        edges = cv2.Canny(gray, 50, 150)
        processed_frames.append(edges)
        
        # Method 3: High contrast preprocessing
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        thresh2 = cv2.adaptiveThreshold(enhanced, 255, cv2.ADAPTIVE_THRESH_MEAN_C, 
                                      cv2.THRESH_BINARY, 15, 2)
        processed_frames.append(thresh2)
        
        # Method 4: Morphological operations
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        morph = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)
        processed_frames.append(morph)
        
        # Method 5: Original grayscale (for OCR)
        processed_frames.append(gray)
        
        return processed_frames
    
    def detect_plates_multiple_strategies(self, frame, processed_frames):
        """
        Use multiple strategies to detect potential number plate regions
        
        Args:
            frame: Original frame
            processed_frames: List of preprocessed frames
            
        Returns:
            list: List of potential plate regions
        """
        potential_plates = []
        
        # Strategy 1: Contour detection on different preprocessed frames
        for i, processed_frame in enumerate(processed_frames[:-1]):  # Skip grayscale
            plates = self._detect_contours(processed_frame, strategy=f"contour_{i}")
            potential_plates.extend(plates)
        
        # Strategy 2: Sliding window approach
        plates = self._sliding_window_detection(frame)
        potential_plates.extend(plates)
        
        # Strategy 3: Color-based detection
        plates = self._color_based_detection(frame)
        potential_plates.extend(plates)
        
        # Strategy 4: Full frame OCR (for cases where detection fails)
        plates = self._full_frame_ocr(frame)
        potential_plates.extend(plates)
        
        return potential_plates
    
    def _detect_contours(self, frame, strategy="contour"):
        """
        Detect contours with more selective parameters
        """
        contours, _ = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        potential_plates = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            
            # More selective area constraints
            if 2000 < area < 30000:  # Reduced range for better selectivity
                x, y, w, h = cv2.boundingRect(contour)
                
                # More selective aspect ratio
                aspect_ratio = w / float(h)
                
                # Tighter aspect ratio range for number plates
                if 2.5 <= aspect_ratio <= 5.5:  # More realistic for number plates
                    potential_plates.append((x, y, w, h, strategy))
        
        return potential_plates
    
    def _sliding_window_detection(self, frame):
        """
        Use sliding window to detect number plates - more selective
        """
        potential_plates = []
        height, width = frame.shape[:2]
        
        # More selective window sizes
        window_sizes = [
            (int(width*0.12), int(height*0.06)),  # Medium windows only
            (int(width*0.18), int(height*0.09)),  # Larger windows
        ]
        
        step_size = 80  # Larger step size to reduce false positives
        
        for w_size, h_size in window_sizes:
            for y in range(0, height - h_size, step_size):
                for x in range(0, width - w_size, step_size):
                    # Extract window
                    window = frame[y:y+h_size, x:x+w_size]
                    
                    # Check if window has good contrast (potential for text)
                    gray_window = cv2.cvtColor(window, cv2.COLOR_BGR2GRAY)
                    std_dev = np.std(gray_window)
                    
                    if std_dev > 30:  # Higher contrast threshold
                        potential_plates.append((x, y, w_size, h_size, "sliding_window"))
        
        return potential_plates
    
    def _color_based_detection(self, frame):
        """
        Detect regions based on color characteristics of number plates - more selective
        """
        potential_plates = []
        
        # Convert to different color spaces
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Look for white/yellow regions (common number plate colors)
        # White plates - more selective range
        lower_white = np.array([0, 0, 180])
        upper_white = np.array([180, 25, 255])
        white_mask = cv2.inRange(hsv, lower_white, upper_white)
        
        # Yellow plates - more selective range
        lower_yellow = np.array([20, 120, 120])
        upper_yellow = np.array([30, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        
        # Combine masks
        combined_mask = cv2.bitwise_or(white_mask, yellow_mask)
        
        # Find contours in the mask
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if 2000 < area < 25000:  # More selective area range
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)
                if 2.5 <= aspect_ratio <= 5.0:  # Tighter aspect ratio
                    potential_plates.append((x, y, w, h, "color_based"))
        
        return potential_plates
    
    def _full_frame_ocr(self, frame):
        """
        Perform OCR on the entire frame as a fallback - more selective
        """
        # Resize frame for faster processing
        height, width = frame.shape[:2]
        scale_factor = 0.5
        resized_frame = cv2.resize(frame, (int(width*scale_factor), int(height*scale_factor)))
        
        # Convert to RGB for EasyOCR
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
        
        # Perform OCR
        results = self.reader.readtext(rgb_frame)
        
        potential_plates = []
        for (bbox, text, confidence) in results:
            if confidence > 0.5 and self._looks_like_plate_text(text):  # Higher confidence threshold
                # Convert bbox back to original scale
                x1, y1 = int(bbox[0][0] / scale_factor), int(bbox[0][1] / scale_factor)
                x3, y3 = int(bbox[2][0] / scale_factor), int(bbox[2][1] / scale_factor)
                w, h = x3 - x1, y3 - y1
                
                # Expand the region slightly
                x1 = max(0, x1 - 10)
                y1 = max(0, y1 - 10)
                w = min(width - x1, w + 20)
                h = min(height - y1, h + 20)
                
                potential_plates.append((x1, y1, w, h, "full_frame_ocr"))
        
        return potential_plates
    
    def _looks_like_plate_text(self, text):
        """
        Check if text looks like it could be a number plate in AB12CD3456 format
        """
        if not text or len(text) < 8:  # Minimum 8 characters for AB12CD3456
            return False
        
        # Clean the text
        cleaned = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # Must be close to 10 characters
        if len(cleaned) < 8 or len(cleaned) > 12:
            return False
        
        # Check if it has a mix of letters and numbers
        has_letters = any(c.isalpha() for c in cleaned)
        has_numbers = any(c.isdigit() for c in cleaned)
        
        # Must have both letters and numbers
        if not (has_letters and has_numbers):
            return False
        
        # Check if it roughly follows the pattern: letters-numbers-letters-numbers
        # This is a simplified check for the AB12CD3456 format
        return True
    
    def extract_text_from_roi(self, frame, roi):
        """
        Extract text from a region of interest with multiple approaches
        """
        x, y, w, h, strategy = roi
        
        # Extract the region
        plate_region = frame[y:y+h, x:x+w]
        
        if plate_region.size == 0:
            return ""
        
        # Try multiple preprocessing methods for OCR
        texts = []
        
        # Method 1: Original region
        try:
            rgb_region = cv2.cvtColor(plate_region, cv2.COLOR_BGR2RGB)
            results = self.reader.readtext(rgb_region)
            text = ' '.join([result[1] for result in results])
            if text.strip():
                texts.append(text.strip())
        except:
            pass
        
        # Method 2: Resized region
        try:
            resized = cv2.resize(plate_region, (w*2, h*2))
            rgb_resized = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
            results = self.reader.readtext(rgb_resized)
            text = ' '.join([result[1] for result in results])
            if text.strip():
                texts.append(text.strip())
        except:
            pass
        
        # Method 3: Enhanced contrast
        try:
            gray = cv2.cvtColor(plate_region, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)
            results = self.reader.readtext(enhanced)
            text = ' '.join([result[1] for result in results])
            if text.strip():
                texts.append(text.strip())
        except:
            pass
        
        # Return the best result (longest text)
        if texts:
            return max(texts, key=len)
        
        return ""
    
    def validate_number_plate(self, text):
        """
        Validation specific to AB12CD3456 format
        """
        if not text or len(text) < 8:  # Minimum 8 characters for AB12CD3456
            return False
        
        # Clean the text
        cleaned_text = re.sub(r'[^A-Z0-9]', '', text.upper())
        
        # Must be exactly 10 characters for AB12CD3456 format
        if len(cleaned_text) != 10:
            return False
        
        # Check if it has the right mix of letters and numbers
        has_letters = any(c.isalpha() for c in cleaned_text)
        has_numbers = any(c.isdigit() for c in cleaned_text)
        
        if not (has_letters and has_numbers):
            return False
        
        # Check against specific patterns first
        for pattern in self.plate_patterns:
            if re.match(pattern, cleaned_text):
                return True
        
        # If no pattern matches, check if it follows the general structure
        # Should have letters in positions 1-2, 5-6 and numbers in positions 3-4, 7-10
        if (cleaned_text[0:2].isalpha() and 
            cleaned_text[2:4].isdigit() and 
            cleaned_text[4:6].isalpha() and 
            cleaned_text[6:10].isdigit()):
            return True
        
        return False
    
    def format_timestamp(self, frame_number, fps):
        """
        Convert frame number to timestamp
        """
        seconds = frame_number / fps
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def process_video(self, sample_rate=10):  # Reduced sample rate for better detection
        """
        Process the video and extract number plates
        """
        cap = cv2.VideoCapture(self.video_path)
        
        if not cap.isOpened():
            logger.error(f"Error: Could not open video file {self.video_path}")
            return
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        logger.info(f"Processing video: {self.video_path}")
        logger.info(f"FPS: {fps}, Total frames: {total_frames}")
        logger.info(f"Sample rate: {sample_rate} (processing every {sample_rate}th frame)")
        
        frame_count = 0
        processed_frames = 0
        
        # Use tqdm for progress bar
        with tqdm(total=total_frames//sample_rate, desc="Processing frames") as pbar:
            while True:
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Process every Nth frame
                if frame_count % sample_rate == 0:
                    processed_frames += 1
                    
                    # Apply multiple preprocessing methods
                    processed_frames_list = self.preprocess_frame_multiple_methods(frame)
                    
                    # Use multiple detection strategies
                    potential_plates = self.detect_plates_multiple_strategies(frame, processed_frames_list)
                    
                    # Process each potential plate region
                    for roi in potential_plates:
                        try:
                            # Extract text from ROI
                            text = self.extract_text_from_roi(frame, roi)
                            
                            # Validate if it's a number plate
                            if text and self.validate_number_plate(text):
                                timestamp = self.format_timestamp(frame_count, fps)
                                
                                # Clean the text for output
                                cleaned_text = re.sub(r'[^A-Z0-9]', '', text.upper())
                                
                                self.results.append({
                                    'Timestamp': timestamp,
                                    'Frame_Number': frame_count,
                                    'Registration_Number': cleaned_text,
                                    'Raw_Text': text,
                                    'Detection_Method': roi[4]
                                })
                                
                                logger.info(f"Found number plate: {cleaned_text} at {timestamp} using {roi[4]}")
                        
                        except Exception as e:
                            logger.warning(f"Error processing ROI: {e}")
                    
                    pbar.update(1)
                
                frame_count += 1
        
        cap.release()
        logger.info(f"Video processing completed. Found {len(self.results)} number plates.")
    
    def save_results(self):
        """
        Save results to Excel file
        """
        if not self.results:
            logger.warning("No number plates found to save.")
            return
        
        # Create DataFrame
        df = pd.DataFrame(self.results)
        
        # Remove duplicates based on registration number and timestamp
        df = df.drop_duplicates(subset=['Registration_Number', 'Timestamp'])
        
        # Sort by timestamp
        df = df.sort_values('Timestamp')
        
        # Save to Excel
        df.to_excel(self.output_path, index=False, sheet_name='Number_Plates')
        
        logger.info(f"Results saved to {self.output_path}")
        logger.info(f"Total unique number plates found: {len(df)}")
        
        return df

def main():
    """
    Main function to run the number plate extraction
    """
    parser = argparse.ArgumentParser(description='Extract number plates from dashcam videos')
    parser.add_argument('--video', '-v', required=True, help='Path to input video file')
    parser.add_argument('--output', '-o', default='number_plates_output.xlsx', 
                       help='Path for output Excel file')
    parser.add_argument('--sample-rate', '-s', type=int, default=10,
                       help='Process every Nth frame (default: 10)')
    
    args = parser.parse_args()
    
    # Check if video file exists
    if not os.path.exists(args.video):
        logger.error(f"Video file not found: {args.video}")
        return
    
    # Create extractor and process video
    extractor = NumberPlateExtractor(args.video, args.output)
    extractor.process_video(sample_rate=args.sample_rate)
    extractor.save_results()

if __name__ == "__main__":
    # If no command line arguments, process videos in test folder
    test_folder = "test"
    
    if os.path.exists(test_folder):
        video_files = [f for f in os.listdir(test_folder) 
                      if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
        
        if video_files:
            logger.info(f"Found {len(video_files)} video files in {test_folder}")
            
            for video_file in video_files:
                video_path = os.path.join(test_folder, video_file)
                output_file = f"number_plates_{os.path.splitext(video_file)[0]}.xlsx"
                
                logger.info(f"Processing: {video_file}")
                
                extractor = NumberPlateExtractor(video_path, output_file)
                extractor.process_video(sample_rate=10)  # More frequent sampling
                extractor.save_results()
                
                logger.info(f"Completed processing: {video_file}")
        else:
            logger.warning(f"No video files found in {test_folder}")
    else:
        logger.warning(f"Test folder not found. Please run with command line arguments.")
        # Uncomment the line below to run with command line arguments
        # main()
