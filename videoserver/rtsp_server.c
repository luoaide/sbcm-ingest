#include <stdio.h>
#include <gst/gst.h>
#include <gst/rtsp-server/rtsp-server.h>

// DESIGN
// Should listen for:
//      - multicast groups that are pushing video feeds
//      - clients that are RTSP-pushing to this server

int start_listener() {

}

int new_connection() {
    
    GstElement *element;
    /* create element */
    element = gst_element_factory_make ("fakesrc", "source");
    if (!element) {
        g_print ("Failed to create element of type 'fakesrc'\n");
        return -1;
    }

    // delete the element and free it's memory
    gst_object_unref (GST_OBJECT (element));
}

int initialize_GStreamer() {
    const gchar *nano_str;
    guint major, minor, micro, nano;

    gst_init (NULL, NULL);

    gst_version (&major, &minor, &micro, &nano);

    if (nano == 1) {
        nano_str = "(CVS)";
    } else if (nano == 2) {
        nano_str = "(Prerelease)";
    } else {
        nano_str = "";
    }

    printf ("This program is linked against GStreamer %d.%d.%d %s\n", major, minor, micro, nano_str);
}

static GMainLoop *loop;

static gboolean
my_bus_callback (GstBus * bus, GstMessage * message, gpointer data)
{
  g_print ("Got %s message\n", GST_MESSAGE_TYPE_NAME (message));

  switch (GST_MESSAGE_TYPE (message)) {
    case GST_MESSAGE_ERROR:{
      GError *err;
      gchar *debug;

      gst_message_parse_error (message, &err, &debug);
      g_print ("Error: %s\n", err->message);
      g_error_free (err);
      g_free (debug);

      g_main_loop_quit (loop);
      break;
    }
    case GST_MESSAGE_EOS:
      /* end-of-stream */
      g_main_loop_quit (loop);
      break;
    default:
      /* unhandled message */
      break;
  }

  /* we want to be notified again the next time there is a message
   * on the bus, so returning TRUE (FALSE means we want to stop watching
   * for messages on the bus and our callback should not be called again)
   */
  return TRUE;
}

gint
main (gint argc, gchar * argv[])
{
  GstElement *pipeline;
  GstBus *bus;
  guint bus_watch_id;

  /* init */
  gst_init (&argc, &argv);

  /* create pipeline, add handler */
  pipeline = gst_pipeline_new ("my_pipeline");

  /* adds a watch for new message on our pipeline's message bus to
   * the default GLib main context, which is the main context that our
   * GLib main loop is attached to below
   */
  bus = gst_pipeline_get_bus (GST_PIPELINE (pipeline));
  bus_watch_id = gst_bus_add_watch (bus, my_bus_callback, NULL);
  gst_object_unref (bus);

  /* [...] */

  /* create a mainloop that runs/iterates the default GLib main context
   * (context NULL), in other words: makes the context check if anything
   * it watches for has happened. When a message has been posted on the
   * bus, the default main context will automatically call our
   * my_bus_callback() function to notify us of that message.
   * The main loop will be run until someone calls g_main_loop_quit()
   */
  loop = g_main_loop_new (NULL, FALSE);
  g_main_loop_run (loop);

  /* clean up */
  gst_element_set_state (pipeline, GST_STATE_NULL);
  gst_object_unref (pipeline);
  g_source_remove (bus_watch_id);
  g_main_loop_unref (loop);

  return 0;
}

int main (int argc, char *argv[]) {

    /* initialize the components */
    GMainLoop *loop;
    GstRTSPServer *server;
    GstRTSPMountPoints *mounts;
    GstRTSPMediaFactory *factory;

    loop = g_main_loop_new (NULL, FALSE);
    server = gst_rtsp_server_new ();

    // A GstRTSPMountPoints object maintains a relation between paths and GstRTSPMediaFactory objects. This object is usually given to GstRTSPClient and used to find the media attached to a path.
    mounts = gst_rtsp_server_get_mount_points (server);
    
    factory = gst_rtsp_media_factory_new ();
    /* feed the default src file */
    gst_rtsp_media_factory_set_launch (factory, "( videotestsrc is-live=1 ! x264enc ! rtph264pay name=pay0 pt=96 )");
    gst_rtsp_media_factory_set_shared (factory, TRUE);
    gst_rtsp_mount_points_add_factory (mounts, "/stream", factory);
    g_object_unref (mounts);
    gst_rtsp_server_attach (server, NULL);
    /* show current stream URL to user */
    g_print ("stream ready at rtsp://127.0.0.1:8554/stream\n");
    g_main_loop_run (loop);

    return 0;
}
