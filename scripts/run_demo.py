import os,subprocess,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1];env=os.environ.copy()
for line in (root/'.env').read_text().splitlines():
 if '=' in line and not line.startswith('#'):
  k,v=line.split('=',1);env[k]=v
npm=shutil.which('npm.cmd' if os.name=='nt' else 'npm')
subprocess.run([npm,'start'],cwd=root/'demo-app',env=env,check=True)
