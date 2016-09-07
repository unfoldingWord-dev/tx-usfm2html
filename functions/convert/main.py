# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

import os
import tempfile
import zipfile
from glob import glob

from contextlib import closing
from future.moves.urllib.request import urlopen
import shutil

import boto3
from general_tools.file_utils import unzip

from convert import convert


def handle(event, context):
    data = retrieve(event, "data", "payload")
    job = retrieve(data, "job", "\"data\"")
    # source: URL of zip archive of input USFM files
    source = retrieve(job, "source", "\"job\"")
    cdn_bucket = retrieve(data, "cdn_bucket", "\"data\"")
    cdn_file = retrieve(data, "cdn_file", "\"data\"")

    print('source: ' + source)
    print('cdn_bucket: ' + cdn_bucket)
    print('cdn_file: ' + cdn_file)

    directory = tempfile.gettempdir()

    # download  and unzip the archive (source)
    basename = os.path.basename(source)
    downloaded_file = os.path.join(directory, basename)
    download_file(source, downloaded_file)
    unzip(downloaded_file, directory)

    inputs = glob(os.path.join(directory, '*.usfm'))
    outputs = convert(inputs, output_dir=directory)

    zip_file = os.path.join(tempfile.gettempdir(), context.aws_request_id+'.zip')
    with zipfile.ZipFile(zip_file, "w") as zf:
        for filename in outputs:
            zf.write(filename, os.path.basename(filename))

    print("Uploading {0} to {1}/{2}".format(zip_file, cdn_bucket, cdn_file))
    boto3.client('s3').upload_file(zip_file, cdn_bucket, cdn_file)

    return {
        'success': True,
    }


def download_file(url, outfile):
    """
    Downloads a file from url and saves it to outfile.
    """
    print("Downloading {}".format(url))
    with closing(urlopen(url)) as request:
        with open(outfile, 'wb') as fp:
            shutil.copyfileobj(request, fp)


def retrieve(dictionary, key, dict_name=None):
    """
    Retrieves a value from a dictionary, raising an error message if the
    specified key is not valid
    :param dict dictionary:
    :param key:
    :param str|unicode dict_name: name of dictionary, for error message
    :return: value corresponding to key
    """
    if key in dictionary:
        return dictionary[key]
    dict_name = "dictionary" if dict_name is None else dict_name
    raise Exception("{k} not found in {d}".format(k=repr(key), d=dict_name))
