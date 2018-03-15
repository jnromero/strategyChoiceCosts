import subprocess
proc = subprocess.Popen(["afinfo output.m4a"], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

start=out.find("estimated duration")
start=out.find(":",start)
start=out.find(" ",start)
end=out.find("sec",start)
duration=float(out[start:end])

print duration