import paho.mqtt.client as mqtt
import logging,time
import paho.mqtt.publish as publish
import threading,json

port=1883
clients=[]
threads=[]
cname1="bridge-c1"
cname2="bridge-c2"
bridge_topics=["sig/a","0","both"]
broker1="test.mosquitto.org"
broker2="0.0.0.0"
logging.basicConfig(\
   filename='bridgelog.log',level=logging.INFO)


class MQTTClient(mqtt.Client):
   run_flag=False
   def __init__(self,cname,**kwargs):
      super(MQTTClient, self).__init__(cname,**kwargs)
      self.last_pub_time=time.time()
      self.topic_ack=[]
      self.run_flag=True
      self.submitted_flag=False
      self.subscribe_flag=False
      self.bad_connection_flag=False
      self.bad_count=0
      self.connected_flag=False
      self.connect_flag=False
      self.disconnect_flag=False
      self.disconnect_time=0.0
      self.pub_msg_count=0
      self.pub_flag=False
      self.sub_topic=""
      self.sub_topics=""
      self.sub_qos=0
      self.devices=[]
      self.broker=""
      self.port=1883
      self.keepalive=60
      self.run_forever=False
      self.cname=""
      self.delay=10
      self.retry_time=time.time()

def on_connect(client, userdata, flags, rc):
 
   logging.debug("Connected flags"+str(flags)+"result code "\
   +str(rc)+"client1_id")
   if rc==0:
      
      client.connected_flag=True
      client.bad_connection_flag=False
      if client.sub_topic!="":
         logging.debug("subscribing "+str(client.sub_topic))
         print("subscribing to ",\
               client.sub_topic, "broker ",client.broker)
         topic=client.sub_topic
         client.subscribe(topic,client.sub_qos)
      elif client.sub_topics!="":
         print("subscribing to ",client.sub_topics,"broker ",client.broker)
         client.subscribe(client.sub_topics)

   else:
     print("set bad connection flag")
     client.bad_connection_flag=True
     client.bad_count +=1
     client.connected_flag=False

def on_subscribe(client,userdata,mid,granted_qos):
   logging.debug("in on subscribe callback result "+str(mid))
   client.subscribe_flag=True
   

def on_message(client, userdata, msg):
    topic=msg.topic
    m_decode=str(msg.payload.decode("utf-8","ignore"))
    print("message received from ",client.broker)
    message_routing(client,topic,m_decode)
    print(msg.payload.decode())

def Initialise_clients(cname,mqttclient_log=False,cleansession=True,flags=""):
   print("initialising clients")
   logging.info("initialising clients")
   client= MQTTClient(cname,clean_session=cleansession)
   client.cname=cname
   client.on_connect= on_connect
   client.on_message=on_message
   client.on_subscribe=on_subscribe
   return client


def message_routing(client,topic,msg):
   clientname=client.cname
   print("in filter ",clientname)
   if client.connector=="c1":
      client_c2.publish(topic,msg)
   if client.connector=="c2":
      client_c1.publish(topic,msg)


MQTTClient.run_flag=True
now=time.time()
count=0

if bridge_topics[2]=="both":
   bridge_topic_c1=bridge_topics[0]
   bridge_topic_c2=bridge_topics[0]
   
client_c1 =Initialise_clients(cname1)
client_c1.sub_topic=bridge_topic_c1
client_c1.broker=broker1
client_c1.enable_bridge_mode()
clients.append(client_c1)
client_c2 =Initialise_clients(cname2)
client_c2.broker=broker2
client_c2.enable_bridge_mode()
client_c2.sub_topic=bridge_topic_c2
clients.append(client_c2)
client_c1.connector="c1"
client_c2.connector="c2"

for client in clients:
   logging.info("connecting to broker "+str(client.broker))
   try:
        res=client.connect(client.broker,client.port,client.keepalive)
        client.loop_start()

   except:
        logging.debug("connection failed")
        print("connection failed", client.broker)
        client.bad_count +=1
        client.bad_connection_flag=True
   

try:
   while MQTTClient.run_flag:
      time.sleep(1)
except:
   pass
client_c2.loop_stop()
client_c1.loop_stop()
MQTTClient.run_flag=False
time.sleep(5)
for client in clients:
   client.disconnect()


