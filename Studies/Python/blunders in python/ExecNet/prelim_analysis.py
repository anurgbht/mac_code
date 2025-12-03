import time
import execnet

def multiplier(channel, factor):
    import time
    while not channel.isclosed():
        param = channel.receive()
        time.sleep(3)
        channel.send([param * factor,param * factor])

st = time.time()

gw = execnet.makegateway()
channel = gw.remote_exec(multiplier, factor=10)
for i in range(5):
    channel.send(i)
    result = channel.receive()
    print(result)

gw.exit()

print(time.time()-st)

