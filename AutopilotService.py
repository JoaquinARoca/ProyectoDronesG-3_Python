############  INSTALAR ##############
# paho-mqtt, version 1.6.1
#####################################

import paho.mqtt.client as mqtt
import json
from dronLink.Dron import Dron

# esta función sirve para publicar los eventos resultantes de las acciones solicitadas
def publish_event (event):
    global sending_topic, client
    client.publish(sending_topic + '/'+event)


def publish_telemetry_info (telemetry_info):
    # cuando reciba datos de telemetría los publico
    global sending_topic, client
    client.publish(sending_topic + '/telemetryInfo', json.dumps(telemetry_info))

def on_message(cli, userdata, message):
    global  sending_topic, client
    global dron
    # el mensaje que se recibe tiene este formato:
    #    "origen"/autopilotServiceDemo/"command"
    # tengo que averiguar el origen y el command
    splited = message.topic.split("/")
    origin = splited[0] # aqui tengo el nombre de la aplicación que origina la petición
    command = splited[2] # aqui tengo el comando

    sending_topic = "autopilotServiceDemo/" + origin # lo necesitaré para enviar las respuestas

    if command == 'connect':
        connection_string = 'tcp:127.0.0.1:5763'
        baud = 115200
        dron.connect(connection_string, baud, freq=10)
        publish_event('connected')

    if command == 'arm_takeOff':
        if dron.state == 'connected':
            print ('vamos a armar')
            dron.arm()
            print ('vamos a despegar')
            dron.takeOff(5, blocking=False, callback=publish_event, params='flying')

    if command == 'go':
        if dron.state == 'flying':
            payload = message.payload.decode("utf-8")
            # aceptar formatos: "Direction" o "Direction|Speed"
            try:
                if '|' in payload:
                    parts = payload.split('|')
                    direction = parts[0]
                    try:
                        speed = float(parts[1])
                        # aplicar velocidad solicitada
                        try:
                            dron.changeNavSpeed(speed)
                        except Exception as e:
                            print('go: error aplicando changeNavSpeed:', e)
                    except Exception:
                        # si no es número, ignoramos speed
                        direction = payload
                else:
                    direction = payload
                # ejecutar navegación
                dron.go(direction)
            except Exception as e:
                print('Error procesando go payload:', payload, e)

    # mínimo: manejar changeHeading publicado por la UI
    if command == 'changeHeading':
        try:
            payload = message.payload.decode("utf-8")
            if payload is None or payload == '':
                print('changeHeading: payload vacío')
            else:
                deg = float(payload) % 360
                if dron.state == 'flying':
                    # si disponemos de heading actual, giramos por el lado más corto usando rotate
                    try:
                        current = dron.heading
                        if current is None:
                            # fallback: usar cambio absoluto
                            dron.changeHeading(deg, blocking=False)
                            print(f'changeHeading (fallback absoluto) solicitado: {deg}°')
                        else:
                            # normalizamos y calculamos delta en [-180,180]
                            cur = float(current) % 360
                            delta = (deg - cur + 360) % 360
                            if delta > 180:
                                # giro más corto en ccw
                                offset = 360 - delta
                                direction = 'ccw'
                            else:
                                offset = delta
                                direction = 'cw'
                            # si el offset es muy pequeño, no hacer nada
                            if offset < 1.0:
                                print(f'changeHeading: ya cerca de {deg}° (actual {cur}°), offset {offset}°')
                            else:
                                dron.rotate(offset, direction=direction, blocking=False)
                                print(f'rotate solicitado: {offset}° {direction} para llegar a {deg}° (actual {cur}°)')
                    except Exception as e:
                        print('Error intentando rotate, fallback a changeHeading:', e)
                        try:
                            dron.changeHeading(deg, blocking=False)
                        except Exception as e2:
                            print('Fallback changeHeading también falló:', e2)
                else:
                    print('changeHeading ignorado: dron no en estado flying')
        except Exception as e:
            print('Error procesando changeHeading:', e)

    # manejo mínimo de cambio de velocidad por MQTT
    if command == 'changeNavSpeed':
        try:
            payload = message.payload.decode('utf-8')
            if payload is None or payload == '':
                print('changeNavSpeed: payload vacío')
            else:
                try:
                    speed = float(payload)
                except Exception:
                    print('changeNavSpeed: payload no numérico:', payload)
                    speed = None
                if speed is not None:
                    print(f'AutopilotService: aplicar changeNavSpeed = {speed} m/s')
                    try:
                        dron.changeNavSpeed(speed)
                    except Exception as e:
                        print('Error aplicando changeNavSpeed en dron:', e)
        except Exception as e:
            print('Error procesando changeNavSpeed:', e)

    if command == 'Land':
        if dron.state == 'flying':
            # operación no bloqueante. Cuando acabe publicará el evento correspondiente
            dron.Land(blocking=False, callback=publish_event, params='landed')

    if command == 'RTL':
        if dron.state == 'flying':
            # operación no bloqueante. Cuando acabe publicará el evento correspondiente
            dron.RTL(blocking=False, callback=publish_event, params='atHome')

    if command == 'startTelemetry':
        # indico qué función va a procesar los datos de telemetría cuando se reciban
        dron.send_telemetry_info(publish_telemetry_info)

    if command == 'stopTelemetry':
        dron.stop_sending_telemetry_info()


def on_connect(client, userdata, flags, rc):
    global connected
    if rc==0:
        print("connected OK Returned code=",rc)
        connected = True
    else:
        print("Bad connection Returned code=",rc)


dron = Dron()

client = mqtt.Client("autopilotServiceDemo", transport="websockets")

# me conecto al broker publico y gratuito
broker_address = "broker.hivemq.com"
broker_port = 8000

client.on_message = on_message
client.on_connect = on_connect
client.connect (broker_address,broker_port)

# me subscribo a todos los mensajes cuyo destino sea este servicio
client.subscribe('+/autopilotServiceDemo/#')
print ('AutopilotServiceDemo esperando peticiones')
client.loop_forever()
