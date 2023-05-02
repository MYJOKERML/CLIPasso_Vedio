#!/bin/bash
for file in $(ls $1/target_images/temp_frames);do
	python $1/run_object_sketching.py --target_file "${file}" --num_strokes 20 --mask_object 1 --fix_scale 1 --num_sketches 1 
done
