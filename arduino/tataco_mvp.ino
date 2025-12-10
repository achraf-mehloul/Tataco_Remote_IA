/*
Tataco MVP v0.4 - Arduino Code
*/

// تعريف منافذ الريلاي
const int RELAY_PINS[] = {2, 3, 4, 5};
const int NUM_RELAYS = 4;
const String RELAY_NAMES[] = {"light", "fan", "tv", "ac"};

// حالات الريلاي
bool relayStates[NUM_RELAYS] = {false, false, false, false};

void setup() {
  Serial.begin(9600);
  
  // تهيئة منافذ الريلاي
  for (int i = 0; i < NUM_RELAYS; i++) {
    pinMode(RELAY_PINS[i], OUTPUT);
    digitalWrite(RELAY_PINS[i], HIGH); // إيقاف في البداية (نشط منخفض)
  }
  
  Serial.println("Tataco MVP v0.4 Ready");
  Serial.println("Commands: light_toggle, fan_toggle, tv_toggle, ac_on, ac_off");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    processCommand(command);
  }
}

void processCommand(String command) {
  Serial.print("Received: ");
  Serial.println(command);
  
  if (command == "light_toggle") {
    toggleRelay(0);
  } else if (command == "fan_toggle") {
    toggleRelay(1);
  } else if (command == "tv_toggle") {
    toggleRelay(2);
  } else if (command == "ac_on") {
    setRelay(3, true);
  } else if (command == "ac_off") {
    setRelay(3, false);
  } else {
    Serial.println("Unknown command");
  }
}

void toggleRelay(int relayIndex) {
  if (relayIndex >= 0 && relayIndex < NUM_RELAYS) {
    relayStates[relayIndex] = !relayStates[relayIndex];
    digitalWrite(RELAY_PINS[relayIndex], relayStates[relayIndex] ? LOW : HIGH);
    Serial.print(RELAY_NAMES[relayIndex]);
    Serial.println(relayStates[relayIndex] ? " ON" : " OFF");
  }
}

void setRelay(int relayIndex, bool state) {
  if (relayIndex >= 0 && relayIndex < NUM_RELAYS) {
    relayStates[relayIndex] = state;
    digitalWrite(RELAY_PINS[relayIndex], state ? LOW : HIGH);
    Serial.print(RELAY_NAMES[relayIndex]);
    Serial.println(state ? " ON" : " OFF");
  }
}
