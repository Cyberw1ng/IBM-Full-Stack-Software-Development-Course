import unittest
import emotion_detection as ed

class Detection(unittest.TestCase):
    def test_joy(self):
        data = ed.emotion_detector("I am glad this happened")
        result = ed.emotion_predictor(data)
        self.assertEqual(result["dominant_emotion"], "joy")
    
    def test_anger(self):
        data = ed.emotion_detector("I am really mad about this")
        result = ed.emotion_predictor(data)
        self.assertEqual(result["dominant_emotion"], "anger")
        
    def test_disgust(self):
        data = ed.emotion_detector("I feel disgusted just hearing about this")
        result = ed.emotion_predictor(data)
        self.assertEqual(result["dominant_emotion"], "disgust")

    def test_sad(self):
        data = ed.emotion_detector("I am so sad about this")
        result = ed.emotion_predictor(data)
        self.assertEqual(result["dominant_emotion"], "sadness")

    def test_fear(self):
        data = ed.emotion_detector("I am really afraid that this will happen")
        result = ed.emotion_predictor(data)
        self.assertEqual(result["dominant_emotion"], "fear")

if __name__ == "__main__":
    unittest.main()
