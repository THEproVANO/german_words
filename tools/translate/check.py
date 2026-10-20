"""python3 tools/translate/check.py IN.tsv OUT.csv — проверяет партию перевода."""
import sys
src=[l.split("\t")[0] for l in open(sys.argv[1]) if l.strip()]
out=[l.rstrip("\n").split(";") for l in open(sys.argv[2]) if l.strip()]
err=[]
if len(out)!=len(src): err.append(f"строк {len(out)}, нужно {len(src)}")
for i,(k,o) in enumerate(zip(src,out),1):
    if len(o)!=3: err.append(f"{i}: полей {len(o)}")
    elif o[0]!=k: err.append(f"{i}: ключ {o[0]!r}, нужно {k!r}")
    elif not o[1].strip() or not o[2].strip(): err.append(f"{i}: пусто")
    elif "**" in o[2]: err.append(f"{i}: ** в примере")
print("OK" if not err else "\n".join(err[:20]))
