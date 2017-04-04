for i in `seq 1 5`
do
for f in "other/cubes6.grl" "other/torus144.grl" "other/torus24.grl" "other/trees90.grl"
    do for m in "smallest" "biggest" "random"
        do
            echo -n "$f,$m,"
            python3 test_refinement.py "$f" "$m" "degree"
        done
    done
done
