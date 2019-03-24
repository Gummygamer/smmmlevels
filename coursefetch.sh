#! /bin/bash
for d in $1/*; do
  if [ -d "$d" ]; then
    cp -v $d/course_data.cdt ${d##*/}-course_data.cdt
    cp -v $d/course_data_sub.cdt ${d##*/}-course_data_sub.cdt
  fi
done
#find ./ -name '*.cdt' -exec cp '{}' ./ \;
