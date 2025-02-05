from PIL import Image
import numpy as np
import cv2
import wave
import PyPDF2
import docx
import tempfile
import os

# Removed unused imports:
# - io (not used in implementation)
# - django.core.files.base import ContentFile (not used)
# - moviepy.editor import VideoFileClip (not needed as we use cv2)

class SteganographyExtractor:
    def __init__(self, stegano_file):
        self.stegano_file = stegano_file

    def extract_message(self):
        """Extract hidden message from file based on file type"""
        if self.stegano_file.file_type == 'image':
            return self._extract_from_image()
        elif self.stegano_file.file_type == 'video':
            return self._extract_from_video()
        elif self.stegano_file.file_type == 'audio':
            return self._extract_from_audio()
        elif self.stegano_file.file_type == 'document':
            return self._extract_from_document()
        else:
            raise ValueError(f"Unsupported file type: {self.stegano_file.file_type}")

    def _extract_from_image(self):
        """Extract message from image using LSB"""
        try:
            img = Image.open(self.stegano_file.processed_file)
            img_array = np.array(img)
            
            binary_data = ''
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):  # RGB channels
                        binary_data += str(img_array[i, j, k] & 1)
                        if len(binary_data) >= 8 and binary_data[-8:] == '00000000':
                            # Found end marker
                            binary_data = binary_data[:-8]
                            return self._binary_to_text(binary_data)
            
            raise ValueError("No hidden message found or invalid format")

        except Exception as e:
            raise ValueError(f"Failed to extract message: {str(e)}")

    def _extract_from_video(self):
        """Extract message from video frame"""
        try:
            # Read the frame directly as an image
            frame = cv2.imdecode(
                np.frombuffer(self.stegano_file.processed_file.read(), np.uint8),
                cv2.IMREAD_COLOR
            )
            
            if frame is None:
                raise ValueError("Could not read frame")

            height, width = frame.shape[:2]
            
            # Extract binary data from blue channel LSBs
            binary_data = ''
            for i in range(height):
                for j in range(width):
                    binary_data += str(frame[i, j, 0] & 1)
                    
                    # Check for end marker
                    if len(binary_data) >= 8 and binary_data[-8:] == '00000000':
                        message_bits = binary_data[:-8]
                        return self._binary_to_text(message_bits)
                    
                    # Early stop if we've read too much
                    if len(binary_data) > width * height:
                        break

            raise ValueError("No hidden message found in frame")

        except Exception as e:
            raise ValueError(f"Failed to extract message from video frame: {str(e)}")

    def _extract_from_audio(self):
        """Extract message from audio file using same LSB method as embedding"""
        temp_path = None
        wav_path = None
        try:
            # Create temporary file for audio processing
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(self.stegano_file.processed_file.read())
                temp_path = temp_file.name

            # Process WAV file
            with wave.open(temp_path, 'rb') as audio_file:
                # Read all frames at once
                frames = audio_file.readframes(audio_file.getnframes())
                frame_array = bytearray(frames)

                # Extract binary data
                binary_data = ''
                for byte in frame_array:
                    binary_data += str(byte & 1)  # Get LSB
                    # Check for end marker after each byte
                    if len(binary_data) >= 8 and len(binary_data) % 8 == 0:
                        if binary_data[-8:] == '00000000':
                            binary_data = binary_data[:-8]  # Remove end marker
                            return self._binary_to_text(binary_data)

            raise ValueError("No hidden message found in audio")

        except Exception as e:
            raise ValueError(f"Failed to extract message from audio: {str(e)}")
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass

    def _extract_from_document(self):
        """Extract message from document file based on file extension"""
        try:
            file_ext = self.stegano_file.processed_file.name.split('.')[-1].lower()
            
            if file_ext == 'pdf':
                return self._extract_from_pdf()
            elif file_ext in ['docx', 'doc']:
                return self._extract_from_word()
            else:
                raise ValueError(f"Unsupported document type: {file_ext}")

        except Exception as e:
            raise ValueError(f"Failed to extract message from document: {str(e)}")

    def _extract_from_pdf(self):
        """Extract hidden message from PDF file using metadata"""
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
                temp_file.write(self.stegano_file.processed_file.read())
                temp_path = temp_file.name

            with open(temp_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Check both standard metadata and XMP metadata
                if pdf_reader.metadata and '/SteganoMessage' in pdf_reader.metadata:
                    message = pdf_reader.metadata['/SteganoMessage']
                    return message
                
                # Try alternate metadata location
                if hasattr(pdf_reader, 'documentInfo') and pdf_reader.documentInfo:
                    if '/SteganoMessage' in pdf_reader.documentInfo:
                        return pdf_reader.documentInfo['/SteganoMessage']

            raise ValueError("No hidden message found in PDF")

        except Exception as e:
            raise ValueError(f"Failed to extract message from PDF: {str(e)}")
        
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass

    def _extract_from_word(self):
        """Extract hidden message from Word document"""
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix='.docx', delete=False) as temp_file:
                temp_file.write(self.stegano_file.processed_file.read())
                temp_path = temp_file.name

            doc = docx.Document(temp_path)
            
            # Look for hidden text in paragraphs
            for paragraph in doc.paragraphs:
                for run in paragraph.runs:
                    if hasattr(run.font, 'hidden') and run.font.hidden:
                        text = run.text
                        if text.startswith('SteganoMessage:'):
                            return text.replace('SteganoMessage:', '').strip()

            raise ValueError("No hidden message found in Word document")

        except Exception as e:
            raise ValueError(f"Failed to extract message from Word document: {str(e)}")
        
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass

    def _binary_to_text(self, binary_data):
        """Convert binary data to text"""
        text = ''
        for i in range(0, len(binary_data), 8):
            byte = binary_data[i:i+8]
            text += chr(int(byte, 2))
        return text
