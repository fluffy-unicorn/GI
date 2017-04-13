
for f in  "colorref/colorref_largeexample_4_1026.grl" "colorref/colorref_largeexample_6_960.grl" "colorref/colorref_smallexample_2_49.grl" "colorref/colorref_smallexample_4_16.grl" "colorref/colorref_smallexample_4_7.grl" "colorref/colorref_smallexample_6_15.grl" "other/cubes3.grl" "other/cubes4.grl" "other/cubes5.grl" "other/products72.grl" "other/torus72.grl" "other/trees36.grl" "other/wheeljoin14.grl"
    do for m in "flat" "degree"
        do for i in `seq 1 10`
            do
            #echo -n $(/usr/bin/time -f"%M" python test_refinement.py "$f" "$m" degree > /dev/null | tr '\n' '\t')
            echo -n "$f","$m",
            python3 test_refinement.py "$f" "biggest" "$m" "fast"
        done
    done    
done


