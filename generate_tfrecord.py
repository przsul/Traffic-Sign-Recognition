"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=images/train_labels.csv --image_dir=images/train --output_path=train.record

  # Create test data:
  python generate_tfrecord.py --csv_input=images/test_labels.csv  --image_dir=images/test --output_path=test.record
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import pandas as pd
import tensorflow as tf

from PIL import Image
from object_detection.utils import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('image_dir', '', 'Path to the image directory')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
FLAGS = flags.FLAGS


# TO-DO replace this with label map
def class_text_to_int(row_label):
    if row_label == 'D40':
        return 1
    elif row_label == 'B43_30':
        return 2
    elif row_label == 'A17':
        return 3
    elif row_label == 'C5':
        return 4
    elif row_label == 'A12a':
        return 5
    elif row_label == 'B1':
        return 6
    elif row_label == 'B33_60':
        return 7
    elif row_label == 'A1':
        return 8
    elif row_label == 'A14':
        return 9
    elif row_label == 'A7':
        return 10
    elif row_label == 'C2':
        return 11
    elif row_label == 'B20':
        return 12
    elif row_label == 'B33_70':
        return 13
    elif row_label == 'D2':
        return 14
    elif row_label == 'A5':
        return 15
    elif row_label == 'B33_50':
        return 16
    elif row_label == 'B33_20':
        return 17
    elif row_label == 'A20':
        return 18
    elif row_label == 'A6_D':
        return 19
    elif row_label == 'A15':
        return 20
    elif row_label == 'A6c':
        return 21
    elif row_label == 'A2':
        return 22
    elif row_label == 'C7':
        return 23
    elif row_label == 'C9':
        return 24
    elif row_label == 'D6b':
        return 25
    elif row_label == 'A11a':
        return 26
    elif row_label == 'D42':
        return 27
    elif row_label == 'C8':
        return 28
    elif row_label == 'C10':
        return 29
    elif row_label == 'D10':
        return 30
    elif row_label == 'D8':
        return 31
    elif row_label == 'B33_10':
        return 32
    elif row_label == 'A30':
        return 33
    elif row_label == 'B33_30':
        return 34		
    elif row_label == 'B42':
        return 35		
    elif row_label == 'D1':
        return 36		
    elif row_label == 'B23':
        return 37		
    elif row_label == 'Green':
        return 38		
    elif row_label == 'D52':
        return 39		
    elif row_label == 'D5':
        return 40		
    elif row_label == 'D6':
        return 41		
    elif row_label == 'A6b':
        return 42	
    elif row_label == 'A6a':
        return 43
    elif row_label == 'D18':
        return 44
    elif row_label == 'Red':
        return 45        
    elif row_label == 'D51':
        return 46
    elif row_label == 'A16':
        return 47        
    elif row_label == 'A28':
        return 48
    elif row_label == 'B33_40':
        return 49
    elif row_label == 'B21':
        return 50
    elif row_label == 'A11':
        return 51
    elif row_label == 'A9':
        return 52
    elif row_label == 'B43_20':
        return 53
    elif row_label == 'A6d':
        return 54
    elif row_label == 'C6':
        return 55
    elif row_label == 'B33_120':
        return 56
    elif row_label == 'C12':
        return 57
    elif row_label == 'B2':
        return 58
    elif row_label == 'C4':
        return 59
    elif row_label == 'B5':
        return 60
    elif row_label == 'D43':
        return 61
    elif row_label == 'B41':
        return 62
    elif row_label == 'A32':
        return 63
    elif row_label == 'B16_3_7':
        return 64
    elif row_label == 'A21':
        return 65
    elif row_label == 'D4a':
        return 66                                                                            
    elif row_label == 'B33_80':
        return 67                                    
    elif row_label == 'D41':
        return 68                                    
    elif row_label == 'A18b':
        return 69                                    
    elif row_label == 'A12b':
        return 70                                    
    elif row_label == 'B36':
        return 71                                    
    elif row_label == 'A29':
        return 72                                    
    elif row_label == 'B35':
        return 73                                    
    elif row_label == 'B31':
        return 74                                    
    elif row_label == 'B25':
        return 75                                    
    elif row_label == 'B33_90':
        return 76                                    
    elif row_label == 'D7':
        return 77                                    
    elif row_label == 'A23':
        return 78                                    
    elif row_label == 'B22':
        return 79                                    
    elif row_label == 'A3':
        return 80                                    
    elif row_label == 'A4':
        return 81                                    
    elif row_label == 'D9':
        return 82                                    
    elif row_label == 'A6e':
        return 83                                    
    elif row_label == 'D3':
        return 84		
    else:
        None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example


def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    path = os.path.join(os.getcwd(), FLAGS.image_dir)
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
