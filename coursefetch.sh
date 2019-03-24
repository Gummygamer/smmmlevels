#! /bin/bash
for d in $1/*; do
  if [ -d "$d" ]; then
    cp -v $d/course_data.cdt levels/${d##*/}-course_data.cdt
    cp -v $d/course_data_sub.cdt levels/${d##*/}-course_data_sub.cdt
  fi
done
