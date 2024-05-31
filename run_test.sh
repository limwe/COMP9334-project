rm -rf output/*

for i in {0..6}
do
    python3 main.py $i
    python3 cf_output_with_ref.py $i
done
