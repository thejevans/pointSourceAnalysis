#!/bin/bash
for f in ../new_point_source_data/*.h5
do
  echo "Converting $f..."
  python ./convertH5_GFU.py -i $f -o ../converted_point_source_data/
  echo "done."
  echo -n "Moving $f..."
  mv $f ../converted_point_source_data/hdf5/
  echo "done."
done
echo "all files converted."
