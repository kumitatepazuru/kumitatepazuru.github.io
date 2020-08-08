#!/bin/bash

if [ $# -ne 1 ]; then
  echo "指定された引数は$#個です。" 1>&2
  echo "実行するには1個の引数が必要です。" 1>&2
  exit 1
fi

INPUT=$1"/src/model.*.hdf5"
OUTPUT=$1"/bin/"
echo INPUT $INPUT
echo OUTPUT $OUTPUT

tensorflowjs_converter --input_format keras $INPUT $OUTPUT
