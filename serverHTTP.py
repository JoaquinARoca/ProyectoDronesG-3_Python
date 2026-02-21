########  INSTALAR  ##########
# Flask
##############################

import json
import threading
import time
from flask import Flask, request, jsonify, send_from_directory
import paho.mqtt.client as mqtt
from threading import Lock

# CONFIGURACIÓN
MQTT_BROKER = "broker.hivemq.com"   # cambia si quieres otro broker
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

# Topics (ajusta si tus tópicos son distintos)
TOPIC_PREFIX_PUB = "mobileFlask/autopilotServiceDemo"        # donde publicamos comandos
TOPIC_TELEMETRY_SUB = "autopilotServiceDemo/mobileFlask/telemetryInfo"  # donde viene telemetría

app = Flask(__name__, static_folder="static", static_url_path="/static")

# Estado compartido de telemetría
telemetry = {
    "alt": 0.0,
    "state": "disconnected",
}
telemetry_lock = Lock()

# --- MQTT client setup ---
mqtt_client = mqtt.Client(client_id="http_gateway_" + str(int(time.time())))
# Si tu broker requiere username/password:
# mqtt_client.username_pw_set("user", "pass")

def on_connect(client, userdata, flags, rc):
    print("MQTT conectado con rc =", rc)
    # Suscribirse a telemetría
    client.subscribe(TOPIC_TELEMETRY_SUB)
    print("Subscribed to", TOPIC_TELEMETRY_SUB)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        # esperamos JSON con campos alt y state según tu ejemplo
        data = json.loads(payload)
        with telemetry_lock:
            if "alt" in data:
                telemetry["alt"] = float(data["alt"])
            if "state" in data:
                telemetry["state"] = data["state"]
    except Exception as e:
        print("Error procesando mensaje MQTT:", e, msg.topic, msg.payload)

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

def mqtt_connect_and_loop():
    while True:
        try:
            print("Intentando conectar a MQTT broker:", MQTT_BROKER, MQTT_PORT)
            mqtt_client.connect(MQTT_BROKER, MQTT_PORT, MQTT_KEEPALIVE)
            mqtt_client.loop_forever()  # bloqueará aquí; si desconecta intentará reconectar internamente
        except Exception as e:
            print("Error MQTT:", e)
            time.sleep(5)

# Lanzar hilo MQTT en background antes de arrancar Flask
mqtt_thread = threading.Thread(target=mqtt_connect_and_loop, daemon=True)
mqtt_thread.start()

# ------------------ Endpoints HTTP ------------------

@app.route("/connect", methods=["POST"])
def http_connect():
    # Publicar comando de conexión (payload vacío)
    topic = f"{TOPIC_PREFIX_PUB}/connect"
    mqtt_client.publish(topic, "")
    return ("", 204)

@app.route("/startTelemetry", methods=["POST"])
def http_start_telemetry():
    topic = f"{TOPIC_PREFIX_PUB}/startTelemetry"
    mqtt_client.publish(topic, "")
    return ("", 204)

@app.route("/takeoff", methods=["POST"])
def http_takeoff():
    data = request.get_json() or {}
    altura = data.get("altura") or data.get("alt") or data.get("height")
    if altura is None:
        return jsonify({"error": "faltó campo 'altura' en JSON"}), 400
    topic = f"{TOPIC_PREFIX_PUB}/arm_takeOff"
    # publicar la altura como string (igual que hacía el cliente mqtt directamente)
    mqtt_client.publish(topic, str(altura))
    return ("", 204)

@app.route("/land", methods=["POST"])
def http_land():
    topic = f"{TOPIC_PREFIX_PUB}/Land"
    mqtt_client.publish(topic, "")
    return ("", 204)

@app.route("/move", methods=["POST"])
def http_move():
    data = request.get_json() or {}
    direction = data.get("direction") or data.get("dir")
    if not direction:
        return jsonify({"error": "faltó campo 'direction' en JSON"}), 400
    topic = f"{TOPIC_PREFIX_PUB}/go"
    mqtt_client.publish(topic, str(direction))
    return ("", 204)

@app.route("/rtl", methods=["POST"])
def http_rtl():
    # Publicar comando RTL
    topic = f"{TOPIC_PREFIX_PUB}/RTL"
    mqtt_client.publish(topic, "")
    return ("", 204)

@app.route("/telemetry", methods=["GET"])
def http_telemetry():
    # Devuelve la última telemetría conocida
    with telemetry_lock:
        resp = {
            "alt": telemetry["alt"],
            "state": telemetry["state"],
        }
    return jsonify(resp)

# Opcional: servir un archivo HTML desde / (si pones tu cliente en carpeta static/index.html)
@app.route("/")
def index():
    try:
        return send_from_directory("templates", "indexHTTP.html")
    except Exception:
        return "<h3>Servidor HTTP → MQTT gateway</h3><p>Coloca tu cliente en /templates/indexHTTP.html</p>"

# ----------------------------------------------------

if __name__ == "__main__":
    # Ejecutar Flask (no usar en producción; para pruebas).
    print("Arrancando Flask en http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
