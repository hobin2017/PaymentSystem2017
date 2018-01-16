"""
Initialization of the Machine Learning model;
"""
import cv2
import numpy as np
import tensorflow as tf
from object_detection import visualization_utils_hobin as vis_util_hobin
from object_detection.utils import label_map_util

class Detection1(object):
    """
    It is used for detect products.
    """
    def __init__(self):
        PATH_TO_CKPT = 'D:\\01PythonFile\\Project1\\object_detection\\output_inference_graph.pb\\frozen_inference_graph.pb'
        PATH_TO_LABELS = 'D:\\01PythonFile\\Project1\\object_detection\\output_inference_graph.pb\\pascal_label_map.pbtxt'
        NUM_CLASSES = 25
        # graph
        detection_graph = tf.Graph()
        with detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        # labels
        label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
        categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

        # -----------------------------------------------------------------------------------------------------------
        with detection_graph.as_default():
            self.sess = tf.Session(graph=detection_graph)
            self.image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            self.detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            self.detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            self.detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            self.num_detections = detection_graph.get_tensor_by_name('num_detections:0')



    def work1(self, pic_prepared):
        """
        :param pic_prepared: the picture;
        :return: a list of detected products;
        """
        image_np_expanded = np.expand_dims(pic_prepared, axis=0)

        (boxes, scores, classes, num) = self.sess.run(
            [self.detection_boxes, self.detection_scores, self.detection_classes, self.num_detections],
            feed_dict={self.image_tensor: image_np_expanded})

        img, result = vis_util_hobin.visualize_boxes_and_labels_on_image_array(
            pic_prepared,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            self.category_index,
            use_normalized_coordinates=True,
            line_thickness=3)
        # print(result)
        return result


