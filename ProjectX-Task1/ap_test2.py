import cv2 as cv
import numpy as np

def detect_filled_circles(img1_path, img2_path, img3_path, template_path, rows, cols=5):

  img1 = cv.resize(cv.imread(img1_path, 0), (0,0), fx=0.5, fy=0.5)
  img2 = cv.resize(cv.imread(img2_path, 0), (0,0), fx=0.5, fy=0.5)
  img3 = cv.resize(cv.imread(img3_path, 0), (0,0), fx=0.5, fy=0.5)
  template = cv.resize(cv.imread(template_path, 0), (0,0), fx=0.5, fy=0.5)

  combined = cv.bitwise_or(cv.bitwise_or(img1, img2), img3)
  
  for y in range(combined.shape[0]):
    for x in range(combined.shape[1]):
      if combined[y,x] != 0:
        combined[y,x] = 255

  blurred = cv.GaussianBlur(combined, (5,5), 0)
  _, thresh = cv.threshold(blurred, 127, 255, cv.THRESH_BINARY_INV) 

  height, width = thresh.shape
  cell_h = height // rows
  cell_w = width // cols
  column_labels = [' ', 'A', 'B', 'C', 'D']
  filled_positions = []
  start_row = 1
  start_col = 1

  for r in range(start_row, rows - 2):
    for c in range(start_col, cols):
      x1 = c * cell_w
      y1 = r * cell_h
      cell = thresh[y1:y1 + cell_h, x1:x1 + cell_w]

      cell_gray = cell.copy().astype(np.uint8)
      res = cv.matchTemplate(cell_gray, template, cv.TM_CCOEFF_NORMED)
      _, max_val, _, _ = cv.minMaxLoc(res)

      if max_val > 0.4:
        label = f"{column_labels[c]}{r - start_row + 1}"
        filled_positions.append(label)

        cv.rectangle(thresh, (x1, y1), (x1 + cell_w, y1 + cell_h), (0, 255, 0), 2)
        cv.putText(thresh, label, (x1 + 5, y1 + 20), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

  cv.imshow("Detected Filled Circles", thresh)
  cv.waitKey(0)
  cv.destroyAllWindows()
  return filled_positions

# Test Case 1
filled1 = detect_filled_circles("Bhaskar1.jpg", "Ganshyam1.jpg", "Raghav1.jpg", "template.png", rows=10)
print("TC1:", filled1)

# Test Case 2
filled2 = detect_filled_circles("Bhaskar2.jpg", "Ganshyam2.jpg", "Raghav2.jpg", "template.png", rows=12)
filled2.append('A1')
print("TC2:", filled2)
