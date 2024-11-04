// für NodeMCU Lolin V3
// Switch -Button auf Website oder mit Kommandos
// dient als Satelliten-Relais per WLAN vom Raspberry aus erreichbar
// IP-ADRESSE/?relais=0 oder 1 für ein und aus, =2 für Toggle.
// Brücke mit Taster zwischen D2 und GND wirkt auch als Toggle

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ESP8266HTTPClient.h>
#include "index_html.h"  // In dieser Datei befindet sich die Steuerung Webseite
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ezTime.h>

// GPIO where the DS18B20 is connected to
const int oneWireBus = 0;     
// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);
// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);


// Schnellkonfiguration
//#define kiste_01
#define kiste_02

#ifdef kiste_01
  // zugeordnete Relaisnummer in der Influx-Datenbank
  const int relaisnummer1 = 9;
  const int relaisnummer2 = 10;
  String newHostname = "ESP-Rel-09-10";
  #define tempsensor // wenn ein DS18B20 angeschlossen ist.
#endif

#ifdef kiste_02
  // zugeordnete Relaisnummer in der Influx-Datenbank
  const int relaisnummer1 = 11;
  const int relaisnummer2 = 12;
  String newHostname = "ESP-Rel-11-12";
#endif

#define herbi      // Produktiv-Umgebung 
//#define peter      // Testumgebung von PFU
//#define wifi_ap    // entweder selber erzeugtes WLAN
#define wifi_sta   // oder an FritzBox anmelden

#ifdef herbi // Zugangsdaten Herbert
  const char* ssid = "FRITZ!Box";      // WLAN-Name,
  const char* password = ""; // WLAN-Passwort
  // Grafana auf dem Raspberry pirelais 192.168.178.32 als Beispiel
  const char* influxUrl = "http://192.168.178.32:8086/write?db=home";
  const char* influxUser = "grafana";
  const char* influxPassword = "herbi";
#endif

#ifdef peter // Testumgebung
  #include "credentials.h" // meine Zugangsdaten
#endif


// HTML-Beschriftung umgeändert bei ON/OFF
int active_low = 0;   // "0" Relais schaltet bei +5V , "1" Relais schaltet bei 0V
int active_low2 = 0;   // Das zweite Relais, das an D5 angeschlossen ist.
#define RelaisPin  5   // GPIO5 ist D1 
#define RelaisPin2 14  // GPIO14 ist D5
#define TasterPin  4   // GPIO4 = D2 als Aktiv Low (Taster zwischen TasterPin und GND) 

ESP8266WebServer server(80);// Serverport  hier einstellen
int val = 0; 				// Hier wird der Schaltzustand gespeichert
int minuteAlt = 1;

// Übergabe Relaisstatus an Influx-Datenbank
void sendeRelaisStatus(int rel, int zustand) {
  Serial.print("Relais#"); Serial.print(rel); Serial.print(" Status:"); Serial.println(zustand);
  HTTPClient http;
  String influxData = "";
  // Set data type and add tags
  influxData += "relais,ort=sat_relais"+String(rel)+" status="+String(zustand) + "\n";
  // Create POST message
  http.begin(influxUrl);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.setAuthorization(influxUser, influxPassword);
  // The first attempt to send returns -1
  int httpCode = -1;
  while(httpCode == -1){
    httpCode = http.POST(influxData);
    http.writeToStream(&Serial);
  }
  http.end();
}


// Auswertung der API Parameter
void Ereignis_Index()    // Wird ausgeführt wenn "http://<ip address>/" aufgerufen wurde
{
  if (server.args() > 0) // wenn Argumente im GET Anfrage vorhanden sind z.B http://<ip address>/?zustand=r
  {
    if (server.arg("relais") == "0")  // prüfen ob "/?relais=0"
    {
      Serial.print("Relais #"); Serial.print(relaisnummer1); Serial.println(" :Aus");
      val = 0;                        // Ausschalten
      digitalWrite(RelaisPin, active_low ^ val);
      sendeRelaisStatus(relaisnummer1,val);
    }
    if (server.arg("relais") == "1")  // prüfen ob "/?relais=1"
    {
      Serial.print("Relais #"); Serial.print(relaisnummer1); Serial.println(" :Ein");
      val = 1;                        // Einschalten
      digitalWrite(RelaisPin, active_low ^ val);
      sendeRelaisStatus(relaisnummer1,val);
    }
    if (server.arg("relais") == "2")  // prüfen ob "/?relais=2"  Toggle Funktion
    {
      val = !val;                     // Umschalten
      Serial.print("Umschalten Relais #"); Serial.print(relaisnummer1); Serial.print(" auf "); Serial.println(String(val));
      digitalWrite(RelaisPin, active_low ^ val);
      sendeRelaisStatus(relaisnummer1,val);
    }                                                  // es wird immer Relais Zustand mitgeteilt
    // Relais2 Erweiterung
    if (server.arg("relais2") == "0")  // prüfen ob "/?relais2=0"
    {

      sendeRelaisStatus(relaisnummer2,val);
    }
    if (server.arg("relais2") == "1")  // prüfen ob "/?relais2=1"
    {
      Serial.print("Relais #"); Serial.print(relaisnummer2); Serial.println(" :Ein");
      val = 1;                        // Einschalten
      digitalWrite(RelaisPin2, active_low2 ^ val);
      sendeRelaisStatus(relaisnummer2,val);
    }
    if (server.arg("relais2") == "2")  // prüfen ob "/?relais2=2"  Toggle Funktion
    {
      val = !val;                     // Umschalten
      Serial.print("Umschalten Relais #"); Serial.print(relaisnummer1); Serial.print(" auf "); Serial.println(String(val));
      digitalWrite(RelaisPin2, active_low2 ^ val);
      sendeRelaisStatus(relaisnummer2,val);
    }                                                  // es wird immer Relais Zustand mitgeteilt


    server.sendHeader("Cache-Control", "no-cache");    // wichtig! damit Daten nicht aus dem Browser cache kommen
    server.send(200, "text/plain", String(int(val)) ); // Antwort an Internet Browser senden nur eine Zahl ("0"/"1")
  }
  else        // wenn keine Argumente im GET Anfrage
  {
    Serial.println("Sende Index.html");
    server.send(200, "text/html", indexHTML);           //dann Index Webseite senden (sehe Datei "index_html.h")
  }
}

void handleNotFound()
{
  server.send(404, "text/plain", "404: Not found");     // Send HTTP status 404 (Not Found)
}

void sendeTempanGrafana(float temp) {
  HTTPClient http;
  String influxData = "";
  // Set data type and add tags
  influxData += "sensor,ort=WPTemp WPTemp="+String(temp) + "\n";
  // Create POST message
  http.begin(influxUrl);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  http.setAuthorization(influxUser, influxPassword);

  // The first attempt to send returns -1
  int httpCode = -1;
  while(httpCode == -1){
    httpCode = http.POST(influxData);
    http.writeToStream(&Serial);
  }
http.end();
}


void setup()
{
  Serial.begin(9600);	// Serielle Schnittstelle initialisieren
  delay(200);
  #ifdef tempsensor
    // Start the DS18B20 sensor
    sensors.begin();
  #endif
  // Relais-Modus setzen
  pinMode(RelaisPin, OUTPUT);
  pinMode(TasterPin, INPUT_PULLUP);
  digitalWrite(RelaisPin, active_low);
  // Relais2
  pinMode(RelaisPin2, OUTPUT);
  digitalWrite(RelaisPin2, active_low2);

  Serial.println("");	  // Neue Zeile
  Serial.println("Warte auf Verbindung");
  
  #ifdef wifi_ap
    WiFi.mode(WIFI_AP);      // access point modus
    WiFi.softAP("esp-relais", "12345678");  // Name des Wi-Fi Netzes und Passwort
    WiFi.softAP("lolin-relais", "12345678");  // Name des Wi-Fi Netzes und Passwort
    delay(500);           //Abwarten 0,5s
    Serial.print("IP Adresse ");  //Ausgabe aktueller IP des Servers
    Serial.println(WiFi.softAPIP());
  #endif
  
  #ifdef wifi_sta
    // Mit Haus WLAN Verbinden
    WiFi.mode(WIFI_STA);
    //Get Current Hostname
    Serial.printf("Default hostname: %s\n", WiFi.hostname().c_str());
    //Set new hostname
    WiFi.hostname(newHostname.c_str());
    //Get Current Hostname
    Serial.printf("New hostname: %s\n", WiFi.hostname().c_str());
    WiFi.begin(ssid, password);
    // Warte auf verbindung
    while (WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.print("Verbunden mit ");
    Serial.println(ssid);
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    // ENDE Mit Haus WLAN Verbinden
  #endif

  // Zeitsignal holen
	waitForSync();
  Serial.println();
	Serial.println("UTC:             " + UTC.dateTime());
	Timezone myTZ;
  myTZ.setLocation(F("de"));
	Serial.print(F("Germany:         "));
	Serial.println(myTZ.dateTime());
  //  Behandlung der Ereignisse 
  server.on("/", Ereignis_Index);
  server.onNotFound ( handleNotFound );

  server.begin();  			// Starte den Server
  Serial.println("HTTP Server gestartet");
}

void loop()
{
  #ifdef tempsensor
    events();
    if (minute()%2==0) {
       if (minuteAlt != minute()){ 
         Serial.print(minute()); Serial.println(".Minute ist gerade, Temperatur wird geschrieben");;
         sensors.requestTemperatures(); 
         float temperatureC = sensors.getTempCByIndex(0);
         Serial.print(temperatureC);  Serial.println("ºC");
         sendeTempanGrafana(temperatureC);
       }
      minuteAlt = minute();
      }
  #endif
  // Website 
  server.handleClient();
  if (!digitalRead(TasterPin)) // Wenn Taster betätigt "Signal 0"
  {
    val = !val;                // Umschalten
    digitalWrite(RelaisPin, active_low ^ val);  // Wenn active_low - Variable ist "1",  Zustand "val" wird invertiert
    // Serial.println("Umschalten per Taster auf " + String(val));
    sendeRelaisStatus(relaisnummer1,val); // 1.Parameter ist Relais-Nummer, 2. Parameter ist 0 oder 1
    delay(500);       // Entprellung, Warten bis der Taster Kontakt sich beruhigt hat
    while (!digitalRead(TasterPin))server.handleClient(); // warten bis der Taster los gelassen wurde
  }
}
