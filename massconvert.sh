i=0
for fi in levels/*.cdt; do
    python main.py "$fi" >> strlvl
    i=$((i+1))
done
