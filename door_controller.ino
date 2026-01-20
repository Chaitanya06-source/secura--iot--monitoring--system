    #include <Arduino.h>
    #include <ESP32Servo.h>

    // Pin config (adjust to your wiring)
    const int TRIG_PIN = 5;
    const int ECHO_PIN = 19;
    const int SERVO_PIN = 18;  // any PWM-capable pin on ESP32

    // Distances in cm
    const float DETECT_DISTANCE_CM = 60.0;  // trigger when something is closer than this
    const unsigned long TRIGGER_COOLDOWN_MS = 5000;  // avoid spamming triggers

    // Servo angles
    const int SERVO_CLOSED_DEG = 0;
    const int SERVO_OPEN_DEG = 90;

    Servo doorServo;
    unsigned long lastTriggerMs = 0;

    float readDistanceCm() {
    // Send 10us pulse
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);

    long duration = pulseIn(ECHO_PIN, HIGH, 30000);  // 30ms timeout (~5m)
    if (duration == 0) return 9999;  // timeout

    // Sound speed: 343 m/s => 29.1 us per cm round-trip; divide by 2
    float distance = (duration * 0.0343) / 2.0;
    return distance;
    }

    void sendTriggerIfNeeded() {
    unsigned long now = millis();
    if (now - lastTriggerMs < TRIGGER_COOLDOWN_MS) return;

    float distance = readDistanceCm();
    if (distance < DETECT_DISTANCE_CM) {
        Serial.println("TRIGGER");
        lastTriggerMs = now;
    }
    }

    void handleSerialCommand() {
    if (!Serial.available()) return;
    String cmd = Serial.readStringUntil('\n');
    cmd.trim();
    cmd.toUpperCase();

    if (cmd == "OPEN") {
        doorServo.write(SERVO_OPEN_DEG);
        Serial.println("ACK_OPEN");
    } else if (cmd == "CLOSE") {
        doorServo.write(SERVO_CLOSED_DEG);
        Serial.println("ACK_CLOSE");
    }
    }

    void setup() {
    Serial.begin(9600);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    doorServo.setPeriodHertz(50);  // standard 50Hz servo
    doorServo.attach(SERVO_PIN, 500, 2400);  // adjust min/max pulse if needed
    doorServo.write(SERVO_CLOSED_DEG);

    delay(500);
    Serial.println("ESP32 door controller ready");
    }

    void loop() {
    sendTriggerIfNeeded();
    handleSerialCommand();
    delay(20);
    }

