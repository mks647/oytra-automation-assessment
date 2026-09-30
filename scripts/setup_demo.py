"""Fetch pinned upstream RealWorld API and prepare a disposable SQLite demo."""
import json,os,secrets,subprocess,shutil,sqlite3
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
APP=ROOT/'demo-app'
COMMIT='30b68e1e881462b2f4164ea09ab4c4f5699c7b0b'
def run(args,env=None): subprocess.run(args,cwd=APP if APP.exists() else ROOT,env=env,check=True)
if APP.exists(): raise SystemExit('demo-app already exists. Keep it and use run_demo.py; for a fresh setup rename that folder first.')
subprocess.run(['git','clone','https://github.com/gothinkster/node-express-realworld-example-app.git',str(APP)],check=True)
run(['git','checkout',COMMIT])
(APP/'package.upstream.json').write_text((APP/'package.json').read_text())
package={'name':'realworld-local-qa','version':'1.0.0','private':True,'description':'Local QA runtime for pinned upstream RealWorld API','dependencies':{'@prisma/client':'4.16.2','prisma':'4.16.2','tsx':'4.23.15','bcryptjs':'2.4.3','body-parser':'1.20.3','cors':'2.8.5','express':'4.18.3','express-jwt':'8.4.1','jsonwebtoken':'9.0.2','slugify':'1.6.6','tslib':'2.8.1'},'scripts':{'start':'tsx src/main.ts'}}
(APP/'package.json').write_text(json.dumps(package,indent=2))
# The original lock describes the original Nx toolchain, not this local runtime.
lock=APP/'package-lock.json'
if lock.exists():lock.rename(APP/'package-lock.upstream.json')
schema=APP/'src/prisma/schema.prisma'
schema.write_text(schema.read_text().replace('provider = "postgresql"','provider = "sqlite"'))
sqlite3.connect(APP/'src/prisma/qa.db').close()
config=ROOT/'.env'
if not config.exists():config.write_text('DATABASE_URL=file:./qa.db\nPORT=3000\nJWT_SECRET='+secrets.token_hex(32)+'\n')
env=os.environ.copy();env['DATABASE_URL']='file:./qa.db'
npm=shutil.which('npm.cmd' if os.name=='nt' else 'npm')
if not npm:raise SystemExit('Install Node.js and reopen VS Code first.')
run([npm,'install'],env)
prisma=APP/'node_modules/.bin'/('prisma.cmd' if os.name=='nt' else 'prisma')
run([str(prisma),'generate','--schema=src/prisma/schema.prisma'],env)
run([str(prisma),'db','push','--schema=src/prisma/schema.prisma'],env)
print('Ready. Run: python scripts/run_demo.py')
