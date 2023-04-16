import sys
sys.path.append('../')

import gi
gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import GObject, Gst, GstRtspServer
from common.bus_call import bus_call

GObject.threads_init()
Gst.init(None)

pipeline = Gst.Pipeline()
camerasrc = Gst.ElementFactory.make("nvarguscamerasrc", "nv-arguscamerasrc")
caps = Gst.ElementFactory.make("capsfilter", "filter")
caps.set_property("caps", Gst.Caps.from_string("video/x-raw(memory:NVMM),width=(int)1280,height=(int)720,format=(string)NV12,framerate=(fraction)30/1"))

# Create nvstreammux instance to form batches from one or more sources.
streammux = Gst.ElementFactory.make("nvstreammux", "Stream-muxer")
streammux.set_property('width', 1280)
streammux.set_property('height', 720)
streammux.set_property('batch-size', 1)
streammux.set_property('batched-push-timeout', 4000000)
# Use nvinfer to run inferencing on decoder's output,
# behaviour of inferencing is set through config file
pgie = Gst.ElementFactory.make("nvinfer", "primary-inference")
pgie.set_property('config-file-path', "dstest1_pgie_config.txt")
# Use convertor to convert from NV12 to RGBA as required by nvosd
nvvidconv = Gst.ElementFactory.make("nvvideoconvert", "convertor")
# Create OSD to draw on the converted RGBA buffer
nvosd = Gst.ElementFactory.make("nvdsosd", "onscreendisplay")
nvvidconv_postosd = Gst.ElementFactory.make("nvvideoconvert", "convertor_postosd")
# Create a caps filter
caps_postosd = Gst.ElementFactory.make("capsfilter", "caps_postosd_filter")
caps_postosd.set_property("caps", Gst.Caps.from_string("video/x-raw(memory:NVMM), format=I420"))

encoder = Gst.ElementFactory.make("nvv4l2h264enc", "encoder")
h264parse = Gst.ElementFactory.make("h264parse", "h264parse")
rtppay = Gst.ElementFactory.make("rtph264pay", "rtppay")
sink = Gst.ElementFactory.make("udpsink", "udpsink")
camerasrc.set_property('bufapi-version', 1)
encoder.set_property('preset-level', 1)
encoder.set_property('insert-sps-pps', 1)
encoder.set_property('bufapi-version', 1)
rtppay.set_property("pt", 96)
sink.set_property('host', '192.168.8.121')  # server IP
sink.set_property('port', 5004)
sink.set_property('async', False)
sink.set_property('sync', 1)

pipeline.add(camerasrc)
pipeline.add(caps)

pipeline.add(streammux)
pipeline.add(pgie)
pipeline.add(nvvidconv)
pipeline.add(nvosd)
pipeline.add(nvvidconv_postosd)
pipeline.add(caps_postosd)

pipeline.add(encoder)
pipeline.add(h264parse)
pipeline.add(rtppay)
pipeline.add(sink)

sinkpad = streammux.get_request_pad("sink_0")
srcpad = caps.get_static_pad("src")

camerasrc .link(caps)
srcpad.link(sinkpad)
streammux.link(pgie)

pgie.link(nvvidconv)
nvvidconv.link(nvosd)
nvosd.link(nvvidconv_postosd)
nvvidconv_postosd.link(caps_postosd)

caps_postosd.link(encoder)
encoder.link(h264parse)
h264parse.link(rtppay)
rtppay.link(sink)

server = GstRtspServer.RTSPServer.new()
server.props.service = "%d" % 8554
server.attach(None)
factory = GstRtspServer.RTSPMediaFactory.new()
factory.set_launch(
    "( udpsrc name=pay0 port=%d buffer-size=524288 caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=(string)H264, payload=96 \" )" % (
    5004))
factory.set_shared(True)
server.get_mount_points().add_factory("/live", factory)

loop = GObject.MainLoop()
bus = pipeline.get_bus()
bus.add_signal_watch()
bus.connect("message", bus_call, loop)
pipeline.set_state(Gst.State.PLAYING)
print("rtsp://192.168.8.115:8554/live")
try:
    loop.run()
except:
    pass
pipeline.set_state(Gst.State.NULL)

