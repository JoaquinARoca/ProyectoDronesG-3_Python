import json
import time
import tkinter as tk
from dronLink.Dron import Dron
import paho.mqtt.client as mqtt

def restart ():
    time.sleep (5)

    arm_takeOffBtn['text'] = 'Armar'
    arm_takeOffBtn['fg'] = 'black'
    arm_takeOffBtn['bg'] = 'dark orange'

    landBtn['text'] = 'Aterrizar'
    landBtn['fg'] = 'black'
    landBtn['bg'] = 'dark orange'

    RTLBtn['text'] = 'RTL'
    RTLBtn['fg'] = 'black'
    RTLBtn['bg'] = 'dark orange'

    previousBtn['fg'] = 'black'
    previousBtn['bg'] = 'dark orange'


def showTelemetryInfo (telemetry_info):
    global heading, altitude, groundSpeed, state
    global altShowLbl, headingShowLbl, stateShowLbl
    altShowLbl['text'] = round (telemetry_info['alt'],2)
    headingShowLbl['text'] =  round(telemetry_info['heading'],2)
    stateShowLbl['text'] = telemetry_info['state']


def connect ():
    global dron, speedSldr
    client.publish('interfazGlobal/autopilotServiceDemo/connect')
    # cambiamos el color del boton
    connectBtn['text'] = 'Conectado'
    connectBtn['fg'] = 'white'
    connectBtn['bg'] = 'green'
    # fijamos la velocidad por defecto en el slider
    speedSldr.set(1)


def takeoff ():
    global dron
    client.publish('interfazGlobal/autopilotServiceDemo/arm_takeOff')
    arm_takeOffBtn['text'] = 'Despegando...'
    arm_takeOffBtn['fg'] = 'black'
    arm_takeOffBtn['bg'] = 'yellow'

def land ():
    global dron
    client.publish('interfazGlobal/autopilotServiceDemo/Land')
    landBtn['text'] = 'Aterrizando ...'
    landBtn['fg'] = 'black'
    landBtn['bg'] = 'yellow'

def RTL():
    global dron
    client.publish('interfazGlobal/autopilotServiceDemo/RTL')
    RTLBtn['text'] = 'Retornando ...'
    RTLBtn['fg'] = 'black'
    RTLBtn['bg'] = 'yellow'

def go (direction, btn):
    global dron, previousBtn
    # cambio el color del anterior boton clicado (si lo hay)
    if previousBtn:
        previousBtn['fg'] = 'black'
        previousBtn['bg'] = 'dark orange'

    client.publish('interfazGlobal/autopilotServiceDemo/go', direction)
    # pongo en verde el boton clicado
    btn['fg'] = 'white'
    btn['bg'] = 'green'
    # tomo nota de que este es el último botón clicado
    previousBtn = btn


def startTelem():
    global dron
    client.publish('interfazGlobal/autopilotServiceDemo/startTelemetry')

def stopTelem():
    global dron, altShowLbl, headingShowLbl, stateShowLbl
    client.publish('interfazGlobal/autopilotServiceDemo/stopTelemetry')
    altShowLbl['text'] = ''
    headingShowLbl['text'] = ''
    stateShowLbl['text'] = ''


def changeHeading (event):
    global dron
    global gradesSldr
    heading = gradesSldr.get()
    client.publish('interfazGlobal/autopilotServiceDemo/changeHeading', str(heading))

def changeNavSpeed (event):
    global dron
    global speedSldr
    speed = speedSldr.get()
    client.publish('interfazGlobal/autopilotServiceDemo/changeNavSpeed', str(speed))


def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)


def on_message(client, userdata, message):
    # aqui proceso los eventos que me envía el autopilot service
    # basicamente son las indicaciones de que se han ido completando las operaciones solicitadas
    # lo cual me permite ir cambiando los colores de los botones
    if message.topic == 'autopilotServiceDemo/interfazGlobal/telemetryInfo':
        # la telemetria llega en json
        # la envio a la función que procesa esa información
        telemetry_info = json.loads(message.payload)
        showTelemetryInfo (telemetry_info)
    if message.topic == 'autopilotServiceDemo/interfazGlobal/connected':
        connectBtn['text'] = 'Conectado'
        connectBtn['fg'] = 'white'
        connectBtn['bg'] = 'green'


    if message.topic == 'autopilotServiceDemo/interfazGlobal/flying':
        arm_takeOffBtn['text'] = 'En el aire'
        arm_takeOffBtn['fg'] = 'white'
        arm_takeOffBtn['bg'] = 'green'

    if message.topic == 'autopilotServiceDemo/interfazGlobal/landed':
        landBtn['text'] = 'En tierra'
        landBtn['fg'] = 'white'
        landBtn['bg'] = 'green'
        restart()
    if message.topic == 'autopilotServiceDemo/interfazGlobal/atHome':
        RTLBtn['text'] = 'En tierra'
        RTLBtn['fg'] = 'white'
        RTLBtn['bg'] = 'green'
        restart()


def crear_ventana():
    global dron
    global client
    global  altShowLbl, headingShowLbl,  speedSldr, gradesSldr, stateShowLbl
    global connectBtn, armBtn, arm_takeOffBtn, landBtn, RTLBtn
    global previousBtn # aqui guardaré el ultimo boton de navegación clicado

    client = mqtt.Client("InterfazGlobal", transport="websockets")

    # me conecto al broker publico y gratuito
    broker_address = "broker.hivemq.com"
    broker_port = 8000

    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(broker_address, broker_port)

    # me subscribo a cualquier mensaje  que venga del autopilot service
    client.subscribe('autopilotServiceDemo/interfazGlobal/#')
    client.loop_start()

    dron = Dron()

    previousBtn = None

    ventana = tk.Tk()
    ventana.title("Dashboard con conexión directa")
    # la interfaz tiene 10 filas y dos columnas
    ventana.rowconfigure(0, weight=1)
    ventana.rowconfigure(1, weight=1)
    ventana.rowconfigure(2, weight=1)
    ventana.rowconfigure(3, weight=1)
    ventana.rowconfigure(4, weight=1)
    ventana.rowconfigure(5, weight=1)
    ventana.rowconfigure(6, weight=1)
    ventana.rowconfigure(7, weight=1)
    ventana.rowconfigure(8, weight=1)
    ventana.rowconfigure(9, weight=1)
    ventana.columnconfigure(0, weight=1)
    ventana.columnconfigure(1, weight=1)

    # Disponemos los botones, indicando qué función ejecutar cuando se clica cada uno de ellos
    # Los tres primeros ocupan las dos columnas de la fila en la que se colocan
    connectBtn = tk.Button(ventana, text="Conectar", bg="dark orange", command = connect)
    connectBtn.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)


    arm_takeOffBtn = tk.Button(ventana, text="Despegar", bg="dark orange", command=takeoff)
    arm_takeOffBtn.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Slider para seleccionar el heading
    gradesSldr = tk.Scale(ventana, label="Grados:", resolution=5, from_=0, to=360, tickinterval=45,orient=tk.HORIZONTAL)
    gradesSldr.set(180)
    gradesSldr.grid(row=4, column=0, columnspan=2,padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
    gradesSldr.bind("<ButtonRelease-1>", changeHeading)

    # los dos siguientes también están en la misma fila
    landBtn = tk.Button(ventana, text="aterrizar", bg="dark orange", command=land)
    landBtn.grid(row=5, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    RTLBtn = tk.Button(ventana, text="RTL", bg="dark orange", command=RTL)
    RTLBtn.grid(row=5, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # este es el frame para la navegación. Pequeña matriz de 3 x 3 botones
    navFrame = tk.LabelFrame (ventana, text = "Navegación")
    navFrame.grid(row=6, column=0, columnspan = 2, padx=50, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    navFrame.rowconfigure(0, weight=1)
    navFrame.rowconfigure(1, weight=1)
    navFrame.rowconfigure(2, weight=1)
    navFrame.columnconfigure(0, weight=1)
    navFrame.columnconfigure(1, weight=1)
    navFrame.columnconfigure(2, weight=1)

    # al clicar en cualquiera de los botones se activa la función go a la que se le pasa la dirección
    # en la que hay que navegar y el boton clicado, para que la función le cambie el color
    NWBtn = tk.Button(navFrame, text="NW", bg="dark orange",
                        command= lambda: go("NorthWest", NWBtn))
    NWBtn.grid(row=0, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    NoBtn = tk.Button(navFrame, text="No", bg="dark orange",
                        command= lambda: go("North", NoBtn))
    NoBtn.grid(row=0, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    NEBtn = tk.Button(navFrame, text="NE", bg="dark orange",
                        command= lambda: go("NorthEast", NEBtn))
    NEBtn.grid(row=0, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    WeBtn = tk.Button(navFrame, text="We", bg="dark orange",
                        command=lambda: go("West", WeBtn))
    WeBtn.grid(row=1, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    StopBtn = tk.Button(navFrame, text="St", bg="dark orange",
                        command=lambda: go("Stop", StopBtn))
    StopBtn.grid(row=1, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    EaBtn = tk.Button(navFrame, text="Ea", bg="dark orange",
                        command=lambda: go("East", EaBtn))
    EaBtn.grid(row=1, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)


    SWBtn = tk.Button(navFrame, text="SW", bg="dark orange",
                        #command=lambda: go("SouthWest", SWBtn))
                        command = lambda: go("Down", SWBtn))
    SWBtn.grid(row=2, column=0, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SoBtn = tk.Button(navFrame, text="So", bg="dark orange",
                        command=lambda: go("South", SoBtn))
    SoBtn.grid(row=2, column=1, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)

    SEBtn = tk.Button(navFrame, text="SE", bg="dark orange",
                        #command=lambda: go("SouthEast", SEBtn))
                        command = lambda: go("Up", SEBtn))
    SEBtn.grid(row=2, column=2, padx=2, pady=2, sticky=tk.N + tk.S + tk.E + tk.W)


    # slider para elegir la velocidad de navegación
    speedSldr = tk.Scale(ventana, label="Velocidad (m/s):", resolution=1, from_=0, to=20, tickinterval=5,
                          orient=tk.HORIZONTAL)
    speedSldr.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)
    speedSldr.bind("<ButtonRelease-1>", changeNavSpeed)

    # botones para pedir/parar datos de telemetría
    StartTelemBtn = tk.Button(ventana, text="Empezar a enviar telemetría", bg="dark orange", command=startTelem)
    StartTelemBtn.grid(row=8, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    StopTelemBtn = tk.Button(ventana, text="Parar de enviar telemetría", bg="dark orange", command=stopTelem)
    StopTelemBtn.grid(row=8, column=1, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # Este es el frame para mostrar los datos de telemetría
    # Contiene etiquetas para informar de qué datos son y los valores. Solo nos interesan 3 datos de telemetría
    telemetryFrame = tk.LabelFrame(ventana, text="Telemetría")
    telemetryFrame.grid(row=9, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N + tk.S + tk.E + tk.W)

    telemetryFrame.rowconfigure(0, weight=1)
    telemetryFrame.rowconfigure(1, weight=1)

    telemetryFrame.columnconfigure(0, weight=1)
    telemetryFrame.columnconfigure(1, weight=1)
    telemetryFrame.columnconfigure(2, weight=1)

    # etiquetas informativas
    altLbl = tk.Label(telemetryFrame, text='Altitud')
    altLbl.grid(row=0, column=0,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    headingLbl = tk.Label(telemetryFrame, text='Heading')
    headingLbl.grid(row=0, column=1,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    stateLbl = tk.Label(telemetryFrame, text='Estado')
    stateLbl.grid(row=0, column=2,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    # etiquetas para colocar aqui los datos cuando se reciben
    altShowLbl = tk.Label(telemetryFrame, text='')
    altShowLbl.grid(row=1, column=0, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    headingShowLbl = tk.Label(telemetryFrame, text='',)
    headingShowLbl.grid(row=1, column=1,  padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    stateShowLbl = tk.Label(telemetryFrame, text='', )
    stateShowLbl.grid(row=1, column=2, padx=5, pady=5, sticky=tk.N + tk.S + tk.E + tk.W)

    return ventana


if __name__ == "__main__":
    ventana = crear_ventana()
    ventana.mainloop()