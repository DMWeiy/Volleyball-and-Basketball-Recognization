#include <Servo.h>

String inputString = "";  // String to store input data
int x = 0;
int y = 0;
int x_axis = 0;
int y_axis = 0;
int last_x = 0;
int last_y = 0;

Servo left_right;
Servo up_down;

// Define a threshold for detecting significant movement
const int THRESHOLD = 5;  // You can adjust this value to your needs

void setup() {
  left_right.attach(3);  // Attach left-right servo to pin 2
  up_down.attach(2);     // Attach up-down servo to pin 3
  Serial.begin(9600);    // Start serial communication
}

void loop() {
  // Check if serial data is available
  if (Serial.available() > 0) {
    inputString = Serial.readStringUntil('\r');  // Read until carriage return
    inputString.trim();  // Remove leading and trailing whitespace

    // Ensure input contains a comma and is in the correct format
    int commaIndex = inputString.indexOf(',');
    if (commaIndex > 0) {
      // Extract x and y coordinates
      x_axis = inputString.substring(0, commaIndex).toInt();
      y_axis = inputString.substring(commaIndex + 1).toInt();

      // Map coordinates to servo range (180 to 0)
      y = map(y_axis, 0, 720, 180, 0);
      x = map(x_axis, 0, 1280, 180, 0);

      // Check if the change in coordinates exceeds the threshold
      if (abs(x - last_x) > THRESHOLD ) {
        // Only update the servo positions if there is a significant change
        left_right.write(x);  // Set horizontal servo position
        up_down.write(y);    // Set vertical servo position

        // Print the new servo positions for debugging
        Serial.print("X: ");
        Serial.println(x);
        Serial.print("Y: ");
        Serial.println(y);

        // Update the last known positions
        last_x = x;
        last_y = y;
      } else {
        // If no significant change, just print a message (optional)
        Serial.println("No significant movement detected.");
      }
    } else {
      // Handle invalid input format if no comma is found
      Serial.println("Invalid input format. Expected: x,y");
    }
  }
}
